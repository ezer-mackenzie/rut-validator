from typing import Optional

import pytest
from sqlalchemy.exc import StatementError
from sqlmodel import Field, Session, SQLModel, create_engine, select

from rut_validator.orm.pydantic import RutStr
from rut_validator.orm.sqlmodel import RutField


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rut: RutStr = RutField(unique=True)


def test_sqlmodel_round_trip_normalizes_rut():
    engine = create_engine("sqlite://")
    try:
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            person = Person.model_validate({"rut": "12.345.678-5"})
            assert isinstance(person.rut, RutStr)
            session.add(person)
            session.commit()
            session.refresh(person)

            stored = session.exec(select(Person)).one()
            assert stored.rut == "123456785"
    finally:
        engine.dispose()


def test_sqlmodel_rejects_invalid_rut_when_persisting():
    engine = create_engine("sqlite://")
    try:
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            session.add(Person(rut="invalid"))
            with pytest.raises(StatementError):
                session.commit()
    finally:
        engine.dispose()

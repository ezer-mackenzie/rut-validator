import json

import pytest
from sqlalchemy.exc import StatementError
from sqlmodel import Field, Session, SQLModel, create_engine, select

from rut_validator.integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rut: RutSQLModel = rut_sqlmodel_field(unique=True)


class OptionalPerson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rut: RutSQLModel | None = rut_sqlmodel_field(default=None, nullable=True)


def test_sqlmodel_round_trip_normalizes_rut():
    engine = create_engine("sqlite://")
    try:
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            person = Person.model_validate({"rut": "12.345.678-5"})
            assert isinstance(person.rut, RutSQLModel)
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


def test_sqlmodel_optional_field_and_json_serialization():
    person = OptionalPerson.model_validate({"rut": None})
    valid = Person.model_validate({"rut": "12.345.678-5"})

    assert person.rut is None
    assert json.loads(valid.model_dump_json()) == {
        "id": None,
        "rut": "123456785",
    }

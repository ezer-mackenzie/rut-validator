"""SQLModel integration with validation and normalized database storage."""

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

from rut_validator.pydantic import RutStr
from rut_validator.sqlmodel import RutField


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rut: RutStr = RutField(unique=True, index=True)


engine = create_engine("sqlite://")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    # model_validate executes Pydantic validation before persistence.
    person = Person.model_validate({"rut": "12.345.678-5"})
    session.add(person)
    session.commit()

    stored = session.exec(select(Person)).one()
    print(stored.rut)  # 123456785

engine.dispose()

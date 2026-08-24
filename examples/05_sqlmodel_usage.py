"""SQLModel integration with validation and normalized database storage."""

from typing import Annotated

from sqlmodel import Field, Session, SQLModel, create_engine, select

from rut_validator.integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rut: Annotated[
        RutSQLModel,
        rut_sqlmodel_field(unique=True, index=True),
    ]


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

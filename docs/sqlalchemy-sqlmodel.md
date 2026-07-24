# SQLAlchemy and SQLModel

## SQLAlchemy 2

```bash
pip install "rut-validator[sqlalchemy]"
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from rut_validator.orm.sqlalchemy import RutSQLAlchemy


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    rut: Mapped[str] = mapped_column(RutSQLAlchemy(), unique=True)


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Person(rut="12.345.678-5"))
    session.commit()
```

`RutSQLAlchemy` validates bind parameters and stores `123456785` in a
`VARCHAR(9)`. It also validates database results so corrupt historical data
cannot silently violate the type invariant. Invalid values surface through
SQLAlchemy's `StatementError` with the validation error as its cause.

## SQLModel

```bash
pip install "rut-validator[sqlmodel]"
```

```python
from sqlmodel import Field, SQLModel

from rut_validator.orm.sqlmodel import RutSQLModel, rut_sqlmodel_field


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rut: RutSQLModel = rut_sqlmodel_field(unique=True, index=True)


person = Person.model_validate({"rut": "12.345.678-5"})
assert person.rut == "123456785"
```

!!! important "Models with `table=True`"

    Use `model_validate()` when immediate validation is required. SQLModel may
    skip part of Pydantic validation when table models are constructed
    directly. `RutSQLAlchemy` validates again before persistence.

The database always receives the normalized representation.

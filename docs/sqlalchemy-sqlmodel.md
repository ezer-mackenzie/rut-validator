# SQLAlchemy y SQLModel

## SQLAlchemy 2

```bash
pip install "rut-validator[sqlalchemy]"
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from rut_validator.sqlalchemy import RutType


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    rut: Mapped[str] = mapped_column(RutType(), unique=True)


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Person(rut="12.345.678-5"))
    session.commit()
```

`RutType` valida al enlazar el parámetro y almacena `123456785` en un
`VARCHAR(9)`. Los valores inválidos generan un `StatementError` de SQLAlchemy
cuya causa es el error de validación.

`RutSQLAlchemy` se conserva como alias de compatibilidad.

## SQLModel

```bash
pip install "rut-validator[sqlmodel]"
```

```python
from typing import Optional
from sqlmodel import Field, SQLModel
from rut_validator.pydantic import RutStr
from rut_validator.sqlmodel import RutField


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rut: RutStr = RutField(unique=True, index=True)


person = Person.model_validate({"rut": "12.345.678-5"})
assert person.rut == "123456785"
```

!!! important "Modelos `table=True`"

    Para validar inmediatamente utiliza `model_validate()`. SQLModel puede
    omitir parte de la validación Pydantic al construir directamente modelos de
    tabla. En cualquier caso, `RutType` vuelve a validar antes de persistir.

La base de datos almacena el valor normalizado.

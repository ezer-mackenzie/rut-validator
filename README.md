# rut-validator

[![PyPI version](https://badge.fury.io/py/rut-validator.svg)](https://pypi.org/project/rut-validator/)
[![Python versions](https://img.shields.io/pypi/pyversions/rut-validator.svg)](https://pypi.org/project/rut-validator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/ezer-mackenzie/rut-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/ezer-mackenzie/rut-validator/actions)
[![codecov](https://codecov.io/gh/ezer-mackenzie/rut-validator/graph/badge.svg)](https://codecov.io/gh/ezer-mackenzie/rut-validator)
[![Documentation Status](https://readthedocs.org/projects/rut-validator/badge/?version=latest)](https://rut-validator.readthedocs.io/en/latest/?badge=latest)

Framework-agnostic Chilean RUT validation with optional integrations for
Pydantic, FastAPI, Django, SQLAlchemy, and SQLModel.

## Features

- Strict modulo-11 check digit validation.
- Formatted, hyphenated, and normalized input detection.
- Immutable and hashable `Rut` value object.
- Functional and class-based validation APIs.
- Structured errors with stable machine-readable codes.
- CLI validation, formatting, inspection, and batch processing.
- Normalized persistence through optional ORM adapters.
- Strict ASCII input handling.
- Python 3.10 through 3.14 support.

Validation confirms syntax and the check digit. It does not confirm that a RUT
exists, is active, or belongs to a particular person or organization.
Values shown below are synthetic validation fixtures and must not be interpreted
as identifying real people.

## Installation

Install the standalone API and CLI:

```bash
pip install rut-validator
```

Install only the integrations your application needs:

```bash
pip install "rut-validator[pydantic]"
pip install "rut-validator[fastapi]"
pip install "rut-validator[django]"
pip install "rut-validator[sqlalchemy]"
pip install "rut-validator[sqlmodel]"
pip install "rut-validator[all]"
```

## Basic usage

```python
from rut_validator import calculate_check_digit, validate_rut

rut = validate_rut("20.884.437-7")

assert rut.normalized == "208844377"
assert rut.formatted == "20.884.437-7"
assert rut.hyphenated == "20884437-7"
assert rut.body == 20884437
assert rut.check_digit == "7"
assert calculate_check_digit("20884437") == "7"
```

For boolean-only checks:

```python
from rut_validator import RutValidator

assert RutValidator.is_valid("12.345.678-5")
assert not RutValidator.is_valid("12.345.678-0")
assert not RutValidator.is_valid(None)
```

## Error handling

```python
from rut_validator import RutValidationError, validate_rut

try:
    validate_rut("12.345.678-0")
except RutValidationError as error:
    print(error.code)
    print(error.as_dict())
```

Public error codes are `invalid_value`, `invalid_format`, and
`invalid_check_digit`.

## Pydantic

```python
from pydantic import BaseModel

from rut_validator.orm.pydantic import RutPydantic


class User(BaseModel):
    name: str
    rut: RutPydantic


user = User(name="Ana", rut="12.345.678-5")
assert user.rut == "123456785"
```

## FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

from rut_validator.orm.pydantic import RutPydantic

app = FastAPI()


class Person(BaseModel):
    rut: RutPydantic


@app.post("/people")
def create_person(person: Person) -> Person:
    return person
```

Invalid values produce FastAPI's standard HTTP `422` response, and
`RutPydantic` contributes its pattern and examples to OpenAPI.

## Django

```python
from django.db import models

from rut_validator.orm.django import RutDjango


class Person(models.Model):
    name = models.CharField(max_length=100)
    rut = RutDjango(unique=True)
```

The field accepts formatted input and stores the normalized nine-character
representation.

## SQLAlchemy

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rut_validator.orm.sqlalchemy import RutSQLAlchemy


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    rut: Mapped[str] = mapped_column(RutSQLAlchemy(), unique=True)
```

`RutSQLAlchemy` validates values both before persistence and after database
reads.

## SQLModel

```python
from sqlmodel import Field, SQLModel

from rut_validator.orm.sqlmodel import RutSQLModel, rut_sqlmodel_field


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rut: RutSQLModel = rut_sqlmodel_field(unique=True, index=True)
```

## CLI

```bash
rut-validator validate 12.345.678-5
rut-validator validate 12.345.678-5 --json
rut-validator format 123456785 --format formatted
rut-validator info 12.345.678-5 --detailed
rut-validator batch ruts.txt --output result.jsonl
```

## Documentation

Read the [published documentation](https://rut-validator.readthedocs.io/) or
serve it locally:

```bash
poetry install --all-extras
poetry run mkdocs serve
```

## Examples

- [Standalone validation](examples/01_pure_validation.py)
- [Pydantic](examples/02_pydantic_usage.py)
- [FastAPI](examples/03_fastapi_usage.py)
- [CLI](examples/04_cli_usage.py)
- [SQLModel](examples/05_sqlmodel_usage.py)

## Development

```bash
git clone https://github.com/ezer-mackenzie/rut-validator.git
cd rut-validator
poetry install --all-extras

poetry run pytest --cov=rut_validator
poetry run ruff check src tests examples
poetry run black --check src tests examples
poetry run mypy src/rut_validator
poetry run mkdocs build --strict
poetry build
```

Install the Git hooks with:

```bash
poetry run pre-commit install
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## Security

Report security issues according to [SECURITY.md](SECURITY.md). Do not include
real personal RUT values in public bug reports or test fixtures.

## License

Licensed under the [MIT License](LICENSE).

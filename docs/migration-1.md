# Migración desde versiones 0.x

La API candidata a 1.0 quedó estabilizada en 0.9.0. Los proyectos que utilizaban
versiones tempranas deben actualizar imports y nombres antes de adoptar 1.0.

## Core y validación

```python
from rut_validator import Rut, RutValidator, validate_rut
from rut_validator.core import RutFormat, ValidationResult
from rut_validator.validation import RutFormatter, RutParser, RutPatterns
```

Las rutas antiguas `rut_validator.types`, `rut_validator.core.validator` y
`rut_validator.core.orm` ya no existen.

## Pydantic

```python
from rut_validator.orm.pydantic import RutPydantic
```

Reemplaza `RutStr` por `RutPydantic`.

## Django

```python
from rut_validator.orm.django import RutDjango
```

Reemplaza `RUTField` por `RutDjango`.

## SQLAlchemy

```python
from rut_validator.orm.sqlalchemy import RutSQLAlchemy
```

Reemplaza `RutType` y aliases anteriores por la clase real
`RutSQLAlchemy`.

## SQLModel

```python
from rut_validator.orm.sqlmodel import RutSQLModel, rut_sqlmodel_field
```

```python
class Person(SQLModel, table=True):
    rut: RutSQLModel = rut_sqlmodel_field(unique=True)
```

## Errores

No compares mensajes. Usa códigos y payloads:

```python
try:
    validate_rut(value)
except RutValidationError as error:
    payload = error.as_dict()
    code = error.code
```

## Contrato congelado

A partir de `1.0.0rc1` sólo se corregirán bugs. No se renombrarán símbolos ni
se moverán módulos públicos antes de `1.0.0`.

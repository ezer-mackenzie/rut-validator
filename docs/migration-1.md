# Migración desde versiones 0.x

La API pública quedó estabilizada en 1.0.0. Los proyectos que utilizaban
versiones tempranas deben actualizar imports y nombres al adoptar 1.0.

## Core y validación

```python
from rut_validator import Rut, RutValidator, validate_rut
from rut_validator.core import RutFormat, ValidationResult
from rut_validator.validation import RutFormatter, RutParser, RutPatterns
```

Las rutas antiguas `rut_validator.types`, `rut_validator.core.validator` y
`rut_validator.core.orm` ya no existen.

`ValidatedRut` era exactamente el mismo objeto que `Rut` y fue eliminado antes
de estabilizar 1.0. Usa directamente:

```python
from rut_validator import Rut
```

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

## Contrato estable

A partir de `1.0.0`, los cambios incompatibles requieren una nueva versión
mayor. Los símbolos obsoletos seguirán la política de deprecación publicada.

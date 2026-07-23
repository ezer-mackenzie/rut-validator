# rut-validator

`rut-validator` valida RUT chilenos, detecta su formato de entrada y entrega
representaciones canónicas. El core es pequeño y puede utilizarse sin instalar
frameworks web u ORMs.

```python
from rut_validator import validate_rut

rut = validate_rut("12.345.678-5")

assert rut.normalized == "123456785"
assert rut.formatted == "12.345.678-5"
assert rut.hyphenated == "12345678-5"
```

## Características

- Validación módulo 11.
- Entradas con puntos, con guion o normalizadas.
- Value object `Rut` inmutable y hashable.
- API funcional y API basada en `RutValidator`.
- CLI para validación, formato y procesamiento batch.
- Extras opcionales para Pydantic, FastAPI, Django, SQLAlchemy y SQLModel.
- Normalización consistente antes de persistir.

!!! warning "Alcance de la validación"

    La validación confirma estructura y dígito verificador. No comprueba que el
    RUT exista, esté activo o pertenezca a una persona determinada.

## Siguiente paso

Empieza con [Instalación y primeros pasos](getting-started.md) o consulta
directamente la [Referencia de API](api-reference.md).

# rut-validator

`rut-validator` validates Chilean RUT values, detects their input format, and
provides canonical representations. Its standalone API does not import web
frameworks or ORM packages.

```python
from rut_validator import validate_rut

rut = validate_rut("12.345.678-5")

assert rut.normalized == "123456785"
assert rut.formatted == "12.345.678-5"
assert rut.hyphenated == "12345678-5"
```

## Features

- Strict modulo-11 validation.
- Formatted, hyphenated, and normalized input.
- Immutable and hashable `Rut` value object.
- Small functional validation API.
- CLI validation, formatting, inspection, and batch processing.
- Optional Pydantic, FastAPI, Django, SQLAlchemy, and SQLModel integrations.
- Consistent normalization before persistence.
- Structured errors with stable machine-readable codes.

!!! warning "Validation scope"

    Validation confirms syntax and the check digit. It does not confirm that a
    RUT exists, is active, or belongs to a particular person or organization.

Continue with [Getting started](getting-started.md), or go directly to the
[API reference](api-reference.md).

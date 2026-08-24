# API reference

## Root package

### `validate_rut(value)`

Validates an input and returns `Rut`. It raises a `RutValidationError` subclass
when validation fails.

### `calculate_check_digit(body)`

Calculates the modulo-11 check digit for an ASCII-only numeric body.

### `is_valid_rut(value)`

Returns a boolean without raising a validation exception.

### `get_validation_result(value)`

Returns the detailed `ValidationResult` without raising a validation exception.

### `Rut`

Immutable value object with `normalized`, `formatted`, and `hyphenated`
canonical representations.

### `RutFormat`

- `FORMATTED`
- `HYPHENATED`
- `NORMALIZED`

### `ValidationResult`

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

## Exceptions

```text
ValueError
└── RutValidationError
    ├── RutInvalidValueError
    ├── RutInvalidFormatError
    └── RutModuleElevenValidationError
```

Every exception has a stable code and can be serialized without parsing its
message:

```python
from rut_validator import RutModuleElevenValidationError, validate_rut

try:
    validate_rut("12.345.678-0")
except RutModuleElevenValidationError as error:
    assert error.code == "invalid_check_digit"
    assert error.expected_check_digit == "5"
    assert error.received_check_digit == "0"
    payload = error.as_dict()
```

Public error codes are `invalid_value`, `invalid_format`, and
`invalid_check_digit`. Error payloads do not include the submitted RUT.

## Optional integrations

| Import | Public symbols |
| --- | --- |
| `rut_validator.integrations.pydantic` | `RutPydantic` |
| `rut_validator.integrations.sqlalchemy` | `RutSQLAlchemy` |
| `rut_validator.integrations.sqlmodel` | `RutSQLModel`, `rut_sqlmodel_field` |
| `rut_validator.integrations.django` | `RutDjango`, `RutDjangoValidator` |

Domain types and their private invariant engine live in `rut_validator.core`.
Framework-independent functions live in `rut_validator.api` and are re-exported
from the package root. Adapters live in `rut_validator.integrations` and consume
those public functions rather than importing the private engine.

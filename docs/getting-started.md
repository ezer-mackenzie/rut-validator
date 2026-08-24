# Getting started

## Requirements

- Python 3.10 through 3.14.
- `pip`, Poetry, or another standards-compliant Python package installer.

## Installation

The base package includes the standalone validation API and CLI:

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

## Validate a RUT

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

## Boolean validation

```python
from rut_validator import is_valid_rut

assert is_valid_rut("12.345.678-5")
assert not is_valid_rut("12.345.678-0")
assert not is_valid_rut(None)
```

Use `is_valid_rut()` when only a boolean is needed. Use `validate_rut()` when the
application needs the validated value or a specific error.

## Handle errors

```python
from rut_validator import RutValidationError, validate_rut

try:
    validate_rut("12.345.678-0")
except RutValidationError as error:
    print(error.code)
    print(error.as_dict())
```

All public validation errors inherit from `RutValidationError`, which inherits
from `ValueError`. Prefer `error.code` and `error.as_dict()` over matching human
readable messages.

## Accepted formats

| Format | Example | Enum |
| --- | --- | --- |
| Formatted | `12.345.678-5` | `RutFormat.FORMATTED` |
| Hyphenated | `12345678-5` | `RutFormat.HYPHENATED` |
| Normalized | `123456785` | `RutFormat.NORMALIZED` |

The validator does not strip whitespace or arbitrary characters. It accepts
ASCII digits (`0-9`) only and rejects visually similar Unicode digits.

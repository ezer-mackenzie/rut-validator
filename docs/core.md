# Core API and value objects

## `Rut`

`Rut` is an immutable validated value object. Equality and hashing use its
normalized representation.

```python
from rut_validator import Rut

left = Rut("12.345.678-5")
right = Rut("123456785")

assert left == right
assert hash(left) == hash(right)
assert str(left) == "12.345.678-5"
```

### Canonical properties

- `value`: original input.
- `format`: detected `RutFormat`.
- `normalized`: body and check digit without separators.
- `formatted`: thousands separators and a hyphen.
- `hyphenated`: a hyphen without thousands separators.
- `body`: numeric body as `int`; use `normalized` when textual leading zeros
  must be preserved.
- `check_digit`: check digit as `str`.
- `is_formatted`, `is_hyphenated`, `is_normalized`: input format indicators.

## Functional validation

```python
from rut_validator import ValidationResult, get_validation_result, validate_rut

result = get_validation_result("12.345.678-5")
assert result is ValidationResult.VALID

rut = validate_rut("12.345.678-5")
assert rut.body == 12345678
```

`get_validation_result()` returns one of:

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

Application code should use `validate_rut()` or `is_valid_rut()` when it needs a
validation guarantee, then read the canonical properties from `Rut`.

## Privacy

A RUT is personal data. The library does not log complete submitted values
during validation, and `repr(rut)` redacts the submitted value. Applications
remain responsible for access control, retention, encryption, observability,
and audit policies. Values in this documentation are synthetic validation
fixtures and must not be interpreted as identifying real people.

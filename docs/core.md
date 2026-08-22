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
- `body`: numeric body as `int`.
- `check_digit`: check digit as `str`.
- `is_formatted`, `is_hyphenated`, `is_normalized`: input format indicators.

## `RutValidator`

```python
from rut_validator import RutValidator, ValidationResult

result = RutValidator.get_validation_result("12.345.678-5")
assert result is ValidationResult.VALID

rut = RutValidator.validate("12.345.678-5")
assert rut.body == 12345678
```

`get_validation_result()` returns one of:

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

## `RutFormatter`

The formatter validates before converting:

```python
from rut_validator.validation import RutFormatter

assert RutFormatter.to_original_format("123456785") == "12.345.678-5"
assert RutFormatter.to_normalize_format("12.345.678-5") == "123456785"
assert RutFormatter.to_hyphenated_format("123456785") == "12345678-5"
```

## Low-level parsing and pattern helpers

`RutParser` and `RutPatterns` are public compatibility APIs for inspecting
syntax and implementing specialized tooling. They are low-level primitives:
methods such as `RutPatterns.normalize()` only transform characters and do not
prove that the input is valid.

Application code should use `validate_rut()`, `RutValidator` or `RutFormatter`
when it needs a validation guarantee. The low-level names will remain available
throughout the `1.x` series; any future removal will follow the deprecation
policy.

## Privacy

A RUT is personal data. The library does not log complete submitted values
during validation, and `repr(rut)` redacts the submitted value. Applications
remain responsible for access control, retention, encryption, observability,
and audit policies. Values in this documentation are synthetic validation
fixtures and must not be interpreted as identifying real people.

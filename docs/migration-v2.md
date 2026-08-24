# Migrating from 1.x to 2.0

Version 2 removes the compatibility wrappers deprecated in 1.1. Update these
imports and calls before changing the package version.

## Validation functions

Replace the stateless `RutValidator` class with functions exported from the
package root:

| Deprecated 1.x API | Canonical API |
| --- | --- |
| `RutValidator.validate(value)` | `validate_rut(value)` |
| `RutValidator.is_valid(value)` | `is_valid_rut(value)` |
| `RutValidator.get_validation_result(value)` | `get_validation_result(value)` |
| `RutValidator.module_eleven(body)` | `calculate_check_digit(body)` |

```python
from rut_validator import get_validation_result, is_valid_rut, validate_rut

rut = validate_rut("12.345.678-5")
assert is_valid_rut("12.345.678-5")
result = get_validation_result("12.345.678-5")
```

`RutValidator.is_valid_check_digit()` has no public version 2 equivalent.
Applications should normally validate the complete RUT with `validate_rut()` or
`is_valid_rut()`.

## Formatting

Replace `RutFormatter` with properties of the validated value:

| Deprecated 1.x API | Canonical API |
| --- | --- |
| `RutFormatter.to_original_format(value)` | `validate_rut(value).formatted` |
| `RutFormatter.to_normalize_format(value)` | `validate_rut(value).normalized` |
| `RutFormatter.to_hyphenated_format(value)` | `validate_rut(value).hyphenated` |

The canonical API always validates before transforming input.

## Low-level parsing and patterns

`RutParser` and `RutPatterns` were removed. They exposed implementation
details and permitted transformations without a complete validation guarantee.
Use `validate_rut()` and read `body`, `check_digit`, `format`, or `normalized`
from the resulting `Rut`.

Regular expressions and cleaning patterns are no longer public API. This
allows the parser implementation to evolve without breaking consumers.

## `Rut` aliases

| Deprecated property or method | Canonical replacement |
| --- | --- |
| `rut.number` | `rut.body` |
| `rut.digit` | `rut.check_digit` |
| `rut.is_dotted` | `rut.is_formatted` |
| `rut.is_numeric` | `rut.is_normalized` |
| `rut.equals(other)` | `rut == other` |

Construct `Rut` with only its input value. The `format_detected` argument was
removed:

```python
from rut_validator import Rut

rut = Rut("12.345.678-5")
```

## Integration imports

Move imports from `rut_validator.orm` to `rut_validator.integrations`:

| Deprecated import | Canonical import |
| --- | --- |
| `rut_validator.orm.pydantic` | `rut_validator.integrations.pydantic` |
| `rut_validator.orm.django` | `rut_validator.integrations.django` |
| `rut_validator.orm.sqlalchemy` | `rut_validator.integrations.sqlalchemy` |
| `rut_validator.orm.sqlmodel` | `rut_validator.integrations.sqlmodel` |

The class and helper names do not change. Rewrite old Django migrations that
refer to `rut_validator.orm.django.RutDjango` before uninstalling 1.x, because
the compatibility module is not present in version 2.

## CLI

Remove `--quiet` from `rut-validator format` calls. The option was a no-op
because the command already prints only the converted value.

## Testing the migration

Run tests with deprecations converted to errors to find remaining legacy calls:

```bash
python -W error::DeprecationWarning -m pytest
```

After migrating, remove direct imports of `rut_validator.validation` and
`rut_validator.orm`; neither package exists in version 2.

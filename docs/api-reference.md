# Referencia de API

## Paquete principal

### `validate_rut(value)`

Valida una entrada y devuelve `Rut`. Lanza una subclase de
`RutValidationError` si falla.

### `calculate_check_digit(body)`

Calcula el DV módulo 11 para un cuerpo ASCII compuesto sólo por dígitos.

### `RutValidator`

- `validate(value) -> Rut`
- `is_valid(value) -> bool`
- `get_validation_result(value) -> ValidationResult`
- `module_eleven(body) -> str`
- `is_valid_check_digit(body, check_digit) -> bool`

### `Rut`

Value object inmutable. Sus representaciones canónicas son `normalized`,
`formatted` y `hyphenated`.

### `RutFormat`

- `FORMATTED`
- `HYPHENATED`
- `NORMALIZED`

### `ValidationResult`

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

## Excepciones

```text
ValueError
└── RutValidationError
    ├── RutInvalidValueError
    ├── RutInvalidFormatError
    └── RutModuleElevenValidationError
```

Todas las excepciones incluyen un código estable y pueden serializarse sin
analizar el mensaje:

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

Los códigos públicos son `invalid_value`, `invalid_format` e
`invalid_check_digit`. Los payloads no incluyen el RUT recibido.

## Integraciones opcionales

| Import | Símbolos |
| --- | --- |
| `rut_validator.orm.pydantic` | `RutPydantic` |
| `rut_validator.orm.sqlalchemy` | `RutSQLAlchemy` |
| `rut_validator.orm.sqlmodel` | `RutSQLModel`, `rut_sqlmodel_field` |
| `rut_validator.orm.django` | `RutDjango`, `RutDjangoValidator` |

Los tipos de dominio están en `rut_validator.core`; la implementación agnóstica
está en `rut_validator.validation`; los adapters viven únicamente en
`rut_validator.orm`.

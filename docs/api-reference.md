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

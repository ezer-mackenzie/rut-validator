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
| `rut_validator.pydantic` | `RutStr` |
| `rut_validator.sqlalchemy` | `RutType`, `RutSQLAlchemy` |
| `rut_validator.sqlmodel` | `RutField`, `RutStr` |
| `rut_validator.django` | `RUTField`, `RutDjangoValidator` |

Las rutas históricas bajo `rut_validator.core.orm` continúan disponibles por
compatibilidad, pero no deben utilizarse en código nuevo.

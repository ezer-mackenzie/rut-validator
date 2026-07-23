# Core y value object

## `Rut`

`Rut` representa un valor validado. Es inmutable, puede utilizarse como clave de
diccionario y compara por su representación normalizada.

```python
from rut_validator import Rut

left = Rut("12.345.678-5")
right = Rut("123456785")

assert left == right
assert hash(left) == hash(right)
assert str(left) == "12.345.678-5"
```

### Propiedades canónicas

- `value`: entrada original.
- `format`: formato detectado.
- `normalized`: dígitos y DV, sin separadores.
- `formatted`: puntos y guion.
- `hyphenated`: sólo guion.
- `body`: cuerpo numérico como `int`.
- `check_digit`: dígito verificador como `str`.
- `is_formatted`, `is_hyphenated`, `is_normalized`: indicadores del formato de entrada.

`number`, `digit`, `is_dotted` e `is_numeric` existen como alias de
compatibilidad. Para código nuevo utiliza los nombres canónicos.

## `RutValidator`

```python
from rut_validator import RutValidator, ValidationResult

result = RutValidator.get_validation_result("12.345.678-5")
assert result is ValidationResult.VALID

rut = RutValidator.validate("12.345.678-5")
assert rut.body == 12345678
```

Resultados posibles:

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

## `RutFormatter`

El formatter público primero valida y después convierte:

```python
from rut_validator.validation import RutFormatter

assert RutFormatter.to_original_format("123456785") == "12.345.678-5"
assert RutFormatter.to_normalize_format("12.345.678-5") == "123456785"
assert RutFormatter.to_hyphenated_format("123456785") == "12345678-5"
```

## Privacidad

Un RUT es un dato personal. La librería no registra el valor completo durante
la validación, pero la aplicación consumidora debe aplicar sus propias políticas
de acceso, retención, cifrado y auditoría.

# Instalación y primeros pasos

## Requisitos

- Python 3.10 o superior.
- `pip`, Poetry u otro instalador compatible con paquetes Python.

## Instalación

El paquete base incluye el core y el CLI:

```bash
pip install rut-validator
```

Las integraciones se instalan mediante extras:

```bash
pip install "rut-validator[pydantic]"
pip install "rut-validator[fastapi]"
pip install "rut-validator[django]"
pip install "rut-validator[sqlalchemy]"
pip install "rut-validator[sqlmodel]"
pip install "rut-validator[all]"
```

## Validación funcional

```python
from rut_validator import calculate_check_digit, validate_rut

rut = validate_rut("20.884.437-7")

print(rut.normalized)   # 208844377
print(rut.formatted)    # 20.884.437-7
print(rut.hyphenated)   # 20884437-7
print(rut.body)         # 20884437
print(rut.check_digit)  # 7

assert calculate_check_digit("20884437") == "7"
```

## Comprobar sin excepciones

```python
from rut_validator import RutValidator

assert RutValidator.is_valid("12.345.678-5")
assert not RutValidator.is_valid("12.345.678-0")
assert not RutValidator.is_valid(None)
```

`is_valid()` siempre devuelve un booleano para entradas proporcionadas por el
usuario. Usa `validate_rut()` cuando necesites conocer la causa de un error.

## Manejo de errores

```python
from rut_validator import (
    RutInvalidFormatError,
    RutModuleElevenValidationError,
    validate_rut,
)

try:
    validate_rut("12.345.678-0")
except RutInvalidFormatError:
    print("La estructura no es válida")
except RutModuleElevenValidationError:
    print("El dígito verificador no coincide")
```

Todos los errores públicos heredan de `RutValidationError`, que a su vez hereda
de `ValueError`.

Para APIs y logs estructurados utiliza `error.code` o `error.as_dict()` en vez
de comparar el mensaje traducible.

## Formatos aceptados

| Formato | Ejemplo | Enum |
| --- | --- | --- |
| Con puntos y guion | `12.345.678-5` | `RutFormat.FORMATTED` |
| Sólo con guion | `12345678-5` | `RutFormat.HYPHENATED` |
| Normalizado | `123456785` | `RutFormat.NORMALIZED` |

No se eliminan espacios ni caracteres arbitrarios durante la validación. Sólo
se aceptan dígitos ASCII (`0-9`); dígitos Unicode visualmente similares se
rechazan.

# Django

```bash
pip install "rut-validator[django]"
```

## Modelo

```python
from django.db import models
from rut_validator.orm.django import RutDjango


class Person(models.Model):
    name = models.CharField(max_length=100)
    rut = RutDjango(unique=True)
```

`RutDjango`:

- usa una longitud de almacenamiento de 9 caracteres;
- normaliza antes de preparar el valor para la base de datos;
- admite `None` cuando el campo se configura como nullable;
- expone errores Django con código `invalid_rut`;
- utiliza un validator serializable para migraciones.

## Validación explícita

Django no ejecuta `full_clean()` automáticamente al llamar `save()`. Cuando la
entrada provenga del usuario, utiliza un `ModelForm`, un serializer o llama
explícitamente:

```python
person = Person(rut="12.345.678-5")
person.full_clean()
person.save()
```

Después de la preparación para base de datos el valor canónico es `123456785`.

## Formularios, nulos y blancos

Configura `blank=True` y `null=True` según las reglas de tu aplicación. Un RUT
vacío no es válido por sí mismo; la omisión debe gestionarse como opcionalidad
del campo, no como un RUT especial.

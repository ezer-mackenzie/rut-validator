# Django

```bash
pip install "rut-validator[django]"
```

## Model field

```python
from django.db import models

from rut_validator.orm.django import RutDjango


class Person(models.Model):
    name = models.CharField(max_length=100)
    rut = RutDjango(unique=True)
```

`RutDjango`:

- stores a maximum of nine normalized characters;
- accepts up to twelve formatted characters in forms;
- normalizes values before preparing database parameters;
- supports `None` when configured with `null=True`;
- reports Django validation errors with code `invalid_rut`;
- uses a deconstructible validator suitable for migrations.

## Explicit validation

Django does not call `full_clean()` automatically from `save()`. For
user-provided values, use a `ModelForm`, a serializer, or call it explicitly:

```python
person = Person(rut="12.345.678-5")
person.full_clean()
person.save()
```

The database representation is `123456785`. A valid `ModelForm` also places the
normalized value on its model instance.

## Optional fields

Use `blank=True` and `null=True` according to the application's data model. An
empty string is not a valid RUT; optionality should be represented by the field
configuration rather than by a special RUT value.

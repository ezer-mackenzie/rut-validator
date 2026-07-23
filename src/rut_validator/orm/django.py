"""Django model field integration."""

from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import deconstructible
from django.db.models import CharField

from ..errors import RutValidationError
from ..validation import RutValidator


@deconstructible
class RutDjangoValidator:
    """Serializable validator suitable for Django migrations."""

    code = "invalid_rut"

    def __call__(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("El RUT debe ser un texto", code=self.code)
        try:
            RutValidator.validate(value)
        except RutValidationError as exc:
            raise ValidationError(str(exc), code=self.code) from exc


class RutDjango(CharField):
    """A Django field that validates and stores normalized RUT strings."""

    description = "RUT chileno normalizado"
    max_input_length = 12

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 9)
        super().__init__(*args, **kwargs)
        self.validators.append(RutDjangoValidator())

    def to_python(self, value: object) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValidationError("El RUT debe ser un texto", code="invalid_rut")
        try:
            return RutValidator.validate(value).normalized
        except RutValidationError as exc:
            raise ValidationError(str(exc), code="invalid_rut") from exc

    def get_prep_value(self, value: object) -> str | None:
        return self.to_python(value)

    def formfield(self, **kwargs: Any) -> Any:
        """Accept formatted input while keeping normalized database storage."""
        kwargs.setdefault("max_length", self.max_input_length)
        return super().formfield(**kwargs)


__all__ = ["RutDjango", "RutDjangoValidator"]

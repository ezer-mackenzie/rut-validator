"""Django model field integration."""

from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.core.validators import deconstructible
from django.db.models import CharField

from rut_validator.errors import RutValidationError
from rut_validator.validation import RutValidator


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


class RUTField(CharField):
    """A Django field that validates and stores normalized RUT strings."""

    description = "RUT chileno normalizado"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 9)
        super().__init__(*args, **kwargs)
        self.validators.append(RutDjangoValidator())

    def to_python(self, value: object) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValidationError("El RUT debe ser un texto", code="invalid_rut")
        try:
            return RutValidator.validate(value).normalized
        except RutValidationError as exc:
            raise ValidationError(str(exc), code="invalid_rut") from exc

    def get_prep_value(self, value: object) -> Optional[str]:
        return self.to_python(value)


__all__ = ["RUTField", "RutDjangoValidator"]

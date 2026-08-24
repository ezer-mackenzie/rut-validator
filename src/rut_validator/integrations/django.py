"""Django model field integration."""

from typing import TYPE_CHECKING, Any, TypeAlias

from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.utils.deconstruct import deconstructible

from ..api import validate_rut
from ..errors import RutValidationError

if TYPE_CHECKING:
    RutDjangoBase: TypeAlias = CharField[str]
else:
    RutDjangoBase: TypeAlias = CharField


@deconstructible
class RutDjangoValidator:
    """Serializable validator suitable for Django migrations."""

    code = "invalid_rut"

    def __call__(self, value: object) -> None:
        """Raise Django's ``ValidationError`` when *value* is not a valid RUT."""
        if not isinstance(value, str):
            raise ValidationError("El RUT debe ser un texto", code=self.code)
        try:
            validate_rut(value)
        except RutValidationError as exc:
            raise ValidationError(str(exc), code=self.code) from exc


class RutDjango(RutDjangoBase):
    """A Django field that validates and stores normalized RUT strings."""

    description = "RUT chileno normalizado"
    max_input_length = 12

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 9)
        super().__init__(*args, **kwargs)
        self.validators.append(RutDjangoValidator())

    def to_python(self, value: object) -> str | None:
        """Convert a supported value to normalized RUT text."""
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValidationError("El RUT debe ser un texto", code="invalid_rut")
        try:
            return validate_rut(value).normalized
        except RutValidationError as exc:
            raise ValidationError(str(exc), code="invalid_rut") from exc

    def get_prep_value(self, value: object) -> str | None:
        """Prepare normalized RUT text for database persistence."""
        return self.to_python(value)

    def formfield(self, **kwargs: Any) -> Any:
        """Accept formatted input while keeping normalized database storage."""
        kwargs.setdefault("max_length", self.max_input_length)
        return super().formfield(**kwargs)


__all__ = ["RutDjango", "RutDjangoValidator"]

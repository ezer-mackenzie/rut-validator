from django.db.models import CharField
from django.core.exceptions import ValidationError

from typing import Any

from ...validator import RutValidator
from ....errors import (
    RutInvalidValueError,
    RutInvalidFormatError,
    RutModuleElevenValidationError,
)


class RUTField(CharField):
    description = "A field to store Chilean RUT (Rol Único Tributario) numbers."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault(
            "max_length", 12
        )  # RUT can be up to 12 characters including formatting
        super().__init__(*args, **kwargs)

        # After initializing the field, we can set up any additional attributes or validators if needed.
        # For example, we could add a validator that uses the RutValidator from the core module

        def validator(value: Any) -> None:
            """
            Custom validator that uses the RutValidator to validate the RUT value.

            Args:
                value (Any): The value to validate as a RUT.

            Raises:
                ValidationError: If the value is not a valid RUT.
            """

            try:
                if value is None:
                    raise ValueError("RUT value cannot be None.")

                RutValidator.validate(str(value))

            except (
                RutInvalidValueError,
                RutInvalidFormatError,
                RutModuleElevenValidationError,
            ) as e:
                raise ValidationError(str(f"Invalid RUT value: {e}"))

        self.validators.append(validator)

    def to_python(self, value: object | None) -> str | None:
        """
        Convert the input value to a Python string and validate it as a RUT.

        Args:
            value (object | None): The value to convert and validate.

        Returns:
            str | None: The validated RUT string or None if the input was None.
        """

        self.ensure_type(value)

        if value is None:
            return None

        try:
            return RutValidator.validate(str(value)).normalized
        except Exception as e:
            raise ValidationError(str(e))

    def get_prep_value(self, value: object | None) -> str | None:
        return self.to_python(value)

    def ensure_type(self, value: object | None) -> str | None:

        # If the value is None, we can return it directly (or we could choose to return an empty string if we prefer).
        if value is None:
            return value

        # If the value is already a string, we can return it directly.
        if not isinstance(value, str):
            raise ValidationError("RUT value must be a string.")

        return str(value)

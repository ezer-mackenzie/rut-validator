"""Custom exceptions for RUT validation."""

from typing import Any


class RutValidationError(ValueError):
    """Base exception carrying a stable machine-readable error code."""

    code = "rut_validation_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable error payload."""
        return {"code": self.code, "message": self.message}


class RutInvalidValueError(RutValidationError):
    """Indicate that a required RUT value is missing or has the wrong type."""

    code = "invalid_value"


class RutInvalidFormatError(RutValidationError):
    """Indicate that text does not use a supported RUT representation."""

    code = "invalid_format"


class RutModuleElevenValidationError(RutValidationError):
    """Indicate that a RUT has an incorrect modulo-11 check digit."""

    code = "invalid_check_digit"

    def __init__(self, expected: str, received: str) -> None:
        self.expected_check_digit = expected
        self.received_check_digit = received
        super().__init__(
            "El dígito verificador no coincide, "
            f"se esperaba '{expected}' en vez de '{received}'"
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON payload containing expected and received digits."""
        payload = super().as_dict()
        payload.update(
            {
                "expected_check_digit": self.expected_check_digit,
                "received_check_digit": self.received_check_digit,
            }
        )
        return payload

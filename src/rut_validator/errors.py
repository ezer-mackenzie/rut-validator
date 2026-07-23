"""Custom exceptions for RUT validation."""

from typing import Any


class RutValidationError(ValueError):
    """Base exception carrying a stable machine-readable error code."""

    code = "rut_validation_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def as_dict(self) -> dict[str, Any]:
        """Return a serialization safe for APIs and command-line JSON."""
        return {"code": self.code, "message": self.message}


class RutInvalidValueError(RutValidationError):
    """Raised when the RUT value is empty or invalid."""

    code = "invalid_value"


class RutInvalidFormatError(RutValidationError):
    """Raised when the RUT format is invalid."""

    code = "invalid_format"


class RutModuleElevenValidationError(RutValidationError):
    """Raised when the RUT fails the modulo 11 validation."""

    code = "invalid_check_digit"

    def __init__(self, expected: str, received: str) -> None:
        self.expected_check_digit = expected
        self.received_check_digit = received
        super().__init__(
            "El dígito verificador no coincide, "
            f"se esperaba '{expected}' en vez de '{received}'"
        )

    def as_dict(self) -> dict[str, Any]:
        payload = super().as_dict()
        payload.update(
            {
                "expected_check_digit": self.expected_check_digit,
                "received_check_digit": self.received_check_digit,
            }
        )
        return payload

"""Custom exceptions for RUT validation."""


class RutValidationError(ValueError):
    """Base exception for all RUT validation errors."""

    pass


class RutInvalidValueError(RutValidationError):
    """Raised when the RUT value is empty or invalid."""

    pass


class RutInvalidFormatError(RutValidationError):
    """Raised when the RUT format is invalid."""

    pass


class RutModuleElevenValidationError(RutValidationError):
    """Raised when the RUT fails the modulo 11 validation."""

    pass

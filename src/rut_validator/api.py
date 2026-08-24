"""Public framework-independent RUT operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .core import engine
from .core.enums import ValidationResult
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)

if TYPE_CHECKING:
    from .core.rut import Rut


def calculate_check_digit(body: str) -> str:
    """Calculate the modulo-11 check digit for an ASCII numeric body.

    Raises:
        RutInvalidValueError: If *body* contains anything other than ASCII
            digits.
    """
    return engine.module_eleven(body)


def validate_rut(value: object) -> Rut:
    """Validate *value* and return its immutable RUT representation.

    Raises:
        RutInvalidValueError: If *value* is missing or not text.
        RutInvalidFormatError: If *value* uses an unsupported representation.
        RutModuleElevenValidationError: If its check digit is incorrect.
    """
    from .core.rut import Rut

    return Rut(cast(str, value))


def get_validation_result(value: object) -> ValidationResult:
    """Classify *value* without raising a validation exception."""
    try:
        engine.validate(value)
    except RutInvalidValueError:
        return ValidationResult.INVALID_VALUE
    except RutInvalidFormatError:
        return ValidationResult.INVALID_FORMAT
    except RutModuleElevenValidationError:
        return ValidationResult.INVALID_CHECK_DIGIT

    return ValidationResult.VALID


def is_valid_rut(value: object) -> bool:
    """Return whether *value* is a valid RUT."""
    return get_validation_result(value) is ValidationResult.VALID


__all__ = [
    "calculate_check_digit",
    "get_validation_result",
    "is_valid_rut",
    "validate_rut",
]

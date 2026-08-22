"""Validate and represent Chilean RUT values."""

from importlib.metadata import PackageNotFoundError, version

from .core import Rut, RutFormat, ValidationResult
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
    RutValidationError,
)
from .validation import RutValidator, calculate_check_digit, validate_rut

try:
    __version__ = version("rut-validator")
except PackageNotFoundError:  # pragma: no cover - source tree without install
    __version__ = "0+unknown"


__all__ = [
    "Rut",
    "RutFormat",
    "RutInvalidFormatError",
    "RutInvalidValueError",
    "RutModuleElevenValidationError",
    "RutValidationError",
    "RutValidator",
    "ValidationResult",
    "calculate_check_digit",
    "validate_rut",
]

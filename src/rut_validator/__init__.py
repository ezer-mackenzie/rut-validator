"""Validate and represent Chilean RUT values."""

from importlib.metadata import PackageNotFoundError, version

from .api import (
    calculate_check_digit,
    get_validation_result,
    is_valid_rut,
    validate_rut,
)
from .core import Rut, RutFormat, ValidationResult
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
    RutValidationError,
)

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
    "ValidationResult",
    "calculate_check_digit",
    "get_validation_result",
    "is_valid_rut",
    "validate_rut",
]

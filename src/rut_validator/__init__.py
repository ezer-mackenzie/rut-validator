"""
rut-validator: Validation of Chilean RUTs for Pydantic and FastAPI
"""

from importlib.metadata import PackageNotFoundError, version

from .core import Rut, RutFormat, ValidationResult
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
    RutValidationError,
)
from .validation import RutValidator, calculate_check_digit, validate_rut

ValidatedRut = Rut
try:
    __version__ = version("rut-validator")
except PackageNotFoundError:  # pragma: no cover - source tree without install
    __version__ = "0+unknown"
__all__ = [
    "Rut",
    "RutFormat",  # Format enumeration
    "RutInvalidFormatError",  # Custom exception
    "RutInvalidValueError",  # Custom exception
    "RutModuleElevenValidationError",  # Custom exception
    "RutValidationError",  # Base exception
    "RutValidator",  # For pure validation
    "ValidatedRut",  # Validation result (alias for Rut)
    "ValidationResult",
    "calculate_check_digit",
    "validate_rut",
]

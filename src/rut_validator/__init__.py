"""
rut-validator: Validation of Chilean RUTs for Pydantic and FastAPI
"""

from importlib.metadata import PackageNotFoundError, version
from warnings import warn

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


def __getattr__(name: str) -> object:
    if name == "ValidatedRut":
        warn(
            "ValidatedRut está obsoleto; usa Rut. "
            "El alias se eliminará en rut-validator 2.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return Rut
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Rut",
    "RutFormat",  # Format enumeration
    "RutInvalidFormatError",  # Custom exception
    "RutInvalidValueError",  # Custom exception
    "RutModuleElevenValidationError",  # Custom exception
    "RutValidationError",  # Base exception
    "RutValidator",  # For pure validation
    "ValidationResult",
    "calculate_check_digit",
    "validate_rut",
]

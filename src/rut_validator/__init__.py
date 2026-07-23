"""
rut-validator: Validation of Chilean RUTs for Pydantic and FastAPI
"""

from importlib.metadata import PackageNotFoundError, version
from typing import Any

from .core.validator import RutValidator, calculate_check_digit, validate_rut
from .core.patterns import RutFormat
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
    RutValidationError,
)
from .types.enums import ValidationResult
from .types.rut import Rut

ValidatedRut = Rut
try:
    __version__ = version("rut-validator")
except PackageNotFoundError:  # pragma: no cover - source tree without install
    __version__ = "0+unknown"
__all__ = [
    "RutValidator",  # For pure validation
    "Rut",
    "ValidatedRut",  # Validation result (alias for Rut)
    "RutStr",  # For use with Pydantic
    "RutFormat",  # Format enumeration
    "ValidationResult",
    "calculate_check_digit",
    "validate_rut",
    "RutInvalidFormatError",  # Custom exception
    "RutInvalidValueError",  # Custom exception
    "RutModuleElevenValidationError",  # Custom exception
    "RutValidationError",  # Base exception
]


def __getattr__(name: str) -> Any:
    """Load optional integrations only when they are requested."""
    if name == "RutStr":
        try:
            from .orm.pydantic import RutStr
        except ImportError as exc:
            raise ImportError(
                "RutStr requiere Pydantic. Instálelo con "
                "`pip install rut-validator[pydantic]`."
            ) from exc
        return RutStr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

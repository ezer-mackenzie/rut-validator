"""
rut-validator: Validation of Chilean RUTs for Pydantic and FastAPI
"""

from typing import Any

from .core.validator import RutValidator
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
__version__ = "0.2.0"
__all__ = [
    "RutValidator",  # For pure validation
    "Rut",
    "ValidatedRut",  # Validation result (alias for Rut)
    "RutStr",  # For use with Pydantic
    "RutFormat",  # Format enumeration
    "ValidationResult",
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

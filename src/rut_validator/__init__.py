"""
rut-validator: Validation of Chilean RUTs for Pydantic and FastAPI
"""

from .core.validator import RutValidator
from .core.patterns import RutFormat
from .core.orm.pydantic.schema import RutStr
from .errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
    RutValidationError,
)
from .types.rut import Rut as ValidatedRut

__version__ = "0.1.0"
__all__ = [
    "RutValidator",  # For pure validation
    "ValidatedRut",  # Validation result (alias for Rut)
    "RutStr",  # For use with Pydantic
    "RutFormat",  # Format enumeration
    "RutInvalidFormatError",  # Custom exception
    "RutInvalidValueError",  # Custom exception
    "RutModuleElevenValidationError",  # Custom exception
    "RutValidationError",  # Base exception
]

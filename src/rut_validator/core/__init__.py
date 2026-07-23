"""Framework-independent domain types."""

from .enums import RutFormat, ValidationResult
from .rut import Rut

__all__ = [
    "Rut",
    "RutFormat",
    "ValidationResult",
]

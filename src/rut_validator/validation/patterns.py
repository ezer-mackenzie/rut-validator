"""RUT pattern definitions and format detection."""

from ..core import engine
from ..core.enums import RutFormat


class RutPatterns:
    """Low-level regex and transformation helpers.

    Transformation methods do not validate the check digit. Application code
    needing a validation guarantee should use ``validate_rut``.
    """

    # Individual patterns for format detection
    FORMATTED_PATTERN = engine.FORMATTED_PATTERN
    HYPHENATED_PATTERN = engine.HYPHENATED_PATTERN
    NORMALIZED_PATTERN = engine.NORMALIZED_PATTERN

    # Combined pattern for general validation
    VALIDATION_PATTERN = engine.VALIDATION_PATTERN

    # Maximum supported length for a formatted RUT string.
    MAX_RUT_LENGTH = engine.MAX_RUT_LENGTH

    # Cleaning pattern (removes dots, hyphens, keeps digits and K/k)
    CLEANING_PATTERN = engine.CLEANING_PATTERN

    @classmethod
    def detect_format(cls, rut: str) -> RutFormat | None:
        """Detect the representation used by *rut*, if supported."""
        return engine.detect_format(rut)

    @classmethod
    def is_valid_format(cls, rut: str) -> bool:
        """Check whether *rut* uses a supported representation."""
        if len(rut) > cls.MAX_RUT_LENGTH:
            return False

        return cls.VALIDATION_PATTERN.fullmatch(rut) is not None

    @classmethod
    def normalize(cls, rut: str) -> str:
        """Remove separators from *rut* and uppercase its check digit."""
        return engine.normalize(rut)

    @classmethod
    def formatted(cls, rut: str) -> str:
        """Format *rut* with thousands separators and a hyphen."""
        return engine.format_normalized(cls.normalize(rut))

    @classmethod
    def hyphenated(cls, rut: str) -> str:
        """Format *rut* with a hyphen before its check digit."""
        return engine.hyphenate_normalized(cls.normalize(rut))

    @classmethod
    def normalized(cls, rut: str) -> str:
        """Remove separators from *rut*."""
        return cls.normalize(rut)

"""RUT pattern definitions and format detection."""

from .. import _engine
from ..core.enums import RutFormat


class RutPatterns:
    """Low-level regex and transformation helpers.

    Transformation methods do not validate the check digit. Application code
    needing a validation guarantee should use ``RutValidator`` or
    ``RutFormatter``.
    """

    # Individual patterns for format detection
    FORMATTED_PATTERN = _engine.FORMATTED_PATTERN
    HYPHENATED_PATTERN = _engine.HYPHENATED_PATTERN
    NORMALIZED_PATTERN = _engine.NORMALIZED_PATTERN

    # Combined pattern for general validation
    VALIDATION_PATTERN = _engine.VALIDATION_PATTERN

    # Maximum supported length for a formatted RUT string.
    MAX_RUT_LENGTH = 15

    # Cleaning pattern (removes dots, hyphens, keeps digits and K/k)
    CLEANING_PATTERN = _engine.CLEANING_PATTERN

    @classmethod
    def detect_format(cls, rut: str) -> RutFormat | None:
        """
        Detect the format of a RUT string.

        Args:
            rut: The RUT string to analyze.

        Returns:
            RutFormat if the format is recognized, None otherwise.
        """
        format_name = _engine.detect_format(rut)
        return RutFormat(format_name) if format_name is not None else None

    @classmethod
    def is_valid_format(cls, rut: str) -> bool:
        """
        Check if a RUT string has a valid format (any supported format).

        Args:
            rut: The RUT string to validate.

        Returns:
            True if the format is valid, False otherwise.
        """
        if len(rut) > cls.MAX_RUT_LENGTH:
            return False

        return cls.VALIDATION_PATTERN.fullmatch(rut) is not None

    @classmethod
    def normalize(cls, rut: str) -> str:
        """
        Normalize a RUT string by removing formatting characters.

        Args:
            rut: The RUT string to normalize.

        Returns:
            The normalized RUT string (digits + check digit, uppercased).
        """
        return _engine.normalize(rut)

    @classmethod
    def formatted(cls, rut: str) -> str:
        """
        Format a RUT string with dots and hyphen.

        Args:
            rut: The RUT string to format (any supported RUT format).

        Returns:
            The formatted RUT string (e.g., "12.345.678-5").
        """
        return _engine.format_normalized(cls.normalize(rut))

    @classmethod
    def hyphenated(cls, rut: str) -> str:
        """
        Format a RUT string with hyphen only (hyphenated format).

        Args:
            rut: The RUT string to format (any supported RUT format).

        Returns:
            The hyphenated RUT string (e.g., "12345678-5").
        """
        return _engine.hyphenate_normalized(cls.normalize(rut))

    @classmethod
    def normalized(cls, rut: str) -> str:
        """
        Return the normalized RUT string without formatting.

        Args:
            rut: The RUT string to normalize (any supported RUT format).

        Returns:
            The normalized RUT string (e.g., "123456785").
        """
        return cls.normalize(rut)

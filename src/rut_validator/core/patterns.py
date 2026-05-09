"""RUT pattern definitions and format detection."""

from re import compile
from typing import Optional

from rut_validator.types.enums import RutFormat


class RutPatterns:
    """Collection of regex patterns for RUT validation and format detection."""

    # Individual patterns for format detection
    FORMATTED_PATTERN = compile(r"^\d{1,2}(?:\.\d{3}){2}-[\dkK]$")
    HYPHENATED_PATTERN = compile(r"^\d{7,8}-[\dkK]$")
    NORMALIZED_PATTERN = compile(r"^\d{7,8}[\dkK]$")

    # Combined pattern for general validation
    VALIDATION_PATTERN = compile(
        r"^(?:\d{1,2}(?:\.\d{3}){2}-[\dkK]|\d{7,8}-[\dkK]|\d{7,8}[\dkK])$"
    )

    # Maximum supported length for a formatted RUT string.
    MAX_RUT_LENGTH = 15

    # Cleaning pattern (removes dots, hyphens, keeps digits and K/k)
    CLEANING_PATTERN = compile(r"[^0-9kK]")

    @classmethod
    def detect_format(cls, rut: str) -> Optional[RutFormat]:
        """
        Detect the format of a RUT string.

        Args:
            rut: The RUT string to analyze.

        Returns:
            RutFormat if the format is recognized, None otherwise.
        """
        if cls.FORMATTED_PATTERN.match(rut):
            return RutFormat.FORMATTED
        
        elif cls.HYPHENATED_PATTERN.match(rut):
            return RutFormat.HYPHENATED
        
        elif cls.NORMALIZED_PATTERN.match(rut):
            return RutFormat.NORMALIZED
        
        return None

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
        
        return cls.VALIDATION_PATTERN.match(rut) is not None

    @classmethod
    def normalize(cls, rut: str) -> str:
        """
        Normalize a RUT string by removing formatting characters.

        Args:
            rut: The RUT string to normalize.

        Returns:
            The normalized RUT string (digits + check digit, uppercased).
        """
        return cls.CLEANING_PATTERN.sub("", rut).upper()

    @classmethod
    def formatted(cls, rut: str) -> str:
        """
        Format a RUT string with dots and hyphen.

        Args:
            rut: The RUT string to format (any supported RUT format).

        Returns:
            The formatted RUT string (e.g., "12.345.678-5").
        """
        normalized_rut = cls.normalize(rut)
        body = normalized_rut[:-1]
        check_digit = normalized_rut[-1]
        body_formatted = f"{int(body):,}".replace(",", ".")
        return f"{body_formatted}-{check_digit}"

    @classmethod
    def hyphenated(cls, rut: str) -> str:
        """
        Format a RUT string with hyphen only (hyphenated format).

        Args:
            rut: The RUT string to format (any supported RUT format).

        Returns:
            The hyphenated RUT string (e.g., "12345678-5").
        """
        normalized_rut = cls.normalize(rut)
        body = normalized_rut[:-1]
        check_digit = normalized_rut[-1]
        return f"{body}-{check_digit}"

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
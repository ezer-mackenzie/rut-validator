"""Validated conversions between supported RUT representations."""

from .validator import validate_rut


class RutFormatter:
    """Convert valid RUT text to canonical representations."""

    @staticmethod
    def to_original_format(rut: str) -> str:
        """Validate and format *rut* with dots and a hyphen."""
        return validate_rut(rut).formatted

    @staticmethod
    def to_normalize_format(rut: str) -> str:
        """Validate and remove separators from *rut*."""
        return validate_rut(rut).normalized

    @staticmethod
    def to_hyphenated_format(rut: str) -> str:
        """Validate and format *rut* with only a hyphen."""
        return validate_rut(rut).hyphenated

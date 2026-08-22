"""Validated conversions between supported RUT representations."""

from .validator import RutValidator


class RutFormatter:
    """Convert valid RUT text to canonical representations."""

    @staticmethod
    def to_original_format(rut: str) -> str:
        """Validate and format *rut* with dots and a hyphen."""
        return RutValidator.validate(rut).formatted

    @staticmethod
    def to_normalize_format(rut: str) -> str:
        """Validate and remove separators from *rut*."""
        return RutValidator.validate(rut).normalized

    @staticmethod
    def to_hyphenated_format(rut: str) -> str:
        """Validate and format *rut* with only a hyphen."""
        return RutValidator.validate(rut).hyphenated

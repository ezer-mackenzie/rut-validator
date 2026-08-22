"""Validated conversions between supported RUT representations."""

from .validator import RutValidator


class RutFormatter:
    """Convert valid RUT text to canonical representations."""

    @staticmethod
    def to_original_format(rut: str) -> str:
        """Validate *rut* and return its dotted canonical representation."""
        return RutValidator.validate(rut).formatted

    @staticmethod
    def to_normalize_format(rut: str) -> str:
        """Validate *rut* and return its separator-free canonical form."""
        return RutValidator.validate(rut).normalized

    @staticmethod
    def to_hyphenated_format(rut: str) -> str:
        """Validate *rut* and return its canonical hyphenated representation."""
        return RutValidator.validate(rut).hyphenated

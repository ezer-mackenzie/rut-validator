from enum import Enum


class RutFormat(Enum):
    """Enumeration of supported RUT formats."""

    FORMATTED = "formatted"  # 12.345.678-9
    HYPHENATED = "hyphenated"  # 12345678-9
    NORMALIZED = "normalized"  # 123456789


class ValidationResult(Enum):
    """Result states for RUT validation."""

    VALID = "valid"
    INVALID_VALUE = "invalid_value"
    INVALID_FORMAT = "invalid_format"
    INVALID_CHECK_DIGIT = "invalid_check_digit"

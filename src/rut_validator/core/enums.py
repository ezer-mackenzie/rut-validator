"""Enumerations used by the RUT domain and validation APIs."""

from enum import Enum


class RutFormat(Enum):
    """Supported input representations of a RUT."""

    FORMATTED = "formatted"  # 12.345.678-9
    HYPHENATED = "hyphenated"  # 12345678-9
    NORMALIZED = "normalized"  # 123456789


class ValidationResult(Enum):
    """Possible outcomes of non-raising validation."""

    VALID = "valid"
    INVALID_VALUE = "invalid_value"
    INVALID_FORMAT = "invalid_format"
    INVALID_CHECK_DIGIT = "invalid_check_digit"

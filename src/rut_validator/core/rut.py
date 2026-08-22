"""Validated RUT value object."""

from dataclasses import dataclass, field

from .. import _engine
from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)
from .enums import RutFormat

_FORMAT_BY_NAME = {
    "formatted": RutFormat.FORMATTED,
    "hyphenated": RutFormat.HYPHENATED,
    "normalized": RutFormat.NORMALIZED,
}


@dataclass(frozen=True, slots=True, init=False, eq=False, repr=False)
class Rut:
    """Immutable, hashable and validated Chilean RUT value object.

    ``value`` preserves the submitted text and ``format`` records its detected
    syntax. Equality and hashing use the canonical normalized representation.
    """

    value: str
    format: RutFormat
    _normalized: str = field(init=False, repr=False)

    def __init__(
        self,
        value: str,
        format_detected: RutFormat | None = None,
    ) -> None:
        if not isinstance(value, str) or value.strip() == "":
            raise RutInvalidValueError("El RUT debe ser un texto no vacío")
        format_name = _engine.detect_format(value)
        if format_name is None:
            raise RutInvalidFormatError(
                "Formato no válido, se esperaba algo como '12345678-9', "
                "'123456789' o '12.345.678-9'"
            )
        detected_format = _FORMAT_BY_NAME[format_name]
        normalized = _engine.normalize(value)
        body, check_digit = normalized[:-1], normalized[-1]
        if format_detected is not None and format_detected != detected_format:
            raise RutInvalidFormatError(
                "El formato indicado no coincide con el formato del RUT"
            )
        object.__setattr__(self, "value", value)
        resolved_format = format_detected or detected_format
        assert resolved_format is not None
        object.__setattr__(self, "format", resolved_format)

        if not _engine.is_valid_check_digit(body, check_digit):
            raise RutModuleElevenValidationError(
                expected=_engine.module_eleven(body),
                received=check_digit,
            )
        object.__setattr__(self, "_normalized", normalized)

    @property
    def normalized(self) -> str:
        """Return body and check digit without separators."""
        return self._normalized

    @property
    def formatted(self) -> str:
        """Return the canonical representation with dots and a hyphen."""
        return _engine.format_normalized(self.normalized)

    @property
    def hyphenated(self) -> str:
        """Return the canonical representation with only a hyphen."""
        return _engine.hyphenate_normalized(self.normalized)

    @property
    def body(self) -> int:
        """Return the numeric body."""
        return int(self.normalized[:-1])

    @property
    def check_digit(self) -> str:
        """Return the check digit."""
        return self.normalized[-1]

    @property
    def number(self) -> int:
        """Backward-compatible alias for :attr:`body`."""
        return self.body

    @property
    def digit(self) -> str:
        """Backward-compatible alias for :attr:`check_digit`."""
        return self.check_digit

    @property
    def is_formatted(self) -> bool:
        """Return whether the input used dots and a hyphen."""
        return self.format == RutFormat.FORMATTED

    @property
    def is_hyphenated(self) -> bool:
        """Return whether the input used only a hyphen."""
        return self.format == RutFormat.HYPHENATED

    @property
    def is_normalized(self) -> bool:
        """Return whether the input contained no separators."""
        return self.format == RutFormat.NORMALIZED

    @property
    def is_dotted(self) -> bool:
        """Backward-compatible alias for :attr:`is_formatted`."""
        return self.is_formatted

    @property
    def is_numeric(self) -> bool:
        """Backward-compatible alias for :attr:`is_normalized`."""
        return self.is_normalized

    def __str__(self) -> str:
        return self.formatted

    def __repr__(self) -> str:
        return f"Rut(value='<redacted>', format={self.format})"

    def equals(self, other: object) -> bool:
        """Return True when two Rut objects represent the same normalized RUT."""
        return self == other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rut):
            return NotImplemented

        return self.normalized == other.normalized

    def __hash__(self) -> int:
        return hash(self.normalized)

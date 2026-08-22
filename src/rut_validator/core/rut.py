"""Validated RUT value object."""

from dataclasses import dataclass, field

from ..errors import RutInvalidFormatError, RutModuleElevenValidationError
from ..validation.parser import RutParser
from ..validation.patterns import RutPatterns
from .enums import RutFormat


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
        body, check_digit, detected_format = RutParser.destructure(value)
        if format_detected is not None and format_detected != detected_format:
            raise RutInvalidFormatError(
                "El formato indicado no coincide con el formato del RUT"
            )
        object.__setattr__(self, "value", value)
        resolved_format = format_detected or detected_format
        assert resolved_format is not None
        object.__setattr__(self, "format", resolved_format)

        from ..validation.validator import RutValidator

        if not RutValidator.is_valid_check_digit(body, check_digit):
            raise RutModuleElevenValidationError(
                expected=RutValidator.module_eleven(body),
                received=check_digit,
            )
        object.__setattr__(self, "_normalized", f"{body}{check_digit.upper()}")

    @property
    def normalized(self) -> str:
        """Return body and check digit without separators."""
        return self._normalized

    @property
    def formatted(self) -> str:
        """Return the canonical representation with dots and a hyphen."""
        return RutPatterns.formatted(self.normalized)

    @property
    def hyphenated(self) -> str:
        """Return the canonical representation with only a hyphen."""
        return RutPatterns.hyphenated(self.normalized)

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

"""Validated RUT value object."""

from dataclasses import InitVar, dataclass, field

from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)
from . import engine
from .enums import RutFormat


def _require_text(value: object) -> str:
    if not isinstance(value, str) or value.strip() == "":
        raise RutInvalidValueError("El RUT debe ser un texto no vacío")
    return value


@dataclass(frozen=True, slots=True, eq=False, repr=False)
class Rut:
    """Immutable, hashable and validated Chilean RUT value object.

    ``value`` preserves the submitted text and ``format`` records its detected
    syntax. Equality and hashing use the canonical normalized representation.
    """

    value: str
    format_detected: InitVar[RutFormat | None] = None
    format: RutFormat = field(init=False)
    _normalized: str = field(init=False, repr=False)

    def __post_init__(self, format_detected: RutFormat | None) -> None:
        value = _require_text(self.value)
        detected_format = engine.detect_format(value)
        if detected_format is None:
            raise RutInvalidFormatError(
                "Formato no válido, se esperaba algo como '12345678-9', "
                "'123456789' o '12.345.678-9'"
            )
        normalized = engine.normalize(value)
        body, check_digit = normalized[:-1], normalized[-1]
        if format_detected is not None and format_detected != detected_format:
            raise RutInvalidFormatError(
                "El formato indicado no coincide con el formato del RUT"
            )
        if not engine.is_valid_check_digit(body, check_digit):
            raise RutModuleElevenValidationError(
                expected=engine.module_eleven(body),
                received=check_digit,
            )
        # This is the supported way to initialize derived fields in a frozen
        # dataclass; regular assignment remains prohibited after construction.
        object.__setattr__(self, "format", detected_format)
        object.__setattr__(self, "_normalized", normalized)

    @property
    def normalized(self) -> str:
        """Body and check digit without separators."""
        return self._normalized

    @property
    def formatted(self) -> str:
        """Canonical representation with dots and a hyphen."""
        return engine.format_normalized(self.normalized)

    @property
    def hyphenated(self) -> str:
        """Canonical representation with only a hyphen."""
        return engine.hyphenate_normalized(self.normalized)

    @property
    def body(self) -> int:
        """Numeric body without the check digit."""
        return int(self.normalized[:-1])

    @property
    def check_digit(self) -> str:
        """Uppercase modulo-11 check digit."""
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
        """Whether the input used dots and a hyphen."""
        return self.format == RutFormat.FORMATTED

    @property
    def is_hyphenated(self) -> bool:
        """Whether the input used only a hyphen."""
        return self.format == RutFormat.HYPHENATED

    @property
    def is_normalized(self) -> bool:
        """Whether the input contained no separators."""
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
        """Compare two RUTs by their normalized representation."""
        return self == other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rut):
            return NotImplemented

        return self.normalized == other.normalized

    def __hash__(self) -> int:
        return hash(self.normalized)

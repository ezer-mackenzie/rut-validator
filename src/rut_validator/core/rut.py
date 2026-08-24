"""Validated RUT value object."""

from dataclasses import dataclass, field

from . import engine
from .enums import RutFormat


@dataclass(frozen=True, slots=True, eq=False, repr=False)
class Rut:
    """Immutable, hashable and validated Chilean RUT value object.

    ``value`` preserves the submitted text and ``format`` records its detected
    syntax. Equality and hashing use the canonical normalized representation.
    """

    value: str
    format: RutFormat = field(init=False)
    _normalized: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        parsed = engine.validate(self.value)
        # This is the supported way to initialize derived fields in a frozen
        # dataclass; regular assignment remains prohibited after construction.
        object.__setattr__(self, "format", parsed.format)
        object.__setattr__(self, "_normalized", parsed.normalized)

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

    def __str__(self) -> str:
        return self.formatted

    def __repr__(self) -> str:
        return f"Rut(value='<redacted>', format={self.format})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rut):
            return NotImplemented

        return self.normalized == other.normalized

    def __hash__(self) -> int:
        return hash(self.normalized)

"""Validated RUT value object."""

from dataclasses import dataclass

from ..errors import RutInvalidFormatError, RutModuleElevenValidationError
from ..validation.parser import RutParser
from ..validation.patterns import RutPatterns
from .enums import RutFormat


@dataclass(frozen=True, slots=True, init=False)
class Rut:
    """
    A class representing a validated RUT (Rol Único Tributario) value object.

    This class encapsulates a validated RUT value and provides properties to access its components,
    such as the body and check digit, as well as formatted and normalized representations.

    The Rut class ensures that the RUT value is valid upon instantiation,
    and it provides methods to retrieve the normalized and formatted versions of the RUT.

    The normalized version is the raw RUT value without any formatting,
    while the formatted version includes thousands separators and a hyphen before the check digit.

    Attributes:
        value (str): The original RUT input string as provided by the caller.
        format (Optional[RutFormat]): The detected format of the input.

    Methods:
        normalized: Returns the normalized RUT value.
        formatted: Returns the formatted RUT value.
        body: Returns the body of the RUT (the numeric part).
        check_digit: Returns the check digit of the RUT.
        is_formatted: Returns True if input was formatted format.
        is_hyphenated: Returns True if input was hyphenated format.
        is_normalized: Returns True if input was normalized format.
    """

    value: str
    format: RutFormat

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

    @property
    def normalized(self) -> str:
        """
        Returns the normalized RUT value.
        """
        return RutPatterns.normalize(self.value)

    @property
    def formatted(self) -> str:
        """
        Returns the formatted RUT value.
        """
        return RutPatterns.formatted(self.normalized)

    @property
    def hyphenated(self) -> str:
        """
        Returns the hyphenated RUT value.
        """
        return RutPatterns.hyphenated(self.normalized)

    @property
    def body(self) -> int:
        """
        Returns the body of the RUT (the numeric part).
        """
        return int(self.normalized[:-1])

    @property
    def check_digit(self) -> str:
        """
        Returns the check digit of the RUT.
        """
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
        """
        Returns True if input was formatted format.
        """
        return self.format == RutFormat.FORMATTED

    @property
    def is_hyphenated(self) -> bool:
        """
        Returns True if input was hyphenated format.
        """
        return self.format == RutFormat.HYPHENATED

    @property
    def is_normalized(self) -> bool:
        """
        Returns True if input was normalized format.
        """
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

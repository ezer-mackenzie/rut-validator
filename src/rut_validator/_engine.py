"""Private, dependency-free primitives shared by domain and validation APIs."""

from re import Pattern, compile
from typing import Final, Literal

from .errors import RutInvalidValueError

FormatName = Literal["formatted", "hyphenated", "normalized"]

FORMATTED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{1,2}(?:\.[0-9]{3}){2}-[0-9kK]")
HYPHENATED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}-[0-9kK]")
NORMALIZED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}[0-9kK]")
VALIDATION_PATTERN: Final[Pattern[str]] = compile(
    r"(?:[0-9]{1,2}(?:\.[0-9]{3}){2}-[0-9kK]" r"|[0-9]{7,8}-[0-9kK]|[0-9]{7,8}[0-9kK])"
)
CLEANING_PATTERN: Final[Pattern[str]] = compile(r"[^0-9kK]")
RUT_MODULE_ELEVEN_FACTORS: Final[tuple[int, ...]] = (2, 3, 4, 5, 6, 7)


def detect_format(value: str) -> FormatName | None:
    """Return the recognized syntax name for *value*, if any."""
    if FORMATTED_PATTERN.fullmatch(value):
        return "formatted"
    if HYPHENATED_PATTERN.fullmatch(value):
        return "hyphenated"
    if NORMALIZED_PATTERN.fullmatch(value):
        return "normalized"
    return None


def normalize(value: str) -> str:
    """Remove RUT separators and uppercase the check digit."""
    return CLEANING_PATTERN.sub("", value).upper()


def format_normalized(value: str) -> str:
    """Format a normalized RUT with dots and a hyphen."""
    body, check_digit = value[:-1], value[-1]
    return f"{int(body):,}".replace(",", ".") + f"-{check_digit}"


def hyphenate_normalized(value: str) -> str:
    """Format a normalized RUT with a hyphen."""
    return f"{value[:-1]}-{value[-1]}"


def module_eleven(body: str) -> str:
    """Calculate the modulo-11 check digit for an ASCII numeric body."""
    if not body.isascii() or not body.isdigit():
        raise RutInvalidValueError("El cuerpo del RUT debe contener sólo dígitos")

    total = sum(
        digit * RUT_MODULE_ELEVEN_FACTORS[index % len(RUT_MODULE_ELEVEN_FACTORS)]
        for index, digit in enumerate(map(int, reversed(body)))
    )
    result = 11 - (total % 11)
    if result == 11:
        return "0"
    if result == 10:
        return "K"
    return str(result)


def is_valid_check_digit(body: object, check_digit: object) -> bool:
    """Return whether two components form a valid modulo-11 RUT."""
    if (
        not isinstance(body, str)
        or not isinstance(check_digit, str)
        or len(check_digit) != 1
        or check_digit not in "0123456789kK"
    ):
        return False
    try:
        expected = module_eleven(body)
    except RutInvalidValueError:
        return False
    return check_digit.upper() == expected

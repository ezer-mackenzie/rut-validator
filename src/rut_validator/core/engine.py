"""Internal primitives shared by the domain object and validation APIs."""

from re import Pattern, compile
from typing import Final

from ..errors import RutInvalidValueError
from .enums import RutFormat

FORMATTED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{1,2}(?:\.[0-9]{3}){2}-[0-9kK]")
HYPHENATED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}-[0-9kK]")
NORMALIZED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}[0-9kK]")
VALIDATION_PATTERN: Final[Pattern[str]] = compile(
    rf"(?:{FORMATTED_PATTERN.pattern}|{HYPHENATED_PATTERN.pattern}"
    rf"|{NORMALIZED_PATTERN.pattern})"
)
CLEANING_PATTERN: Final[Pattern[str]] = compile(r"[^0-9kK]")
MAX_RUT_LENGTH: Final = 12
RUT_MODULE_ELEVEN_FACTORS: Final[tuple[int, ...]] = (2, 3, 4, 5, 6, 7)


def detect_format(value: str) -> RutFormat | None:
    if FORMATTED_PATTERN.fullmatch(value):
        return RutFormat.FORMATTED

    if HYPHENATED_PATTERN.fullmatch(value):
        return RutFormat.HYPHENATED

    if NORMALIZED_PATTERN.fullmatch(value):
        return RutFormat.NORMALIZED

    return None


def normalize(value: str) -> str:
    return CLEANING_PATTERN.sub("", value).upper()


def format_normalized(value: str) -> str:
    body, check_digit = value[:-1], value[-1]
    return f"{int(body):,}".replace(",", ".") + f"-{check_digit}"


def hyphenate_normalized(value: str) -> str:
    return f"{value[:-1]}-{value[-1]}"


def module_eleven(body: str) -> str:
    """Calculate the modulo-11 check digit for an ASCII numeric body.

    Raises:
        RutInvalidValueError: If *body* contains anything other than ASCII
            digits.
    """
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
    """Check a body and digit without raising for malformed values."""
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

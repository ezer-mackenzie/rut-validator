"""Internal primitives shared by the domain object and validation APIs."""

from dataclasses import dataclass
from re import Pattern, compile
from typing import Final

from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)
from .enums import RutFormat

FORMATTED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{1,2}(?:\.[0-9]{3}){2}-[0-9kK]")
HYPHENATED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}-[0-9kK]")
NORMALIZED_PATTERN: Final[Pattern[str]] = compile(r"[0-9]{7,8}[0-9kK]")
FORMAT_PATTERNS: Final[tuple[tuple[RutFormat, Pattern[str]], ...]] = (
    (RutFormat.FORMATTED, FORMATTED_PATTERN),
    (RutFormat.HYPHENATED, HYPHENATED_PATTERN),
    (RutFormat.NORMALIZED, NORMALIZED_PATTERN),
)
RUT_MODULE_ELEVEN_FACTORS: Final[tuple[int, ...]] = (2, 3, 4, 5, 6, 7)


@dataclass(frozen=True, slots=True)
class _ParsedRut:
    body: str
    check_digit: str
    format: RutFormat
    normalized: str


def detect_format(value: str) -> RutFormat | None:
    for rut_format, pattern in FORMAT_PATTERNS:
        if pattern.fullmatch(value):
            return rut_format

    return None


def normalize(value: str) -> str:
    return value.replace(".", "").replace("-", "").upper()


def format_normalized(value: str) -> str:
    body, check_digit = value[:-1], value[-1]
    groups: list[str] = []
    while body:
        groups.append(body[-3:])
        body = body[:-3]
    return f"{'.'.join(reversed(groups))}-{check_digit}"


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


def parse(value: object) -> _ParsedRut:
    """Parse a supported representation without checking its check digit."""
    if not isinstance(value, str) or value.strip() == "":
        raise RutInvalidValueError("El RUT debe ser un texto no vacío")

    detected_format = detect_format(value)
    if detected_format is None:
        raise RutInvalidFormatError(
            "Formato no válido, se esperaba algo como '12345678-9', "
            "'123456789' o '12.345.678-9'"
        )

    normalized = normalize(value)
    return _ParsedRut(
        body=normalized[:-1],
        check_digit=normalized[-1],
        format=detected_format,
        normalized=normalized,
    )


def validate(value: object) -> _ParsedRut:
    """Parse and validate a RUT into its canonical components."""
    parsed = parse(value)
    if not is_valid_check_digit(parsed.body, parsed.check_digit):
        raise RutModuleElevenValidationError(
            expected=module_eleven(parsed.body),
            received=parsed.check_digit,
        )
    return parsed

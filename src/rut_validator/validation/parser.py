"""Low-level parsing of supported RUT representations."""

from ..core.enums import RutFormat
from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
)
from .patterns import RutPatterns


class RutParser:
    """Low-level parser for RUT syntax and format detection.

    Parsing does not validate the check digit. Use ``RutValidator`` when a
    complete validation guarantee is required.
    """

    @classmethod
    def parse(cls, rut: object) -> tuple[str, str, RutFormat]:
        """Parse *rut* into its body, check digit, and detected format.

        Raises:
            RutInvalidValueError: If *rut* is missing or not text.
            RutInvalidFormatError: If *rut* uses an unsupported representation.
        """
        if not isinstance(rut, str) or rut.strip() == "":
            raise RutInvalidValueError(
                "No se puede parsear un RUT vacío, por favor ingrese un valor"
            )

        body, check_digit, format_detected = cls.destructure(rut)
        return body, check_digit, format_detected

    @classmethod
    def destructure(cls, rut: object) -> tuple[str, str, RutFormat]:
        """Split supported RUT text without checking its check digit.

        Raises:
            RutInvalidValueError: If *rut* is missing or not text.
            RutInvalidFormatError: If *rut* uses an unsupported representation.
        """
        if not isinstance(rut, str) or rut.strip() == "":
            raise RutInvalidValueError("El RUT debe ser un texto no vacío")

        format_detected = RutPatterns.detect_format(rut)

        if format_detected is None:
            raise RutInvalidFormatError(
                "Formato no válido, se esperaba algo como '12345678-9', '123456789' o '12.345.678-9'"
            )

        normalized = RutPatterns.normalize(rut)
        body, digit_check = normalized[:-1], normalized[-1]
        return body, digit_check, format_detected

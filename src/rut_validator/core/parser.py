from typing import Optional, Tuple

from rut_validator.core.patterns import RutPatterns
from rut_validator.types.enums import RutFormat

from rut_validator.errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
)


class RutParser:
    """Parser for Chilean RUT strings with format detection."""

    @classmethod
    def parse(cls, rut: object) -> Tuple[str, str, Optional[RutFormat]]:
        """
        Parses a RUT string and returns body, check_digit, and detected format.

        Args:
            rut: The RUT string to parse.

        Returns:
            Tuple of (body, check_digit, format).

        Raises:
            RutInvalidValueError: If RUT is empty or None.
            RutInvalidFormatError: If RUT format is invalid.
        """
        if not isinstance(rut, str) or rut.strip() == "":
            raise RutInvalidValueError(
                "No se puede parsear un RUT vacío, por favor ingrese un valor"
            )

        body, check_digit, format_detected = cls.destructure(rut)
        return body, check_digit, format_detected

    @classmethod
    def destructure(cls, rut: object) -> Tuple[str, str, Optional[RutFormat]]:
        """
        Destructures a RUT string into its body and check digit components,
        while also detecting the input format.

        Args:
            rut: The RUT string to parse.

        Returns:
            Tuple of (body, check_digit, format).
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

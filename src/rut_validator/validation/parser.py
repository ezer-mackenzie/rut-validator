"""Low-level parsing of supported RUT representations."""

from ..core import engine
from ..core.enums import RutFormat
from ..errors import RutInvalidValueError


class RutParser:
    """Low-level parser for RUT syntax and format detection.

    Parsing does not validate the check digit. Use ``validate_rut`` when a
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

        parsed = engine.parse(rut)
        return parsed.body, parsed.check_digit, parsed.format

    @classmethod
    def destructure(cls, rut: object) -> tuple[str, str, RutFormat]:
        """Split supported RUT text without checking its check digit.

        Raises:
            RutInvalidValueError: If *rut* is missing or not text.
            RutInvalidFormatError: If *rut* uses an unsupported representation.
        """
        parsed = engine.parse(rut)
        return parsed.body, parsed.check_digit, parsed.format

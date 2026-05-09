from rut_validator.core.patterns import RutPatterns


class RutFormatter:
    """Formatter for RUT strings with different output formats."""

    @staticmethod
    def to_original_format(rut: str) -> str:
        """
        Converts a RUT string to its original format with dots and dashes (e.g. "12345678-9" -> "12.345.678-9").

        Args:
            rut (str): The RUT string to format (e.g. "123456789")

        Returns:
            str: The RUT string in original format (e.g. "12.345.678-9")
        """
        return RutPatterns.formatted(rut)

    @staticmethod
    def to_normalize_format(rut: str) -> str:
        """
        Cleans the RUT string by removing dots and dashes, leaving only the digits and check digit.
        This is used internally to normalize the RUT before validation.

        Args:
            rut (str): The RUT string to clean (e.g. "12.345.678-9")

        Returns:
            str: The cleaned RUT string (e.g. "123456789")
        """
        return RutPatterns.normalized(rut)

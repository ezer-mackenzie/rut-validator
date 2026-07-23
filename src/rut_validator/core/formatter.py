from rut_validator.core.validator import RutValidator


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
        return RutValidator.validate(rut).formatted

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
        return RutValidator.validate(rut).normalized

    @staticmethod
    def to_hyphenated_format(rut: str) -> str:
        """Validate *rut* and return its canonical hyphenated representation."""
        return RutValidator.validate(rut).hyphenated

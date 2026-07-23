"""Pure RUT validator - no dependencies."""

from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Final

from rut_validator.core.enums import ValidationResult
from rut_validator.validation.parser import RutParser

from rut_validator.errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)

if TYPE_CHECKING:
    from rut_validator.core.rut import Rut

logger = logging.getLogger(__name__)
RUT_MODULE_ELEVEN_FACTORS: Final[tuple[int, ...]] = (2, 3, 4, 5, 6, 7)


def calculate_check_digit(body: str) -> str:
    """Calculate the modulo-11 check digit for a numeric RUT body."""
    return RutValidator.module_eleven(body)


def validate_rut(value: object) -> "Rut":
    """Validate *value* and return an immutable :class:`Rut` value object."""
    return RutValidator.validate(value)


class RutValidator:
    """Validator for Chilean RUTs with pure Python logic."""

    __slots__ = []

    @classmethod
    def get_validation_result(cls, rut: object) -> ValidationResult:
        """
        Get the validation result for a RUT string.

        Args:
            rut (str): The RUT string to validate.

        Returns:
            ValidationResult: The validation result.
        """
        logger.debug("Getting RUT validation result")

        try:
            body, check_digit, _ = RutParser.parse(rut)

        except RutInvalidValueError:
            logger.debug("RUT invalid due to empty or missing value")
            return ValidationResult.INVALID_VALUE

        except RutInvalidFormatError:
            logger.debug("RUT invalid due to incorrect format")
            return ValidationResult.INVALID_FORMAT

        if cls.is_valid_check_digit(body, check_digit):
            logger.debug("RUT check digit is valid")
            return ValidationResult.VALID

        logger.debug("RUT check digit is invalid")
        return ValidationResult.INVALID_CHECK_DIGIT

    @classmethod
    def is_valid(cls, rut: object) -> bool:
        """
        Check if a RUT string is valid without raising exceptions.

        Args:
            rut (str): The RUT string to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        validation_result = cls.get_validation_result(rut)
        is_valid = validation_result == ValidationResult.VALID

        logger.debug("RUT validity: %s (%s)", is_valid, validation_result)

        return is_valid

    @classmethod
    def validate(cls, rut: object) -> Rut:
        """
        Validate a RUT string and return a Rut object.

        Args:
            rut (str): The RUT string to validate.

        Returns:
            Rut: A validated Rut object.

        Raises:
            RutInvalidValueError: If the RUT is empty or missing.
            RutInvalidFormatError: If the RUT format is invalid.
            RutModuleElevenValidationError: If the check digit does not match.
        """
        logger.debug("Validating RUT")

        try:
            body, check_digit, format_detected = RutParser.parse(rut)

        except RutInvalidValueError:
            raise RutInvalidValueError(
                "No se puede parsear un RUT vacío, por favor ingrese un valor"
            )

        except RutInvalidFormatError:
            raise RutInvalidFormatError(
                "Formato no válido, se esperaba algo como '12345678-9', "
                "'123456789' o '12.345.678-9'"
            )

        if not cls.is_valid_check_digit(body, check_digit):
            check_digit_expected = cls.module_eleven(body)

            logger.debug("RUT check digit validation failed")

            raise RutModuleElevenValidationError(
                expected=check_digit_expected,
                received=check_digit,
            )

        from rut_validator.core.rut import Rut

        logger.debug("RUT validation successful")
        assert isinstance(rut, str)
        assert format_detected is not None
        return Rut._from_validated(rut, format_detected)

    @classmethod
    def module_eleven(cls, body: str) -> str:
        """
        Calculates the check digit using the modulo 11 algorithm.

        Returns:
            str: The calculated check digit (0-9 or 'K')
        """
        if not isinstance(body, str) or not body.isascii() or not body.isdigit():
            raise RutInvalidValueError("El cuerpo del RUT debe contener sólo dígitos")

        reversed_digits = map(int, reversed(body))
        total = sum(
            d * RUT_MODULE_ELEVEN_FACTORS[i % len(RUT_MODULE_ELEVEN_FACTORS)]
            for i, d in enumerate(reversed_digits)
        )
        remainder = total % 11
        result = 11 - remainder

        if result == 11:
            return "0"

        if result == 10:
            return "K"

        return str(result)

    @classmethod
    def is_valid_check_digit(cls, body: object, check_digit: object) -> bool:
        """
        Validates that the provided check digit matches the calculated one.

        Args:
            body (str): The numeric part of the RUT.
            check_digit (str): The check digit to validate.

        Returns:
            bool: True if the check digit is valid, False otherwise.
        """
        if (
            not isinstance(body, str)
            or not isinstance(check_digit, str)
            or len(check_digit) != 1
            or check_digit not in "0123456789kK"
        ):
            return False

        try:
            expected_check_digit = cls.module_eleven(body)
        except RutInvalidValueError:
            return False
        return check_digit.upper() == expected_check_digit

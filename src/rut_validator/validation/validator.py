"""Pure RUT validator - no dependencies."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .. import _engine
from ..core.enums import ValidationResult
from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
)
from .parser import RutParser

if TYPE_CHECKING:
    from ..core.rut import Rut

logger = logging.getLogger(__name__)
RUT_MODULE_ELEVEN_FACTORS = _engine.RUT_MODULE_ELEVEN_FACTORS


def calculate_check_digit(body: str) -> str:
    """Calculate the modulo-11 check digit for a numeric RUT body."""
    return RutValidator.module_eleven(body)


def validate_rut(value: object) -> Rut:
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

        if not isinstance(rut, str) or rut.strip() == "":
            raise RutInvalidValueError(
                "No se puede parsear un RUT vacío, por favor ingrese un valor"
            )

        from ..core.rut import Rut

        value = Rut(rut)
        logger.debug("RUT validation successful")
        return value

    @classmethod
    def module_eleven(cls, body: str) -> str:
        """
        Calculates the check digit using the modulo 11 algorithm.

        Returns:
            str: The calculated check digit (0-9 or 'K')
        """
        return _engine.module_eleven(body)

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
        return _engine.is_valid_check_digit(body, check_digit)

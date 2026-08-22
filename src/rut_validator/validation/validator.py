"""Framework-independent validation of Chilean RUT values."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..core import engine
from ..core.enums import ValidationResult
from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
)
from .parser import RutParser

if TYPE_CHECKING:
    from ..core.rut import Rut

logger = logging.getLogger(__name__)
RUT_MODULE_ELEVEN_FACTORS = engine.RUT_MODULE_ELEVEN_FACTORS


def calculate_check_digit(body: str) -> str:
    """Return the modulo-11 check digit for an ASCII numeric body.

    Raises:
        RutInvalidValueError: If *body* contains non-ASCII or non-digit text.
    """
    return RutValidator.module_eleven(body)


def validate_rut(value: object) -> Rut:
    """Return *value* as an immutable, validated :class:`Rut`.

    Raises:
        RutInvalidValueError: If *value* is missing or not text.
        RutInvalidFormatError: If *value* uses an unsupported representation.
        RutModuleElevenValidationError: If its check digit is incorrect.
    """
    return RutValidator.validate(value)


class RutValidator:
    """Expose raising and non-raising RUT validation operations."""

    __slots__ = []

    @classmethod
    def get_validation_result(cls, rut: object) -> ValidationResult:
        """Return the detailed validation outcome for *rut*."""
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
        """Return whether *rut* is valid without raising validation errors."""
        validation_result = cls.get_validation_result(rut)
        is_valid = validation_result == ValidationResult.VALID

        logger.debug("RUT validity: %s (%s)", is_valid, validation_result)

        return is_valid

    @classmethod
    def validate(cls, rut: object) -> Rut:
        """Return *rut* as an immutable, validated :class:`Rut`.

        Raises:
            RutInvalidValueError: If *rut* is missing or not text.
            RutInvalidFormatError: If *rut* uses an unsupported representation.
            RutModuleElevenValidationError: If its check digit is incorrect.
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
        """Return the modulo-11 check digit for an ASCII numeric body.

        Raises:
            RutInvalidValueError: If *body* contains non-ASCII or non-digit text.
        """
        return engine.module_eleven(body)

    @classmethod
    def is_valid_check_digit(cls, body: object, check_digit: object) -> bool:
        """Return whether *check_digit* is valid for *body*."""
        return engine.is_valid_check_digit(body, check_digit)

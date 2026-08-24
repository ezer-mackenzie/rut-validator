"""Framework-independent validation of Chilean RUT values."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..core import engine
from ..core.enums import ValidationResult
from ..errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)

if TYPE_CHECKING:
    from ..core.rut import Rut

logger = logging.getLogger(__name__)
RUT_MODULE_ELEVEN_FACTORS = engine.RUT_MODULE_ELEVEN_FACTORS


def calculate_check_digit(body: str) -> str:
    """Calculate the modulo-11 check digit for an ASCII numeric body.

    Raises:
        RutInvalidValueError: If *body* contains non-ASCII or non-digit text.
    """
    return engine.module_eleven(body)


def validate_rut(value: object) -> Rut:
    """Validate *value* and return its immutable :class:`Rut` representation.

    Raises:
        RutInvalidValueError: If *value* is missing or not text.
        RutInvalidFormatError: If *value* uses an unsupported representation.
        RutModuleElevenValidationError: If its check digit is incorrect.
    """
    logger.debug("Validating RUT")

    if not isinstance(value, str) or value.strip() == "":
        raise RutInvalidValueError(
            "No se puede parsear un RUT vacío, por favor ingrese un valor"
        )

    from ..core.rut import Rut

    rut = Rut(value)
    logger.debug("RUT validation successful")
    return rut


def get_validation_result(value: object) -> ValidationResult:
    """Classify *value* without raising a validation exception."""
    logger.debug("Getting RUT validation result")

    try:
        engine.validate(value)
    except RutInvalidValueError:
        logger.debug("RUT invalid due to empty or missing value")
        return ValidationResult.INVALID_VALUE
    except RutInvalidFormatError:
        logger.debug("RUT invalid due to incorrect format")
        return ValidationResult.INVALID_FORMAT
    except RutModuleElevenValidationError:
        logger.debug("RUT check digit is invalid")
        return ValidationResult.INVALID_CHECK_DIGIT

    logger.debug("RUT check digit is valid")
    return ValidationResult.VALID


def is_valid_rut(value: object) -> bool:
    """Check *value* without raising a validation exception."""
    result = get_validation_result(value)
    is_valid = result is ValidationResult.VALID
    logger.debug("RUT validity: %s (%s)", is_valid, result)
    return is_valid


class RutValidator:
    """Validate RUT values with either exceptions or structured outcomes."""

    __slots__ = []

    @classmethod
    def get_validation_result(cls, rut: object) -> ValidationResult:
        """Classify *rut* without raising a validation exception."""
        return get_validation_result(rut)

    @classmethod
    def is_valid(cls, rut: object) -> bool:
        """Check *rut* without raising a validation exception."""
        result = cls.get_validation_result(rut)
        is_valid = result is ValidationResult.VALID
        logger.debug("RUT validity: %s (%s)", is_valid, result)
        return is_valid

    @classmethod
    def validate(cls, rut: object) -> Rut:
        """Validate *rut* and return its immutable :class:`Rut` representation.

        Raises:
            RutInvalidValueError: If *rut* is missing or not text.
            RutInvalidFormatError: If *rut* uses an unsupported representation.
            RutModuleElevenValidationError: If its check digit is incorrect.
        """
        return validate_rut(rut)

    @classmethod
    def module_eleven(cls, body: str) -> str:
        """Calculate the modulo-11 check digit for an ASCII numeric body.

        Raises:
            RutInvalidValueError: If *body* contains non-ASCII or non-digit text.
        """
        return engine.module_eleven(body)

    @classmethod
    def is_valid_check_digit(cls, body: object, check_digit: object) -> bool:
        """Check a body and digit without raising for malformed values."""
        return engine.is_valid_check_digit(body, check_digit)

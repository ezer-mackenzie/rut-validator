"""Characterization tests for the public 1.x compatibility contract."""

from inspect import signature

import pytest

import rut_validator
from rut_validator import (
    Rut,
    RutFormat,
    RutValidator,
    ValidationResult,
    get_validation_result,
    is_valid_rut,
    validation,
)
from rut_validator.errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def test_root_exports_are_stable():
    assert set(rut_validator.__all__) == {
        "Rut",
        "RutFormat",
        "RutInvalidFormatError",
        "RutInvalidValueError",
        "RutModuleElevenValidationError",
        "RutValidationError",
        "RutValidator",
        "ValidationResult",
        "calculate_check_digit",
        "get_validation_result",
        "is_valid_rut",
        "validate_rut",
    }


def test_validation_compatibility_exports_are_stable():
    assert set(validation.__all__) == {
        "RutFormatter",
        "RutParser",
        "RutPatterns",
        "RutValidator",
        "calculate_check_digit",
        "get_validation_result",
        "is_valid_rut",
        "validate_rut",
    }


def test_rut_constructor_and_legacy_aliases_are_stable():
    parameters = signature(Rut).parameters
    rut = Rut("12.345.678-5", RutFormat.FORMATTED)

    assert list(parameters) == ["value", "format_detected"]
    assert parameters["format_detected"].default is None
    assert rut.number == rut.body
    assert rut.digit == rut.check_digit
    assert rut.is_dotted is rut.is_formatted
    assert rut.is_numeric is rut.is_normalized
    assert rut.equals(Rut("123456785"))


@pytest.mark.parametrize(
    ("value", "error", "result"),
    [
        (None, RutInvalidValueError, ValidationResult.INVALID_VALUE),
        (" 12345678-5", RutInvalidFormatError, ValidationResult.INVALID_FORMAT),
        ("１２３４５６７８５", RutInvalidFormatError, ValidationResult.INVALID_FORMAT),
        ("12345678‐5", RutInvalidFormatError, ValidationResult.INVALID_FORMAT),
        ("1234567890123", RutInvalidFormatError, ValidationResult.INVALID_FORMAT),
        (
            "12.345.678-0",
            RutModuleElevenValidationError,
            ValidationResult.INVALID_CHECK_DIGIT,
        ),
    ],
)
def test_validation_failures_keep_their_public_classification(value, error, result):
    with pytest.raises(error):
        RutValidator.validate(value)

    assert RutValidator.get_validation_result(value) is result
    assert get_validation_result(value) is result
    assert is_valid_rut(value) is (result is ValidationResult.VALID)


def test_public_error_codes_are_stable():
    assert RutInvalidValueError.code == "invalid_value"
    assert RutInvalidFormatError.code == "invalid_format"
    assert RutModuleElevenValidationError.code == "invalid_check_digit"

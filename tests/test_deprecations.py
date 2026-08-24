"""Deprecation contract for the migration from version 1 to version 2."""

import pytest

from rut_validator import Rut, RutFormat, ValidationResult, validate_rut
from rut_validator.errors import RutInvalidValueError
from rut_validator.validation import RutFormatter, RutParser, RutPatterns, RutValidator


def test_rut_legacy_constructor_argument_warns():
    with pytest.warns(
        DeprecationWarning,
        match=r"format_detected.*Rut\(value\)",
    ) as captured:
        rut = Rut("12.345.678-5", RutFormat.FORMATTED)

    assert rut.normalized == "123456785"
    assert captured[0].filename == __file__


@pytest.mark.parametrize(
    ("attribute", "replacement"),
    [
        ("number", "Rut.body"),
        ("digit", "Rut.check_digit"),
        ("is_dotted", "Rut.is_formatted"),
        ("is_numeric", "Rut.is_normalized"),
    ],
)
def test_rut_legacy_properties_warn(attribute: str, replacement: str):
    rut = Rut("12.345.678-5")

    with pytest.warns(DeprecationWarning, match=replacement):
        getattr(rut, attribute)


def test_rut_equals_warns():
    rut = Rut("12.345.678-5")

    with pytest.warns(DeprecationWarning, match="== operator"):
        assert rut.equals(Rut("123456785"))


def test_validation_facades_warn_and_keep_working():
    with pytest.warns(DeprecationWarning, match="RutValidator"):
        assert RutValidator.validate("12.345.678-5").normalized == "123456785"

    with pytest.warns(DeprecationWarning, match="RutFormatter"):
        assert RutFormatter.to_normalize_format("12.345.678-5") == "123456785"

    with pytest.warns(DeprecationWarning, match="RutParser"):
        assert RutParser.parse("12.345.678-5")[:2] == ("12345678", "5")

    with pytest.warns(DeprecationWarning, match="RutPatterns"):
        assert RutPatterns.detect_format("12.345.678-5") is RutFormat.FORMATTED

    with pytest.warns(DeprecationWarning, match="calculate_check_digit"):
        assert RutValidator.module_eleven("12345678") == "5"


def test_parser_invalid_value_warns_before_preserving_legacy_error():
    with pytest.warns(DeprecationWarning), pytest.raises(RutInvalidValueError):
        RutParser.parse(None)


def test_pattern_compatibility_methods_warn_on_every_branch():
    with pytest.warns(DeprecationWarning):
        assert RutPatterns.normalize("12.345.678-5") == "123456785"
    with pytest.warns(DeprecationWarning):
        assert RutPatterns.is_valid_format("12.345.678-5") is True
    with pytest.warns(DeprecationWarning):
        assert RutPatterns.is_valid_format("1" * 100) is False


def test_validator_subclasses_keep_their_classification_hook():
    class CustomValidator(RutValidator):
        @classmethod
        def get_validation_result(cls, rut: object) -> ValidationResult:
            return ValidationResult.VALID

    with pytest.warns(DeprecationWarning, match="is_valid_rut"):
        assert CustomValidator.is_valid("not-a-rut") is True


def test_canonical_api_does_not_warn():
    assert validate_rut("12.345.678-5").normalized == "123456785"

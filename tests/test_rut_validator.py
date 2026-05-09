import pytest

from rut_validator.core.parser import RutParser
from rut_validator.core.validator import RutValidator
from rut_validator.core.patterns import RutFormat, RutPatterns
from rut_validator.errors import RutInvalidFormatError, RutValidationError
from rut_validator.types.rut import Rut


def test_rut_object_normalizes_and_formats_correctly():
    rut = Rut("12.345.678-5")

    assert rut.value == "12.345.678-5"
    assert rut.normalized == "123456785"
    assert rut.body == 12345678
    assert rut.check_digit == "5"
    assert rut.formatted == "12.345.678-5"
    assert rut.is_dotted is True
    assert rut.is_hyphenated is False
    assert rut.is_normalized is False


def test_rut_object_preserves_input_value():
    original = "20884437-7"
    rut = Rut(original)

    assert rut.value == original
    assert rut.normalized == "208844377"
    assert rut.format == RutFormat.HYPHENATED


def test_rut_validator_returns_rut_object():
    rut = RutValidator.validate("12345678-5")

    assert isinstance(rut, Rut)
    assert rut.normalized == "123456785"


def test_rut_format_detection():
    # Test formatted format
    rut_formatted = Rut("20.884.437-7")
    assert rut_formatted.format == RutFormat.FORMATTED
    assert rut_formatted.is_dotted is True

    # Test hyphenated format
    rut_hyphen = Rut("20884437-7")
    assert rut_hyphen.format == RutFormat.HYPHENATED
    assert rut_hyphen.is_hyphenated is True

    # Test normalized format
    rut_normalized = Rut("208844377")
    assert rut_normalized.format == RutFormat.NORMALIZED
    assert rut_normalized.is_normalized is True


def test_rut_invalid_format_raises_error():
    with pytest.raises(RutInvalidFormatError):
        Rut("12-345678-9")


def test_rut_parser_destructure_detects_format():
    body, check_digit, detected_format = RutParser.destructure("12.345.678-5")

    assert body == "12345678"
    assert check_digit == "5"
    assert detected_format == RutFormat.FORMATTED


def test_rut_invalid_check_digit_raises_error():
    with pytest.raises(RutValidationError):
        Rut("12.345.678-0")


def test_rut_equality_and_hash():
    rut1 = Rut("12.345.678-5")
    rut2 = Rut("12345678-5")

    assert rut1 == rut2
    assert hash(rut1) == hash(rut2)
    assert {rut1} == {rut2}


def test_rut_equality_across_all_formats():
    rut_numeric = Rut("208844377")
    rut_hyphen = Rut("20884437-7")
    rut_dotted = Rut("20.884.437-7")

    assert rut_numeric == rut_hyphen == rut_dotted
    assert rut_numeric.equals(rut_hyphen)
    assert hash(rut_hyphen) == hash(rut_dotted)
    assert {rut_numeric} == {rut_dotted}


def test_rut_format_properties():
    """Test that all format properties return consistent values regardless of input format."""
    rut_normalized = Rut("208844377")
    rut_hyphen = Rut("20884437-7")
    rut_formatted = Rut("20.884.437-7")

    # All should return the same formatted versions
    assert rut_normalized.formatted == "20.884.437-7"
    assert rut_normalized.hyphenated == "20884437-7"
    assert rut_normalized.normalized == "208844377"

    assert rut_hyphen.formatted == "20.884.437-7"
    assert rut_hyphen.hyphenated == "20884437-7"
    assert rut_hyphen.normalized == "208844377"

    assert rut_formatted.formatted == "20.884.437-7"
    assert rut_formatted.hyphenated == "20884437-7"
    assert rut_formatted.normalized == "208844377"


def test_rutpatterns_format_methods_accept_raw_input():
    assert RutPatterns.detect_format("20.884.437-7") == RutFormat.FORMATTED
    assert RutPatterns.detect_format("20884437-7") == RutFormat.HYPHENATED
    assert RutPatterns.detect_format("208844377") == RutFormat.NORMALIZED

    assert RutPatterns.normalized("20.884.437-7") == "208844377"
    assert RutPatterns.hyphenated("20.884.437-7") == "20884437-7"
    assert RutPatterns.formatted("20.884.437-7") == "20.884.437-7"

    assert RutPatterns.formatted("20884437-7") == "20.884.437-7"
    assert RutPatterns.hyphenated("208844377") == "20884437-7"
    assert RutPatterns.normalized("20884437-7") == "208844377"


def test_is_valid_check_digit_helper():
    assert RutValidator.is_valid_check_digit("12345678", "5")
    assert not RutValidator.is_valid_check_digit("12345678", "0")


def test_is_valid_returns_false_for_invalid_rut():
    assert not RutValidator.is_valid("12-345678-9")
    assert not RutValidator.is_valid("12.345.678-0")

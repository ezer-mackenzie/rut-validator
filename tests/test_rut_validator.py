from inspect import signature

import pytest

from rut_validator import (
    Rut,
    RutFormat,
    ValidationResult,
    calculate_check_digit,
    get_validation_result,
    is_valid_rut,
    validate_rut,
)
from rut_validator.core import engine
from rut_validator.errors import (
    RutInvalidFormatError,
    RutInvalidValueError,
    RutModuleElevenValidationError,
)


def test_rut_preserves_input_and_exposes_canonical_representations():
    rut = Rut("12.345.678-5")

    assert rut.value == "12.345.678-5"
    assert rut.normalized == "123456785"
    assert rut.formatted == "12.345.678-5"
    assert rut.hyphenated == "12345678-5"
    assert rut.body == 12345678
    assert rut.check_digit == "5"
    assert rut.format is RutFormat.FORMATTED
    assert rut.is_formatted is True
    assert rut.is_hyphenated is False
    assert rut.is_normalized is False


def test_rut_constructor_has_only_the_value_argument():
    assert list(signature(Rut).parameters) == ["value"]


@pytest.mark.parametrize("value", [None, 123456785, b"123456785", [], True])
def test_rut_rejects_non_text_values(value: object):
    with pytest.raises(RutInvalidValueError):
        validate_rut(value)


def test_rut_accepts_string_subclasses():
    class RutText(str):
        pass

    assert Rut(RutText("12345678-5")).normalized == "123456785"


@pytest.mark.parametrize(
    ("value", "rut_format"),
    [
        ("20.884.437-7", RutFormat.FORMATTED),
        ("20884437-7", RutFormat.HYPHENATED),
        ("208844377", RutFormat.NORMALIZED),
    ],
)
def test_rut_detects_supported_formats(value: str, rut_format: RutFormat):
    assert Rut(value).format is rut_format


@pytest.mark.parametrize("body", ["1234567", "12345678", "01234567"])
def test_canonical_formats_round_trip_without_changing_identity(body: str):
    normalized = body + calculate_check_digit(body)
    rut = validate_rut(normalized)

    assert validate_rut(rut.formatted).normalized == normalized
    assert validate_rut(rut.hyphenated).normalized == normalized
    assert validate_rut(str(rut)).normalized == normalized


def test_rut_rejects_invalid_format_and_check_digit():
    with pytest.raises(RutInvalidFormatError):
        Rut("12-345678-9")
    with pytest.raises(RutModuleElevenValidationError):
        Rut("12.345.678-0")


def test_validation_checks_the_digit_once(monkeypatch: pytest.MonkeyPatch):
    calls = 0
    original = engine.is_valid_check_digit

    def counting_check(body: str, check_digit: str) -> bool:
        nonlocal calls
        calls += 1
        return original(body, check_digit)

    monkeypatch.setattr(engine, "is_valid_check_digit", counting_check)

    assert validate_rut("12345678-5").normalized == "123456785"
    assert calls == 1


def test_rut_equality_hash_and_redacted_repr():
    rut = Rut("12.345.678-5")
    equivalent = Rut("12345678-5")

    assert rut == equivalent
    assert hash(rut) == hash(equivalent)
    assert {rut} == {equivalent}
    assert repr(rut) == "Rut(value='<redacted>', format=RutFormat.FORMATTED)"
    assert rut.value not in repr(rut)
    assert rut != "123456785"


def test_rut_equality_includes_subclasses():
    class SpecializedRut(Rut):
        pass

    rut = Rut("12.345.678-5")
    specialized = SpecializedRut("123456785")

    assert rut == specialized
    assert specialized == rut
    assert hash(rut) == hash(specialized)


def test_rut_is_immutable():
    rut = Rut("12.345.678-5")

    with pytest.raises(AttributeError):
        rut.value = "208844377"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("12.345.678-5", ValidationResult.VALID),
        (None, ValidationResult.INVALID_VALUE),
        ("invalid", ValidationResult.INVALID_FORMAT),
        ("12.345.678-0", ValidationResult.INVALID_CHECK_DIGIT),
    ],
)
def test_validation_result_classifies_every_outcome(
    value: object,
    expected: ValidationResult,
):
    assert get_validation_result(value) is expected
    assert is_valid_rut(value) is (expected is ValidationResult.VALID)


@pytest.mark.parametrize(
    "value",
    [
        "１２３４５６７８５",
        "١٢٣٤٥٦٧８٥",
        "123456785\n",
        " 123456785",
        "123456785 ",
        "12345678‐5",
        "12345678–5",
        "1" * 100_000,
    ],
)
def test_validation_rejects_unicode_whitespace_and_oversized_input(value: str):
    assert is_valid_rut(value) is False


def test_calculate_check_digit_validates_body():
    assert calculate_check_digit("12345678") == "5"
    with pytest.raises(RutInvalidValueError):
        calculate_check_digit("１２３４５６７８")


def test_structured_check_digit_error():
    with pytest.raises(RutModuleElevenValidationError) as captured:
        validate_rut("12.345.678-0")

    assert captured.value.as_dict() == {
        "code": "invalid_check_digit",
        "message": "El dígito verificador no coincide, se esperaba '5' en vez de '0'",
        "expected_check_digit": "5",
        "received_check_digit": "0",
    }

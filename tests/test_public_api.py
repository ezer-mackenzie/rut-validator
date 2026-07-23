import rut_validator
from rut_validator import Rut, calculate_check_digit, validate_rut
from rut_validator.core.formatter import RutFormatter
from rut_validator.django import RUTField
from rut_validator.pydantic import RutStr
from rut_validator.sqlalchemy import RutType
from rut_validator.sqlmodel import RutField


def test_public_standalone_helpers():
    rut = validate_rut("12.345.678-5")

    assert isinstance(rut, Rut)
    assert rut.normalized == "123456785"
    assert calculate_check_digit("12345678") == "5"
    assert rut_validator.__version__ != "0+unknown"


def test_public_integration_imports():
    assert RutStr("12.345.678-5") == "123456785"
    assert RutType.impl.length == 9
    assert RUTField().max_length == 9
    assert callable(RutField)


def test_formatter_validates_and_formats():
    assert RutFormatter.to_original_format("123456785") == "12.345.678-5"
    assert RutFormatter.to_normalize_format("12.345.678-5") == "123456785"
    assert RutFormatter.to_hyphenated_format("123456785") == "12345678-5"

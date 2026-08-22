import pytest

import rut_validator
from rut_validator import Rut, calculate_check_digit, validate_rut
from rut_validator.errors import RutInvalidFormatError
from rut_validator.orm.django import RutDjango
from rut_validator.orm.pydantic import RutPydantic
from rut_validator.orm.sqlalchemy import RutSQLAlchemy
from rut_validator.orm.sqlmodel import RutSQLModel, rut_sqlmodel_field
from rut_validator.validation import RutFormatter


def test_public_standalone_helpers():
    rut = validate_rut("12.345.678-5")

    assert isinstance(rut, Rut)
    assert rut.normalized == "123456785"
    assert calculate_check_digit("12345678") == "5"
    assert rut_validator.__version__ != "0+unknown"


def test_public_integration_imports():
    assert RutPydantic("12.345.678-5") == "123456785"
    assert RutSQLAlchemy.impl.length == 9
    assert RutDjango().max_length == 9
    assert issubclass(RutSQLModel, RutPydantic)
    assert callable(rut_sqlmodel_field)


def test_formatter_validates_and_formats():
    assert RutFormatter.to_original_format("123456785") == "12.345.678-5"
    assert RutFormatter.to_normalize_format("12.345.678-5") == "123456785"
    assert RutFormatter.to_hyphenated_format("123456785") == "12345678-5"

    with pytest.raises(RutInvalidFormatError):
        RutFormatter.to_normalize_format("prefix-12.345.678-5")


def test_redundant_validated_rut_alias_is_not_public():
    assert "ValidatedRut" not in rut_validator.__all__
    assert not hasattr(rut_validator, "ValidatedRut")

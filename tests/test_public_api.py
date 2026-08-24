from importlib import import_module

import pytest

import rut_validator
from rut_validator import (
    Rut,
    ValidationResult,
    calculate_check_digit,
    get_validation_result,
    is_valid_rut,
    validate_rut,
)
from rut_validator.errors import RutInvalidFormatError
from rut_validator.integrations.django import RutDjango
from rut_validator.integrations.pydantic import RutPydantic
from rut_validator.integrations.sqlalchemy import RutSQLAlchemy
from rut_validator.integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field
from rut_validator.validation import RutFormatter


def test_public_standalone_helpers():
    rut = validate_rut("12.345.678-5")

    assert isinstance(rut, Rut)
    assert rut.normalized == "123456785"
    assert calculate_check_digit("12345678") == "5"
    assert is_valid_rut("12.345.678-5") is True
    assert is_valid_rut("12.345.678-0") is False
    assert get_validation_result(None) is ValidationResult.INVALID_VALUE
    assert rut_validator.__version__ != "0+unknown"


def test_public_integration_imports():
    assert RutPydantic("12.345.678-5") == "123456785"
    assert RutSQLAlchemy.impl.length == 9
    assert RutDjango().max_length == 9
    assert issubclass(RutSQLModel, RutPydantic)
    assert callable(rut_sqlmodel_field)


def test_formatter_validates_and_formats():
    with pytest.warns(DeprecationWarning, match="RutFormatter"):
        formatted = RutFormatter.to_original_format("123456785")
    with pytest.warns(DeprecationWarning, match="RutFormatter"):
        normalized = RutFormatter.to_normalize_format("12.345.678-5")
    with pytest.warns(DeprecationWarning, match="RutFormatter"):
        hyphenated = RutFormatter.to_hyphenated_format("123456785")

    assert formatted == "12.345.678-5"
    assert normalized == "123456785"
    assert hyphenated == "12345678-5"

    with pytest.warns(DeprecationWarning), pytest.raises(RutInvalidFormatError):
        RutFormatter.to_normalize_format("prefix-12.345.678-5")


def test_redundant_validated_rut_alias_is_not_public():
    assert "ValidatedRut" not in rut_validator.__all__
    assert not hasattr(rut_validator, "ValidatedRut")


@pytest.mark.parametrize(
    ("legacy_module", "canonical_module", "symbol"),
    [
        (
            "rut_validator.orm.pydantic",
            "rut_validator.integrations.pydantic",
            "RutPydantic",
        ),
        (
            "rut_validator.orm.sqlalchemy",
            "rut_validator.integrations.sqlalchemy",
            "RutSQLAlchemy",
        ),
        (
            "rut_validator.orm.sqlmodel",
            "rut_validator.integrations.sqlmodel",
            "RutSQLModel",
        ),
        (
            "rut_validator.orm.django",
            "rut_validator.integrations.django",
            "RutDjango",
        ),
    ],
)
def test_legacy_integration_imports_warn_and_preserve_identity(
    legacy_module: str,
    canonical_module: str,
    symbol: str,
):
    legacy = import_module(legacy_module)
    canonical = import_module(canonical_module)

    with pytest.warns(DeprecationWarning, match="removed in rut-validator 2.0.0"):
        legacy_symbol = getattr(legacy, symbol)

    assert legacy_symbol is getattr(canonical, symbol)
    with pytest.raises(AttributeError):
        getattr(legacy, "MissingIntegration")

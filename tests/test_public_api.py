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
from rut_validator.integrations.django import RutDjango
from rut_validator.integrations.pydantic import RutPydantic
from rut_validator.integrations.sqlalchemy import RutSQLAlchemy
from rut_validator.integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field


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


@pytest.mark.parametrize(
    "symbol",
    [
        "RutValidator",
        "RutFormatter",
        "RutParser",
        "RutPatterns",
        "ValidatedRut",
    ],
)
def test_removed_root_symbols_are_unavailable(symbol: str):
    assert symbol not in rut_validator.__all__
    assert not hasattr(rut_validator, symbol)


@pytest.mark.parametrize(
    "module",
    [
        "rut_validator.validation",
        "rut_validator.orm",
        "rut_validator.orm.pydantic",
        "rut_validator.orm.sqlalchemy",
        "rut_validator.orm.sqlmodel",
        "rut_validator.orm.django",
    ],
)
def test_removed_compatibility_modules_are_unavailable(module: str):
    with pytest.raises(ModuleNotFoundError):
        import_module(module)


def test_removed_rut_aliases_are_unavailable():
    rut = Rut("12.345.678-5")

    for attribute in ("number", "digit", "is_dotted", "is_numeric", "equals"):
        assert not hasattr(rut, attribute)

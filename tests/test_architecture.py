import subprocess
import sys

from rut_validator.core import Rut, RutFormat, ValidationResult
from rut_validator.validation import (
    RutFormatter,
    RutParser,
    RutPatterns,
    RutValidator,
)


def test_core_exports_only_domain_types():
    import rut_validator.core as core

    assert core.__all__ == ["RutFormat", "Rut", "ValidationResult"]
    assert Rut
    assert RutFormat
    assert ValidationResult


def test_validation_layer_exposes_framework_agnostic_implementation():
    assert RutFormatter
    assert RutParser
    assert RutPatterns
    assert RutValidator


def test_package_root_does_not_import_optional_frameworks():
    code = """
import sys
import rut_validator
assert rut_validator.RutValidator.is_valid("12.345.678-5")
frameworks = {"django", "sqlalchemy", "sqlmodel", "pydantic"}
assert not frameworks.intersection(sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

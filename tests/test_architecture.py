import ast
import subprocess
import sys
from pathlib import Path

import pytest

from rut_validator.core import Rut, RutFormat, ValidationResult
from rut_validator.validation import (
    RutFormatter,
    RutParser,
    RutPatterns,
    RutValidator,
)


def test_core_exports_only_domain_types():
    from rut_validator import core

    assert set(core.__all__) == {"RutFormat", "Rut", "ValidationResult"}
    assert Rut
    assert RutFormat
    assert ValidationResult


def test_validation_layer_exposes_framework_agnostic_implementation():
    assert RutFormatter
    assert RutParser
    assert RutPatterns
    assert RutValidator


def _imported_modules(relative_path: str) -> set[str]:
    source_path = Path(__file__).parents[1] / "src" / "rut_validator" / relative_path
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    return {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }


def test_domain_object_does_not_import_the_validation_layer():
    imports = _imported_modules("core/rut.py")

    assert not any("validation" in module for module in imports)


def test_engine_does_not_import_validation_or_optional_layers():
    imports = _imported_modules("core/engine.py")

    forbidden = ("validation", "orm", "django", "pydantic", "sqlalchemy", "sqlmodel")
    assert not any(any(name in module for name in forbidden) for module in imports)


def test_validation_implementation_does_not_depend_on_legacy_facades():
    validator_imports = _imported_modules("validation/validator.py")
    parser_imports = _imported_modules("validation/parser.py")

    assert not any(
        "parser" in module or "patterns" in module for module in validator_imports
    )
    assert not any("patterns" in module for module in parser_imports)


@pytest.mark.parametrize(
    "module",
    [
        "rut_validator",
        "rut_validator.core",
        "rut_validator.integrations",
        "rut_validator.validation",
        "rut_validator.orm",
    ],
)
def test_standalone_layers_do_not_import_optional_frameworks(module):
    code = f"""
import sys
import {module}
import rut_validator
assert rut_validator.is_valid_rut("12.345.678-5")
frameworks = {{"django", "sqlalchemy", "sqlmodel", "pydantic"}}
assert not frameworks.intersection(sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

import ast
import subprocess
import sys
from pathlib import Path

import pytest

from rut_validator.core import Rut, RutFormat, ValidationResult


def test_core_exports_only_domain_types():
    from rut_validator import core

    assert set(core.__all__) == {"RutFormat", "Rut", "ValidationResult"}
    assert Rut
    assert RutFormat
    assert ValidationResult


def _imported_modules(relative_path: str) -> set[str]:
    source_path = Path(__file__).parents[1] / "src" / "rut_validator" / relative_path
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    return {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }


def test_domain_object_depends_only_on_core_primitives():
    imports = _imported_modules("core/rut.py")

    assert not any("api" in module or "integrations" in module for module in imports)


def test_engine_does_not_import_public_or_optional_layers():
    imports = _imported_modules("core/engine.py")
    forbidden = ("api", "integrations", "django", "pydantic", "sqlalchemy", "sqlmodel")

    assert not any(any(name in module for name in forbidden) for module in imports)


@pytest.mark.parametrize(
    "relative_path",
    [
        "integrations/django.py",
        "integrations/pydantic.py",
        "integrations/sqlalchemy.py",
    ],
)
def test_integrations_use_the_public_api(relative_path: str):
    imports = _imported_modules(relative_path)

    assert "api" in imports
    assert "core" not in imports


@pytest.mark.parametrize(
    "module",
    [
        "rut_validator",
        "rut_validator.api",
        "rut_validator.core",
        "rut_validator.integrations",
    ],
)
def test_standalone_layers_do_not_import_optional_frameworks(module: str):
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

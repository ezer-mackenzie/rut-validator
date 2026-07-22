import json

from click.testing import CliRunner

from rut_validator.cli import cli


def test_cli_validate_json():
    result = CliRunner().invoke(cli, ["validate", "12.345.678-5", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.output)["normalized"] == "123456785"


def test_cli_format():
    result = CliRunner().invoke(cli, ["format", "123456785", "--format", "hyphenated"])

    assert result.exit_code == 0
    assert result.output == "12345678-5\n"


def test_cli_invalid_value_has_nonzero_exit_code():
    result = CliRunner().invoke(cli, ["validate", "invalid"])

    assert result.exit_code != 0
    assert "Formato no válido" in result.output

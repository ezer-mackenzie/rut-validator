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


def test_cli_invalid_json_is_machine_readable():
    result = CliRunner().invoke(cli, ["validate", "invalid", "--json"])

    assert result.exit_code == 1
    assert json.loads(result.output) == {
        "valid": False,
        "error": {
            "code": "invalid_format",
            "message": (
                "Formato no válido, se esperaba algo como '12345678-9', "
                "'123456789' o '12.345.678-9'"
            ),
        },
    }


def test_cli_info_and_detailed_output():
    runner = CliRunner()

    compact = runner.invoke(cli, ["info", "12.345.678-5"])
    detailed = runner.invoke(cli, ["info", "12.345.678-5", "--detailed"])

    assert compact.exit_code == 0
    assert json.loads(compact.output)["check_digit"] == "5"
    assert detailed.exit_code == 0
    assert "normalized: 123456785" in detailed.output


def test_cli_batch_outputs_json_lines_and_nonzero_for_invalid_rows():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("ruts.txt", "w", encoding="utf-8") as stream:
            stream.write("12.345.678-5\ninvalid\n")

        result = runner.invoke(cli, ["batch", "ruts.txt"])

    rows = [json.loads(line) for line in result.output.splitlines()]
    assert result.exit_code == 1
    assert rows[0]["valid"] is True
    assert rows[1]["error"]["code"] == "invalid_format"

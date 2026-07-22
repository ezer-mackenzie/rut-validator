"""Click commands for validating and formatting RUT values."""

import json as json_module
from pathlib import Path
from typing import Optional

import click

from rut_validator import RutValidator
from rut_validator.errors import RutValidationError


def _payload(value: str) -> dict[str, object]:
    rut = RutValidator.validate(value)
    return {
        "valid": True,
        "normalized": rut.normalized,
        "formatted": rut.formatted,
        "hyphenated": rut.hyphenated,
        "body": rut.body,
        "check_digit": rut.check_digit,
        "input_format": rut.format.value,
    }


@click.group()
@click.version_option(package_name="rut-validator")
def cli() -> None:
    """Valida y formatea RUT chilenos."""


@cli.command()
@click.argument("rut")
@click.option("as_json", "--json", is_flag=True, help="Entrega JSON.")
def validate(rut: str, as_json: bool) -> None:
    """Valida RUT y muestra sus representaciones."""
    try:
        data = _payload(rut)
    except RutValidationError as exc:
        if as_json:
            click.echo(json_module.dumps({"valid": False, "error": str(exc)}))
        raise click.ClickException(str(exc)) from exc
    if as_json:
        click.echo(json_module.dumps(data, ensure_ascii=False))
    else:
        click.echo(data["formatted"])


@cli.command(name="format")
@click.argument("rut")
@click.option(
    "output_format",
    "--format",
    type=click.Choice(["formatted", "dotted", "hyphenated", "normalized", "numeric"]),
    default="formatted",
    show_default=True,
)
@click.option("--quiet", is_flag=True, help="Muestra sólo el resultado.")
def format_command(rut: str, output_format: str, quiet: bool) -> None:
    """Convierte RUT a un formato canónico."""
    del quiet
    try:
        value = RutValidator.validate(rut)
    except RutValidationError as exc:
        raise click.ClickException(str(exc)) from exc
    formats = {
        "formatted": value.formatted,
        "dotted": value.formatted,
        "hyphenated": value.hyphenated,
        "normalized": value.normalized,
        "numeric": value.normalized,
    }
    click.echo(formats[output_format])


@cli.command()
@click.argument("rut")
@click.option("--detailed", is_flag=True)
def info(rut: str, detailed: bool) -> None:
    """Muestra información estructurada de RUT."""
    try:
        data = _payload(rut)
    except RutValidationError as exc:
        raise click.ClickException(str(exc)) from exc
    if detailed:
        for key, value in data.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo(json_module.dumps(data, ensure_ascii=False))


@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path))
def batch(file: Path, output: Optional[Path]) -> None:
    """Valida un RUT por línea y entrega JSON Lines."""
    rows: list[str] = []
    has_errors = False
    for line_number, raw_value in enumerate(
        file.read_text(encoding="utf-8").splitlines(), 1
    ):
        value = raw_value.strip()
        if not value:
            continue
        try:
            data = _payload(value)
        except RutValidationError as exc:
            has_errors = True
            data = {"valid": False, "value": value, "error": str(exc)}
        data["line"] = line_number
        rows.append(json_module.dumps(data, ensure_ascii=False))
    rendered = "\n".join(rows) + ("\n" if rows else "")
    if output is None:
        click.echo(rendered, nl=False)
    else:
        output.write_text(rendered, encoding="utf-8")
    if has_errors:
        raise click.exceptions.Exit(1)

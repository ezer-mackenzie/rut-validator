"""Click commands for validating and formatting RUT values."""

import json as json_module
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TextIO

import click

from ..api import validate_rut
from ..errors import RutValidationError


def _payload(value: str) -> dict[str, object]:
    rut = validate_rut(value)
    return {
        "valid": True,
        "normalized": rut.normalized,
        "formatted": rut.formatted,
        "hyphenated": rut.hyphenated,
        "body": rut.body,
        "check_digit": rut.check_digit,
        "input_format": rut.format.value,
    }


def _write_batch_rows(source: TextIO, destination: TextIO) -> bool:
    has_errors = False
    for line_number, raw_line in enumerate(source, 1):
        raw_value = raw_line.removesuffix("\n").removesuffix("\r")
        if raw_value == "":
            continue
        data: dict[str, object]
        try:
            data = _payload(raw_value)
        except RutValidationError as exc:
            has_errors = True
            data = {"valid": False, "error": exc.as_dict()}
        data["line"] = line_number
        destination.write(json_module.dumps(data, ensure_ascii=False) + "\n")
    return has_errors


def _process_batch(file: Path, output: Path | None) -> bool:
    try:
        with file.open(encoding="utf-8") as source:
            if output is None:
                return _write_batch_rows(source, click.get_text_stream("stdout"))

            with TemporaryDirectory(
                prefix=".rut-validator-",
                dir=output.parent,
            ) as temporary_directory:
                temporary_output = Path(temporary_directory) / output.name
                with temporary_output.open("w", encoding="utf-8") as destination:
                    has_errors = _write_batch_rows(source, destination)
                temporary_output.replace(output)
                return has_errors
    except OSError as exc:
        raise click.ClickException("No se pudo procesar el archivo") from exc


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
            click.echo(
                json_module.dumps(
                    {"valid": False, "error": exc.as_dict()},
                    ensure_ascii=False,
                )
            )
            raise click.exceptions.Exit(1) from exc
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
def format_command(rut: str, output_format: str) -> None:
    """Convierte RUT a un formato canónico."""
    try:
        value = validate_rut(rut)
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
def batch(file: Path, output: Path | None) -> None:
    """Valida un RUT por línea y entrega JSON Lines."""
    if _process_batch(file, output):
        raise click.exceptions.Exit(1)

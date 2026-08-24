# Command-line interface

The base installation exposes the `rut-validator` command.

## Validate

```bash
rut-validator validate 12.345.678-5
rut-validator validate 12.345.678-5 --json
```

JSON output includes validity, canonical formats, body, check digit, and input
format. On failure, `--json` produces a clean JSON object with `code` and
`message` and does not echo the submitted RUT.

## Format

```bash
rut-validator format 123456785 --format formatted
rut-validator format 123456785 --format hyphenated
rut-validator format 123456785 --format normalized
```

The legacy `--quiet` option remains accepted as a deprecated no-op until 2.0.0:
`format` already writes only the converted value.

## Inspect

```bash
rut-validator info 12.345.678-5
rut-validator info 12.345.678-5 --detailed
```

## Batch processing

Provide one RUT per line:

```text
12.345.678-5
20.884.437-7
invalid
```

```bash
rut-validator batch ruts.txt
rut-validator batch ruts.txt --output result.jsonl
```

Output uses JSON Lines. The command exits with status `1` when any line is
invalid and `0` when every line is valid.

Blank lines are skipped. Other lines are validated exactly as written; leading
or trailing whitespace is not removed silently.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Successful operation |
| `1` | Validation error or partially invalid batch |
| `2` | Invalid command usage |

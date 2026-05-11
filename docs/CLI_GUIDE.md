# RUT Validator CLI Documentation

A comprehensive command-line interface for validating, formatting, and analyzing Chilean RUTs (Rol Único Tributario).

## Installation

The CLI is included with the `rut-validator` package. Install it with:

```bash
pip install rut-validator
# or with poetry
poetry install
```

Then use it with:

```bash
rut-validator [COMMAND] [OPTIONS] [ARGS]
```

Or if installed via poetry:

```bash
poetry run rut-validator [COMMAND] [OPTIONS] [ARGS]
```

## Quick Start

### Validate a RUT

```bash
# Validate a RUT in any format
rut-validator validate "20.884.437-7"
rut-validator validate "20884437-7"
rut-validator validate "208844377"
```

### Format a RUT

```bash
# Convert to different formats
rut-validator format "208844377" --format dotted          # → 20.884.437-7
rut-validator format "208844377" --format hyphenated      # → 20884437-7
rut-validator format "20.884.437-7" --format numeric      # → 208844377
```

### Get RUT Information

```bash
# Show detailed RUT information
rut-validator info "20.884.437-7"
rut-validator info "20.884.437-7" --detailed
```

### Batch Processing

```bash
# Validate multiple RUTs from a file
rut-validator batch ruts.txt
rut-validator batch ruts.txt --output results.txt
rut-validator batch ruts.txt --only-valid
rut-validator batch ruts.txt --json
```

## Available Commands

### 1. `validate` - Validate a Chilean RUT

Validates a RUT string and returns detailed information about it.

**Usage:**
```bash
rut-validator validate [RUT] [OPTIONS]
```

**Arguments:**
- `RUT` (optional): The RUT to validate. If not provided, will prompt for input.

**Options:**
- `-q, --quiet`: Output only the result (no formatting)
- `-j, --json`: Output result as JSON
- `-i, --input FILE`: Read RUT from a file instead of command line

**Examples:**
```bash
# Basic validation with detailed output
rut-validator validate "20.884.437-7"

# Quiet mode (just the formatted RUT)
rut-validator validate "20.884.437-7" --quiet

# JSON output
rut-validator validate "20.884.437-7" --json

# Read from file
rut-validator validate --input rut.txt

# Interactive prompt
rut-validator validate
```

**Output:**
```
  📋 Original Input  20.884.437-7
  ✓ Validated       20.884.437-7
  🔢 Normalized      208844377
  💯 Body            20884437
  ✍️  Check Digit   7
  📊 Format          Dotted (12.345.678-9)

✅ RUT is valid: 20.884.437-7
```

---

### 2. `format` - Format a RUT to a Specified Format

Converts a validated RUT to a specific output format.

**Usage:**
```bash
rut-validator format RUT [OPTIONS]
```

**Arguments:**
- `RUT` (required): The RUT to format

**Options:**
- `-f, --format {dotted|hyphenated|numeric}`: Output format (default: dotted)
- `-q, --quiet`: Output only the formatted RUT
- `-j, --json`: Output result as JSON

**Supported Formats:**
- `dotted`: Standard Chilean format with dots and dash (e.g., `12.345.678-9`)
- `hyphenated`: Numbers with dash before check digit (e.g., `12345678-9`)
- `numeric`: Pure numeric format (e.g., `123456789`)

**Examples:**
```bash
# Format to dotted (default)
rut-validator format "208844377"

# Format to hyphenated
rut-validator format "20.884.437-7" --format hyphenated

# Format to numeric
rut-validator format "20884437-7" --format numeric

# Quiet mode (just the result)
rut-validator format "208844377" -q

# JSON output
rut-validator format "208844377" --json
```

**Output:**
```
✅ Formatted: 20.884.437-7
```

---

### 3. `info` - Display RUT Information

Shows information about a RUT without requiring full validation of the check digit.

**Usage:**
```bash
rut-validator info RUT [OPTIONS]
```

**Arguments:**
- `RUT` (required): The RUT to analyze

**Options:**
- `-d, --detailed`: Show detailed technical information including check digit validation
- `-j, --json`: Output result as JSON

**Examples:**
```bash
# Basic format detection
rut-validator info "20.884.437-7"

# Detailed analysis with validation
rut-validator info "20.884.437-7" --detailed

# JSON output
rut-validator info "20.884.437-7" --json
```

**Output:**
```
RUT Information
────────────────────────────────────────
  Input                20.884.437-7
  Valid Format         Yes
  Detected Format      dotted

Parsed Components:
  Body                 20884437
  Check Digit          7
  Normalized           208844377

Validation:
  ✓ Valid
  Formatted: 20.884.437-7
```

---

### 4. `batch` - Validate Multiple RUTs

Process multiple RUTs from a file, validating each one.

**Usage:**
```bash
rut-validator batch INPUT_FILE [OPTIONS]
```

**Arguments:**
- `INPUT_FILE` (required): Path to file containing RUTs (one per line)

**Options:**
- `-o, --output FILE`: Output file for results (default: stdout)
- `-q, --quiet`: Output only valid results
- `-j, --json`: Output results as JSON
- `--only-valid`: Output only valid RUTs
- `--only-invalid`: Output only invalid RUTs

**File Format:**
Each line in the input file should contain one RUT in any supported format:
```
20.884.437-7
12345678-9
208844377
invalid-rut
```

**Examples:**
```bash
# Process file and show all results
rut-validator batch ruts.txt

# Save results to file
rut-validator batch ruts.txt -o results.txt

# Only show valid RUTs
rut-validator batch ruts.txt --only-valid

# Only show invalid RUTs
rut-validator batch ruts.txt --only-invalid

# JSON format output
rut-validator batch ruts.txt --json

# Quiet mode (only valid results)
rut-validator batch ruts.txt --quiet

# Combine options
rut-validator batch ruts.txt --only-valid --json -o valid_ruts.json
```

**Output:**
```
✓ 20.884.437-7
✗ 12345678-9 - El dígito verificador no coincide, se esperaba '5' en vez de '9'
✓ 11.111.111-1
✗ invalid-rut - Formato no válido, se esperaba algo como '12345678-9', '123456789' o '12.345.678-9'
✓ 20.884.437-7

⚠️  3 valid, 2 invalid
```

---

## Global Options

These options are available for all commands:

- `-h, --help`: Show help message
- `--version`: Show CLI version

**Examples:**
```bash
# Show help for a specific command
rut-validator validate --help
rut-validator format --help

# Show version
rut-validator --version
```

---

## JSON Output Format

All commands support JSON output with the `--json` flag. This is useful for integration with other tools.

### Validate Command JSON Output

```json
{
  "valid": true,
  "original": "20.884.437-7",
  "formatted": "20.884.437-7",
  "normalized": "208844377",
  "body": 20884437,
  "check_digit": "7",
  "format": "dotted"
}
```

### Batch Command JSON Output

```json
{
  "total": 5,
  "valid_count": 3,
  "invalid_count": 2,
  "results": [
    {
      "valid": true,
      "input": "20.884.437-7",
      "formatted": "20.884.437-7",
      "normalized": "208844377",
      "body": 20884437,
      "check_digit": "7",
      "format": "dotted"
    },
    {
      "valid": false,
      "input": "invalid-rut",
      "message": "Formato no válido, se esperaba algo como '12345678-9', '123456789' o '12.345.678-9'"
    }
  ]
}
```

---

## Exit Codes

The CLI follows standard Unix exit code conventions:

- `0`: Success (validation passed or command completed)
- `1`: Failure (validation failed or error occurred)

---

## Error Handling

The CLI provides clear error messages for various failure scenarios:

```bash
# Invalid format
$ rut-validator validate "invalid-format"
❌ Formato no válido, se esperaba algo como '12345678-9', '123456789' o '12.345.678-9'

# Invalid check digit
$ rut-validator validate "12345678-9"
❌ El dígito verificador no coincide, se esperaba '5' en vez de '9'

# Empty input
$ rut-validator validate ""
❌ RUT cannot be empty
```

---

## Usage Examples by Scenario

### Scenario 1: Validating a Single RUT

```bash
# User receives a RUT and needs to validate it
$ rut-validator validate "20.884.437-7"
```

### Scenario 2: Standardizing RUT Formats

```bash
# Convert multiple RUT formats to standard format
$ rut-validator format "208844377"
$ rut-validator format "20884437-7"
$ rut-validator format "20.884.437-7"
```

### Scenario 3: Batch Import Validation

```bash
# Validate RUTs from a CSV export before importing to database
$ rut-validator batch users.txt --only-invalid -o invalid_users.txt
```

### Scenario 4: Integration with Scripts

```bash
# Use JSON output in shell scripts or other programs
$ rut-validator validate "20.884.437-7" --json | jq '.body'
20884437
```

### Scenario 5: Data Pipeline

```bash
# Clean and validate RUT data for processing
$ rut-validator batch raw_ruts.txt --only-valid --json -o clean_ruts.json
```

---

## Advanced Usage

### Using with Other Tools

The CLI can be combined with standard Unix tools:

```bash
# Count valid RUTs
rut-validator batch ruts.txt | grep "✓" | wc -l

# Extract only formatted RUTs
rut-validator batch ruts.txt | grep "✓" | awk '{print $2}'

# Find invalid RUTs and their errors
rut-validator batch ruts.txt --only-invalid
```

### Scripting

Use the exit code to control script flow:

```bash
#!/bin/bash

if rut-validator validate "$1" > /dev/null 2>&1; then
    echo "RUT is valid"
    exit 0
else
    echo "RUT is invalid"
    exit 1
fi
```

---

## Architecture

The CLI is built with:

- **Click**: Modern Python command-line interface framework
- **Modular Design**: Each command is in its own module for maintainability
- **Type Hints**: Full type annotations for better IDE support and fewer bugs
- **Consistent Output**: Formatted terminal output with emojis and colors
- **JSON Support**: Structured data output for programmatic use

### Structure

```
rut_validator/cli/
├── __init__.py              # CLI package entry point
├── main.py                  # Main CLI group and entry point
├── output.py                # Output formatting utilities
└── commands/
    ├── __init__.py
    ├── validate.py          # Validate command implementation
    ├── format.py            # Format command implementation
    ├── batch.py             # Batch command implementation
    └── info.py              # Info command implementation
```

### Adding New Commands

To add a new command:

1. Create a new file in `cli/commands/`:
   ```python
   # cli/commands/mycommand.py
   import click
   
   @click.command(name="mycommand")
   @click.argument("arg")
   def mycommand_command(arg: str) -> None:
       """Description of the command."""
       pass
   ```

2. Register it in `cli/main.py`:
   ```python
   from .commands.mycommand import mycommand_command
   cli.add_command(mycommand_command, name="mycommand")
   ```

---

## Troubleshooting

### Command Not Found

If you get "Command not found: rut-validator", ensure:
1. Package is installed: `pip list | grep rut-validator`
2. Virtual environment is activated (if using one)
3. Poetry environment: Use `poetry run rut-validator`

### Python Not Found

Make sure Python 3.9+ is installed:
```bash
python --version  # or python3 --version
```

### Import Errors

If you get import errors, reinstall the package:
```bash
pip install -e .     # Development mode
# or
poetry install
```

---

## Support

For bugs, feature requests, or questions:
- GitHub Issues: https://github.com/yourusername/rut-validator/issues
- Documentation: https://rut-validator.readthedocs.io/
- PyPI: https://pypi.org/project/rut-validator/

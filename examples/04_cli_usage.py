"""
Examples of using the RUT Validator CLI.

This script demonstrates various CLI commands for validating, formatting,
and processing Chilean RUTs.
"""

import subprocess
import json
from pathlib import Path


def run_command(cmd: str) -> str:
    """Run a CLI command and return the output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


def example_basic_validation():
    """Example 1: Basic RUT validation."""
    print("=" * 60)
    print("Example 1: Basic RUT Validation")
    print("=" * 60)
    
    # Validate a RUT in different formats
    ruts = ["20.884.437-7", "20884437-7", "208844377"]
    
    for rut in ruts:
        output = run_command(f"poetry run rut-validator validate '{rut}'")
        print(f"\nInput: {rut}")
        print(output)


def example_format_conversion():
    """Example 2: Convert between RUT formats."""
    print("\n" + "=" * 60)
    print("Example 2: Format Conversion")
    print("=" * 60)
    
    rut = "208844377"
    formats = ["dotted", "hyphenated", "numeric"]
    
    for fmt in formats:
        output = run_command(f"poetry run rut-validator format '{rut}' --format {fmt}")
        print(f"\nFormat: {fmt}")
        print(output)


def example_rut_info():
    """Example 3: Get RUT information."""
    print("\n" + "=" * 60)
    print("Example 3: RUT Information")
    print("=" * 60)
    
    rut = "20.884.437-7"
    output = run_command(f"poetry run rut-validator info '{rut}' --detailed")
    print(output)


def example_batch_processing():
    """Example 4: Batch validation."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Validation")
    print("=" * 60)
    
    # Create a test file
    test_file = Path("example_ruts.txt")
    test_file.write_text("""20.884.437-7
12345678-9
11.111.111-1
invalid-rut
208844377
""")
    
    print("Input file (example_ruts.txt):")
    print(test_file.read_text())
    
    print("\nBatch validation output:")
    output = run_command(f"poetry run rut-validator batch {test_file}")
    print(output)
    
    # Clean up
    test_file.unlink()


def example_json_output():
    """Example 5: JSON output for integration."""
    print("\n" + "=" * 60)
    print("Example 5: JSON Output")
    print("=" * 60)
    
    rut = "20.884.437-7"
    
    print("\nValidate command with JSON output:")
    output = run_command(f"poetry run rut-validator validate '{rut}' --json")
    print(output)
    
    # Parse and show structure
    try:
        data = json.loads(output)
        print("\nParsed JSON structure:")
        print(f"  - Valid: {data['valid']}")
        print(f"  - Body: {data['body']}")
        print(f"  - Check Digit: {data['check_digit']}")
        print(f"  - Format: {data['format']}")
    except json.JSONDecodeError:
        print("Could not parse JSON")


def example_quiet_mode():
    """Example 6: Quiet mode for scripting."""
    print("\n" + "=" * 60)
    print("Example 6: Quiet Mode (for scripting)")
    print("=" * 60)
    
    rut = "20.884.437-7"
    
    print("\nQuiet mode output (just the result):")
    output = run_command(f"poetry run rut-validator format '{rut}' --quiet")
    print(f"Result: {output.strip()}")


def example_error_handling():
    """Example 7: Error handling."""
    print("\n" + "=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)
    
    invalid_ruts = [
        "invalid-format",
        "12345678-9",  # Invalid check digit
        "",  # Empty
    ]
    
    for rut in invalid_ruts:
        print(f"\nValidating: '{rut}'")
        output = run_command(f"poetry run rut-validator validate '{rut}' 2>&1")
        print(output[:200])


def example_help():
    """Example 8: Help and documentation."""
    print("\n" + "=" * 60)
    print("Example 8: Available Commands")
    print("=" * 60)
    
    output = run_command("poetry run rut-validator --help")
    print(output)


if __name__ == "__main__":
    example_basic_validation()
    example_format_conversion()
    example_rut_info()
    example_batch_processing()
    example_json_output()
    example_quiet_mode()
    example_error_handling()
    example_help()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

"""
Example 1: Pure validation - no Pydantic or FastAPI required

This is useful when you just need to validate RUTs without
integrating with web frameworks.
"""

from rut_validator import validate_rut

# ✅ Valid RUT
print("=" * 60)
print("EXAMPLE 1: Pure RUT Validation")
print("=" * 60)

try:
    result = validate_rut("12345678-5")
    print("\n✅ Input: '12345678-5'")
    print(f"   Normalized: {result.normalized}")
    print(f"   Formatted:  {result.formatted}")
    print(f"   Body:       {result.body}")
    print(f"   Digit:      {result.check_digit}")
    print(f"   Format:     {result.format}")
    print(f"   Is formatted: {result.is_formatted}")
except ValueError as e:
    print(f"❌ Error: {e}")

# ❌ Invalid RUT (wrong check digit)
print("\n" + "-" * 60)
try:
    result = validate_rut("12345678-1")  # Should be 5
    print("✅ Input: '12345678-1'")
except ValueError as e:
    print("❌ Input: '12345678-1'")
    print(f"   Error: {e}")

# ❌ Invalid format
print("\n" + "-" * 60)
try:
    result = validate_rut("invalid-rut")
    print("✅ Input: 'invalid-rut'")
except ValueError as e:
    print("❌ Input: 'invalid-rut'")
    print(f"   Error: {e}")

# ✅ Valid RUT without hyphen
print("\n" + "-" * 60)
try:
    result = validate_rut("123456785")
    print("✅ Input: '123456785'")
    print(f"   Normalized: {result.normalized}")
    print(f"   Formatted:  {result.formatted}")
    print(f"   Format:     {result.format}")
except ValueError as e:
    print(f"❌ Error: {e}")

# ✅ Valid RUT with K digit
print("\n" + "-" * 60)
try:
    result = validate_rut("10000013-K")
    print("✅ Input: '10000013-K'")
    print(f"   Digit: {result.check_digit}")
    print(f"   Format: {result.format}")
except ValueError as e:
    print(f"❌ Error: {e}")

# ✅ Format detection examples
print("\n" + "=" * 60)
print("FORMAT DETECTION EXAMPLES")
print("=" * 60)

formats_to_test = [
    ("20.884.437-7", "Dotted format"),
    ("20884437-7", "Hyphenated format"),
    ("208844377", "Numeric format"),
]

for rut_str, description in formats_to_test:
    try:
        result = validate_rut(rut_str)
        print(f"\n✅ {description}: '{rut_str}'")
        print(f"   Format detected: {result.format}")
        print(f"   Is formatted: {result.is_formatted}")
        print(f"   Is hyphenated: {result.is_hyphenated}")
        print(f"   Is normalized: {result.is_normalized}")
    except ValueError as e:
        print(f"❌ Error with {description}: {e}")

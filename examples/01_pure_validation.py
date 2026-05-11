"""
Example 1: Pure validation - no Pydantic or FastAPI required

This is useful when you just need to validate RUTs without
integrating with web frameworks.
"""

from rut_validator import RutValidator

# ✅ Valid RUT
print("=" * 60)
print("EXAMPLE 1: Pure RUT Validation")
print("=" * 60)

try:
    result = RutValidator.validate("12345678-9")
    print("\n✅ Input: '12345678-9'")
    print(f"   Normalized: {result.normalized}")
    print(f"   Formatted:  {result.formatted}")
    print(f"   Number:     {result.number}")
    print(f"   Digit:      {result.digit}")
    print(f"   Format:     {result.format}")
    print(f"   Is dotted:  {result.is_dotted}")
except ValueError as e:
    print(f"❌ Error: {e}")

# ❌ Invalid RUT (wrong check digit)
print("\n" + "-" * 60)
try:
    result = RutValidator.validate("12345678-1")  # Should be 9
    print("✅ Input: '12345678-1'")
except ValueError as e:
    print("❌ Input: '12345678-1'")
    print(f"   Error: {e}")

# ❌ Invalid format
print("\n" + "-" * 60)
try:
    result = RutValidator.validate("invalid-rut")
    print("✅ Input: 'invalid-rut'")
except ValueError as e:
    print("❌ Input: 'invalid-rut'")
    print(f"   Error: {e}")

# ✅ Valid RUT without hyphen
print("\n" + "-" * 60)
try:
    result = RutValidator.validate("123456789")
    print("✅ Input: '123456789'")
    print(f"   Normalized: {result.normalized}")
    print(f"   Formatted:  {result.formatted}")
    print(f"   Format:     {result.format}")
except ValueError as e:
    print(f"❌ Error: {e}")

# ✅ Valid RUT with K digit
print("\n" + "-" * 60)
try:
    result = RutValidator.validate("12345677-6")  # Use a valid RUT
    print("✅ Input: '12345677-6'")
    print(f"   Digit: {result.digit}")
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
        result = RutValidator.validate(rut_str)
        print(f"\n✅ {description}: '{rut_str}'")
        print(f"   Format detected: {result.format}")
        print(f"   Is dotted: {result.is_dotted}")
        print(f"   Is hyphenated: {result.is_hyphenated}")
        print(f"   Is numeric: {result.is_numeric}")
    except ValueError as e:
        print(f"❌ Error with {description}: {e}")

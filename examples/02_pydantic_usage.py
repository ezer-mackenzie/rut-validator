"""
Example 2: Using RutPydantic with Pydantic models

This shows how RutPydantic automatically validates RUTs
when used in Pydantic BaseModel.
"""

import json

from pydantic import BaseModel, ValidationError

from rut_validator.integrations.pydantic import RutPydantic

print("=" * 60)
print("EXAMPLE 2: Pydantic Integration")
print("=" * 60)


# Define a model with RutPydantic
class Person(BaseModel):
    name: str
    rut: RutPydantic  # ✅ Automatically validated!


# ✅ Valid person
print("\n✅ Creating valid person:")
try:
    person = Person(name="Juan Pérez", rut="12345678-5")
    print(f"   Name: {person.name}")
    print(f"   RUT (normalized): {person.rut}")
    print(f"   Type of rut: {type(person.rut).__name__}")
except ValidationError as e:
    print(f"   ❌ Error: {e}")

# ❌ Invalid RUT
print("\n" + "-" * 60)
print("❌ Creating person with invalid RUT:")
try:
    person = Person(name="Juan Pérez", rut="12345678-k")  # Wrong digit
    print(f"   ✅ Success: {person}")
except ValidationError as e:
    print("   Error occurred (expected):")
    for error in e.errors():
        print(f"   - Field: {error['loc'][0]}")
        print(f"   - Type: {error['type']}")
        print(f"   - Message: {error['msg']}")

# ✅ Valid without hyphen
print("\n" + "-" * 60)
print("✅ Creating person with RUT (no hyphen):")
try:
    person = Person(name="María García", rut="123456785")
    print(f"   Name: {person.name}")
    print(f"   RUT (normalized): {person.rut}")
except ValidationError as e:
    print(f"   ❌ Error: {e}")

# ✅ Serialization
print("\n" + "-" * 60)
print("✅ Model serialization:")
person = Person(name="Carlos López", rut="12345678-5")
print("   model_dump():")
print(f"   {person.model_dump()}")
print("\n   model_dump_json():")
print(f"   {person.model_dump_json()}")

# ✅ JSON Schema (useful for FastAPI OpenAPI)
print("\n" + "-" * 60)
print("✅ JSON Schema (for OpenAPI documentation):")
schema = Person.model_json_schema()
print("   RUT field schema:")
print(json.dumps(schema["properties"]["rut"], indent=2))

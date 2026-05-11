# Rut Value Object and Validation Design

This document explains why `Rut` needs `__eq__` and `__hash__`, and why `RutValidator` benefits from a dedicated validation result enum.

## Why implement `__eq__` and `__hash__` on `Rut`

`Rut` is a value object: two RUTs with the same normalized value should be considered equal, even if they come from different input formats.

### Examples

- `Rut("12.345.678-5")` should equal `Rut("12345678-5")`
- `Rut` objects should work naturally in sets and dictionary keys

### Why this matters

- `__eq__` makes comparisons semantics-based, not identity-based.
- `__hash__` allows the object to be used safely in hashed collections.

### Practical benefits

- Users can write `if rut1 == rut2:` and get the correct value equality.
- `Rut` can be used in `set()` or as a dictionary key.
- Code becomes more predictable and easier to reason about.

## Why `RutValidator.is_valid()` should return `bool`

`is_valid()` is a lightweight check that tells you whether the RUT is valid.

Use cases:

- quick validation before user feedback
- form validation without exceptions
- conditional flows like `if RutValidator.is_valid(rut): ...`

## Why `RutValidator.validate()` should return `Rut`

`validate()` is the full validation operation:

- it verifies format
- it computes the check digit
- it raises detailed exceptions on failure
- it returns a fully initialized `Rut` object on success

This is a clean separation of responsibilities:

- `is_valid()` → boolean check
- `validate()` → validated object or exception

## Why use an enum for validation results

A dedicated `ValidationResult` enum makes your intent explicit.

Instead of returning `True`/`False` and guessing why validation failed, the enum can represent:

- `VALID`
- `INVALID_VALUE`
- `INVALID_FORMAT`
- `INVALID_CHECK_DIGIT`

### Benefits

- clearer internal logic
- easier debugging and logging
- better error handling in higher-level code

## Current implementation notes

- `RutValidator.get_validation_result()` returns a `ValidationResult` enum
- `RutValidator.is_valid()` returns `True` only for `ValidationResult.VALID`
- `RutValidator.validate()` raises appropriate exceptions for invalid input
- `Rut.__eq__()` compares normalized values
- `Rut.__hash__()` hashes the normalized value

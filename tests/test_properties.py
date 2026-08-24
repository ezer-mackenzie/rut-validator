from hypothesis import given
from hypothesis import strategies as st

from rut_validator import calculate_check_digit, is_valid_rut, validate_rut


@given(st.integers(min_value=1_000_000, max_value=99_999_999))
def test_every_generated_body_validates_with_its_calculated_digit(body: int):
    body_text = str(body)
    check_digit = calculate_check_digit(body_text)

    rut = validate_rut(f"{body_text}-{check_digit}")

    assert rut.normalized == f"{body_text}{check_digit}"


@given(st.integers(min_value=1_000_000, max_value=99_999_999))
def test_mutating_generated_check_digit_is_always_rejected(body: int):
    body_text = str(body)
    expected = calculate_check_digit(body_text)
    replacement = next(value for value in "0123456789K" if value != expected)

    assert not is_valid_rut(f"{body_text}-{replacement}")

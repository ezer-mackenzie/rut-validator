import pytest
from django.core.exceptions import ValidationError

from rut_validator.core.orm.django.schema import RUTField


class TestRUTField:
    def test_valid_rut_saves_normalized(self):
        field = RUTField()
        normalized = field.to_python("12.345.678-5")
        assert normalized == "123456785"

    def test_invalid_format_raises_validation_error(self):
        field = RUTField()
        with pytest.raises(ValidationError):
            field.to_python("invalid-rut")

    def test_invalid_check_digit_raises_validation_error(self):
        field = RUTField()
        with pytest.raises(ValidationError):
            field.to_python("12.345.678-0")

    def test_none_value_returns_none(self):
        field = RUTField()
        assert field.to_python(None) is None

    def test_non_string_raises_validation_error(self):
        field = RUTField()
        with pytest.raises(ValidationError):
            field.to_python(123456789)

    def test_max_length_constraint(self):
        field = RUTField()
        assert field.max_length == 9  # Normalized storage length

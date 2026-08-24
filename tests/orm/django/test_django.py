import pytest
from django.core.exceptions import ValidationError

from rut_validator.integrations.django import RutDjango


class TestRutDjango:
    def test_valid_rut_saves_normalized(self):
        field = RutDjango()
        normalized = field.to_python("12.345.678-5")
        assert normalized == "123456785"

    def test_invalid_format_raises_validation_error(self):
        field = RutDjango()
        with pytest.raises(ValidationError):
            field.to_python("invalid-rut")

    def test_invalid_check_digit_raises_validation_error(self):
        field = RutDjango()
        with pytest.raises(ValidationError):
            field.to_python("12.345.678-0")

    def test_none_value_returns_none(self):
        field = RutDjango()
        assert field.to_python(None) is None

    def test_non_string_raises_validation_error(self):
        field = RutDjango()
        with pytest.raises(ValidationError):
            field.to_python(123456789)

    def test_max_length_constraint(self):
        field = RutDjango()
        assert field.max_length == 9  # Normalized storage length

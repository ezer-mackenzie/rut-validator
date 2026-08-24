import pytest
from django.core.exceptions import ValidationError

from rut_validator.integrations.django import RutDjango, RutDjangoValidator


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

    def test_serializable_validator_accepts_valid_text(self):
        assert RutDjangoValidator()("12.345.678-5") is None

    @pytest.mark.parametrize("value", [123456785, "invalid-rut"])
    def test_serializable_validator_rejects_invalid_values(self, value: object):
        with pytest.raises(ValidationError):
            RutDjangoValidator()(value)

    def test_formfield_accepts_formatted_input_length(self):
        form_field = RutDjango().formfield()

        assert form_field.max_length == 12

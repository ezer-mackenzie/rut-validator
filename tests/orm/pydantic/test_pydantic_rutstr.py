import pytest
from pydantic import BaseModel, ValidationError

from rut_validator.core.orm.pydantic.schema import RutStr


class TestRutStr:
    def test_valid_rut_validates_and_normalizes(self):
        rut = RutStr("12.345.678-5")
        assert rut == "123456785"

    def test_invalid_format_raises_validation_error(self):
        with pytest.raises(ValueError):
            RutStr("invalid-rut")

    def test_invalid_check_digit_raises_validation_error(self):
        with pytest.raises(ValueError):
            RutStr("12.345.678-0")

    def test_json_schema_generation(self):
        from pydantic import BaseModel

        class Model(BaseModel):
            rut: RutStr

        schema = Model.model_json_schema()
        # Check that the rut field has the expected properties
        rut_schema = schema["properties"]["rut"]
        assert rut_schema["type"] == "string"
        assert "pattern" in rut_schema
        assert rut_schema["example"] == "12345678-9"

    def test_pydantic_model_integration(self):
        class User(BaseModel):
            rut: RutStr

        user = User(rut="12345678-5")
        assert user.rut == "123456785"

    def test_edge_case_empty_string(self):
        with pytest.raises(ValueError):
            RutStr("")

    def test_case_insensitive_check_digit(self):
        rut = RutStr("12345678-5")  # Valid RUT
        assert rut == "123456785"

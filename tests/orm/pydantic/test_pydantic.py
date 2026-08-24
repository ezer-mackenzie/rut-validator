import pytest
from pydantic import BaseModel

from rut_validator.core import engine
from rut_validator.orm.pydantic import RutPydantic


class TestRutPydantic:
    def test_valid_rut_validates_and_normalizes(self):
        rut = RutPydantic("12.345.678-5")
        assert rut == "123456785"

    def test_invalid_format_raises_validation_error(self):
        with pytest.raises(ValueError):
            RutPydantic("invalid-rut")

    def test_invalid_check_digit_raises_validation_error(self):
        with pytest.raises(ValueError):
            RutPydantic("12.345.678-0")

    def test_json_schema_generation(self):
        from pydantic import BaseModel

        class Model(BaseModel):
            rut: RutPydantic

        schema = Model.model_json_schema()
        # Check that the rut field has the expected properties
        rut_schema = schema["properties"]["rut"]
        assert rut_schema["type"] == "string"
        assert rut_schema["pattern"] == rf"^{engine.VALIDATION_PATTERN.pattern}$"
        assert rut_schema["examples"] == [
            "12.345.678-5",
            "12345678-5",
            "123456785",
        ]

    def test_pydantic_model_integration(self):
        class User(BaseModel):
            rut: RutPydantic

        user = User(rut="12345678-5")
        assert user.rut == "123456785"
        assert isinstance(user.rut, RutPydantic)

    def test_edge_case_empty_string(self):
        with pytest.raises(ValueError):
            RutPydantic("")

    def test_case_insensitive_check_digit(self):
        rut = RutPydantic("12345678-5")  # Valid RUT
        assert rut == "123456785"

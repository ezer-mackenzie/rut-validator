"""Pydantic v2 integration for Chilean RUT values."""

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from rut_validator.errors import RutValidationError
from rut_validator.validation import RutValidator


class RutStr(str):
    """A validated RUT string stored in normalized form."""

    def __new__(cls, value: str) -> "RutStr":
        return str.__new__(cls, cls._normalize(value))

    @staticmethod
    def _normalize(value: str) -> str:
        try:
            return RutValidator.validate(value).normalized
        except RutValidationError as exc:
            raise ValueError(str(exc)) from exc

    @classmethod
    def _from_input(cls, value: str) -> "RutStr":
        return str.__new__(cls, cls._normalize(value))

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: type[Any],
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._from_input,
            core_schema.str_schema(strict=True),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        field_schema = handler(schema)
        field_schema.update(
            {
                "type": "string",
                "pattern": (
                    r"^(?:\d{1,2}(?:\.\d{3}){2}-[0-9kK]"
                    r"|\d{7,8}-[0-9kK]|\d{7,8}[0-9kK])$"
                ),
                "examples": ["12.345.678-5", "12345678-5", "123456785"],
                "description": "RUT chileno válido; se normaliza antes de almacenar.",
            }
        )
        return field_schema


__all__ = ["RutStr"]

"""Pydantic v2 integration for Chilean RUT values."""

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from ..errors import RutValidationError
from ..validation import RutPatterns, validate_rut


class RutPydantic(str):
    """A validated RUT string stored in normalized form."""

    def __new__(cls, value: str) -> "RutPydantic":  # noqa: PYI034
        return str.__new__(cls, cls._normalize(value))

    @staticmethod
    def _normalize(value: str) -> str:
        try:
            return validate_rut(value).normalized
        except RutValidationError as exc:
            raise ValueError(str(exc)) from exc

    @classmethod
    def _from_input(cls, value: str) -> "RutPydantic":
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
                "pattern": rf"^{RutPatterns.VALIDATION_PATTERN.pattern}$",
                "examples": ["12.345.678-5", "12345678-5", "123456785"],
                "description": "RUT chileno válido; se normaliza antes de almacenar.",
            }
        )
        return field_schema


__all__ = ["RutPydantic"]

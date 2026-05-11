"""RutStr - Pydantic-integrated RUT validator (style: EmailStr)"""

from typing import Any, Annotated
from typing import TYPE_CHECKING

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue

from pydantic_core.core_schema import str_schema, no_info_after_validator_function
from pydantic_core.core_schema import CoreSchema

from ...validator import RutValidator


if TYPE_CHECKING:
    # For type checkers, we can just treat RutStr as a regular string.
    RutStr = Annotated[str, ...]

else:

    class RutStr(str):
        @classmethod
        def __get_pydantic_core_schema__(
            cls,
            _source_type: type[Any],
            _handler: GetCoreSchemaHandler,
        ) -> CoreSchema:
            """
            Defines the core schema for Pydantic validation.
            This method is called by Pydantic to get the schema that will be used for validation
            and parsing of the field.
            """

            return no_info_after_validator_function(
                cls._validate,
                str_schema(),
            )

        @classmethod
        def __get_pydantic_json_schema__(
            cls,
            schema: CoreSchema,
            handler: GetJsonSchemaHandler,
        ) -> JsonSchemaValue:
            """Defines JSON schema for OpenAPI/Swagger"""
            field_schema = handler(schema)
            field_schema.update(
                {
                    "type": "string",
                    "pattern": r"^\d{1,8}-[0-9kK]$|^\d{8}[0-9kK]$",
                    "example": "12345678-9",
                    "description": "Valid Chilean RUT (e.g: 12345678-9 or 123456789)",
                }
            )

            return field_schema

        def __new__(cls, value: str) -> 'RutStr':
            validated = cls._validate(value)
            return str.__new__(cls, validated)

        @classmethod
        def _validate(cls, input_value: str, /) -> str:
            """
            Validates the input value as a RUT and returns the normalized form.
            If the input is not a valid RUT, it raises a ValueError with an appropriate message.

            Args:
                input_value (str): The input value to validate as a RUT.

            Returns:
                str: The normalized RUT.

            Raises:
                ValueError: If the input is not a valid RUT.
            """
            try:
                return RutValidator.validate(input_value).normalized
            except Exception as e:
                raise ValueError(str(e))

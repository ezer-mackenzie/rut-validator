from sqlalchemy.types import String, TypeDecorator
from sqlalchemy import Dialect

from typing import Any

from rut_validator.core.validator import RutValidator

class RutSQLAlchemy(TypeDecorator):  # type: ignore
    """
    Custom SQLAlchemy type for RUT validation and normalization. This type will ensure that any value being stored in the database is a valid RUT and is normalized to a consistent format.
    When retrieving values from the database, it returns the stored normalized string.
    """

    impl = String  # Save as VARCHAR/String into the database
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> str | None:
        """
        the `process_bind_param` method is called when a value is being bound to a parameter in a SQL statement. This is where we can validate and normalize the RUT value before it gets sent to the database.
        If the value is None, we can return it directly (or we could choose to return an empty string if we prefer). If the value is already a RutStr instance, we can return its normalized form directly.
        If it's a regular string, we validate and normalize it using the RutStr._validate method before returning it.

        Args:
            value (Any): The value to be bound to the SQL parameter. This can be a string, a RutStr instance, or None.
            dialect (Dialect): The SQLAlchemy dialect in use, which can be useful if we need to handle different database backends differently (though in this case we likely won't need it).

        Returns:
            str | None: The validated and normalized RUT string to be stored in the database, or None if the input was None.
        """
        if value is None:
            return None

        try:
            validated_rut = RutValidator.validate(str(value))
            return validated_rut.normalized
        except Exception as e:
            raise ValueError(str(e))

    def process_result_value(self, value: Any, dialect: Dialect) -> str | None:
        """
        The `process_result_value` method is called when a value is being retrieved from the database.
        This is where we can convert the stored string back into a RutStr object for easier manipulation in Python.

        Args:
            value (Any): The value retrieved from the database. This can be a string or None.
            dialect (Dialect): The SQLAlchemy dialect in use.

        Returns:
            str | None: The stored normalized RUT string, or None if the input was None.
        """
        if value is None:
            return None

        return value

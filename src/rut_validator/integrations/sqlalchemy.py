"""SQLAlchemy 2 integration."""

from sqlalchemy import Dialect
from sqlalchemy.types import String, TypeDecorator

from ..errors import RutValidationError
from ..validation import validate_rut


class RutSQLAlchemy(TypeDecorator[str]):
    """SQLAlchemy type that stores RUTs as normalized strings."""

    impl = String(9)
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect: Dialect) -> str | None:
        """Validate and normalize a value before binding it to a statement."""
        del dialect
        if value is None:
            return None
        try:
            return validate_rut(value).normalized
        except RutValidationError as exc:
            raise ValueError(str(exc)) from exc

    def process_result_value(self, value: str | None, dialect: Dialect) -> str | None:
        """Validate normalized RUT text loaded from the database."""
        del dialect
        if value is None:
            return None
        try:
            return validate_rut(value).normalized
        except RutValidationError as exc:
            raise ValueError("La base de datos contiene un RUT inválido") from exc


__all__ = ["RutSQLAlchemy"]

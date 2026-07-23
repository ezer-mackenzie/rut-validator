"""SQLAlchemy 2 integration."""

from typing import Optional

from sqlalchemy import Dialect
from sqlalchemy.types import String, TypeDecorator

from ..errors import RutValidationError
from ..validation import RutValidator


class RutType(TypeDecorator[str]):
    """Store a valid RUT as a normalized nine-character string."""

    impl = String(9)
    cache_ok = True

    def process_bind_param(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[str]:
        del dialect

        if value is None:
            return None

        try:
            return RutValidator.validate(value).normalized

        except RutValidationError as exc:
            raise ValueError(str(exc)) from exc

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[str]:
        del dialect
        return value


RutSQLAlchemy = RutType

__all__ = ["RutSQLAlchemy", "RutType"]

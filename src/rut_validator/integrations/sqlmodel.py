"""Helpers for using validated RUT strings with SQLModel."""

from typing import Any

from sqlmodel import Field

from .pydantic import RutPydantic
from .sqlalchemy import RutSQLAlchemy


class RutSQLModel(RutPydantic):
    """Validated RUT type intended for SQLModel attributes."""


def rut_sqlmodel_field(**kwargs: Any) -> Any:
    """Create a SQLModel field backed by :class:`RutSQLAlchemy`.

    Examples:
        ``rut: RutSQLModel = rut_sqlmodel_field(index=True, unique=True)``
    """

    return Field(sa_type=RutSQLAlchemy, **kwargs)


__all__ = ["RutSQLModel", "rut_sqlmodel_field"]

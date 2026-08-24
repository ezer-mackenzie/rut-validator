"""Helpers for using validated RUT strings with SQLModel."""

from typing import Any, cast

from pydantic.fields import FieldInfo
from sqlmodel import Field

from .pydantic import RutPydantic
from .sqlalchemy import RutSQLAlchemy


class RutSQLModel(RutPydantic):
    """Validated RUT type intended for SQLModel attributes."""


def rut_sqlmodel_field(**kwargs: Any) -> FieldInfo:
    """Create a SQLModel field backed by :class:`RutSQLAlchemy`.

    Examples:
        ``rut: Annotated[RutSQLModel, rut_sqlmodel_field(unique=True)]``
    """

    return cast(FieldInfo, Field(sa_type=RutSQLAlchemy, **kwargs))


__all__ = ["RutSQLModel", "rut_sqlmodel_field"]

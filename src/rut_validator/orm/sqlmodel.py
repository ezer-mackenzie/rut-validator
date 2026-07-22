"""Helpers for using validated RUT strings with SQLModel."""

from typing import Any

from sqlmodel import Field

from rut_validator.orm.pydantic import RutStr
from rut_validator.orm.sqlalchemy import RutType


def RutField(**kwargs: Any) -> Any:
    """Create a SQLModel field backed by :class:`RutType`.

    Use it as ``rut: RutStr = RutField(index=True, unique=True)``.
    """

    return Field(sa_type=RutType, **kwargs)


__all__ = ["RutField", "RutStr"]

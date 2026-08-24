"""Compatibility imports for the former SQLAlchemy integration path."""

from typing import TYPE_CHECKING, Any

from ._compat import warn_for_legacy_import

if TYPE_CHECKING:
    from ..integrations.sqlalchemy import RutSQLAlchemy

__all__ = ["RutSQLAlchemy"]


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(name)

    warn_for_legacy_import(
        "rut_validator.orm.sqlalchemy",
        "rut_validator.integrations.sqlalchemy",
    )
    from ..integrations import sqlalchemy

    value = getattr(sqlalchemy, name)
    globals()[name] = value
    return value

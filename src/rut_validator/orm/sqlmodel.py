"""Compatibility imports for the former SQLModel integration path."""

from typing import TYPE_CHECKING, Any

from ._compat import warn_for_legacy_import

if TYPE_CHECKING:
    from ..integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field

__all__ = ["RutSQLModel", "rut_sqlmodel_field"]


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(name)

    warn_for_legacy_import(
        "rut_validator.orm.sqlmodel",
        "rut_validator.integrations.sqlmodel",
    )
    from ..integrations import sqlmodel

    value = getattr(sqlmodel, name)
    globals()[name] = value
    return value

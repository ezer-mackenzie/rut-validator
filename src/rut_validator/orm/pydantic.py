"""Compatibility imports for the former Pydantic integration path."""

from typing import TYPE_CHECKING, Any

from ._compat import warn_for_legacy_import

if TYPE_CHECKING:
    from ..integrations.pydantic import RutPydantic

__all__ = ["RutPydantic"]


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(name)

    warn_for_legacy_import(
        "rut_validator.orm.pydantic",
        "rut_validator.integrations.pydantic",
    )
    from ..integrations import pydantic

    value = getattr(pydantic, name)
    globals()[name] = value
    return value

"""Compatibility imports for the former Django integration path."""

from typing import TYPE_CHECKING, Any

from ._compat import warn_for_legacy_import

if TYPE_CHECKING:
    from ..integrations.django import RutDjango, RutDjangoValidator

__all__ = ["RutDjango", "RutDjangoValidator"]


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(name)

    warn_for_legacy_import(
        "rut_validator.orm.django",
        "rut_validator.integrations.django",
    )
    from ..integrations import django

    value = getattr(django, name)
    globals()[name] = value
    return value

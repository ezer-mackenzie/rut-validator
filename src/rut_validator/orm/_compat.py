"""Compatibility helpers for deprecated ORM import paths."""

from warnings import warn


def warn_for_legacy_import(old_module: str, new_module: str) -> None:
    """Warn when a symbol is loaded from a legacy integration module."""
    warn(
        f"{old_module} is deprecated; import from {new_module} instead. "
        "The legacy path will be removed in rut-validator 2.0.0.",
        DeprecationWarning,
        stacklevel=3,
    )

"""Shared deprecation warnings for the version 2 migration."""

from warnings import warn


def warn_deprecated(name: str, replacement: str, *, stacklevel: int = 3) -> None:
    """Warn that *name* will be removed in version 2."""
    warn(
        f"{name} is deprecated; use {replacement} instead. "
        "It will be removed in rut-validator 2.0.0.",
        DeprecationWarning,
        stacklevel=stacklevel,
    )

"""Compatibility import; use :mod:`rut_validator.orm.django`."""

from rut_validator.orm.django import RUTField, RutDjangoValidator

__all__ = ["RUTField", "RutDjangoValidator"]

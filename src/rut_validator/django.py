"""Public Django integration; install with ``rut-validator[django]``."""

from rut_validator.orm.django import RUTField, RutDjangoValidator

__all__ = ["RUTField", "RutDjangoValidator"]

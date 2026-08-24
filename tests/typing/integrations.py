"""Static contract fixtures for optional integrations."""

from typing import Annotated

from django.db.models import Field as DjangoField
from pydantic.fields import FieldInfo
from sqlalchemy.types import TypeDecorator
from sqlmodel import SQLModel

from rut_validator.integrations.django import RutDjango
from rut_validator.integrations.pydantic import RutPydantic
from rut_validator.integrations.sqlalchemy import RutSQLAlchemy
from rut_validator.integrations.sqlmodel import RutSQLModel, rut_sqlmodel_field

pydantic_value: RutPydantic = RutPydantic("12.345.678-5")
django_field: DjangoField[str, str] = RutDjango()
sqlalchemy_type: TypeDecorator[str] = RutSQLAlchemy()
sqlmodel_field: FieldInfo = rut_sqlmodel_field(unique=True)


class Person(SQLModel, table=True):
    rut: Annotated[RutSQLModel, rut_sqlmodel_field(unique=True)]

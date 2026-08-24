from typing import ClassVar

import django
import pytest
from django import forms
from django.conf import settings
from django.db import IntegrityError, connection, models

from rut_validator.integrations.django import RutDjango

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        INSTALLED_APPS=[],
        SECRET_KEY="rut-validator-tests",
    )
    django.setup()


class Person(models.Model):
    rut = RutDjango(unique=True)

    class Meta:
        app_label = "rut_validator_tests"


class OptionalPerson(models.Model):
    rut = RutDjango(null=True, blank=True)

    class Meta:
        app_label = "rut_validator_tests"


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields: ClassVar = ["rut"]


@pytest.fixture(autouse=True)
def person_tables():
    with connection.schema_editor() as editor:
        editor.create_model(Person)
        editor.create_model(OptionalPerson)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(OptionalPerson)
        editor.delete_model(Person)


def test_model_full_clean_and_database_round_trip_normalize_value():
    person = Person(rut="12.345.678-5")

    person.full_clean()
    person.save()
    stored = Person.objects.get(pk=person.pk)

    assert person.rut == "123456785"
    assert stored.rut == "123456785"


def test_model_form_validates_and_normalizes_value():
    form = PersonForm(data={"rut": "12.345.678-5"})

    assert form.is_valid(), form.errors
    assert form.instance.rut == "123456785"


def test_optional_field_accepts_none():
    person = OptionalPerson(rut=None)

    person.full_clean()
    person.save()

    assert OptionalPerson.objects.get(pk=person.pk).rut is None


def test_unique_constraint_is_enforced():
    Person.objects.create(rut="123456785")

    with pytest.raises(IntegrityError):
        Person.objects.create(rut="12.345.678-5")


def test_field_deconstruct_uses_stable_public_path():
    _, path, args, kwargs = RutDjango().deconstruct()

    assert path == "rut_validator.integrations.django.RutDjango"
    assert args == []
    assert kwargs["max_length"] == 9

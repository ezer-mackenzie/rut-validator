rut-validator
===================

.. image:: https://badge.fury.io/py/rut-validator.svg
   :target: https://pypi.org/project/rut-validator/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/rut-validator.svg
   :target: https://pypi.org/project/rut-validator/
   :alt: Python versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

Librería para validar RUT chileno con enfoque Pydantic-first y soporte completo para frameworks web.

Características principales
--------------------------

✅ **Validación pura de RUT chileno** usando algoritmo módulo 11
✅ **Detección automática de formato**: dotted (``12.345.678-9``), hyphenated (``12345678-9``), numeric (``123456789``)
✅ **Integración completa con Pydantic** (``RutStr``)
✅ **Campo Django** (``RUTField``) listo para usar
✅ **Tipo SQLAlchemy** (``RutSQLAlchemy``) para bases de datos
✅ **Compatible con FastAPI** y otros frameworks web
✅ **Type hints completos** para mejor desarrollo
✅ **Sin dependencias externas** para funcionalidad core
✅ **Tests exhaustivos** con alta cobertura

Instalación
-----------

.. code-block:: bash

   pip install rut-validator

   # Con soporte Pydantic
   pip install rut-validator[pydantic]

   # Con soporte FastAPI
   pip install rut-validator[fastapi]

   # Para desarrollo
   pip install rut-validator[dev]

Uso básico
----------

Validación simple
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rut_validator import RutValidator

   # Validar RUT con cualquier formato
   rut = RutValidator.validate("20.884.437-7")
   print(f"RUT válido: {rut.formatted}")  # "20.884.437-7"
   print(f"Número: {rut.number}")          # 20884437
   print(f"Dígito: {rut.digit}")          # "7"
   print(f"Formato: {rut.format}")        # RutFormat.DOTTED

Detección de formato
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rut_validator import RutValidator

   # La librería detecta automáticamente el formato de entrada
   formats = [
       "20.884.437-7",  # Formato dotted
       "20884437-7",    # Formato hyphenated
       "208844377",     # Formato numeric
   ]

   for rut_str in formats:
       rut = RutValidator.validate(rut_str)
       print(f"'{rut_str}' -> Formato: {rut.format}, Es dotted: {rut.is_dotted}")

Con Pydantic
~~~~~~~~~~~~

.. code-block:: python

   from pydantic import BaseModel
   from rut_validator import RutStr

   class User(BaseModel):
       name: str
       rut: RutStr  # Validación automática

   # Uso
   user = User(name="Juan Pérez", rut="12.345.678-5")
   print(user.rut)  # "12.345.678-5"

Contenido
---------

.. toctree::
   :maxdepth: 2
   :caption: Guías de usuario:

   installation
   quickstart
   pydantic-integration
   django-integration
   sqlalchemy-integration
   fastapi-integration

.. toctree::
   :maxdepth: 2
   :caption: Referencia de API:

   api-reference

.. toctree::
   :maxdepth: 2
   :caption: Desarrollo:

   contributing
   changelog

Índices y tablas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
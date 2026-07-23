# rut-validator

[![PyPI version](https://badge.fury.io/py/rut-validator.svg)](https://pypi.org/project/rut-validator/)
[![Python versions](https://img.shields.io/pypi/pyversions/rut-validator.svg)](https://pypi.org/project/rut-validator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ezer-mackenzie/rut-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/ezer-mackenzie/rut-validator/actions)
[![codecov](https://codecov.io/gh/ezer-mackenzie/rut-validator/branch/main/graph/badge.svg)](https://codecov.io/gh/ezer-mackenzie/rut-validator)
[![Documentation Status](https://readthedocs.org/projects/rut-validator/badge/?version=latest)](https://rut-validator.readthedocs.io/en/latest/?badge=latest)

Librería para validar RUT chileno con enfoque Pydantic-first y soporte completo para frameworks web.

## ✨ Características

- ✅ **Validación pura de RUT chileno** usando algoritmo módulo 11
- ✅ **Detección automática de formato**: dotted (`12.345.678-9`), hyphenated (`12345678-9`), numeric (`123456789`)
- ✅ **Integración completa con Pydantic** (`RutStr`)
- ✅ **Campo Django** (`RUTField`) listo para usar
- ✅ **Tipo SQLAlchemy** (`RutSQLAlchemy`) para bases de datos
- ✅ **Integración SQLModel** con almacenamiento normalizado
- ✅ **Compatible con FastAPI** y otros frameworks web
- ✅ **Type hints completos** para mejor desarrollo
- ✅ **Sin dependencias externas** para funcionalidad core
- ✅ **Tests exhaustivos** con alta cobertura

## 🚀 Instalación

```bash
pip install rut-validator

# Con soporte Pydantic
pip install rut-validator[pydantic]

# Con soporte para una integración concreta
pip install rut-validator[sqlalchemy]
pip install rut-validator[django]
pip install rut-validator[sqlmodel]

# Con soporte FastAPI
pip install rut-validator[fastapi]

# Todas las integraciones
pip install rut-validator[all]

# Para desarrollo
pip install rut-validator[dev]
```

## 📖 Uso Básico

### Validación Simple

```python
from rut_validator import RutValidator

# Validar RUT con cualquier formato
rut = RutValidator.validate("20.884.437-7")
print(f"RUT válido: {rut.formatted}")  # "20.884.437-7"
print(f"Número: {rut.body}")           # 20884437
print(f"Dígito: {rut.check_digit}")    # "7"
print(f"Formato: {rut.format}")        # RutFormat.FORMATTED
```

Para un uso funcional más directo:

```python
from rut_validator import calculate_check_digit, validate_rut

rut = validate_rut("12.345.678-5")
assert rut.normalized == "123456785"
assert calculate_check_digit("12345678") == "5"
```

### Detección de Formato

```python
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
```

### Con Pydantic

```python
from pydantic import BaseModel
from rut_validator.orm.pydantic import RutStr

class User(BaseModel):
    name: str
    rut: RutStr  # Validación automática

# Uso
user = User(name="Juan Pérez", rut="12.345.678-5")
print(user.rut)  # "123456785" (normalizado)
```

### Con Django

```python
from django.db import models
from rut_validator.orm.django import RUTField

class Person(models.Model):
    name = models.CharField(max_length=100)
    rut = RUTField(unique=True)  # Validación automática en DB
```

### Con SQLAlchemy

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from rut_validator.orm.sqlalchemy import RutType

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rut = Column(RutType)  # Validación y normalización automáticas
```

## 📚 Documentación

Lee la documentación completa en [docs/index.md](docs/index.md) o constrúyela
localmente:

```bash
poetry install --all-extras
poetry run mkdocs serve
```

## 🧪 Ejemplos

- [Validación pura](examples/01_pure_validation.py)
- [Uso con Pydantic](examples/02_pydantic_usage.py)
- [Uso con FastAPI](examples/03_fastapi_usage.py)
- [Uso del CLI](examples/04_cli_usage.py)
- [Uso con SQLModel](examples/05_sqlmodel_usage.py)

## 🔧 Desarrollo

### Configuración del entorno

```bash
# Clonar repositorio
git clone https://github.com/ezer-mackenzie/rut-validator.git
cd rut-validator

# Instalar dependencias de desarrollo
poetry install --with dev

# Ejecutar tests
poetry run pytest

# Ejecutar linting
poetry run black src/ tests/
poetry run isort src/ tests/
poetry run flake8 src/ tests/
poetry run mypy src/rut_validator/
```

### Pre-commit hooks

```bash
poetry run pre-commit install
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Algoritmo de validación basado en el estándar chileno del Servicio de Impuestos Internos
- Inspirado en bibliotecas similares pero con enfoque moderno y tipado fuerte

## 📞 Soporte

- 🐛 [Reportar bugs](https://github.com/ezer-mackenzie/rut-validator/issues)
- 💡 [Sugerir features](https://github.com/ezer-mackenzie/rut-validator/issues)
- 📖 [Documentación](https://rut-validator.readthedocs.io/)

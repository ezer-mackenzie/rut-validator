# Auditoría y TODO para `rut-validator` v1.0

Fecha de auditoría: 2026-07-22

## Veredicto

El proyecto todavía no está listo para publicar como 1.0. El algoritmo base funciona para los casos cubiertos, el wheel se construye y `mypy` pasa, pero hay bloqueos de instalación, API pública, tests, CLI, documentación y compatibilidad declarada. La prioridad debe ser fijar primero el contrato público y luego hacer que todas las integraciones lo reutilicen.

## Estado observado

- [x] El wheel y el sdist se construyen con Poetry.
- [x] `mypy src/rut_validator` pasa (con integraciones ignoradas parcialmente).
- [x] Cobertura global observada: 91%.
- [ ] Suite verde: 28 tests pasan y 2 fallan por `Rut.is_dotted` inexistente.
- [ ] Ruff verde: hay un import no usado en el ejemplo FastAPI.
- [ ] Instalación standalone funcional: el import desde un wheel sin extras falla por Pydantic.
- [ ] CLI funcional: el entry point referencia `rut_validator.cli:cli`, que no existe.
- [ ] Ejemplos ejecutables: los ejemplos 01 y 02 fallan.
- [ ] Documentación construible con `sphinx-build -W`.
- [ ] CI real y versionado soportado verificados.
- [ ] Integración SQLModel implementada y probada.

## P0 — Bloqueos antes de cualquier 1.0

### 1. Definir y congelar el contrato público

- [ ] Elegir nombres canónicos y consistentes:
  - `RutFormat.FORMATTED` vs el término documentado `DOTTED`.
  - `Rut.body`/`Rut.check_digit` vs `number`/`digit`.
  - `is_formatted`/`is_normalized` vs `is_dotted`/`is_numeric`.
- [ ] Recomendación: conservar `body`, `check_digit`, `is_formatted`, `is_hyphenated`, `is_normalized` como API canónica y añadir alias de compatibilidad (`number`, `digit`, `is_dotted`, `is_numeric`) con documentación clara. No eliminar alias hasta una futura versión mayor.
- [ ] Exportar desde `rut_validator` solamente símbolos estables: `Rut`, `RutValidator`, `RutFormat`, `ValidationResult` y errores. Decidir si se mantiene `ValidatedRut` como alias documentado.
- [ ] Añadir tests de contrato para todos los exports y atributos documentados.
- [ ] Obtener `__version__` desde metadata (`importlib.metadata`) o una única fuente; evitar duplicarlo entre `pyproject.toml`, `__init__.py` y Sphinx.

**Aceptación:** README, docstrings, ejemplos y tests usan exactamente la misma API; no hay atributos prometidos que no existan.

### 2. Hacer el core realmente standalone

- [ ] Quitar Django y SQLAlchemy de `project.dependencies`; moverlos a extras `django` y `sqlalchemy`.
- [ ] Quitar el import incondicional de `RutStr` desde `rut_validator.__init__`, o implementar un export diferido que dé un error de instalación explícito sólo al pedir `RutStr`.
- [ ] Crear extras coherentes, por ejemplo:
  - `pydantic = [pydantic>=2,...]`
  - `sqlalchemy = [sqlalchemy>=2,...]`
  - `sqlmodel = [sqlmodel compatible,...]`
  - `django = [...]`
  - `fastapi = [fastapi..., pydantic...]`
  - `all = [...]`
- [ ] Quitar Click de dependencias base si se elimina el CLI, o mantenerlo sólo si se implementa el CLI para v1.
- [ ] Probar wheels en entornos limpios: base sin extras y cada extra por separado.
- [ ] Añadir mensajes de error útiles cuando falta una dependencia opcional.

**Aceptación:** `pip install rut-validator` seguido de `from rut_validator import Rut, RutValidator` funciona sin Pydantic, Django, SQLAlchemy ni Click instalados.

### 3. Corregir robustez del core

- [ ] Hacer que todas las entradas públicas manejen tipos no `str` de forma deliberada. Hoy `None`, `int`, `bytes` y listas filtran `AttributeError`/`TypeError` desde `.strip()` o regex.
- [ ] Recomendación de contrato:
  - `validate(value)` exige `str` y lanza `RutInvalidValueError` para `None`/tipo incorrecto.
  - `is_valid(value)` nunca lanza por entrada del usuario y retorna `False` para cualquier tipo/formato inválido.
  - `get_validation_result(value)` retorna `INVALID_VALUE` para `None`, vacío o tipo incorrecto.
- [ ] No aceptar `skip_validation=True` como parte pública de `Rut`; sustituirlo por constructor interno seguro (`_from_validated`) para que nadie cree objetos inválidos accidentalmente.
- [ ] Validar antes de formatear. `RutPatterns.normalize/formatted/hyphenated` actualmente limpian caracteres arbitrarios y pueden ocultar entradas inválidas.
- [ ] Decidir explícitamente reglas de negocio: cantidad mínima/máxima de dígitos, ceros iniciales y si `00000000-0` se considera válido. Documentarlas con fuentes/criterio de dominio.
- [ ] Considerar límites de tamaño antes de regex y cálculo para evitar trabajo innecesario con entradas gigantes.
- [ ] Usar logging parametrizado (`logger.debug("... %s", value)`) y no registrar RUT completos por defecto, ya que son datos personales.
- [ ] Acortar mensajes y preservar la excepción original con `raise ... from e` sólo donde aporte contexto; no capturar `Exception` de forma amplia en adapters.
- [ ] Convertir factores a tupla constante tipada y simplificar imports/orden/formato.

**Aceptación:** ninguna entrada inválida produce excepciones internas inesperadas; el comportamiento es idéntico en `Rut`, validator y adapters.

### 4. Resolver compatibilidad de Python

- [ ] El código Django y SQLAlchemy usa `str | None`, sintaxis que Python 3.9 no puede parsear sin `from __future__ import annotations` (y el operador de unión igualmente requiere parser compatible). Añadir future imports donde corresponda o usar `Optional`.
- [ ] Decidir una matriz realista para v1: recomendar Python 3.10–3.13, o mantener 3.9 sólo si CI lo ejecuta de verdad.
- [ ] No prometer Python 3.14 hasta que las dependencias e integraciones lo soporten y CI lo pruebe.
- [ ] Añadir CI por versión y por extras; no basta correr todo en un único entorno con todas las dependencias presentes.

**Aceptación:** cada versión declarada en classifiers y `requires-python` instala, importa y ejecuta la suite.

### 5. Corregir Pydantic v2

- [ ] Elegir uno de dos contratos, sin mezclarlos:
  1. `RutStr`: subtipo de `str`, almacena normalizado y sólo ofrece comportamiento de string.
  2. `Rut`: value object rico, con serializer JSON a string y schema Pydantic propio.
- [ ] Recomendación: ofrecer ambos. `RutStr` para máxima interoperabilidad y `Rut` para `.formatted`, `.body`, etc.
- [ ] Corregir el core schema para que `RutStr` devuelva `cls(normalized)` sin recursión; hoy el modelo Pydantic devuelve un `str` plano, no `RutStr`.
- [ ] No hacer que ejemplos de `RutStr` accedan a `.formatted`, `.number` o `.digit` salvo que esas propiedades se implementen realmente.
- [ ] Definir coerción estricta: `str_schema(strict=True)` si enteros/bytes no deben aceptarse.
- [ ] Corregir JSON Schema: el patrón publicado no incluye correctamente todos los formatos aceptados, usa límites inconsistentes y `example` debería alinearse con la normalización. Considerar `examples` y un `format` propio.
- [ ] Añadir serializer explícito y tests para `model_dump`, `model_dump_json`, JSON Schema, listas/opcionales/uniones, assignment validation, defaults y FastAPI request/response.
- [ ] Probar Pydantic 2.x mínimo y último soportado; no fijar innecesariamente un mínimo tan reciente si el código soporta versiones anteriores.
- [ ] Añadir `TypeAdapter` y tests de anotaciones reutilizables.

**Aceptación:** el tipo resultante, su serialización y el OpenAPI coinciden con lo documentado.

### 6. Implementar SQLModel como integración de primera clase

- [ ] Añadir extra `sqlmodel` y una ruta pública documentada.
- [ ] Reutilizar el tipo Pydantic para validación en creación del modelo y el `TypeDecorator` SQLAlchemy para persistencia normalizada.
- [ ] Proveer un patrón estable, por ejemplo un tipo/anotación `RutField` o helper de `Field(sa_type=...)`, evitando duplicar el algoritmo.
- [ ] Decidir tipo de atributo en runtime (`RutStr`, `Rut` o `str`) y tipo almacenado (`VARCHAR(9)` normalizado recomendado).
- [ ] Probar con SQLite real:
  - create/drop metadata;
  - insert válido en los tres formatos;
  - rechazo inválido antes de commit;
  - round-trip y consultas;
  - `Optional`/`nullable`;
  - `unique` e índice;
  - serialización Pydantic/JSON;
  - carga desde DB de un valor corrupto (política explícita).
- [ ] Añadir ejemplo completo de modelo SQLModel y sesión.

**Aceptación:** un modelo SQLModel valida al instanciar, persiste normalizado y recupera el tipo documentado.

### 7. Reparar o retirar el CLI

- [ ] Decidir si el CLI forma parte de v1.
- [ ] Si sí: crear `rut_validator/cli.py` o corregir el entry point; implementar y probar los comandos prometidos (`validate`, `format`, `info`, `batch`, JSON, quiet y exit codes).
- [ ] Si no: eliminar `[project.scripts]`, Click, guía y ejemplo CLI para no publicar una función rota.
- [ ] Evitar `shell=True` en ejemplos; usar listas de argumentos.
- [ ] Añadir tests con `CliRunner`, stdout/stderr, JSON estable y códigos 0/1/2.

**Aceptación:** `rut-validator --help` funciona desde el wheel instalado o no existe ninguna promesa de CLI.

## P1 — Integraciones ORM y calidad de producción

### 8. SQLAlchemy

- [ ] Renombrar a un nombre de tipo convencional y claro (`RUTType` o `RutType`), manteniendo alias si hace falta.
- [ ] Declarar longitud (`String(9)`) y documentar que se almacena normalizado.
- [ ] Aceptar únicamente tipos documentados; no convertir cualquier objeto con `str(value)` silenciosamente.
- [ ] Traducir sólo `RutValidationError`, no `Exception` genérica.
- [ ] Decidir si `process_result_value` valida datos de DB o confía y devuelve `str`/`Rut`.
- [ ] Añadir tests de integración con engine/session SQLite, nullability, rollback, queries, bulk insert y round-trip; los actuales llaman métodos directamente y no prueban ORM real.
- [ ] Añadir typing SQLAlchemy 2 (`Mapped`, `mapped_column`) en documentación y ejemplo.

### 9. Django

- [ ] Mover el validator fuera de `__init__`; una closure puede dificultar serialización/deconstruction de migraciones.
- [ ] Implementar `deconstruct()` si hay configuración propia y probar `makemigrations`/serialización del field.
- [ ] Respetar `blank`, `null`, validators de `CharField`, forms y `full_clean()`.
- [ ] No capturar `Exception` general en `to_python`.
- [ ] Definir si `to_python` debe normalizar al leer y escribir, y cómo trata valores ya convertidos.
- [ ] Añadir `default_error_messages`, código de error estable e i18n con `gettext_lazy`.
- [ ] Probar un modelo real con SQLite: save/load, ModelForm, unique, null/blank y migración.
- [ ] Revisar rango Django: el declarado `<5.0` deja fuera versiones actuales; soportar una matriz vigente o documentar la limitación.

### 10. Diseño/refactor interno

- [ ] Separar claramente: parseo estricto, cálculo del DV, validación y representación.
- [ ] Evitar que `RutParser.destructure` y `Rut` repitan decisiones de validación.
- [ ] Considerar una función pura pública (`calculate_check_digit(body)`) y otra (`validate_rut(value)`) además de la clase estática, si simplifica uso standalone.
- [ ] Hacer `Rut` inmutable (`frozen=True` o implementación equivalente) porque es hashable; hoy `value` puede mutar y romper sets/dicts.
- [ ] Si se usa dataclass, no combinar decorador con un `__init__` manual sin una razón clara; aplicar `slots=True`, `frozen=True` de forma coherente.
- [ ] Guardar una representación canónica interna para no normalizar repetidamente en cada propiedad.
- [ ] Alinear `RutFormatter` y `RutPatterns`: ahora el formatter es una capa casi vacía y no está bien cubierta. Eliminarlo o convertirlo en la única API de formato.
- [ ] Reexportar adapters desde módulos públicos amigables (`rut_validator.pydantic`, `rut_validator.sqlalchemy`, etc.) en vez de rutas `core.orm...`.

## P1 — Tests imprescindibles

- [ ] Tests exhaustivos del algoritmo para resultados `0`, `K` y `1..9`, mayúscula/minúscula y vectores conocidos.
- [ ] Tests parametrizados de los tres formatos y equivalencia entre ellos.
- [ ] Entradas: `None`, bool, int, bytes, espacios, Unicode, guiones/puntos extra, saltos de línea, largos extremos y caracteres similares a dígitos.
- [ ] Formato punteado estricto, ceros iniciales y cuerpos en límites admitidos.
- [ ] Tests de excepciones exactas, mensajes/códigos estables y `ValidationResult`.
- [ ] Tests de inmutabilidad, igualdad, hash, repr, str y pickle/copy si se prometen.
- [ ] Tests de API pública/imports con y sin extras.
- [ ] Tests de wheel instalado, no sólo imports desde el checkout.
- [ ] Tests de ejemplos (smoke o doctest) para impedir documentación ejecutable rota.
- [ ] Property-based tests con Hypothesis: generar cuerpos, calcular DV, validar y mutar DV para comprobar rechazo.
- [ ] Mutation testing opcional para demostrar que los tests detectan errores en módulo 11.
- [ ] Fijar umbral de cobertura (recomendado >=95% en core; adapters medidos por separado) sin usar cobertura como sustituto de escenarios.

## P1 — Empaquetado, CI y release

- [ ] Corregir URLs `yourusername` por `ezer-mackenzie` en metadata, badges y documentación.
- [ ] Añadir/recuperar un workflow CI no vacío y versionado; actualmente `.github/workflows/ci.yml` está sin seguimiento y vacío.
- [ ] CI: lint/format, typing, tests por versión, tests por extra, build, `twine check`, instalación del wheel y docs.
- [ ] Verificar `poetry.lock` tras reorganizar extras.
- [ ] Añadir chequeo de metadata/README renderizado (`twine check dist/*`).
- [ ] Añadir pre-commit real si se anuncia; no se observó configuración `.pre-commit-config.yaml`.
- [ ] Usar un solo linter/formatter principal o configurar Black/isort/Ruff sin reglas contradictorias.
- [ ] No publicar desde una release si CI y artefactos no han pasado; idealmente construir una vez y publicar el artefacto probado.
- [ ] Probar en TestPyPI y realizar smoke test en entorno limpio antes del tag 1.0.
- [ ] Cambiar classifier de Beta a Production/Stable sólo cuando se cumplan gates.

## P2 — Documentación y experiencia de usuario

- [ ] Corregir todos los RUT de ejemplo: varios usan `12345678-9`, pero el DV correcto calculado por la librería es `5`.
- [ ] Actualizar ejemplos para la API elegida y ejecutarlos en CI.
- [ ] Arreglar Sphinx: falta `linkify-it-py` para la extensión activada, falta `_static`, y el toctree referencia páginas inexistentes (`installation`, `quickstart`, integraciones, API, contributing, changelog).
- [ ] Decidir entre documentación Markdown existente y páginas RST; eliminar duplicación y contradicciones.
- [ ] Corregir afirmaciones falsas: “tests exhaustivos”, “CI/CD”, “soporte completo” y “sin dependencias” todavía no se cumplen.
- [ ] Documentar formatos aceptados, canonicalización, privacidad del RUT, errores, typing y política de compatibilidad.
- [ ] Añadir una tabla clara de instalación por extra y compatibilidad de versiones.
- [ ] Incluir ejemplos standalone, Pydantic, FastAPI, SQLAlchemy 2, SQLModel y Django que se ejecuten.
- [ ] Actualizar copyright/fechas y enlazar changelog real.
- [ ] Definir política semver: qué partes son API pública y cuáles internas.

## Seguridad y privacidad

- [ ] Evitar loguear el RUT completo en `debug`, `info` y `warning`; enmascarar o eliminar esos logs.
- [ ] No presentar validación de módulo 11 como verificación de identidad o existencia ante el SII.
- [ ] Documentar que el RUT es dato personal y que normalizar no equivale a autorización para almacenarlo.
- [ ] Añadir pruebas contra entradas desproporcionadas y revisar exposición de datos en errores/logs.
- [ ] Revisar dependencias con Dependabot/pip-audit en CI, sin convertirlo en garantía absoluta.

## Gates de salida para v1.0

- [ ] Contrato público escrito y estable.
- [ ] Core sin dependencias externas y wheel base importable en entorno limpio.
- [ ] Suite, Ruff/format, mypy, build, metadata y docs verdes.
- [ ] CI cubre todas las versiones Python y versiones mínimas/máximas de adapters declaradas.
- [ ] Pydantic, SQLAlchemy, SQLModel y Django tienen pruebas de integración reales.
- [ ] Ejemplos ejecutables y documentación sin APIs ficticias.
- [ ] CLI implementado y probado, o completamente retirado.
- [ ] Cobertura de casos límite y property-based tests del algoritmo.
- [ ] URLs, classifiers, changelog y política de soporte correctos.
- [ ] Release candidate instalada desde wheel y validada en proyecto standalone y proyectos con cada extra.

## Orden recomendado de implementación

1. Congelar API y reglas de dominio.
2. Corregir core, value object y tipos de entrada.
3. Separar dependencias opcionales y probar instalación limpia.
4. Reparar Pydantic y definir serialización.
5. Refactorizar SQLAlchemy y construir SQLModel encima.
6. Endurecer Django.
7. Implementar o retirar CLI.
8. Rehacer tests de integración, ejemplos y docs.
9. Activar matriz CI/release gates.
10. Publicar `1.0.0rc1`, probar consumidores reales y luego `1.0.0`.

## Comandos de verificación sugeridos

```bash
poetry run ruff check src tests examples
poetry run black --check src tests examples
poetry run mypy src/rut_validator
poetry run pytest --cov=rut_validator --cov-report=term-missing
poetry build
python -m twine check dist/*
python -m venv /tmp/rut-clean
/tmp/rut-clean/bin/pip install --no-deps dist/*.whl
/tmp/rut-clean/bin/python -c "from rut_validator import RutValidator; assert RutValidator.is_valid('12.345.678-5')"
sphinx-build -W -b html docs /tmp/rut-docs
```

## Evidencia puntual de esta auditoría

- Suite: 2 fallos por `is_dotted` ausente.
- Wheel standalone: `ModuleNotFoundError: No module named 'pydantic'` al importar el paquete.
- CLI: `ModuleNotFoundError: No module named 'rut_validator.cli'`.
- Pydantic: un campo `RutStr` válido termina siendo `<class 'str'>` y no posee `.formatted`.
- Ejemplos: usan DV erróneos y propiedades ausentes; terminan con excepción.
- Tipos no string: filtran `AttributeError`/`TypeError` desde el core.
- Docs: build estricto falla por dependencia/configuración y contiene toctrees sin archivos correspondientes.
- Metadata: URLs placeholder y dependencias base incompatibles con la promesa standalone.

# Desarrollo y contribución

## Preparar el entorno

```bash
git clone https://github.com/ezer-mackenzie/rut-validator.git
cd rut-validator
poetry install --all-extras
```

## Verificaciones

```bash
poetry run pytest --cov=rut_validator
poetry run ruff check src tests examples
poetry run black --check src tests examples
poetry run mypy src/rut_validator
poetry run mkdocs build --strict
poetry build
```

## Servir documentación

```bash
poetry run mkdocs serve
```

MkDocs sirve el sitio en `http://127.0.0.1:8000` y recarga al modificar archivos.

## Commits

El proyecto utiliza Conventional Commits:

- `feat:` funcionalidad nueva;
- `fix:` corrección;
- `refactor:` cambio interno;
- `test:` cobertura;
- `docs:` documentación;
- `chore:` mantenimiento y release.

Toda API pública nueva debe incluir tests, documentación y una entrada en el
changelog.

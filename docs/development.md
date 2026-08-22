# Development and contribution

## Set up the environment

```bash
git clone https://github.com/ezer-mackenzie/rut-validator.git
cd rut-validator
poetry install --all-extras
```

## Quality checks

```bash
poetry run pytest --cov=rut_validator
poetry run ruff check src tests examples
poetry run black --check src tests examples
poetry run mypy src/rut_validator
poetry run mkdocs build --strict
poetry build
```

## Serve documentation

```bash
poetry run mkdocs serve
```

MkDocs serves the site at `http://127.0.0.1:8000` and reloads it when files
change.

## Commits

The project uses Conventional Commits:

- `feat:` new functionality;
- `fix:` bug fix;
- `refactor:` internal change;
- `test:` test coverage;
- `docs:` documentation;
- `chore:` maintenance and releases.

Every new public API must include tests, documentation, and a changelog entry.

## Internal dependency direction

The private `rut_validator._engine` module contains dependency-free syntax,
formatting, and modulo-11 primitives shared by the domain object and public
validation APIs. It is not public API.

```text
_engine -> core
_engine -> validation -> core
                         ^
orm ---------------------|
```

`core` must not import `validation`, and neither standalone layer may import an
optional framework. Keep public parsing and formatting entry points in
`rut_validator.validation`; `_engine` exists only to prevent dependency cycles.

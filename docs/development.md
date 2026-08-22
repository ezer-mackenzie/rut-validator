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

## Coverage reporting

The Python 3.14 CI job stores `coverage.xml` as a short-lived GitHub artifact.
After the complete `CI` workflow succeeds, `.github/workflows/codecov.yml`
downloads that artifact and uploads it to Codecov using GitHub OIDC. The root
`codecov.yml` configures Codecov status checks and comments; it is not a GitHub
Actions workflow.

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

The internal `rut_validator.core.engine` module contains syntax, formatting,
and modulo-11 primitives shared by the domain object and public validation
APIs. It uses the canonical `RutFormat` enum and is not public API.

```text
core.engine -> core.Rut
core.engine -> validation -> core.Rut
                               ^
orm ---------------------------|
```

`core` must not import `validation`, and neither standalone layer may import an
optional framework. Keep public parsing and formatting entry points in
`rut_validator.validation`; the private engine exists only to centralize domain
invariants and prevent dependency cycles. ORM adapters consume the public
validation layer, never `core.engine` directly.

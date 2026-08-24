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
core.Rut -----------> core.engine
root API -----------> core.Rut / core.engine
integrations -------> root API
CLI ----------------> root API
legacy facades -----> root API / core.engine
```

`core` must not import `validation`, and neither standalone layer may import an
optional framework. The private engine exists only to centralize domain
invariants and prevent dependency cycles. Integrations consume public validation
helpers, never `core.engine` directly.

## `Rut` design decisions

`Rut` keeps manual equality and hashing during the 1.x to 2.0 migration. A
dataclass-generated equality method would require identical concrete classes,
while the established contract compares `Rut` subclasses by their normalized
value. `value` and `format` also describe the submitted representation and must
not participate in equality.

The manual redacted `repr` remains mandatory because the submitted RUT is
personal data. `value` will continue to preserve the original input in 2.0;
changing it to the normalized representation would combine an unrelated
semantic change with the API cleanup. Applications should use `normalized` when
they need canonical storage.

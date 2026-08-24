# AGENTS.md

This file gives coding agents the minimum context needed to work safely and
efficiently in this repository.

## Project overview

`rut-validator` is a production-stable Python library for validating Chilean
RUT values. It provides a framework-agnostic core, a CLI, and optional adapters
for Pydantic/FastAPI, Django, SQLAlchemy, and SQLModel.

Validation proves only that the syntax and modulo-11 check digit are valid. It
does not prove that a RUT exists, is active, or belongs to a person or company.

## Repository map

- `src/rut_validator/core/`: domain objects, enums, and private invariant
  primitives.
- `src/rut_validator/api.py`: public framework-independent validation helpers.
- `src/rut_validator/integrations/`: canonical optional framework and ORM adapters.
- `src/rut_validator/cli/`: Click-based command-line interface.
- `tests/integrations/`: real optional-framework integration tests.
- `tests/typing/`: static public-contract fixtures checked by mypy.
- `tests/`: unit, property-based, public API, architecture, and CLI tests.
- `docs/`: MkDocs documentation for the public API and integrations.
- `examples/`: runnable usage examples.

## Architectural rules

- Keep the core and API layers framework-agnostic. Private core primitives may
  be consumed by the public API, but adapters must use public
  validation helpers rather than importing internal core modules.
- Importing `rut_validator`, `rut_validator.api`, `rut_validator.core`, or
  `rut_validator.integrations` must not import optional frameworks.
- Keep integrations optional and located in `src/rut_validator/integrations/`.
- Treat `core.engine` as the single private authority for syntax, normalization,
  formatting, and modulo-11 invariants. Do not expose it as public API or wrap
  its stateless functions in namespace classes.
- Do not restore the removed `rut_validator.validation` or `rut_validator.orm`
  packages. Version 2 integrations live only under `rut_validator.integrations`.
- Use `Rut` as the canonical immutable and hashable value object.
- Preserve normalized storage as body plus check digit without separators.
- Preserve textual identity, including leading zeros, across `formatted`,
  `hyphenated`, `str(rut)`, and reparsing. `Rut.body` is numeric and may omit a
  leading zero; `Rut.normalized` is the canonical textual identity.
- Public formatting operations must validate before transforming a value.
- Accept ASCII digits only. Do not silently accept whitespace, Unicode digits,
  alternate hyphens, malformed types, or oversized input.
- Preserve the stable public error codes: `invalid_value`, `invalid_format`, and
  `invalid_check_digit`.
- Do not expose an API that can construct an invalid `Rut` instance.
- Do not log or include a submitted full RUT in structured CLI errors.

## `Rut` implementation invariants

- Keep manual equality and hashing based on `normalized`. Dataclass-generated
  equality requires the same concrete class and would break equality between
  `Rut` and valid subclasses.
- Keep the manually redacted `repr`; submitted RUT values are personal data.
- `object.__setattr__` inside `__post_init__` is intentional and is the supported
  way to initialize derived fields in a frozen dataclass. It does not authorize
  mutation after construction.
- Keep `value` as the original input, `format` as the detected input format, and
  `_normalized` as the cached canonical representation.

## Public API and compatibility

The root package exports the common standalone API, including `Rut`,
`validate_rut`, `is_valid_rut`, and `calculate_check_digit`. Framework-specific
types are imported from `rut_validator.integrations` modules.

The public version 2 surface intentionally excludes the old validation facade
classes, parsing/pattern helpers, `Rut` aliases, and low-level check-digit
comparison. Do not reintroduce them without a new, explicitly approved API
design.

The package follows semantic versioning. Treat removal, renaming, changed error
behavior, and changed accepted input as compatibility-sensitive changes. Every
new public API requires tests, documentation, and a changelog entry.

## Development workflow

Install all development and optional dependencies:

```bash
poetry install --all-extras
```

Run the relevant focused tests while developing, then run the complete quality
checks before finishing:

```bash
poetry run pytest --cov=rut_validator
poetry run ruff check src tests examples
poetry run black --check src tests examples
poetry run mypy src/rut_validator tests/typing
poetry run basedpyright
poetry run actionlint
poetry run mkdocs build --strict
poetry build
```

Coverage must remain at or above 95%. The supported Python versions are 3.10
through 3.14.

## Testing expectations

- Add regression tests for every bug fix.
- Test valid, malformed, boundary, and incorrect-check-digit inputs.
- When changing modulo-11 behavior, preserve or extend the Hypothesis tests in
  `tests/test_properties.py`.
- When changing exports or dependencies, run `tests/test_public_api.py` and
  `tests/test_architecture.py`.
- Changes to adapters must include real integration round trips where relevant.
- Preserve tests proving that standalone imports do not load optional
  frameworks and that integrations never import `core.engine` directly.
- Keep warnings as errors. Add only narrow, documented filters for verified
  third-party warnings; never ignore complete warning categories globally.
- Do not use real personal RUT values in tests, documentation, issues, or logs.

## Typing expectations

- Mypy checks source plus `tests/typing`; basedpyright runs strictly over the
  standalone API, core, errors, and CLI.
- Some framework hook parameters legitimately use `Any` because their upstream
  APIs are dynamic. Prevent `Any` or `Unknown` from escaping through our public
  return types instead of replacing framework contracts with invented types.
- `rut_sqlmodel_field()` returns `FieldInfo`; document and test SQLModel fields
  with `Annotated[RutSQLModel, rut_sqlmodel_field(...)]` so model attributes
  remain precisely typed.

## Style and scope

- Support Python 3.10 syntax and add complete type annotations.
- Keep changes small and consistent with the existing package boundaries.
- Prefer the established public helpers over duplicating validation logic.
- Update examples and English documentation when behavior changes.
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or
  `chore:`) when the user asks for a commit.
- When collaborating as Codex, add
  `Co-authored-by: Codex <noreply@openai.com>` to requested commits.
- Do not bump the version, publish to PyPI, or create a release unless explicitly
  requested.

## Release safety

- Never reuse a version, tag, or PyPI filename. PyPI artifacts are immutable.
- A release tag must match `project.version`, point at the tested commit, and be
  created only after CI succeeds.
- CI stores the validated wheel and sdist. The publish workflow must promote
  those exact artifacts rather than rebuilding them independently.
- Keep Codecov in its separate workflow after successful CI.
- If the worktree contains unrelated or untracked user files, preserve them and
  exclude them from commits unless the user explicitly places them in scope.

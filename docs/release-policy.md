# Versioning and releases

The project follows Semantic Versioning.

- The `1.x` public API is stable.
- Domain types under `rut_validator.core`, framework-agnostic behavior under
  `rut_validator.validation`, and adapters under `rut_validator.orm` form the
  documented architecture.
- Names listed in the API reference are public. Names prefixed with `_` are
  internal implementation details.

## Compatibility

- Python 3.10 through 3.14 is validated in CI.
- The base installation depends only on Click and does not import optional
  frameworks.
- Pydantic 2.x, SQLAlchemy 2.x, Django 4.2–5.x, SQLModel 0.x, and FastAPI 0.x
  are tested through isolated extras.

## Deprecation policy

A public symbol is not removed in a minor release. It first emits
`DeprecationWarning`, is documented in the changelog, and remains available for
at least one minor release. Removal requires a new major version.

## Release gate

A release is tagged only when:

1. tests, lint, formatting, and type checks pass;
2. MkDocs builds in strict mode;
3. wheel and source distribution build successfully;
4. Twine validates both artifacts;
5. the installed base wheel imports without optional frameworks;
6. dependency auditing reports no known vulnerabilities;
7. package version, documentation, and changelog agree.

RUT validation does not certify identity, ownership, or registration with the
Chilean Internal Revenue Service (SII).

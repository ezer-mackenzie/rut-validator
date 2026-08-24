# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Canonical dotted formatting now preserves leading zeros in the RUT body, so
  formatting and reparsing cannot change the normalized identity.
- The CLI batch payload now has an explicit common mapping type, avoiding
  partially unknown inference in strict type checkers.
- `rut_sqlmodel_field()` now declares its concrete `FieldInfo` return contract
  instead of propagating SQLModel's permissive `Any` annotation.
- Validation error payloads now declare `dict[str, str]` instead of leaking an
  unnecessary `Any` value type.

## [2.0.0] - 2026-08-24

### Removed

- The deprecated `RutValidator`, `RutFormatter`, `RutParser`, and `RutPatterns`
  compatibility classes.
- The deprecated `Rut` constructor argument `format_detected`, aliases
  `number`, `digit`, `is_dotted`, `is_numeric`, and method `equals()`.
- The deprecated `rut_validator.validation` and `rut_validator.orm` packages.
- The deprecated no-op CLI option `format --quiet`.

### Changed

- The private engine no longer retains combined regex constants, length
  constants, or expected-format branches left over from the 1.x compatibility
  layer; normalization now removes only separators from an already detected
  valid format.
- Framework-independent functions now live in `rut_validator.api` and remain
  exported from the package root.
- Optional adapters consume the public functional API and live exclusively in
  `rut_validator.integrations`.
- Pydantic JSON Schema no longer publishes a syntax-only regex that could not
  express modulo-11 validation; runtime validation remains strict.

## [1.1.0] - 2026-08-24

### Added

- `is_valid_rut()` and `get_validation_result()` provide functional replacements
  for the non-raising `RutValidator` operations and are exported from the root
  package.
- `rut_validator.integrations` is the canonical package for Pydantic, Django,
  SQLAlchemy, and SQLModel adapters.
- A version 2 migration guide documents every deprecated API and its
  replacement.

### Deprecated

- `RutValidator`, `RutFormatter`, `RutParser`, and the methods of `RutPatterns`
  now emit `DeprecationWarning` and will be removed in 2.0.0.
- `Rut(..., format_detected=...)`, `Rut.equals()`, `Rut.number`, `Rut.digit`,
  `Rut.is_dotted`, and `Rut.is_numeric` will be removed in 2.0.0.
- The no-op CLI option `format --quiet` will be removed in 2.0.0.
- Imports from `rut_validator.orm` now resolve lazily to the canonical
  `rut_validator.integrations` classes while warning about their removal in
  2.0.0.

### Fixed

- Pydantic JSON Schema now derives its accepted RUT pattern from the same
  canonical definition used by runtime validation.

### Changed

- RUT parsing and validation now produce one private, immutable analysis result
  in `core.engine`, removing repeated format detection and normalization.
- `Rut`, `RutParser`, and `RutValidator` now share the same engine path while
  preserving the complete public `1.x` contract.
- Production validation no longer depends on the legacy `RutParser` and
  `RutPatterns` facades; they remain available for compatibility.
- CLI, optional adapters, formatter compatibility methods, documentation, and
  examples now use the canonical functional validation helpers internally.
- Characterization tests now freeze the `1.x` exports, constructor signature,
  legacy aliases, error codes, and invalid-input classification ahead of the
  version 2 migration.
- Documentation, examples, framework tests, and new Django migration paths now
  use `rut_validator.integrations`; existing migrations using
  `rut_validator.orm` remain importable through compatibility shims.

## [1.0.1] - 2026-08-22

### Fixed

- Batch CLI validation no longer silently accepts leading or trailing
  whitespace.
- `Rut` rejects an explicitly supplied input format when it contradicts the
  actual value.
- `Rut.__repr__` redacts the submitted value to reduce accidental disclosure in
  logs and debugging output.

### Changed

- Dependency metadata and the Poetry lock file are synchronized.
- The development extra now installs FastAPI because the default test matrix
  collects the FastAPI integration suite.
- CI now verifies Poetry metadata consistency explicitly.
- Codecov upload now runs in a dedicated workflow after CI succeeds, using a
  coverage artifact and GitHub OIDC authentication.
- Dependency auditing now targets the declared project instead of unrelated
  packages installed as CI tooling.
- Unused isort and Flake8 development dependencies were removed; Ruff and
  Black remain the maintained linting and formatting tools.
- Unused standalone RUT fixture files were removed.
- The legacy `format --quiet` compatibility option is documented as a no-op
  because format output is already quiet.
- Validation constructs `Rut` through a single check-digit validation pass.
- `Rut` now caches the normalized representation established during validation.
- Shared invariant primitives now live in a private core engine and use the
  canonical `RutFormat` enum, removing duplicated format literals and the
  dependency from `core.Rut` to the public validation layer.
- Documentation now distinguishes validating APIs from low-level parsing and
  pattern helpers.
- Public docstrings now follow a concise PEP 257 style, document validation
  errors where relevant, and avoid repeating type annotations.

## [1.0.0] - 2026-07-23

### Added
- Stable public API and documented deprecation policy
- CI coverage for Python 3.10 through 3.14
- Architectural tests preventing optional frameworks from leaking into
  standalone imports

### Changed
- Internal imports now consistently respect package-layer boundaries
- Django typing uses its canonical `deconstructible` import and a
  runtime-safe generic `CharField` base
- `Rut` construction no longer exposes an unchecked protected factory
- Package status is now Production/Stable

### Removed
- Redundant `ValidatedRut` alias; use `Rut` directly
- Obsolete `Makefile`; Poetry, pre-commit, and CI provide the maintained
  development workflows
- Legacy migration documentation and references to pre-1.0 APIs

### Documentation
- Rewritten the complete MkDocs site in English as the canonical documentation
- Rewritten the README in English with current 1.0 examples and commands

## [0.9.0] - 2026-07-23

### Added
- Isolated CI jobs for every optional integration extra
- Installed-wheel smoke tests and safe example execution
- Dependency auditing with `pip-audit`
- A 95% project coverage release gate
- Migration guide for the stabilized public API

### Changed
- CI actions and pre-commit configuration now use the current project toolchain
- Package metadata no longer uses the deprecated license classifier

## [0.8.0] - 2026-07-23

### Added
- Real Django model, ModelForm, migration deconstruction, nullable, unique, and
  SQLite round-trip tests
- FastAPI TestClient coverage for valid requests, HTTP 422, and OpenAPI
- SQLAlchemy rollback, nullable, and corrupted database value tests
- SQLModel optional field and JSON serialization tests

### Changed
- Django forms accept formatted 12-character input while databases keep
  normalized 9-character storage
- SQLAlchemy validates values read from the database to preserve its type
  invariant

## [0.7.0] - 2026-07-23

### Added
- Stable machine-readable codes and structured payloads for validation errors
- Check-digit metadata on modulo-11 validation failures
- Property-based modulo-11 tests powered by Hypothesis
- CLI coverage for structured JSON errors, info, and batch processing

### Changed
- Format recognition now accepts ASCII digits only and uses complete matches
- Boolean validation helpers safely reject malformed types, Unicode digits,
  whitespace, alternate hyphens, and oversized input
- CLI JSON errors remain valid JSON and omit the submitted RUT

### Removed
- The tracked temporary v1 audit; `tmp/` and `temp/` are now local-only

## [0.6.0] - 2026-07-23

### Changed
- The modulo-11 factors are now a typed `Final` constant colocated with the
  framework-agnostic validator
- Framework implementations now use explicit class names:
  `RutPydantic`, `RutDjango`, `RutSQLAlchemy`, and `RutSQLModel`
- SQLModel field configuration is exposed as `rut_sqlmodel_field`

### Removed
- `constants.py`, whose only value now belongs to the agnostic implementation
- Framework class aliases such as `RutType`, `RutStr`, `RUTField`, and
  `RutField`

## [0.5.0] - 2026-07-23

### Changed
- `rut_validator.core` now contains only domain types
- Framework-agnostic parsing, formatting, and validation moved to
  `rut_validator.validation`
- Framework adapters now live exclusively in `rut_validator.orm`
- Documentation and examples now use the canonical architecture

### Removed
- Legacy `rut_validator.core.orm` compatibility modules
- Redundant root adapter re-export modules
- Legacy `rut_validator.types` and unused `rut_validator.utils` packages
- Lazy `RutStr` export from the package root

## [0.4.0] - 2026-07-23

### Added
- New MkDocs Material documentation site
- Guides for core, CLI, Pydantic, FastAPI, Django, SQLAlchemy, and SQLModel
- API reference, development workflow, and release policy

### Changed
- Replaced the complete legacy Sphinx documentation tree
- CI and Read the Docs now build MkDocs in strict mode
- Development commands now use the current optional dependency layout

## [0.3.0] - 2026-07-23

### Added
- Functional standalone helpers `validate_rut` and `calculate_check_digit`
- Stable convenience imports for Pydantic, Django, SQLAlchemy, and SQLModel
- Strict hyphenated output support in `RutFormatter`
- An `all` installation extra for every supported integration

### Changed
- Public formatting validates input before converting it
- Runtime version is now read from installed package metadata
- Expanded API contract and database round-trip coverage

## [0.2.0] - 2026-07-22

### Added
- Public optional integrations under `rut_validator.orm`
- Functional CLI for validation, formatting, information, and batch processing
- SQLModel field helper and compatibility aliases for the `Rut` value object

### Changed
- Framework integrations are optional; the standalone validator no longer imports Pydantic
- `Rut` is immutable and consistently validates its input
- Python support now reflects the tested modern syntax baseline (3.10+)

### Fixed
- Graceful handling of non-string values in the validator
- Pydantic models now retain the `RutStr` subtype
- Legacy integration import paths remain available as compatibility shims

## [0.1.0] - 2026-05-10

### Added
- Core Chilean RUT validation with modulo 11 algorithm
- Support for formatted, hyphenated, and normalized RUT inputs
- `RutParser` for parsing and normalizing RUT strings
- `RutPatterns` for regex-based validation, format detection, and formatting helpers
- `RutValidator` with `get_validation_result`, `is_valid`, and `validate`
- `Rut` value object with `normalized`, `formatted`, `hyphenated`, `body`, `check_digit`, equality, and hash support
- Pydantic integration via `RutStr`, including JSON schema generation
- Django integration via `RUTField`
- SQLAlchemy integration via `RutSQLAlchemy`
- Example usage scripts and framework documentation
- Custom exception hierarchy for invalid values, invalid formats, and modulo 11 failures
- Comprehensive documentation and CLI usage guide
- Modular architecture for easy extension
- Type hints throughout the codebase
- CI/CD pipeline with GitHub Actions
- Code quality checks using black, isort, flake8, and mypy
- Pre-commit hooks configuration
- Security policy and contribution guidelines
- MIT license

### Features
- Pure Python implementation with no external runtime dependencies for core validation
- Format-aware normalization and formatting helpers
- ORM and framework-ready validation adapters
- Stable public package exports and typed exception APIs
- Validation result enumeration for fine-grained status handling

### Documentation
- Usage documentation for Pydantic, Django, SQLAlchemy, and FastAPI
- Example scripts for pure validation, Pydantic, FastAPI, and CLI guidance
- API documentation in docstrings
- Installation and developer setup guides
- Contribution guidelines and project policies

### Development
- Poetry for dependency and packaging management
- Tests covering core validation and ORM adapters
- GitHub Actions CI workflow
- Pre-commit hooks for formatting and linting
- Type hints across the package
- Type checking with mypy
- Makefile for common development tasks

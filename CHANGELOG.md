# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

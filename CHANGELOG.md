# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
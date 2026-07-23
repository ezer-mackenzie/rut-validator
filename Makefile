.PHONY: help install test lint format type-check clean build docs serve-docs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	poetry install

install-dev: ## Install development dependencies
	poetry install --all-extras

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=rut_validator --cov-report=html --cov-report=term

lint: ## Run all linting tools
	poetry run black --check --diff src/ tests/
	poetry run isort --check-only --diff src/ tests/
	poetry run flake8 src/ tests/

format: ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

type-check: ## Run mypy type checking
	poetry run mypy src/rut_validator/

quality: lint type-check ## Run all quality checks

fix: format ## Auto-fix code formatting

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	poetry build

publish: ## Publish to PyPI (requires PYPI_API_TOKEN)
	poetry publish

docs: ## Build documentation
	poetry run mkdocs build --strict

serve-docs: ## Serve documentation locally
	poetry run mkdocs serve

pre-commit: ## Run pre-commit on all files
	poetry run pre-commit run --all-files

setup-dev: install-dev pre-commit ## Set up development environment

check: quality test ## Run all checks (lint, type-check, tests)

release: check build publish ## Full release process

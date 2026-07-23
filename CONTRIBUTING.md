# Contributing to rut-validator

Thank you for your interest in contributing to rut-validator! We welcome contributions from the community.

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors

## How to Contribute

### 1. Reporting Bugs

- Use the [GitHub Issues](https://github.com/ezer-mackenzie/rut-validator/issues) to report bugs
- Include detailed steps to reproduce the issue
- Provide sample code if possible
- Include your Python version and operating system

### 2. Suggesting Features

- Open a [GitHub Issue](https://github.com/ezer-mackenzie/rut-validator/issues) with the "enhancement" label
- Clearly describe the feature and its use case
- Explain why this feature would be useful to other users

### 3. Contributing Code

#### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/ezer-mackenzie/rut-validator.git
cd rut-validator

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest
```

#### Making Changes

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

2. **Write tests** for your changes first (TDD approach)

3. **Implement your changes** following the existing code style

4. **Run the test suite**:
   ```bash
   poetry run pytest --cov=rut_validator
   ```

5. **Run linting tools**:
   ```bash
   poetry run black src/ tests/
   poetry run isort src/ tests/
   poetry run flake8 src/ tests/
   poetry run mypy src/rut_validator/
   ```

6. **Update documentation** if needed

7. **Commit your changes**:
   ```bash
   git commit -m "feat: add your feature description"
   # Follow conventional commits: https://www.conventionalcommits.org/
   ```

8. **Push and create a Pull Request**

#### Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test additions/modifications
- `chore:` for maintenance tasks

### 4. Documentation

- Update docstrings for any new public APIs
- Update the README if adding new features
- Update examples if introducing breaking changes

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints for all public APIs
- Write descriptive variable and function names
- Keep functions small and focused on a single responsibility

### Testing

- Write tests for all new functionality
- Maintain high test coverage (>90%)
- Test edge cases and error conditions
- Use descriptive test names

### Architecture

- Keep the core validation logic framework-agnostic
- Framework integrations should be in separate modules
- Maintain backward compatibility when possible

## Pull Request Process

1. **Ensure CI passes** - All tests, linting, and type checking must pass
2. **Update CHANGELOG.md** - Add an entry for your changes
3. **Update version** - If it's a breaking change, update version in pyproject.toml
4. **Squash commits** - Keep the git history clean
5. **Wait for review** - A maintainer will review your PR

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- GitHub's contributor insights
- Release notes

Thank you for contributing to rut-validator! 🎉

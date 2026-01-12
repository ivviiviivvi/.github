# Contributing to ivviiviivvi

Thank you for your interest in contributing! We welcome contributions from the community and are pleased to have you join us.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Community and Support](#community-and-support)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@ivviiviivvi.com.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up your development environment** (see below)
4. **Create a branch** for your changes
5. **Make your changes** following our guidelines
6. **Test your changes** thoroughly
7. **Submit a pull request**

## Development Setup

### Prerequisites

- **Python 3.11+** (Python 3.12 recommended)
- **pip** (Python package manager)
- **Git** for version control
- **Node.js 20+** (for JavaScript projects)

### Installation Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/.github.git
cd .github

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Verify installation
pre-commit run --all-files
```

### For Node.js Projects

```bash
# Install Node.js dependencies
npm install

# Run tests
npm test
```

## Code Style Guidelines

We follow consistent code style across the project to maintain readability and quality.

### Python Code (PEP 8)

- **Style Guide**: [PEP 8](https://peps.python.org/pep-0008/)
- **Line Length**: 88 characters (Black formatter default)
- **Imports**: Organized with `isort`
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Google-style or NumPy-style

```python
def calculate_sum(numbers: list[int]) -> int:
    """Calculate the sum of a list of numbers.
    
    Args:
        numbers: A list of integers to sum.
        
    Returns:
        The sum of all numbers in the list.
    """
    return sum(numbers)
```

### YAML Files

- **Indentation**: 2 spaces (not tabs)
- **Quotes**: Use double quotes for strings
- **Comments**: Use `#` for inline comments

```yaml
name: CI
on:
  push:
    branches:
      - main  # Main branch only
```

### Markdown Files

- **Line Length**: 80-100 characters for readability
- **Headers**: Use ATX-style headers (`#`, `##`, etc.)
- **Lists**: Use `-` for unordered lists, `1.` for ordered
- **Code Blocks**: Use triple backticks with language identifier

### JavaScript/TypeScript

- **Style Guide**: Airbnb or Prettier defaults
- **Indentation**: 2 spaces
- **Semicolons**: Required
- **Quotes**: Single quotes for strings

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear and structured commit messages.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes only
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no feature change or bug fix)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config, etc.)
- **ci**: CI/CD configuration changes
- **build**: Build system or external dependencies

### Examples

```bash
# Feature
feat(auth): add OAuth2 authentication support

Implement OAuth2 authentication flow with Google and GitHub providers.
Includes token refresh and session management.

Closes #123

# Bug fix
fix(api): resolve null pointer exception in user endpoint

Added null check before accessing user.profile to prevent crashes
when profile data is missing.

Fixes #456

# Documentation
docs(readme): update installation instructions

Add Docker setup instructions and troubleshooting section.

# Chore
chore(deps): update dependencies to latest versions

Update pytest from 7.4.0 to 7.4.3 and black from 23.9.1 to 23.11.0
```

### Rules

- ✅ Use present tense ("add feature" not "added feature")
- ✅ Use imperative mood ("move cursor to..." not "moves cursor to...")
- ✅ Keep subject line under 50 characters
- ✅ Capitalize subject line
- ✅ No period at the end of subject line
- ✅ Separate subject from body with blank line
- ✅ Wrap body at 72 characters
- ✅ Use body to explain *what* and *why*, not *how*

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest changes from main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run all tests** and ensure they pass:
   ```bash
   pytest
   npm test  # If applicable
   ```

3. **Run pre-commit hooks**:
   ```bash
   pre-commit run --all-files
   ```

4. **Update documentation** if you changed APIs or behavior

5. **Add tests** for new features or bug fixes

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] Pre-commit hooks pass
- [ ] Commit messages follow Conventional Commits
- [ ] No merge conflicts with main branch
- [ ] Related issues referenced (e.g., `Closes #123`)

### Review Process

1. **Automated Checks**: CI/CD workflows run automatically
2. **Code Review**: Maintainers review your changes (2 approvals required)
3. **CODEOWNERS Review**: Relevant team owners must approve
4. **Feedback**: Address any requested changes
5. **Merge**: Once approved, maintainers will merge your PR

### Response Times

- **Initial Response**: Within 24-48 hours
- **Full Review**: Within 3-5 business days
- **Follow-up**: Within 24 hours after changes

## Issue Reporting Guidelines

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check documentation** and FAQs
3. **Verify it's a bug** and not expected behavior

### Bug Reports

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:

- Clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots or error messages
- Possible solution (if you have one)

### Feature Requests

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.yml) and include:

- Problem statement (what problem does this solve?)
- Proposed solution
- Alternatives considered
- Additional context or mockups

### Security Vulnerabilities

**Do NOT create public issues for security vulnerabilities.**

Follow our [Security Policy](SECURITY.md) to report privately.

## Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_module.py

# Run tests matching pattern
pytest -k "test_authentication"
```

### Coverage Thresholds

- **Minimum Coverage**: 80% overall
- **New Code**: 90% coverage required
- **Critical Paths**: 95%+ coverage required

### Writing Tests

```python
import pytest

def test_example_function():
    """Test example function with valid input."""
    result = example_function(input_data)
    assert result == expected_output

def test_example_function_invalid_input():
    """Test example function raises error with invalid input."""
    with pytest.raises(ValueError):
        example_function(invalid_data)
```

### Test Organization

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test fixtures and data
```

## Pre-commit Hooks

We use pre-commit hooks to automatically check code quality before commits.

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Configuration

Our `.pre-commit-config.yaml` includes:

- **black**: Python code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **prettier**: YAML/JSON/Markdown formatting
- **detect-secrets**: Secret scanning
- **trailing-whitespace**: Remove trailing whitespace
- **end-of-file-fixer**: Ensure files end with newline

### Running Manually

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks (use sparingly)
git commit --no-verify
```

### Updating Hooks

```bash
pre-commit autoupdate
```

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `fix/*`: Bug fixes
- `docs/*`: Documentation updates
- `chore/*`: Maintenance tasks

### Creating a Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Keeping Your Branch Updated

```bash
git fetch origin
git rebase origin/main
```

### Resolving Conflicts

```bash
# During rebase
git rebase origin/main
# Fix conflicts in files
git add <resolved-files>
git rebase --continue
```

## Community and Support

- **Questions**: Use [GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions)
- **Documentation**: See [SUPPORT.md](SUPPORT.md)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

### Getting Help

- 💬 [GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions) - Ask questions
- 📖 [Documentation](docs/) - Read the docs
- 🐛 [Issue Tracker](https://github.com/ivviiviivvi/.github/issues) - Report bugs
- 📧 [Email](mailto:support@ivviiviivvi.com) - Contact us

## Recognition

Contributors are recognized in:

- Release notes
- `CONTRIBUTORS.md` file
- Project README
- Annual contributor spotlight

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to ivviiviivvi!** 🎉

For more information, contact us at contribute@ivviiviivvi.com

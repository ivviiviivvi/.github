# Contributing to this Project

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Code Review Expectations](#code-review-expectations)
- [Testing Requirements](#testing-requirements)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior through the appropriate channels.

## Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** following our guidelines
5. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Node.js 20 or higher (for some tooling)

### Installation

```bash
# Clone the repository
git clone https://github.com/ivviiviivvi/.github.git
cd .github

# Install Python dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_specific.py

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Running Linters

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
```

## How to Contribute

### Reporting Bugs

Use our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, browser, version)

### Suggesting Features

Use our [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) and include:
- Problem statement
- Proposed solution
- Alternatives considered

### Improving Documentation

Documentation improvements are always welcome! Use our [Documentation template](.github/ISSUE_TEMPLATE/documentation.yml) for doc issues.

## Code Style Guidelines

### Python

- Follow **PEP 8** style guide
- Use **Python 3.11+** features
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names

```python
# Good
def calculate_total_price(items: list[Item]) -> Decimal:
    """Calculate the total price of items including tax."""
    return sum(item.price for item in items) * Decimal('1.08')

# Bad
def calc(x):
    return sum(i.p for i in x) * 1.08
```

### JavaScript/TypeScript

- Use ES6+ features
- Prefer `const` over `let`, avoid `var`
- Use meaningful variable and function names
- Follow existing code patterns

### YAML

- Use 2-space indentation
- Quote strings when necessary
- Maintain consistent formatting

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style changes (formatting, no logic change)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Adding or updating tests
- `chore:` Maintenance tasks
- `ci:` CI/CD changes

### Examples

```
feat(workflows): add automated dependency updates

Implement Dependabot configuration for npm, pip, and GitHub Actions.
This will help keep dependencies up to date automatically.

Closes #123
```

```
fix(security): patch XSS vulnerability in user input

Sanitize user input before rendering to prevent XSS attacks.

BREAKING CHANGE: API now requires authentication token
```

## Pull Request Process

1. **Update Documentation**: Update README, docs, or comments as needed
2. **Add Tests**: Include tests for new functionality
3. **Run Linters**: Ensure all linting checks pass
4. **Run Tests**: Ensure all tests pass
5. **Update Changelog**: Add entry to CHANGELOG.md (if applicable)
6. **Fill PR Template**: Complete all sections of the PR template
7. **Request Review**: Request review from appropriate team members

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass locally
- [ ] No new warnings
- [ ] Linting passes
- [ ] No hardcoded secrets

## Issue Reporting Guidelines

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if the issue is already fixed in the latest version
3. Gather relevant information (logs, screenshots, etc.)

### Creating a Quality Issue

- Use appropriate issue template
- Provide clear, concise description
- Include reproduction steps
- Add relevant labels
- Link related issues

## Code Review Expectations

### For Authors

- Respond to feedback promptly
- Be open to suggestions
- Keep PRs focused and reasonably sized
- Update PR based on feedback
- Resolve all conversations before merge

### For Reviewers

- Be constructive and respectful
- Explain the reasoning behind suggestions
- Approve when satisfied with changes
- Request changes if issues need addressing
- Use GitHub's review features effectively

## Testing Requirements

### Unit Tests

- Write tests for new functionality
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use descriptive test names

### Integration Tests

- Test interactions between components
- Verify end-to-end workflows
- Test with realistic data

### Test Guidelines

```python
# Good test
def test_calculate_total_price_with_multiple_items():
    """Test total price calculation with multiple items."""
    items = [Item(price=10.00), Item(price=20.00)]
    total = calculate_total_price(items)
    assert total == Decimal('32.40')  # 30.00 * 1.08 tax

# Bad test
def test1():
    assert calc([Item(10), Item(20)]) == 32.4
```

## Getting Help

- 💬 [Discussions](https://github.com/ivviiviivvi/.github/discussions) - Ask questions
- 📚 [Documentation](README.md) - Read the docs
- 🐛 [Issues](https://github.com/ivviiviivvi/.github/issues) - Report bugs

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in commit messages

Thank you for contributing! 🎉

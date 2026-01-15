# Testing Best Practices Guide

> **Comprehensive testing standards for GitHub .github repository - Phase 8**

## Table of Contents

- [Overview](#overview)
- [Testing Philosophy](#testing-philosophy)
- [Test Structure](#test-structure)
- [Coverage Requirements](#coverage-requirements)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Overview

This guide establishes testing standards for all Python code in the
organization. Following these practices ensures:

- ✅ **80%+ code coverage** on all scripts
- ✅ **Security-focused testing** for critical components
- ✅ **Fast, reliable test suite** (\<2 minutes)
- ✅ **CI/CD integration** with automated checks
- ✅ **Consistent patterns** across the codebase

---

## Testing Philosophy

### Core Principles

1. **Test Behavior, Not Implementation**: Test what code does, not how it does
   it
1. **Fast First**: Unit tests should run in milliseconds
1. **Security-Critical**: Always test security boundaries
1. **Comprehensive Coverage**: Target 80%+ coverage, 100% for critical paths
1. **Maintainable**: Tests should be easy to read and update

### Test Pyramid

```
    /\
   /  \  E2E (5%)      - Full system integration
  /____\
 /      \ Integration (15%) - Component interaction
/________\
   Unit (80%)          - Individual functions/classes
```

**Focus**: 80% unit tests, 15% integration tests, 5% end-to-end tests

---

## Test Structure

### Directory Organization

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_web_crawler.py
│   ├── test_ecosystem_visualizer.py
│   ├── test_sync_labels.py
│   ├── test_mouthpiece_filter.py
│   └── test_quota_manager.py
├── integration/             # Integration tests (slower)
│   ├── test_agent_tracking.py
│   └── test_workflow_orchestration.py
└── fixtures/                # Test data and mock responses
    ├── sample_workflows.yml
    └── mock_api_responses.json
```

### File Naming Conventions

- **Test files**: `test_<module_name>.py`
- **Test classes**: `Test<Feature>` (e.g., `TestSSRFProtection`)
- **Test functions**: `test_<behavior>` (e.g., `test_blocks_private_ips`)

---

## Coverage Requirements

### Minimum Targets

| Category              | Coverage | Priority    |
| --------------------- | -------- | ----------- |
| **Security-critical** | 100%     | 🔴 CRITICAL |
| **Core scripts**      | 80-90%   | 🟡 HIGH     |
| **Utilities**         | 70-80%   | 🟢 MEDIUM   |
| **Overall**           | 80%+     | 🟡 HIGH     |

### Security-Critical Components

Must have 100% coverage:

- `web_crawler.py` - SSRF protection, link validation
- Input validation functions
- Authentication/authorization logic
- Secret handling code

### Coverage Exclusions

Exclude from coverage (in `pytest.ini`):

```python
# pragma: no cover
- Abstract methods
- `if __name__ == '__main__'` blocks
- Debug logging
- Type checking imports (TYPE_CHECKING)
```

---

## Writing Tests

### Basic Test Structure

```python
#!/usr/bin/env python3
"""
Unit tests for module_name.py
Focus: Primary functionality, edge cases, error handling
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))
from module_name import function_to_test


class TestFeatureName:
    """Test specific feature or component"""

    @pytest.fixture
    def setup_data(self):
        """Reusable test data"""
        return {"key": "value"}

    def test_basic_functionality(self, setup_data):
        """Test the happy path"""
        result = function_to_test(setup_data)
        assert result is not None
        assert result == expected_value

    def test_handles_edge_case(self):
        """Test edge cases and boundaries"""
        result = function_to_test(edge_case_input)
        assert result == expected_edge_behavior

    def test_raises_on_invalid_input(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Test Categories with Markers

```python
@pytest.mark.unit
def test_fast_unit_test():
    """Fast, isolated test"""
    pass

@pytest.mark.integration
def test_component_interaction():
    """Test interaction between components"""
    pass

@pytest.mark.security
def test_ssrf_protection():
    """Security-focused test"""
    pass

@pytest.mark.slow
def test_long_running_operation():
    """Test that takes >1s"""
    pass

@pytest.mark.performance
def test_benchmark_processing_speed():
    """Performance benchmark"""
    pass
```

### Parameterized Tests

```python
@pytest.mark.parametrize("input_value,expected", [
    ("valid", True),
    ("invalid", False),
    ("", False),
    (None, False),
])
def test_validation(input_value, expected):
    """Test multiple inputs efficiently"""
    result = validate(input_value)
    assert result == expected
```

### Mocking External Dependencies

```python
@patch('module_name.requests.get')
def test_api_call(mock_get):
    """Mock external API calls"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_data()
    assert result == {"data": "test"}
    mock_get.assert_called_once()
```

---

## Running Tests

### Command Line

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_web_crawler.py

# Run specific test
pytest tests/unit/test_web_crawler.py::TestSSRFProtection::test_blocks_private_ips

# Run with coverage
pytest tests/ --cov=automation/scripts --cov-report=html

# Run only unit tests
pytest tests/ -m unit

# Run security tests
pytest tests/ -m security

# Run with verbose output
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest tests/ --cov=automation/scripts --cov-report=html
# View: open htmlcov/index.html

# Generate terminal report with missing lines
pytest tests/ --cov=automation/scripts --cov-report=term-missing

# Fail if coverage below 80%
pytest tests/ --cov=automation/scripts --cov-fail-under=80
```

---

## CI/CD Integration

### GitHub Actions Workflow

Located at `.github/workflows/test-coverage.yml`:

**Triggers:**

- Push to `main` or `develop`
- Pull requests
- Manual dispatch

**Matrix Strategy:**

- Python 3.10, 3.11, 3.12
- Parallel execution for speed

**Steps:**

1. Check out code
1. Set up Python with caching
1. Install dependencies
1. Run tests with coverage
1. Upload coverage to Codecov
1. Comment coverage on PRs

### Pre-commit Hooks

Tests run automatically on `pre-push`:

```bash
# Install pre-commit hooks
pre-commit install --hook-type pre-push

# Manually run tests
pre-commit run pytest-check --all-files
```

### Coverage Enforcement

- **CI fails** if coverage drops below 70%
- **PR reviews** show coverage delta
- **Annotations** highlight uncovered lines

---

## Best Practices

### Do's ✅

- **Write descriptive test names**: `test_blocks_private_ips` > `test_1`
- **Use fixtures for setup**: Reuse test data and mocks
- **Test one behavior per test**: Single assertion principle
- **Mock external dependencies**: Network, file system, APIs
- **Test error paths**: Exceptions, edge cases, invalid input
- **Use parameterization**: Test multiple inputs efficiently
- **Add docstrings**: Explain what the test validates
- **Keep tests fast**: Unit tests \<10ms, integration \<1s

### Don'ts ❌

- **Don't test implementation details**: Test behavior, not internals
- **Don't write flaky tests**: Tests must be deterministic
- **Don't skip cleanup**: Use fixtures for teardown
- **Don't duplicate setup**: Use fixtures and conftest.py
- **Don't ignore warnings**: Fix or suppress explicitly
- **Don't commit failing tests**: All tests must pass before merge
- **Don't test external services**: Mock them
- **Don't write slow unit tests**: Mock I/O operations

---

## Common Patterns

### Testing SSRF Protection

```python
@pytest.mark.security
@pytest.mark.parametrize("private_ip", [
    "127.0.0.1",
    "10.0.0.1",
    "192.168.1.1",
    "169.254.169.254",  # AWS metadata
])
def test_blocks_private_ips(crawler, private_ip):
    """Verify SSRF protection blocks private IPs"""
    with pytest.raises(SecurityError):
        crawler.fetch(f"http://{private_ip}/")
```

### Testing File Operations

```python
def test_reads_markdown_file(tmp_path):
    """Test markdown file reading"""
    # Setup
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test\nContent here")

    # Execute
    content = read_markdown(test_file)

    # Verify
    assert "Test" in content
```

### Testing API Calls

```python
@patch('module.requests.Session.get')
def test_fetches_github_data(mock_get):
    """Test GitHub API integration"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"repo": "test"}
    mock_get.return_value = mock_response

    result = fetch_github_data("org", "repo")

    assert result["repo"] == "test"
    mock_get.assert_called_with("https://api.github.com/repos/org/repo")
```

### Testing Error Handling

```python
def test_handles_connection_error():
    """Test handling of network errors"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(NetworkError):
            fetch_data("https://example.com")
```

---

## Troubleshooting

### Common Issues

**Problem**: Tests fail locally but pass in CI (or vice versa)

**Solutions**:

- Check Python version differences
- Verify environment variables
- Check file path assumptions
- Review timezone/locale dependencies

---

**Problem**: Slow test suite

**Solutions**:

- Profile tests: `pytest --durations=10`
- Mark slow tests: `@pytest.mark.slow`
- Use mocks instead of real I/O
- Parallelize: `pytest -n auto` (requires pytest-xdist)

---

**Problem**: Flaky tests

**Solutions**:

- Avoid time-based assertions
- Mock external dependencies completely
- Use deterministic test data
- Fix race conditions in async code

---

**Problem**: Low coverage despite tests

**Solutions**:

- Check coverage exclusions
- Test error paths and edge cases
- Add parametrized tests
- Review uncovered lines: `--cov-report=term-missing`

---

**Problem**: ImportError in tests

**Solutions**:

- Verify sys.path manipulation
- Check relative imports
- Install missing test dependencies
- Use `PYTHONPATH` environment variable

---

## Additional Resources

### Tools

- **pytest**: Test framework - <https://pytest.org>
- **pytest-cov**: Coverage plugin - <https://pytest-cov.readthedocs.io>
- **pytest-mock**: Mocking helpers - <https://pytest-mock.readthedocs.io>
- **Codecov**: Coverage reporting - <https://codecov.io>

### Documentation

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest parametrize](https://docs.pytest.org/en/stable/parametrize.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

### Organization Resources

- [pytest.ini](../../pytest.ini) - Test configuration
- [conftest.py](../../tests/conftest.py) - Shared fixtures
- [Test Coverage Workflow](../../.github/workflows/test-coverage.yml) - CI
  configuration
- [CLEANUP_ROADMAP.md](../../CLEANUP_ROADMAP.md) - Phase 8 details

---

## Success Metrics

### Phase 8 Completion Criteria

- [x] ✅ `pytest.ini` configured with 80% coverage target
- [x] ✅ Test directory structure created (`unit/`, `integration/`, `fixtures/`)
- [x] ✅ Unit tests for critical scripts (web_crawler, ecosystem_visualizer,
      sync_labels)
- [x] ✅ Shared fixtures in `conftest.py`
- [x] ✅ CI workflow for automated testing
- [x] ✅ Pre-commit hooks for test execution
- [x] ✅ Documentation for testing standards
- [ ] ⏳ Achieve 80%+ coverage on all scripts
- [ ] ⏳ All security tests passing
- [ ] ⏳ Integration tests passing

### Quality Gates

**Before merging code:**

1. All tests pass locally
1. Coverage ≥ 80% for new code
1. No security test failures
1. CI pipeline green
1. Code review approved

---

_Last Updated: 2026-01-14_ _Phase 8: Testing & Quality Assurance_

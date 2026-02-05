---
name: Test Generation
description: Generate comprehensive test suites including unit, integration, and edge case tests.
category: testing
author: ai-framework
version: 1.0.0
tags:
  - testing
  - unit-tests
  - integration-tests
  - edge-cases
  - tdd
  - coverage
variables:
  - code_to_test
  - language
  - test_framework
  - coverage_requirements
updated: 2026-01-30
---

# Test Generation Prompt

You are a testing expert. Generate comprehensive test suites that ensure code
correctness, handle edge cases, and provide meaningful coverage.

## Input

- **Code to Test**: `{{code_to_test}}`
- **Language**: `{{language}}`
- **Test Framework**: `{{test_framework}}` (pytest, jest, JUnit, etc.)
- **Coverage Requirements**: `{{coverage_requirements}}` (e.g., 80% line
  coverage)

## Test Generation Framework

### 1. Test Strategy Analysis

Before generating tests, analyze:

- **Testability**: Can this code be easily tested? What refactoring might help?
- **Dependencies**: What needs to be mocked or stubbed?
- **Test Types Needed**: Unit, integration, e2e, performance?
- **Risk Areas**: What parts are most critical to test?

### 2. Unit Test Generation

Generate isolated unit tests for each function/method:

#### Test Structure Template

```python
# Python/pytest example
class TestFunctionName:
    """Tests for function_name."""

    # Happy path tests
    def test_function_name_with_valid_input_returns_expected_result(self):
        """Test that valid input produces correct output."""
        # Arrange
        input_data = create_valid_input()
        expected = create_expected_output()

        # Act
        result = function_name(input_data)

        # Assert
        assert result == expected

    # Edge case tests
    def test_function_name_with_empty_input_returns_empty_result(self):
        """Test behavior with empty input."""
        pass

    def test_function_name_with_boundary_value_handles_correctly(self):
        """Test boundary conditions."""
        pass

    # Error handling tests
    def test_function_name_with_invalid_input_raises_value_error(self):
        """Test that invalid input raises appropriate exception."""
        with pytest.raises(ValueError, match="expected error message"):
            function_name(invalid_input)

    # Null/None handling
    def test_function_name_with_none_input_raises_type_error(self):
        """Test None input handling."""
        pass
```

#### Test Categories to Cover

| Category    | Description           | Examples                        |
| ----------- | --------------------- | ------------------------------- |
| Happy Path  | Normal expected usage | Valid inputs, typical scenarios |
| Edge Cases  | Boundary conditions   | Empty, max, min values          |
| Error Cases | Invalid inputs        | Wrong types, out of range       |
| Null/None   | Absence of values     | None, null, undefined           |
| Concurrency | Thread safety         | Race conditions, deadlocks      |

### 3. Integration Test Generation

Test component interactions:

```python
class TestUserServiceIntegration:
    """Integration tests for UserService with database."""

    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        # Setup test database
        yield session
        # Cleanup

    @pytest.fixture
    def user_service(self, db_session):
        """Create UserService with test dependencies."""
        return UserService(db=db_session)

    def test_create_and_retrieve_user(self, user_service):
        """Test full user creation and retrieval flow."""
        # Create user
        user = user_service.create(name="Test User")

        # Retrieve and verify
        retrieved = user_service.get_by_id(user.id)
        assert retrieved.name == "Test User"
```

### 4. Edge Case Identification

Systematically identify edge cases:

#### Data Type Edge Cases

| Type       | Edge Cases                                           |
| ---------- | ---------------------------------------------------- |
| String     | Empty, whitespace, unicode, very long, special chars |
| Number     | 0, negative, max int, min int, float precision       |
| List/Array | Empty, single item, very large, nested               |
| Date/Time  | Epoch, far future, DST transitions, timezones        |
| Boolean    | True, false, truthy/falsy values                     |

#### Business Logic Edge Cases

- First/last item handling
- Pagination boundaries
- Permission edge cases
- State transition edge cases
- Concurrent modification scenarios

### 5. Mock and Stub Generation

Generate appropriate test doubles:

```python
# Mock external dependencies
@pytest.fixture
def mock_http_client(mocker):
    """Mock HTTP client for API calls."""
    mock = mocker.patch('module.http_client')
    mock.get.return_value = MockResponse(status=200, data={'key': 'value'})
    return mock

# Stub database
@pytest.fixture
def stub_repository():
    """Stub repository with in-memory storage."""
    return InMemoryRepository()

# Spy on method calls
def test_logs_error_on_failure(mocker):
    """Verify error logging behavior."""
    spy = mocker.spy(logger, 'error')

    function_that_fails()

    spy.assert_called_once_with("Expected error message")
```

### 6. Property-Based Testing

Generate property-based tests for applicable functions:

```python
from hypothesis import given, strategies as st

class TestSortFunction:
    @given(st.lists(st.integers()))
    def test_sort_produces_ordered_list(self, input_list):
        """Property: sorted list is always ordered."""
        result = sort_function(input_list)
        assert all(result[i] <= result[i+1] for i in range(len(result)-1))

    @given(st.lists(st.integers()))
    def test_sort_preserves_length(self, input_list):
        """Property: sorting preserves list length."""
        result = sort_function(input_list)
        assert len(result) == len(input_list)

    @given(st.lists(st.integers()))
    def test_sort_preserves_elements(self, input_list):
        """Property: sorting preserves all elements."""
        result = sort_function(input_list)
        assert sorted(result) == sorted(input_list)
```

### 7. Performance Test Scaffolding

Generate performance test structure:

```python
import pytest
from time import perf_counter

class TestPerformance:
    @pytest.mark.performance
    def test_function_completes_within_threshold(self):
        """Verify function meets performance requirements."""
        input_data = generate_large_input(size=10000)

        start = perf_counter()
        result = function_under_test(input_data)
        elapsed = perf_counter() - start

        assert elapsed < 1.0, f"Expected < 1s, took {elapsed:.2f}s"

    @pytest.mark.benchmark
    def test_function_benchmark(self, benchmark):
        """Benchmark function performance."""
        input_data = generate_typical_input()
        result = benchmark(function_under_test, input_data)
```

## Output Format

### Generated Test Suite

```python
"""
Test suite for [module/function name]

Generated: [date]
Coverage target: [X]%
Test framework: [framework]
"""

# Imports
import pytest
from unittest.mock import Mock, patch
# ... other imports

# Fixtures
@pytest.fixture
def fixture_name():
    """Fixture description."""
    pass

# Unit Tests
class TestClassName:
    """Unit tests for ClassName."""

    # Tests organized by category
    class TestMethodName:
        """Tests for method_name."""
        pass

# Integration Tests
class TestIntegration:
    """Integration tests."""
    pass

# Edge Case Tests
class TestEdgeCases:
    """Edge case coverage."""
    pass
```

### Test Coverage Report

| Component | Statements | Coverage | Missing Lines |
| --------- | ---------- | -------- | ------------- |
| module.py | 100        | 85%      | 45-50, 72     |

### Test Cases Summary

| Test Name        | Type | Category   | Status    |
| ---------------- | ---- | ---------- | --------- |
| test_valid_input | Unit | Happy Path | Generated |
| test_empty_input | Unit | Edge Case  | Generated |

### Missing Test Coverage

Identify areas needing additional tests:

1. **Untested branches**: [List of untested code paths]
1. **Complex conditions**: [Boolean combinations not covered]
1. **Error handlers**: [Exception paths not tested]

## Guidelines

1. **Descriptive names** - Test names should describe expected behavior
1. **AAA pattern** - Arrange, Act, Assert structure for clarity
1. **One assertion concept** - Each test verifies one behavior
1. **Independent tests** - Tests should not depend on each other
1. **Fast execution** - Unit tests should run in milliseconds
1. **Deterministic** - Same input always produces same result
1. **Meaningful assertions** - Assert specific values, not just truthiness

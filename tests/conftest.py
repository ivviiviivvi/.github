#!/usr/bin/env python3
"""
Shared pytest fixtures and configuration for test suite
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_github_token():
    """Mock GitHub API token"""
    return "ghp_test_token_1234567890abcdefghijklmnopqrstuvwxyz"


@pytest.fixture
def mock_org_name():
    """Mock organization name"""
    return "test-organization"


@pytest.fixture
def mock_github_api_response():
    """Mock successful GitHub API response"""
    response = MagicMock()
    response.status_code = 200
    response.ok = True
    response.json.return_value = {"data": "test"}
    return response


@pytest.fixture
def mock_github_api_error():
    """Mock failed GitHub API response"""
    response = MagicMock()
    response.status_code = 404
    response.ok = False
    response.json.return_value = {"message": "Not Found"}
    return response


@pytest.fixture
def sample_workflow_data():
    """Sample workflow data for testing"""
    return {
        "name": "CI Test",
        "path": ".github/workflows/ci-test.yml",
        "triggers": ["push", "pull_request"],
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [{"uses": "actions/checkout@v4"}, {"run": "pytest"}],
            }
        },
    }


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content with links for testing"""
    return """
# Test Document

This is a test document with several links:

- [GitHub](https://github.com)
- [Example](https://example.com/path)
- Bare URL: https://test.com

## Code Block

```python
# This should not be extracted as a link
url = "https://not-a-real-link.com"
```

## More Links

Check out https://api.github.com/repos for more info.
"""


@pytest.fixture
def sample_label_data():
    """Sample label data for testing sync_labels.py"""
    return [
        {"name": "bug", "color": "d73a4a", "description": "Something isn't working"},
        {
            "name": "enhancement",
            "color": "a2eeef",
            "description": "New feature or request",
        },
        {
            "name": "documentation",
            "color": "0075ca",
            "description": "Improvements or additions to documentation",
        },
    ]


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create temporary project directory structure"""
    project = tmp_path / "test-project"
    project.mkdir()

    # Create .github structure
    github_dir = project / ".github"
    github_dir.mkdir()

    workflows_dir = github_dir / "workflows"
    workflows_dir.mkdir()

    # Create sample files
    (project / "README.md").write_text("# Test Project\n")
    (workflows_dir / "ci.yml").write_text("name: CI\non: push\n")

    return project


@pytest.fixture
def sample_agent_metadata():
    """Sample agent metadata for testing"""
    return {
        "name": "test-agent",
        "version": "1.0.0",
        "description": "Test agent for unit tests",
        "capabilities": ["test", "validate"],
        "created_at": "2024-01-14T00:00:00Z",
    }


@pytest.fixture
def mock_requests_session(monkeypatch):
    """Mock requests.Session for testing HTTP calls"""
    session = MagicMock()
    session.get.return_value.status_code = 200
    session.get.return_value.ok = True
    session.post.return_value.status_code = 201
    session.post.return_value.ok = True

    def mock_session_init(*args, **kwargs):
        return session

    monkeypatch.setattr("requests.Session", mock_session_init)
    return session


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables before each test"""
    # Clear GitHub-related environment variables
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.delenv("GITHUB_API_URL", raising=False)


@pytest.fixture
def capture_output(capsys):
    """Fixture to capture stdout/stderr"""
    return capsys


# Markers configuration
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, external dependencies)"
    )
    config.addinivalue_line("markers", "security: Security-focused tests")
    config.addinivalue_line("markers", "performance: Performance benchmarks")
    config.addinivalue_line("markers", "slow: Tests that take >1s to run")


# Performance tracking
import time as _time


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Track test performance"""
    item.start_time = _time.time()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    """Mark slow tests"""
    if hasattr(item, "start_time"):
        duration = _time.time() - item.start_time
        if duration > 1.0 and "slow" not in [m.name for m in item.iter_markers()]:
            print(
                f"\n⚠️  Test {item.nodeid} took {duration:.2f}s (consider marking as slow)"
            )

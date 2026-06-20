"""Root conftest.py - Mocks secret_manager BEFORE test collection.

This prevents any 1Password CLI calls during testing. The mock is installed
via pytest_configure which runs before any test modules are imported.
"""

import sys
import types
from unittest.mock import MagicMock


def pytest_configure(config):
    """Install secret_manager mock before any test collection.

    This hook runs before pytest collects test modules, preventing any
    imports of secret_manager from triggering real 1Password CLI calls.
    """
    # Create a comprehensive mock for secret_manager
    mock_secret_manager = MagicMock()

    # Mock all the functions that might be called
    mock_secret_manager.get_secret = MagicMock(return_value="mock-secret-value")
    mock_secret_manager.ensure_secret = MagicMock(return_value="mock-secret-value")
    mock_secret_manager.get_github_token = MagicMock(return_value="mock-github-token")
    mock_secret_manager.ensure_github_token = MagicMock(return_value="mock-github-token")

    # Install the mock in sys.modules BEFORE any imports happen
    sys.modules["secret_manager"] = mock_secret_manager

    try:
        __import__("github")
    except ImportError:
        mock_github_module = types.ModuleType("github")

        class MockGithubException(Exception):
            """Small PyGithub exception stand-in for import-time tests."""

            def __init__(self, status=None, data=None, headers=None):
                self.status = status
                self.data = data
                self.headers = headers
                message = data.get("message") if isinstance(data, dict) else data
                super().__init__(message or status)

        class MockAuth:
            """Small PyGithub Auth stand-in."""

            @staticmethod
            def Token(token):
                return token

        class MockGithub:
            """Small PyGithub client stand-in."""

            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        mock_github_module.Auth = MockAuth
        mock_github_module.Github = MockGithub
        mock_github_module.GithubException = MockGithubException
        mock_github_module.Label = MagicMock()
        mock_github_module.Repository = MagicMock()

        label_module = types.ModuleType("github.Label")
        label_module.Label = MagicMock()
        repository_module = types.ModuleType("github.Repository")
        repository_module.Repository = MagicMock()

        sys.modules["github"] = mock_github_module
        sys.modules["github.Label"] = label_module
        sys.modules["github.Repository"] = repository_module


def pytest_unconfigure(config):
    """Clean up the secret_manager mock after all tests complete."""
    sys.modules.pop("secret_manager", None)

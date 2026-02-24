"""Root conftest.py - Mocks secret_manager BEFORE test collection.

This prevents any 1Password CLI calls during testing. The mock is installed
via pytest_configure which runs before any test modules are imported.
"""

import sys
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


def pytest_unconfigure(config):
    """Clean up the secret_manager mock after all tests complete."""
    sys.modules.pop("secret_manager", None)

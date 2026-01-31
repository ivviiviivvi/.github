#!/usr/bin/env python3
"""Unit tests for automation/scripts/secret_manager.py
Focus: 1Password CLI integration, secret retrieval, error handling.
"""

import importlib
import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


def _load_real_secret_manager():
    """Force load the real secret_manager module, removing any mocks."""
    # Remove any mock from sys.modules
    sys.modules.pop("secret_manager", None)

    # Load the module from the actual file path
    scripts_path = Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"
    spec = importlib.util.spec_from_file_location("secret_manager", scripts_path / "secret_manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["secret_manager"] = module
    spec.loader.exec_module(module)
    return module


# Load the real module at import time
secret_manager = _load_real_secret_manager()


@pytest.fixture(autouse=True)
def ensure_real_secret_manager():
    """Ensure the real secret_manager module is loaded for each test."""
    global secret_manager
    # Reload fresh for each test to avoid cross-test pollution
    secret_manager = _load_real_secret_manager()
    yield
    # Clean up after test - other tests may want to mock it
    sys.modules.pop("secret_manager", None)


# Helper functions that call through the module (ensures patches work correctly)
def get_secret(item_name, field="password", vault="Private"):
    """Call get_secret through the module for proper patch support."""
    return secret_manager.get_secret(item_name, field, vault)


def ensure_secret(item_name, field="password", vault="Private"):
    """Call ensure_secret through the module for proper patch support."""
    return secret_manager.ensure_secret(item_name, field, vault)


def get_github_token(item_name):
    """Call get_github_token through the module for proper patch support."""
    return secret_manager.get_github_token(item_name)


def ensure_github_token(item_name):
    """Call ensure_github_token through the module for proper patch support."""
    return secret_manager.ensure_github_token(item_name)


def _print_secret_error(item_name, field, vault):
    """Call _print_secret_error through the module for proper patch support."""
    return secret_manager._print_secret_error(item_name, field, vault)


class TestGetSecret:
    """Test get_secret function."""

    def test_successful_retrieval(self):
        """Test successful secret retrieval from 1Password."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="my-secret-value\n",
                returncode=0,
            )

            result = get_secret("my-item", "password")

            assert result == "my-secret-value"
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert "op" in call_args[0][0]
            assert "my-item" in call_args[0][0]

    def test_returns_none_on_empty_result(self):
        """Test returns None when secret is empty."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="",
                returncode=0,
            )

            result = get_secret("my-item", "password")

            assert result is None

    def test_returns_none_on_whitespace_result(self):
        """Test returns None when secret is only whitespace."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="   \n",
                returncode=0,
            )

            result = get_secret("my-item", "password")

            assert result is None

    def test_handles_cli_error(self):
        """Test handles CalledProcessError gracefully."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd=["op"],
                stderr="Item not found",
            )

            result = get_secret("nonexistent", "password")

            assert result is None

    def test_handles_cli_not_installed(self):
        """Test handles 1Password CLI not being installed."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("op not found")

            result = get_secret("my-item", "password")

            assert result is None

    def test_uses_custom_vault(self):
        """Test uses custom vault when specified."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="secret\n", returncode=0)

            get_secret("my-item", "password", vault="Work")

            call_args = mock_run.call_args[0][0]
            assert "--vault" in call_args
            assert "Work" in call_args

    def test_default_vault_is_private(self):
        """Test default vault is Private (no --vault flag)."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="secret\n", returncode=0)

            get_secret("my-item", "password")

            call_args = mock_run.call_args[0][0]
            assert "--vault" not in call_args

    def test_retrieves_custom_field(self):
        """Test retrieves custom field."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="api-key\n", returncode=0)

            result = get_secret("api-service", "credential")

            assert result == "api-key"
            call_args = mock_run.call_args[0][0]
            assert "credential" in call_args


class TestEnsureSecret:
    """Test ensure_secret function."""

    def test_returns_secret_when_found(self):
        """Test returns secret when retrieval succeeds."""
        with patch("secret_manager.get_secret") as mock_get:
            mock_get.return_value = "my-secret"

            result = ensure_secret("my-item", "password")

            assert result == "my-secret"

    def test_exits_when_secret_not_found(self):
        """Test exits with code 1 when secret not found."""
        with patch("secret_manager.get_secret") as mock_get:
            mock_get.return_value = None
            with patch("secret_manager._print_secret_error"):
                with pytest.raises(SystemExit) as exc_info:
                    ensure_secret("nonexistent", "password")

                assert exc_info.value.code == 1

    def test_prints_error_when_secret_not_found(self):
        """Test prints detailed error message when secret not found."""
        with patch("secret_manager.get_secret") as mock_get:
            mock_get.return_value = None
            with patch("secret_manager._print_secret_error") as mock_print:
                with pytest.raises(SystemExit):
                    ensure_secret("my-item", "credential", "MyVault")

                mock_print.assert_called_once_with("my-item", "credential", "MyVault")


class TestGetGitHubToken:
    """Test get_github_token function."""

    def test_raises_without_item_name(self):
        """Test raises ValueError when item_name is empty."""
        with pytest.raises(ValueError) as exc_info:
            get_github_token("")

        assert "Token name required" in str(exc_info.value)

    def test_raises_with_none_item_name(self):
        """Test raises ValueError when item_name is None."""
        with pytest.raises(ValueError):
            get_github_token(None)

    def test_returns_env_var_when_set(self):
        """Test returns environment variable when set."""
        with patch.dict("os.environ", {"ORG_LABEL_SYNC_TOKEN": "env-token"}):
            result = get_github_token("org-label-sync-token")

            assert result == "env-token"

    def test_converts_item_name_to_env_var(self):
        """Test converts item name to uppercase with underscores."""
        with patch.dict("os.environ", {"MY_CUSTOM_TOKEN": "token-value"}):
            result = get_github_token("my-custom-token")

            assert result == "token-value"

    def test_falls_back_to_1password_when_no_env(self):
        """Test falls back to 1Password when env var not set."""
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("secret_manager.get_secret") as mock_get,
        ):
            mock_get.return_value = "1p-token"

            result = get_github_token("org-label-sync-token")

            assert result == "1p-token"
            mock_get.assert_called_once_with("org-label-sync-token", "password")

    def test_returns_none_when_both_sources_fail(self):
        """Test returns None when both env and 1Password fail."""
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("secret_manager.get_secret") as mock_get,
        ):
            mock_get.return_value = None

            result = get_github_token("org-label-sync-token")

            assert result is None


class TestEnsureGitHubToken:
    """Test ensure_github_token function."""

    def test_delegates_to_ensure_secret(self):
        """Test delegates to ensure_secret with password field."""
        with patch("secret_manager.ensure_secret") as mock_ensure:
            mock_ensure.return_value = "my-token"

            result = ensure_github_token("org-label-sync-token")

            assert result == "my-token"
            mock_ensure.assert_called_once_with("org-label-sync-token", "password")


class TestPrintSecretError:
    """Test _print_secret_error function."""

    def test_prints_item_details(self, capsys):
        """Test prints item details in error message."""
        _print_secret_error("my-item", "credential", "MyVault")

        captured = capsys.readouterr()
        assert "my-item" in captured.err
        assert "credential" in captured.err
        assert "MyVault" in captured.err

    def test_prints_setup_instructions(self, capsys):
        """Test prints 1Password setup instructions."""
        _print_secret_error("my-item", "password", "Private")

        captured = capsys.readouterr()
        assert "1Password CLI" in captured.err
        assert "op item create" in captured.err
        assert "Service Account" in captured.err

    def test_explains_why_no_env_vars(self, capsys):
        """Test explains security rationale for no env vars."""
        _print_secret_error("my-item", "password", "Private")

        captured = capsys.readouterr()
        assert "WHY NO ENVIRONMENT VARIABLES" in captured.err
        assert "process listings" in captured.err


class TestSubprocessCommand:
    """Test subprocess command construction."""

    def test_includes_reveal_flag(self):
        """Test includes --reveal flag for security."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="secret\n", returncode=0)

            get_secret("my-item", "password")

            call_args = mock_run.call_args[0][0]
            assert "--reveal" in call_args

    def test_captures_output(self):
        """Test captures stdout and stderr."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="secret\n", returncode=0)

            get_secret("my-item", "password")

            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["capture_output"] is True
            assert call_kwargs["text"] is True

    def test_uses_check_for_errors(self):
        """Test uses check=True to raise on non-zero exit."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="secret\n", returncode=0)

            get_secret("my-item", "password")

            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["check"] is True


class TestSecurityConsiderations:
    """Test security-related behavior."""

    def test_strips_trailing_newlines(self):
        """Test strips trailing newlines from secrets."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="my-secret\n\n",
                returncode=0,
            )

            result = get_secret("my-item", "password")

            assert result == "my-secret"
            assert not result.endswith("\n")

    def test_handles_stderr_in_errors(self):
        """Test captures and reports stderr from failed commands."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd=["op"],
                stderr="Detailed error message",
            )

            # Should not raise, just return None
            result = get_secret("my-item", "password")
            assert result is None

    def test_empty_secret_returns_none_not_empty_string(self):
        """Test empty secret returns None, not empty string."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)

            result = get_secret("my-item", "password")

            assert result is None
            assert result != ""


class TestIntegration:
    """Integration-style tests for common usage patterns."""

    def test_typical_github_token_flow_with_env(self):
        """Test typical flow: env var set for dev container."""
        with patch.dict("os.environ", {"ORG_PROJECT_ADMIN_TOKEN": "ghp_xxxx"}):
            token = get_github_token("org-project-admin-token")
            assert token == "ghp_xxxx"

    def test_typical_github_token_flow_with_1password(self):
        """Test typical flow: 1Password in production."""
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("secret_manager.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(
                stdout="ghp_production_token\n",
                returncode=0,
            )

            token = get_github_token("org-project-admin-token")
            assert token == "ghp_production_token"

    def test_api_key_retrieval(self):
        """Test retrieving API key with custom field."""
        with patch("secret_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="api-key-12345\n",
                returncode=0,
            )

            api_key = get_secret("datadog-api-key", "credential", "Work")

            assert api_key == "api-key-12345"  # pragma: allowlist secret
            call_args = mock_run.call_args[0][0]
            assert "credential" in call_args
            assert "--vault" in call_args
            assert "Work" in call_args

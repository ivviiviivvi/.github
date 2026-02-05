#!/usr/bin/env python3
"""Unit tests for automation/scripts/validate_tokens.py

Focus: Token validation against GitHub API and 1Password integration.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from validate_tokens import (TOKENS, get_token_from_1password, main,
                             validate_token)


@pytest.mark.unit
class TestTokensRegistry:
    """Test token registry configuration."""

    def test_tokens_dict_exists(self):
        """Test TOKENS dictionary is defined."""
        assert isinstance(TOKENS, dict)

    def test_each_token_has_required_fields(self):
        """Test each token config has required fields."""
        required_fields = {"scopes", "test_endpoint", "purpose"}

        for token_name, config in TOKENS.items():
            for field in required_fields:
                assert field in config, f"{token_name} missing {field}"

    def test_tokens_have_valid_endpoints(self):
        """Test token endpoints start with /."""
        for token_name, config in TOKENS.items():
            endpoint = config["test_endpoint"]
            assert endpoint.startswith("/"), f"{token_name} endpoint should start with /"

    def test_scopes_are_lists(self):
        """Test scopes are defined as lists."""
        for token_name, config in TOKENS.items():
            assert isinstance(config["scopes"], list)


@pytest.mark.unit
class TestGetTokenFrom1Password:
    """Test 1Password token retrieval."""

    def test_returns_token_on_success(self):
        """Test returns stripped token on successful retrieval."""
        mock_result = MagicMock()
        mock_result.stdout = "  ghp_test_token_123  \n"  # allow-secret: test fixture

        with patch("subprocess.run", return_value=mock_result):
            token = get_token_from_1password("test-token")  # allow-secret: test fixture

        assert token == "ghp_test_token_123"  # allow-secret: test fixture

    def test_returns_none_on_subprocess_error(self):
        """Test returns None when 1Password CLI fails."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "op")
            token = get_token_from_1password("test-token")  # allow-secret: test fixture

        assert token is None

    def test_exits_on_missing_cli(self, capsys):
        """Test exits when 1Password CLI is not installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            with pytest.raises(SystemExit) as exc_info:
                get_token_from_1password("test-token")

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "1Password CLI not found" in captured.out

    def test_calls_op_with_correct_arguments(self):
        """Test calls op CLI with correct path format."""
        mock_result = MagicMock()
        mock_result.stdout = "token"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            get_token_from_1password("my-token")

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "op" in call_args
        assert "read" in call_args
        assert "op://Personal/my-token/password" in call_args


@pytest.mark.unit
class TestValidateToken:
    """Test token validation logic."""

    @pytest.fixture
    def token_config(self):
        """Return sample token configuration."""
        return {
            "scopes": ["repo", "workflow"],
            "test_endpoint": "/user",
            "purpose": "Test purpose",
        }

    def test_returns_valid_result_on_success(self, token_config):
        """Test returns valid result on successful API call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo, workflow, user",
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch("validate_tokens.get_token_from_1password", return_value="test_token"):
            with patch("requests.get", return_value=mock_response):
                result = validate_token("test-token", token_config)

        assert result["valid"] is True
        assert result["token"] == "test-token"
        assert "rate_limit" in result

    def test_returns_invalid_when_token_not_found(self, token_config):
        """Test returns invalid when token not in 1Password."""
        with patch("validate_tokens.get_token_from_1password", return_value=None):
            result = validate_token("missing-token", token_config)

        assert result["valid"] is False
        assert "not found" in result["error"]

    def test_returns_invalid_on_401(self, token_config):
        """Test returns invalid on unauthorized response."""
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch("validate_tokens.get_token_from_1password", return_value="bad_token"):
            with patch("requests.get", return_value=mock_response):
                result = validate_token("bad-token", token_config)

        assert result["valid"] is False
        assert "Invalid or expired" in result["error"]

    def test_returns_invalid_on_403(self, token_config):
        """Test returns invalid on forbidden response."""
        mock_response = MagicMock()
        mock_response.status_code = 403

        with patch("validate_tokens.get_token_from_1password", return_value="limited_token"):
            with patch("requests.get", return_value=mock_response):
                result = validate_token("limited-token", token_config)

        assert result["valid"] is False
        assert "Insufficient permissions" in result["error"]

    def test_includes_warning_for_missing_scopes(self, token_config):
        """Test adds warning when expected scopes are missing."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo",  # Missing 'workflow'
            "X-RateLimit-Remaining": "5000",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch("validate_tokens.get_token_from_1password", return_value="test_token"):
            with patch("requests.get", return_value=mock_response):
                result = validate_token("test-token", token_config)

        assert result["valid"] is True
        assert "warning" in result
        assert "workflow" in result["warning"]

    def test_handles_network_error(self, token_config):
        """Test handles network errors gracefully."""
        with patch("validate_tokens.get_token_from_1password", return_value="test_token"):
            with patch("requests.get") as mock_get:
                mock_get.side_effect = requests.RequestException("Connection failed")
                result = validate_token("test-token", token_config)

        assert result["valid"] is False
        assert "Network error" in result["error"]

    def test_handles_unexpected_error(self, token_config):
        """Test handles unexpected errors gracefully."""
        with patch("validate_tokens.get_token_from_1password", return_value="test_token"):
            with patch("requests.get") as mock_get:
                mock_get.side_effect = Exception("Unexpected error")
                result = validate_token("test-token", token_config)

        assert result["valid"] is False
        assert "Unexpected error" in result["error"]

    def test_parses_rate_limit_correctly(self, token_config):
        """Test rate limit information is parsed correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo, workflow",
            "X-RateLimit-Remaining": "4500",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": "1704067200",  # 2024-01-01 00:00:00 UTC
        }

        with patch("validate_tokens.get_token_from_1password", return_value="test_token"):
            with patch("requests.get", return_value=mock_response):
                result = validate_token("test-token", token_config)

        assert result["rate_limit"]["remaining"] == 4500
        assert result["rate_limit"]["limit"] == 5000

    def test_result_includes_purpose(self, token_config):
        """Test result includes token purpose."""
        with patch("validate_tokens.get_token_from_1password", return_value=None):
            result = validate_token("test-token", token_config)

        assert result["purpose"] == "Test purpose"


@pytest.mark.unit
class TestMainFunction:
    """Test main entry point."""

    def test_exits_zero_when_all_valid(self, capsys):
        """Test exits with 0 when all tokens are valid."""
        mock_result = {
            "valid": True,
            "rate_limit": {"remaining": 5000, "limit": 5000},
            "token": "test-token",
            "purpose": "Test purpose",
        }

        with patch("validate_tokens.validate_token", return_value=mock_result):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "All tokens are healthy" in captured.out

    def test_exits_one_when_any_invalid(self, capsys):
        """Test exits with 1 when any token is invalid."""
        mock_result = {
            "valid": False,
            "error": "Token not found",
            "token": "test",
            "purpose": "Test",
        }

        with patch("validate_tokens.validate_token", return_value=mock_result):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Some tokens failed" in captured.out

    def test_prints_token_status(self, capsys):
        """Test prints status for each token."""
        mock_result = {
            "valid": True,
            "rate_limit": {"remaining": 4000, "limit": 5000},
            "token": "test-token",
            "purpose": "Test purpose",
        }

        with patch("validate_tokens.validate_token", return_value=mock_result):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        # Should print checking message and result
        assert "Checking" in captured.out

    def test_shows_warning_for_missing_scopes(self, capsys):
        """Test displays warning when scopes are missing."""
        mock_result = {
            "valid": True,
            "rate_limit": {"remaining": 5000, "limit": 5000},
            "warning": "Missing scopes: admin",
            "token": "test-token",
            "purpose": "Test purpose",
        }

        with patch("validate_tokens.validate_token", return_value=mock_result):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Missing scopes" in captured.out

    def test_prints_summary(self, capsys):
        """Test prints validation summary."""
        mock_result = {
            "valid": True,
            "rate_limit": {"remaining": 5000, "limit": 5000},
            "token": "test-token",
            "purpose": "Test purpose",
        }

        with patch("validate_tokens.validate_token", return_value=mock_result):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Summary" in captured.out
        assert "Valid tokens" in captured.out

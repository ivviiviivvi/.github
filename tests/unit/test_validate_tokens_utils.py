#!/usr/bin/env python3
"""Unit tests for automation/scripts/utils/validate-tokens.py

Focus: Token validation and health checks for organization tokens.
Note: This tests the utils/validate-tokens.py, separate from scripts/validate_tokens.py.
"""

import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module with hyphenated filename
spec = importlib.util.spec_from_file_location(
    "validate_tokens_utils",
    Path(__file__).parent.parent.parent / "src" / "automation" / "scripts" / "utils" / "validate-tokens.py",
)
validate_tokens_utils = importlib.util.module_from_spec(spec)
sys.modules["validate_tokens_utils"] = validate_tokens_utils
spec.loader.exec_module(validate_tokens_utils)


@pytest.mark.unit
class TestValidateToken:
    """Test validate_token function."""

    def test_skips_planned_token_without_env_var(self):
        """Test skips planned tokens if no env var."""
        config = {"status": "planned", "test_endpoint": "/user"}

        with patch.dict("os.environ", {}, clear=True):
            with patch.object(validate_tokens_utils, "get_secret", return_value=None):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert result["status"] == "planned"
        assert "not yet created" in result["error"]

    def test_validates_token_from_env_var(self):
        """Test validates token from environment variable."""
        config = {"status": "active", "test_endpoint": "/user", "scopes": ["repo"]}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo, workflow",
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch.dict("os.environ", {"TEST_TOKEN": "ghp_test123"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert result["valid"]
        assert "repo" in result["scopes"]
        assert result["rate_limit"]["remaining"] == 4999

    def test_validates_token_from_1password(self):
        """Test validates token from 1Password."""
        config = {"status": "active", "test_endpoint": "/user", "scopes": []}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "",
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch.dict("os.environ", {}, clear=True):
            with patch.object(validate_tokens_utils, "get_secret", return_value="secret_token"):
                with patch("requests.get", return_value=mock_response):
                    result = validate_tokens_utils.validate_token("test-token", config)

        assert result["valid"]

    def test_handles_token_not_found(self):
        """Test handles token not found."""
        config = {"status": "active", "test_endpoint": "/user"}

        with patch.dict("os.environ", {}, clear=True):
            with patch.object(validate_tokens_utils, "get_secret", return_value=None):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "not found" in result["error"]

    def test_handles_invalid_token(self):
        """Test handles 401 response."""
        config = {"status": "active", "test_endpoint": "/user"}

        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch.dict("os.environ", {"TEST_TOKEN": "invalid"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "Invalid or expired" in result["error"]

    def test_handles_rate_limit_exceeded(self):
        """Test handles 403 response."""
        config = {"status": "active", "test_endpoint": "/user"}

        mock_response = MagicMock()
        mock_response.status_code = 403

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "Rate limit" in result["error"] or "insufficient" in result["error"]

    def test_handles_other_http_error(self):
        """Test handles other HTTP errors."""
        config = {"status": "active", "test_endpoint": "/user"}

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "HTTP 500" in result["error"]

    def test_handles_timeout(self):
        """Test handles request timeout."""
        import requests

        config = {"status": "active", "test_endpoint": "/user"}

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", side_effect=requests.exceptions.Timeout):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "timeout" in result["error"].lower()

    def test_handles_connection_error(self):
        """Test handles connection error."""
        import requests

        config = {"status": "active", "test_endpoint": "/user"}

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "Connection" in result["error"]

    def test_handles_unexpected_error(self):
        """Test handles unexpected errors."""
        config = {"status": "active", "test_endpoint": "/user"}

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", side_effect=Exception("Unexpected")):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert not result["valid"]
        assert "Unexpected" in result["error"]

    def test_warns_on_missing_scopes(self):
        """Test warns when expected scopes are missing."""
        config = {
            "status": "active",
            "test_endpoint": "/user",
            "scopes": ["repo", "admin:org"],
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo",  # Missing admin:org
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert result["valid"]
        assert result["warning"] is not None
        assert "admin:org" in result["warning"]

    def test_skips_scope_validation_for_unknown(self):
        """Test skips scope validation when expected is 'unknown'."""
        config = {
            "status": "active",
            "test_endpoint": "/user",
            "scopes": ["unknown"],
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-OAuth-Scopes": "repo",
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int(datetime.now().timestamp())),
        }

        with patch.dict("os.environ", {"TEST_TOKEN": "valid"}, clear=True):
            with patch("requests.get", return_value=mock_response):
                result = validate_tokens_utils.validate_token("test-token", config)

        assert result["valid"]
        assert result["warning"] is None


@pytest.mark.unit
class TestPrintSummary:
    """Test print_summary function."""

    def test_prints_valid_count(self, capsys):
        """Test prints valid token count."""
        results = [
            {"token": "token1", "valid": True, "status": "active"},
            {"token": "token2", "valid": True, "status": "active"},
            {"token": "token3", "valid": False, "status": "active"},
        ]

        validate_tokens_utils.print_summary(results)

        captured = capsys.readouterr()
        assert "Valid:   2/3" in captured.out

    def test_prints_failed_count(self, capsys):
        """Test prints failed token count."""
        results = [
            {"token": "token1", "valid": False, "status": "active"},
            {"token": "token2", "valid": False, "status": "active"},
        ]

        validate_tokens_utils.print_summary(results)

        captured = capsys.readouterr()
        assert "Failed:  2/2" in captured.out

    def test_prints_planned_count(self, capsys):
        """Test prints planned token count."""
        results = [
            {"token": "token1", "valid": False, "status": "planned"},
            {"token": "token2", "valid": True, "status": "active"},
        ]

        validate_tokens_utils.print_summary(results)

        captured = capsys.readouterr()
        assert "Planned: 1/2" in captured.out

    def test_prints_warning_count(self, capsys):
        """Test prints warning count."""
        results = [
            {"token": "token1", "valid": True, "status": "active", "warning": "Test"},
        ]

        validate_tokens_utils.print_summary(results)

        captured = capsys.readouterr()
        assert "Warnings: 1" in captured.out

    def test_verbose_shows_details(self, capsys):
        """Test verbose mode shows details."""
        results = [
            {
                "token": "token1",
                "valid": True,
                "status": "active",
                "scopes": ["repo"],
                "rate_limit": {"remaining": 100, "limit": 5000},
            },
        ]

        validate_tokens_utils.print_summary(results, verbose=True)

        captured = capsys.readouterr()
        assert "Token scopes" in captured.out
        assert "Rate limit" in captured.out

    def test_returns_true_when_all_valid(self):
        """Test returns True when all non-planned tokens are valid."""
        results = [
            {"token": "token1", "valid": True, "status": "active"},
            {"token": "token2", "valid": False, "status": "planned"},
        ]

        result = validate_tokens_utils.print_summary(results)

        assert result is True

    def test_returns_false_when_failures_exist(self):
        """Test returns False when active tokens fail."""
        results = [
            {"token": "token1", "valid": False, "status": "active"},
        ]

        result = validate_tokens_utils.print_summary(results)

        assert result is False


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_validates_all_tokens(self, monkeypatch):
        """Test main validates all tokens by default."""
        monkeypatch.setattr(sys, "argv", ["validate-tokens.py", "--ignore-planned"])

        with patch.object(validate_tokens_utils, "validate_token") as mock_validate:
            mock_validate.return_value = {
                "token": "test",
                "valid": True,
                "status": "active",
                "scopes": [],
                "rate_limit": {"remaining": 100, "limit": 5000},
                "error": None,
                "warning": None,
            }
            with pytest.raises(SystemExit) as exc:
                validate_tokens_utils.main()

            assert exc.value.code == 0

    def test_main_validates_single_token(self, monkeypatch):
        """Test main validates single token when specified."""
        monkeypatch.setattr(sys, "argv", ["validate-tokens.py", "--token", "org-label-sync-token", "--ignore-planned"])

        with patch.object(validate_tokens_utils, "validate_token") as mock_validate:
            mock_validate.return_value = {
                "token": "org-label-sync-token",
                "valid": True,
                "status": "active",
                "scopes": [],
                "rate_limit": {"remaining": 100, "limit": 5000},
                "error": None,
                "warning": None,
            }
            with pytest.raises(SystemExit) as exc:
                validate_tokens_utils.main()

            mock_validate.assert_called_once()
            assert exc.value.code == 0

    def test_main_exits_1_on_failure(self, monkeypatch):
        """Test main exits with code 1 on validation failure."""
        monkeypatch.setattr(sys, "argv", ["validate-tokens.py"])

        with patch.object(validate_tokens_utils, "validate_token") as mock_validate:
            mock_validate.return_value = {
                "token": "test",
                "valid": False,
                "status": "active",
                "scopes": [],
                "rate_limit": None,
                "error": "Failed",
                "warning": None,
            }
            with pytest.raises(SystemExit) as exc:
                validate_tokens_utils.main()

            assert exc.value.code == 1

    def test_main_verbose_flag(self, monkeypatch, capsys):
        """Test main with verbose flag."""
        monkeypatch.setattr(sys, "argv", ["validate-tokens.py", "--verbose", "--ignore-planned"])

        with patch.object(validate_tokens_utils, "validate_token") as mock_validate:
            mock_validate.return_value = {
                "token": "test",
                "valid": True,
                "status": "active",
                "scopes": ["repo"],
                "rate_limit": {"remaining": 100, "limit": 5000},
                "error": None,
                "warning": None,
            }
            with pytest.raises(SystemExit):
                validate_tokens_utils.main()

            captured = capsys.readouterr()
            assert "Detailed Results" in captured.out


@pytest.mark.unit
class TestTokensRegistry:
    """Test TOKENS registry configuration."""

    def test_all_tokens_have_required_fields(self):
        """Test all tokens have required configuration fields."""
        for token_name, config in validate_tokens_utils.TOKENS.items():
            assert "scopes" in config, f"{token_name} missing scopes"
            assert "test_endpoint" in config, f"{token_name} missing test_endpoint"
            assert "status" in config, f"{token_name} missing status"

    def test_all_endpoints_start_with_slash(self):
        """Test all test endpoints start with /."""
        for token_name, config in validate_tokens_utils.TOKENS.items():
            assert config["test_endpoint"].startswith("/"), f"{token_name} endpoint should start with /"

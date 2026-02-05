#!/usr/bin/env python3
"""Unit tests for automation/scripts/utils/quick-validate.py

Focus: Quick token validation using environment variables.
Note: This script runs at import time, so we test by mocking and re-importing.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def load_quick_validate(env_vars, mock_responses):
    """Load the quick-validate module with mocked environment and requests."""
    # Remove cached module if present
    if "quick_validate" in sys.modules:
        del sys.modules["quick_validate"]

    # Create mock response
    mock_response = MagicMock()
    mock_response.status_code = mock_responses.get("status_code", 200)
    mock_response.headers = mock_responses.get("headers", {"X-RateLimit-Remaining": "5000"})

    with patch.dict("os.environ", env_vars, clear=True):
        with patch("requests.get", return_value=mock_response):
            spec = importlib.util.spec_from_file_location(
                "quick_validate",
                Path(__file__).parent.parent.parent / "src" / "automation" / "scripts" / "utils" / "quick-validate.py",
            )
            module = importlib.util.module_from_spec(spec)
            # Don't execute - just return for inspection
            return spec, module


@pytest.mark.unit
class TestQuickValidateModule:
    """Test quick-validate module structure."""

    def test_has_expected_token_list(self):
        """Test module has expected token list."""
        expected_tokens = [
            "ORG_LABEL_SYNC_TOKEN",
            "ORG_PROJECT_ADMIN_TOKEN",
            "ORG_ONBOARDING_TOKEN",
            "ORG_REPO_ANALYSIS_TOKEN",
        ]

        # Load spec without executing
        spec = importlib.util.spec_from_file_location(
            "quick_validate_check",
            Path(__file__).parent.parent.parent / "src" / "automation" / "scripts" / "utils" / "quick-validate.py",
        )
        source = spec.loader.get_source("quick_validate_check")

        for token in expected_tokens:
            assert token in source


@pytest.mark.unit
class TestTokenValidation:
    """Test token validation behavior through execution."""

    def test_validates_all_tokens_present(self, capsys):
        """Test validates when all tokens are present."""
        env_vars = {
            "ORG_LABEL_SYNC_TOKEN": "ghp_test1",
            "ORG_PROJECT_ADMIN_TOKEN": "ghp_test2",
            "ORG_ONBOARDING_TOKEN": "ghp_test3",
            "ORG_REPO_ANALYSIS_TOKEN": "ghp_test4",
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch.dict("os.environ", env_vars, clear=True):
            with patch("requests.get", return_value=mock_response):
                with pytest.raises(SystemExit) as exc:
                    exec(
                        compile(
                            open(
                                Path(__file__).parent.parent.parent
                                / "src"
                                / "automation"
                                / "scripts"
                                / "utils"
                                / "quick-validate.py"
                            ).read(),
                            "quick-validate.py",
                            "exec",
                        )
                    )
                assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Valid:  4/4" in captured.out

    def test_reports_missing_tokens(self, capsys):
        """Test reports when tokens are missing."""
        env_vars = {
            "ORG_LABEL_SYNC_TOKEN": "ghp_test1",
            # Missing other tokens
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch.dict("os.environ", env_vars, clear=True):
            with patch("requests.get", return_value=mock_response):
                with pytest.raises(SystemExit) as exc:
                    exec(
                        compile(
                            open(
                                Path(__file__).parent.parent.parent
                                / "src"
                                / "automation"
                                / "scripts"
                                / "utils"
                                / "quick-validate.py"
                            ).read(),
                            "quick-validate.py",
                            "exec",
                        )
                    )
                assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Not found in environment" in captured.out

    def test_reports_invalid_tokens(self, capsys):
        """Test reports when tokens are invalid."""
        env_vars = {
            "ORG_LABEL_SYNC_TOKEN": "invalid_token",
            "ORG_PROJECT_ADMIN_TOKEN": "invalid_token",
            "ORG_ONBOARDING_TOKEN": "invalid_token",
            "ORG_REPO_ANALYSIS_TOKEN": "invalid_token",
        }

        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch.dict("os.environ", env_vars, clear=True):
            with patch("requests.get", return_value=mock_response):
                with pytest.raises(SystemExit) as exc:
                    exec(
                        compile(
                            open(
                                Path(__file__).parent.parent.parent
                                / "src"
                                / "automation"
                                / "scripts"
                                / "utils"
                                / "quick-validate.py"
                            ).read(),
                            "quick-validate.py",
                            "exec",
                        )
                    )
                assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "HTTP 401" in captured.out

    def test_shows_rate_limit_remaining(self, capsys):
        """Test shows rate limit remaining for valid tokens."""
        env_vars = {
            "ORG_LABEL_SYNC_TOKEN": "ghp_test1",
            "ORG_PROJECT_ADMIN_TOKEN": "ghp_test2",
            "ORG_ONBOARDING_TOKEN": "ghp_test3",
            "ORG_REPO_ANALYSIS_TOKEN": "ghp_test4",
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"X-RateLimit-Remaining": "4500"}

        with patch.dict("os.environ", env_vars, clear=True):
            with patch("requests.get", return_value=mock_response):
                with pytest.raises(SystemExit):
                    exec(
                        compile(
                            open(
                                Path(__file__).parent.parent.parent
                                / "src"
                                / "automation"
                                / "scripts"
                                / "utils"
                                / "quick-validate.py"
                            ).read(),
                            "quick-validate.py",
                            "exec",
                        )
                    )

        captured = capsys.readouterr()
        assert "rate limit: 4500/5000" in captured.out

    def test_shows_help_on_failure(self, capsys):
        """Test shows help message on token failure."""
        env_vars = {}  # No tokens

        with patch.dict("os.environ", env_vars, clear=True):
            with pytest.raises(SystemExit) as exc:
                exec(
                    compile(
                        open(
                            Path(__file__).parent.parent.parent
                            / "src"
                            / "automation"
                            / "scripts"
                            / "utils"
                            / "quick-validate.py"
                        ).read(),
                        "quick-validate.py",
                        "exec",
                    )
                )
            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Export them first" in captured.out
        assert "op read" in captured.out

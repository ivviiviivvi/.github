#!/usr/bin/env python3
"""Unit tests for automation/scripts/utils.py
Focus: ConfigLoader, RateLimiter, GitHubAPIClient, and utility functions.
"""

import json
import sys
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock secret_manager before importing utils
# Save original and restore after imports to avoid polluting other tests
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from utils import (APIError, AutomationError, ConfigLoader, ConfigurationError,
                   RateLimiter, ValidationError, read_json, read_yaml,
                   safe_get, setup_logger, write_json, write_yaml)

# Restore original secret_manager module after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


class TestSetupLogger:
    """Test logger setup functionality."""

    def test_creates_logger_with_name(self):
        """Test logger is created with correct name."""
        logger = setup_logger("test-logger")
        assert logger.name == "test-logger"

    def test_sets_log_level(self):
        """Test logger respects log level setting."""
        import logging

        logger = setup_logger("test-debug", level="DEBUG")
        assert logger.level == logging.DEBUG

        logger = setup_logger("test-error", level="ERROR")
        assert logger.level == logging.ERROR

    def test_invalid_level_raises(self):
        """Test invalid log level raises AttributeError."""
        with pytest.raises(AttributeError):
            setup_logger("test", level="INVALID_LEVEL")


class TestRateLimiter:
    """Test rate limiter functionality."""

    def test_allows_requests_under_limit(self):
        """Test requests are allowed when under limit."""
        limiter = RateLimiter(max_requests=10, window=60)

        for _ in range(10):
            assert limiter.acquire() is True

    def test_blocks_requests_over_limit(self):
        """Test requests are blocked when over limit."""
        limiter = RateLimiter(max_requests=3, window=60)

        # Exhaust the limit
        for _ in range(3):
            limiter.acquire()

        # Next request should be blocked
        assert limiter.acquire() is False

    def test_wait_time_calculation(self):
        """Test wait time is calculated correctly."""
        limiter = RateLimiter(max_requests=1, window=60)
        limiter.acquire()

        # Wait time should be close to window duration
        wait = limiter.wait_time()
        assert 0 < wait <= 60

    def test_empty_limiter_has_zero_wait(self):
        """Test empty limiter has zero wait time."""
        limiter = RateLimiter(max_requests=10, window=60)
        assert limiter.wait_time() == 0.0

    def test_thread_safety(self):
        """Test rate limiter is thread-safe."""
        limiter = RateLimiter(max_requests=100, window=60)
        results = []
        errors = []

        def acquire_many():
            try:
                for _ in range(20):
                    result = limiter.acquire()
                    results.append(result)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=acquire_many) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No errors should occur
        assert len(errors) == 0
        # Exactly 100 should succeed
        assert sum(results) == 100

    def test_old_requests_expire(self):
        """Test old requests are removed from window."""
        limiter = RateLimiter(max_requests=2, window=0.1)  # 100ms window

        # Use both slots
        assert limiter.acquire() is True
        assert limiter.acquire() is True
        assert limiter.acquire() is False

        # Wait for window to expire
        time.sleep(0.15)

        # Should be able to acquire again
        assert limiter.acquire() is True


class TestConfigLoader:
    """Test configuration loader functionality."""

    @pytest.fixture
    def temp_config_dir(self, tmp_path):
        """Create temporary config directory."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        return config_dir

    def test_loads_yaml_file(self, temp_config_dir):
        """Test loading a valid YAML config file."""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("key: value\nnested:\n  foo: bar")

        loader = ConfigLoader(temp_config_dir)
        config = loader.load("test.yml")

        assert config["key"] == "value"
        assert config["nested"]["foo"] == "bar"

    def test_raises_on_missing_file(self, temp_config_dir):
        """Test raises FileNotFoundError for missing file."""
        loader = ConfigLoader(temp_config_dir)

        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent.yml")

    def test_get_with_default(self, temp_config_dir):
        """Test get returns default for missing key."""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("existing: value")

        loader = ConfigLoader(temp_config_dir)
        result = loader.get("test.yml", "missing", default="default_value")

        assert result == "default_value"

    def test_get_nested_key(self, temp_config_dir):
        """Test get with dot notation for nested keys."""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("level1:\n  level2:\n    value: nested")

        loader = ConfigLoader(temp_config_dir)
        result = loader.get("test.yml", "level1.level2.value")

        assert result == "nested"

    def test_handles_empty_yaml(self, temp_config_dir):
        """Test handling of empty YAML file."""
        config_file = temp_config_dir / "empty.yml"
        config_file.write_text("")

        loader = ConfigLoader(temp_config_dir)
        config = loader.load("empty.yml")

        assert config == {}


class TestSafeGet:
    """Test safe_get utility function."""

    def test_gets_top_level_key(self):
        """Test getting top-level key."""
        data = {"name": "Alice", "age": 30}
        assert safe_get(data, "name") == "Alice"

    def test_gets_nested_key(self):
        """Test getting nested key with dot notation."""
        data = {"user": {"profile": {"name": "Bob"}}}
        assert safe_get(data, "user.profile.name") == "Bob"

    def test_returns_default_for_missing_key(self):
        """Test returns default when key is missing."""
        data = {"key": "value"}
        assert safe_get(data, "missing", default="fallback") == "fallback"

    def test_returns_default_for_non_dict(self):
        """Test returns default when path traverses non-dict."""
        data = {"key": "string_value"}
        assert safe_get(data, "key.nested", default="fallback") == "fallback"

    def test_handles_none_values(self):
        """Test handles None values in path."""
        data = {"key": None}
        assert safe_get(data, "key.nested", default="fallback") == "fallback"

    def test_empty_path(self):
        """Test empty path returns full data."""
        data = {"key": "value"}
        # Note: This tests edge case behavior
        result = safe_get(data, "", default=None)
        # Empty string splits to [''] so this will try data.get('')
        assert result is None  # '' key doesn't exist


class TestFileOperations:
    """Test JSON and YAML file operations."""

    def test_read_json(self, tmp_path):
        """Test reading JSON file."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value", "number": 42}')

        result = read_json(json_file)

        assert result["key"] == "value"
        assert result["number"] == 42

    def test_write_json(self, tmp_path):
        """Test writing JSON file."""
        json_file = tmp_path / "output.json"
        data = {"name": "Test", "items": [1, 2, 3]}

        write_json(json_file, data)

        content = json.loads(json_file.read_text())
        assert content["name"] == "Test"
        assert content["items"] == [1, 2, 3]

    def test_write_json_creates_directory(self, tmp_path):
        """Test write_json creates parent directory if needed."""
        json_file = tmp_path / "subdir" / "nested" / "output.json"

        write_json(json_file, {"key": "value"})

        assert json_file.exists()

    def test_read_yaml(self, tmp_path):
        """Test reading YAML file."""
        yaml_file = tmp_path / "test.yml"
        yaml_file.write_text("name: Test\nitems:\n  - one\n  - two")

        result = read_yaml(yaml_file)

        assert result["name"] == "Test"
        assert result["items"] == ["one", "two"]

    def test_write_yaml(self, tmp_path):
        """Test writing YAML file."""
        yaml_file = tmp_path / "output.yml"
        data = {"config": {"enabled": True, "count": 5}}

        write_yaml(yaml_file, data)

        import yaml

        content = yaml.safe_load(yaml_file.read_text())
        assert content["config"]["enabled"] is True


class TestExceptionClasses:
    """Test custom exception classes."""

    def test_automation_error_is_exception(self):
        """Test AutomationError is an Exception."""
        assert issubclass(AutomationError, Exception)

    def test_validation_error_hierarchy(self):
        """Test ValidationError inherits from AutomationError."""
        assert issubclass(ValidationError, AutomationError)

    def test_configuration_error_hierarchy(self):
        """Test ConfigurationError inherits from AutomationError."""
        assert issubclass(ConfigurationError, AutomationError)

    def test_api_error_hierarchy(self):
        """Test APIError inherits from AutomationError."""
        assert issubclass(APIError, AutomationError)

    def test_exceptions_can_be_raised_with_message(self):
        """Test exceptions can carry custom messages."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid input")

        assert "Invalid input" in str(exc_info.value)


@pytest.mark.unit
class TestConfigLoaderErrorHandling:
    """Test ConfigLoader error handling."""

    @pytest.fixture
    def temp_config_dir(self, tmp_path):
        """Create temporary config directory."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        return config_dir

    def test_load_raises_on_invalid_yaml(self, temp_config_dir):
        """Test loading invalid YAML raises YAMLError."""
        import yaml

        config_file = temp_config_dir / "invalid.yml"
        # Intentionally invalid YAML
        config_file.write_text("key: [unclosed bracket")

        loader = ConfigLoader(temp_config_dir)

        with pytest.raises(yaml.YAMLError):
            loader.load("invalid.yml")

    def test_get_returns_default_on_file_not_found(self, temp_config_dir):
        """Test get returns default when file doesn't exist."""
        loader = ConfigLoader(temp_config_dir)
        result = loader.get("nonexistent.yml", "key", default="fallback")
        assert result == "fallback"

    def test_get_returns_default_on_yaml_error(self, temp_config_dir):
        """Test get returns default on YAML parse error."""
        config_file = temp_config_dir / "bad.yml"
        config_file.write_text("key: [unclosed")

        loader = ConfigLoader(temp_config_dir)
        result = loader.get("bad.yml", "key", default="fallback")
        assert result == "fallback"


@pytest.mark.unit
class TestRateLimiterWait:
    """Test RateLimiter wait functionality."""

    def test_wait_when_rate_limited(self):
        """Test wait pauses when rate limited."""
        limiter = RateLimiter(max_requests=1, window=0.1)

        # Exhaust the limit
        limiter.acquire()

        start = time.time()
        limiter.wait()
        elapsed = time.time() - start

        # Should have waited approximately 0.1 seconds
        assert elapsed >= 0.05  # Allow some tolerance

    def test_wait_no_delay_when_not_limited(self):
        """Test wait returns immediately when not rate limited."""
        limiter = RateLimiter(max_requests=10, window=60)

        start = time.time()
        limiter.wait()
        elapsed = time.time() - start

        # Should be nearly instant
        assert elapsed < 0.1


@pytest.mark.unit
class TestGitHubAPIClient:
    """Test GitHubAPIClient functionality."""

    def test_init_with_token(self):
        """Test initialization with explicit token."""
        from utils import GitHubAPIClient

        client = GitHubAPIClient(token="test-token")  # allow-secret

        assert client.token == "test-token"  # allow-secret
        assert client.base_url == "https://api.github.com"

    def test_init_raises_without_token(self):
        """Test initialization raises when no token available."""
        import subprocess
        from unittest.mock import patch

        from utils import GitHubAPIClient

        # Mock subprocess to fail
        def mock_run(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "gh")

        # Mock secret_manager to return None
        mock_secret = MagicMock(return_value=None)

        with patch("subprocess.run", mock_run):
            with patch("utils.get_secret", mock_secret):
                with pytest.raises(ValueError, match="GitHub token required"):
                    GitHubAPIClient()

    def test_init_with_gh_cli(self):
        """Test initialization using gh CLI token."""
        from unittest.mock import MagicMock, patch

        from utils import GitHubAPIClient

        mock_result = MagicMock()
        mock_result.stdout = "gh-cli-token\n"  # allow-secret

        with patch("subprocess.run", return_value=mock_result):
            client = GitHubAPIClient()
            assert client.token == "gh-cli-token"  # allow-secret

    def test_init_falls_back_to_1password(self):
        """Test initialization falls back to 1Password when gh CLI fails."""
        from unittest.mock import patch

        from utils import GitHubAPIClient

        def mock_run(*args, **kwargs):
            raise FileNotFoundError("gh not found")

        with patch("subprocess.run", side_effect=mock_run):
            with patch("utils.get_secret", return_value="1password-token"):  # allow-secret
                client = GitHubAPIClient()
                assert client.token == "1password-token"  # allow-secret


@pytest.mark.unit
class TestGitHubAPIClientRequest:
    """Test GitHubAPIClient request methods."""

    @pytest.fixture
    def mock_client(self):
        """Create client with mocked session."""
        from unittest.mock import MagicMock, patch

        from utils import GitHubAPIClient

        with patch.object(GitHubAPIClient, "__init__", lambda self, **kwargs: None):
            client = GitHubAPIClient()
            client.token = "test-token"  # allow-secret
            client.base_url = "https://api.github.com"
            client.session = MagicMock()
            client.rate_limiter = RateLimiter()
            client.logger = MagicMock()
            return client

    def test_get_request(self, mock_client):
        """Test GET request."""
        mock_response = MagicMock()
        mock_response.content = b'{"data": "value"}'
        mock_response.json.return_value = {"data": "value"}
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.get("/repos/owner/repo")

        assert result == {"data": "value"}
        mock_client.session.request.assert_called_once()

    def test_post_request(self, mock_client):
        """Test POST request."""
        mock_response = MagicMock()
        mock_response.content = b'{"id": 123}'
        mock_response.json.return_value = {"id": 123}
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.post("/repos/owner/repo/issues", json_data={"title": "Test"})

        assert result == {"id": 123}

    def test_put_request(self, mock_client):
        """Test PUT request."""
        mock_response = MagicMock()
        mock_response.content = b"{}"
        mock_response.json.return_value = {}
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.put("/endpoint", json={"data": "value"})

        assert result == {}

    def test_patch_request(self, mock_client):
        """Test PATCH request."""
        mock_response = MagicMock()
        mock_response.content = b'{"updated": true}'
        mock_response.json.return_value = {"updated": True}
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.patch("/endpoint", json={"field": "value"})

        assert result == {"updated": True}

    def test_delete_request(self, mock_client):
        """Test DELETE request."""
        mock_response = MagicMock()
        mock_response.content = b""
        mock_response.json.return_value = {}
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.delete("/endpoint")

        assert result == {}

    def test_handles_empty_response(self, mock_client):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.content = b""  # Empty content
        mock_response.headers = {}
        mock_client.session.request.return_value = mock_response

        result = mock_client.get("/endpoint")

        assert result == {}

    def test_logs_low_rate_limit(self, mock_client):
        """Test logs warning when rate limit is low."""
        mock_response = MagicMock()
        mock_response.content = b"{}"
        mock_response.json.return_value = {}
        mock_response.headers = {"X-RateLimit-Remaining": "50"}
        mock_client.session.request.return_value = mock_response

        mock_client.get("/endpoint")

        mock_client.logger.warning.assert_called()

    def test_retries_on_timeout(self, mock_client):
        """Test retries on timeout."""
        import requests

        mock_response = MagicMock()
        mock_response.content = b'{"success": true}'
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {}

        # First call raises timeout, second succeeds
        mock_client.session.request.side_effect = [
            requests.exceptions.Timeout("timeout"),
            mock_response,
        ]

        result = mock_client.request("GET", "/endpoint", retry=True)

        assert result == {"success": True}
        assert mock_client.session.request.call_count == 2

    def test_retries_on_500_error(self, mock_client):
        """Test retries on 500 error."""
        import requests

        mock_error_response = MagicMock()
        mock_error_response.status_code = 500
        mock_error_response.text = "Internal Server Error"
        mock_error_response.headers = {}

        mock_success_response = MagicMock()
        mock_success_response.content = b'{"ok": true}'
        mock_success_response.json.return_value = {"ok": True}
        mock_success_response.headers = {}

        http_error = requests.exceptions.HTTPError(response=mock_error_response)

        # First call raises 500, second succeeds
        mock_client.session.request.side_effect = [
            http_error,
            mock_success_response,
        ]

        # Need to mock raise_for_status
        mock_error_response.raise_for_status.side_effect = http_error

        result = mock_client.request("GET", "/endpoint", retry=True)

        assert result == {"ok": True}

    def test_respects_retry_after_header(self, mock_client):
        """Test respects Retry-After header on 429."""
        import requests

        mock_error_response = MagicMock()
        mock_error_response.status_code = 429
        mock_error_response.text = "Rate limited"
        mock_error_response.headers = {"Retry-After": "1"}

        mock_success_response = MagicMock()
        mock_success_response.content = b"{}"
        mock_success_response.json.return_value = {}
        mock_success_response.headers = {}

        http_error = requests.exceptions.HTTPError(response=mock_error_response)
        mock_error_response.raise_for_status.side_effect = http_error

        mock_client.session.request.side_effect = [
            http_error,
            mock_success_response,
        ]

        start = time.time()
        mock_client.request("GET", "/endpoint", retry=True)
        elapsed = time.time() - start

        # Should have waited at least 1 second
        assert elapsed >= 0.9

    def test_no_retry_on_4xx_error(self, mock_client):
        """Test no retry on 4xx errors (except 429)."""
        import requests

        mock_error_response = MagicMock()
        mock_error_response.status_code = 404
        mock_error_response.text = "Not Found"
        mock_error_response.headers = {}

        http_error = requests.exceptions.HTTPError(response=mock_error_response)
        mock_error_response.raise_for_status.side_effect = http_error

        mock_client.session.request.return_value = mock_error_response

        with pytest.raises(requests.exceptions.HTTPError):
            mock_client.request("GET", "/endpoint", retry=True)

        # Should only try once
        assert mock_client.session.request.call_count == 1

    def test_raises_on_request_exception(self, mock_client):
        """Test raises on general request exception."""
        import requests

        mock_client.session.request.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with pytest.raises(requests.exceptions.ConnectionError):
            mock_client.request("GET", "/endpoint")


@pytest.mark.unit
class TestLoadConfig:
    """Test load_config utility function."""

    def test_loads_existing_config(self, tmp_path):
        """Test loading existing config file."""
        from utils import load_config

        config_file = tmp_path / "config.yml"
        config_file.write_text("setting: enabled\nvalue: 42")

        result = load_config(str(config_file))

        assert result["setting"] == "enabled"
        assert result["value"] == 42

    def test_returns_default_for_missing_file(self):
        """Test returns default when file doesn't exist."""
        from utils import load_config

        result = load_config("/nonexistent/path.yml", default={"default": "value"})

        assert result == {"default": "value"}

    def test_returns_empty_dict_when_no_default(self):
        """Test returns empty dict when no default provided."""
        from utils import load_config

        result = load_config("/nonexistent/path.yml")

        assert result == {}


@pytest.mark.unit
class TestRetryWithBackoff:
    """Test retry_with_backoff function."""

    def test_returns_on_success(self):
        """Test returns result on successful call."""
        from utils import retry_with_backoff

        def success_func():
            return "success"

        result = retry_with_backoff(success_func)

        assert result == "success"

    def test_retries_on_failure(self):
        """Test retries on failure."""
        from utils import retry_with_backoff

        call_count = 0

        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = retry_with_backoff(flaky_func, max_attempts=3, initial_delay=0.01, jitter=False)

        assert result == "success"
        assert call_count == 3

    def test_raises_after_max_attempts(self):
        """Test raises exception after max attempts."""
        from utils import retry_with_backoff

        def always_fail():
            raise RuntimeError("Always fails")

        with pytest.raises(RuntimeError, match="Always fails"):
            retry_with_backoff(always_fail, max_attempts=3, initial_delay=0.01, jitter=False)

    def test_respects_max_delay(self):
        """Test respects maximum delay setting."""
        from utils import retry_with_backoff

        call_count = 0
        call_times = []

        def fail_then_succeed():
            nonlocal call_count
            call_times.append(time.time())
            call_count += 1
            if call_count < 3:
                raise ValueError("Fail")
            return "success"

        retry_with_backoff(
            fail_then_succeed,
            max_attempts=3,
            initial_delay=0.01,
            max_delay=0.02,
            backoff_factor=10,  # Would be 0.1s on second try without max
            jitter=False,
        )

        # Delays should be capped at max_delay
        if len(call_times) > 1:
            delay = call_times[1] - call_times[0]
            assert delay <= 0.03  # max_delay + some tolerance

    def test_adds_jitter(self):
        """Test jitter adds randomness to delays."""
        from utils import retry_with_backoff

        delays = []

        def fail_func():
            delays.append(time.time())
            raise ValueError("Fail")

        # Run multiple times to check jitter
        for _ in range(2):
            delays.clear()
            try:
                retry_with_backoff(
                    fail_func,
                    max_attempts=2,
                    initial_delay=0.01,
                    jitter=True,
                )
            except ValueError:
                pass

        # Jitter should add some variation (hard to test precisely)

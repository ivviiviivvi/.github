#!/usr/bin/env python3
"""
Unit tests for automation/scripts/utils.py
Focus: ConfigLoader, RateLimiter, GitHubAPIClient, and utility functions
"""

import json
import sys
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

# Mock secret_manager before importing utils
# Save original and restore after imports to avoid polluting other tests
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from utils import (
    APIError,
    AutomationError,
    ConfigLoader,
    ConfigurationError,
    RateLimiter,
    ValidationError,
    read_json,
    read_yaml,
    safe_get,
    setup_logger,
    write_json,
    write_yaml,
)

# Restore original secret_manager module after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


class TestSetupLogger:
    """Test logger setup functionality"""

    def test_creates_logger_with_name(self):
        """Test logger is created with correct name"""
        logger = setup_logger("test-logger")
        assert logger.name == "test-logger"

    def test_sets_log_level(self):
        """Test logger respects log level setting"""
        import logging

        logger = setup_logger("test-debug", level="DEBUG")
        assert logger.level == logging.DEBUG

        logger = setup_logger("test-error", level="ERROR")
        assert logger.level == logging.ERROR

    def test_invalid_level_raises(self):
        """Test invalid log level raises AttributeError"""
        with pytest.raises(AttributeError):
            setup_logger("test", level="INVALID_LEVEL")


class TestRateLimiter:
    """Test rate limiter functionality"""

    def test_allows_requests_under_limit(self):
        """Test requests are allowed when under limit"""
        limiter = RateLimiter(max_requests=10, window=60)

        for _ in range(10):
            assert limiter.acquire() is True

    def test_blocks_requests_over_limit(self):
        """Test requests are blocked when over limit"""
        limiter = RateLimiter(max_requests=3, window=60)

        # Exhaust the limit
        for _ in range(3):
            limiter.acquire()

        # Next request should be blocked
        assert limiter.acquire() is False

    def test_wait_time_calculation(self):
        """Test wait time is calculated correctly"""
        limiter = RateLimiter(max_requests=1, window=60)
        limiter.acquire()

        # Wait time should be close to window duration
        wait = limiter.wait_time()
        assert 0 < wait <= 60

    def test_empty_limiter_has_zero_wait(self):
        """Test empty limiter has zero wait time"""
        limiter = RateLimiter(max_requests=10, window=60)
        assert limiter.wait_time() == 0.0

    def test_thread_safety(self):
        """Test rate limiter is thread-safe"""
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
        """Test old requests are removed from window"""
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
    """Test configuration loader functionality"""

    @pytest.fixture
    def temp_config_dir(self, tmp_path):
        """Create temporary config directory"""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        return config_dir

    def test_loads_yaml_file(self, temp_config_dir):
        """Test loading a valid YAML config file"""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("key: value\nnested:\n  foo: bar")

        loader = ConfigLoader(temp_config_dir)
        config = loader.load("test.yml")

        assert config["key"] == "value"
        assert config["nested"]["foo"] == "bar"

    def test_raises_on_missing_file(self, temp_config_dir):
        """Test raises FileNotFoundError for missing file"""
        loader = ConfigLoader(temp_config_dir)

        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent.yml")

    def test_get_with_default(self, temp_config_dir):
        """Test get returns default for missing key"""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("existing: value")

        loader = ConfigLoader(temp_config_dir)
        result = loader.get("test.yml", "missing", default="default_value")

        assert result == "default_value"

    def test_get_nested_key(self, temp_config_dir):
        """Test get with dot notation for nested keys"""
        config_file = temp_config_dir / "test.yml"
        config_file.write_text("level1:\n  level2:\n    value: nested")

        loader = ConfigLoader(temp_config_dir)
        result = loader.get("test.yml", "level1.level2.value")

        assert result == "nested"

    def test_handles_empty_yaml(self, temp_config_dir):
        """Test handling of empty YAML file"""
        config_file = temp_config_dir / "empty.yml"
        config_file.write_text("")

        loader = ConfigLoader(temp_config_dir)
        config = loader.load("empty.yml")

        assert config == {}


class TestSafeGet:
    """Test safe_get utility function"""

    def test_gets_top_level_key(self):
        """Test getting top-level key"""
        data = {"name": "Alice", "age": 30}
        assert safe_get(data, "name") == "Alice"

    def test_gets_nested_key(self):
        """Test getting nested key with dot notation"""
        data = {"user": {"profile": {"name": "Bob"}}}
        assert safe_get(data, "user.profile.name") == "Bob"

    def test_returns_default_for_missing_key(self):
        """Test returns default when key is missing"""
        data = {"key": "value"}
        assert safe_get(data, "missing", default="fallback") == "fallback"

    def test_returns_default_for_non_dict(self):
        """Test returns default when path traverses non-dict"""
        data = {"key": "string_value"}
        assert safe_get(data, "key.nested", default="fallback") == "fallback"

    def test_handles_none_values(self):
        """Test handles None values in path"""
        data = {"key": None}
        assert safe_get(data, "key.nested", default="fallback") == "fallback"

    def test_empty_path(self):
        """Test empty path returns full data"""
        data = {"key": "value"}
        # Note: This tests edge case behavior
        result = safe_get(data, "", default=None)
        # Empty string splits to [''] so this will try data.get('')
        assert result is None  # '' key doesn't exist


class TestFileOperations:
    """Test JSON and YAML file operations"""

    def test_read_json(self, tmp_path):
        """Test reading JSON file"""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value", "number": 42}')

        result = read_json(json_file)

        assert result["key"] == "value"
        assert result["number"] == 42

    def test_write_json(self, tmp_path):
        """Test writing JSON file"""
        json_file = tmp_path / "output.json"
        data = {"name": "Test", "items": [1, 2, 3]}

        write_json(json_file, data)

        content = json.loads(json_file.read_text())
        assert content["name"] == "Test"
        assert content["items"] == [1, 2, 3]

    def test_write_json_creates_directory(self, tmp_path):
        """Test write_json creates parent directory if needed"""
        json_file = tmp_path / "subdir" / "nested" / "output.json"

        write_json(json_file, {"key": "value"})

        assert json_file.exists()

    def test_read_yaml(self, tmp_path):
        """Test reading YAML file"""
        yaml_file = tmp_path / "test.yml"
        yaml_file.write_text("name: Test\nitems:\n  - one\n  - two")

        result = read_yaml(yaml_file)

        assert result["name"] == "Test"
        assert result["items"] == ["one", "two"]

    def test_write_yaml(self, tmp_path):
        """Test writing YAML file"""
        yaml_file = tmp_path / "output.yml"
        data = {"config": {"enabled": True, "count": 5}}

        write_yaml(yaml_file, data)

        import yaml

        content = yaml.safe_load(yaml_file.read_text())
        assert content["config"]["enabled"] is True


class TestExceptionClasses:
    """Test custom exception classes"""

    def test_automation_error_is_exception(self):
        """Test AutomationError is an Exception"""
        assert issubclass(AutomationError, Exception)

    def test_validation_error_hierarchy(self):
        """Test ValidationError inherits from AutomationError"""
        assert issubclass(ValidationError, AutomationError)

    def test_configuration_error_hierarchy(self):
        """Test ConfigurationError inherits from AutomationError"""
        assert issubclass(ConfigurationError, AutomationError)

    def test_api_error_hierarchy(self):
        """Test APIError inherits from AutomationError"""
        assert issubclass(APIError, AutomationError)

    def test_exceptions_can_be_raised_with_message(self):
        """Test exceptions can carry custom messages"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid input")

        assert "Invalid input" in str(exc_info.value)

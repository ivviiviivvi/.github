#!/usr/bin/env python3
"""Extended unit tests for quota_manager.py to improve coverage.

Focus: acquire_lock edge cases, file error handling, date parsing, CLI.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


@pytest.mark.unit
class TestAcquireLockFcntl:
    """Test acquire_lock using fcntl (Unix)."""

    def test_lock_file_creation_oserror(self):
        """Test lock file creation handles OSError."""
        import quota_manager

        with patch("quota_manager.HAS_FCNTL", True):
            with patch("os.path.exists", return_value=False):
                with patch("builtins.open", side_effect=[OSError("Permission denied"), MagicMock()]):
                    with patch("quota_manager.fcntl") as mock_fcntl:
                        mock_fcntl.LOCK_EX = 2
                        mock_fcntl.LOCK_NB = 4
                        mock_fcntl.LOCK_UN = 8
                        mock_fcntl.flock.return_value = None

                        # Should not raise, OSError is caught
                        with quota_manager.acquire_lock(timeout=1):
                            pass

    def test_lock_timeout_fcntl(self):
        """Test acquire_lock timeout with fcntl."""
        import quota_manager

        with patch("quota_manager.HAS_FCNTL", True):
            with patch("os.path.exists", return_value=True):
                mock_fd = MagicMock()
                with patch("builtins.open", return_value=mock_fd):
                    with patch("quota_manager.fcntl") as mock_fcntl:
                        mock_fcntl.LOCK_EX = 2
                        mock_fcntl.LOCK_NB = 4
                        mock_fcntl.LOCK_UN = 8
                        mock_fcntl.flock.side_effect = OSError("Lock held")

                        with pytest.raises(TimeoutError):
                            with quota_manager.acquire_lock(timeout=0.1):
                                pass


@pytest.mark.unit
class TestAcquireLockFallback:
    """Test acquire_lock using directory-based fallback (Windows)."""

    def test_fallback_lock_acquires_and_releases(self):
        """Test fallback lock acquires and releases directory."""
        import quota_manager

        with patch("quota_manager.HAS_FCNTL", False):
            with patch("os.mkdir") as mock_mkdir:
                with patch("os.rmdir") as mock_rmdir:
                    with quota_manager.acquire_lock(timeout=1):
                        mock_mkdir.assert_called_once()
                    mock_rmdir.assert_called_once()

    def test_fallback_lock_timeout(self):
        """Test fallback lock timeout on FileExistsError."""
        import quota_manager

        with patch("quota_manager.HAS_FCNTL", False):
            with patch("os.mkdir", side_effect=FileExistsError):
                with pytest.raises(TimeoutError):
                    with quota_manager.acquire_lock(timeout=0.2):
                        pass

    def test_fallback_lock_retries_on_exists(self):
        """Test fallback lock retries when directory exists."""
        import quota_manager

        call_count = [0]

        def mkdir_side_effect(path):
            call_count[0] += 1
            if call_count[0] < 3:
                raise FileExistsError("Lock held")
            # Third call succeeds

        with patch("quota_manager.HAS_FCNTL", False):
            with patch("os.mkdir", side_effect=mkdir_side_effect):
                with patch("os.rmdir"):
                    with quota_manager.acquire_lock(timeout=5):
                        pass

        assert call_count[0] == 3


@pytest.mark.unit
class TestGetSubscriptions:
    """Test get_subscriptions function."""

    def test_file_not_found_returns_empty(self):
        """Test returns empty subscriptions when file not found."""
        import quota_manager

        with patch("builtins.open", side_effect=FileNotFoundError):
            result = quota_manager.get_subscriptions()
        assert result == {"subscriptions": []}

    def test_json_decode_error_returns_empty(self):
        """Test returns empty subscriptions on JSON decode error."""
        import quota_manager

        with patch("builtins.open", mock_open(read_data="invalid json {")):
            result = quota_manager.get_subscriptions()
        assert result == {"subscriptions": []}


@pytest.mark.unit
class TestIncrementUsage:
    """Test increment_usage function."""

    def test_file_not_found_creates_new(self):
        """Test creates new subscriptions when file not found."""
        import quota_manager

        call_data = {}

        def track_dump(data, f, **kwargs):
            call_data["data"] = data

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", side_effect=[FileNotFoundError, MagicMock()]):
                with patch("json.dump", side_effect=track_dump):
                    quota_manager.increment_usage("test-sub", 1)

        # Should have empty subscriptions list since file not found
        assert call_data["data"] == {"subscriptions": []}


@pytest.mark.unit
class TestResetQuotas:
    """Test reset_quotas function."""

    def test_file_not_found_returns_early(self):
        """Test returns early when file not found."""
        import quota_manager

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", side_effect=FileNotFoundError):
                with patch("json.dump") as mock_dump:
                    quota_manager.reset_quotas()
                    mock_dump.assert_not_called()

    def test_invalid_date_skips_subscription(self):
        """Test subscriptions with invalid dates are skipped."""
        import quota_manager

        subscriptions = {
            "subscriptions": [
                {
                    "name": "bad-date-sub",
                    "usage": 10,
                    "reset_cadence": "daily",
                    "last_reset": "not-a-date",
                }
            ]
        }

        written_data = {}

        def track_dump(data, f, **kwargs):
            written_data["data"] = data

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", mock_open()):
                with patch("json.load", return_value=subscriptions):
                    with patch("json.dump", side_effect=track_dump):
                        quota_manager.reset_quotas()

        # Usage should not be reset because last_reset couldn't be parsed
        assert written_data["data"]["subscriptions"][0]["usage"] == 10

    def test_last_reset_none_from_valueerror(self):
        """Test subscriptions with invalid date string trigger ValueError catch."""
        import quota_manager

        subscriptions = {
            "subscriptions": [
                {
                    "name": "bad-format-sub",
                    "usage": 5,
                    "reset_cadence": "daily",
                    "last_reset": "01-01-2023",  # Wrong format, will cause ValueError
                }
            ]
        }

        written_data = {}

        def track_dump(data, f, **kwargs):
            written_data["data"] = data

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", mock_open()):
                with patch("json.load", return_value=subscriptions):
                    with patch("json.dump", side_effect=track_dump):
                        quota_manager.reset_quotas()

        # Usage should not be reset because ValueError was caught
        # and last_reset became None, triggering continue
        assert written_data["data"]["subscriptions"][0]["usage"] == 5


@pytest.mark.unit
class TestTaskQueueFunctions:
    """Test task queue functions."""

    def test_add_task_file_not_found_creates_new(self):
        """Test add_task creates new queue when file not found."""
        import quota_manager

        written_data = {}

        def track_dump(data, f, **kwargs):
            written_data["data"] = data

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", side_effect=[FileNotFoundError, MagicMock()]):
                with patch("json.dump", side_effect=track_dump):
                    quota_manager.add_task_to_queue({"task": "test"})

        assert written_data["data"] == [{"task": "test"}]

    def test_get_tasks_file_not_found_returns_empty(self):
        """Test get_tasks returns empty list when file not found."""
        import quota_manager

        with patch("builtins.open", side_effect=FileNotFoundError):
            result = quota_manager.get_tasks_from_queue()
        assert result == []

    def test_get_tasks_json_error_returns_empty(self):
        """Test get_tasks returns empty list on JSON error."""
        import quota_manager

        with patch("builtins.open", mock_open(read_data="not json")):
            result = quota_manager.get_tasks_from_queue()
        assert result == []

    def test_remove_task_file_not_found_returns(self):
        """Test remove_task returns early when file not found."""
        import quota_manager

        with patch("quota_manager.acquire_lock"):
            with patch("builtins.open", side_effect=FileNotFoundError):
                with patch("json.dump") as mock_dump:
                    quota_manager.remove_task_from_queue({"task": "test"})
                    mock_dump.assert_not_called()


@pytest.mark.unit
class TestMainCLI:
    """Test main function CLI."""

    def test_main_no_args_does_nothing(self):
        """Test main with no args does nothing."""
        import quota_manager

        with patch("sys.argv", ["quota_manager.py"]):
            # Should not raise
            quota_manager.main()

    def test_main_increment_default_amount(self):
        """Test main increment_usage with default amount."""
        import quota_manager

        with patch("sys.argv", ["quota_manager.py", "increment_usage", "sub1"]):
            with patch("quota_manager.increment_usage") as mock_inc:
                quota_manager.main()
                mock_inc.assert_called_with("sub1", 1)


@pytest.mark.unit
class TestHasFcntlImport:
    """Test fcntl import handling."""

    def test_module_handles_no_fcntl(self):
        """Test module works when fcntl is not available."""
        # We can't truly test the import failure, but we can test
        # that the fallback path works correctly
        import quota_manager

        # Temporarily set HAS_FCNTL to False
        original = quota_manager.HAS_FCNTL
        try:
            quota_manager.HAS_FCNTL = False

            with patch("os.mkdir") as mock_mkdir:
                with patch("os.rmdir"):
                    with quota_manager.acquire_lock(timeout=1):
                        mock_mkdir.assert_called_once()
        finally:
            quota_manager.HAS_FCNTL = original

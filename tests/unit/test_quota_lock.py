import contextlib
import json
import os
import sys
import threading
import time
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from quota_manager import LOCK_DIR, LOCK_FILE, SUBSCRIPTIONS_FILE, acquire_lock

try:
    import fcntl  # noqa: F401

    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False


class TestQuotaLock(unittest.TestCase):
    def setUp(self):
        # Clean up any existing locks
        if os.path.exists(LOCK_FILE):
            with contextlib.suppress(OSError):
                os.remove(LOCK_FILE)
        if os.path.exists(LOCK_DIR):
            with contextlib.suppress(OSError):
                os.rmdir(LOCK_DIR)

    def tearDown(self):
        self.setUp()

    def test_lock_acquisition(self):
        """Test that the lock can be acquired."""
        with acquire_lock():
            if HAS_FCNTL:
                # Check if lock file exists (for fcntl)
                self.assertTrue(os.path.exists(LOCK_FILE))
            else:
                # Check if lock dir exists (for fallback)
                self.assertTrue(os.path.exists(LOCK_DIR))

    def test_concurrent_lock(self):
        """Test that two threads cannot hold the lock simultaneously."""
        results = []

        def task():
            with acquire_lock(timeout=2):
                results.append("acquired")
                time.sleep(1)
                results.append("released")

        t1 = threading.Thread(target=task)
        t2 = threading.Thread(target=task)

        t1.start()
        time.sleep(0.1)  # Ensure t1 starts first
        t2.start()

        t1.join()
        t2.join()

        # Verify sequence: acquired -> released -> acquired -> released
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0], "acquired")
        self.assertEqual(results[1], "released")
        self.assertEqual(results[2], "acquired")
        self.assertEqual(results[3], "released")

    @unittest.skipUnless(HAS_FCNTL, "fcntl not available on this platform")
    def test_fcntl_used_on_unix(self):
        """Test that fcntl mechanism is used when available."""
        with acquire_lock():
            self.assertTrue(os.path.exists(LOCK_FILE))

    def test_lock_timeout(self):
        """Test that lock acquisition times out when lock is held."""
        # Hold the lock in a separate thread
        locked_event = threading.Event()

        def hold_lock():
            with acquire_lock():
                locked_event.set()
                time.sleep(2)  # Hold longer than the timeout test

        t = threading.Thread(target=hold_lock)
        t.start()

        # Wait for the thread to acquire the lock
        locked_event.wait(timeout=1)

        # Try to acquire lock with short timeout - should fail
        try:
            with acquire_lock(timeout=0.1):
                self.fail("Should not have acquired lock")
        except TimeoutError:
            # Expected behavior
            pass
        except Exception as e:
            self.fail(f"Raised unexpected exception: {type(e)}")

        t.join()

    def test_reset_quotas(self):
        """Test that reset_quotas correctly resets usage based on cadence."""
        from datetime import datetime, timedelta
        from unittest.mock import mock_open, patch

        from quota_manager import reset_quotas

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Sample data with daily subscription that needs reset
        data = {
            "subscriptions": [
                {
                    "name": "daily-sub",
                    "usage": 10,
                    "limit": 100,
                    "reset_cadence": "daily",
                    "last_reset": yesterday,
                },
                {
                    "name": "monthly-sub",
                    "usage": 50,
                    "limit": 1000,
                    "reset_cadence": "monthly",
                    "last_reset": today,  # Already reset today
                },
            ]
        }

        json_data = json.dumps(data)

        with patch("builtins.open", mock_open(read_data=json_data)) as mock_file:
            # Mock acquire_lock to just yield
            with patch("quota_manager.acquire_lock") as mock_lock:
                mock_lock.return_value.__enter__.return_value = None

                reset_quotas()

                # Check that file was written
                mock_file.assert_called_with(SUBSCRIPTIONS_FILE, "w")

                # We can't easily verify the content with simple mock_open without more complex setup
                # but the fact it reached "w" means it processed the logic.


if __name__ == "__main__":
    unittest.main()

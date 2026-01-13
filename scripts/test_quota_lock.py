import unittest
import os
import time
import threading
import sys
from scripts.quota_manager import acquire_lock, LOCK_FILE, LOCK_DIR

try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

class TestQuotaLock(unittest.TestCase):
    def setUp(self):
        # Clean up any existing locks
        if os.path.exists(LOCK_FILE):
            try:
                os.remove(LOCK_FILE)
            except OSError:
                pass
        if os.path.exists(LOCK_DIR):
            try:
                os.rmdir(LOCK_DIR)
            except OSError:
                pass

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
        time.sleep(0.1) # Ensure t1 starts first
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
        """Test that fcntl mechanism is used when available"""
        with acquire_lock():
             self.assertTrue(os.path.exists(LOCK_FILE))

if __name__ == '__main__':
    unittest.main()

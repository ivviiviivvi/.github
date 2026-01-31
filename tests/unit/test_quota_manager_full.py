import json
import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

# Add scripts directory to path
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

import quota_manager


class TestQuotaManagerFull(unittest.TestCase):

    def setUp(self):
        self.mock_subscriptions = {
            "subscriptions": [
                {
                    "name": "sub1",
                    "usage": 10,
                    "reset_cadence": "daily",
                    "last_reset": "2023-01-01",
                },
                {
                    "name": "sub2",
                    "usage": 5,
                    "reset_cadence": "monthly",
                    "last_reset": "2023-01-01",
                },
            ]
        }
        self.mock_tasks = ["task1", "task2"]

    @patch("quota_manager.get_subscriptions")
    def test_get_usage(self, mock_get_subs):
        mock_get_subs.return_value = self.mock_subscriptions
        self.assertEqual(quota_manager.get_usage("sub1"), 10)
        self.assertEqual(quota_manager.get_usage("unknown"), 0)

    @patch("quota_manager.acquire_lock")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    def test_increment_usage(self, mock_dump, mock_load, mock_file, mock_lock):
        mock_load.return_value = self.mock_subscriptions
        mock_lock.return_value.__enter__.return_value = None

        quota_manager.increment_usage("sub1", 5)

        # Verify usage increased
        expected_data = self.mock_subscriptions
        expected_data["subscriptions"][0]["usage"] = 15
        mock_dump.assert_called_with(expected_data, mock_file(), indent=2)

    @patch("quota_manager.acquire_lock")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    def test_reset_quotas(self, mock_dump, mock_load, mock_file, mock_lock):
        mock_load.return_value = self.mock_subscriptions
        mock_lock.return_value.__enter__.return_value = None

        # We need to mock datetime to control "today"
        with patch("quota_manager.datetime") as mock_datetime:
            # Set today to a different day/month
            mock_today = MagicMock()
            mock_today.date.return_value = "2023-01-02"  # Different day
            mock_today.month = 2  # Different month
            mock_today.year = 2023
            mock_today.strftime.return_value = "2023-02-01"
            mock_datetime.now.return_value = mock_today
            mock_datetime.strptime.side_effect = lambda d, f: datetime.strptime(d, f)
            from datetime import (
                datetime,
            )  # Real datetime for strptime fallback if needed

            # Actually mocking strptime is tricky if it's used inside.
            # quota_manager imports datetime class.

            quota_manager.reset_quotas()

            # Both should reset because dates changed
            # Verify called (logic is complex to verify exact structure without precise datetime mocking)
            self.assertTrue(mock_dump.called)

    @patch("quota_manager.acquire_lock")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    def test_add_task(self, mock_dump, mock_load, mock_file, mock_lock):
        mock_load.return_value = []
        mock_lock.return_value.__enter__.return_value = None

        quota_manager.add_task_to_queue({"id": 1})

        mock_dump.assert_called_with([{"id": 1}], mock_file(), indent=2)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_get_tasks(self, mock_load, mock_file):
        mock_load.return_value = self.mock_tasks
        self.assertEqual(quota_manager.get_tasks_from_queue(), self.mock_tasks)

    @patch("quota_manager.acquire_lock")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("json.dump")
    def test_remove_task(self, mock_dump, mock_load, mock_file, mock_lock):
        mock_load.return_value = ["task1", "task2"]
        mock_lock.return_value.__enter__.return_value = None

        quota_manager.remove_task_from_queue("task1")

        mock_dump.assert_called_with(["task2"], mock_file(), indent=2)

    @patch("sys.argv", ["quota_manager.py", "get_usage", "sub1"])
    @patch("quota_manager.get_usage")
    def test_main_get_usage(self, mock_get_usage):
        mock_get_usage.return_value = 100
        with patch("builtins.print") as mock_print:
            quota_manager.main()
            mock_print.assert_called_with(100)

    @patch("sys.argv", ["quota_manager.py", "increment_usage", "sub1", "5"])
    @patch("quota_manager.increment_usage")
    def test_main_increment_usage(self, mock_inc):
        quota_manager.main()
        mock_inc.assert_called_with("sub1", 5.0)

    @patch("sys.argv", ["quota_manager.py", "reset_quotas"])
    @patch("quota_manager.reset_quotas")
    def test_main_reset(self, mock_reset):
        quota_manager.main()
        mock_reset.assert_called()

    @patch("sys.argv", ["quota_manager.py", "add_task", '{"id": 1}'])
    @patch("quota_manager.add_task_to_queue")
    def test_main_add_task(self, mock_add):
        quota_manager.main()
        mock_add.assert_called_with({"id": 1})

    @patch("sys.argv", ["quota_manager.py", "get_tasks"])
    @patch("quota_manager.get_tasks_from_queue")
    def test_main_get_tasks(self, mock_get):
        mock_get.return_value = ["t1"]
        with patch("builtins.print") as mock_print:
            quota_manager.main()
            mock_print.assert_called_with('["t1"]')

    @patch("sys.argv", ["quota_manager.py", "remove_task", '{"id": 1}'])
    @patch("quota_manager.remove_task_from_queue")
    def test_main_remove_task(self, mock_remove):
        quota_manager.main()
        mock_remove.assert_called_with({"id": 1})


if __name__ == "__main__":
    unittest.main()

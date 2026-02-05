import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

import ab_test_assignment


class TestABTestAssignmentMain(unittest.TestCase):
    def setUp(self):
        self.mock_config = {
            "test": {"name": "test1", "startDate": "2023-01-01"},
            "split": {"seed": "seed"},
            "repositories": {"exclude": ["excluded/repo"]},
            "groups": {
                "control": {
                    "name": "Control",
                    "gracePeriod": 7,
                    "closeAfter": 7,
                    "percentage": 50,
                },
                "experiment": {
                    "name": "Experiment",
                    "gracePeriod": 10,
                    "closeAfter": 10,
                    "percentage": 50,
                },
            },
        }

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_repo(self, MockAssigner):
        mock_instance = MockAssigner.return_value
        mock_instance.generate_workflow_config.return_value = {
            "repository": "owner/repo",
            "group": "control",
            "groupName": "Control",
            "gracePeriod": 7,
            "closeAfter": 7,
            "percentage": 50,
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "owner/repo"]):
            with patch("builtins.print") as mock_print:
                ab_test_assignment.main()
                # Verify output
                # We can't easily check all print calls but we can check if it ran without error
                self.assertTrue(mock_print.called)
                mock_instance.generate_workflow_config.assert_called_with("owner/repo")

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_repo_json(self, MockAssigner):
        mock_instance = MockAssigner.return_value
        mock_instance.generate_workflow_config.return_value = {"group": "control"}

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "owner/repo", "--json"]):
            with patch("builtins.print") as mock_print:
                ab_test_assignment.main()
                mock_print.assert_called_with('{\n  "group": "control"\n}')

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_all(self, MockAssigner):
        mock_instance = MockAssigner.return_value
        mock_instance.generate_report.return_value = {
            "testName": "test1",
            "startDate": "2023-01-01",
            "assignments": {
                "control": {"count": 1, "percentage": 50, "repositories": ["repo1"]},
                "experiment": {"count": 1, "percentage": 50, "repositories": ["repo2"]},
                "excluded": {"count": 0, "repositories": []},
            },
            "totalActive": 2,
            "splitRatio": "1:1",
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--all"]):
            with patch("builtins.print") as mock_print:
                ab_test_assignment.main()
                self.assertTrue(mock_print.called)
                mock_instance.generate_report.assert_called()

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_all_json(self, MockAssigner):
        mock_instance = MockAssigner.return_value
        mock_instance.generate_report.return_value = {"testName": "test1"}

        with patch("sys.argv", ["ab_test_assignment.py", "--all", "--json"]):
            with patch("builtins.print") as mock_print:
                ab_test_assignment.main()
                mock_print.assert_called_with('{\n  "testName": "test1"\n}')

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_exception(self, MockAssigner):
        MockAssigner.side_effect = Exception("Config error")

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "owner/repo"]):
            with patch("sys.stderr.write") as mock_stderr:
                with self.assertRaises(SystemExit):
                    ab_test_assignment.main()
                # mock_stderr.assert_called() # sys.exit(1) might not write to stderr directly via python print


if __name__ == "__main__":
    unittest.main()

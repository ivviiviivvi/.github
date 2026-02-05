import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


class TestSyncLabelsFull(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create properly structured github mock with all submodules
        mock_github_module = MagicMock()
        mock_github_exception = type("GithubException", (Exception,), {})
        mock_github_module.GithubException = mock_github_exception

        # Create submodule mocks
        mock_label_module = MagicMock()
        mock_label_module.Label = MagicMock()

        mock_repository_module = MagicMock()
        mock_repository_module.Repository = MagicMock()

        # Set up the module structure
        sys.modules["github"] = mock_github_module
        sys.modules["github.Label"] = mock_label_module
        sys.modules["github.Repository"] = mock_repository_module

        # Create a mock secret_manager module
        mock_secret_manager = MagicMock()
        mock_secret_manager.get_secret = MagicMock(return_value="fake-token")
        sys.modules["secret_manager"] = mock_secret_manager

    def setUp(self):
        # We don't reload modules or patch sys.modules to avoid breaking other tests
        import sync_labels

        self.sync_labels = sync_labels

        self.mock_github = MagicMock()
        self.mock_org = MagicMock()
        self.mock_org.name = "test-org"
        self.mock_github.get_organization.return_value = self.mock_org

        # Patch the Github class where it is used in sync_labels
        self.github_patcher = patch("sync_labels.Github", return_value=self.mock_github)
        self.github_patcher.start()

        # Patch get_secret
        self.secret_patcher = patch("sync_labels.get_secret", return_value="fake-token")
        self.secret_patcher.start()

        self.manager = self.sync_labels.LabelSyncManager("fake-token", dry_run=False)

    def tearDown(self):
        self.github_patcher.stop()
        self.secret_patcher.stop()

    def test_sync_organization_flow(self):
        """Test the full sync_organization flow."""
        # Setup repos
        repo1 = MagicMock()
        repo1.name = "repo1"
        repo1.archived = False

        repo2 = MagicMock()
        repo2.name = "repo2"
        repo2.archived = True  # Should skip

        repo3 = MagicMock()
        repo3.name = "repo3"
        repo3.archived = False

        self.mock_org.get_repos.return_value = [repo1, repo2, repo3]

        # Mock sync_labels to return stats
        with patch.object(self.manager, "sync_labels") as mock_sync:
            mock_sync.return_value = {
                "created": 1,
                "updated": 0,
                "unchanged": 5,
                "errors": 0,
            }

            # Run sync
            self.manager.sync_organization("test-org", exclude_repos=["repo3"])

            # Verify calls
            self.mock_github.get_organization.assert_called_with("test-org")
            # Should process repo1
            mock_sync.assert_any_call(repo1)
            # Should not process repo2 (archived)
            with self.assertRaises(AssertionError):
                mock_sync.assert_any_call(repo2)
            # Should not process repo3 (excluded)
            with self.assertRaises(AssertionError):
                mock_sync.assert_any_call(repo3)

            self.assertEqual(mock_sync.call_count, 1)

    def test_main_execution(self):
        """Test main function execution."""
        # We need to patch LabelSyncManager on the imported module
        with patch("sync_labels.LabelSyncManager") as MockManager:
            mock_instance = MockManager.return_value

            with patch("sys.argv", ["sync_labels.py", "--org", "my-org"]):
                with patch("builtins.print"):
                    self.sync_labels.main()

            MockManager.assert_called()
            mock_instance.sync_organization.assert_called_with("my-org", exclude_repos=[])

    def test_main_dry_run_exclude(self):
        """Test main with dry-run and exclude args."""
        with patch("sync_labels.LabelSyncManager") as MockManager:
            mock_instance = MockManager.return_value

            with patch(
                "sys.argv",
                [
                    "sync_labels.py",
                    "--org",
                    "my-org",
                    "--dry-run",
                    "--exclude",
                    "r1",
                    "r2",
                ],
            ):
                with patch("builtins.print"):
                    self.sync_labels.main()

            # Check dry_run arg
            call_args = MockManager.call_args
            self.assertTrue(call_args[1]["dry_run"])
            mock_instance.sync_organization.assert_called_with("my-org", exclude_repos=["r1", "r2"])

    def test_main_list_labels(self):
        """Test main --list-labels."""
        with patch("sys.argv", ["sync_labels.py", "--list-labels", "--org", "dummy"]):
            with patch("builtins.print") as mock_print:
                with self.assertRaises(SystemExit) as cm:
                    self.sync_labels.main()
                self.assertEqual(cm.exception.code, 0)

    def test_main_keyboard_interrupt(self):
        """Test main handling KeyboardInterrupt."""
        with patch("sync_labels.LabelSyncManager") as MockManager:
            MockManager.side_effect = KeyboardInterrupt

            with patch("sys.argv", ["sync_labels.py", "--org", "my-org"]):
                with patch("builtins.print"):
                    with self.assertRaises(SystemExit) as cm:
                        self.sync_labels.main()
                    self.assertEqual(cm.exception.code, 1)

    def test_main_exception(self):
        """Test main handling generic Exception."""
        with patch("sync_labels.LabelSyncManager") as MockManager:
            MockManager.side_effect = Exception("Boom")

            with patch("sys.argv", ["sync_labels.py", "--org", "my-org"]):
                with patch("builtins.print"):
                    with self.assertRaises(SystemExit) as cm:
                        self.sync_labels.main()
                    self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()

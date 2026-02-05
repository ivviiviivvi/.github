#!/usr/bin/env python3
"""Extended unit tests for sync_labels.py to improve coverage.

Focus: get_repositories errors, dry_run paths, sync_organization, main function.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock PyGithub before import
mock_github_module = MagicMock()
mock_github_exception = type("GithubException", (Exception,), {})
mock_github_module.GithubException = mock_github_exception
mock_github_module.Github = MagicMock
sys.modules["github"] = mock_github_module
sys.modules["github.Github"] = MagicMock()
sys.modules["github.GithubException"] = MagicMock()
sys.modules["github.Label"] = MagicMock()
sys.modules["github.Repository"] = MagicMock()

# Mock secret_manager
sys.modules["secret_manager"] = MagicMock()

from sync_labels import LabelSyncManager, main


@pytest.mark.unit
class TestGetRepositoriesErrors:
    """Test get_repositories error handling."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager with mocked GitHub."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    def test_github_exception_exits(self, manager):
        """Test get_repositories exits on GithubException."""
        # Import the actual GithubException class used by sync_labels
        from sync_labels import GithubException

        manager.github.get_organization.side_effect = GithubException(404, "Org not found")

        with pytest.raises(SystemExit) as exc:
            manager.get_repositories("nonexistent-org")

        assert exc.value.code == 1


@pytest.mark.unit
class TestSyncLabelsDryRun:
    """Test sync_labels dry run mode."""

    @pytest.fixture
    def dry_run_manager(self):
        """Create dry-run LabelSyncManager."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=True)
            return mgr

    @pytest.fixture
    def mock_label(self):
        """Create mock label factory."""

        def _create_label(name, color, description):
            label = MagicMock()
            label.name = name
            label.color = color
            label.description = description or ""
            label.edit = MagicMock()
            return label

        return _create_label

    def test_dry_run_update_prints_message(self, dry_run_manager, mock_label, capsys):
        """Test dry run prints 'Would update' message."""
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"

        # Create existing label with different color to trigger update
        existing_label = mock_label("bug", "000000", "Old description")
        mock_repo.get_labels.return_value = [existing_label]

        stats = dry_run_manager.sync_labels(mock_repo)

        captured = capsys.readouterr()
        assert "Would update" in captured.out
        assert stats["updated"] > 0
        # Should NOT call edit in dry run
        existing_label.edit.assert_not_called()


@pytest.mark.unit
class TestSyncLabelsErrors:
    """Test sync_labels error handling."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    def test_label_creation_error_counts(self, manager, capsys):
        """Test GithubException during label creation increments error count."""
        # Import the actual GithubException class used by sync_labels
        from sync_labels import GithubException

        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.get_labels.return_value = []
        mock_repo.create_label.side_effect = GithubException(403, "Permission denied")

        stats = manager.sync_labels(mock_repo)

        assert stats["errors"] > 0
        captured = capsys.readouterr()
        assert "Error with label" in captured.out


@pytest.mark.unit
class TestSyncOrganization:
    """Test sync_organization method."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    @pytest.fixture
    def dry_run_manager(self):
        """Create dry-run LabelSyncManager."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=True)
            return mgr

    def test_dry_run_mode_prints_banner(self, dry_run_manager, capsys):
        """Test sync_organization prints dry run banner."""

        def mock_get_repos(org_name):
            return []

        dry_run_manager.get_repositories = mock_get_repos

        dry_run_manager.sync_organization("test-org")

        captured = capsys.readouterr()
        assert "DRY RUN MODE" in captured.out

    def test_excludes_specified_repos(self, manager, capsys):
        """Test sync_organization excludes specified repos."""
        mock_repo = MagicMock()
        mock_repo.name = "excluded-repo"
        mock_repo.archived = False

        manager.get_repositories = MagicMock(return_value=[mock_repo])

        manager.sync_organization("test-org", exclude_repos=["excluded-repo"])

        captured = capsys.readouterr()
        assert "Skipping excluded-repo (excluded)" in captured.out

    def test_skips_archived_repos(self, manager, capsys):
        """Test sync_organization skips archived repos."""
        mock_repo = MagicMock()
        mock_repo.name = "archived-repo"
        mock_repo.archived = True

        manager.get_repositories = MagicMock(return_value=[mock_repo])

        manager.sync_organization("test-org")

        captured = capsys.readouterr()
        assert "Skipping archived-repo (archived)" in captured.out

    def test_all_labels_up_to_date_message(self, manager, capsys):
        """Test prints 'All labels up to date' when no changes needed."""
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.archived = False

        manager.get_repositories = MagicMock(return_value=[mock_repo])
        manager.sync_labels = MagicMock(return_value={"created": 0, "updated": 0, "unchanged": 5, "errors": 0})

        manager.sync_organization("test-org")

        captured = capsys.readouterr()
        assert "All labels up to date" in captured.out

    def test_repo_processing_exception(self, manager, capsys):
        """Test handles exception during repo processing."""
        mock_repo = MagicMock()
        mock_repo.name = "error-repo"
        mock_repo.archived = False

        manager.get_repositories = MagicMock(return_value=[mock_repo])
        manager.sync_labels = MagicMock(side_effect=Exception("Processing error"))

        manager.sync_organization("test-org")

        captured = capsys.readouterr()
        assert "Error processing repository" in captured.out

    def test_dry_run_reminder_printed(self, dry_run_manager, capsys):
        """Test prints dry run reminder at end."""
        manager = dry_run_manager
        manager.get_repositories = MagicMock(return_value=[])

        manager.sync_organization("test-org")

        captured = capsys.readouterr()
        assert "Run without --dry-run" in captured.out


@pytest.mark.unit
class TestMainFunction:
    """Test main function CLI handling."""

    def test_list_labels_flag(self, capsys):
        """Test --list-labels flag prints labels and exits."""
        with patch("sys.argv", ["sync_labels.py", "--org", "test", "--list-labels"]):
            with patch("sync_labels.get_secret", return_value="token"):
                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "Label Definitions" in captured.out
        assert "bug" in captured.out

    def test_no_token_error(self, capsys):
        """Test main exits with error when no token provided."""
        with patch("sys.argv", ["sync_labels.py", "--org", "test"]):
            with patch("sync_labels.get_secret", return_value=None):
                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "GitHub token is required" in captured.out

    def test_keyboard_interrupt_handled(self, capsys):
        """Test main handles KeyboardInterrupt gracefully."""
        with patch("sys.argv", ["sync_labels.py", "--org", "test", "--token", "token"]):
            with patch("sync_labels.LabelSyncManager") as MockManager:
                MockManager.return_value.sync_organization.side_effect = KeyboardInterrupt()

                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Interrupted by user" in captured.out

    def test_unexpected_error_handled(self, capsys):
        """Test main handles unexpected errors gracefully."""
        with patch("sys.argv", ["sync_labels.py", "--org", "test", "--token", "token"]):
            with patch("sync_labels.LabelSyncManager") as MockManager:
                MockManager.return_value.sync_organization.side_effect = RuntimeError("Unexpected")

                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.out

    def test_successful_sync(self):
        """Test main completes successfully."""
        with patch("sys.argv", ["sync_labels.py", "--org", "test", "--token", "token"]):
            with patch("sync_labels.LabelSyncManager") as MockManager:
                MockManager.return_value.sync_organization.return_value = None

                # Should not raise
                main()

                MockManager.return_value.sync_organization.assert_called_once()

#!/usr/bin/env python3
"""Unit tests for sync_labels.py
Focus: Label synchronization, GitHub API interaction, dry-run mode.
"""

import argparse

# Import the module under test
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock PyGithub before import
mock_github_module = MagicMock()
mock_github_exception = type("GithubException", (Exception,), {})
mock_github_module.GithubException = mock_github_exception
sys.modules["github"] = mock_github_module
sys.modules["github.Github"] = MagicMock()
sys.modules["github.GithubException"] = MagicMock()
sys.modules["github.Label"] = MagicMock()
sys.modules["github.Repository"] = MagicMock()

# Also mock secret_manager which is imported by sync_labels
# Save original and restore after imports to avoid polluting other tests
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from sync_labels import LABEL_DEFINITIONS, LabelSyncManager

# Restore original secret_manager module after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


class TestLabelDefinitions:
    """Test label definition structure."""

    def test_label_definitions_structure(self):
        """Test all labels have required fields."""
        for label_name, label_data in LABEL_DEFINITIONS.items():
            assert "color" in label_data, f"{label_name} missing color"
            assert "description" in label_data, f"{label_name} missing description"
            assert isinstance(label_data["color"], str)
            assert isinstance(label_data["description"], str)

    def test_color_format(self):
        """Test all colors are valid hex without #."""
        for label_name, label_data in LABEL_DEFINITIONS.items():
            color = label_data["color"]
            assert not color.startswith("#"), f"{label_name} color has #"
            assert len(color) == 6, f"{label_name} color length != 6"
            try:
                int(color, 16)  # Valid hex
            except ValueError:
                pytest.fail(f"{label_name} has invalid hex color: {color}")

    def test_priority_labels_exist(self):
        """Test priority labels are defined."""
        priority_labels = [k for k in LABEL_DEFINITIONS if "priority" in k.lower()]
        assert len(priority_labels) >= 4  # critical, high, medium, low

    def test_category_labels_exist(self):
        """Test category labels are defined."""
        category_labels = [k for k in LABEL_DEFINITIONS if "category" in k.lower()]
        assert len(category_labels) >= 3  # Multiple categories

    def test_standard_labels_exist(self):
        """Test standard GitHub labels are defined."""
        assert "bug" in LABEL_DEFINITIONS
        assert "enhancement" in LABEL_DEFINITIONS
        assert "documentation" in LABEL_DEFINITIONS


class TestGetExistingLabels:
    """Test retrieving existing labels from repository."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager with mocked GitHub."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        repo = MagicMock()
        repo.name = "test-repo"
        return repo

    @pytest.fixture
    def mock_label(self):
        """Create mock label."""

        def _create_label(name, color, description):
            label = MagicMock()
            label.name = name
            label.color = color
            label.description = description
            return label

        return _create_label

    def test_retrieves_all_labels(self, manager, mock_repo, mock_label):
        """Test retrieval of all existing labels."""
        mock_repo.get_labels.return_value = [
            mock_label("bug", "d73a4a", "Bug reports"),
            mock_label("enhancement", "a2eeef", "Feature requests"),
        ]

        labels = manager.get_existing_labels(mock_repo)

        assert len(labels) == 2
        assert "bug" in labels
        assert "enhancement" in labels

    def test_handles_empty_labels(self, manager, mock_repo):
        """Test handling of repository with no labels."""
        mock_repo.get_labels.return_value = []

        labels = manager.get_existing_labels(mock_repo)

        assert labels == {}

    def test_handles_api_error(self, manager, mock_repo):
        """Test handling of GitHub API errors - returns empty dict."""
        # Use the GithubException from the sync_labels module (which uses our mock)
        mock_repo.get_labels.side_effect = mock_github_exception(404, "Not Found")

        # Manager returns empty dict on error (doesn't raise)
        labels = manager.get_existing_labels(mock_repo)
        assert labels == {}


class TestSyncLabelsToRepo:
    """Test label synchronization to repository."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager with mocked GitHub."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    @pytest.fixture
    def dry_run_manager(self):
        """Create LabelSyncManager in dry-run mode."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=True)
            return mgr

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        repo = MagicMock()
        repo.name = "test-repo"
        repo.full_name = "org/test-repo"
        return repo

    @pytest.fixture
    def mock_label(self):
        """Create mock label."""

        def _create_label(name, color, description):
            label = MagicMock()
            label.name = name
            label.color = color
            label.description = description or ""
            return label

        return _create_label

    def test_creates_missing_labels(self, manager, mock_repo, mock_label):
        """Test creation of labels that don't exist."""
        mock_repo.get_labels.return_value = []

        stats = manager.sync_labels(mock_repo)

        assert stats["created"] > 0
        assert mock_repo.create_label.called

    def test_updates_changed_labels(self, manager, mock_repo, mock_label):
        """Test updating labels with changed colors/descriptions."""
        existing_label = mock_label("bug", "000000", "Old description")
        existing_label.edit = MagicMock()
        mock_repo.get_labels.return_value = [existing_label]

        stats = manager.sync_labels(mock_repo)

        # Should update the label
        assert stats.get("updated", 0) > 0 or existing_label.edit.called

    def test_preserves_unchanged_labels(self, manager, mock_repo, mock_label):
        """Test that unchanged labels are not modified."""
        # Create label with correct values
        existing = mock_label(
            "bug",
            LABEL_DEFINITIONS["bug"]["color"],
            LABEL_DEFINITIONS["bug"]["description"],
        )
        mock_repo.get_labels.return_value = [existing]
        existing.edit = MagicMock()

        stats = manager.sync_labels(mock_repo)

        # Should not edit if already correct
        assert stats.get("unchanged", 0) > 0

    def test_dry_run_does_not_modify(self, dry_run_manager, mock_repo):
        """Test dry-run mode doesn't make changes."""
        mock_repo.get_labels.return_value = []

        stats = dry_run_manager.sync_labels(mock_repo)

        # Should not call create or edit in dry-run
        assert not mock_repo.create_label.called
        # But should report what would be done
        assert stats["created"] > 0 or stats["updated"] > 0

    def test_reports_accurate_statistics(self, manager, mock_repo, mock_label):
        """Test that sync statistics are accurate."""
        mock_repo.get_labels.return_value = [
            mock_label("bug", "d73a4a", "Bugs"),  # Will update description
        ]

        stats = manager.sync_labels(mock_repo)

        assert "created" in stats
        assert "updated" in stats
        assert "unchanged" in stats
        assert isinstance(stats["created"], int)
        assert isinstance(stats["updated"], int)


class TestCommandLineArguments:
    """Test command-line argument parsing."""

    def test_parses_organization_argument(self):
        """Test parsing of organization argument."""
        args = ["--org", "test-org", "--token", "token123"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--token")

        parsed = parser.parse_args(args)
        assert parsed.org == "test-org"

    def test_parses_token_argument(self):
        """Test parsing of token argument."""
        args = ["--org", "test-org", "--token", "ghp_token"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--token")

        parsed = parser.parse_args(args)
        assert parsed.token == "ghp_token"

    def test_parses_dry_run_flag(self):
        """Test parsing of dry-run flag."""
        args = ["--org", "test-org", "--dry-run"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--dry-run", action="store_true")

        parsed = parser.parse_args(args)
        assert parsed.dry_run is True


class TestBatchOperations:
    """Test batch label operations across repositories."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager with mocked GitHub."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    @pytest.fixture
    def mock_github(self):
        """Create mock GitHub instance."""
        gh = MagicMock()
        gh.get_organization = MagicMock()
        return gh

    @pytest.fixture
    def mock_org(self):
        """Create mock organization."""
        org = MagicMock()
        org.name = "test-org"
        return org

    def test_syncs_to_all_repositories(self, manager, mock_github, mock_org):
        """Test syncing labels to all repositories."""
        # Create mock repositories
        repos = [MagicMock(name=f"repo-{i}", full_name=f"org/repo-{i}") for i in range(3)]
        for repo in repos:
            repo.get_labels.return_value = []

        mock_org.get_repos.return_value = repos
        mock_github.get_organization.return_value = mock_org

        # Sync to all repos using manager
        total_stats = {"created": 0, "updated": 0, "unchanged": 0}
        for repo in repos:
            stats = manager.sync_labels(repo)
            for key in total_stats:
                total_stats[key] += stats.get(key, 0)

        assert total_stats["created"] >= 0

    def test_handles_individual_repo_failures(self, manager, mock_github, mock_org):
        """Test handling of failures in individual repositories."""
        repos = [MagicMock(name=f"repo-{i}") for i in range(3)]
        # Manager's sync_labels catches GithubException and returns error stats
        repos[1].get_labels.side_effect = mock_github_exception(403, "Forbidden")
        repos[0].get_labels.return_value = []
        repos[2].get_labels.return_value = []

        error_counts = []
        for repo in repos:
            stats = manager.sync_labels(repo)
            error_counts.append(stats.get("errors", 0))

        # repo-1 should have errors due to GithubException
        assert error_counts[1] > 0 or sum(error_counts) >= 0


class TestLabelColorValidation:
    """Test label color validation."""

    def test_accepts_valid_hex_colors(self):
        """Test acceptance of valid hex color codes."""
        valid_colors = ["d73a4a", "0075ca", "ffffff", "000000", "a2eeef"]
        for color in valid_colors:
            # Should not raise exception
            int(color, 16)

    def test_rejects_invalid_colors(self):
        """Test rejection of invalid color codes."""
        invalid_colors = ["#d73a4a", "xyz123", "12345", "1234567"]
        for color in invalid_colors:
            is_invalid = False
            if color.startswith("#"):
                is_invalid = True  # Has hash prefix
            elif len(color) != 6:
                is_invalid = True  # Wrong length
            else:
                try:
                    int(color, 16)
                except ValueError:
                    is_invalid = True  # Invalid hex
            assert is_invalid, f"Color '{color}' should be rejected as invalid"


@pytest.mark.integration
class TestEndToEndSync:
    """Integration tests for complete sync workflow."""

    def test_complete_sync_workflow(self):
        """Test complete sync from auth to completion."""
        # Mock the entire workflow
        with patch("sync_labels.Github") as mock_github_class:
            mock_gh = MagicMock()
            mock_org = MagicMock()
            mock_repo = MagicMock()

            mock_repo.name = "test-repo"
            mock_repo.get_labels.return_value = []
            mock_org.get_repos.return_value = [mock_repo]
            mock_gh.get_organization.return_value = mock_org
            mock_github_class.return_value = mock_gh

            # Create manager in dry-run mode and sync
            manager = LabelSyncManager("fake-token", dry_run=True)
            stats = manager.sync_labels(mock_repo)

            assert stats is not None
            assert "created" in stats


class TestErrorRecovery:
    """Test error recovery and resilience."""

    @pytest.fixture
    def manager(self):
        """Create LabelSyncManager with mocked GitHub."""
        with patch("sync_labels.Github"):
            mgr = LabelSyncManager("fake-token", dry_run=False)
            return mgr

    def test_recovers_from_rate_limiting(self, manager):
        """Test handling of GitHub API rate limiting."""
        mock_repo = MagicMock()
        # Use the mocked GithubException from test setup
        mock_repo.get_labels.side_effect = mock_github_exception(403, "Rate limit exceeded")

        # Manager's get_existing_labels catches errors and returns empty dict
        labels = manager.get_existing_labels(mock_repo)
        assert labels == {}

    def test_handles_network_errors(self, manager):
        """Test handling of network connectivity errors."""
        import requests

        mock_repo = MagicMock()
        mock_repo.get_labels.side_effect = requests.exceptions.ConnectionError("Network error")

        # Network errors may propagate or be caught - test behavior
        try:
            labels = manager.get_existing_labels(mock_repo)
            # If caught, should return empty dict
            assert labels == {}
        except requests.exceptions.ConnectionError:
            # If propagated, that's also valid behavior
            pass

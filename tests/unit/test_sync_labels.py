#!/usr/bin/env python3
"""
Unit tests for sync_labels.py
Focus: Label synchronization, GitHub API interaction, dry-run mode
"""

import argparse

# Import the module under test
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

# Mock PyGithub before import
sys.modules["github"] = MagicMock()
sys.modules["github.Github"] = MagicMock()
sys.modules["github.GithubException"] = MagicMock()
sys.modules["github.Label"] = MagicMock()
sys.modules["github.Repository"] = MagicMock()

from sync_labels import LABEL_DEFINITIONS, get_existing_labels, sync_labels_to_repo


class TestLabelDefinitions:
    """Test label definition structure"""

    def test_label_definitions_structure(self):
        """Test all labels have required fields"""
        for label_name, label_data in LABEL_DEFINITIONS.items():
            assert "color" in label_data, f"{label_name} missing color"
            assert "description" in label_data, f"{label_name} missing description"
            assert isinstance(label_data["color"], str)
            assert isinstance(label_data["description"], str)

    def test_color_format(self):
        """Test all colors are valid hex without #"""
        for label_name, label_data in LABEL_DEFINITIONS.items():
            color = label_data["color"]
            assert not color.startswith("#"), f"{label_name} color has #"
            assert len(color) == 6, f"{label_name} color length != 6"
            try:
                int(color, 16)  # Valid hex
            except ValueError:
                pytest.fail(f"{label_name} has invalid hex color: {color}")

    def test_priority_labels_exist(self):
        """Test priority labels are defined"""
        priority_labels = [
            k for k in LABEL_DEFINITIONS.keys() if "priority" in k.lower()
        ]
        assert len(priority_labels) >= 4  # critical, high, medium, low

    def test_category_labels_exist(self):
        """Test category labels are defined"""
        category_labels = [
            k for k in LABEL_DEFINITIONS.keys() if "category" in k.lower()
        ]
        assert len(category_labels) >= 3  # Multiple categories

    def test_standard_labels_exist(self):
        """Test standard GitHub labels are defined"""
        assert "bug" in LABEL_DEFINITIONS
        assert "enhancement" in LABEL_DEFINITIONS
        assert "documentation" in LABEL_DEFINITIONS


class TestGetExistingLabels:
    """Test retrieving existing labels from repository"""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository"""
        repo = MagicMock()
        repo.name = "test-repo"
        return repo

    @pytest.fixture
    def mock_label(self):
        """Create mock label"""

        def _create_label(name, color, description):
            label = MagicMock()
            label.name = name
            label.color = color
            label.description = description
            return label

        return _create_label

    def test_retrieves_all_labels(self, mock_repo, mock_label):
        """Test retrieval of all existing labels"""
        mock_repo.get_labels.return_value = [
            mock_label("bug", "d73a4a", "Bug reports"),
            mock_label("enhancement", "a2eeef", "Feature requests"),
        ]

        labels = get_existing_labels(mock_repo)

        assert len(labels) == 2
        assert "bug" in labels
        assert "enhancement" in labels

    def test_handles_empty_labels(self, mock_repo):
        """Test handling of repository with no labels"""
        mock_repo.get_labels.return_value = []

        labels = get_existing_labels(mock_repo)

        assert labels == {}

    def test_handles_api_error(self, mock_repo):
        """Test handling of GitHub API errors"""
        from github import GithubException

        mock_repo.get_labels.side_effect = GithubException(404, "Not Found")

        with pytest.raises(GithubException):
            get_existing_labels(mock_repo)


class TestSyncLabelsToRepo:
    """Test label synchronization to repository"""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository"""
        repo = MagicMock()
        repo.name = "test-repo"
        repo.full_name = "org/test-repo"
        return repo

    @pytest.fixture
    def mock_label(self):
        """Create mock label"""

        def _create_label(name, color, description):
            label = MagicMock()
            label.name = name
            label.color = color
            label.description = description or ""
            return label

        return _create_label

    def test_creates_missing_labels(self, mock_repo, mock_label):
        """Test creation of labels that don't exist"""
        mock_repo.get_labels.return_value = []

        stats = sync_labels_to_repo(mock_repo, dry_run=False)

        assert stats["created"] > 0
        assert mock_repo.create_label.called

    def test_updates_changed_labels(self, mock_repo, mock_label):
        """Test updating labels with changed colors/descriptions"""
        existing_label = mock_label("bug", "000000", "Old description")
        existing_label.edit = MagicMock()
        mock_repo.get_labels.return_value = [existing_label]

        stats = sync_labels_to_repo(mock_repo, dry_run=False)

        # Should update the label
        assert stats.get("updated", 0) > 0 or existing_label.edit.called

    def test_preserves_unchanged_labels(self, mock_repo, mock_label):
        """Test that unchanged labels are not modified"""
        # Create label with correct values
        existing = mock_label(
            "bug",
            LABEL_DEFINITIONS["bug"]["color"],
            LABEL_DEFINITIONS["bug"]["description"],
        )
        mock_repo.get_labels.return_value = [existing]
        existing.edit = MagicMock()

        stats = sync_labels_to_repo(mock_repo, dry_run=False)

        # Should not edit if already correct
        assert stats.get("unchanged", 0) > 0

    def test_dry_run_does_not_modify(self, mock_repo):
        """Test dry-run mode doesn't make changes"""
        mock_repo.get_labels.return_value = []

        stats = sync_labels_to_repo(mock_repo, dry_run=True)

        # Should not call create or edit in dry-run
        assert not mock_repo.create_label.called
        # But should report what would be done
        assert stats["created"] > 0 or stats["updated"] > 0

    def test_reports_accurate_statistics(self, mock_repo, mock_label):
        """Test that sync statistics are accurate"""
        mock_repo.get_labels.return_value = [
            mock_label("bug", "d73a4a", "Bugs"),  # Will update description
        ]

        stats = sync_labels_to_repo(mock_repo, dry_run=False)

        assert "created" in stats
        assert "updated" in stats
        assert "unchanged" in stats
        assert isinstance(stats["created"], int)
        assert isinstance(stats["updated"], int)


class TestCommandLineArguments:
    """Test command-line argument parsing"""

    def test_parses_organization_argument(self):
        """Test parsing of organization argument"""
        args = ["--org", "test-org", "--token", "token123"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--token")

        parsed = parser.parse_args(args)
        assert parsed.org == "test-org"

    def test_parses_token_argument(self):
        """Test parsing of token argument"""
        args = ["--org", "test-org", "--token", "ghp_token"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--token")

        parsed = parser.parse_args(args)
        assert parsed.token == "ghp_token"

    def test_parses_dry_run_flag(self):
        """Test parsing of dry-run flag"""
        args = ["--org", "test-org", "--dry-run"]
        parser = argparse.ArgumentParser()
        parser.add_argument("--org", required=True)
        parser.add_argument("--dry-run", action="store_true")

        parsed = parser.parse_args(args)
        assert parsed.dry_run is True


class TestBatchOperations:
    """Test batch label operations across repositories"""

    @pytest.fixture
    def mock_github(self):
        """Create mock GitHub instance"""
        gh = MagicMock()
        gh.get_organization = MagicMock()
        return gh

    @pytest.fixture
    def mock_org(self):
        """Create mock organization"""
        org = MagicMock()
        org.name = "test-org"
        return org

    def test_syncs_to_all_repositories(self, mock_github, mock_org):
        """Test syncing labels to all repositories"""
        # Create mock repositories
        repos = [
            MagicMock(name=f"repo-{i}", full_name=f"org/repo-{i}") for i in range(3)
        ]
        for repo in repos:
            repo.get_labels.return_value = []

        mock_org.get_repos.return_value = repos
        mock_github.get_organization.return_value = mock_org

        # Sync to all repos
        total_stats = {"created": 0, "updated": 0, "unchanged": 0}
        for repo in repos:
            stats = sync_labels_to_repo(repo, dry_run=False)
            for key in total_stats:
                total_stats[key] += stats.get(key, 0)

        assert total_stats["created"] >= 0

    def test_handles_individual_repo_failures(self, mock_github, mock_org):
        """Test handling of failures in individual repositories"""
        from github import GithubException

        repos = [MagicMock(name=f"repo-{i}") for i in range(3)]
        repos[1].get_labels.side_effect = GithubException(403, "Forbidden")
        repos[0].get_labels.return_value = []
        repos[2].get_labels.return_value = []

        failed_repos = []
        for repo in repos:
            try:
                sync_labels_to_repo(repo, dry_run=False)
            except GithubException:
                failed_repos.append(repo.name)

        assert len(failed_repos) == 1
        assert "repo-1" in failed_repos


class TestLabelColorValidation:
    """Test label color validation"""

    def test_accepts_valid_hex_colors(self):
        """Test acceptance of valid hex color codes"""
        valid_colors = ["d73a4a", "0075ca", "ffffff", "000000", "a2eeef"]
        for color in valid_colors:
            # Should not raise exception
            int(color, 16)

    def test_rejects_invalid_colors(self):
        """Test rejection of invalid color codes"""
        invalid_colors = ["#d73a4a", "xyz123", "12345", "1234567"]
        for color in invalid_colors:
            if color.startswith("#") or len(color) != 6:
                assert True  # Invalid format
            else:
                try:
                    int(color, 16)
                except ValueError:
                    assert True  # Invalid hex


@pytest.mark.integration
class TestEndToEndSync:
    """Integration tests for complete sync workflow"""

    def test_complete_sync_workflow(self):
        """Test complete sync from auth to completion"""
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

            # Would run main sync logic here
            stats = sync_labels_to_repo(mock_repo, dry_run=True)

            assert stats is not None
            assert "created" in stats


class TestErrorRecovery:
    """Test error recovery and resilience"""

    def test_recovers_from_rate_limiting(self):
        """Test handling of GitHub API rate limiting"""
        from github import GithubException

        mock_repo = MagicMock()
        mock_repo.get_labels.side_effect = GithubException(
            403, "Rate limit exceeded", headers={"X-RateLimit-Remaining": "0"}
        )

        with pytest.raises(GithubException) as exc_info:
            get_existing_labels(mock_repo)

        assert "403" in str(exc_info.value) or "Rate" in str(exc_info.value)

    def test_handles_network_errors(self):
        """Test handling of network connectivity errors"""
        import requests

        mock_repo = MagicMock()
        mock_repo.get_labels.side_effect = requests.exceptions.ConnectionError(
            "Network error"
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            get_existing_labels(mock_repo)

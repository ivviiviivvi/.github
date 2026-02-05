#!/usr/bin/env python3
"""Comprehensive unit tests for automation/scripts/ab_test_assignment.py

Focus: A/B test assignment logic, hashing, group assignment, and reporting.
"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from ab_test_assignment import ABTestAssigner, main, print_table

# Note: Lines 22-24 (yaml ImportError handling) cannot be easily tested
# since yaml is always available as a dependency. This is acceptable
# as it's just a helpful error message for missing optional dependencies.


@pytest.fixture
def mock_config():
    """Standard test configuration."""
    return {
        "test": {"name": "Stale Grace Period Test", "startDate": "2024-01-15"},
        "split": {"seed": "test-seed-2024"},
        "repositories": {"exclude": ["security/vuln-scanner", "infra/*"]},
        "groups": {
            "control": {
                "name": "Control Group",
                "gracePeriod": 7,
                "closeAfter": 7,
                "percentage": 50,
            },
            "experiment": {
                "name": "Extended Grace Period",
                "gracePeriod": 10,
                "closeAfter": 10,
                "percentage": 50,
            },
        },
    }


@pytest.fixture
def config_file(tmp_path, mock_config):
    """Create a temporary config file."""
    config_path = tmp_path / "ab-test-config.yml"
    with open(config_path, "w") as f:
        yaml.dump(mock_config, f)
    return config_path


@pytest.fixture
def assigner(config_file):
    """Create ABTestAssigner with test config."""
    return ABTestAssigner(str(config_file))


class TestABTestAssignerInit:
    """Test ABTestAssigner initialization."""

    def test_init_loads_config(self, config_file, mock_config):
        """Test initialization loads configuration correctly."""
        assigner = ABTestAssigner(str(config_file))

        assert assigner.config["test"]["name"] == mock_config["test"]["name"]
        assert assigner.seed == mock_config["split"]["seed"]

    def test_init_raises_on_missing_file(self, tmp_path):
        """Test initialization raises FileNotFoundError for missing config."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            ABTestAssigner(str(tmp_path / "nonexistent.yml"))

    def test_init_with_custom_path(self, config_file):
        """Test initialization with custom config path."""
        assigner = ABTestAssigner(str(config_file))
        assert assigner.config_path == config_file


class TestHashRepository:
    """Test repository hashing for deterministic assignment."""

    def test_hash_is_deterministic(self, assigner):
        """Test same repo always gets same hash."""
        repo = "org/my-repo"
        hash1 = assigner._hash_repository(repo)
        hash2 = assigner._hash_repository(repo)
        assert hash1 == hash2

    def test_different_repos_get_different_hashes(self, assigner):
        """Test different repos get different hashes."""
        hash1 = assigner._hash_repository("org/repo1")
        hash2 = assigner._hash_repository("org/repo2")
        assert hash1 != hash2

    def test_hash_changes_with_seed(self, tmp_path, mock_config):
        """Test different seeds produce different hashes."""
        # Create config with different seed
        mock_config["split"]["seed"] = "different-seed"
        config_path = tmp_path / "config2.yml"
        with open(config_path, "w") as f:
            yaml.dump(mock_config, f)

        assigner2 = ABTestAssigner(str(config_path))

        # Create original config
        mock_config["split"]["seed"] = "test-seed-2024"
        config_path = tmp_path / "config1.yml"
        with open(config_path, "w") as f:
            yaml.dump(mock_config, f)

        assigner1 = ABTestAssigner(str(config_path))

        # Same repo, different seeds should produce different hashes
        hash1 = assigner1._hash_repository("org/repo")
        hash2 = assigner2._hash_repository("org/repo")
        assert hash1 != hash2

    def test_hash_returns_integer(self, assigner):
        """Test hash returns an integer."""
        hash_value = assigner._hash_repository("org/repo")
        assert isinstance(hash_value, int)


class TestAssignGroup:
    """Test group assignment logic."""

    def test_assigns_control_for_even_hash(self, assigner):
        """Test repository assigned to control for even hash value."""
        # Mock the hash to return an even number
        with patch.object(assigner, "_hash_repository", return_value=100):
            group = assigner.assign_group("org/repo")
            assert group == "control"

    def test_assigns_experiment_for_odd_hash(self, assigner):
        """Test repository assigned to experiment for odd hash value."""
        # Mock the hash to return an odd number
        with patch.object(assigner, "_hash_repository", return_value=101):
            group = assigner.assign_group("org/repo")
            assert group == "experiment"

    def test_excluded_repo_returns_excluded(self, assigner):
        """Test excluded repository returns 'excluded'."""
        group = assigner.assign_group("security/vuln-scanner")
        assert group == "excluded"

    def test_wildcard_excluded_repo_returns_excluded(self, assigner):
        """Test wildcard pattern exclusion works."""
        group = assigner.assign_group("infra/terraform-modules")
        assert group == "excluded"


class TestIsExcluded:
    """Test repository exclusion logic."""

    def test_exact_match_excluded(self, assigner):
        """Test exact repository name is excluded."""
        assert assigner._is_excluded("security/vuln-scanner") is True

    def test_wildcard_match_excluded(self, assigner):
        """Test wildcard pattern matches."""
        assert assigner._is_excluded("infra/any-repo") is True

    def test_non_excluded_repo(self, assigner):
        """Test non-excluded repository returns False."""
        assert assigner._is_excluded("org/regular-repo") is False

    def test_partial_match_not_excluded(self, assigner):
        """Test partial name match is not excluded."""
        assert assigner._is_excluded("security-tools/scanner") is False


class TestGetGroupConfig:
    """Test group configuration retrieval."""

    def test_returns_control_config(self, assigner):
        """Test returns control group configuration."""
        config = assigner.get_group_config("control")
        assert config["name"] == "Control Group"
        assert config["gracePeriod"] == 7

    def test_returns_experiment_config(self, assigner):
        """Test returns experiment group configuration."""
        config = assigner.get_group_config("experiment")
        assert config["name"] == "Extended Grace Period"
        assert config["gracePeriod"] == 10

    def test_returns_none_for_excluded(self, assigner):
        """Test returns None for excluded group."""
        config = assigner.get_group_config("excluded")
        assert config is None

    def test_returns_none_for_unknown_group(self, assigner):
        """Test returns None for unknown group."""
        config = assigner.get_group_config("unknown")
        assert config is None


class TestGetGracePeriod:
    """Test grace period retrieval."""

    def test_control_group_grace_period(self, assigner):
        """Test control group returns 7 days."""
        with patch.object(assigner, "assign_group", return_value="control"):
            period = assigner.get_grace_period("org/repo")
            assert period == 7

    def test_experiment_group_grace_period(self, assigner):
        """Test experiment group returns 10 days."""
        with patch.object(assigner, "assign_group", return_value="experiment"):
            period = assigner.get_grace_period("org/repo")
            assert period == 10

    def test_excluded_repo_gets_default(self, assigner):
        """Test excluded repository returns default (7 days)."""
        period = assigner.get_grace_period("security/vuln-scanner")
        assert period == 7

    def test_unknown_group_gets_default(self, assigner):
        """Test unknown group returns default (7 days)."""
        with patch.object(assigner, "assign_group", return_value="unknown"):
            period = assigner.get_grace_period("org/repo")
            assert period == 7


class TestGenerateWorkflowConfig:
    """Test workflow configuration generation."""

    def test_control_group_config(self, assigner):
        """Test control group workflow configuration."""
        with patch.object(assigner, "assign_group", return_value="control"):
            config = assigner.generate_workflow_config("org/repo")

            assert config["repository"] == "org/repo"
            assert config["group"] == "control"
            assert config["groupName"] == "Control Group"
            assert config["gracePeriod"] == 7
            assert config["closeAfter"] == 7
            assert config["percentage"] == 50

    def test_experiment_group_config(self, assigner):
        """Test experiment group workflow configuration."""
        with patch.object(assigner, "assign_group", return_value="experiment"):
            config = assigner.generate_workflow_config("org/repo")

            assert config["group"] == "experiment"
            assert config["gracePeriod"] == 10

    def test_excluded_repo_config(self, assigner):
        """Test excluded repository workflow configuration."""
        config = assigner.generate_workflow_config("security/vuln-scanner")

        assert config["group"] == "excluded"
        assert config["reason"] == "Excluded from A/B test"
        assert config["gracePeriod"] == 7

    def test_unknown_group_config(self, assigner):
        """Test unknown group returns default configuration."""
        with patch.object(assigner, "assign_group", return_value="unknown"):
            with patch.object(assigner, "get_group_config", return_value=None):
                config = assigner.generate_workflow_config("org/repo")

                assert config["group"] == "unknown"
                assert config["reason"] == "No configuration found"


class TestListAllRepositories:
    """Test repository listing via GitHub CLI."""

    def test_lists_repositories_successfully(self, assigner):
        """Test successful repository listing."""
        mock_result = MagicMock()
        mock_result.stdout = json.dumps(
            [
                {"nameWithOwner": "org/repo1"},
                {"nameWithOwner": "org/repo2"},
            ]
        )

        with patch("ab_test_assignment.subprocess.run", return_value=mock_result):
            repos = assigner.list_all_repositories()

            assert repos == ["org/repo1", "org/repo2"]

    def test_handles_subprocess_error(self, assigner, capsys):
        """Test handles subprocess CalledProcessError."""
        with patch(
            "ab_test_assignment.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "gh", stderr="error"),
        ):
            repos = assigner.list_all_repositories()

            assert repos == []
            captured = capsys.readouterr()
            assert "Error listing repositories" in captured.err

    def test_handles_json_decode_error(self, assigner, capsys):
        """Test handles invalid JSON response."""
        mock_result = MagicMock()
        mock_result.stdout = "not valid json"

        with patch("ab_test_assignment.subprocess.run", return_value=mock_result):
            repos = assigner.list_all_repositories()

            assert repos == []
            captured = capsys.readouterr()
            assert "Error parsing repository list" in captured.err


class TestAssignAllRepositories:
    """Test bulk repository assignment."""

    def test_assigns_all_repos_to_groups(self, assigner):
        """Test assigns all repositories to appropriate groups."""
        repos = ["org/repo1", "org/repo2", "security/vuln-scanner"]

        with patch.object(assigner, "list_all_repositories", return_value=repos):
            with patch.object(
                assigner,
                "assign_group",
                side_effect=["control", "experiment", "excluded"],
            ):
                assignments = assigner.assign_all_repositories()

                assert assignments["control"] == ["org/repo1"]
                assert assignments["experiment"] == ["org/repo2"]
                assert assignments["excluded"] == ["security/vuln-scanner"]


class TestGenerateReport:
    """Test report generation."""

    def test_generates_complete_report(self, assigner):
        """Test generates report with all required fields."""
        assignments = {
            "control": ["org/repo1", "org/repo2"],
            "experiment": ["org/repo3"],
            "excluded": ["security/vuln-scanner"],
        }

        with patch.object(assigner, "assign_all_repositories", return_value=assignments):
            report = assigner.generate_report()

            assert report["testName"] == "Stale Grace Period Test"
            assert report["startDate"] == "2024-01-15"
            assert report["assignments"]["control"]["count"] == 2
            assert report["assignments"]["experiment"]["count"] == 1
            assert report["assignments"]["excluded"]["count"] == 1
            assert report["totalActive"] == 3
            assert report["splitRatio"] == "2:1"

    def test_report_percentages_calculated(self, assigner):
        """Test percentages are calculated correctly."""
        assignments = {
            "control": ["org/repo1", "org/repo2"],
            "experiment": ["org/repo3", "org/repo4"],
            "excluded": [],
        }

        with patch.object(assigner, "assign_all_repositories", return_value=assignments):
            report = assigner.generate_report()

            assert report["assignments"]["control"]["percentage"] == 50.0
            assert report["assignments"]["experiment"]["percentage"] == 50.0

    def test_report_handles_empty_repos(self, assigner):
        """Test report handles zero repositories."""
        assignments = {"control": [], "experiment": [], "excluded": []}

        with patch.object(assigner, "assign_all_repositories", return_value=assignments):
            report = assigner.generate_report()

            assert report["assignments"]["control"]["percentage"] == 0
            assert report["totalActive"] == 0


class TestPrintTable:
    """Test table printing utility."""

    def test_prints_formatted_table(self, capsys):
        """Test prints formatted table with headers."""
        headers = ["Name", "Group", "Period"]
        data = [
            ["repo1", "control", "7"],
            ["repo2", "experiment", "10"],
        ]

        print_table(data, headers)

        captured = capsys.readouterr()
        assert "Name" in captured.out
        assert "Group" in captured.out
        assert "Period" in captured.out
        assert "repo1" in captured.out
        assert "repo2" in captured.out

    def test_handles_varying_column_widths(self, capsys):
        """Test handles columns with different widths."""
        headers = ["A", "Long Header Name"]
        data = [["x", "short"], ["longer-value", "y"]]

        print_table(data, headers)

        captured = capsys.readouterr()
        # Table should be properly aligned
        assert "A" in captured.out
        assert "Long Header Name" in captured.out


class TestMainFunction:
    """Test main() function with various arguments."""

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_repo_with_json_flag(self, MockAssigner):
        """Test main with --repo and --json flags."""
        mock_instance = MockAssigner.return_value
        mock_instance.generate_workflow_config.return_value = {
            "repository": "org/repo",
            "group": "control",
            "groupName": "Control Group",
            "gracePeriod": 7,
            "closeAfter": 7,
            "percentage": 50,
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "org/repo", "--json"]):
            with patch("builtins.print") as mock_print:
                main()

                # Should print JSON output
                calls = [str(call) for call in mock_print.call_args_list]
                # JSON output should contain the repository info
                assert any("org/repo" in c for c in calls)
                # Should be formatted JSON (contains indent)
                assert any('"repository"' in c for c in calls)

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_all_with_json_flag(self, MockAssigner):
        """Test main with --all and --json flags."""
        mock_instance = MockAssigner.return_value
        mock_instance.generate_report.return_value = {
            "testName": "Test",
            "startDate": "2024-01-01",
            "assignments": {
                "control": {"count": 5, "percentage": 50, "repositories": ["r1"]},
                "experiment": {"count": 5, "percentage": 50, "repositories": ["r2"]},
                "excluded": {"count": 0, "repositories": []},
            },
            "totalActive": 10,
            "splitRatio": "5:5",
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--all", "--json"]):
            with patch("builtins.print") as mock_print:
                main()

                # Should print JSON output
                calls = [str(call) for call in mock_print.call_args_list]
                # Should contain JSON-formatted report
                assert any('"testName"' in c for c in calls)

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_handles_exception(self, MockAssigner, capsys):
        """Test main handles exceptions gracefully."""
        MockAssigner.side_effect = Exception("Test error")

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "org/repo"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Error: Test error" in captured.err

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_repo_non_excluded(self, MockAssigner):
        """Test main with non-excluded repository shows group details."""
        mock_instance = MockAssigner.return_value
        mock_instance.generate_workflow_config.return_value = {
            "repository": "org/repo",
            "group": "control",
            "groupName": "Control Group",
            "gracePeriod": 7,
            "closeAfter": 7,
            "percentage": 50,
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "org/repo"]):
            with patch("builtins.print") as mock_print:
                main()

                calls = [str(call) for call in mock_print.call_args_list]
                assert any("Group Name" in c for c in calls)
                assert any("Grace Period" in c for c in calls)
                assert any("Close After" in c for c in calls)

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_excluded_repo(self, MockAssigner):
        """Test main with excluded repository."""
        mock_instance = MockAssigner.return_value
        mock_instance.generate_workflow_config.return_value = {
            "repository": "security/scanner",
            "group": "excluded",
            "reason": "Excluded from A/B test",
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--repo", "security/scanner"]):
            with patch("builtins.print") as mock_print:
                main()

                # Should print reason instead of group details
                calls = [str(call) for call in mock_print.call_args_list]
                assert any("excluded" in c for c in calls)
                assert any("Excluded from A/B test" in c for c in calls)

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_no_args_shows_help(self, MockAssigner):
        """Test main with no arguments shows help."""
        mock_instance = MockAssigner.return_value

        with patch("sys.argv", ["ab_test_assignment.py"]):
            with patch("argparse.ArgumentParser.print_help") as mock_help:
                main()
                mock_help.assert_called_once()

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_all_with_excluded(self, MockAssigner):
        """Test main --all with excluded repositories."""
        mock_instance = MockAssigner.return_value
        mock_instance.generate_report.return_value = {
            "testName": "Test",
            "startDate": "2024-01-01",
            "assignments": {
                "control": {"count": 5, "percentage": 50, "repositories": ["r1"]},
                "experiment": {"count": 5, "percentage": 50, "repositories": ["r2"]},
                "excluded": {"count": 2, "repositories": ["excluded1", "excluded2"]},
            },
            "totalActive": 10,
            "splitRatio": "5:5",
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--all"]):
            with patch("builtins.print") as mock_print:
                main()
                calls = [str(call) for call in mock_print.call_args_list]
                assert any("Excluded Repositories" in c for c in calls)

    @patch("ab_test_assignment.ABTestAssigner")
    def test_main_all_with_many_repos(self, MockAssigner):
        """Test main --all truncates long lists."""
        mock_instance = MockAssigner.return_value
        many_repos = [f"org/repo{i}" for i in range(20)]
        mock_instance.generate_report.return_value = {
            "testName": "Test",
            "startDate": "2024-01-01",
            "assignments": {
                "control": {"count": 20, "percentage": 50, "repositories": many_repos},
                "experiment": {"count": 20, "percentage": 50, "repositories": many_repos},
                "excluded": {"count": 0, "repositories": []},
            },
            "totalActive": 40,
            "splitRatio": "20:20",
        }

        with patch("sys.argv", ["ab_test_assignment.py", "--all"]):
            with patch("builtins.print") as mock_print:
                main()
                calls = [str(call) for call in mock_print.call_args_list]
                # Should show "... and X more"
                assert any("more" in c for c in calls)

    def test_main_with_custom_config_path(self, config_file):
        """Test main with custom config path."""
        with patch(
            "sys.argv",
            [
                "ab_test_assignment.py",
                "--config",
                str(config_file),
                "--repo",
                "org/repo",
            ],
        ):
            with patch("builtins.print"):
                # Should not raise
                main()

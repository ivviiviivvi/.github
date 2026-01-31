#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_pilot_workflows.py

Focus: Workflow generation from YAML configuration.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from generate_pilot_workflows import WorkflowGenerator, main


@pytest.mark.unit
class TestWorkflowGeneratorInit:
    """Test WorkflowGenerator initialization."""

    def test_init_loads_config(self, tmp_path):
        """Test initialization loads config from file."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: true
    priority: P1
    labelRules: []
    autoAssign:
      enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)

        generator = WorkflowGenerator(str(config_path))

        assert generator.repo["name"] == "test-repo"
        assert generator.repo["owner"] == "test-owner"

    def test_init_with_missing_file(self):
        """Test initialization with missing config file."""
        with pytest.raises(FileNotFoundError):
            WorkflowGenerator("/nonexistent/config.yml")


@pytest.mark.unit
class TestGenerateIssueTriage:
    """Test issue triage workflow generation."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: true
    priority: P1
    labelRules:
      - pattern: bug
        conditions:
          - titleContains: [bug, error]
          - bodyContains: [crash, fail]
      - pattern: feature
        conditions:
          - titleContains: [feature, request]
          - bodyContains: [enhancement]
    autoAssign:
      enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_issue_triage_workflow(self, generator):
        """Test generates issue triage workflow."""
        result = generator.generate_issue_triage()

        assert result is not None
        assert "name: Issue Triage" in result
        assert "issues:" in result
        assert "github-script@v7" in result

    def test_generates_label_rules(self, generator):
        """Test generates label rules from config."""
        result = generator.generate_issue_triage()

        assert "bug" in result
        assert "feature" in result

    def test_returns_none_when_disabled(self, tmp_path):
        """Test returns None when disabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_issue_triage()

        assert result is None

    def test_generates_auto_assign_when_enabled(self, tmp_path):
        """Test generates auto-assign section when enabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: true
    priority: P1
    labelRules: []
    autoAssign:
      enabled: true
      teams:
        - team1
        - team2
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_issue_triage()

        assert result is not None
        assert "Auto-assign to team" in result


@pytest.mark.unit
class TestGenerateAutoAssignReviewers:
    """Test auto-assign reviewers workflow generation."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: true
    priority: P2
    rules:
      - paths:
          - src/
          - lib/
        reviewers:
          - user1
          - user2
        count: 2
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_auto_assign_workflow(self, generator):
        """Test generates auto-assign reviewers workflow."""
        result = generator.generate_auto_assign_reviewers()

        assert result is not None
        assert "name: Auto-Assign Reviewers" in result
        assert "pull_request:" in result

    def test_returns_none_when_disabled(self, tmp_path):
        """Test returns None when disabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_auto_assign_reviewers()

        assert result is None


@pytest.mark.unit
class TestGenerateStaleManagement:
    """Test stale management workflow generation."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: true
    priority: P3
    schedule: '0 0 * * *'
customization:
  stale:
    daysUntilStale: 60
    daysUntilClose: 7
    staleIssueLabel: stale
    stalePRLabel: stale
    exemptLabels:
      - pinned
      - security
    staleIssueMessage: 'This issue is stale.'
    stalePRMessage: 'This PR is stale.'
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_stale_workflow(self, generator):
        """Test generates stale management workflow."""
        result = generator.generate_stale_management()

        assert result is not None
        assert "name: Stale Management" in result
        assert "schedule:" in result
        assert "actions/stale@v9" in result

    def test_returns_none_when_disabled(self, tmp_path):
        """Test returns None when disabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_stale_management()

        assert result is None


@pytest.mark.unit
class TestGenerateStatusSync:
    """Test status sync workflow generation."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  statusSync:
    enabled: true
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_status_sync_workflow(self, generator):
        """Test generates status sync workflow."""
        result = generator.generate_status_sync()

        assert result is not None
        assert "name: Status Sync" in result
        assert "pull_request:" in result
        assert "check_suite:" in result

    def test_returns_none_when_disabled(self, tmp_path):
        """Test returns None when disabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  statusSync:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_status_sync()

        assert result is None

    def test_default_enabled(self, tmp_path):
        """Test status sync is enabled by default."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_status_sync()

        assert result is not None


@pytest.mark.unit
class TestGenerateCollectMetrics:
    """Test collect metrics workflow generation."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  workflowMetrics:
    enabled: true
    schedule: '0 */6 * * *'
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_collect_metrics_workflow(self, generator):
        """Test generates collect metrics workflow."""
        result = generator.generate_collect_metrics()

        assert result is not None
        assert "name: Collect Metrics" in result
        assert "schedule:" in result
        assert "0 */6 * * *" in result

    def test_returns_none_when_disabled(self, tmp_path):
        """Test returns None when disabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  workflowMetrics:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_collect_metrics()

        assert result is None

    def test_default_schedule(self, tmp_path):
        """Test default schedule when not specified."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  workflowMetrics:
    enabled: true
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        result = generator.generate_collect_metrics()

        assert result is not None
        assert "0 */6 * * *" in result


@pytest.mark.unit
class TestGenerateAutoAssign:
    """Test generate_auto_assign alias."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with test config."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: true
    priority: P2
    rules: []
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_is_alias_for_auto_assign_reviewers(self, generator):
        """Test generate_auto_assign is alias for generate_auto_assign_reviewers."""
        result1 = generator.generate_auto_assign()
        result2 = generator.generate_auto_assign_reviewers()

        assert result1 == result2


@pytest.mark.unit
class TestGenerateAll:
    """Test generate_all method."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create generator with all workflows enabled."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: true
    priority: P1
    labelRules: []
    autoAssign:
      enabled: false
  autoAssignReviewers:
    enabled: true
    priority: P2
    rules: []
  staleManagement:
    enabled: true
    priority: P3
    schedule: '0 0 * * *'
  statusSync:
    enabled: true
  workflowMetrics:
    enabled: true
customization:
  stale:
    daysUntilStale: 60
    daysUntilClose: 7
    staleIssueLabel: stale
    stalePRLabel: stale
    exemptLabels: []
    staleIssueMessage: 'Stale.'
    stalePRMessage: 'Stale.'
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        return WorkflowGenerator(str(config_path))

    def test_generates_all_workflows(self, generator, tmp_path, capsys):
        """Test generates all workflow files."""
        output_dir = tmp_path / "workflows"

        generator.generate_all(str(output_dir))

        assert output_dir.exists()
        # Check that files were created
        files = list(output_dir.glob("*.yml"))
        assert len(files) >= 1

        captured = capsys.readouterr()
        assert "Generated" in captured.out

    def test_skips_disabled_workflows(self, tmp_path, capsys):
        """Test skips disabled workflows."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
  statusSync:
    enabled: false
  workflowMetrics:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)
        generator = WorkflowGenerator(str(config_path))

        output_dir = tmp_path / "workflows"
        generator.generate_all(str(output_dir))

        captured = capsys.readouterr()
        assert "Skipped" in captured.out

    def test_creates_output_directory(self, generator, tmp_path):
        """Test creates output directory if it doesn't exist."""
        output_dir = tmp_path / "nested" / "workflows"

        generator.generate_all(str(output_dir))

        assert output_dir.exists()


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_no_args(self, capsys):
        """Test main with no arguments."""
        with patch.object(sys, "argv", ["generate_pilot_workflows.py"]):
            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_missing_config(self, capsys):
        """Test main with missing config file."""
        with patch.object(
            sys, "argv", ["generate_pilot_workflows.py", "/nonexistent/config.yml"]
        ):
            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_main_with_valid_config(self, tmp_path, capsys):
        """Test main with valid config file."""
        config_content = """
repository:
  name: test-repo
  owner: test-owner
workflows:
  issueTriage:
    enabled: false
  autoAssignReviewers:
    enabled: false
  staleManagement:
    enabled: false
customization:
  stale:
    daysUntilStale: 60
"""
        config_path = tmp_path / "config.yml"
        config_path.write_text(config_content)

        with patch.object(sys, "argv", ["generate_pilot_workflows.py", str(config_path)]):
            main()

        captured = capsys.readouterr()
        assert "Workflows generated" in captured.out

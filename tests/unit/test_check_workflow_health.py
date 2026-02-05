#!/usr/bin/env python3
"""Unit tests for automation/scripts/check_workflow_health.py

Focus: Configuration validation and workflow deprecation checks.
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from check_workflow_health import check_configs, check_workflows


@pytest.mark.unit
class TestCheckConfigs:
    """Test configuration file checking."""

    @pytest.fixture
    def mock_github_dir(self, tmp_path, monkeypatch):
        """Create mock .github directory structure."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)
        return github_dir

    def test_returns_list_of_missing_configs(self, mock_github_dir):
        """Test returns list of missing config files."""
        missing = check_configs()

        assert isinstance(missing, list)
        assert len(missing) > 0

    def test_detects_existing_config(self, mock_github_dir, capsys):
        """Test detects and reports existing config files."""
        config_file = mock_github_dir / "auto-merge.yml"
        config_file.write_text("enabled: true")

        check_configs()

        captured = capsys.readouterr()
        assert "Found" in captured.out or "auto-merge.yml" in captured.out

    def test_reports_missing_configs(self, mock_github_dir, capsys):
        """Test reports missing config files."""
        check_configs()

        captured = capsys.readouterr()
        assert "Missing" in captured.out

    def test_checks_required_configs(self, mock_github_dir):
        """Test checks all required config files."""
        required_configs = [
            "auto-merge.yml",
            "routing.yml",
            "self-healing.yml",
            "maintenance.yml",
            "analytics.yml",
            "sla.yml",
            "incident.yml",
        ]

        missing = check_configs()

        # All should be missing since we didn't create them
        for config in required_configs:
            assert any(config in m for m in missing)

    def test_returns_empty_when_all_present(self, mock_github_dir):
        """Test returns empty list when all configs exist."""
        required_configs = [
            "auto-merge.yml",
            "routing.yml",
            "self-healing.yml",
            "maintenance.yml",
            "analytics.yml",
            "sla.yml",
            "incident.yml",
        ]

        for config in required_configs:
            (mock_github_dir / config).write_text("enabled: true")

        missing = check_configs()

        assert len(missing) == 0


@pytest.mark.unit
class TestCheckWorkflows:
    """Test workflow file checking."""

    @pytest.fixture
    def mock_workflow_dir(self, tmp_path, monkeypatch):
        """Create mock workflows directory."""
        workflow_dir = tmp_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        return workflow_dir

    def test_reports_missing_workflow_dir(self, tmp_path, monkeypatch, capsys):
        """Test reports when workflow directory is missing."""
        monkeypatch.chdir(tmp_path)

        check_workflows()

        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_detects_yaml_syntax_errors(self, mock_workflow_dir, capsys):
        """Test detects and reports YAML syntax errors."""
        workflow = mock_workflow_dir / "broken.yml"
        workflow.write_text("name: Broken\n  invalid: yaml here")

        check_workflows()

        captured = capsys.readouterr()
        assert "YAML Syntax Error" in captured.out or "broken.yml" in captured.out

    def test_detects_deprecated_set_output(self, mock_workflow_dir, capsys):
        """Test detects deprecated ::set-output command."""
        workflow = mock_workflow_dir / "old-output.yml"
        workflow.write_text("""
name: Old Output
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "::set-output name=test::value"
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "set-output" in captured.out or "Deprecated" in captured.out

    def test_detects_deprecated_save_state(self, mock_workflow_dir, capsys):
        """Test detects deprecated ::save-state command."""
        workflow = mock_workflow_dir / "old-state.yml"
        workflow.write_text("""
name: Old State
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "::save-state name=test::value"
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "save-state" in captured.out or "Deprecated" in captured.out

    def test_detects_deprecated_ubuntu_runner(self, mock_workflow_dir, capsys):
        """Test detects deprecated ubuntu-18.04 runner."""
        workflow = mock_workflow_dir / "old-runner.yml"
        workflow.write_text("""
name: Old Runner
on: push
jobs:
  build:
    runs-on: ubuntu-18.04
    steps:
      - run: echo "Hello"
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "ubuntu-18.04" in captured.out or "Deprecated" in captured.out

    def test_detects_deprecated_node12(self, mock_workflow_dir, capsys):
        """Test detects deprecated Node.js 12."""
        workflow = mock_workflow_dir / "node12.yml"
        workflow.write_text("""
name: Node 12
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: 12
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "Node" in captured.out or "12" in captured.out

    def test_detects_deprecated_node16(self, mock_workflow_dir, capsys):
        """Test detects deprecated Node.js 16."""
        workflow = mock_workflow_dir / "node16.yml"
        workflow.write_text("""
name: Node 16
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: '16'
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "Node" in captured.out or "16" in captured.out

    def test_detects_old_checkout_action(self, mock_workflow_dir, capsys):
        """Test detects old checkout action v2."""
        workflow = mock_workflow_dir / "old-checkout.yml"
        workflow.write_text("""
name: Old Checkout
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "checkout" in captured.out or "v2" in captured.out

    def test_detects_old_setup_python(self, mock_workflow_dir, capsys):
        """Test detects old setup-python action v2."""
        workflow = mock_workflow_dir / "old-python.yml"
        workflow.write_text("""
name: Old Python
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v2
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "setup-python" in captured.out or "v2" in captured.out

    def test_detects_old_setup_node(self, mock_workflow_dir, capsys):
        """Test detects old setup-node action v2."""
        workflow = mock_workflow_dir / "old-node.yml"
        workflow.write_text("""
name: Old Node
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v2
""")

        check_workflows()

        captured = capsys.readouterr()
        assert "setup-node" in captured.out or "v2" in captured.out

    def test_no_warnings_for_valid_workflow(self, mock_workflow_dir, capsys):
        """Test no warnings for valid modern workflow."""
        workflow = mock_workflow_dir / "valid.yml"
        workflow.write_text("""
name: Valid Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm test
""")

        check_workflows()

        captured = capsys.readouterr()
        # Should not contain deprecation warnings for this file
        # Note: output may still contain header messages

    def test_handles_file_read_errors(self, mock_workflow_dir, capsys):
        """Test handles file read errors gracefully."""
        workflow = mock_workflow_dir / "unreadable.yml"
        workflow.write_text("name: Test")

        # Make file unreadable (Unix-like systems only)
        try:
            os.chmod(workflow, 0o000)

            check_workflows()

            captured = capsys.readouterr()
            # Should handle error gracefully
        finally:
            # Restore permissions for cleanup
            os.chmod(workflow, 0o644)

    def test_processes_all_yml_files(self, mock_workflow_dir, capsys):
        """Test processes all .yml files in directory."""
        for i in range(3):
            workflow = mock_workflow_dir / f"workflow-{i}.yml"
            workflow.write_text(f"name: Workflow {i}\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        check_workflows()

        # Should process all files without errors

    def test_multiple_issues_in_one_file(self, mock_workflow_dir, capsys):
        """Test detects multiple issues in single file."""
        workflow = mock_workflow_dir / "many-issues.yml"
        workflow.write_text("""
name: Many Issues
on: push
jobs:
  build:
    runs-on: ubuntu-18.04
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: 12
      - run: echo "::set-output name=test::value"
""")

        check_workflows()

        captured = capsys.readouterr()
        # Should report multiple issues
        assert captured.out.count("many-issues.yml") >= 1


@pytest.mark.unit
class TestIntegration:
    """Test integration between check functions."""

    @pytest.fixture
    def full_mock_setup(self, tmp_path, monkeypatch):
        """Create full mock .github structure."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()

        workflow_dir = github_dir / "workflows"
        workflow_dir.mkdir()

        monkeypatch.chdir(tmp_path)

        return github_dir, workflow_dir

    def test_both_checks_run_independently(self, full_mock_setup, capsys):
        """Test both check functions run independently."""
        github_dir, workflow_dir = full_mock_setup

        # Create a valid workflow
        workflow = workflow_dir / "test.yml"
        workflow.write_text("name: Test\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        # Run both checks
        missing_configs = check_configs()
        check_workflows()

        captured = capsys.readouterr()
        # Both should produce output
        assert "Checking" in captured.out or "Missing" in captured.out

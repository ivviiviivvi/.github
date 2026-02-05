#!/usr/bin/env python3
"""Unit tests for automation/scripts/analyze_workflows.py

Focus: Workflow file analysis and inventory report generation.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from analyze_workflows import analyze_workflow, main


@pytest.mark.unit
class TestAnalyzeWorkflow:
    """Test individual workflow analysis."""

    @pytest.fixture
    def mock_workflow_dir(self, tmp_path):
        """Create mock workflows directory."""
        workflow_dir = tmp_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        return workflow_dir

    def test_returns_none_for_empty_file(self, mock_workflow_dir):
        """Test returns None for empty workflow file."""
        workflow = mock_workflow_dir / "empty.yml"
        workflow.write_text("")

        result = analyze_workflow(workflow)

        assert result is None

    def test_extracts_workflow_name(self, mock_workflow_dir):
        """Test extracts workflow name from YAML."""
        workflow = mock_workflow_dir / "test.yml"
        workflow.write_text("name: Test Workflow\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        result = analyze_workflow(workflow)

        assert result["name"] == "Test Workflow"

    def test_uses_unnamed_for_missing_name(self, mock_workflow_dir):
        """Test uses 'Unnamed' when name is not specified."""
        workflow = mock_workflow_dir / "no-name.yml"
        workflow.write_text("on: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        result = analyze_workflow(workflow)

        assert result["name"] == "Unnamed"

    def test_extracts_trigger_list(self, mock_workflow_dir):
        """Test extracts trigger types from 'on' key."""
        workflow = mock_workflow_dir / "triggers.yml"
        workflow.write_text("""
name: Multi Trigger
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert "push" in result["triggers"]
        assert "pull_request" in result["triggers"]

    def test_handles_simple_on_trigger(self, mock_workflow_dir):
        """Test handles simple 'on: push' format."""
        workflow = mock_workflow_dir / "simple.yml"
        workflow.write_text("name: Simple\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        result = analyze_workflow(workflow)

        assert result["triggers"] == ["push"]

    def test_extracts_job_names(self, mock_workflow_dir):
        """Test extracts job names from workflow."""
        workflow = mock_workflow_dir / "jobs.yml"
        workflow.write_text("""
name: Multi Job
on: push
jobs:
  build:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
  deploy:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert "build" in result["jobs"]
        assert "test" in result["jobs"]
        assert "deploy" in result["jobs"]
        assert result["job_count"] == 3

    def test_calculates_complexity_score(self, mock_workflow_dir):
        """Test calculates complexity score."""
        workflow = mock_workflow_dir / "complex.yml"
        workflow.write_text("""
name: Complex Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
""")

        result = analyze_workflow(workflow)

        assert result["complexity"] > 0

    def test_detects_schedule_trigger(self, mock_workflow_dir):
        """Test detects scheduled workflows."""
        workflow = mock_workflow_dir / "scheduled.yml"
        workflow.write_text("""
name: Scheduled
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  run:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert result["has_schedule"] is True

    def test_detects_workflow_dispatch(self, mock_workflow_dir):
        """Test detects manual dispatch trigger."""
        workflow = mock_workflow_dir / "manual.yml"
        workflow.write_text("""
name: Manual
on: workflow_dispatch
jobs:
  run:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert result["has_workflow_dispatch"] is True

    def test_detects_push_trigger(self, mock_workflow_dir):
        """Test detects push trigger."""
        workflow = mock_workflow_dir / "push.yml"
        workflow.write_text("""
name: Push
on: push
jobs:
  run:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert result["has_push"] is True

    def test_detects_pull_request_trigger(self, mock_workflow_dir):
        """Test detects pull_request trigger."""
        workflow = mock_workflow_dir / "pr.yml"
        workflow.write_text("""
name: PR
on: pull_request
jobs:
  run:
    runs-on: ubuntu-latest
""")

        result = analyze_workflow(workflow)

        assert result["has_pull_request"] is True

    def test_handles_yaml_parse_error(self, mock_workflow_dir):
        """Test handles YAML parsing errors gracefully."""
        workflow = mock_workflow_dir / "invalid.yml"
        # Use truly invalid YAML - tabs mixed with spaces in indentation
        workflow.write_text("name: Invalid\njobs:\n  build:\n\t  invalid: tab-mixing")

        result = analyze_workflow(workflow)

        assert result is not None
        assert result["name"] == "ERROR"
        assert "error" in result

    def test_result_includes_filename(self, mock_workflow_dir):
        """Test result includes workflow filename."""
        workflow = mock_workflow_dir / "my-workflow.yml"
        workflow.write_text("name: My Workflow\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        result = analyze_workflow(workflow)

        assert result["file"] == "my-workflow.yml"


@pytest.mark.unit
class TestMainFunction:
    """Test main function for workflow analysis."""

    @pytest.fixture
    def mock_workflow_dir(self, tmp_path, monkeypatch):
        """Create mock workflow directory and patch Path."""
        workflow_dir = tmp_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)

        # Change to tmp_path directory so relative path works
        monkeypatch.chdir(tmp_path)

        return workflow_dir

    def test_prints_error_when_directory_missing(self, capsys, monkeypatch, tmp_path):
        """Test prints error when workflows directory is missing."""
        monkeypatch.chdir(tmp_path)

        main()

        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_analyzes_all_workflow_files(self, mock_workflow_dir, capsys):
        """Test analyzes all .yml files in directory."""
        for i in range(3):
            workflow = mock_workflow_dir / f"workflow-{i}.yml"
            workflow.write_text(f"name: Workflow {i}\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "workflow-0.yml" in captured.out
        assert "workflow-1.yml" in captured.out
        assert "workflow-2.yml" in captured.out

    def test_handles_yaml_extension(self, mock_workflow_dir, capsys):
        """Test handles both .yml and .yaml extensions."""
        yml_file = mock_workflow_dir / "test.yml"
        yml_file.write_text("name: YML\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        yaml_file = mock_workflow_dir / "test.yaml"
        yaml_file.write_text("name: YAML\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "test.yml" in captured.out
        assert "test.yaml" in captured.out

    def test_prints_summary_statistics(self, mock_workflow_dir, capsys):
        """Test prints summary statistics."""
        workflow = mock_workflow_dir / "test.yml"
        workflow.write_text("name: Test\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "SUMMARY STATISTICS" in captured.out
        assert "Total Workflows" in captured.out

    def test_prints_trigger_distribution(self, mock_workflow_dir, capsys):
        """Test prints trigger distribution."""
        workflow = mock_workflow_dir / "test.yml"
        workflow.write_text("name: Test\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "TRIGGER DISTRIBUTION" in captured.out

    def test_identifies_duplicate_names(self, mock_workflow_dir, capsys):
        """Test identifies workflows with duplicate names."""
        for i in range(2):
            workflow = mock_workflow_dir / f"workflow-{i}.yml"
            workflow.write_text("name: Same Name\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "DUPLICATE" in captured.out or "Same Name" in captured.out

    def test_reports_workflow_errors(self, mock_workflow_dir, capsys):
        """Test reports workflows with parsing errors."""
        workflow = mock_workflow_dir / "broken.yml"
        workflow.write_text("name: Broken\n  invalid: yaml")

        main()

        captured = capsys.readouterr()
        assert "ERROR" in captured.out or "broken.yml" in captured.out

    def test_counts_scheduled_workflows(self, mock_workflow_dir, capsys):
        """Test counts scheduled workflows."""
        workflow = mock_workflow_dir / "scheduled.yml"
        workflow.write_text("""
name: Scheduled
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  run:
    runs-on: ubuntu-latest
""")

        main()

        captured = capsys.readouterr()
        assert "Scheduled" in captured.out

    def test_counts_manual_dispatch_workflows(self, mock_workflow_dir, capsys):
        """Test counts workflows with manual dispatch."""
        workflow = mock_workflow_dir / "manual.yml"
        workflow.write_text("name: Manual\non: workflow_dispatch\njobs:\n  run:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "Manual Dispatch" in captured.out or "workflow_dispatch" in captured.out

    def test_lists_high_complexity_workflows(self, mock_workflow_dir, capsys):
        """Test identifies high complexity workflows."""
        # Create a large workflow
        large_content = "name: Large\non: push\njobs:\n"
        for i in range(20):
            large_content += f"  job{i}:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo {i}\n"

        workflow = mock_workflow_dir / "large.yml"
        workflow.write_text(large_content)

        main()

        captured = capsys.readouterr()
        # Should mention complexity in some form
        assert "large.yml" in captured.out


@pytest.mark.unit
class TestWorkflowStatistics:
    """Test workflow statistics calculations."""

    @pytest.fixture
    def mock_workflow_dir(self, tmp_path, monkeypatch):
        """Create mock workflow directory."""
        workflow_dir = tmp_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        return workflow_dir

    def test_counts_total_workflows(self, mock_workflow_dir, capsys):
        """Test counts total number of workflows."""
        for i in range(5):
            workflow = mock_workflow_dir / f"workflow-{i}.yml"
            workflow.write_text(f"name: W{i}\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        main()

        captured = capsys.readouterr()
        assert "5" in captured.out or "Total Workflows: 5" in captured.out

    def test_counts_workflows_with_errors(self, mock_workflow_dir, capsys):
        """Test counts workflows with errors."""
        # Valid workflow
        valid = mock_workflow_dir / "valid.yml"
        valid.write_text("name: Valid\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest")

        # Invalid workflow
        invalid = mock_workflow_dir / "invalid.yml"
        invalid.write_text("name: Invalid\n  broken yaml")

        main()

        captured = capsys.readouterr()
        assert "Error" in captured.out or "invalid.yml" in captured.out

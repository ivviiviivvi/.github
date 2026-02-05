#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_workflow_health_report.py

Focus: Workflow health report generation with security and performance metrics.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from generate_workflow_health_report import find_unpinned_actions, main


@pytest.mark.unit
class TestFindUnpinnedActions:
    """Test find_unpinned_actions function."""

    def test_finds_main_branch_reference(self):
        """Test finds @main branch reference."""
        node = {"jobs": {"build": {"steps": [{"uses": "actions/checkout@main"}]}}}

        result = find_unpinned_actions(node)

        assert "actions/checkout@main" in result

    def test_finds_master_branch_reference(self):
        """Test finds @master branch reference."""
        node = {"jobs": {"build": {"steps": [{"uses": "actions/setup-node@master"}]}}}

        result = find_unpinned_actions(node)

        assert "actions/setup-node@master" in result

    def test_ignores_sha_pinned_actions(self):
        """Test ignores SHA-pinned actions."""
        node = {"jobs": {"build": {"steps": [{"uses": "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683"}]}}}

        result = find_unpinned_actions(node)

        assert len(result) == 0

    def test_ignores_version_pinned_actions(self):
        """Test ignores version-pinned actions."""
        node = {"jobs": {"build": {"steps": [{"uses": "actions/checkout@v4"}, {"uses": "actions/setup-python@v5"}]}}}

        result = find_unpinned_actions(node)

        assert len(result) == 0

    def test_handles_nested_structures(self):
        """Test handles deeply nested structures."""
        node = {
            "jobs": {
                "job1": {"steps": [{"uses": "org/action1@main"}]},
                "job2": {"steps": [{"uses": "org/action2@master"}]},
            }
        }

        result = find_unpinned_actions(node)

        assert len(result) == 2

    def test_handles_empty_node(self):
        """Test handles empty node."""
        result = find_unpinned_actions({})

        assert result == []

    def test_handles_list_values(self):
        """Test handles list values correctly."""
        node = [
            {"uses": "action1@main"},
            {"uses": "action2@v1"},
        ]

        result = find_unpinned_actions(node)

        assert "action1@main" in result
        assert len(result) == 1

    def test_ignores_non_uses_keys(self):
        """Test ignores non-uses keys."""
        node = {
            "name": "actions/checkout@main",  # Not a 'uses' key
            "run": "echo @main",
        }

        result = find_unpinned_actions(node)

        assert result == []


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_generates_health_report(self, tmp_path, monkeypatch):
        """Test generates health report JSON."""
        # Create workflow directory structure
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        # Create a simple workflow
        workflow = workflows_dir / "test.yml"
        workflow.write_text("""name: Test
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report_file = metrics_dir / "latest.json"
        assert report_file.exists()

        report = json.loads(report_file.read_text())
        assert report["total_workflows"] == 1
        assert "overall_health" in report

    def test_detects_missing_permissions(self, tmp_path, monkeypatch, capsys):
        """Test detects workflows missing permissions."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "no-perms.yml"
        workflow.write_text("""name: No Permissions
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert any("Missing explicit permissions" in w for w in report["warnings"])

    def test_detects_unpinned_actions(self, tmp_path, monkeypatch):
        """Test detects unpinned actions."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "unpinned.yml"
        workflow.write_text("""name: Unpinned
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@main
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert any("unpinned actions" in e for e in report["errors"])

    def test_recommends_pip_caching(self, tmp_path):
        """Test recommends pip caching when setup-python without cache."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "no-cache.yml"
        workflow.write_text("""name: No Cache
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/setup-python@v5
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert any("pip caching" in r for r in report["recommendations"])

    def test_recommends_npm_caching(self, tmp_path):
        """Test recommends npm caching when setup-node without cache."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "no-npm-cache.yml"
        workflow.write_text("""name: No NPM Cache
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/setup-node@v4
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert any("npm caching" in r for r in report["recommendations"])

    def test_detects_missing_timeout(self, tmp_path):
        """Test detects workflows missing timeout."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "no-timeout.yml"
        workflow.write_text("""name: No Timeout
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo test
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert any("Missing timeout" in w for w in report["warnings"])

    def test_calculates_health_status_excellent(self, tmp_path, capsys):
        """Test calculates excellent health status."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        # Create a healthy workflow
        workflow = workflows_dir / "healthy.yml"
        workflow.write_text("""name: Healthy
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        captured = capsys.readouterr()
        assert "excellent" in captured.out.lower()

    def test_calculates_health_status_unknown_no_workflows(self, tmp_path, capsys):
        """Test calculates unknown health when no workflows."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert report["overall_health"] == "unknown"

    def test_writes_to_github_output(self, tmp_path, monkeypatch):
        """Test writes to GITHUB_OUTPUT when available."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"
        output_file = tmp_path / "github_output.txt"

        workflow = workflows_dir / "test.yml"
        workflow.write_text("""name: Test
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo test
""")

        monkeypatch.setenv("GITHUB_OUTPUT", str(output_file))

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        output_content = output_file.read_text()
        assert "health=" in output_content
        assert "errors=" in output_content
        assert "warnings=" in output_content

    def test_handles_yaml_files(self, tmp_path):
        """Test handles both .yml and .yaml extensions."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        (workflows_dir / "test1.yml").write_text("name: Test1\non: push\njobs: {}")
        (workflows_dir / "test2.yaml").write_text("name: Test2\non: push\njobs: {}")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        report = json.loads((metrics_dir / "latest.json").read_text())
        assert report["total_workflows"] == 2

    def test_prints_summary(self, tmp_path, capsys):
        """Test prints summary to stdout."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        metrics_dir = tmp_path / "metrics" / "health"

        workflow = workflows_dir / "test.yml"
        workflow.write_text("""name: Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps: []
""")

        with patch("generate_workflow_health_report.REPO_ROOT", tmp_path):
            with patch("generate_workflow_health_report.WORKFLOWS_DIR", workflows_dir):
                with patch("generate_workflow_health_report.METRICS_DIR", metrics_dir):
                    main()

        captured = capsys.readouterr()
        assert "Overall Health:" in captured.out
        assert "Healthy Workflows:" in captured.out
        assert "Errors:" in captured.out
        assert "Warnings:" in captured.out

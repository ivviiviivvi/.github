#!/usr/bin/env python3
"""
Unit tests for ecosystem_visualizer.py
Focus: Diagram generation, workflow categorization, path calculation
"""

import json

# Import the module under test
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))
from ecosystem_visualizer import EcosystemVisualizer


class TestEcosystemVisualizer:
    """Test EcosystemVisualizer initialization and basic functionality"""

    def test_initializes_without_report_path(self):
        """Test initialization without report data"""
        viz = EcosystemVisualizer()
        assert viz.report_path is None
        assert viz.report_data is None

    def test_initializes_with_valid_report(self, tmp_path):
        """Test initialization with valid report data"""
        report_file = tmp_path / "report.json"
        report_data = {"timestamp": "2024-01-14T00:00:00Z", "workflows": []}
        report_file.write_text(json.dumps(report_data))

        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_path == report_file
        assert viz.report_data == report_data

    def test_handles_missing_report_file(self, tmp_path):
        """Test handling of non-existent report file"""
        report_file = tmp_path / "nonexistent.json"
        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_data is None


class TestWorkflowCategorization:
    """Test workflow categorization logic"""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    @pytest.mark.parametrize(
        "workflow_name,expected_category",
        [
            ("safeguard-1-rate-limiting.yml", "🛡️"),
            ("security-scanning.yml", "🔐"),
            ("codeql-analysis.yml", "🔐"),
            ("reusable-python-test.yml", "♻️"),
            ("gemini_workflow.yml", "🤖"),
            ("jules-agent.yml", "🤖"),
            ("ci-test.yml", "🚀"),
            ("deploy-to-production.yml", "🚀"),
            ("pr-batch-merge.yml", "🔀"),
            ("schedule-daily-report.yml", "⏱️"),
            ("health-check.yml", "💓"),
            ("monitor-metrics.yml", "💓"),
            ("random-workflow.yml", "⚙️"),  # Default category
        ],
    )
    def test_categorizes_workflow_correctly(
        self, viz, workflow_name, expected_category
    ):
        """Test workflow categorization based on name patterns"""
        category = viz._categorize_workflow(workflow_name)
        assert category == expected_category

    def test_default_category_for_unknown_workflow(self, viz):
        """Test that unknown workflows get default category"""
        category = viz._categorize_workflow("unknown-workflow.yml")
        assert category == "⚙️"


class TestRelativePathCalculation:
    """Test relative path calculation for links"""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_calculates_path_from_root(self, viz):
        """Test path calculation when output is at root"""
        output_path = Path("dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == ".github/workflows/"

    def test_calculates_path_from_subdirectory(self, viz):
        """Test path calculation when output is in subdirectory"""
        output_path = Path("reports/dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == "../.github/workflows/"

    def test_calculates_path_from_nested_directory(self, viz):
        """Test path calculation when output is deeply nested"""
        output_path = Path("reports/archives/2024/dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == "../../../.github/workflows/"

    def test_handles_current_directory(self, viz):
        """Test path calculation for current directory"""
        output_path = Path(".")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert target in result


class TestMermaidDiagramGeneration:
    """Test Mermaid diagram generation"""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_generates_basic_diagram(self, viz):
        """Test basic Mermaid diagram generation"""
        workflows = [
            {"name": "ci-test.yml", "category": "🚀"},
            {"name": "security-scan.yml", "category": "🔐"},
        ]

        diagram = viz._generate_mermaid_diagram(workflows)

        assert "graph TD" in diagram or "flowchart" in diagram
        assert "ci-test" in diagram
        assert "security-scan" in diagram

    def test_respects_max_workflows_limit(self, viz):
        """Test that diagram respects MAX_DIAGRAM_WORKFLOWS limit"""
        # Create more workflows than the limit
        workflows = [
            {"name": f"workflow-{i}.yml", "category": "🚀"}
            for i in range(viz.MAX_DIAGRAM_WORKFLOWS + 5)
        ]

        diagram = viz._generate_mermaid_diagram(workflows)

        # Should not include all workflows
        workflow_count = sum(1 for w in workflows if w["name"] in diagram)
        assert workflow_count <= viz.MAX_DIAGRAM_WORKFLOWS

    def test_handles_empty_workflow_list(self, viz):
        """Test diagram generation with no workflows"""
        diagram = viz._generate_mermaid_diagram([])

        assert diagram is not None
        # Should have basic structure even if empty


class TestWorkflowListing:
    """Test workflow listing and organization"""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_groups_workflows_by_category(self, viz):
        """Test workflows are grouped by category"""
        workflows = [
            {"name": "ci-1.yml", "path": ".github/workflows/ci-1.yml"},
            {"name": "ci-2.yml", "path": ".github/workflows/ci-2.yml"},
            {"name": "security-1.yml", "path": ".github/workflows/security-1.yml"},
        ]

        grouped = viz._group_workflows_by_category(workflows)

        assert "🚀" in grouped  # CI category
        assert "🔐" in grouped  # Security category
        assert len(grouped["🚀"]) == 2
        assert len(grouped["🔐"]) == 1

    def test_sorts_categories(self, viz):
        """Test that categories are sorted in expected order"""
        categories = viz.WORKFLOW_CATEGORIES.keys()

        # Should start with safeguards
        assert list(categories)[0] == "🛡️"


class TestDashboardGeneration:
    """Test dashboard markdown generation"""

    @pytest.fixture
    def viz_with_data(self, tmp_path):
        """Create visualizer with sample report data"""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "workflows": [
                {
                    "name": "ci-test.yml",
                    "path": ".github/workflows/ci-test.yml",
                    "triggers": ["push", "pull_request"],
                }
            ],
            "metrics": {"total_workflows": 1, "active_workflows": 1},
        }
        report_file.write_text(json.dumps(report_data))
        return EcosystemVisualizer(report_path=report_file)

    def test_generates_dashboard_with_metadata(self, viz_with_data, tmp_path):
        """Test dashboard includes metadata section"""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard(output_path)

        assert "test-org" in dashboard
        assert "2024-01-14" in dashboard
        assert "Workflows" in dashboard

    def test_includes_mermaid_diagram(self, viz_with_data, tmp_path):
        """Test dashboard includes Mermaid diagram"""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard(output_path)

        assert "```mermaid" in dashboard
        assert "ci-test" in dashboard

    def test_includes_workflow_lists(self, viz_with_data, tmp_path):
        """Test dashboard includes workflow listings"""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard(output_path)

        assert "ci-test.yml" in dashboard
        assert "🚀" in dashboard  # CI/CD category


class TestTechnologyDetection:
    """Test technology stack detection"""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_detects_python_workflows(self, viz):
        """Test detection of Python-related workflows"""
        workflow_content = """
        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/setup-python@v4
              - run: pytest
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Python" in technologies or "pytest" in technologies

    def test_detects_nodejs_workflows(self, viz):
        """Test detection of Node.js-related workflows"""
        workflow_content = """
        jobs:
          build:
            steps:
              - uses: actions/setup-node@v3
              - run: npm install
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Node.js" in technologies or "npm" in technologies

    def test_detects_docker_workflows(self, viz):
        """Test detection of Docker-related workflows"""
        workflow_content = """
        jobs:
          build:
            steps:
              - uses: docker/build-push-action@v4
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Docker" in technologies


@pytest.mark.integration
class TestEndToEndVisualization:
    """Integration tests for complete visualization workflow"""

    def test_complete_visualization_workflow(self, tmp_path):
        """Test complete workflow from data to dashboard"""
        # Setup
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "workflows": [
                {"name": "ci.yml", "path": ".github/workflows/ci.yml"},
                {"name": "security.yml", "path": ".github/workflows/security.yml"},
            ],
        }
        report_file.write_text(json.dumps(report_data))

        # Execute
        viz = EcosystemVisualizer(report_path=report_file)
        output_path = tmp_path / "dashboard.md"
        dashboard = viz.generate_dashboard(output_path)

        # Verify
        assert dashboard is not None
        assert "test-org" in dashboard
        assert "ci.yml" in dashboard
        assert "security.yml" in dashboard
        output_path.write_text(dashboard)
        assert output_path.exists()


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_handles_malformed_json(self, tmp_path):
        """Test handling of malformed JSON report"""
        report_file = tmp_path / "bad.json"
        report_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            viz = EcosystemVisualizer(report_path=report_file)

    def test_handles_empty_report(self, tmp_path):
        """Test handling of empty report data"""
        report_file = tmp_path / "empty.json"
        report_file.write_text(json.dumps({}))

        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_data == {}

    def test_handles_missing_required_fields(self, tmp_path):
        """Test handling of report missing required fields"""
        report_file = tmp_path / "incomplete.json"
        report_file.write_text(json.dumps({"timestamp": "2024-01-14"}))

        viz = EcosystemVisualizer(report_path=report_file)
        # Should not crash, but may have limited functionality
        assert viz.report_data is not None

#!/usr/bin/env python3
"""Unit tests for ecosystem_visualizer.py
Focus: Diagram generation, workflow categorization, path calculation.
"""

import json
# Import the module under test
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))
from ecosystem_visualizer import EcosystemVisualizer


class TestEcosystemVisualizer:
    """Test EcosystemVisualizer initialization and basic functionality."""

    def test_initializes_without_report_path(self):
        """Test initialization without report data."""
        viz = EcosystemVisualizer()
        assert viz.report_path is None
        assert viz.report_data is None

    def test_initializes_with_valid_report(self, tmp_path):
        """Test initialization with valid report data."""
        report_file = tmp_path / "report.json"
        report_data = {"timestamp": "2024-01-14T00:00:00Z", "workflows": []}
        report_file.write_text(json.dumps(report_data))

        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_path == report_file
        assert viz.report_data == report_data

    def test_handles_missing_report_file(self, tmp_path):
        """Test handling of non-existent report file."""
        report_file = tmp_path / "nonexistent.json"
        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_data is None


class TestWorkflowCategorization:
    """Test workflow categorization logic."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    @pytest.mark.parametrize(
        "workflow_name,expected_emoji",
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
    def test_categorizes_workflow_correctly(self, viz, workflow_name, expected_emoji):
        """Test workflow categorization based on name patterns."""
        # _classify_workflow returns tuple (emoji, category_name)
        emoji, category_name = viz._classify_workflow(workflow_name)
        assert emoji == expected_emoji
        # Verify category_name is also set correctly
        assert category_name == viz.WORKFLOW_CATEGORIES[expected_emoji]

    def test_default_category_for_unknown_workflow(self, viz):
        """Test that unknown workflows get default category."""
        emoji, category_name = viz._classify_workflow("unknown-workflow.yml")
        assert emoji == "⚙️"
        assert category_name == "Utility & Other"


class TestRelativePathCalculation:
    """Test relative path calculation for links."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_calculates_path_from_root(self, viz):
        """Test path calculation when output is at root."""
        output_path = Path("dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == ".github/workflows/"

    def test_calculates_path_from_subdirectory(self, viz):
        """Test path calculation when output is in subdirectory."""
        output_path = Path("reports/dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == "../.github/workflows/"

    def test_calculates_path_from_nested_directory(self, viz):
        """Test path calculation when output is deeply nested."""
        output_path = Path("reports/archives/2024/dashboard.md")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert result == "../../../.github/workflows/"

    def test_handles_current_directory(self, viz):
        """Test path calculation for current directory."""
        output_path = Path(".")
        target = ".github/workflows/"

        result = viz._calculate_relative_path(output_path, target)
        assert target in result


class TestMermaidDiagramGeneration:
    """Test Mermaid diagram generation."""

    @pytest.fixture
    def viz_with_workflows(self, tmp_path):
        """Create visualizer with workflow data."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {
                "workflows": ["ci-test.yml", "security-scan.yml"],
                "copilot_agents": [],
                "copilot_instructions": [],
            },
        }
        report_file.write_text(json.dumps(report_data))
        return EcosystemVisualizer(report_path=report_file)

    def test_generates_basic_diagram(self, viz_with_workflows, tmp_path):
        """Test basic Mermaid diagram generation."""
        output_path = tmp_path / "diagram.md"
        diagram = viz_with_workflows.generate_mermaid_diagram(output_path)

        assert "graph TD" in diagram or "flowchart" in diagram
        assert "ci-test" in diagram
        assert "security-scan" in diagram

    def test_respects_max_workflows_limit(self, tmp_path):
        """Test that diagram respects MAX_DIAGRAM_WORKFLOWS limit."""
        # Create more workflows than the limit
        report_file = tmp_path / "report.json"
        workflows = [f"workflow-{i}.yml" for i in range(15)]  # More than default limit
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {
                "workflows": workflows,
                "copilot_agents": [],
                "copilot_instructions": [],
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram(tmp_path / "diagram.md")

        # Should not include all workflows
        workflow_count = sum(1 for w in workflows if w in diagram)
        assert workflow_count <= viz.MAX_DIAGRAM_WORKFLOWS

    def test_handles_empty_workflow_list(self, tmp_path):
        """Test diagram generation with no workflows."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": [],
                "copilot_instructions": [],
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram(tmp_path / "diagram.md")

        assert diagram is not None
        # Should have basic structure even if empty
        assert "graph TD" in diagram


class TestWorkflowListing:
    """Test workflow listing and organization."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_classifies_workflows_by_category(self, viz):
        """Test workflows are classified correctly by category."""
        workflows = [
            "ci-1.yml",
            "ci-2.yml",
            "security-1.yml",
        ]

        # Use _classify_workflow to group them
        grouped = {}
        for workflow_name in workflows:
            emoji, category_name = viz._classify_workflow(workflow_name)
            if emoji not in grouped:
                grouped[emoji] = []
            grouped[emoji].append(workflow_name)

        assert "🚀" in grouped  # CI category
        assert "🔐" in grouped  # Security category
        assert len(grouped["🚀"]) == 2
        assert len(grouped["🔐"]) == 1

    def test_sorts_categories(self, viz):
        """Test that categories are sorted in expected order."""
        categories = viz.WORKFLOW_CATEGORIES.keys()

        # Should start with safeguards
        assert list(categories)[0] == "🛡️"


class TestDashboardGeneration:
    """Test dashboard markdown generation."""

    @pytest.fixture
    def viz_with_data(self, tmp_path):
        """Create visualizer with sample report data."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {
                "workflows": ["ci-test.yml"],
                "copilot_agents": [],
                "copilot_instructions": [],
                "copilot_prompts": [],
                "copilot_chatmodes": [],
                "technologies": [],
            },
            "metrics": {"total_workflows": 1, "active_workflows": 1},
        }
        report_file.write_text(json.dumps(report_data))
        return EcosystemVisualizer(report_path=report_file)

    def test_generates_dashboard_with_metadata(self, viz_with_data, tmp_path):
        """Test dashboard includes metadata section."""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard_markdown(output_path)

        assert "test-org" in dashboard or "Organization" in dashboard
        assert "2024" in dashboard or "Dashboard" in dashboard

    def test_includes_mermaid_diagram(self, viz_with_data, tmp_path):
        """Test dashboard includes Mermaid diagram."""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard_markdown(output_path)

        assert "```mermaid" in dashboard
        assert "ci-test" in dashboard

    def test_includes_workflow_lists(self, viz_with_data, tmp_path):
        """Test dashboard includes workflow listings."""
        output_path = tmp_path / "dashboard.md"

        dashboard = viz_with_data.generate_dashboard_markdown(output_path)

        assert "ci-test" in dashboard
        assert "Workflow" in dashboard or "🚀" in dashboard


class TestTechnologyDetection:
    """Test technology stack detection."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_detects_python_workflows(self, viz):
        """Test detection of Python-related workflows."""
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
        """Test detection of Node.js-related workflows."""
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
        """Test detection of Docker-related workflows."""
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
    """Integration tests for complete visualization workflow."""

    def test_complete_visualization_workflow(self, tmp_path):
        """Test complete workflow from data to dashboard."""
        # Setup
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {
                "workflows": ["ci.yml", "security.yml"],
                "copilot_agents": [],
                "copilot_instructions": [],
                "copilot_prompts": [],
                "copilot_chatmodes": [],
                "technologies": [],
            },
        }
        report_file.write_text(json.dumps(report_data))

        # Execute
        viz = EcosystemVisualizer(report_path=report_file)
        output_path = tmp_path / "dashboard.md"
        dashboard = viz.generate_dashboard_markdown(output_path)

        # Verify
        assert dashboard is not None
        assert "test-org" in dashboard or "Organization" in dashboard
        assert "ci" in dashboard
        assert "security" in dashboard
        output_path.write_text(dashboard)
        assert output_path.exists()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_handles_malformed_json(self, tmp_path):
        """Test handling of malformed JSON report."""
        report_file = tmp_path / "bad.json"
        report_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            EcosystemVisualizer(report_path=report_file)

    def test_handles_empty_report(self, tmp_path):
        """Test handling of empty report data."""
        report_file = tmp_path / "empty.json"
        report_file.write_text(json.dumps({}))

        viz = EcosystemVisualizer(report_path=report_file)
        assert viz.report_data == {}

    def test_handles_missing_required_fields(self, tmp_path):
        """Test handling of report missing required fields."""
        report_file = tmp_path / "incomplete.json"
        report_file.write_text(json.dumps({"timestamp": "2024-01-14"}))

        viz = EcosystemVisualizer(report_path=report_file)
        # Should not crash, but may have limited functionality
        assert viz.report_data is not None


@pytest.mark.unit
class TestMermaidDiagramCopilot:
    """Test Mermaid diagram generation with Copilot customizations."""

    def test_includes_copilot_agents(self, tmp_path):
        """Test diagram includes Copilot agents section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": ["agent1.agent.md", "agent2.agent.md"],
                "copilot_instructions": [],
                "copilot_prompts": [],
                "copilot_chatmodes": [],
            }
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "AGENTS" in diagram
        assert "2 agents" in diagram

    def test_includes_copilot_instructions(self, tmp_path):
        """Test diagram includes Copilot instructions section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": [],
                "copilot_instructions": ["instr1.md", "instr2.md", "instr3.md"],
                "copilot_prompts": [],
                "copilot_chatmodes": [],
            }
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "INSTR" in diagram
        assert "3 instructions" in diagram

    def test_includes_copilot_prompts(self, tmp_path):
        """Test diagram includes Copilot prompts section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": [],
                "copilot_instructions": [],
                "copilot_prompts": ["prompt1.prompt.md"],
                "copilot_chatmodes": [],
            }
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "PROMPTS" in diagram
        assert "1 prompts" in diagram

    def test_includes_copilot_chatmodes(self, tmp_path):
        """Test diagram includes Copilot chatmodes section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": [],
                "copilot_instructions": [],
                "copilot_prompts": [],
                "copilot_chatmodes": ["mode1.chatmode.md", "mode2.chatmode.md"],
            }
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "CHATMODES" in diagram
        assert "2 modes" in diagram

    def test_includes_technologies(self, tmp_path):
        """Test diagram includes technologies section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "ecosystem_map": {
                "workflows": [],
                "copilot_agents": [],
                "copilot_instructions": [],
                "copilot_prompts": [],
                "copilot_chatmodes": [],
                "technologies": ["Python", "Node.js", "Docker"],
            }
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "Technologies" in diagram
        assert "TECH0" in diagram
        assert "Python" in diagram


@pytest.mark.unit
class TestRenderGroupedSection:
    """Test _render_grouped_section helper."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_groups_by_category(self, viz):
        """Test items are grouped by category."""
        items = [
            {"category": "Security", "severity": "high", "description": "Issue 1"},
            {"category": "Security", "severity": "low", "description": "Issue 2"},
            {"category": "Performance", "severity": "medium", "description": "Issue 3"},
        ]

        parts = viz._render_grouped_section(items)
        result = "".join(parts)

        assert "Security" in result
        assert "Performance" in result
        assert "Issue 1" in result
        assert "Issue 2" in result
        assert "Issue 3" in result

    def test_shows_low_severity(self, viz):
        """Test category shows LOW severity when all items are low."""
        items = [
            {"category": "Minor", "severity": "low", "description": "Minor issue 1"},
            {"category": "Minor", "severity": "low", "description": "Minor issue 2"},
        ]

        parts = viz._render_grouped_section(items)
        result = "".join(parts)

        # Should show LOW since that's the only severity
        assert "LOW" in result
        assert "🟢" in result

    def test_shows_highest_severity(self, viz):
        """Test category shows highest severity among items."""
        items = [
            {"category": "Testing", "severity": "low", "description": "Minor issue"},
            {"category": "Testing", "severity": "critical", "description": "Critical issue"},
        ]

        parts = viz._render_grouped_section(items)
        result = "".join(parts)

        # Should show CRITICAL since that's the highest
        assert "CRITICAL" in result
        assert "🔴" in result

    def test_includes_recommendations(self, viz):
        """Test recommendations are included when present."""
        items = [
            {
                "category": "Docs",
                "severity": "medium",
                "description": "Missing docs",
                "recommendation": "Add README",
            }
        ]

        parts = viz._render_grouped_section(items)
        result = "".join(parts)

        assert "Add README" in result
        assert "💡" in result

    def test_handles_unknown_severity(self, viz):
        """Test handling of unknown severity values."""
        items = [
            {"category": "Unknown", "severity": "unknown", "description": "Test"},
        ]

        parts = viz._render_grouped_section(items)
        result = "".join(parts)

        assert "UNKNOWN" in result
        assert "⚪" in result


@pytest.mark.unit
class TestTechnologyDetectionExpanded:
    """Extended tests for technology detection."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_detects_go(self, viz):
        """Test detection of Go workflows."""
        workflow_content = """
        jobs:
          build:
            steps:
              - uses: actions/setup-go@v4
              - run: go build ./...
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Go" in technologies

    def test_detects_java(self, viz):
        """Test detection of Java workflows."""
        workflow_content = """
        jobs:
          build:
            steps:
              - uses: actions/setup-java@v3
              - run: mvn clean install
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Java" in technologies

    def test_detects_rust(self, viz):
        """Test detection of Rust workflows."""
        workflow_content = """
        jobs:
          build:
            steps:
              - run: cargo build --release
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Rust" in technologies

    def test_detects_terraform(self, viz):
        """Test detection of Terraform workflows."""
        workflow_content = """
        jobs:
          deploy:
            steps:
              - uses: hashicorp/setup-terraform@v2
              - run: terraform plan
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Terraform" in technologies

    def test_detects_multiple_technologies(self, viz):
        """Test detection of multiple technologies in one workflow."""
        workflow_content = """
        jobs:
          test:
            steps:
              - uses: actions/setup-python@v4
              - uses: actions/setup-node@v3
              - run: pip install pytest
              - run: npm install
        """

        technologies = viz._detect_technologies(workflow_content)
        assert "Python" in technologies
        assert "Node.js" in technologies


@pytest.mark.unit
class TestDashboardRepositoryHealth:
    """Test dashboard generation with repository health data."""

    def test_displays_repository_health(self, tmp_path):
        """Test dashboard displays repository health section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {"workflows": []},
            "repository_health": {
                "total_repos": 100,
                "active_repos": 75,
                "stale_repos": 25,
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "75" in dashboard  # active repos
        assert "25" in dashboard  # stale repos
        assert "100" in dashboard  # total
        assert "75.0%" in dashboard  # percentage
        assert "█" in dashboard  # progress bar

    def test_displays_error_when_no_repos(self, tmp_path):
        """Test dashboard handles zero repositories."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "repository_health": {"error": "API rate limited"},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "Data Unavailable" in dashboard or "API rate limited" in dashboard


@pytest.mark.unit
class TestDashboardLinkValidation:
    """Test dashboard generation with link validation data."""

    def test_displays_link_health(self, tmp_path):
        """Test dashboard displays link validation section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "link_validation": {
                "total_links": 200,
                "valid": 180,
                "broken": 20,
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "180" in dashboard  # valid
        assert "20" in dashboard  # broken
        assert "90.0%" in dashboard  # percentage

    def test_displays_broken_links_list(self, tmp_path):
        """Test dashboard displays broken links details."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "link_validation": {
                "total_links": 10,
                "valid": 8,
                "broken": 2,
                "broken_links": [
                    {"url": "https://example.com/404", "status": "404"},
                    {"url": "https://example.com/500", "status": "500"},
                ],
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "example.com/404" in dashboard
        assert "404" in dashboard
        assert "🔴" in dashboard  # 4xx indicator
        assert "💥" in dashboard  # 5xx indicator

    def test_handles_no_link_data(self, tmp_path):
        """Test dashboard handles missing link validation."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "No Data" in dashboard or "skipped" in dashboard


@pytest.mark.unit
class TestDashboardAlerts:
    """Test dashboard generation with alerts."""

    def test_displays_blind_spots(self, tmp_path):
        """Test dashboard displays blind spots section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "blind_spots": [
                {
                    "category": "Testing",
                    "severity": "high",
                    "description": "No unit tests",
                    "recommendation": "Add pytest",
                }
            ],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "Blind Spots" in dashboard
        assert "No unit tests" in dashboard

    def test_displays_shatter_points(self, tmp_path):
        """Test dashboard displays shatter points section."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "shatter_points": [
                {
                    "category": "Security",
                    "severity": "critical",
                    "description": "Exposed secrets",
                }
            ],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "Shatter Points" in dashboard
        assert "Exposed secrets" in dashboard

    def test_no_alerts_shows_healthy(self, tmp_path):
        """Test dashboard shows healthy when no alerts."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "blind_spots": [],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "No alerts" in dashboard or "healthy" in dashboard


@pytest.mark.unit
class TestDashboardTechnologyCoverage:
    """Test dashboard technology coverage section."""

    def test_small_tech_list_as_bullets(self, tmp_path):
        """Test small technology list renders as bullet points."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {
                "workflows": [],
                "technologies": ["Python", "Node.js"],
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "Python" in dashboard
        assert "Node.js" in dashboard

    def test_large_tech_list_as_table(self, tmp_path):
        """Test large technology list renders as collapsible table."""
        report_file = tmp_path / "report.json"
        technologies = ["Python", "Node.js", "Go", "Rust", "Java", "Docker"]
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {
                "workflows": [],
                "technologies": technologies,
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "<details>" in dashboard
        assert "View all" in dashboard
        for tech in technologies:
            assert tech in dashboard


@pytest.mark.unit
class TestHealthBadge:
    """Test health badge generation."""

    def test_excellent_health_badge(self, tmp_path):
        """Test badge for excellent health (80%+)."""
        report_file = tmp_path / "report.json"
        report_data = {
            "repository_health": {"total_repos": 10, "active_repos": 10},
            "link_validation": {"total_links": 10, "valid": 10},
            "blind_spots": [],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        badge = viz.generate_health_badge()

        assert "brightgreen" in badge
        assert "excellent" in badge

    def test_good_health_badge(self, tmp_path):
        """Test badge for good health (60-79%)."""
        report_file = tmp_path / "report.json"
        report_data = {
            "repository_health": {"total_repos": 10, "active_repos": 7},
            "link_validation": {"total_links": 10, "valid": 7},
            "blind_spots": [],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        badge = viz.generate_health_badge()

        assert "green" in badge
        assert "good" in badge

    def test_fair_health_badge(self, tmp_path):
        """Test badge for fair health (40-59%)."""
        report_file = tmp_path / "report.json"
        # Score calculation:
        # - Repo: 5/10 * 40 = 20 points
        # - Links: 5/10 * 30 = 15 points
        # - Alerts: 30 - (2 critical * 10) = 10 points
        # - Total: 45/100 = 45% (fair)
        report_data = {
            "repository_health": {"total_repos": 10, "active_repos": 5},
            "link_validation": {"total_links": 10, "valid": 5},
            "blind_spots": [
                {"severity": "critical", "category": "A", "description": "Issue 1"},
                {"severity": "critical", "category": "B", "description": "Issue 2"},
            ],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        badge = viz.generate_health_badge()

        assert "yellow" in badge
        assert "fair" in badge

    def test_poor_health_badge(self, tmp_path):
        """Test badge for poor health (20-39%)."""
        report_file = tmp_path / "report.json"
        # Score calculation:
        # - Repo: 3/10 * 40 = 12 points
        # - Links: 3/10 * 30 = 9 points
        # - Alerts: 30 - (3 critical * 10) = 0 points (min 0)
        # - Total: 21/100 = 21% (poor)
        report_data = {
            "repository_health": {"total_repos": 10, "active_repos": 3},
            "link_validation": {"total_links": 10, "valid": 3},
            "blind_spots": [
                {"severity": "high", "category": "A", "description": "Issue 1"},
                {"severity": "high", "category": "B", "description": "Issue 2"},
                {"severity": "high", "category": "C", "description": "Issue 3"},
            ],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        badge = viz.generate_health_badge()

        assert "orange" in badge
        assert "poor" in badge

    def test_critical_health_badge(self, tmp_path):
        """Test badge for critical health (<20%)."""
        report_file = tmp_path / "report.json"
        report_data = {
            "repository_health": {"total_repos": 10, "active_repos": 1},
            "link_validation": {"total_links": 10, "valid": 1},
            "blind_spots": [
                {"severity": "critical", "category": "Sec", "description": "Critical1"},
                {"severity": "critical", "category": "Sec", "description": "Critical2"},
                {"severity": "critical", "category": "Sec", "description": "Critical3"},
            ],
            "shatter_points": [],
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        badge = viz.generate_health_badge()

        assert "red" in badge
        assert "critical" in badge

    def test_unknown_health_badge(self):
        """Test badge when no data available."""
        viz = EcosystemVisualizer()

        badge = viz.generate_health_badge()

        assert "unknown" in badge
        assert "lightgrey" in badge


@pytest.mark.unit
class TestDashboardWorkflowListing:
    """Test dashboard active workflows section."""

    def test_displays_workflow_limit_note(self, tmp_path):
        """Test dashboard notes when workflows exceed diagram limit."""
        report_file = tmp_path / "report.json"
        workflows = [f"workflow-{i}.yml" for i in range(20)]
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": workflows},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        # Should mention the limit in the note
        assert str(viz.MAX_DIAGRAM_WORKFLOWS) in dashboard
        assert "20 workflows" in dashboard

    def test_handles_no_workflows(self, tmp_path):
        """Test dashboard handles empty workflow list."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "No active workflows" in dashboard


@pytest.mark.unit
class TestMainFunction:
    """Test main function entry point."""

    def test_no_report_shows_error(self, capsys, monkeypatch):
        """Test main shows error when no report specified."""
        # Mock argparse to return no report
        monkeypatch.setattr("sys.argv", ["ecosystem_visualizer.py"])

        # Import and run main
        from ecosystem_visualizer import main

        main()

        captured = capsys.readouterr()
        assert "No report specified" in captured.out or "❌" in captured.out

    def test_find_latest_with_no_reports_dir(self, capsys, monkeypatch, tmp_path):
        """Test find-latest with missing reports directory."""
        # Change to temp directory where there's no reports/ folder
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["ecosystem_visualizer.py", "--find-latest"])

        from ecosystem_visualizer import main

        main()

        captured = capsys.readouterr()
        assert "not found" in captured.out or "⚠️" in captured.out

    def test_find_latest_with_empty_reports_dir(self, capsys, monkeypatch, tmp_path):
        """Test find-latest with empty reports directory."""
        # Create empty reports directory
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["ecosystem_visualizer.py", "--find-latest"])

        from ecosystem_visualizer import main

        main()

        captured = capsys.readouterr()
        assert "No reports found" in captured.out or "⚠️" in captured.out

    def test_find_latest_with_reports(self, capsys, monkeypatch, tmp_path):
        """Test find-latest finds and uses the latest report."""
        # Create reports directory with a report
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()

        report_file = reports_dir / "org_health_2024-01-15.json"
        report_data = {
            "timestamp": "2024-01-15T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {"workflows": ["test.yml"]},
        }
        report_file.write_text(json.dumps(report_data))

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["ecosystem_visualizer.py", "--find-latest"])

        from ecosystem_visualizer import main

        main()

        captured = capsys.readouterr()
        assert "org_health_2024-01-15.json" in captured.out
        assert "DASHBOARD" in captured.out or "saved" in captured.out


@pytest.mark.unit
class TestRelativePathEdgeCases:
    """Test edge cases for relative path calculation."""

    @pytest.fixture
    def viz(self):
        return EcosystemVisualizer()

    def test_handles_none_output_path(self, viz):
        """Test path calculation with None output path."""
        result = viz._calculate_relative_path(None, ".github/workflows/")
        assert result == "../.github/workflows/"

    def test_handles_absolute_path(self, viz):
        """Test path calculation with absolute output path."""
        output_path = Path("/home/user/project/reports/dashboard.md")
        result = viz._calculate_relative_path(output_path, ".github/workflows/")
        # Should calculate based on depth
        assert "../" in result


@pytest.mark.unit
class TestMermaidDiagramNoData:
    """Test Mermaid diagram edge cases."""

    def test_returns_message_without_ecosystem_map(self, tmp_path):
        """Test diagram returns message when no ecosystem_map."""
        report_file = tmp_path / "report.json"
        report_data = {"timestamp": "2024-01-14T12:00:00Z"}
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        diagram = viz.generate_mermaid_diagram()

        assert "No ecosystem data" in diagram

    def test_returns_message_without_report(self):
        """Test diagram returns message when no report data."""
        viz = EcosystemVisualizer()

        diagram = viz.generate_mermaid_diagram()

        assert "No ecosystem data" in diagram


@pytest.mark.unit
class TestDashboardNoData:
    """Test dashboard generation edge cases."""

    def test_returns_message_without_report(self):
        """Test dashboard returns message when no report data."""
        viz = EcosystemVisualizer()

        dashboard = viz.generate_dashboard_markdown()

        assert "No report data" in dashboard


@pytest.mark.unit
class TestDashboardInvalidTimestamp:
    """Test dashboard with invalid timestamp handling."""

    def test_handles_invalid_timestamp_format(self, tmp_path):
        """Test dashboard handles invalid timestamp gracefully."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "not-a-valid-iso-timestamp",
            "organization": "test-org",
            "ecosystem_map": {"workflows": []},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        # Should not raise, but use the original timestamp string
        dashboard = viz.generate_dashboard_markdown()

        assert "not-a-valid-iso-timestamp" in dashboard
        assert "test-org" in dashboard


@pytest.mark.unit
class TestDashboardBrokenLinksStatusCodes:
    """Test dashboard broken links status code handling."""

    def test_displays_unknown_status_indicator(self, tmp_path):
        """Test dashboard displays warning indicator for non-4xx/5xx status."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "ecosystem_map": {"workflows": []},
            "link_validation": {
                "total_links": 10,
                "valid": 8,
                "broken": 2,
                "broken_links": [
                    {"url": "https://example.com/timeout", "status": "timeout"},
                    {"url": "https://example.com/error", "status": "connection_error"},
                ],
            },
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        # Should show warning indicator for non-4xx/5xx status
        assert "⚠️" in dashboard
        assert "timeout" in dashboard
        assert "connection_error" in dashboard


@pytest.mark.unit
class TestDashboardMissingEcosystemMap:
    """Test dashboard with missing ecosystem_map sections."""

    def test_handles_no_ecosystem_map_for_technologies(self, tmp_path):
        """Test dashboard handles missing ecosystem_map for technologies."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            # No ecosystem_map key
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        dashboard = viz.generate_dashboard_markdown()

        assert "No technology data available" in dashboard
        assert "No workflow data available" in dashboard


@pytest.mark.unit
class TestDashboardWritesToFile:
    """Test dashboard file writing."""

    def test_writes_dashboard_to_output_path(self, tmp_path, capsys):
        """Test dashboard is written to specified output path."""
        report_file = tmp_path / "report.json"
        report_data = {
            "timestamp": "2024-01-14T12:00:00Z",
            "organization": "test-org",
            "ecosystem_map": {"workflows": ["test.yml"]},
        }
        report_file.write_text(json.dumps(report_data))
        viz = EcosystemVisualizer(report_path=report_file)

        output_path = tmp_path / "dashboard.md"
        dashboard = viz.generate_dashboard_markdown(output_path)

        # Check file was written
        assert output_path.exists()
        assert output_path.read_text() == dashboard

        # Check status message was printed
        captured = capsys.readouterr()
        assert "Dashboard saved" in captured.out

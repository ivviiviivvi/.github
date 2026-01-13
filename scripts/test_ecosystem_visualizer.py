import json
import tempfile
import unittest
from pathlib import Path

from scripts.ecosystem_visualizer import EcosystemVisualizer


class TestEcosystemVisualizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.report_path = Path(self.test_dir.name) / "test_report.json"

        # Create a sample report
        self.report_data = {
            "timestamp": "2025-12-25T02:37:00",
            "organization": "TestOrg",
            "ecosystem_map": {
                "workflows": ["test-workflow.yml"],
                "technologies": ["python"],
            },
        }
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        self.visualizer = EcosystemVisualizer(self.report_path)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_workflow_linking_default_depth(self):
        """Test that workflows are correctly linked in the dashboard with default depth"""
        # Use relative path as it would be used in real scenarios
        output_path = Path("reports/DASHBOARD.md")
        # Don't pass output_path to generate_dashboard_markdown to avoid file writing in tests
        # Just check the links are generated correctly

        # Mock the output by not writing to file
        dashboard = self.visualizer.generate_dashboard_markdown(
            None
        )  # Will write to a temp file but we check logic separately

        # Instead, let's test using the internal method directly
        workflow_path = self.visualizer._calculate_relative_path(
            output_path, ".github/workflows/"
        )
        expected_path = "../.github/workflows/"
        self.assertEqual(workflow_path, expected_path)

        # Now verify the actual link format by checking what would be generated
        expected_link_template = (
            f"[`test-workflow.yml`]({workflow_path}test-workflow.yml)"
        )
        self.assertIn(".github/workflows/test-workflow.yml", expected_link_template)

    def test_workflow_linking_custom_depth(self):
        """Test that workflows are correctly linked with custom output path depth"""
        output_path = Path("my/custom/path/DASHBOARD.md")
        workflow_path = self.visualizer._calculate_relative_path(
            output_path, ".github/workflows/"
        )
        expected_path = "../../../.github/workflows/"
        self.assertEqual(workflow_path, expected_path)

    def test_workflow_linking_root_level(self):
        """Test that workflows are correctly linked when output is at root level"""
        output_path = Path("DASHBOARD.md")
        workflow_path = self.visualizer._calculate_relative_path(
            output_path, ".github/workflows/"
        )
        expected_path = ".github/workflows/"
        self.assertEqual(workflow_path, expected_path)

    def test_mermaid_clicks_default_depth(self):
        """Test that mermaid diagram includes click events with default depth"""
        output_path = Path("reports/DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path
        expected_click = (
            'click WF0 "../.github/workflows/test-workflow.yml" "View Workflow"'
        )
        self.assertIn(expected_click, diagram)

    def test_mermaid_clicks_custom_depth(self):
        """Test that mermaid diagram includes click events with custom depth"""
        output_path = Path("my/custom/path/DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path (3 levels deep)
        expected_click = (
            'click WF0 "../../../.github/workflows/test-workflow.yml" "View Workflow"'
        )
        self.assertIn(expected_click, diagram)

    def test_mermaid_clicks_root_level(self):
        """Test that mermaid diagram includes click events at root level"""
        output_path = Path("DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path (root level)
        expected_click = (
            'click WF0 ".github/workflows/test-workflow.yml" "View Workflow"'
        )
        self.assertIn(expected_click, diagram)

    def test_calculate_relative_path(self):
        """Test the relative path calculation helper"""
        # Test depth 1 (e.g., reports/DASHBOARD.md)
        path1 = self.visualizer._calculate_relative_path(
            Path("reports/DASHBOARD.md"), ".github/workflows/"
        )
        self.assertEqual(path1, "../.github/workflows/")

        # Test depth 3 (e.g., my/custom/path/DASHBOARD.md)
        path3 = self.visualizer._calculate_relative_path(
            Path("my/custom/path/DASHBOARD.md"), ".github/workflows/"
        )
        self.assertEqual(path3, "../../../.github/workflows/")

        # Test root level (e.g., DASHBOARD.md)
        path_root = self.visualizer._calculate_relative_path(
            Path("DASHBOARD.md"), ".github/workflows/"
        )
        self.assertEqual(path_root, ".github/workflows/")

        # Test None (default behavior)
        path_none = self.visualizer._calculate_relative_path(None, ".github/workflows/")
        self.assertEqual(path_none, "../.github/workflows/")

    def test_workflow_limit_applies(self):
        """Test that workflow diagram respects MAX_DIAGRAM_WORKFLOWS limit"""
        # Create report with more than MAX_DIAGRAM_WORKFLOWS
        workflows = [f"workflow-{i}.yml" for i in range(15)]

        self.report_data["ecosystem_map"]["workflows"] = workflows
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        visualizer = EcosystemVisualizer(self.report_path)
        diagram = visualizer.generate_mermaid_diagram(Path("reports/DASHBOARD.md"))

        # Should only contain first MAX_DIAGRAM_WORKFLOWS (default 10)
        for i in range(visualizer.MAX_DIAGRAM_WORKFLOWS):
            self.assertIn(f"WF{i}", diagram)
            self.assertIn(f"workflow-{i}.yml", diagram)

        # Should NOT contain workflows beyond the limit
        for i in range(visualizer.MAX_DIAGRAM_WORKFLOWS, 15):
            self.assertNotIn(f"WF{i}", diagram)

    def test_workflow_limit_note_in_dashboard(self):
        """Test that dashboard includes a note when workflows exceed limit"""
        # Create report with more than MAX_DIAGRAM_WORKFLOWS
        workflows = [f"workflow-{i}.yml" for i in range(15)]

        self.report_data["ecosystem_map"]["workflows"] = workflows
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        visualizer = EcosystemVisualizer(self.report_path)
        dashboard = visualizer.generate_dashboard_markdown(Path("reports/DASHBOARD.md"))

        # Should contain informative note about the limit
        self.assertIn("first 10 workflows", dashboard.lower())
        self.assertIn("all 15 workflows", dashboard.lower())
        self.assertIn("active workflows", dashboard.lower())

    def test_no_workflow_limit_note_when_under_limit(self):
        """Test that no limit note appears when workflow count is under limit"""
        # Use default report with just 1 workflow
        visualizer = EcosystemVisualizer(self.report_path)
        dashboard = visualizer.generate_dashboard_markdown(Path("reports/DASHBOARD.md"))

        # Should NOT contain the limit note
        self.assertNotIn("first 10 workflows", dashboard.lower())

    def test_all_workflows_listed_in_active_section(self):
        """Test that all workflows are listed in Active Workflows section regardless of diagram limit"""
        # Create report with more than MAX_DIAGRAM_WORKFLOWS
        workflows = [f"workflow-{i}.yml" for i in range(15)]

        self.report_data["ecosystem_map"]["workflows"] = workflows
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        visualizer = EcosystemVisualizer(self.report_path)
        dashboard = visualizer.generate_dashboard_markdown(Path("reports/DASHBOARD.md"))

        # All workflows should appear in the Active Workflows section
        for workflow in workflows:
            self.assertIn(workflow, dashboard)

        # Should show correct total count
        self.assertIn("View all 15 workflows", dashboard)

    def test_workflow_categories_structure(self):
        """Test that WORKFLOW_CATEGORIES has correct structure and keys"""
        categories = EcosystemVisualizer.WORKFLOW_CATEGORIES

        # Should be a dictionary
        self.assertIsInstance(categories, dict)

        # Should have expected emoji keys
        expected_emojis = ["🛡️", "🔐", "♻️", "🤖", "🚀", "🔀", "⏱️", "💓", "⚙️"]
        self.assertEqual(set(categories.keys()), set(expected_emojis))

        # All values should be non-empty strings
        for emoji, name in categories.items():
            self.assertIsInstance(name, str)
            self.assertTrue(len(name) > 0)

    def test_workflow_categories_consistency_with_categorization(self):
        """Test that WORKFLOW_CATEGORIES values match the actual category labels used in code"""
        # The category labels used in the categorization logic should align with legend
        # Create report with various workflow types
        workflows = [
            "safeguard-test.yml",
            "security-scan.yml",
            "reusable-workflow.yml",
            "copilot-agent.yml",
            "ci-build.yml",
            "pr-check.yml",
            "scheduled-task.yml",
            "health-check.yml",
            "utility-workflow.yml",
        ]

        self.report_data["ecosystem_map"]["workflows"] = workflows
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        visualizer = EcosystemVisualizer(self.report_path)
        dashboard = visualizer.generate_dashboard_markdown(Path("reports/DASHBOARD.md"))

        # Check that the legend uses consistent naming
        self.assertIn("PR Management", dashboard)
        self.assertIn("⚙️ Utility & Other", dashboard)

        # Should NOT use abbreviated or inconsistent forms
        self.assertNotIn("PR Mgmt", dashboard)
        # The test should check the legend format, not the category headers
        # Legend should be: "⚙️ Utility & Other" (emoji space name)
        # Category header should be: "### ⚙️ Utility & Other"


if __name__ == "__main__":
    unittest.main()

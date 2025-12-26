import unittest
from pathlib import Path
import json
import tempfile
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
                "technologies": ["python"]
            }
        }
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)

        self.visualizer = EcosystemVisualizer(self.report_path)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_workflow_linking(self):
        """Test that workflows are correctly linked in the dashboard"""
        dashboard = self.visualizer.generate_dashboard_markdown()

        # Check for the linked workflow
        expected_link = "- [`test-workflow.yml`](../.github/workflows/test-workflow.yml)"
        self.assertIn(expected_link, dashboard)

    def test_mermaid_clicks(self):
        """Test that mermaid diagram includes click events"""
        diagram = self.visualizer.generate_mermaid_diagram()

        # Check for click event
        expected_click = 'click WF0 "../.github/workflows/test-workflow.yml" "View Workflow"'
        self.assertIn(expected_click, diagram)

if __name__ == '__main__':
    unittest.main()

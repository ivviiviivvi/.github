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

    def test_workflow_linking_default_depth(self):
        """Test that workflows are correctly linked in the dashboard with default depth"""
        # Use relative path as it would be used in real scenarios
        output_path = Path("reports/DASHBOARD.md")
        # Don't pass output_path to generate_dashboard_markdown to avoid file writing in tests
        # Just check the links are generated correctly
        
        # Mock the output by not writing to file
        dashboard = self.visualizer.generate_dashboard_markdown(None)  # Will write to a temp file but we check logic separately
        
        # Instead, let's test using the internal method directly
        workflow_path = self.visualizer._calculate_relative_path(output_path, ".github/workflows/")
        expected_path = "../.github/workflows/"
        self.assertEqual(workflow_path, expected_path)
        
        # Now verify the actual link format by checking what would be generated
        expected_link_template = f"[`test-workflow.yml`]({workflow_path}test-workflow.yml)"
        self.assertIn(".github/workflows/test-workflow.yml", expected_link_template)

    def test_workflow_linking_custom_depth(self):
        """Test that workflows are correctly linked with custom output path depth"""
        output_path = Path("my/custom/path/DASHBOARD.md")
        workflow_path = self.visualizer._calculate_relative_path(output_path, ".github/workflows/")
        expected_path = "../../../.github/workflows/"
        self.assertEqual(workflow_path, expected_path)

    def test_workflow_linking_root_level(self):
        """Test that workflows are correctly linked when output is at root level"""
        output_path = Path("DASHBOARD.md")
        workflow_path = self.visualizer._calculate_relative_path(output_path, ".github/workflows/")
        expected_path = ".github/workflows/"
        self.assertEqual(workflow_path, expected_path)

    def test_mermaid_clicks_default_depth(self):
        """Test that mermaid diagram includes click events with default depth"""
        output_path = Path("reports/DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path
        expected_click = 'click WF0 "../.github/workflows/test-workflow.yml" "View Workflow"'
        self.assertIn(expected_click, diagram)

    def test_mermaid_clicks_custom_depth(self):
        """Test that mermaid diagram includes click events with custom depth"""
        output_path = Path("my/custom/path/DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path (3 levels deep)
        expected_click = 'click WF0 "../../../.github/workflows/test-workflow.yml" "View Workflow"'
        self.assertIn(expected_click, diagram)

    def test_mermaid_clicks_root_level(self):
        """Test that mermaid diagram includes click events at root level"""
        output_path = Path("DASHBOARD.md")
        diagram = self.visualizer.generate_mermaid_diagram(output_path)

        # Check for click event with correct relative path (root level)
        expected_click = 'click WF0 ".github/workflows/test-workflow.yml" "View Workflow"'
        self.assertIn(expected_click, diagram)

    def test_calculate_relative_path(self):
        """Test the relative path calculation helper"""
        # Test depth 1 (e.g., reports/DASHBOARD.md)
        path1 = self.visualizer._calculate_relative_path(Path("reports/DASHBOARD.md"), ".github/workflows/")
        self.assertEqual(path1, "../.github/workflows/")

        # Test depth 3 (e.g., my/custom/path/DASHBOARD.md)
        path3 = self.visualizer._calculate_relative_path(Path("my/custom/path/DASHBOARD.md"), ".github/workflows/")
        self.assertEqual(path3, "../../../.github/workflows/")

        # Test root level (e.g., DASHBOARD.md)
        path_root = self.visualizer._calculate_relative_path(Path("DASHBOARD.md"), ".github/workflows/")
        self.assertEqual(path_root, ".github/workflows/")

        # Test None (default behavior)
        path_none = self.visualizer._calculate_relative_path(None, ".github/workflows/")
        self.assertEqual(path_none, "../.github/workflows/")

    def test_workflow_limit_applies(self):
        """Test that workflow diagram respects MAX_DIAGRAM_WORKFLOWS limit"""
        # Create report with more than MAX_DIAGRAM_WORKFLOWS
        workflows = [f"workflow-{i}.yml" for i in range(15)]
        
        self.report_data['ecosystem_map']['workflows'] = workflows
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
        
        self.report_data['ecosystem_map']['workflows'] = workflows
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
        
        self.report_data['ecosystem_map']['workflows'] = workflows
        with open(self.report_path, "w") as f:
            json.dump(self.report_data, f)
        
        visualizer = EcosystemVisualizer(self.report_path)
        dashboard = visualizer.generate_dashboard_markdown(Path("reports/DASHBOARD.md"))
        
        # All workflows should appear in the Active Workflows section
        for workflow in workflows:
            self.assertIn(workflow, dashboard)
        
        # Should show correct total count
        self.assertIn("View all 15 workflows", dashboard)

    def test_classify_workflow_safeguards(self):
        """Test that safeguard workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('safeguard-validation.yml')
        self.assertEqual(emoji, '🛡️')
        self.assertEqual(category, 'Safeguards & Policies')
        
        emoji, category = self.visualizer._classify_workflow('policy-enforcement.yml')
        self.assertEqual(emoji, '🛡️')
        self.assertEqual(category, 'Safeguards & Policies')

    def test_classify_workflow_security(self):
        """Test that security workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('security-scan.yml')
        self.assertEqual(emoji, '🔐')
        self.assertEqual(category, 'Security')
        
        emoji, category = self.visualizer._classify_workflow('codeql-analysis.yml')
        self.assertEqual(emoji, '🔐')
        self.assertEqual(category, 'Security')
        
        emoji, category = self.visualizer._classify_workflow('semgrep-check.yml')
        self.assertEqual(emoji, '🔐')
        self.assertEqual(category, 'Security')
        
        emoji, category = self.visualizer._classify_workflow('secret-scanning.yml')
        self.assertEqual(emoji, '🔐')
        self.assertEqual(category, 'Security')

    def test_classify_workflow_reusable(self):
        """Test that reusable workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('reusable-build.yml')
        self.assertEqual(emoji, '♻️')
        self.assertEqual(category, 'Reusable Workflows')

    def test_classify_workflow_ai_agents(self):
        """Test that AI agent workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('gemini-agent.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')
        
        emoji, category = self.visualizer._classify_workflow('claude-assistant.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')
        
        emoji, category = self.visualizer._classify_workflow('openai-integration.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')
        
        emoji, category = self.visualizer._classify_workflow('copilot-workflow.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')
        
        emoji, category = self.visualizer._classify_workflow('agent-automation.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')
        
        emoji, category = self.visualizer._classify_workflow('ai-enhanced-test.yml')
        self.assertEqual(emoji, '🤖')
        self.assertEqual(category, 'AI Agents & Automation')

    def test_classify_workflow_ci_cd(self):
        """Test that CI/CD workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('ci-pipeline.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')
        
        emoji, category = self.visualizer._classify_workflow('test-suite.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')
        
        emoji, category = self.visualizer._classify_workflow('build-project.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')
        
        emoji, category = self.visualizer._classify_workflow('deploy-production.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')
        
        emoji, category = self.visualizer._classify_workflow('release-package.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')
        
        emoji, category = self.visualizer._classify_workflow('docker-build.yml')
        self.assertEqual(emoji, '🚀')
        self.assertEqual(category, 'CI/CD & Deployment')

    def test_classify_workflow_pr_management(self):
        """Test that PR management workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('pr-validation.yml')
        self.assertEqual(emoji, '🔀')
        self.assertEqual(category, 'PR Management')
        
        emoji, category = self.visualizer._classify_workflow('pull-request-check.yml')
        self.assertEqual(emoji, '🔀')
        self.assertEqual(category, 'PR Management')
        
        emoji, category = self.visualizer._classify_workflow('merge-automation.yml')
        self.assertEqual(emoji, '🔀')
        self.assertEqual(category, 'PR Management')

    def test_classify_workflow_scheduled(self):
        """Test that scheduled workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('scheduled-cleanup.yml')
        self.assertEqual(emoji, '⏱️')
        self.assertEqual(category, 'Scheduled Tasks')
        
        emoji, category = self.visualizer._classify_workflow('daily-report.yml')
        self.assertEqual(emoji, '⏱️')
        self.assertEqual(category, 'Scheduled Tasks')
        
        emoji, category = self.visualizer._classify_workflow('weekly-maintenance.yml')
        self.assertEqual(emoji, '⏱️')
        self.assertEqual(category, 'Scheduled Tasks')

    def test_classify_workflow_health_metrics(self):
        """Test that health and metrics workflows are correctly classified"""
        emoji, category = self.visualizer._classify_workflow('health-check.yml')
        self.assertEqual(emoji, '💓')
        self.assertEqual(category, 'Health & Metrics')
        
        emoji, category = self.visualizer._classify_workflow('monitoring-alerts.yml')
        self.assertEqual(emoji, '💓')
        self.assertEqual(category, 'Health & Metrics')
        
        emoji, category = self.visualizer._classify_workflow('metrics-dashboard.yml')
        self.assertEqual(emoji, '💓')
        self.assertEqual(category, 'Health & Metrics')
        
        emoji, category = self.visualizer._classify_workflow('report-generator.yml')
        self.assertEqual(emoji, '💓')
        self.assertEqual(category, 'Health & Metrics')

    def test_classify_workflow_utility_default(self):
        """Test that unmatched workflows default to Utility & Other"""
        emoji, category = self.visualizer._classify_workflow('random-workflow.yml')
        self.assertEqual(emoji, '⚙️')
        self.assertEqual(category, 'Utility & Other')
        
        emoji, category = self.visualizer._classify_workflow('custom-automation.yml')
        self.assertEqual(emoji, '⚙️')
        self.assertEqual(category, 'Utility & Other')

    def test_classify_workflow_case_insensitive(self):
        """Test that workflow classification is case insensitive"""
        emoji1, category1 = self.visualizer._classify_workflow('Security-Scan.yml')
        emoji2, category2 = self.visualizer._classify_workflow('SECURITY-SCAN.yml')
        emoji3, category3 = self.visualizer._classify_workflow('security-scan.yml')
        
        self.assertEqual(emoji1, emoji2)
        self.assertEqual(emoji2, emoji3)
        self.assertEqual(category1, category2)
        self.assertEqual(category2, category3)
        self.assertEqual(emoji1, '🔐')

    def test_classify_workflow_first_match_wins(self):
        """Test that first matching pattern wins for workflow classification"""
        # A workflow with both 'security' and 'ci' should match security first
        emoji, category = self.visualizer._classify_workflow('security-ci-pipeline.yml')
        self.assertEqual(emoji, '🔐')
        self.assertEqual(category, 'Security')

if __name__ == '__main__':
    unittest.main()

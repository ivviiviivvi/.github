import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

# Add scripts directory to path
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)


class TestWebCrawlerFull(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure secret_manager is mocked if not present
        if "secret_manager" not in sys.modules:
            sys.modules["secret_manager"] = MagicMock()

    def setUp(self):
        import web_crawler

        self.web_crawler = web_crawler

        self.get_secret_patcher = patch("web_crawler.get_secret")
        self.get_secret_patcher.start()

        self.crawler = self.web_crawler.OrganizationCrawler(
            github_token="fake-token", org_name="test-org"
        )
        self.crawler.session = MagicMock()

    def tearDown(self):
        self.get_secret_patcher.stop()

    def test_analyze_repository_health(self):
        """Test repository health analysis."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "name": "active-repo",
                "full_name": "org/active-repo",
                "updated_at": "2025-01-01T00:00:00Z",  # Assume recent
                "stargazers_count": 10,
                "open_issues_count": 2,
            },
            {
                "name": "stale-repo",
                "full_name": "org/stale-repo",
                "updated_at": "2020-01-01T00:00:00Z",  # Old
                "stargazers_count": 0,
                "open_issues_count": 0,
            },
        ]
        self.crawler.session.get.return_value = mock_response

        # Mock datetime to control "now"
        with patch("web_crawler.datetime") as mock_datetime:
            # Re-implement datetime.fromisoformat since we are mocking the class
            from datetime import datetime as real_datetime, timezone

            mock_datetime.fromisoformat.side_effect = (
                lambda d: real_datetime.fromisoformat(d)
            )

            mock_now = real_datetime(2025, 1, 30, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now

            health = self.crawler.analyze_repository_health()

            self.assertEqual(health["total_repos"], 2)
            self.assertEqual(health["active_repos"], 1)
            self.assertEqual(health["stale_repos"], 1)

    def test_map_ecosystem(self):
        """Test ecosystem mapping."""
        # Mock Path methods
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.glob") as mock_glob,
        ):

            # Setup glob returns for different directories
            def glob_side_effect(pattern):
                if pattern == "*.yml":  # workflows
                    return [Path(".github/workflows/ci.yml")]
                if pattern == "*.md":  # agents/instructions
                    return [Path("agents/coder.md")]
                return []

            mock_glob.side_effect = glob_side_effect

            ecosystem = self.crawler.map_ecosystem(Path("."))

            self.assertIn("ci.yml", ecosystem["workflows"])
            self.assertIn("coder", ecosystem["copilot_agents"])

    def test_identify_blind_spots(self):
        """Test blind spot identification."""
        ecosystem = {"workflows": ["ci.yml"]}  # < 5 workflows
        health = {
            "repositories": [
                {"name": "stale-1", "is_active": False},
                {"name": "active-1", "is_active": True},
            ]
        }

        blind_spots = self.crawler.identify_blind_spots(ecosystem, health)

        categories = [b["category"] for b in blind_spots]
        self.assertIn("Stale Repositories", categories)
        self.assertIn("CI/CD Coverage", categories)

    def test_identify_shatter_points(self):
        """Test shatter point identification."""
        ecosystem = {
            "workflows": ["ci.yml"]
        }  # Missing security-scan.yml, deployment.yml

        shatter_points = self.crawler.identify_shatter_points(ecosystem)

        descriptions = [s["description"] for s in shatter_points]
        self.assertTrue(any("security-scan.yml" in d for d in descriptions))

    def test_generate_report(self):
        """Test report generation."""
        self.crawler.results = {
            "timestamp": "2025-01-30",
            "organization": "test-org",
            "link_validation": {"total_links": 10},
            "repository_health": {"total_repos": 5},
            "ecosystem_map": {"workflows": []},
            "blind_spots": [{"category": "Test"}],
            "shatter_points": [],
        }

        with patch("builtins.open", mock_open()) as mock_file:
            with patch("pathlib.Path.mkdir"):
                with patch("pathlib.Path.write_text") as mock_write_text:
                    report_path = self.crawler.generate_report(Path("reports"))

                    self.assertTrue(str(report_path).endswith(".json"))
                    mock_file.assert_called()  # JSON write
                    mock_write_text.assert_called()  # Markdown write

    def test_run_full_analysis(self):
        """Test full analysis orchestration."""
        with (
            patch.object(self.crawler, "map_ecosystem") as mock_map,
            patch.object(self.crawler, "analyze_repository_health") as mock_health,
            patch.object(self.crawler, "crawl_markdown_files") as mock_crawl,
            patch.object(self.crawler, "validate_links") as mock_validate,
            patch.object(self.crawler, "identify_blind_spots") as mock_blind,
            patch.object(self.crawler, "identify_shatter_points") as mock_shatter,
            patch.object(self.crawler, "generate_report") as mock_report,
        ):

            self.crawler.run_full_analysis(Path("."), validate_external_links=True)

            mock_map.assert_called()
            mock_health.assert_called()
            mock_crawl.assert_called()
            mock_validate.assert_called()
            mock_blind.assert_called()
            mock_shatter.assert_called()
            mock_report.assert_called()

    def test_main(self):
        """Test main function."""
        # Patch OrganizationCrawler on the imported module
        with patch("web_crawler.OrganizationCrawler") as MockCrawler:
            mock_instance = MockCrawler.return_value
            mock_instance.run_full_analysis.return_value = {
                "ecosystem_map": {},
                "repository_health": {},
            }

            with patch("sys.argv", ["web_crawler.py", "--org-name", "test-org"]):
                self.web_crawler.main()

            mock_instance.run_full_analysis.assert_called()


if __name__ == "__main__":
    unittest.main()

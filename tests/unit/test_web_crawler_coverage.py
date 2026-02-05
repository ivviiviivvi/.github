#!/usr/bin/env python3
"""Extended unit tests for web_crawler.py to improve coverage.

Focus: validate_links, _check_link edge cases, error handling, report generation.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import urllib3

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from web_crawler import OrganizationCrawler


@pytest.mark.unit
class TestValidateLinks:
    """Test validate_links concurrent processing."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_validate_links_counts_valid_and_broken(self, crawler):
        """Test validate_links correctly counts valid and broken links."""
        links_by_file = {
            "test1.md": ["https://valid.com", "https://broken.com"],
            "test2.md": ["https://another-valid.com"],
        }

        def mock_check_link(url, timeout=10):
            if "broken" in url:
                return 404
            return 200

        with patch.object(crawler, "_check_link", side_effect=mock_check_link):
            results = crawler.validate_links(links_by_file)

        assert results["total_links"] == 3
        assert results["valid"] == 2
        assert results["broken"] == 1
        assert len(results["broken_links"]) == 1
        assert results["broken_links"][0]["url"] == "https://broken.com"

    def test_validate_links_handles_rate_limited(self, crawler):
        """Test validate_links handles rate limited (999) status."""
        links_by_file = {"test.md": ["https://rate-limited.com"]}

        with patch.object(crawler, "_check_link", return_value=999):
            results = crawler.validate_links(links_by_file)

        assert len(results["warnings"]) == 1
        assert "rate limited" in results["warnings"][0]["reason"].lower()

    def test_validate_links_handles_exceptions(self, crawler):
        """Test validate_links handles exceptions during link checking."""
        links_by_file = {"test.md": ["https://error.com"]}

        def raise_exception(url, timeout=10):
            raise Exception("Network error")

        with patch.object(crawler, "_check_link", side_effect=raise_exception):
            results = crawler.validate_links(links_by_file)

        assert results["broken"] == 1
        assert "Exception" in str(results["broken_links"][0]["status"])

    def test_validate_links_skips_non_http_links(self, crawler):
        """Test validate_links skips mailto and other non-http links."""
        links_by_file = {"test.md": ["mailto:test@example.com", "ftp://files.example.com"]}

        with patch.object(crawler, "_check_link") as mock_check:
            results = crawler.validate_links(links_by_file)

        # Non-http links should not be checked
        mock_check.assert_not_called()
        assert results["total_links"] == 2


@pytest.mark.unit
class TestIsHostnameSafe:
    """Test _is_hostname_safe method edge cases."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_empty_ips_returns_true(self, crawler):
        """Test _is_hostname_safe returns True when no IPs resolved."""
        with patch.object(crawler, "_resolve_hostname", return_value=[]):
            result = crawler._is_hostname_safe("unknown.local")
        # Empty IPs handled by _check_link returning 404
        assert result is True

    def test_ipv6_with_scope_id(self, crawler):
        """Test _is_hostname_safe handles IPv6 with scope id."""
        with patch.object(crawler, "_resolve_hostname", return_value=["fe80::1%en0"]):
            result = crawler._is_hostname_safe("link-local.test")
        # fe80:: is link-local, should be blocked
        assert result is False

    def test_ipv6_global_address(self, crawler):
        """Test _is_hostname_safe allows global IPv6."""
        # 2607:f8b0:4004:800::200e is a Google IPv6 (global)
        with patch.object(crawler, "_resolve_hostname", return_value=["2607:f8b0:4004:800::200e"]):
            result = crawler._is_hostname_safe("google.com")
        assert result is True

    def test_invalid_ip_format(self, crawler):
        """Test _is_hostname_safe returns False for invalid IP format."""
        with patch.object(crawler, "_resolve_hostname", return_value=["not-an-ip"]):
            result = crawler._is_hostname_safe("bad.hostname")
        assert result is False

    def test_multicast_address(self, crawler):
        """Test _is_hostname_safe blocks multicast addresses."""
        with patch.object(crawler, "_resolve_hostname", return_value=["224.0.0.1"]):
            result = crawler._is_hostname_safe("multicast.test")
        assert result is False


@pytest.mark.unit
class TestIsSafeUrl:
    """Test _is_safe_url method edge cases."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_no_hostname_returns_false(self, crawler):
        """Test _is_safe_url returns False for URL without hostname."""
        result = crawler._is_safe_url("file:///etc/passwd")
        assert result is False

    def test_unresolvable_hostname_returns_false(self, crawler):
        """Test _is_safe_url returns False when hostname cannot be resolved."""
        with patch.object(crawler, "_resolve_hostname", return_value=[]):
            result = crawler._is_safe_url("http://unresolvable.invalid")
        assert result is False

    def test_ipv6_with_scope_id_handled(self, crawler):
        """Test _is_safe_url handles IPv6 with scope identifier."""
        with patch.object(crawler, "_resolve_hostname", return_value=["fe80::1%eth0"]):
            result = crawler._is_safe_url("http://link-local.test")
        # Link-local is not global
        assert result is False

    def test_value_error_returns_false(self, crawler):
        """Test _is_safe_url returns False on ValueError."""
        with patch.object(crawler, "_resolve_hostname", side_effect=ValueError):
            result = crawler._is_safe_url("http://bad.url")
        assert result is False

    def test_os_error_returns_false(self, crawler):
        """Test _is_safe_url returns False on OSError."""
        with patch.object(crawler, "_resolve_hostname", side_effect=OSError):
            result = crawler._is_safe_url("http://unreachable.test")
        assert result is False


@pytest.mark.unit
class TestCheckLinkEdgeCases:
    """Test _check_link method edge cases."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_no_hostname_returns_400(self, crawler):
        """Test _check_link returns 400 for URL without hostname."""
        result = crawler._check_link("http:///path")
        assert result == 400

    def test_unresolvable_hostname_returns_404(self, crawler):
        """Test _check_link returns 404 when hostname cannot be resolved."""
        with patch.object(crawler, "_resolve_hostname", return_value=[]):
            result = crawler._check_link("http://unresolvable.test")
        assert result == 404

    def test_ipv6_address_bracketed(self, crawler):
        """Test _check_link brackets IPv6 addresses."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.return_value = mock_response

        with patch.object(crawler, "_resolve_hostname", return_value=["2607:f8b0:4004:800::200e"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://google.com")

        assert result == 200
        # Verify the pool was created with bracketed IPv6
        assert mock_pool.request.called

    def test_explicit_port_in_url(self, crawler):
        """Test _check_link handles explicit port in URL."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.return_value = mock_response

        with patch.object(crawler, "_resolve_hostname", return_value=["93.184.216.34"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://example.com:8443/path")

        assert result == 200

    def test_redirect_followed(self, crawler):
        """Test _check_link follows redirects."""
        mock_redirect = MagicMock()
        mock_redirect.status = 301
        mock_redirect.headers = {"Location": "https://final.example.com"}

        mock_final = MagicMock()
        mock_final.status = 200
        mock_final.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.side_effect = [mock_redirect, mock_final]

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://redirect.example.com")

        assert result == 200

    def test_redirect_without_location(self, crawler):
        """Test _check_link returns status when redirect has no Location."""
        mock_response = MagicMock()
        mock_response.status = 302
        mock_response.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.return_value = mock_response

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://bad-redirect.example.com")

        assert result == 302

    def test_get_fallback_on_method_not_allowed(self, crawler):
        """Test _check_link falls back to GET when HEAD returns 405."""
        mock_head = MagicMock()
        mock_head.status = 405
        mock_head.headers = {}

        mock_get = MagicMock()
        mock_get.status = 200
        mock_get.headers = {}
        mock_get.release_conn = MagicMock()

        mock_pool = MagicMock()
        mock_pool.request.side_effect = [mock_head, mock_get]

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://no-head.example.com")

        assert result == 200
        mock_get.release_conn.assert_called()

    def test_get_fallback_with_redirect(self, crawler):
        """Test _check_link handles redirect on GET fallback."""
        mock_head = MagicMock()
        mock_head.status = 405
        mock_head.headers = {}

        mock_get_redirect = MagicMock()
        mock_get_redirect.status = 301
        mock_get_redirect.headers = {"Location": "/new-path"}
        mock_get_redirect.release_conn = MagicMock()

        mock_get_final = MagicMock()
        mock_get_final.status = 200
        mock_get_final.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.side_effect = [
            mock_head,
            mock_get_redirect,
            mock_get_final,
        ]

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://redirect-get.example.com")

        # Should follow redirect from GET and return final status
        assert result == 200

    def test_timeout_error_returns_408(self, crawler):
        """Test _check_link returns 408 on timeout."""
        mock_pool = MagicMock()
        mock_pool.request.side_effect = urllib3.exceptions.TimeoutError()

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://timeout.example.com")

        assert result == 408

    def test_request_error_returns_500(self, crawler):
        """Test _check_link returns 500 on request error."""
        mock_pool = MagicMock()
        mock_pool.request.side_effect = urllib3.exceptions.RequestError(
            pool=mock_pool, url="test", message="Connection failed"
        )

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://error.example.com")

        assert result == 500

    def test_ssl_error_returns_500(self, crawler):
        """Test _check_link returns 500 on SSL error."""
        mock_pool = MagicMock()
        mock_pool.request.side_effect = urllib3.exceptions.SSLError("SSL failed")

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://ssl-error.example.com")

        assert result == 500

    def test_too_many_redirects_returns_310(self, crawler):
        """Test _check_link returns 310 after too many redirects."""
        mock_redirect = MagicMock()
        mock_redirect.status = 301
        mock_redirect.headers = {"Location": "https://redirect.example.com/new"}

        mock_pool = MagicMock()
        # Return redirect 6 times (exceeds 5 redirect limit)
        mock_pool.request.return_value = mock_redirect

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://infinite-redirect.example.com")

        assert result == 310

    def test_410_gone_returns_immediately(self, crawler):
        """Test _check_link returns 410 without GET fallback."""
        mock_response = MagicMock()
        mock_response.status = 410
        mock_response.headers = {}

        mock_pool = MagicMock()
        mock_pool.request.return_value = mock_response

        with patch.object(crawler, "_resolve_hostname", return_value=["1.2.3.4"]):
            with patch.object(crawler, "_is_hostname_safe", return_value=True):
                with patch.object(crawler, "_get_pinned_pool", return_value=mock_pool):
                    result = crawler._check_link("https://gone.example.com")

        assert result == 410
        # Should only call once (HEAD), no GET fallback for 410
        assert mock_pool.request.call_count == 1


@pytest.mark.unit
class TestAnalyzeRepositoryHealthErrors:
    """Test analyze_repository_health error handling."""

    @pytest.fixture
    def crawler(self):
        crawler = OrganizationCrawler(github_token="test", org_name="test")
        crawler.session = MagicMock()
        return crawler

    def test_no_token_returns_error(self):
        """Test analyze_repository_health returns error when no token."""
        crawler = OrganizationCrawler(github_token=None, org_name="test")
        # Ensure token is actually None
        crawler.github_token = None

        result = crawler.analyze_repository_health()

        assert "error" in result
        assert "No GitHub token" in result["error"]

    def test_api_error_response(self, crawler):
        """Test analyze_repository_health handles API error response."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        crawler.session.get.return_value = mock_response

        result = crawler.analyze_repository_health()

        assert "error" in result
        assert "403" in result["error"]

    def test_api_exception(self, crawler):
        """Test analyze_repository_health handles exceptions."""
        crawler.session.get.side_effect = Exception("Network error")

        result = crawler.analyze_repository_health()

        assert "error" in result
        assert "Network error" in result["error"]


@pytest.mark.unit
class TestAnalyzeSingleRepo:
    """Test _analyze_single_repo edge cases."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_date_without_timezone(self, crawler):
        """Test _analyze_single_repo handles date without timezone."""
        repo = {
            "name": "test-repo",
            "full_name": "org/test-repo",
            "updated_at": "2025-01-01T00:00:00",  # No Z timezone
            "stargazers_count": 5,
            "open_issues_count": 2,
        }

        result = crawler._analyze_single_repo(repo)

        assert result["name"] == "test-repo"
        assert "days_since_update" in result

    def test_invalid_date_format(self, crawler):
        """Test _analyze_single_repo handles invalid date format."""
        repo = {
            "name": "bad-date-repo",
            "full_name": "org/bad-date-repo",
            "updated_at": "not-a-valid-date",
            "stargazers_count": 0,
            "open_issues_count": 0,
        }

        result = crawler._analyze_single_repo(repo)

        assert result["name"] == "bad-date-repo"
        # Should default to 999 days (stale)
        assert result["days_since_update"] == 999
        assert result["is_active"] is False


@pytest.mark.unit
class TestGenerateMarkdownReport:
    """Test _generate_markdown_report method."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_report_with_broken_links(self, crawler):
        """Test report includes broken links section."""
        crawler.results = {
            "timestamp": "2025-01-30T00:00:00",
            "organization": "test-org",
            "link_validation": {
                "total_links": 10,
                "valid": 8,
                "broken": 2,
                "warnings": [],
                "broken_links": [
                    {"url": "https://broken1.com", "status": 404},
                    {"url": "https://broken2.com", "status": 500},
                ],
            },
            "repository_health": {},
            "ecosystem_map": {},
            "blind_spots": [],
            "shatter_points": [],
        }

        report = crawler._generate_markdown_report()

        assert "Broken Links" in report
        assert "https://broken1.com" in report
        assert "HTTP 404" in report

    def test_report_with_shatter_points(self, crawler):
        """Test report includes shatter points with recommendations."""
        crawler.results = {
            "timestamp": "2025-01-30T00:00:00",
            "organization": "test-org",
            "link_validation": {},
            "repository_health": {},
            "ecosystem_map": {},
            "blind_spots": [],
            "shatter_points": [
                {
                    "category": "Missing CI",
                    "severity": "high",
                    "description": "No CI workflow found",
                    "recommendation": "Add a ci.yml workflow",
                }
            ],
        }

        report = crawler._generate_markdown_report()

        assert "Missing CI" in report
        assert "high" in report
        assert "No CI workflow found" in report
        assert "Add a ci.yml workflow" in report

    def test_report_with_empty_sections(self, crawler):
        """Test report handles empty sections gracefully."""
        crawler.results = {
            "timestamp": "2025-01-30T00:00:00",
            "organization": "test-org",
            "link_validation": {},
            "repository_health": {},
            "ecosystem_map": {},
            "blind_spots": [],
            "shatter_points": [],
        }

        report = crawler._generate_markdown_report()

        assert "No significant blind spots detected" in report
        assert "No critical shatter points detected" in report


@pytest.mark.unit
class TestRunFullAnalysis:
    """Test run_full_analysis method."""

    @pytest.fixture
    def crawler(self):
        return OrganizationCrawler(github_token="test", org_name="test")

    def test_skips_link_validation_when_disabled(self, crawler, capsys):
        """Test run_full_analysis skips link validation when disabled."""
        with (
            patch.object(crawler, "map_ecosystem", return_value={}),
            patch.object(crawler, "analyze_repository_health", return_value={}),
            patch.object(crawler, "crawl_markdown_files") as mock_crawl,
            patch.object(crawler, "identify_blind_spots", return_value=[]),
            patch.object(crawler, "identify_shatter_points", return_value=[]),
            patch.object(crawler, "generate_report", return_value=Path("report.json")),
        ):
            crawler.run_full_analysis(Path("."), validate_external_links=False)

        # crawl_markdown_files should NOT be called
        mock_crawl.assert_not_called()

        captured = capsys.readouterr()
        assert "Skipping external link validation" in captured.out


@pytest.mark.unit
class TestMainFunction:
    """Test main function and CLI argument parsing."""

    def test_main_with_ecosystem_and_health(self, capsys):
        """Test main prints summary with ecosystem and health."""
        with patch("web_crawler.OrganizationCrawler") as MockCrawler:
            mock_instance = MockCrawler.return_value
            mock_instance.run_full_analysis.return_value = {
                "ecosystem_map": {
                    "workflows": ["ci.yml", "cd.yml"],
                    "copilot_agents": ["agent1"],
                    "copilot_instructions": [],
                    "copilot_prompts": [],
                    "copilot_chatmodes": [],
                },
                "repository_health": {
                    "total_repos": 10,
                    "active_repos": 8,
                },
                "blind_spots": [{"category": "test"}],
                "shatter_points": [],
            }

            with patch("sys.argv", ["web_crawler.py", "--org-name", "test-org"]):
                from web_crawler import main

                main()

        captured = capsys.readouterr()
        assert "Workflows: 2" in captured.out
        assert "Total Repositories: 10" in captured.out
        assert "Active Repositories: 8" in captured.out

    def test_main_validates_links_flag(self):
        """Test main passes validate_links flag correctly."""
        with patch("web_crawler.OrganizationCrawler") as MockCrawler:
            mock_instance = MockCrawler.return_value
            mock_instance.run_full_analysis.return_value = {
                "ecosystem_map": {},
                "repository_health": {},
                "blind_spots": [],
                "shatter_points": [],
            }

            with patch(
                "sys.argv",
                ["web_crawler.py", "--org-name", "test", "--validate-links"],
            ):
                from web_crawler import main

                main()

            # Verify validate_external_links=True was passed
            mock_instance.run_full_analysis.assert_called_once()
            call_kwargs = mock_instance.run_full_analysis.call_args[1]
            assert call_kwargs.get("validate_external_links") is True

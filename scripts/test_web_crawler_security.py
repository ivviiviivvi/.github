import unittest
from unittest.mock import MagicMock, patch
from web_crawler import OrganizationCrawler

class TestWebCrawlerSecurity(unittest.TestCase):
    def setUp(self):
        self.crawler = OrganizationCrawler()
        self.crawler.session = MagicMock()

    def test_ssrf_protection_private_ip(self):
        """Verify that private IPs are blocked."""
        url = "http://169.254.169.254/latest/meta-data/"
        # We expect _check_link to return 403 and NOT call session.head
        status = self.crawler._check_link(url)
        self.assertEqual(status, 403)
        self.crawler.session.head.assert_not_called()

    def test_ssrf_protection_localhost(self):
        """Verify that localhost is blocked."""
        url = "http://localhost:8080/admin"
        status = self.crawler._check_link(url)
        self.assertEqual(status, 403)
        self.crawler.session.head.assert_not_called()

    @patch('socket.getaddrinfo')
    def test_ssrf_protection_public_ip(self, mock_getaddrinfo):
        """Verify that public IPs are allowed."""
        url = "http://example.com"

        # Mock getaddrinfo to return a public IP (e.g., 93.184.216.34)
        mock_getaddrinfo.return_value = [(2, 1, 6, '', ('93.184.216.34', 80))]

        # Mock session.head to return 200
        self.crawler.session.head.return_value.status_code = 200

        status = self.crawler._check_link(url)
        self.assertEqual(status, 200)
        self.crawler.session.head.assert_called()

if __name__ == '__main__':
    unittest.main()

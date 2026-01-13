import os
import socket
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add scripts directory to path to import web_crawler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_crawler import OrganizationCrawler


class TestSSRFProtection(unittest.TestCase):
    def setUp(self):
        self.crawler = OrganizationCrawler()

    @patch("socket.getaddrinfo")
    @patch("urllib3.PoolManager.request")
    def test_blocks_private_ips(self, mock_request, mock_getaddrinfo):
        # Mock DNS resolution to return a private IP
        # Format: list of (family, type, proto, canonname, sockaddr)
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.168.1.1", 80))
        ]

        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_request.return_value = mock_response

        # Test URL that resolves to private IP
        url = "http://internal-service.local/admin"

        print(f"\nTesting URL: {url} (resolves to private IP)")

        # Call the method
        status = self.crawler._check_link(url)

        if mock_request.called:
            print("❌ VULNERABLE: Request was attempted to private IP!")
            self.fail("SSRF Vulnerability detected: Request attempted to private IP")
        else:
            print("✅ SECURE: Request was blocked.")

    @patch("socket.getaddrinfo")
    @patch("urllib3.PoolManager.request")
    def test_blocks_mixed_ips(self, mock_request, mock_getaddrinfo):
        """Test that if a domain resolves to multiple IPs (safe and unsafe), it is blocked."""
        # Mock DNS resolution to return one public and one private IP
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 80)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.168.1.1", 80)),
        ]

        mock_response = MagicMock()
        mock_response.status = 200
        mock_request.return_value = mock_response

        url = "http://mixed-records.local"
        print(f"\nTesting URL: {url} (resolves to mixed IPs)")

        status = self.crawler._check_link(url)

        if mock_request.called:
            print("❌ VULNERABLE: Request was attempted to mixed IPs (one private)!")
            self.fail("SSRF Vulnerability detected: Request attempted to mixed IPs")
        else:
            print("✅ SECURE: Mixed IP request was blocked.")

    @patch("socket.getaddrinfo")
    @patch("urllib3.HTTPConnectionPool.request")
    def test_allows_public_ips(self, mock_request, mock_getaddrinfo):
        # Mock DNS resolution to return a public IP
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 80))
        ]

        mock_response = MagicMock()
        mock_response.status = 200
        mock_request.return_value = mock_response

        url = "http://google.com"
        print(f"\nTesting URL: {url} (resolves to public IP)")

        status = self.crawler._check_link(url)

        if mock_request.called:
            print("✅ CORRECT: Request was allowed for public IP.")
        else:
            print("❌ BROKEN: Public IP request was blocked!")
            self.fail("Public IP request was blocked")


if __name__ == "__main__":
    unittest.main()

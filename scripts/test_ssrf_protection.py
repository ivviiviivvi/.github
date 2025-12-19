import unittest
import sys
import os
import socket
from unittest.mock import patch, MagicMock

# Add scripts directory to path to import web_crawler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_crawler import OrganizationCrawler

class TestSSRFProtection(unittest.TestCase):
    def setUp(self):
        self.crawler = OrganizationCrawler()

    @patch('socket.getaddrinfo')
    @patch('requests.Session.head')
    @patch('requests.Session.get')
    def test_blocks_private_ips(self, mock_get, mock_head, mock_getaddrinfo):
        # Mock DNS resolution to return a private IP
        # Format: list of (family, type, proto, canonname, sockaddr)
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('192.168.1.1', 80))
        ]

        # Mock requests to return success (if they were called)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        mock_get.return_value = mock_response

        # Test URL that resolves to private IP
        url = "http://internal-service.local/admin"

        print(f"\nTesting URL: {url} (resolves to private IP)")

        # Call the method
        status = self.crawler._check_link(url)

        if mock_head.called or mock_get.called:
            print("❌ VULNERABLE: Request was attempted to private IP!")
            self.fail("SSRF Vulnerability detected: Request attempted to private IP")
        else:
            print("✅ SECURE: Request was blocked.")

    @patch('socket.getaddrinfo')
    @patch('requests.Session.head')
    @patch('requests.Session.get')
    def test_allows_public_ips(self, mock_get, mock_head, mock_getaddrinfo):
        # Mock DNS resolution to return a public IP
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('8.8.8.8', 80))
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        url = "http://google.com"
        print(f"\nTesting URL: {url} (resolves to public IP)")

        status = self.crawler._check_link(url)

        if mock_head.called:
            print("✅ CORRECT: Request was allowed for public IP.")
        else:
            print("❌ BROKEN: Public IP request was blocked!")
            self.fail("Public IP request was blocked")

    @patch('socket.getaddrinfo')
    def test_blocks_mixed_ips(self, mock_getaddrinfo):
        """Verify that if ANY resolved IP is private, it is blocked (DNS Rebinding/Dual-stack protection)"""
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('8.8.8.8', 80)),      # Public
            (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('192.168.1.1', 80))   # Private
        ]

        print(f"\nTesting URL: http://risky.com (resolves to mixed IPs)")
        result = self.crawler._is_safe_url("http://risky.com")
        self.assertFalse(result, "Should return False if any resolved IP is private")

    @patch('socket.getaddrinfo')
    def test_blocks_ipv6_private(self, mock_getaddrinfo):
        """Verify that IPv6 private addresses are blocked"""
        mock_getaddrinfo.return_value = [
            (socket.AF_INET6, socket.SOCK_STREAM, 6, '', ('::1', 80, 0, 0))
        ]

        print(f"\nTesting URL: http://localhost6 (resolves to IPv6 loopback)")
        result = self.crawler._is_safe_url("http://localhost6")
        self.assertFalse(result, "Should return False for IPv6 loopback")

if __name__ == '__main__':
    unittest.main()

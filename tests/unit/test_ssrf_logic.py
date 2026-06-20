import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

import web_crawler

# Import the module under test


class TestSSRFLogic(unittest.TestCase):
    def setUp(self):
        # Initialize crawler with dummy values to avoid API calls or env var
        # issues
        self.crawler = web_crawler.OrganizationCrawler(github_token="dummy", org_name="dummy")

    @patch("socket.getaddrinfo")
    def test_is_safe_url(self, mock_getaddrinfo):
        def resolve_to(ip_address):
            mock_getaddrinfo.return_value = [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip_address, 80)),
            ]

        # Case 1: Safe Public IP
        resolve_to("8.8.8.8")
        self.assertTrue(self.crawler._is_safe_url("http://google.com"))

        # Case 2: Private IP (10.x)
        resolve_to("10.0.0.1")
        self.assertFalse(self.crawler._is_safe_url("http://internal.corp"))

        # Case 3: Loopback
        resolve_to("127.0.0.1")
        self.assertFalse(self.crawler._is_safe_url("http://localhost"))

        # Case 4: Cloud Metadata (169.254)
        resolve_to("169.254.169.254")
        self.assertFalse(self.crawler._is_safe_url("http://169.254.169.254"))


if __name__ == "__main__":
    unittest.main()

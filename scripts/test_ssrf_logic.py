import unittest
from unittest.mock import patch, MagicMock
import socket
import ipaddress
import urllib.parse
import sys
import os

# Add scripts directory to path to handle imports correctly regardless of where test is run
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the module under test
import web_crawler

class TestSSRFLogic(unittest.TestCase):
    def setUp(self):
        # Initialize crawler with dummy values to avoid API calls or env var issues
        self.crawler = web_crawler.OrganizationCrawler(github_token="dummy", org_name="dummy")

    @patch('socket.gethostbyname')
    def test_is_safe_url(self, mock_gethostbyname):
        # Case 1: Safe Public IP
        mock_gethostbyname.return_value = "8.8.8.8"
        self.assertTrue(self.crawler._is_safe_url("http://google.com"))

        # Case 2: Private IP (10.x)
        mock_gethostbyname.return_value = "10.0.0.1"
        self.assertFalse(self.crawler._is_safe_url("http://internal.corp"))

        # Case 3: Loopback
        mock_gethostbyname.return_value = "127.0.0.1"
        self.assertFalse(self.crawler._is_safe_url("http://localhost"))

        # Case 4: Cloud Metadata (169.254)
        mock_gethostbyname.return_value = "169.254.169.254"
        self.assertFalse(self.crawler._is_safe_url("http://169.254.169.254"))

if __name__ == '__main__':
    unittest.main()

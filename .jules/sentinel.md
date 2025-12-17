## 2025-12-17 - SSRF in Organization Crawler
**Vulnerability:** The `OrganizationCrawler` in `scripts/web_crawler.py` was vulnerable to Server-Side Request Forgery (SSRF) because it validated links by making HTTP requests to them without checking if they resolved to private IP addresses.
**Learning:** Even internal tools running in CI/CD environments (like GitHub Actions) are attack vectors if they process untrusted input (markdown files) and can access metadata services (e.g., AWS IMDS, localhost).
**Prevention:** Implement strict DNS resolution checks before making requests. Resolve the hostname to an IP and verify it is not in a private or reserved range using `ipaddress` module.

# Sentinel Journal

## 2025-12-18 - Unchecked URL Access in Web Crawler
**Vulnerability:** The `scripts/web_crawler.py` script was vulnerable to Server-Side Request Forgery (SSRF). It blindly followed links found in markdown files, allowing a malicious actor (or a mistake in a markdown file) to trigger requests to internal services or private IP addresses from the runner environment.
**Learning:** Tools that fetch external resources (crawlers, link checkers) must always validate the destination IP address, not just the URL scheme. `requests` does not inherently block private ranges.
**Prevention:** Always resolve the hostname to an IP address and check if it falls within private or loopback ranges before making a request. Use a helper function like `_is_safe_url` to enforce this check globally for the crawler.

## 2025-12-18 - Incomplete DNS Validation in SSRF Protection
**Vulnerability:** The initial SSRF fix used `socket.gethostbyname`, which only returns the first IP address. Hostnames with multiple A records (some private, some public) could bypass the check if `requests` selected a different IP than the validator.
**Learning:** Functions like `gethostbyname` are insufficient for security validation because they don't reveal the full picture of DNS resolution.
**Prevention:** Use `socket.getaddrinfo` to enumerate all resolved IP addresses and ensure *every* possible destination is safe before allowing the request.

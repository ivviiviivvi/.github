# Sentinel Journal

## 2025-12-18 - Unchecked URL Access in Web Crawler
**Vulnerability:** The `scripts/web_crawler.py` script was vulnerable to Server-Side Request Forgery (SSRF). It blindly followed links found in markdown files, allowing a malicious actor (or a mistake in a markdown file) to trigger requests to internal services or private IP addresses from the runner environment.
**Learning:** Tools that fetch external resources (crawlers, link checkers) must always validate the destination IP address, not just the URL scheme. `requests` does not inherently block private ranges.
**Prevention:** Always resolve the hostname to an IP address and check if it falls within private or loopback ranges before making a request. Use a helper function like `_is_safe_url` to enforce this check globally for the crawler.

## 2025-12-19 - SSRF Protection Enhancement (IPv6 & Multi-IP)
**Vulnerability:** The initial SSRF protection using `socket.gethostbyname` only checked the first resolved IPv4 address. This left the system vulnerable to DNS rebinding or dual-stack attacks where a hostname resolves to both a safe public IP and a private/IPv6 address (e.g., `::1`), which `requests` might prefer.
**Learning:** `socket.gethostbyname` is insufficient for security checks. Applications must check ALL resolved addresses (IPv4 and IPv6) returned by `socket.getaddrinfo`.
**Prevention:** Updated `_is_safe_url` to use `socket.getaddrinfo`, iterate through all resolved IPs, and block the request if *any* of them are private, loopback, or reserved.

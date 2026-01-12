## 2024-05-23 - [Optimizing SSRF Checks with Caching]
**Learning:** In a high-volume crawler, repeated IP validation for the same hostname can be a CPU bottleneck. Caching the safety check (`_is_hostname_safe`) is effective, BUT it is critical that the underlying DNS resolution (`_resolve_hostname`) is ALSO cached and that both methods use the same cache or the same data source. If `_resolve_hostname` is not cached or if the cache is bypassed, a race condition (DNS Rebinding) could occur where the IP checked is different from the IP used.
**Action:** When caching security checks that depend on external state (like DNS), ensure the state itself is also cached or pinned for the duration of the operation to prevent TOCTOU vulnerabilities. In this case, `_resolve_hostname` was already cached, making the optimization safe.

## 2026-01-09 - [Pre-compiling Regex in Loops]
**Learning:** Repeatedly calling `re.findall`, `re.split` or `any()` checks with strings in a loop (especially in text processing hotspots like `MouthpieceFilter`) incurs significant overhead. Specifically, replacing an `any()` check over a list of keywords with a single pre-compiled regex search provided an ~18% performance improvement in text transformation tasks.
**Action:** When performing repeated text pattern matching or keyword searching, always pre-compile regex patterns as class constants (`_PATTERN = re.compile(...)`) and use `_PATTERN.search()` or `_PATTERN.findall()` instead of inline method calls or list comprehensions.

## 2026-01-10 - [SSL Context Creation Overhead]
**Learning:** In a high-concurrency web crawler, creating a new `ssl.create_default_context()` for every HTTPS connection attempt (for SSRF protection via `HTTPSConnectionPool`) is surprisingly expensive (~40ms per call). For a crawl with 1000 links, this adds 40 seconds of pure CPU overhead.
**Action:** Create the SSL context once during initialization and pass it to the connection pool for each request. This maintains security (same context configuration) while eliminating the setup cost.

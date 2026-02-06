## 2025-02-19 - \[Secure ML Model Persistence\]

**Vulnerability:** Insecure deserialization in
`src/automation/scripts/predict_workflow_failures.py`. The script used
`pickle.load()` on model files without any integrity checks. An attacker who
could modify the `.pkl` file could execute arbitrary code when the model was
loaded. **Learning:** `pickle` is inherently insecure for untrusted data. While
standard libraries like `joblib` are common in ML, they also rely on pickle.
When a safer format (like ONNX) is not feasible, cryptographic signatures (HMAC)
are a robust way to verify file integrity before deserialization.
**Prevention:** Avoid `pickle` for untrusted data. If pickle is necessary, use
HMAC-SHA256 to sign and verify the data. Ensure the verification happens
*before* any unpickling occurs.

## 2025-02-18 - \[Prevent DoS via urllib3 Large File Download\]

**Vulnerability:** Potential Denial of Service (DoS) in
`scripts/web_crawler.py`. The crawler used `urllib3`'s default behavior for
fallback GET requests, which eagerly downloads the entire response body. If a
crawled link pointed to a massive file (e.g., ISO, large video), it could
exhaust memory or bandwidth, crashing the crawler. **Learning:** `urllib3` (and
`requests`) defaults to `preload_content=True`. When validating links where only
the status code matters (after a failed HEAD request), explicitly set
`preload_content=False` (or `stream=True` in requests) to avoid downloading the
body. **Prevention:** For status checks on untrusted URLs, always use
`preload_content=False` and ensure the connection is released via
`response.release_conn()` or `response.close()`.

## 2025-02-17 - \[Fix Code Injection in GitHub Actions\]

**Vulnerability:** Unmitigated Code Injection in
`.github/workflows/batch-pr-operations.yml`. The workflow interpolated user
inputs directly into a JavaScript code block executed by
`actions/github-script`. A malicious user with workflow dispatch permissions
could inject arbitrary JavaScript code. **Learning:** GitHub Actions
`github-script` action executes code in a Node.js context. Direct interpolation
of inputs (e.g., `const val = '${{ inputs.val }}'`) is dangerous because the
input is evaluated before the script runs, allowing code injection (e.g., input
`'; system('rm -rf /'); //`). **Prevention:** Always use environment variables
to pass inputs to `github-script`. Map inputs to `env:` in the workflow step,
and access them via `process.env.VAR_NAME` within the script. This ensures data
is treated as data, not code.

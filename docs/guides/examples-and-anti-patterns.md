# Examples & Anti-Patterns

> **Learn by example: Common use cases and mistakes to avoid**

This guide provides practical examples of both good practices and common
pitfalls to avoid in the {{ORG_NAME}}/.github repository.

______________________________________________________________________

## Table of Contents

- [Workflow Examples](#workflow-examples)
- [Testing Examples](#testing-examples)
- [Documentation Examples](#documentation-examples)
- [Code Examples](#code-examples)
- [Security Examples](#security-examples)
- [Common Anti-Patterns](#common-anti-patterns)

______________________________________________________________________

## Workflow Examples

### ✅ Good: Secure Workflow with Proper Configuration

```yaml
name: Secure CI Workflow

on:
  push:
    branches: [main, develop]
    paths:
      - "src/**"
      - "tests/**"
  pull_request:
    branches: [main]
  workflow_dispatch:

# Explicit minimal permissions
permissions:
  contents: read
  pull-requests: write
  checks: write

# Prevent duplicate runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15 # Always set timeout

    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
      fail-fast: false # Test all versions even if one fails

    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4 - Pinned to SHA
        with:
          fetch-depth: 0 # Full history for better context

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip" # Enable caching

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest tests/ --cov --cov-report=xml --cov-report=term-missing

      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### ❌ Bad: Insecure and Inefficient Workflow

```yaml
name: Bad CI Workflow

on: [push] # ❌ Runs on every push to any branch

permissions: write-all # ❌ Excessive permissions

jobs:
  test:
    runs-on: ubuntu-latest
    # ❌ No timeout - could run forever
    # ❌ No concurrency control - wastes resources

    steps:
      - uses: actions/checkout@v4 # ❌ Not pinned to SHA

      - uses: actions/setup-python@v5 # ❌ Not pinned to SHA
        with:
          python-version: "3.11"
          # ❌ No caching

      - run: pip install -r requirements.txt

      - run: pytest
        # ❌ No coverage reporting
        # ❌ No failure handling

      - name: Deploy # ❌ Deploying from any branch
        run: |
          echo "${{ secrets.API_KEY }}" > key.txt  # ❌ Writing secret to file
          ./deploy.sh
```

**Problems**:

- Not pinned to SHAs (security risk)
- No timeout (resource waste)
- Excessive permissions (security risk)
- No caching (slow)
- No concurrency control (waste)
- Runs on every push (too frequent)
- Exposes secrets unsafely
- No proper error handling

______________________________________________________________________

## Testing Examples

### ✅ Good: Comprehensive Test Suite

```python
"""Tests for data processor module."""
import pytest
from unittest.mock import Mock, patch
from automation.scripts.data_processor import DataProcessor, ValidationError


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create a DataProcessor instance for testing."""
        return DataProcessor(max_items=100)

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return {
            "items": ["item1", "item2", "item3"],
            "metadata": {"version": "1.0"}
        }

    def test_initialization(self):
        """Test processor initialization with default values."""
        processor = DataProcessor()
        assert processor.max_items == 1000
        assert processor.strict_mode is False

    def test_process_valid_data(self, processor, sample_data):
        """Test processing with valid data."""
        result = processor.process(sample_data)

        assert result["status"] == "success"
        assert len(result["processed_items"]) == 3
        assert result["metadata"]["version"] == "1.0"

    def test_empty_data_raises_error(self, processor):
        """Test that empty data raises ValidationError."""
        with pytest.raises(ValidationError, match="Data cannot be empty"):
            processor.process({"items": []})

    @pytest.mark.parametrize("max_items,input_count,expected_count", [
        (5, 3, 3),    # Under limit
        (5, 5, 5),    # At limit
        (5, 7, 5),    # Over limit (truncated)
    ])
    def test_item_limit_enforcement(self, max_items, input_count, expected_count):
        """Test that item limit is enforced correctly."""
        processor = DataProcessor(max_items=max_items)
        data = {"items": [f"item{i}" for i in range(input_count)]}

        result = processor.process(data)
        assert len(result["processed_items"]) == expected_count

    @patch('automation.scripts.data_processor.external_api_call')
    def test_handles_api_failure_gracefully(self, mock_api, processor, sample_data):
        """Test graceful handling of external API failures."""
        mock_api.side_effect = ConnectionError("API unavailable")

        result = processor.process(sample_data)

        assert result["status"] == "partial_success"
        assert "API unavailable" in result["errors"]
        mock_api.assert_called_once()

    @pytest.mark.security
    def test_sanitizes_user_input(self, processor):
        """Test that user input is properly sanitized."""
        malicious_data = {
            "items": ["<script>alert('xss')</script>", "normal_item"]
        }

        result = processor.process(malicious_data)

        # Verify script tags are removed
        assert "<script>" not in str(result["processed_items"])
        assert "normal_item" in result["processed_items"]

    @pytest.mark.slow
    def test_large_dataset_performance(self, processor):
        """Test processing performance with large dataset."""
        import time

        large_data = {"items": [f"item{i}" for i in range(10000)]}

        start = time.time()
        result = processor.process(large_data)
        duration = time.time() - start

        assert duration < 5.0  # Should complete within 5 seconds
        assert result["status"] == "success"
```

### ❌ Bad: Inadequate Tests

```python
"""Bad test examples."""
import pytest
from automation.scripts.data_processor import DataProcessor


def test_it_works():  # ❌ Vague name
    """Test the processor."""  # ❌ Vague description
    p = DataProcessor()
    d = {"items": ["a", "b"]}
    r = p.process(d)
    assert r  # ❌ Weak assertion
    assert r["status"] == "success"
    # ❌ Doesn't test edge cases
    # ❌ Doesn't test error conditions
    # ❌ No fixtures for reusability


def test_process():  # ❌ Not descriptive
    processor = DataProcessor()
    # ❌ No setup or fixtures
    result = processor.process(None)  # ❌ Will crash
    # ❌ No error handling test


# ❌ Tests are interdependent
data = None

def test_first():
    global data
    data = DataProcessor().process({"items": ["test"]})
    assert data

def test_second():
    # ❌ Depends on test_first running first
    assert data["status"] == "success"


class TestBad:
    def test_something(self):
        processor = DataProcessor()
        processor.process({"items": ["1"]})
        # ❌ No assertion at all!
```

**Problems**:

- Vague test/function names
- Weak or missing assertions
- No edge case testing
- No error condition testing
- Interdependent tests (fragile)
- No use of fixtures
- Missing test markers
- Poor documentation

______________________________________________________________________

## Documentation Examples

### ✅ Good: Clear, Comprehensive Documentation

````markdown
# Feature X Setup Guide

> **Complete guide to setting up and using Feature X in production environments**

## Overview

Feature X provides automated data synchronization across multiple repositories. This guide covers:

- Initial setup (15 minutes)
- Configuration options
- Common use cases
- Troubleshooting

## Prerequisites

Before starting, ensure you have:

| Requirement | Version | Installation                     |
| ----------- | ------- | -------------------------------- |
| Python      | 3.10+   | [python.org](https://python.org) |
| GitHub CLI  | 2.40+   | `brew install gh`                |
| Access      | Admin   | Contact @devops-team             |

## Quick Start

**Get running in 5 minutes:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
export GITHUB_TOKEN="your_token_here"

# 3. Run setup
python setup_feature_x.py --interactive

# 4. Verify installation
python -m feature_x.verify
```
````

## Configuration

### Basic Configuration

Edit `config/feature-x.yml`:

```yaml
feature_x:
  enabled: true
  sync_interval: 3600 # seconds
  repositories:
    - owner/repo1
    - owner/repo2
```

### Advanced Options

For custom deployments:

```yaml
feature_x:
  enabled: true
  sync_interval: 1800
  batch_size: 50 # Process 50 repos at a time
  retry_failed: true
  notification:
    slack_webhook: "https://hooks.slack.com/..."
    email: "alerts@example.com"
```

## Common Use Cases

### Use Case 1: Sync Labels Across Repos

```bash
# Sync labels to all configured repositories
python -m feature_x.sync_labels --config config/feature-x.yml

# Dry run (preview changes)
python -m feature_x.sync_labels --dry-run

# Sync to specific repos only
python -m feature_x.sync_labels --repos owner/repo1,owner/repo2
```

### Use Case 2: Scheduled Automation

Add to cron or GitHub Actions:

```yaml
# .github/workflows/feature-x-sync.yml
name: Feature X Sync

on:
  schedule:
    - cron: "0 */6 * * *" # Every 6 hours

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@SHA
      - name: Run sync
        run: python -m feature_x.sync_labels
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

### Issue: "Authentication failed"

**Symptom**: `Error: 401 Unauthorized`

**Cause**: Invalid or expired GitHub token

**Solution**:

```bash
# Generate new token
gh auth refresh

# Export token
export GITHUB_TOKEN=$(gh auth token)

# Verify
python -m feature_x.verify
```

### Issue: "Rate limit exceeded"

**Symptom**: `Error: 403 Forbidden - Rate limit exceeded`

**Solution**:

```bash
# Check rate limit status
gh api rate_limit

# Wait for reset or use authenticated requests (increases limit from 60 to 5000/hour)
export GITHUB_TOKEN=$(gh auth token)
```

## FAQ

**Q: Can I sync to private repositories?**

A: Yes, ensure your token has `repo` scope.

**Q: How do I exclude certain repositories?**

A: Add to `config/feature-x.yml`:

```yaml
feature_x:
  exclude_repos:
    - owner/repo-to-skip
```

## Related Resources

- API Documentation
- Configuration Reference
- GitHub Actions Integration

______________________________________________________________________

_Last Updated: 2026-01-14_ _Maintained by: DevOps Team_ _For issues:
[Open a ticket](https://github.com/org/repo/issues/new)_

````

### ❌ Bad: Poor Documentation

```markdown
# Feature X

This is feature x.

## Setup

Install it:

````

pip install something

```

Run it:

```

python script.py

```

That's it!

## Config

Put this in a file:

```

enabled: true

```

## Problems

If it doesn't work, check the logs.
```

**Problems**:

- No table of contents
- No prerequisites
- Vague instructions ("something", "a file")
- No examples of actual usage
- No troubleshooting details
- No context or "why"
- No links to related docs
- No maintainer info
- No proper code blocks with language tags
- No expected results

______________________________________________________________________

## Code Examples

### ✅ Good: Well-Structured Python Function

```python
"""User authentication module."""
import logging
from typing import Optional, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


def authenticate_user(
    username: str,
    password: str,
    *,
    max_attempts: int = 3,
    lockout_duration: int = 300
) -> Dict[str, any]:
    """
    Authenticate a user with username and password.

    Implements rate limiting and account lockout after failed attempts.

    Args:
        username: User's username (case-insensitive)
        password: User's password
        max_attempts: Maximum failed attempts before lockout (default: 3)
        lockout_duration: Lockout duration in seconds (default: 300)

    Returns:
        Dictionary containing:
            - user_id: Unique user identifier
            - token: JWT authentication token
            - expires_at: Token expiration timestamp

    Raises:
        AuthenticationError: If authentication fails or account is locked
        ValueError: If username or password is empty

    Example:
        >>> result = authenticate_user("alice", "secret123")
        >>> print(result["token"])
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    # Validate inputs
    if not username or not password:
        raise ValueError("Username and password are required")

    username = username.lower().strip()

    # Check if account is locked
    if is_account_locked(username):
        logger.warning(f"Login attempt for locked account: {username}")
        raise AuthenticationError(
            f"Account locked. Try again in {lockout_duration} seconds"
        )

    # Verify credentials
    try:
        user = get_user_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            record_failed_attempt(username)
            attempts_remaining = max_attempts - get_failed_attempts(username)

            logger.info(f"Failed login attempt for: {username}")
            raise AuthenticationError(
                f"Invalid credentials. {attempts_remaining} attempts remaining"
            )

        # Success - reset failed attempts and generate token
        reset_failed_attempts(username)
        token = generate_jwt_token(user.id)
        expires_at = datetime.utcnow() + timedelta(hours=24)

        logger.info(f"Successful login: {username}")
        return {
            "user_id": user.id,
            "token": token,
            "expires_at": expires_at.isoformat()
        }

    except Exception as e:
        logger.error(f"Authentication error for {username}: {e}")
        raise AuthenticationError("Authentication failed") from e
```

### ❌ Bad: Poorly Structured Function

```python
def auth(u, p):  # ❌ No type hints, unclear names
    # ❌ No docstring
    if not u:  # ❌ Missing password check
        return False

    usr = db.query("SELECT * FROM users WHERE username = '" + u + "'")  # ❌ SQL injection!
    # ❌ No error handling

    if usr and usr[0][2] == p:  # ❌ Storing plaintext passwords!
        return usr[0][0]  # ❌ Magic number (what is [0]?)

    return None  # ❌ Inconsistent return types (False vs None)


# ❌ Global state
failed_logins = {}

def check_login(username, password):
    global failed_logins  # ❌ Using globals

    result = auth(username, password)
    if not result:
        failed_logins[username] = failed_logins.get(username, 0) + 1
        print("Login failed")  # ❌ Using print instead of logging
        return

    print("Login success")  # ❌ No structured return value
    return result
```

**Problems**:

- No type hints
- No docstrings
- SQL injection vulnerability
- Plaintext passwords
- Poor variable names
- No error handling
- Using globals
- print() instead of logging
- Inconsistent return types
- Magic numbers
- No input validation

______________________________________________________________________

## Security Examples

### ✅ Good: Secure API Request Handler

```python
"""Secure API request handler."""
import ipaddress
import re
from typing import Dict, List
from urllib.parse import urlparse

# Private IP ranges to block
PRIVATE_IP_RANGES = [
    ipaddress.ip_network('127.0.0.0/8'),    # Localhost
    ipaddress.ip_network('10.0.0.0/8'),     # Private
    ipaddress.ip_network('172.16.0.0/12'),  # Private
    ipaddress.ip_network('192.168.0.0/16'), # Private
    ipaddress.ip_network('169.254.0.0/16'), # Link-local
]


def fetch_external_url(
    url: str,
    *,
    timeout: int = 10,
    allow_redirects: bool = False
) -> Dict[str, any]:
    """
    Fetch content from an external URL with security checks.

    Implements SSRF protection by blocking private IPs and validating URLs.

    Args:
        url: URL to fetch (must be http:// or https://)
        timeout: Request timeout in seconds
        allow_redirects: Whether to follow redirects

    Returns:
        Dictionary with status_code, content, and headers

    Raises:
        ValueError: If URL is invalid or points to private network
        requests.RequestException: If request fails
    """
    # Validate URL scheme
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Invalid scheme: {parsed.scheme}")

    # Validate hostname exists
    if not parsed.hostname:
        raise ValueError("URL must have a hostname")

    # Block private IPs (SSRF protection)
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for private_range in PRIVATE_IP_RANGES:
            if ip in private_range:
                raise ValueError(f"Private IP access denied: {ip}")
    except ValueError as e:
        # Hostname might be a domain name, resolve it
        try:
            import socket
            resolved_ip = socket.gethostbyname(parsed.hostname)
            ip = ipaddress.ip_address(resolved_ip)
            for private_range in PRIVATE_IP_RANGES:
                if ip in private_range:
                    raise ValueError(f"Domain resolves to private IP: {resolved_ip}")
        except (socket.gaierror, ValueError):
            # If resolution fails or it's truly invalid, raise original error
            if "Private IP" in str(e):
                raise

    # Make request with safety measures
    import requests

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=allow_redirects,
        headers={'User-Agent': 'MyApp/1.0'},
        verify=True  # Verify SSL certificates
    )
    response.raise_for_status()

    return {
        "status_code": response.status_code,
        "content": response.text[:10000],  # Limit content size
        "headers": dict(response.headers)
    }
```

### ❌ Bad: Insecure API Handler

```python
def get_url(url):  # ❌ No SSRF protection
    import requests

    response = requests.get(url, verify=False)  # ❌ Disabling SSL verification!
    return response.text  # ❌ No size limit - could crash with huge response


def run_command(cmd):  # ❌ Command injection vulnerability
    import os
    os.system(cmd)  # ❌ NEVER do this with user input!


def load_config(filename):  # ❌ Path traversal vulnerability
    with open(f"/app/config/{filename}") as f:  # ❌ User could pass ../../etc/passwd
        return f.read()


def store_api_key(key):
    # ❌ Storing in plain text
    with open("api_key.txt", "w") as f:
        f.write(key)

    # ❌ Logging secrets
    print(f"Stored API key: {key}")
```

______________________________________________________________________

## Common Anti-Patterns

### Anti-Pattern 1: God Object

**❌ Bad**:

```python
class WorkflowManager:
    """Does everything."""

    def __init__(self):
        self.config = {}
        self.users = []
        self.logs = []
        self.metrics = {}
        self.cache = {}

    def load_config(self): ...
    def save_config(self): ...
    def add_user(self): ...
    def remove_user(self): ...
    def log_event(self): ...
    def get_logs(self): ...
    def collect_metrics(self): ...
    def generate_report(self): ...
    def send_email(self): ...
    def backup_database(self): ...
    # ... 50 more methods ...
```

**✅ Good** - Single Responsibility:

```python
class ConfigManager:
    """Manages configuration."""
    def load(self): ...
    def save(self): ...
    def validate(self): ...


class UserManager:
    """Manages users."""
    def add_user(self): ...
    def remove_user(self): ...
    def get_user(self): ...


class MetricsCollector:
    """Collects and reports metrics."""
    def collect(self): ...
    def generate_report(self): ...
```

### Anti-Pattern 2: Magic Numbers

**❌ Bad**:

```python
if user.age > 18 and user.age < 65:  # What's special about 65?
    ...

if response.status_code == 429:  # What does 429 mean?
    time.sleep(60)  # Why 60 seconds?
```

**✅ Good** - Named Constants:

```python
MINIMUM_AGE = 18
RETIREMENT_AGE = 65
RATE_LIMIT_STATUS = 429
RATE_LIMIT_RETRY_SECONDS = 60

if MINIMUM_AGE < user.age < RETIREMENT_AGE:
    ...

if response.status_code == RATE_LIMIT_STATUS:
    time.sleep(RATE_LIMIT_RETRY_SECONDS)
```

### Anti-Pattern 3: Cargo Cult Programming

**❌ Bad** - Copying code without understanding:

```python
# Copied from Stack Overflow, not sure what it does
import sys
sys.path.insert(0, '..')
from some_module import *  # ❌ Star imports

# Copied error handling pattern
try:
    do_something()
except:  # ❌ Bare except
    pass  # ❌ Silently ignoring errors

# Copied without understanding
import os
os.system('rm -rf /tmp/*')  # ❌ Dangerous!
```

**✅ Good** - Understanding what you write:

```python
# Explicit imports
from some_module import SpecificClass, specific_function

# Targeted error handling
try:
    result = do_something()
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise
except IOError as e:
    logger.error(f"File operation failed: {e}")
    return None

# Safe file operations
import shutil
temp_dir = Path('/tmp/my_app')
if temp_dir.exists():
    shutil.rmtree(temp_dir)
```

### Anti-Pattern 4: Premature Optimization

**❌ Bad**:

```python
# Optimizing before profiling
class UltraFastCache:
    """Ultra-optimized cache using advanced algorithms."""
    def __init__(self):
        # 500 lines of complex optimization code
        # ... but only caching 10 items
        self.cache = {}  # ❌ Simple dict would work fine!
```

**✅ Good** - Optimize when needed:

```python
# Start simple
cache = {}

# Profile first
import cProfile
cProfile.run('my_function()')

# Then optimize bottlenecks
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    ...
```

______________________________________________________________________

## Learning from Examples

### How to Use This Guide

1. **Review good examples** before implementing new features
1. **Compare with anti-patterns** to catch mistakes
1. **Adapt examples** to your specific needs
1. **Share with team** for consistent standards
1. **Update guide** when discovering new patterns

### Contributing Examples

Found a great example or common mistake? Add it!

```bash
git checkout -b docs/add-example
# Edit this file
git commit -m "docs: add example for X pattern"
gh pr create
```

______________________________________________________________________

## Related Resources

- [Best Practices Guide](best-practices.md) - Comprehensive best practices
- [New Contributor Guide](NEW_CONTRIBUTOR_GUIDE.md) - Getting started
- [Common Tasks Runbook](common-tasks-runbook.md) - Step-by-step procedures

______________________________________________________________________

_Last Updated: 2026-01-14_ _Maintained by: Documentation Team_

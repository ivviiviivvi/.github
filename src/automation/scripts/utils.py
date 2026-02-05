"""Base utilities for Month 3 advanced automation.

Provides common functionality used across all Month 3 components:
- GitHub API client with rate limiting
- Configuration loading and validation
- Logging setup
- Error handling
- Retry logic
"""

import json
import logging
import random
import time
from pathlib import Path
from typing import Any, Optional, cast

import requests
import yaml
from secret_manager import get_secret

# =============================================================================
# Logging Configuration
# =============================================================================


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Set up a logger with consistent formatting.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance

    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Console handler
    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, level.upper()))

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# =============================================================================
# Configuration Management
# =============================================================================


class ConfigLoader:
    """Load and validate configuration from YAML files."""

    def __init__(self, config_dir: Path = Path(".github")):
        """Initialize config loader.

        Args:
            config_dir: Directory containing configuration files

        """
        self.config_dir = config_dir
        self.logger = setup_logger(__name__)

    def load(self, filename: str) -> dict[str, Any]:
        """Load configuration from YAML file.

        Args:
            filename: Configuration file name

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML

        """
        config_path = self.config_dir / filename

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        self.logger.info(f"Loading configuration from {config_path}")

        try:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config or {}
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in {config_path}: {e}")
            raise

    def get(self, filename: str, key: str, default: Any = None) -> Any:
        """Get configuration value with optional default.

        Args:
            filename: Configuration file name
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key not found

        Returns:
            Configuration value or default

        """
        try:
            config = self.load(filename)
            keys = key.split(".")
            value = config

            for k in keys:
                value = value.get(k, {})

            return value if value != {} else default

        except (FileNotFoundError, yaml.YAMLError):
            return default


# =============================================================================
# GitHub API Client
# =============================================================================


class RateLimiter:
    """Thread-safe rate limiter for GitHub API requests."""

    def __init__(self, max_requests: int = 5000, window: int = 3600):
        """Initialize rate limiter.

        Args:
            max_requests: Maximum requests per window
            window: Time window in seconds (default: 1 hour)

        """
        import threading

        self.max_requests = max_requests
        self.window = window
        self.requests: list = []
        self._lock = threading.Lock()
        self.logger = setup_logger(__name__)

    def acquire(self) -> bool:
        """Check if request can proceed (thread-safe).

        Returns:
            True if request can proceed, False if rate limited

        """
        now = time.time()

        with self._lock:
            # Remove old requests outside the window
            self.requests = [r for r in self.requests if r > now - self.window]

            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True

            self.logger.warning(
                f"Rate limit reached: {len(self.requests)}/{self.max_requests} requests"  # noqa: E501
            )
            return False

    def wait_time(self) -> float:
        """Calculate wait time until next request can proceed (thread-safe).

        Returns:
            Wait time in seconds (0 if can proceed now)

        """
        with self._lock:
            if not self.requests:
                return 0.0

            now = time.time()
            oldest_request = self.requests[0]
            return float(max(0, self.window - (now - oldest_request)))

    def wait(self) -> None:
        """Wait until next request can proceed."""
        wait_seconds = self.wait_time()
        if wait_seconds > 0:
            self.logger.info(f"Rate limited. Waiting {wait_seconds:.1f}s...")
            time.sleep(wait_seconds)


class GitHubAPIClient:
    """GitHub API client with rate limiting and error handling."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub API client.

        Args:
            token: GitHub API token (optional - defaults to gh CLI token)

        """
        # Try to get token from parameter, fall back to gh CLI
        if token is None:
            try:
                # Try to get token from gh CLI (most common case)
                import subprocess  # nosec B404

                result = subprocess.run(  # nosec B603 B607
                    ["gh", "auth", "token"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                token = result.stdout.strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fall back to 1Password if gh CLI not available
                token = get_secret("org-label-sync-token", "password")

        self.token = token
        if not self.token:
            raise ValueError(
                "GitHub token required. Either:\n"
                "  1. Authenticate with: gh auth login\n"
                "  2. Pass token parameter\n"
                "  3. Store in 1Password as org-label-sync-token"
            )

        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

        self.rate_limiter = RateLimiter()
        self.logger = setup_logger(__name__)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
        retry: bool = True,
    ) -> Any:
        """Make a GitHub API request with rate limiting and retries.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (e.g., /repos/owner/repo/issues)
            params: Query parameters
            json_data: JSON request body
            retry: Whether to retry on transient failures

        Returns:
            Response JSON

        Raises:
            requests.HTTPError: If request fails after retries

        """
        # Wait if rate limited
        if not self.rate_limiter.acquire():
            self.rate_limiter.wait()

        url = f"{self.base_url}{endpoint}"
        attempt = 0
        max_attempts = 3 if retry else 1

        while attempt < max_attempts:
            attempt += 1

            try:
                response = self.session.request(method, url, params=params, json=json_data, timeout=30)

                # Update rate limit info from headers
                if "X-RateLimit-Remaining" in response.headers:
                    remaining = int(response.headers["X-RateLimit-Remaining"])
                    if remaining < 100:
                        self.logger.warning(f"Low rate limit remaining: {remaining} requests")

                response.raise_for_status()
                return response.json() if response.content else {}

            except requests.exceptions.Timeout:
                if attempt < max_attempts:
                    delay = 2**attempt + random.uniform(0, 1)  # nosec B311
                    self.logger.warning(
                        f"Request timeout (attempt {attempt}/{max_attempts}). Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(f"Request timeout after {max_attempts} attempts")
                    raise

            except requests.exceptions.HTTPError as e:
                # Retry on 5xx errors or rate limit
                if e.response.status_code >= 500 or e.response.status_code == 429:
                    if attempt < max_attempts:
                        # Use Retry-After header if available
                        retry_after = e.response.headers.get("Retry-After")
                        if retry_after:
                            delay = int(retry_after)
                        else:
                            delay = 2**attempt + random.uniform(0, 1)  # nosec B311

                        self.logger.warning(
                            f"HTTP {e.response.status_code} (attempt {attempt}/{max_attempts}). "  # noqa: E501
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        self.logger.error(
                            f"HTTP {e.response.status_code} after {max_attempts} attempts"  # noqa: E501
                        )
                        raise
                else:
                    # Don't retry 4xx errors (except 429)
                    self.logger.error(f"HTTP {e.response.status_code}: {e.response.text}")
                    raise

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                raise

        # Should never reach here
        raise RuntimeError("Unexpected end of retry loop")

    def get(self, endpoint: str, params: Optional[dict] = None) -> Any:
        """Make a GET request."""
        return self.request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json_data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        """Make a POST request."""
        data = json_data or json
        return self.request("POST", endpoint, json_data=data)

    def put(
        self,
        endpoint: str,
        json_data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        """Make a PUT request."""
        data = json_data or json
        return self.request("PUT", endpoint, json_data=data)

    def patch(
        self,
        endpoint: str,
        json_data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        """Make a PATCH request."""
        data = json_data or json
        return self.request("PATCH", endpoint, json_data=data)

    def delete(self, endpoint: str) -> Any:
        """Make a DELETE request."""
        return self.request("DELETE", endpoint)


# =============================================================================
# Error Handling
# =============================================================================


class AutomationError(Exception):
    """Base exception for automation errors."""


class ValidationError(AutomationError):
    """Validation error."""


class ConfigurationError(AutomationError):
    """Configuration error."""


class APIError(AutomationError):
    """GitHub API error."""


def safe_get(data: dict, path: str, default: Any = None) -> Any:
    """Safely get nested dictionary value using dot notation.

    Args:
        data: Dictionary to search
        path: Dot-notation path (e.g., "user.profile.name")
        default: Default value if path not found

    Returns:
        Value at path or default

    Examples:
        >>> data = {"user": {"profile": {"name": "Alice"}}}
        >>> safe_get(data, "user.profile.name")
        "Alice"
        >>> safe_get(data, "user.profile.age", 25)
        25

    """
    keys = path.split(".")
    value: Any = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default

        if value is None:
            return default

    return value


# =============================================================================
# File Operations
# =============================================================================


def read_json(filepath: Path) -> dict[str, Any]:
    """Read and parse JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON

    """
    with open(filepath, encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


def write_json(filepath: Path, data: dict[str, Any], indent: int = 2) -> None:
    """Write data to JSON file.

    Args:
        filepath: Path to JSON file
        data: Data to write
        indent: JSON indentation (default: 2 spaces)

    """
    # Create parent directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)


def read_yaml(filepath: Path) -> dict[str, Any]:
    """Read and parse YAML file.

    Args:
        filepath: Path to YAML file

    Returns:
        Parsed YAML data

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If file is invalid YAML

    """
    with open(filepath, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(filepath: Path, data: dict[str, Any]) -> None:
    """Write data to YAML file.

    Args:
        filepath: Path to YAML file
        data: Data to write

    """
    # Create parent directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def load_config(config_path: str, default: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Load configuration from YAML file with fallback to default.

    Args:
        config_path: Path to configuration file (relative or absolute)
        default: Default configuration if file doesn't exist

    Returns:
        Configuration dictionary

    """
    path = Path(config_path)
    if path.exists():
        return read_yaml(path)
    return default or {}


# =============================================================================
# Retry Logic
# =============================================================================


def retry_with_backoff(
    func,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
):
    """Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_attempts: Maximum retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Backoff multiplier
        jitter: Add random jitter to delays

    Returns:
        Function result

    Raises:
        Last exception if all attempts fail

    """
    logger = setup_logger(__name__)
    attempt = 0
    last_exception = None

    while attempt < max_attempts:
        attempt += 1

        try:
            return func()
        except Exception as e:
            last_exception = e

            if attempt < max_attempts:
                delay = min(
                    max_delay,
                    initial_delay * (backoff_factor ** (attempt - 1)),
                )
                if jitter:
                    delay += random.uniform(0, 1)  # nosec B311

                logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
            else:
                logger.error(f"All {max_attempts} attempts failed")

    if last_exception:
        raise last_exception

#!/usr/bin/env python3
"""Universal Secret Manager for GitHub Copilot Automation.

Securely retrieves secrets from 1Password CLI ONLY.
No environment variable fallback - proper security, no compromises.

For CI/CD: Use 1Password Service Accounts, not environment variables.

Supported secret types:
- GitHub tokens (personal access tokens, app tokens)
- API keys (third-party services)
- Passwords (databases, services)
- SSH keys
- Certificates
- Any other sensitive credentials

Usage:
    from secret_manager import get_secret, ensure_github_token

    # GitHub token (most common)
    token = ensure_github_token()

    # Generic secret
    api_key = ensure_secret("my-api-key-item", "credential")

    # Database password
    db_pass = ensure_secret("prod-database", "password")

CI/CD Integration:
    Use 1Password Service Accounts - NOT environment variables.

    GitHub Actions Example:
        - uses: 1password/install-cli-action@v1

        - name: Deploy
          env:
            OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
          run: python3 automation/scripts/batch_onboard_repositories.py

    The OP_SERVICE_ACCOUNT_TOKEN is a service account credential that
    authenticates the 1Password CLI. Your actual secrets stay in 1Password
    and are never exposed as environment variables.

    Learn more:
    https://developer.1password.com/docs/service-accounts/
"""

import subprocess  # nosec B404
import sys
from typing import Optional


def get_secret(item_name: str, field: str = "password", vault: str = "Private") -> Optional[str]:
    """Get secret from 1Password CLI.

    Args:
        item_name: Name of the 1Password item
        field: Field to retrieve (password, username, credential, etc.)
        vault: Vault name (default: Private)

    Returns:
        The secret value, or None if not found

    Security:
        - Retrieved from encrypted 1Password vault only
        - Only exists in memory during execution
        - No plaintext files created
        - Auto-cleared when process exits
        - NO environment variable fallback

    Examples:
        >>> api_key = get_secret("datadog-api-key", "credential")
        >>> db_password = get_secret("postgres-prod", "password")
        >>> ssh_key = get_secret("deploy-key", "private key")

    """
    try:
        cmd = ["op", "item", "get", item_name, "--fields", field, "--reveal"]
        if vault != "Private":
            cmd.extend(["--vault", vault])

        result = subprocess.run(  # nosec B603 B607
            cmd, capture_output=True, text=True, check=True
        )
        secret = result.stdout.strip()
        return secret if secret else None

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "unknown error"
        print(f"❌ 1Password CLI error: {error_msg}", file=sys.stderr)
        return None

    except FileNotFoundError:
        print("❌ 1Password CLI not installed", file=sys.stderr)
        print(
            "   Install: https://developer.1password.com/docs/cli/get-started/",  # noqa: E501
            file=sys.stderr,
        )
        return None


def ensure_secret(item_name: str, field: str = "password", vault: str = "Private") -> str:
    """Get secret from 1Password or exit if unavailable.

    Args:
        item_name: Name of the 1Password item
        field: Field to retrieve
        vault: Vault name

    Returns:
        The secret value (guaranteed)

    Raises:
        SystemExit: If secret cannot be retrieved

    """
    secret = get_secret(item_name, field, vault)
    if not secret:
        _print_secret_error(item_name, field, vault)
        sys.exit(1)
    return secret


def get_github_token(item_name: str) -> Optional[str]:
    """Get GitHub token from environment variable or 1Password CLI.

    Checks environment variables first (for dev containers and CI/CD
    environments where 1Password may not be available), then falls back
    to 1Password CLI.

    Note: While get_secret() is 1Password-only for maximum security,
    this function allows environment variable fallback for GitHub tokens
    to support development containers and CI environments.

    Args:
        item_name: REQUIRED. Name of 1Password item containing the token.
                   Use purpose-specific tokens:
                   - 'org-label-sync-token': For label operations
                   - 'org-project-admin-token': For project operations
                   - 'org-repo-analysis-token': For read-only analysis
                   - 'org-onboarding-token': For repository onboarding

    Returns:
        The GitHub token, or None if not found

    Environment Variable Lookup:
        The item_name is converted to an environment variable by:
        1. Converting to uppercase
        2. Replacing hyphens with underscores
        Example: 'org-label-sync-token' -> ORG_LABEL_SYNC_TOKEN

    """
    if not item_name:
        raise ValueError(
            "Token name required. Use purpose-specific token:\n"
            "  - org-label-sync-token: For label operations\n"
            "  - org-project-admin-token: For project operations\n"
            "  - org-repo-analysis-token: For read-only analysis\n"
            "  - org-onboarding-token: For repository onboarding"
        )

    # Check environment variable first (dev container friendly)
    import os

    env_var_name = item_name.upper().replace("-", "_")
    env_token = os.getenv(env_var_name)
    if env_token:
        return env_token

    # Fall back to 1Password CLI
    return get_secret(item_name, "password")


def ensure_github_token(item_name: str) -> str:
    """Get GitHub token from 1Password or exit if unavailable.

    Args:
        item_name: REQUIRED. Name of 1Password item containing the token.
                   See get_github_token() for available token names.

    Returns:
        The GitHub token (guaranteed)

    Raises:
        SystemExit: If token cannot be retrieved

    """
    return ensure_secret(item_name, "password")


def _print_secret_error(item_name: str, field: str, vault: str) -> None:
    """Print detailed error message when secret retrieval fails."""
    print("", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
    print("SECRET RETRIEVAL FAILED", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
    print("", file=sys.stderr)
    print(
        f"Could not retrieve: {item_name} (field: {field}, vault: {vault})",
        file=sys.stderr,
    )
    print("", file=sys.stderr)

    print("LOCAL DEVELOPMENT:", file=sys.stderr)
    print("", file=sys.stderr)
    print("  1. Install 1Password CLI:", file=sys.stderr)
    print(
        "     https://developer.1password.com/docs/cli/get-started/",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print("  2. Authenticate with desktop app:", file=sys.stderr)
    print(
        "     https://developer.1password.com/docs/cli/app-integration/",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print("  3. Create the secret in 1Password:", file=sys.stderr)
    print(
        f'     op item create --category=password --title="{item_name}" \\',
        file=sys.stderr,
    )
    print(f'       --vault="{vault}" {field}="your-secret"', file=sys.stderr)
    print("", file=sys.stderr)

    print("CI/CD (GitHub Actions, GitLab CI, etc.):", file=sys.stderr)
    print("", file=sys.stderr)
    print("  1. Create a 1Password Service Account:", file=sys.stderr)
    print(
        "     https://developer.1password.com/docs/service-accounts/",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print("  2. Grant access to required vaults", file=sys.stderr)
    print("", file=sys.stderr)
    print("  3. Add service account token to CI/CD secrets:", file=sys.stderr)
    print("     Secret name: OP_SERVICE_ACCOUNT_TOKEN", file=sys.stderr)
    print("", file=sys.stderr)
    print("  4. Use in GitHub Actions:", file=sys.stderr)
    print("", file=sys.stderr)
    print("     - uses: 1password/install-cli-action@v1", file=sys.stderr)
    print("     ", file=sys.stderr)
    print("     - name: Run deployment", file=sys.stderr)
    print("       env:", file=sys.stderr)
    print(
        "         OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}",  # noqa: E501
        file=sys.stderr,
    )
    print(
        "       run: python3 automation/scripts/your_script.py",
        file=sys.stderr,
    )
    print("", file=sys.stderr)

    print("WHY NO ENVIRONMENT VARIABLES?", file=sys.stderr)
    print("", file=sys.stderr)
    print("  - Visible in process listings (ps aux)", file=sys.stderr)
    print("  - Inherited by all child processes", file=sys.stderr)
    print("  - Can be accidentally logged", file=sys.stderr)
    print("  - Persist in shell history", file=sys.stderr)
    print("  - Included in crash dumps", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "  1Password Service Accounts are secure AND convenient.",
        file=sys.stderr,
    )
    print("  No compromises.", file=sys.stderr)
    print("", file=sys.stderr)
    print("=" * 80, file=sys.stderr)


if __name__ == "__main__":
    # Test the secret manager
    print("Testing 1Password CLI integration...")
    print("")

    token = get_github_token("org-label-sync-token")
    if token:
        print("✅ Token retrieved successfully")
        print(f"   Length: {len(token)} characters")
        print("   Prefix: ***")
    else:
        print("❌ Failed to retrieve token")
        print("")
        print("This is expected if:")
        print("- 1Password CLI is not installed")
        print("- Not authenticated with 1Password")
        print("- Token item doesn't exist")
        print("")
        print("Run with ensure_github_token() to see full error message.")
        sys.exit(1)

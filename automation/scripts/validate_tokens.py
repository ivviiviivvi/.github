#!/usr/bin/env python3
"""
Token Validation Script
Validates all organization tokens are working correctly
Based on MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md recommendations
"""

import sys
from datetime import datetime
from typing import Dict, Optional

import requests

# Token registry (keep in sync with TOKEN_REGISTRY.md)
TOKENS = {
    "org-label-sync-token": {
        "scopes": ["repo", "workflow"],
        "test_endpoint": "/user/repos",
        "purpose": "Label synchronization",
    },
    "org-project-admin-token": {
        "scopes": ["project", "read:org"],
        "test_endpoint": "/user",
        "purpose": "GitHub Projects management",
    },
    "org-repo-analysis-token": {
        "scopes": ["repo:status", "read:org"],
        "test_endpoint": "/users/ivviiviivvi/repos",
        "purpose": "Read-only analysis",
    },
    "org-onboarding-token": {
        "scopes": ["repo", "workflow", "admin:org"],
        "test_endpoint": "/user/repos",
        "purpose": "Repository onboarding",
    },
}


def get_token_from_1password(token_name: str) -> Optional[str]:
    """Retrieve token from 1Password CLI."""
    import subprocess

    try:
        result = subprocess.run(
            ["op", "read", f"op://Personal/{token_name}/password"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        print("✗ 1Password CLI not found")
        print("  Install: brew install --cask 1password-cli")
        sys.exit(1)


def validate_token(token_name: str, config: Dict) -> Dict:
    """Validate a single token."""
    result = {
        "token": token_name,
        "valid": False,
        "scopes": [],
        "rate_limit": None,
        "error": None,
        "purpose": config["purpose"],
    }

    try:
        # Get token from 1Password
        token = get_token_from_1password(token_name)
        if not token:
            result["error"] = "Token not found in 1Password"
            return result

        # Test token with GitHub API
        response = requests.get(
            f"https://api.github.com{config['test_endpoint']}",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            timeout=10,
        )

        if response.status_code == 200:
            result["valid"] = True
            result["scopes"] = response.headers.get("X-OAuth-Scopes", "").split(", ")
            result["rate_limit"] = {
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 0)),
                "limit": int(response.headers.get("X-RateLimit-Limit", 0)),
                "reset": datetime.fromtimestamp(
                    int(response.headers.get("X-RateLimit-Reset", 0))
                ).isoformat(),
            }

            # Verify scopes match expected
            expected = set(config["scopes"])
            actual = set(result["scopes"])

            # Check if expected scopes are present (actual may have more)
            if not expected.issubset(actual):
                missing = expected - actual
                result["warning"] = f"Missing scopes: {', '.join(missing)}"
        elif response.status_code == 401:
            result["error"] = "Invalid or expired token"
        elif response.status_code == 403:
            result["error"] = "Insufficient permissions or rate limited"
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"

    except requests.RequestException as e:
        result["error"] = f"Network error: {str(e)}"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"

    return result


def main():
    """Validate all tokens."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          Token Validation                                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Validating organization tokens...")
    print()

    results = []
    all_valid = True

    for token_name, config in TOKENS.items():
        print(f"Checking {token_name}...", end=" ", flush=True)
        result = validate_token(token_name, config)
        results.append(result)

        if result["valid"]:
            rate_info = result["rate_limit"]
            print(
                f"✓ Valid (rate: {rate_info['remaining']}/{rate_info['limit']})"  # noqa: E501
            )

            if "warning" in result:
                print(f"  ⚠ {result['warning']}")
        else:
            print("✗ Failed")
            print(f"  Error: {result['error']}")
            all_valid = False

    print()
    print("=" * 60)
    print("Summary:")
    print()

    valid_count = sum(1 for r in results if r["valid"])
    total_count = len(results)

    print(f"  Valid tokens:   {valid_count}/{total_count}")
    print(f"  Failed tokens:  {total_count - valid_count}/{total_count}")
    print()

    if all_valid:
        print("✓ All tokens are healthy!")
        print()
        print("Token purposes:")
        for r in results:
            print(f"  • {r['token']}: {r['purpose']}")
        print()
        sys.exit(0)
    else:
        print("⚠ Some tokens failed validation!")
        print()
        print("Failed tokens:")
        for r in results:
            if not r["valid"]:
                print(f"  • {r['token']}: {r['error']}")
        print()
        print("Actions:")
        print("  1. Check if tokens are created in GitHub")
        print("  2. Verify tokens are stored in 1Password")
        print("  3. Confirm token scopes match requirements")
        print("  4. Run: ./token-segmentation-migration.sh")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()

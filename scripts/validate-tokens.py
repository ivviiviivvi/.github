#!/usr/bin/env python3
"""
Token Health Check
Validates all organization tokens are working correctly

Usage:
    python3 scripts/validate-tokens.py
    python3 scripts/validate-tokens.py --token org-label-sync-token
    python3 scripts/validate-tokens.py --verbose
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List

import requests

# Add parent directory to path for imports
sys.path.insert(0, "automation/scripts")
from secret_manager import get_secret  # noqa: E402

# ANSI color codes
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

# Token registry (keep in sync with TOKEN_REGISTRY.md)
TOKENS = {
    "master-org-token-011726": {
        "scopes": ["unknown"],  # To be documented
        "test_endpoint": "/user",
        "status": "deprecated",
    },
    "org-label-sync-token": {
        "scopes": ["repo", "workflow"],
        "test_endpoint": "/user/repos",
        "status": "planned",
    },
    "org-project-admin-token": {
        "scopes": ["project", "read:org"],
        "test_endpoint": "/user",
        "status": "planned",
    },
    "org-repo-analysis-token": {
        "scopes": ["repo:status", "read:org"],
        "test_endpoint": "/users/ivviiviivvi/repos",
        "status": "planned",
    },
    "org-onboarding-token": {
        "scopes": ["repo", "workflow", "admin:org"],
        "test_endpoint": "/user/repos",
        "status": "planned",
    },
}


def validate_token(token_name: str, config: Dict, verbose: bool = False) -> Dict:
    """Validate a single token"""
    result = {
        "token": token_name,
        "valid": False,
        "scopes": [],
        "rate_limit": None,
        "error": None,
        "warning": None,
        "status": config.get("status", "active"),
    }

    try:
        # Skip planned tokens (unless we have env var)
        env_var_name = token_name.upper().replace("-", "_")
        token = os.getenv(env_var_name)

        if not token and config.get("status") == "planned":
            result["error"] = "Token not yet created"
            return result

        # Get token from environment variable or 1Password
        if verbose:
            if token:
                print("  → Using token from environment variable")
            else:
                print("  → Retrieving from 1Password...")

        if not token:
            token = get_secret(token_name, "password")

        if not token:
            result["error"] = "Token not found in 1Password or environment"
            return result

        if verbose:
            print(f"  → Token retrieved ({len(token)} chars)")
            print(f"  → Testing endpoint: {config['test_endpoint']}")

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

            # Get scopes
            scopes_header = response.headers.get("X-OAuth-Scopes", "")
            result["scopes"] = [
                s.strip() for s in scopes_header.split(",") if s.strip()
            ]

            # Get rate limit
            result["rate_limit"] = {
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 0)),
                "limit": int(response.headers.get("X-RateLimit-Limit", 0)),
                "reset": datetime.fromtimestamp(
                    int(response.headers.get("X-RateLimit-Reset", 0))
                ),
            }

            if verbose:
                print(
                    f"  → Rate limit: {result['rate_limit']['remaining']}/{result['rate_limit']['limit']}"  # noqa: E501
                )
                print(f"  → Scopes: {', '.join(result['scopes'])}")

            # Verify scopes match expected (only for active tokens)
            expected = set(config.get("scopes", []))
            actual = set(result["scopes"])

            # Skip scope validation if expected is "unknown"
            if "unknown" not in expected:
                if not expected.issubset(actual):
                    missing = expected - actual
                    result["warning"] = f"Missing scopes: {', '.join(missing)}"
                    if verbose:
                        print(f"  {YELLOW}⚠{NC}  Warning: {result['warning']}")
        elif response.status_code == 401:
            result["error"] = "Invalid or expired token"
        elif response.status_code == 403:
            result["error"] = "Rate limit exceeded or insufficient permissions"
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"

    except requests.exceptions.Timeout:
        result["error"] = "Request timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error - check internet connection"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"

    return result


def print_summary(results: List[Dict], verbose: bool = False):
    """Print validation summary"""
    print("\n" + "=" * 80)
    print(f"{BLUE}Token Validation Summary{NC}")
    print("=" * 80 + "\n")

    valid_count = sum(1 for r in results if r["valid"])
    failed_count = sum(
        1 for r in results if not r["valid"] and r["status"] != "planned"
    )
    planned_count = sum(1 for r in results if r["status"] == "planned")
    warning_count = sum(1 for r in results if r.get("warning"))

    print(f"  {GREEN}✓{NC} Valid:   {valid_count}/{len(results)}")
    print(f"  {RED}✗{NC} Failed:  {failed_count}/{len(results)}")
    print(f"  {YELLOW}⏳{NC} Planned: {planned_count}/{len(results)}")
    if warning_count > 0:
        print(f"  {YELLOW}⚠{NC}  Warnings: {warning_count}")

    if verbose:
        print("\n" + "-" * 80)
        print(f"{BLUE}Detailed Results:{NC}\n")
        for result in results:
            status_icon = (
                "✓"
                if result["valid"]
                else "✗" if result["status"] != "planned" else "⏳"
            )
            status_color = (
                GREEN
                if result["valid"]
                else RED if result["status"] != "planned" else YELLOW
            )

            print(f"{status_color}{status_icon}{NC} {result['token']}")
            if result["valid"]:
                print(f"    Scopes: {', '.join(result['scopes'])}")
                print(
                    f"    Rate limit: {result['rate_limit']['remaining']}/{result['rate_limit']['limit']}"  # noqa: E501
                )
                if result.get("warning"):
                    print(f"    {YELLOW}Warning: {result['warning']}{NC}")
            elif result["status"] == "planned":
                print("    Status: Not yet created")
            else:
                print(f"    Error: {result['error']}")
            print()

    return valid_count == len([r for r in results if r["status"] != "planned"])


def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="Validate organization GitHub tokens")
    parser.add_argument(
        "--token",
        help="Validate specific token only",
        choices=list(TOKENS.keys()),
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )
    parser.add_argument(
        "--ignore-planned",
        action="store_true",
        help="Don't fail if planned tokens are missing",
    )

    args = parser.parse_args()

    print(f"{BLUE}🔍 Validating organization tokens...{NC}\n")

    # Select tokens to validate
    tokens_to_validate = {args.token: TOKENS[args.token]} if args.token else TOKENS

    results = []
    for token_name, config in tokens_to_validate.items():
        print(f"Checking {token_name}...", end=" ")

        if args.verbose:
            print()

        result = validate_token(token_name, config, args.verbose)
        results.append(result)

        if not args.verbose:
            if result["valid"]:
                rate_info = f"(rate limit: {result['rate_limit']['remaining']})"
                print(f"{GREEN}✅ Valid{NC} {rate_info}")
            elif result["status"] == "planned":
                print(f"{YELLOW}⏳ Planned{NC} (not yet created)")
            else:
                print(f"{RED}❌ Failed{NC}: {result['error']}")

    # Print summary
    all_valid = print_summary(results, args.verbose)

    # Exit with appropriate code
    if not all_valid and not args.ignore_planned:
        print(f"\n{RED}⚠️  Some tokens failed validation!{NC}")
        print("Review docs/TOKEN_REGISTRY.md and rotate failed tokens.")
        print(
            "Or create planned tokens: see docs/MASTER_ORG_TOKEN_QUICK_ACTION.md"  # noqa: E501
        )
        sys.exit(1)
    elif planned_count := sum(1 for r in results if r["status"] == "planned"):
        print(
            f"\n{YELLOW}⏳ {planned_count} token(s) planned but not yet created{NC}"  # noqa: E501
        )
        print("See docs/MASTER_ORG_TOKEN_QUICK_ACTION.md for next steps")
        sys.exit(0)
    else:
        print(f"\n{GREEN}✅ All tokens are healthy!{NC}")
        sys.exit(0)


if __name__ == "__main__":
    main()

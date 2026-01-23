#!/usr/bin/env python3
"""Quick token validator using environment variables"""

import os
import sys

import requests

tokens = {
    "ORG_LABEL_SYNC_TOKEN": "org-label-sync-token",
    "ORG_PROJECT_ADMIN_TOKEN": "org-project-admin-token",
    "ORG_ONBOARDING_TOKEN": "org-onboarding-token",
    "ORG_REPO_ANALYSIS_TOKEN": "org-repo-analysis-token",
}

print("🔍 Validating tokens...\n")

valid_count = 0
failed_count = 0

for env_var, name in tokens.items():
    token = os.getenv(env_var)
    print(f"Checking {name}... ", end="", flush=True)

    if not token:
        print("❌ Not found in environment")
        failed_count += 1
        continue

    # Test with GitHub API
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {token}"},
        timeout=10,
    )

    if response.status_code == 200:
        rate_remaining = response.headers.get("X-RateLimit-Remaining", "?")
        print(f"✅ Valid (rate limit: {rate_remaining}/5000)")
        valid_count += 1
    else:
        print(f"❌ Failed: HTTP {response.status_code}")
        failed_count += 1

print(f"\n{'='*80}")
print(f"  ✓ Valid:  {valid_count}/4")
print(f"  ✗ Failed: {failed_count}/4")
print(f"{'='*80}\n")

if valid_count == 4:
    print("✅ All tokens validated! Phase 3 Day 1 Task 2 COMPLETE.\n")
    sys.exit(0)
else:
    print("⚠️  Some tokens failed. Export them first:\n")
    print("  In host terminal (outside VS Code):")
    print(
        "    op read 'op://Personal/org-label-sync-token/password' | xargs -I {} echo \"export ORG_LABEL_SYNC_TOKEN='{}'\""  # noqa: E501
    )
    print("    # ... repeat for other tokens ...")
    print("\n  Then paste the export commands here.\n")
    sys.exit(1)

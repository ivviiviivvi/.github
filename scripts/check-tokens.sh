#!/bin/bash
# Load tokens from environment variables for dev container
# Run this after copying the export commands from your host terminal

echo "🔍 Checking for GitHub tokens in environment..."
echo ""

tokens=(
    "ORG_LABEL_SYNC_TOKEN"
    "ORG_PROJECT_ADMIN_TOKEN"
    "ORG_ONBOARDING_TOKEN"
    "ORG_REPO_ANALYSIS_TOKEN"
)

found=0
missing=0

for token in "${tokens[@]}"; do
    if [[ -n "${!token}" ]]; then
        echo "  ✅ $token: Set (${!token:0:4}...)"
        ((found++))
    else
        echo "  ❌ $token: Not set"
        ((missing++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Found: $found/4"
echo "  Missing: $missing/4"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ $found -eq 4 ]]; then
    echo "✅ All tokens loaded! Ready for Phase 3 validation."
    echo ""
    echo "Run: ./scripts/validate.sh"
    exit 0
else
    echo "⚠️  Missing tokens. Get them from host terminal:"
    echo ""
    echo "In a regular terminal (outside VS Code):"
    echo ""
    echo "  op read 'op://Personal/org-label-sync-token/password' | \\"
    echo "    xargs -I {} echo \"export ORG_LABEL_SYNC_TOKEN='{}'\""
    echo "  op read 'op://Personal/org-project-admin-token/password' | \\"
    echo "    xargs -I {} echo \"export ORG_PROJECT_ADMIN_TOKEN='{}'\""
    echo "  op read 'op://Personal/org-onboarding-token/password' | \\"
    echo "    xargs -I {} echo \"export ORG_ONBOARDING_TOKEN='{}'\""
    echo "  op read 'op://Personal/org-repo-analysis-token/password' | \\"
    echo "    xargs -I {} echo \"export ORG_REPO_ANALYSIS_TOKEN='{}'\""
    echo ""
    echo "Copy and paste the export commands here."
    exit 1
fi

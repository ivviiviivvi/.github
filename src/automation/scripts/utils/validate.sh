#!/bin/bash
# Simplified Phase 3 validation - handles auth automatically
# Just run: ./scripts/validate.sh

cd "$(dirname "$0")/.."

# Try to authenticate automatically
if [[ -z "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]]; then
    # Check if already signed in
    if ! op account list &>/dev/null; then
        echo "🔐 Authenticating with 1Password..."
        eval $(op signin)
    fi
fi

echo "🔍 Running Phase 3 Day 1 validation..."
echo ""

PYTHONPATH=/workspace/automation/scripts python3 scripts/validate-tokens.py

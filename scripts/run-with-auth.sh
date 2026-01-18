#!/bin/bash
# Wrapper script that handles 1Password authentication automatically
# Usage: ./scripts/run-with-auth.sh <command>

set -euo pipefail

# Check if service account token is already set
if [[ -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]]; then
    # Already authenticated, run command directly
    exec "$@"
fi

# Check if token is in shell profile
if [[ -f "$HOME/.bashrc" ]] && grep -q "OP_SERVICE_ACCOUNT_TOKEN" "$HOME/.bashrc" 2>/dev/null; then
    source "$HOME/.bashrc"
    exec "$@"
fi

if [[ -f "$HOME/.zshrc" ]] && grep -q "OP_SERVICE_ACCOUNT_TOKEN" "$HOME/.zshrc" 2>/dev/null; then
    source "$HOME/.zshrc"
    exec "$@"
fi

# Try to use existing op session
if op account list &>/dev/null; then
    # Already signed in
    exec "$@"
fi

# Last resort: sign in interactively (but cache it)
echo "⚠️  Need to authenticate once..." >&2
eval $(op signin)
exec "$@"

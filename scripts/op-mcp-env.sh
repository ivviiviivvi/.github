#!/usr/bin/env bash
set -euo pipefail

# Load environment variables needed by MCP servers from 1Password.
#
# This script is intentionally conservative:
# - It does NOT print secret values.
# - It only exports variables into the current shell when sourced.
#
# Usage (local):
#   source scripts/op-mcp-env.sh
#   # then: Developer: Reload Window in VS Code (so extensions inherit env)
#
# Usage (non-interactive CI/Codespaces):
#   export OP_SERVICE_ACCOUNT_TOKEN=...   # from Codespaces/Actions secret
#   export OP_GITHUB_TOKEN_REF='op://Vault/Item/token'
#   source scripts/op-mcp-env.sh

die() {
  echo "error: $*" >&2
  return 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "This script must be sourced so it can export env vars into your current shell:" >&2
  echo "  source scripts/op-mcp-env.sh" >&2
  exit 2
fi

if ! command -v op >/dev/null 2>&1; then
  cat >&2 <<'TXT'
error: 1Password CLI (op) is not installed or not on PATH.

Local (recommended): install 1Password CLI from https://developer.1password.com/docs/cli/

Codespaces: you typically cannot use the desktop app integration; use 1Password
Secrets Automation and set OP_SERVICE_ACCOUNT_TOKEN as a Codespaces secret.
TXT
  return 1
fi

# In local environments, the user can be signed in via the desktop app integration.
# In Codespaces/CI, use OP_SERVICE_ACCOUNT_TOKEN.

OP_GITHUB_TOKEN_REF_DEFAULT="op://Dev/GitHub Token/token"
OP_GITHUB_TOKEN_REF="${OP_GITHUB_TOKEN_REF:-${OP_GITHUB_TOKEN_REF_DEFAULT}}"

echo "Loading MCP secrets via 1Password..." >&2
echo "- Using OP_GITHUB_TOKEN_REF=${OP_GITHUB_TOKEN_REF}" >&2

token="$(op read "$OP_GITHUB_TOKEN_REF" 2>/dev/null || true)"
if [[ -z "$token" ]]; then
  cat >&2 <<TXT
error: failed to read GitHub token from 1Password.

Tried:
  $OP_GITHUB_TOKEN_REF

Fix options:
  1) Set OP_GITHUB_TOKEN_REF to your real item reference, for example:
       export OP_GITHUB_TOKEN_REF='op://<Vault>/<Item>/<field>'

  2) If you're in Codespaces/CI, ensure OP_SERVICE_ACCOUNT_TOKEN is set and valid.

Helpful discovery commands (safe):
  op vault list
  op item list --vault '<Vault>'
  op item get '<Item>' --vault '<Vault>' --format json | head
TXT
  return 1
fi

export GITHUB_TOKEN="$token"

echo "Exported: GITHUB_TOKEN (hidden)" >&2
echo "Next: run 'Developer: Reload Window' in VS Code so MCP servers inherit the env." >&2

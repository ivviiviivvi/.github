#!/bin/bash
# Log branch deletion with SHA preservation for recovery
# Usage: ./log-branch-deletion.sh <branch-name> [pr-number] [reason]
# This script MUST be called before deleting any branch

set -e

BRANCH_NAME="${1}"
PR_NUMBER="${2:-unknown}"
REASON="${3:-manual-deletion}"

# Validate inputs
if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Branch name required"
  echo "Usage: $0 <branch-name> [pr-number] [reason]"
  exit 1
fi

# Create audit directory if it doesn't exist
AUDIT_DIR=".github/branch-deletion-audit"
mkdir -p "$AUDIT_DIR"

# Get current timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
DATE_PREFIX=$(date -u +%Y-%m)
AUDIT_FILE="$AUDIT_DIR/$DATE_PREFIX-deletions.jsonl"

# Capture branch metadata before deletion
echo "📝 Capturing branch metadata for: $BRANCH_NAME"

# Get tip commit SHA from remote
TIP_SHA=$(git ls-remote origin "refs/heads/$BRANCH_NAME" 2>/dev/null | awk '{print $1}' || echo "unknown")

if [ "$TIP_SHA" = "unknown" ] || [ -z "$TIP_SHA" ]; then
  echo "⚠️  Warning: Could not retrieve tip SHA from remote. Branch may already be deleted."
  # Try local branch if remote lookup failed
  TIP_SHA=$(git rev-parse "refs/heads/$BRANCH_NAME" 2>/dev/null || echo "already-deleted")
fi

# Get commit metadata
COMMIT_AUTHOR="unknown"
COMMIT_DATE="unknown"
COMMIT_MESSAGE="unknown"
COMMIT_PARENTS="unknown"

if [ "$TIP_SHA" != "unknown" ] && [ "$TIP_SHA" != "already-deleted" ]; then
  # Fetch commit details
  COMMIT_AUTHOR=$(git log -1 --format="%an <%ae>" "$TIP_SHA" 2>/dev/null || echo "unknown")
  COMMIT_DATE=$(git log -1 --format="%aI" "$TIP_SHA" 2>/dev/null || echo "unknown")
  COMMIT_MESSAGE=$(git log -1 --format="%s" "$TIP_SHA" 2>/dev/null | head -c 200 || echo "unknown")
  COMMIT_PARENTS=$(git log -1 --format="%P" "$TIP_SHA" 2>/dev/null || echo "unknown")
fi

# Get PR metadata if PR number provided
PR_TITLE="unknown"
PR_URL="unknown"
PR_STATE="unknown"

if [ "$PR_NUMBER" != "unknown" ] && command -v gh >/dev/null 2>&1; then
  PR_TITLE=$(gh pr view "$PR_NUMBER" --json title -q .title 2>/dev/null || echo "unknown")
  PR_URL=$(gh pr view "$PR_NUMBER" --json url -q .url 2>/dev/null || echo "unknown")
  PR_STATE=$(gh pr view "$PR_NUMBER" --json state -q .state 2>/dev/null || echo "unknown")
fi

# Create JSON record
cat >> "$AUDIT_FILE" << EOF
{"timestamp":"$TIMESTAMP","branch":"$BRANCH_NAME","tip_sha":"$TIP_SHA","pr_number":"$PR_NUMBER","pr_title":"$PR_TITLE","pr_url":"$PR_URL","pr_state":"$PR_STATE","reason":"$REASON","commit_author":"$COMMIT_AUTHOR","commit_date":"$COMMIT_DATE","commit_message":"$COMMIT_MESSAGE","commit_parents":"$COMMIT_PARENTS","deleted_by":"${GITHUB_ACTOR:-${USER:-unknown}}","repository":"${GITHUB_REPOSITORY:-unknown}"}
EOF

echo "✅ Branch metadata logged to: $AUDIT_FILE"
echo "   Branch: $BRANCH_NAME"
echo "   Tip SHA: $TIP_SHA"
echo "   PR: #$PR_NUMBER"
echo "   Reason: $REASON"

# Output SHA for caller to use
echo "$TIP_SHA"

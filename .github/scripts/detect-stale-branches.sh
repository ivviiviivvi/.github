#!/bin/bash
# Detect stale branches (14+ days without activity)
# Usage: ./detect-stale-branches.sh [owner/repo] [days]

set -e

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")}"
STALE_DAYS="${2:-14}"

# Validate inputs
if [ -z "$REPO" ]; then
  echo "Error: Repository not specified and unable to detect from current directory"
  echo "Usage: $0 <owner/repo> [days]"
  echo "Example: $0 myorg/myrepo 14"
  exit 1
fi

# Calculate stale date with better error handling
if command -v date >/dev/null 2>&1; then
  # Try GNU date first (Linux)
  STALE_DATE=$(date -d "$STALE_DAYS days ago" +%Y-%m-%d 2>/dev/null || \
               date -v -${STALE_DAYS}d +%Y-%m-%d 2>/dev/null || echo "")
else
  echo "Error: 'date' command not found"
  exit 1
fi

if [ -z "$STALE_DATE" ]; then
  echo "Error: Unable to calculate stale date. Ensure 'date' command supports -d or -v flag."
  exit 1
fi

echo "Detecting stale branches in $REPO (older than $STALE_DAYS days, before $STALE_DATE)..."
echo ""
echo "BRANCH NAME                                    LAST COMMIT DATE    AUTHOR"
echo "============================================== =================== ========================="

gh api "repos/$REPO/branches" --paginate | jq -r --arg stale_date "$STALE_DATE" '
  .[] |
  select(.commit.commit.author.date < $stale_date) |
  select(.name != "main" and .name != "master") |
  "\(.name)\t\(.commit.commit.author.date[0:10])\t\(.commit.commit.author.name)"
' | column -t -s $'\t' | head -50

echo ""
echo "Note: Showing up to 50 branches. Use --paginate for full list."
echo "Run with: $0 [owner/repo] [days]"

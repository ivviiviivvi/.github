#!/usr/bin/env bash
#
# commit_changes.sh - Automated commit and push helper
#
# Usage: commit_changes.sh <message> [files...]
#
# Environment Variables:
#   None required (uses GitHub Actions bot identity)
#

set -euo pipefail

# Configure Git
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"

# Parse arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <message> [files...]"
    echo ""
    echo "Examples:"
    echo "  $0 'Update subscriptions' .github/subscriptions.json"
    echo "  $0 'Update task queue'"
    exit 1
fi

MSG="$1"
shift

# Build file list as array for proper handling
if [ "$#" -eq 0 ]; then
    FILES=( ".github/subscriptions.json" ".github/task_queue.json" )
else
    FILES=( "$@" )
fi

# Add changes, commit, and push
# Use array expansion for proper handling of filenames with spaces
git add "${FILES[@]}"

# Check if there are changes to commit
if git diff-index --quiet HEAD; then
  echo "No changes to commit."
else
  git commit -m "$MSG"
  git push
fi

#!/bin/bash
set -e

# Configure Git
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"

# Parse arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <message> [files...]"
    exit 1
fi

MSG="$1"
shift

if [ "$#" -eq 0 ]; then
    FILES=".github/subscriptions.json .github/task_queue.json"
else
    FILES="$@"
fi

# Add changes, commit, and push
# Use array expansion for FILES if possible, but for sh compatibility string splitting is okay if no spaces in filenames
git add $FILES

# Check if there are changes to commit
if git diff-index --quiet HEAD; then
  echo "No changes to commit."
else
  git commit -m "$MSG"
  git push
fi

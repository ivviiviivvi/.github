#!/bin/bash
set -e

# Configure Git
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"

# Add changes, commit, and push
git add .github/subscriptions.json .github/task_queue.json
# Check if there are changes to commit
if git diff-index --quiet HEAD; then
  echo "No changes to commit."
else
  git commit -m "$1"
  git push
fi

#!/bin/bash

# Script to create labels for AI Rapid Development Workflow
# Run this once to set up labels in your repository

set -e

echo "🏷️  Creating labels for AI Rapid Development Workflow..."
echo ""

# Auto-merge labels
echo "Creating auto-merge labels..."
gh label create "automerge:when-ci-passes" \
  --color "0E8A16" \
  --description "Auto-merge immediately when CI passes" \
  --force || true

gh label create "automerge:after-24h" \
  --color "1D76DB" \
  --description "Auto-merge 24h after creation if CI passes" \
  --force || true

gh label create "automerge:batch" \
  --color "5319E7" \
  --description "Batch merge with related PRs" \
  --force || true

# Stale labels
echo "Creating stale labels..."
gh label create "stale:warning" \
  --color "FEF2C0" \
  --description "PR inactive 48+ hours" \
  --force || true

gh label create "stale:final-warning" \
  --color "FF9800" \
  --description "PR will be closed soon (72+ hours inactive)" \
  --force || true

# Control labels
echo "Creating control labels..."
gh label create "keep-alive" \
  --color "006B75" \
  --description "Prevent stale auto-closure" \
  --force || true

gh label create "hold" \
  --color "D93F0B" \
  --description "Temporarily block merge" \
  --force || true

gh label create "do-not-extract-tasks" \
  --color "E99695" \
  --description "Skip task extraction when PR closes" \
  --force || true

gh label create "needs-review" \
  --color "FBCA04" \
  --description "Blocks auto-merge, requires manual approval" \
  --force || true

# Task labels
echo "Creating task labels..."
gh label create "extracted-tasks" \
  --color "C5DEF5" \
  --description "Tasks extracted from closed PR" \
  --force || true

gh label create "needs-triage" \
  --color "FBCA04" \
  --description "Needs review and prioritization" \
  --force || true

gh label create "task-from-pr" \
  --color "C5DEF5" \
  --description "Issue created from PR task" \
  --force || true

# Task Catcher labels
echo "Creating Task Catcher labels..."
gh label create "has-blockers" \
  --color "D93F0B" \
  --description "PR has unresolved blocker items" \
  --force || true

gh label create "has-pending-tasks" \
  --color "FBCA04" \
  --description "PR has unchecked tasks" \
  --force || true

gh label create "ignore-task-checks" \
  --color "E99695" \
  --description "Skip task catcher blocking (use sparingly)" \
  --force || true

gh label create "create-issues-for-tasks" \
  --color "0E8A16" \
  --description "Create issues for incomplete tasks when PR merges" \
  --force || true

# Batch merge label
echo "Creating batch merge label..."
gh label create "batch-merge" \
  --color "5319E7" \
  --description "Related to batch merge operations" \
  --force || true

gh label create "automation" \
  --color "0052CC" \
  --description "Created by automation" \
  --force || true

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "Usage examples:"
echo "  gh pr create --label 'automerge:when-ci-passes'"
echo "  gh pr create --label 'automerge:after-24h'"
echo "  gh pr edit 123 --add-label 'batch:api-update'"
echo "  gh pr edit 456 --add-label 'keep-alive'"
echo ""
echo "See AI_RAPID_WORKFLOW.md for complete documentation."

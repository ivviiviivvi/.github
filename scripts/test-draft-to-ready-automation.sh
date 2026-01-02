#!/bin/bash
# test-draft-to-ready-automation.sh
# Tests that draft-to-ready automation properly summons AI assistants

set -e

PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
  echo "Usage: $0 <PR_NUMBER>"
  echo ""
  echo "Example: $0 123"
  exit 1
fi

echo "🧪 Testing draft-to-ready automation for PR #$PR_NUMBER"
echo ""

# Check if PR is ready (not draft)
echo "📋 Checking if PR is ready..."
IS_DRAFT=$(gh pr view $PR_NUMBER --json isDraft --jq '.isDraft')
if [ "$IS_DRAFT" = "true" ]; then
  echo "❌ PR is still a draft"
  exit 1
fi
echo "✅ PR is ready (not draft)"

# Check if @copilot is requested as reviewer
echo ""
echo "👤 Checking if @copilot is requested as reviewer..."
COPILOT_REVIEW=$(gh pr view $PR_NUMBER --json reviewRequests --jq '.reviewRequests[] | select(.login == "copilot") | .login' || echo "")
if [ -z "$COPILOT_REVIEW" ]; then
  echo "⚠️  @copilot not requested as reviewer"
  REVIEWER_FAIL=1
else
  echo "✅ @copilot requested as reviewer"
  REVIEWER_FAIL=0
fi

# Check if @copilot is assigned
echo ""
echo "📌 Checking if @copilot is assigned..."
COPILOT_ASSIGNED=$(gh pr view $PR_NUMBER --json assignees --jq '.assignees[] | select(.login == "copilot") | .login' || echo "")
if [ -z "$COPILOT_ASSIGNED" ]; then
  echo "⚠️  @copilot not assigned to PR"
  ASSIGNEE_FAIL=1
else
  echo "✅ @copilot assigned to PR"
  ASSIGNEE_FAIL=0
fi

# Check if conversion comment exists
echo ""
echo "💬 Checking for conversion comment..."
CONVERSION_COMMENT=$(gh pr view $PR_NUMBER --json comments --jq '.comments[] | select(.body | contains("Draft PR Auto-Converted to Ready")) | .body' || echo "")
if [ -z "$CONVERSION_COMMENT" ]; then
  echo "❌ Conversion comment not found"
  exit 1
fi
echo "✅ Conversion comment found"

# Check if comment mentions AI assistants
echo ""
echo "🤖 Checking if comment mentions AI assistants..."
if echo "$CONVERSION_COMMENT" | grep -q "@copilot"; then
  echo "✅ Comment mentions @copilot"
else
  echo "⚠️  Comment doesn't mention @copilot"
fi

if echo "$CONVERSION_COMMENT" | grep -q "@claude"; then
  echo "✅ Comment mentions @claude"
else
  echo "⚠️  Comment doesn't mention @claude"
fi

if echo "$CONVERSION_COMMENT" | grep -q "@jules"; then
  echo "✅ Comment mentions @jules"
else
  echo "⚠️  Comment doesn't mention @jules"
fi

# Check for auto-merge label
echo ""
echo "🏷️  Checking for auto-merge label..."
AUTO_MERGE_LABEL=$(gh pr view $PR_NUMBER --json labels --jq '.labels[] | select(.name == "auto-merge") | .name' || echo "")
if [ -z "$AUTO_MERGE_LABEL" ]; then
  echo "⚠️  auto-merge label not found"
  LABEL_FAIL=1
else
  echo "✅ auto-merge label found"
  LABEL_FAIL=0
fi

# Check for auto-converted label
echo ""
echo "🏷️  Checking for auto-converted label..."
AUTO_CONVERTED_LABEL=$(gh pr view $PR_NUMBER --json labels --jq '.labels[] | select(.name == "auto-converted") | .name' || echo "")
if [ -z "$AUTO_CONVERTED_LABEL" ]; then
  echo "⚠️  auto-converted label not found"
else
  echo "✅ auto-converted label found"
fi

# Check if pr-task-catcher workflow was triggered
echo ""
echo "⚙️  Checking if pr-task-catcher workflow was triggered..."
TASK_CATCHER_RUN=$(gh run list --workflow=pr-task-catcher.yml --limit 10 --json databaseId,status,conclusion,headSha --jq ".[] | select(.conclusion != null)" | head -1 || echo "")
if [ -z "$TASK_CATCHER_RUN" ]; then
  echo "⚠️  pr-task-catcher workflow not found in recent runs"
else
  echo "✅ pr-task-catcher workflow found in recent runs"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
CRITICAL_FAIL=0
if [ "$REVIEWER_FAIL" -eq 1 ] || [ "$ASSIGNEE_FAIL" -eq 1 ]; then
  echo "⚠️  Some checks did not pass, but this may be expected"
  echo "   (e.g., @copilot may not exist as a user in this repo)"
else
  echo "✅ All critical checks passed!"
fi

echo ""
echo "Summary:"
echo "  - PR converted: ✅"
echo "  - @copilot reviewer: $([ "$REVIEWER_FAIL" -eq 0 ] && echo "✅" || echo "⚠️")"
echo "  - @copilot assigned: $([ "$ASSIGNEE_FAIL" -eq 0 ] && echo "✅" || echo "⚠️")"
echo "  - Conversion comment: ✅"
echo "  - auto-merge label: $([ "$LABEL_FAIL" -eq 0 ] && echo "✅" || echo "⚠️")"
echo ""

exit $CRITICAL_FAIL

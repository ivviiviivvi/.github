# Testing Plan: Draft-to-Ready Automation Fix

## Overview
This document outlines the testing plan for validating that AI assistants are properly summoned after the `draft-to-ready-automation.yml` workflow auto-converts a draft PR to ready.

## Test Scenarios

### Scenario 1: Trusted Agent PR (Jules)
**Setup:**
1. Create a draft PR from Jules agent
2. Ensure PR has changes and passes basic validation

**Expected Behavior:**
- [ ] PR is automatically converted from draft to ready
- [ ] @copilot is requested as a reviewer
- [ ] @copilot is assigned to the PR
- [ ] `pr-task-catcher.yml` workflow is triggered and scans the PR
- [ ] Auto-merge is attempted (may queue if checks incomplete)
- [ ] PR comment is posted indicating assistants have been notified
- [ ] @claude can be summoned via comment (e.g., "@claude please review")
- [ ] @jules can be summoned via comment (e.g., "@jules please update")
- [ ] @gemini-cli can be summoned via comment (e.g., "@gemini-cli /review")
- [ ] Notification comment is posted listing all available AI assistants
- [ ] All GitHub Apps with permissions can interact with the PR

**Verification:**
```bash
# Check PR reviewers
gh pr view <PR_NUMBER> --json reviewRequests

# Check PR assignees
gh pr view <PR_NUMBER> --json assignees

# Check PR comments
gh pr view <PR_NUMBER> --json comments

# Check workflow runs
gh run list --workflow=pr-task-catcher.yml --json databaseId,status,conclusion
```

### Scenario 2: PR with auto-ready Label
**Setup:**
1. Create a draft PR manually
2. Add `auto-ready` label to the PR

**Expected Behavior:**
- [ ] Same as Scenario 1

**Verification:**
- Same as Scenario 1

### Scenario 3: Dependabot PR
**Setup:**
1. Wait for or trigger a Dependabot PR
2. Ensure it's created as a draft (if configured that way)

**Expected Behavior:**
- [ ] Same as Scenario 1

### Scenario 4: Manual PR Conversion (Baseline)
**Setup:**
1. Create a draft PR manually
2. Manually mark it as ready using GitHub UI

**Expected Behavior:**
- [ ] @copilot is requested as a reviewer (via `auto-assign.yml`)
- [ ] PR task catcher runs (via trigger on `ready_for_review`)
- [ ] This should work as before (baseline comparison)

**Verification:**
- Same as Scenario 1, but verify workflows run via event triggers, not workflow_dispatch

### Scenario 5: PR with skip-auto-ready Label
**Setup:**
1. Create a draft PR with `skip-auto-ready` label

**Expected Behavior:**
- [ ] PR remains as draft
- [ ] No automation is triggered
- [ ] PR comment is not posted

**Verification:**
```bash
# Check PR is still draft
gh pr view <PR_NUMBER> --json isDraft
```

## Automated Test

Create a test script to validate the fix:

```bash
#!/bin/bash
# test-draft-to-ready-automation.sh

set -e

PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
  echo "Usage: $0 <PR_NUMBER>"
  exit 1
fi

echo "🧪 Testing draft-to-ready automation for PR #$PR_NUMBER"

# Check if PR is ready (not draft)
IS_DRAFT=$(gh pr view $PR_NUMBER --json isDraft --jq '.isDraft')
if [ "$IS_DRAFT" = "true" ]; then
  echo "❌ PR is still a draft"
  exit 1
fi
echo "✅ PR is ready (not draft)"

# Check if @copilot is requested as reviewer
COPILOT_REVIEW=$(gh pr view $PR_NUMBER --json reviewRequests --jq '.reviewRequests[] | select(.login == "copilot") | .login')
if [ -z "$COPILOT_REVIEW" ]; then
  echo "⚠️  @copilot not requested as reviewer"
else
  echo "✅ @copilot requested as reviewer"
fi

# Check if @copilot is assigned
COPILOT_ASSIGNED=$(gh pr view $PR_NUMBER --json assignees --jq '.assignees[] | select(.login == "copilot") | .login')
if [ -z "$COPILOT_ASSIGNED" ]; then
  echo "⚠️  @copilot not assigned to PR"
else
  echo "✅ @copilot assigned to PR"
fi

# Check if conversion comment exists
CONVERSION_COMMENT=$(gh pr view $PR_NUMBER --json comments --jq '.comments[] | select(.body | contains("Draft PR Auto-Converted to Ready")) | .body')
if [ -z "$CONVERSION_COMMENT" ]; then
  echo "❌ Conversion comment not found"
  exit 1
fi
echo "✅ Conversion comment found"

# Check if comment mentions AI assistants
if echo "$CONVERSION_COMMENT" | grep -q "@copilot"; then
  echo "✅ Comment mentions @copilot"
else
  echo "⚠️  Comment doesn't mention @copilot"
fi

# Check for auto-merge label
AUTO_MERGE_LABEL=$(gh pr view $PR_NUMBER --json labels --jq '.labels[] | select(.name == "auto-merge") | .name')
if [ -z "$AUTO_MERGE_LABEL" ]; then
  echo "⚠️  auto-merge label not found"
else
  echo "✅ auto-merge label found"
fi

echo ""
echo "✅ All critical checks passed!"
```

## Manual Verification Checklist

After the workflow runs:

- [ ] Check GitHub Actions logs for `draft-to-ready-automation.yml`
- [ ] Verify "Trigger Auto-Assign Workflow" step succeeded
- [ ] Verify "Trigger PR Task Catcher" step succeeded
- [ ] Verify "Enable Auto-Merge via GitHub CLI" step ran (may fail if checks incomplete)
- [ ] Check that PR has conversion comment
- [ ] Check that PR has `auto-merge` and `auto-converted` labels
- [ ] Try summoning @claude with a comment: "@claude please review this PR"
- [ ] Try summoning @jules with a comment: "@jules what do you think?"
- [ ] Verify that these assistants respond

## Performance Considerations

The new steps add approximately 10-15 seconds to the workflow execution time:
- Requesting reviewers: ~2-3 seconds
- Assigning assignee: ~2-3 seconds
- Triggering workflow_dispatch: ~3-5 seconds
- Attempting auto-merge: ~2-4 seconds

This is acceptable overhead for the improved functionality.

## Rollback Plan

If the fix causes issues:

1. Revert the changes to `draft-to-ready-automation.yml`
2. Remove the new steps (Trigger Auto-Assign, Trigger PR Task Catcher, Enable Auto-Merge)
3. Restore the original PR comment text
4. The workflow will still convert drafts, but assistants won't be summoned automatically

## Success Criteria

The fix is considered successful if:

1. ✅ PRs are converted from draft to ready as before
2. ✅ @copilot is requested as a reviewer for all auto-converted PRs
3. ✅ PR task catcher workflow runs for all auto-converted PRs
4. ✅ @claude, @jules, and other assistants can be summoned on auto-converted PRs
5. ✅ No regressions in existing functionality
6. ✅ No errors in workflow logs

## Notes

- The fix is non-breaking and maintains backwards compatibility
- Manual PR conversions (via UI) continue to work as before
- The fix only affects PRs auto-converted by the workflow
- Error handling ensures partial failures don't break the workflow

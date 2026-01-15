# Workflow Testing Guide

> **Complete testing scenarios for validating the workflow system**

**Purpose:** Ensure all workflow automations function correctly before
production deployment\
**Environment:** Sandbox/Test Repository\
**Duration:**
2-3 hours for complete test suite

---

## 📋 Prerequisites

Before testing:

- [ ] Sandbox repository created
- [ ] Workflow files copied to `.github/workflows/`
- [ ] CODEOWNERS file configured
- [ ] Labels configured (or use GitHub defaults)
- [ ] GitHub Actions enabled
- [ ] Workflow permissions: Read & Write
- [ ] Test user accounts available (optional, for multi-user tests)

---

## 🧪 Test Scenarios

### Test Suite 1: Issue Triage Automation

**File:** `.github/workflows/issue-triage.yml`

#### Test 1.1: Auto-Label on Issue Creation

**Objective:** Verify `needs-triage` label is added to new issues

**Steps:**

1. Create new issue (any template or no template)
1. Submit the issue

**Expected Results:**

- ✅ Issue created successfully
- ✅ `needs-triage` label added automatically (within 1 minute)
- ✅ Automation comment posted with triage instructions
- ✅ Workflow run shows success in Actions tab

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Notes:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 1.2: Content-Based Auto-Labeling

**Objective:** Verify issues are labeled based on content keywords

**Test 1.2a: Bug Detection**

**Steps:**

1. Create issue with title: "Bug: Login fails with error 500"
1. Body: "Getting error when trying to log in. Server returns 500."

**Expected Results:**

- ✅ `type: bug` label added
- ✅ `needs-triage` label present

**Actual Results:**

- [ ] Pass | \[ \] Fail

**Test 1.2b: Feature Detection**

**Steps:**

1. Create issue with title: "Feature: Add dark mode support"
1. Body: "It would be great to have dark mode as a feature"

**Expected Results:**

- ✅ `type: feature` label added

**Actual Results:**

- [ ] Pass | \[ \] Fail

**Test 1.2c: Security Detection**

**Steps:**

1. Create issue with title: "Security: SQL injection in search"
1. Body: "Found security vulnerability in search function"

**Expected Results:**

- ✅ `type: security` label added
- ✅ `priority: critical` label added (if configured)

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 1.3: Triage Completion

**Objective:** Verify `needs-triage` is removed when type/priority/status labels
added

**Steps:**

1. Create issue (gets `needs-triage`)
1. Manually add labels:
   - `type: bug`
   - `priority: high`
   - `status: backlog`

**Expected Results:**

- ✅ `needs-triage` label removed automatically (within 1 minute)
- ✅ Triage completion comment posted

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Notes:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 1.4: SLA Enforcement

**Objective:** Verify 48-hour triage SLA tracking

**Steps:**

1. Create issue
1. Do NOT triage it (leave `needs-triage`)
1. Wait 48+ hours OR manually set issue creation date to 48+ hours ago (via API)
1. Trigger workflow manually or wait for scheduled run

**Expected Results:**

- ✅ SLA violation comment posted
- ✅ `needs-attention` label added
- ✅ Maintainers mentioned in comment

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Notes:** \_\_\_\_\_\_\_\_\_\_\_

---

### Test Suite 2: Auto-Assign Reviewers

**File:** `.github/workflows/auto-assign-reviewers.yml`

#### Test 2.1: Reviewer Assignment on PR Creation

**Objective:** Verify reviewers assigned based on CODEOWNERS

**Setup:** Create CODEOWNERS file:

```
# Example CODEOWNERS
*.md @doc-team
*.py @python-team
*.js @frontend-team
src/api/ @backend-team
```

**Steps:**

1. Create branch
1. Modify file: `README.md`
1. Create PR

**Expected Results:**

- ✅ PR created successfully
- ✅ `@doc-team` assigned as reviewer
- ✅ `awaiting-review` label added
- ✅ PR author NOT assigned as reviewer

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Reviewers assigned:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 2.2: Multiple Files Multiple Reviewers

**Objective:** Verify multiple reviewers assigned for multi-file PRs

**Steps:**

1. Create branch
1. Modify files:
   - `README.md` (owned by @doc-team)
   - `src/api/handler.py` (owned by @backend-team)
1. Create PR

**Expected Results:**

- ✅ Both `@doc-team` and `@backend-team` assigned
- ✅ No duplicate assignments
- ✅ `awaiting-review` label added

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Reviewers assigned:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 2.3: Draft PR (No Assignment)

**Objective:** Verify reviewers NOT assigned to draft PRs

**Steps:**

1. Create branch with changes
1. Create PR as DRAFT

**Expected Results:**

- ✅ No reviewers assigned
- ✅ `draft` label added (if configured)
- ✅ `awaiting-review` label NOT added

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 2.4: Draft to Ready Transition

**Objective:** Verify reviewers assigned when draft becomes ready

**Steps:**

1. Create draft PR (no reviewers assigned)
1. Click "Ready for review"

**Expected Results:**

- ✅ Reviewers assigned based on CODEOWNERS
- ✅ `awaiting-review` label added
- ✅ Workflow triggered on `ready_for_review` event

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Test Suite 3: Status Sync

**File:** `.github/workflows/status-sync.yml`

#### Test 3.1: PR to Issue Sync

**Objective:** Verify issue status updates when PR is created

**Steps:**

1. Create issue (e.g., #42)
1. Create branch
1. Create PR with body: "Fixes #42"

**Expected Results:**

- ✅ Issue #42 labeled with `has-pr`
- ✅ Comment added to issue linking to PR
- ✅ Issue status updated to `status: in-progress`

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Issue labels:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 3.2: PR Draft to Ready Status Sync

**Objective:** Verify issue updates when PR transitions

**Steps:**

1. Create issue #43
1. Create draft PR with "Fixes #43"
1. Mark PR ready for review

**Expected Results:**

- ✅ Issue comment: "PR is now ready for review"
- ✅ Issue labels updated

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 3.3: PR Merge Closes Issue

**Objective:** Verify issue closes when PR merges

**Steps:**

1. Create issue #44
1. Create PR with "Fixes #44"
1. Approve and merge PR

**Expected Results:**

- ✅ Issue #44 automatically closed
- ✅ Closing comment references merged PR
- ✅ Issue labeled with `completed` or `merged` (if configured)

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 3.4: Multiple Issues One PR

**Objective:** Verify multiple issues are linked and closed

**Steps:**

1. Create issues #45, #46, #47

1. Create PR with body:

   ```
   Fixes #45
   Fixes #46
   Closes #47
   ```

1. Merge PR

**Expected Results:**

- ✅ All three issues closed
- ✅ All three issues have PR link comments
- ✅ All statuses synced

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Test Suite 4: Stale Management

**File:** `.github/workflows/stale-management.yml`

#### Test 4.1: Stale Issue Detection

**Objective:** Verify issues are marked stale after 90 days

**Steps:**

1. Create issue
1. Set creation date to 90+ days ago (via API or wait)
1. Trigger workflow manually

**Expected Results:**

- ✅ `stale` label added
- ✅ Comment posted: "This issue is stale. Reply to keep it open."
- ✅ 7-day grace period mentioned

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Grace period ends:** \_\_\_\_\_\_\_\_\_\_\_

---

#### Test 4.2: Stale Issue Reactivation

**Objective:** Verify commenting removes stale label

**Steps:**

1. Create stale issue (from Test 4.1)
1. Add any comment

**Expected Results:**

- ✅ `stale` label removed automatically
- ✅ Issue stays open

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 4.3: Stale Issue Closure

**Objective:** Verify stale issues close after grace period

**Steps:**

1. Create issue marked stale
1. Wait 7+ days without activity (or adjust workflow for testing)
1. Trigger workflow

**Expected Results:**

- ✅ Issue closed automatically
- ✅ Closing comment explains why

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 4.4: Stale PR Detection (30 days)

**Objective:** Verify PRs are marked stale faster than issues

**Steps:**

1. Create PR
1. Set creation date to 30+ days ago
1. Trigger workflow

**Expected Results:**

- ✅ `stale` label added
- ✅ Comment posted
- ✅ 7-day grace period

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 4.5: Exempt Labels

**Objective:** Verify certain labels exempt items from stale detection

**Setup:** Configure in workflow:

```yaml
exempt-issue-labels: "pinned, security, long-term"
```

**Steps:**

1. Create issue with `pinned` label
1. Set date to 90+ days ago
1. Trigger workflow

**Expected Results:**

- ✅ Issue NOT marked stale
- ✅ `pinned` label prevents stale detection

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Test Suite 5: Assignment Warnings

**File:** `.github/workflows/stale-management.yml` (included)

#### Test 5.1: 14-Day Inactivity Warning

**Objective:** Verify assignees warned after 14 days of inactivity

**Steps:**

1. Create issue
1. Assign to user
1. Set assignment date to 14+ days ago
1. Ensure no activity since assignment
1. Trigger workflow

**Expected Results:**

- ✅ Comment posted mentioning assignee
- ✅ Warning: "Assigned 14 days ago with no activity"
- ✅ Asks assignee to update or unassign

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 5.2: 21-Day Auto-Unassign

**Objective:** Verify auto-unassignment after 21 days

**Steps:**

1. Create assigned issue from Test 5.1
1. Wait 7 more days (21 total)
1. Trigger workflow

**Expected Results:**

- ✅ Assignee removed
- ✅ Comment explains auto-unassignment
- ✅ Issue returned to backlog

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

#### Test 5.3: Activity Resets Timer

**Objective:** Verify any activity resets the inactivity timer

**Steps:**

1. Create assigned issue (14+ days old)
1. Assignee adds a comment
1. Trigger workflow

**Expected Results:**

- ✅ No warning posted
- ✅ Timer reset by activity

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

## 📊 Integration Tests

### Integration Test 1: Full Contributor Flow

**Objective:** Validate entire contribution lifecycle

**Steps:**

1. Create issue (auto-triaged)
1. Maintainer adds type/priority (triage complete)
1. Contributor requests assignment
1. Maintainer assigns
1. Contributor creates PR with "Fixes #X"
1. Reviewers auto-assigned
1. PR approved
1. PR merged
1. Issue closes

**Expected Results:**

- ✅ Each step triggers appropriate automation
- ✅ Labels update correctly throughout
- ✅ Status syncs between issue and PR
- ✅ No manual intervention required except approval

**Actual Results:**

- [ ] Pass | \[ \] Fail
- **Issues encountered:** \_\_\_\_\_\_\_\_\_\_\_

---

### Integration Test 2: Stale to Reactivation

**Objective:** Validate stale lifecycle

**Steps:**

1. Issue becomes stale (90 days)
1. Contributor comments (reactivated)
1. Work continues
1. PR created and merged
1. Issue closes successfully

**Expected Results:**

- ✅ Stale label removed on reactivation
- ✅ Normal flow continues
- ✅ No issues with stale history

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Integration Test 3: Multi-Reviewer Flow

**Objective:** Validate complex CODEOWNERS scenarios

**Steps:**

1. Create PR touching files owned by 3 different teams
1. Verify all teams assigned
1. Each team approves
1. PR merges when all approvals received

**Expected Results:**

- ✅ All reviewers assigned correctly
- ✅ Approvals tracked
- ✅ Merge blocked until all approve (if branch protection set)

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

## 🔍 Edge Cases & Negative Tests

### Edge Case 1: Malformed PR Body

**Steps:**

1. Create PR with body: "This fixes issue 123" (no #)

**Expected Results:**

- ✅ Workflow handles gracefully
- ✅ No crash
- ⚠️ May not link issue (expected)

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Edge Case 2: Issue Already Closed

**Steps:**

1. Create issue
1. Close issue manually
1. Create PR with "Fixes #X"
1. Merge PR

**Expected Results:**

- ✅ No error
- ✅ Issue stays closed
- ✅ PR merged successfully

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Edge Case 3: PR Without CODEOWNERS Match

**Steps:**

1. Create PR touching files not in CODEOWNERS

**Expected Results:**

- ✅ Workflow runs successfully
- ⚠️ No reviewers assigned (expected)
- ✅ `awaiting-review` label still added

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

### Edge Case 4: PR Author in CODEOWNERS

**Steps:**

1. User creates PR for file they own in CODEOWNERS

**Expected Results:**

- ✅ User NOT assigned as own reviewer
- ✅ Other owners assigned (if multiple)

**Actual Results:**

- [ ] Pass | \[ \] Fail

---

## 📋 Test Results Summary

### Overall Statistics

**Total Tests:** 30\
**Passed:** \_\_\_\
**Failed:**\_\_\_\
**Skipped:**
\_\_\_\
**Pass Rate:**\_\_\_%

### Critical Failures

\[List any critical issues that block deployment\]

| Test | Issue | Impact | Severity |
| ---- | ----- | ------ | -------- |
|      |       |        |          |

### Non-Critical Issues

\[List minor issues that can be addressed post-deployment\]

| Test | Issue | Workaround |
| ---- | ----- | ---------- |
|      |       |            |

---

## ✅ Sign-Off

- [ ] All critical tests passed
- [ ] Edge cases documented
- [ ] Known issues documented
- [ ] Workarounds identified
- [ ] Ready for production deployment

**Tester:** @\_\_\_\_\_\_\_\_\_\_\_\
**Date:** YYYY-MM-DD\
**Environment:**
Sandbox Repository\
**Workflow Versions:**

- issue-triage.yml: v\_\_\_
- auto-assign-reviewers.yml: v\_\_\_
- status-sync.yml: v\_\_\_
- stale-management.yml: v\_\_\_

**Recommendation:** \[ \] Approve for Production | \[ \] Fix Critical Issues |
\[ \] Retest Required

**Notes:**

---

---

## 🔄 Retest Checklist

If retesting after fixes:

- [ ] Review changed workflow files
- [ ] Identify affected tests
- [ ] Rerun failed tests
- [ ] Verify fixes work
- [ ] Check no regressions
- [ ] Update test results
- [ ] Get new sign-off

---

_Last Updated: January 15, 2026_

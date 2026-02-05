______________________________________________________________________

## name: Workflow System Deployment about: Deploy the new discussion/issue/PR workflow system title: "Deploy Workflow System: \[Environment\]" labels: type: infrastructure, priority: high, status: backlog assignees: ''

# Workflow System Deployment Checklist

**Environment:** \[Sandbox / Staging / Production\] **Target Date:** YYYY-MM-DD
**Owner:** @username

______________________________________________________________________

## 📋 Pre-Deployment

### Documentation Review

- [ ] Read [WORKFLOW_DESIGN.md](../../docs/WORKFLOW_DESIGN.md) - Architecture
  overview
- [ ] Review
  [WORKFLOW_IMPLEMENTATION_SUMMARY.md](../../docs/WORKFLOW_IMPLEMENTATION_SUMMARY.md)
  \- Deployment guide
- [ ] Check [CONTRIBUTOR_WORKFLOW.md](../../docs/CONTRIBUTOR_WORKFLOW.md) -
  User-facing guide
- [ ] Read [MAINTAINER_WORKFLOW.md](../../docs/MAINTAINER_WORKFLOW.md) -
  Operations guide

### Environment Preparation

- [ ] Verify GitHub Actions enabled for repository
- [ ] Confirm workflow permissions: Read & Write
- [ ] Check secrets/tokens configured if needed
- [ ] Review branch protection settings
- [ ] Ensure CODEOWNERS file exists and is accurate

______________________________________________________________________

## 🧪 Sandbox Testing (Required First)

### Create Test Repository

- [ ] Create sandbox repository (e.g., `.github-workflow-test`)
- [ ] Copy workflow files from `.github/workflows/`:
  - [ ] `issue-triage.yml`
  - [ ] `auto-assign-reviewers.yml`
  - [ ] `status-sync.yml`
  - [ ] `stale-management.yml`
- [ ] Copy `.github/CODEOWNERS` file
- [ ] Copy label configuration (or use default labels)

### Test Issue Workflows

- [ ] **Test 1**: Create test issue without template
  - [ ] Verify `needs-triage` label added
  - [ ] Check automation comment posted
- [ ] **Test 2**: Add type/priority labels manually
  - [ ] Verify `needs-triage` removed automatically
  - [ ] Check `status: backlog` added
- [ ] **Test 3**: Test stale issue detection
  - [ ] Create issue, set date to 90+ days ago (or adjust workflow)
  - [ ] Run workflow manually
  - [ ] Verify stale label added

### Test PR Workflows

- [ ] **Test 4**: Create test PR
  - [ ] Verify reviewers assigned based on CODEOWNERS
  - [ ] Check `awaiting-review` label added
- [ ] **Test 5**: Link PR to issue
  - [ ] Add "Fixes #123" to PR description
  - [ ] Verify status sync between issue and PR
- [ ] **Test 6**: Test PR lifecycle
  - [ ] Mark as draft → check labels update
  - [ ] Mark ready for review → check labels update
  - [ ] Approve → check labels update
  - [ ] Merge → verify issue closes

### Test SLA Enforcement

- [ ] **Test 7**: Create issue, wait 48+ hours (or adjust workflow)
  - [ ] Verify SLA warning comment added
  - [ ] Check `needs-attention` label
- [ ] **Test 8**: Test assignment warnings (14 days)
  - [ ] Assign issue, wait 14+ days (or adjust)
  - [ ] Verify warning comment
- [ ] **Test 9**: Test auto-unassign (21 days)
  - [ ] Wait additional 7 days
  - [ ] Verify auto-unassignment

### Document Test Results

- [ ] All workflows executed without errors
- [ ] Labels applied correctly
- [ ] Comments posted as expected
- [ ] SLA timers working
- [ ] Status sync functioning
- [ ] No false positives or unexpected behavior

**Test Summary:**

```
Pass: X/9
Fail: X/9
Issues Found: [List any issues]
```

______________________________________________________________________

## 🔒 Branch Protection Configuration

- [ ] Navigate to: Settings → Branches → Branch protection rules

- [ ] Add rule for `main` (or default branch):

  - [ ] ✅ Require a pull request before merging
  - [ ] ✅ Require approvals: 1 (minimum)
  - [ ] ✅ Dismiss stale pull request approvals when new commits are pushed
  - [ ] ✅ Require review from Code Owners
  - [ ] ✅ Require status checks to pass before merging
    - Add checks: `lint`, `test`, `build` (as applicable)
  - [ ] ✅ Require branches to be up to date before merging
  - [ ] ✅ Require conversation resolution before merging
  - [ ] ✅ Include administrators (optional)

- [ ] Test branch protection:

  - [ ] Try to push directly to main → should fail
  - [ ] Create PR without approval → should not merge
  - [ ] Create PR without required checks → should not merge

______________________________________________________________________

## 🚀 Production Deployment

### Phase 1: Passive Workflows (Week 1)

Enable workflows that only add labels/comments, no closures:

- [ ] Deploy `issue-triage.yml`
  - Workflow URL: `.github/workflows/issue-triage.yml`
  - Status: ⬜ Not Started | 🟡 In Progress | ✅ Complete
- [ ] Deploy `auto-assign-reviewers.yml`
  - Workflow URL: `.github/workflows/auto-assign-reviewers.yml`
  - Status: ⬜ Not Started | 🟡 In Progress | ✅ Complete
- [ ] Deploy `status-sync.yml`
  - Workflow URL: `.github/workflows/status-sync.yml`
  - Status: ⬜ Not Started | 🟡 In Progress | ✅ Complete

#### Week 1 Monitoring

- [ ] Day 1: Check first 10 issues/PRs for correct labeling
- [ ] Day 3: Review workflow run logs for errors
- [ ] Day 5: Survey 3-5 contributors for feedback
- [ ] Day 7: Compile metrics:
  - Issues triaged: \_\_\_
  - PRs auto-assigned: \_\_\_
  - Status syncs: \_\_\_
  - Errors: \_\_\_

### Phase 2: Active Workflows (Week 2)

Enable workflows that take action (stale management):

- [ ] Deploy `stale-management.yml`
  - Workflow URL: `.github/workflows/stale-management.yml`
  - Status: ⬜ Not Started | 🟡 In Progress | ✅ Complete
  - **Note:** Review and adjust timers before enabling:
    - `days-before-issue-stale`: Currently 90
    - `days-before-pr-stale`: Currently 30
    - `days-before-close`: Currently 7

#### Week 2 Monitoring

- [ ] Day 8: Review stale candidates before any closures
- [ ] Day 10: Check for false positives in stale detection
- [ ] Day 12: Monitor community feedback on auto-closures
- [ ] Day 14: Compile phase 2 metrics:
  - Items marked stale: \_\_\_
  - Items closed: \_\_\_
  - Items reactivated: \_\_\_
  - Community complaints: \_\_\_

______________________________________________________________________

## 📚 Documentation Updates

- [ ] Update repository README with workflow info
- [ ] Add workflow badges to README (optional)
- [ ] Update CONTRIBUTING.md with new process
- [ ] Create or update project wiki with workflow guide
- [ ] Post announcement in Discussions
- [ ] Update issue templates with workflow references

______________________________________________________________________

## 👥 Team Training

### Maintainer Training (30-60 minutes)

- [ ] Schedule training session
- [ ] Cover key topics:
  - [ ] How automation works
  - [ ] Manual intervention points
  - [ ] Monitoring workflows
  - [ ] Handling edge cases
- [ ] Walk through [MAINTAINER_WORKFLOW.md](../../docs/MAINTAINER_WORKFLOW.md)
- [ ] Q&A session
- [ ] Record session for future reference

### Contributor Communication

- [ ] Post announcement in Discussions
- [ ] Update new issue template with workflow info
- [ ] Add comment template for explaining workflow to confused users
- [ ] Create FAQ for common questions

**Training Dates:**

- Maintainer training: YYYY-MM-DD at HH:MM
- Announcement posted: YYYY-MM-DD
- FAQ published: YYYY-MM-DD

______________________________________________________________________

## 📊 Metrics & Monitoring

### Setup Monitoring Dashboard

- [ ] Enable workflow run notifications
- [ ] Set up metrics collection (see below for workflow)
- [ ] Configure alerts for workflow failures
- [ ] Schedule weekly review meetings

### Key Metrics to Track

- Issues triaged within 48 hours: \_\_\_\_%
- PRs with reviewers assigned automatically: \_\_\_\_%
- Average time to first review: \_\_\_ hours
- Stale items identified: \_\_\_
- False positive rate: \_\_\_\_%
- Contributor satisfaction: \_\_\_/5

**Review Schedule:**

- Daily: Check workflow runs for errors
- Weekly: Review metrics dashboard
- Monthly: Analyze trends and adjust

______________________________________________________________________

## ✅ Validation

### Smoke Tests (Post-Deployment)

- [ ] Create new issue → verify auto-labeling
- [ ] Create new PR → verify reviewer assignment
- [ ] Link PR to issue → verify status sync
- [ ] Check stale management scheduled run
- [ ] Review workflow logs for errors

### User Acceptance

- [ ] Poll 5 contributors: "How is the new workflow?"
- [ ] Review Discussions for workflow-related questions
- [ ] Check for confusion or complaints
- [ ] Document common questions for FAQ

**Validation Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Issues
Found

______________________________________________________________________

## 🐛 Issues & Rollback

### Known Issues

\[Document any issues discovered during deployment\]

| Issue | Severity | Status | Workaround |
| ----- | -------- | ------ | ---------- |
|       |          |        |            |

### Rollback Plan

If critical issues arise:

1. Disable problematic workflow(s) via GitHub UI
1. Document the issue
1. Fix and re-test in sandbox
1. Re-deploy when ready

**Rollback Executed?** ⬜ No | ✅ Yes **Reason:** \_\_\_\_\_\_\_\_\_\_\_
**Re-deployment Date:** YYYY-MM-DD

______________________________________________________________________

## 📝 Post-Deployment

- [ ] Mark deployment as complete
- [ ] Archive sandbox test repository
- [ ] Update documentation with lessons learned
- [ ] Schedule 30-day retrospective
- [ ] Create follow-up issues for improvements

**Retrospective Date:** YYYY-MM-DD **Lessons Learned:** \[Link to doc\]

______________________________________________________________________

## 📋 Sign-off

- [ ] Technical Lead: @\_\_\_\_\_\_\_\_\_\_\_ (Date: \_\_\_\_\_\_)
- [ ] Product Owner: @\_\_\_\_\_\_\_\_\_\_\_ (Date: \_\_\_\_\_\_)
- [ ] Deployment successful and stable

______________________________________________________________________

**Deployment Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete | ❌ Failed

**Notes:** \[Add any additional notes here\]

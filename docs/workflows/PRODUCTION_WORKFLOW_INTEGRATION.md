# Production Workflow Integration Guide

## Adding Slack Notifications to Existing Workflows

**Date:** February 17, 2026\
**Purpose:** Step-by-step code changes for Week 5
deployment\
**Target:** February 18, 2026, 2:30 PM UTC

______________________________________________________________________

## 📋 Overview

This guide provides the **exact code changes** needed to integrate Slack
notifications into all five production workflows. Each workflow requires adding
one or more notification steps using our new `slack-notify` composite action.

**Workflows to Update:**

1. issue-triage.yml (P1 on failure)
1. auto-assign-reviewers.yml (P1 on failure)
1. status-sync.yml (P2 on failure)
1. stale-management.yml (P2 on failure)
1. workflow-metrics.yml (P3 on success, P2 on failure)

______________________________________________________________________

## 🎯 Integration Pattern

All integrations follow this pattern:

```yaml
- name: Notify Slack on [Condition]
  if: [condition]
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: [P0|P1|P2|P3]
    title: "[Workflow Name] - [Status]"
    message: "Description of what happened"
    workflow: workflow-name
    status: [success|failure|warning]
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

______________________________________________________________________

## 1️⃣ issue-triage.yml

### Current Last Step

```yaml
- name: Comment on issue
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ This issue has been automatically triaged and labeled.'
      })
```

### Add After Last Step

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P1
    title: "Issue Triage Workflow Failed"
    message: "The issue triage workflow encountered an error and could not complete. New issues may not be automatically triaged and labeled."
    workflow: issue-triage
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Rationale:** P1 (high priority) because failure means new issues won't be
automatically triaged, requiring manual intervention.

______________________________________________________________________

## 2️⃣ auto-assign-reviewers.yml

### Current Last Step

```yaml
- name: Assign reviewers
  uses: actions/github-script@v7
  with:
    script: |
      const reviewers = ['user1', 'user2'];
      github.rest.pulls.requestReviewers({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: context.issue.number,
        reviewers: reviewers
      })
```

### Add After Last Step

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P1
    title: "Auto-Assign Reviewers Failed"
    message: "The reviewer assignment workflow failed. Pull requests are not receiving automatic reviewer assignments. Check CODEOWNERS file and workflow permissions."
    workflow: auto-assign-reviewers
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Rationale:** P1 (high priority) because PRs need timely reviews. Failure
blocks the review process.

______________________________________________________________________

## 3️⃣ status-sync.yml

### Current Last Step

```yaml
- name: Update PR status
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.repos.createCommitStatus({
        owner: context.repo.owner,
        repo: context.repo.repo,
        sha: context.sha,
        state: 'success',
        context: 'status-sync'
      })
```

### Add After Last Step

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P2
    title: "Status Sync Workflow Failed"
    message: "The PR status synchronization workflow encountered errors. Some PRs may have outdated or missing status checks. Review workflow logs for details."
    workflow: status-sync
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Rationale:** P2 (medium priority) because status sync failures don't block
development, but should be addressed within a few hours.

______________________________________________________________________

## 4️⃣ stale-management.yml

### Current Last Step

```yaml
- name: Close stale issues
  uses: actions/stale@v9
  with:
    days-before-stale: 60
    days-before-close: 7
    stale-issue-label: "stale"
    stale-issue-message: "This issue has been marked as stale..."
```

### Add After Last Step

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P2
    title: "Stale Management Workflow Failed"
    message: "The stale issue/PR management workflow failed. Stale items may not be automatically processed. This is a maintenance task and does not require immediate action."
    workflow: stale-management
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Rationale:** P2 (medium priority) because stale management is maintenance.
Failure is not urgent but should be fixed.

______________________________________________________________________

## 5️⃣ workflow-metrics.yml

### Current Last Step

```yaml
- name: Upload metrics
  uses: actions/upload-artifact@v4
  with:
    name: workflow-metrics
    path: metrics.json
```

### Add TWO Steps After Last Step

```yaml
- name: Notify Slack on Success
  if: success()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P3
    title: "Workflow Metrics Collection Complete"
    message: "Successfully collected and uploaded workflow performance metrics."
    workflow: workflow-metrics
    status: success
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}

- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P2
    title: "Workflow Metrics Collection Failed"
    message: "Failed to collect workflow metrics. Performance tracking may be incomplete. Check workflow logs for errors."
    workflow: workflow-metrics
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Rationale:**

- P3 for success (won't send to Slack, dashboard only - reduces noise)
- P2 for failure (metrics are important but not urgent)

______________________________________________________________________

## 🔧 Deployment Commands

### Using Git Command Line

```bash
# 1. Ensure you're on main branch
git checkout main
git pull origin main

# 2. Create deployment branch (optional but recommended)
git checkout -b deploy/week5-slack-integration

# 3. Edit each workflow file (see sections above)
# For each file:
#   - Open in editor
#   - Add notification step(s) at the end
#   - Save file

# 4. Verify changes
git diff

# 5. Commit changes
git add .github/workflows/issue-triage.yml
git add .github/workflows/auto-assign-reviewers.yml
git add .github/workflows/status-sync.yml
git add .github/workflows/stale-management.yml
git add .github/workflows/workflow-metrics.yml

git commit -m "feat: integrate Slack notifications in all production workflows

- Add P1 failure notifications to issue-triage.yml
- Add P1 failure notifications to auto-assign-reviewers.yml
- Add P2 failure notifications to status-sync.yml
- Add P2 failure notifications to stale-management.yml
- Add P3 success + P2 failure notifications to workflow-metrics.yml

All workflows now send real-time alerts to #workflow-alerts
based on priority (P0/P1/P2) and skip P3 (success) to reduce noise.

Implements Week 5 Slack Integration Phase 2.
Related: SLACK_INTEGRATION_TRAINING.md, SLACK_INTEGRATION_CONFIGURATION.md"

# 6. Push to remote (or create PR)
git push origin deploy/week5-slack-integration

# OR push directly to main (if approved)
git checkout main
git merge deploy/week5-slack-integration
git push origin main
```

### Using GitHub Web Interface

1. Navigate to each workflow file in `.github/workflows/`
1. Click "Edit" button
1. Scroll to bottom of file
1. Add the notification step(s) from sections above
1. Click "Commit changes"
1. Repeat for all 5 workflows

______________________________________________________________________

## ✅ Pre-Deployment Checklist

Before deploying these changes, ensure:

### Secrets Configuration

- [ ] `SLACK_WEBHOOK_ALERTS` secret exists in repository settings
- [ ] `SLACK_WEBHOOK_METRICS` secret exists in repository settings
- [ ] Both webhooks tested with curl (return 200 OK)
- [ ] Webhooks point to correct Slack channels

### Slack Channels

- [ ] #workflow-alerts channel exists
- [ ] #workflow-metrics channel exists
- [ ] Team members joined both channels (>80%)
- [ ] Channel topics and descriptions set

### Testing

- [ ] Test workflow (`test-slack-notifications.yml`) runs successfully
- [ ] P0 test notification received with @channel
- [ ] P1 test notification received with @here
- [ ] P2 test notification received (no mention)
- [ ] P3 test did NOT send to Slack (correct behavior)
- [ ] Daily summary workflow tested manually

### Documentation

- [ ] Team completed training session
- [ ] Configuration guide reviewed
- [ ] Deployment checklist in progress
- [ ] On-call rotation defined for P0/P1 alerts

______________________________________________________________________

## 🧪 Post-Deployment Validation

After deploying, validate the integration:

### Immediate (First 5 Minutes)

1. **Trigger a test failure:**

   ```bash
   # Manually fail a workflow to test notification
   # OR wait for natural workflow execution
   ```

1. **Check Slack:**

   - Did notification appear in #workflow-alerts?
   - Was priority level correct?
   - Was mention appropriate (@channel/@here/none)?
   - Did "View Details" button work?

### First Hour

1. **Monitor all workflows:**

   - Watch GitHub Actions dashboard
   - Track any workflow executions
   - Verify notifications sent (or not sent for P3)

1. **Team feedback:**

   - Ask in #workflow-alerts if anyone sees issues
   - Check for duplicate notifications
   - Verify message clarity

### First Day

1. **Check daily summary:**

   - Wait for 9 AM UTC next day
   - Verify summary posted to #workflow-metrics
   - Validate metrics accuracy

1. **Review metrics:**

   - Notification delivery rate
   - Response times to P1 alerts
   - Any false positives

______________________________________________________________________

## 🚨 Rollback Procedure

If critical issues arise:

### Quick Rollback (5 minutes)

```bash
# Revert the commit
git revert <commit-hash>
git push origin main

# OR restore previous versions
git checkout <previous-commit> -- .github/workflows/
git commit -m "revert: temporarily disable Slack notifications"
git push origin main
```

### Partial Rollback

If only one workflow has issues:

```bash
# Restore single workflow
git checkout <previous-commit> -- .github/workflows/issue-triage.yml
git commit -m "revert: disable Slack for issue-triage temporarily"
git push origin main
```

### Communication

Post in #workflow-alerts:

```
🔄 Slack Integration Rollback

We've temporarily disabled Slack notifications due to [issue].

Current status:
• Workflows continue to function normally
• No Slack notifications until issue resolved
• Investigating root cause

Expected resolution: [timeframe]

Updates will be posted here. Thank you for your patience.
```

______________________________________________________________________

## 📊 Expected Notification Volume

Based on historical data:

| Workflow              | Avg Runs/Day | Expected Failures | Notifications/Day |
| --------------------- | ------------ | ----------------- | ----------------- |
| issue-triage          | 12           | 0.1 (1%)          | ~0-1 (P1)         |
| auto-assign-reviewers | 10           | 0.2 (2%)          | ~0-1 (P1)         |
| status-sync           | 15           | 0.3 (2%)          | ~0-1 (P2)         |
| stale-management      | 1            | 0.01 (1%)         | ~0 (P2)           |
| workflow-metrics      | 1            | 0.01 (1%)         | 0 (P3 skipped)    |

**Total Expected:** 2-3 Slack notifications per day (P1 + P2)

**Peak Times:**

- Monday mornings: Higher issue/PR volume
- After deployments: More workflow activity

______________________________________________________________________

## 🎯 Success Criteria

After deployment, these should be true:

### Technical

- ✅ All 5 workflows updated successfully
- ✅ No YAML syntax errors
- ✅ Workflows execute without errors
- ✅ Notifications deliver to correct channel
- ✅ Priority routing works correctly
- ✅ No duplicate notifications

### Operational

- ✅ Notification delivery rate >99%
- ✅ Average P1 response time \<30 min
- ✅ False positive rate \<5%
- ✅ Daily summary posts at 9 AM UTC
- ✅ Team channel adoption >80%

### User Experience

- ✅ Messages are clear and actionable
- ✅ "View Details" links work
- ✅ Mentions notify correct people
- ✅ No notification fatigue reported
- ✅ Team finds notifications helpful

______________________________________________________________________

## 🔍 Troubleshooting

### Issue: Notification Not Sent

**Check:**

1. Workflow completed (not cancelled)
1. Condition met (e.g., `if: failure()` and workflow failed)
1. Secret configured correctly
1. Webhook URL valid
1. Not P3 (which skips Slack intentionally)

**Debug:**

```yaml
- name: Debug notification
  run: |
    echo "Workflow status: ${{ job.status }}"
    echo "Should notify: ${{ failure() }}"
```

### Issue: Wrong Priority

**Check:**

1. Priority parameter spelling: Must be `P0`, `P1`, `P2`, or `P3` (uppercase)
1. Correct priority for workflow importance
1. If statement condition matches intended trigger

### Issue: Webhook Error

**Check:**

1. Secret name matches: `SLACK_WEBHOOK_ALERTS`
1. Webhook URL format: `https://hooks.slack.com/services/...`
1. Slack app not deleted or disabled
1. Rate limits not exceeded (150 requests/minute)

**Test webhook manually:**

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
```

### Issue: Duplicate Notifications

**Check:**

1. Only one notification step per condition
1. No multiple `if: failure()` steps
1. Workflow not re-running multiple times

______________________________________________________________________

## 📚 Additional Resources

**Documentation:**

- [SLACK_INTEGRATION_TRAINING.md](../guides/SLACK_INTEGRATION_TRAINING.md) -
  Team training materials
- [SLACK_INTEGRATION_CONFIGURATION.md](../guides/SLACK_INTEGRATION_CONFIGURATION.md)
  \- Setup guide
- [WEEK5_DEPLOYMENT_CHECKLIST.md](../reports/WEEK5_DEPLOYMENT_CHECKLIST.md) -
  Complete checklist

**Code:**

- `.github/actions/slack-notify/action.yml` - Action source code
- `.github/workflows/slack-daily-summary.yml` - Daily summary implementation
- `.github/workflows/test-slack-notifications.yml` - Testing tool

**Support:**

- Slack: #workflow-alerts
- GitHub: Open issue with `slack-integration` label
- On-call: See CODEOWNERS

______________________________________________________________________

## ✅ Deployment Sign-Off

**Prepared by:** Workflow Team\
**Date:** February 17, 2026\
**Review status:**
Ready for deployment

**Approved by:**

- [ ] Workflow Team Lead: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date:
  \_\_\_\_\_\_\_
- [ ] Engineering Manager: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date:
  \_\_\_\_\_\_\_

**Deployment window:** February 18, 2026, 2:30-3:00 PM UTC

______________________________________________________________________

_Production Workflow Integration Guide - Version 1.0_

# Slack Integration Configuration Guide

## Week 5 - Setup and Testing Instructions

**Last Updated:** February 17, 2026\
**Status:** Ready for
Configuration\
**Target Deployment:** February 18, 2026

---

## 📋 Overview

This guide provides step-by-step instructions for configuring and testing the
Slack integration for our workflow notification system.

**What's Included:**

- GitHub Secrets configuration
- Slack webhook setup
- Testing procedures for all priority levels
- Validation checklist
- Troubleshooting guide

---

## 🔐 Part 1: Configure GitHub Secrets

### Prerequisites

- Admin access to GitHub repository settings
- Admin access to Slack workspace
- Slack webhooks created for both channels

### Step 1: Create Slack Incoming Webhooks

#### For #workflow-alerts Channel

1. **Navigate to Slack Apps:**
   - Go to <https://api.slack.com/apps>
   - Click "Create New App" → "From scratch"
   - App Name: `Workflow Alerts Bot`
   - Workspace: Your workspace
   - Click "Create App"

1. **Enable Incoming Webhooks:**
   - In app settings, click "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" to **On**
   - Click "Add New Webhook to Workspace"
   - Select channel: **#workflow-alerts**
   - Click "Allow"

1. **Copy Webhook URL:**
   - You'll see a webhook URL like:

     ```
     https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
     ```

   - **Copy this URL** - you'll need it for GitHub secrets

   - **Keep it secure** - treat it like a password!

1. **Customize Bot Appearance (Optional):**
   - Go to "Basic Information" → "Display Information"
   - Display Name: `Workflow Alerts`
   - Default Username: `workflow-bot`
   - Icon: Upload a workflow icon or use emoji `:robot_face:`
   - Click "Save Changes"

#### For #workflow-metrics Channel

1. **Repeat the process above** for a second webhook
1. **App Name:** `Workflow Metrics Bot`
1. **Select channel:** **#workflow-metrics**
1. **Copy the second webhook URL**

**Result:** You should now have **two webhook URLs**:

- One for #workflow-alerts
- One for #workflow-metrics

---

### Step 2: Add Secrets to GitHub

1. **Navigate to Repository Settings:**
   - Go to: <https://github.com/ivviiviivvi/.github/settings/secrets/actions>
   - Or: Repository → Settings → Secrets and variables → Actions

1. **Add First Secret:**
   - Click "New repository secret"
   - **Name:** `SLACK_WEBHOOK_ALERTS`
   - **Secret:** Paste the webhook URL for #workflow-alerts
   - Click "Add secret"

1. **Add Second Secret:**
   - Click "New repository secret"
   - **Name:** `SLACK_WEBHOOK_METRICS`
   - **Secret:** Paste the webhook URL for #workflow-metrics
   - Click "Add secret"

1. **Verify Secrets:**
   - You should see both secrets listed:
     - ✅ `SLACK_WEBHOOK_ALERTS` (updated now)
     - ✅ `SLACK_WEBHOOK_METRICS` (updated now)

---

## 🧪 Part 2: Testing Procedures

### Test 1: Manual Slack Notification Test

Before integrating with workflows, test that webhooks work correctly.

#### Create Test Workflow

**File:** `.github/workflows/test-slack-notifications.yml`

```yaml
name: Test Slack Notifications

on:
  workflow_dispatch:
    inputs:
      priority:
        description: "Priority level to test"
        required: true
        type: choice
        options:
          - P0
          - P1
          - P2
          - P3
      message:
        description: "Test message"
        required: false
        default: "This is a test notification"
        type: string

jobs:
  test-notification:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Send Test Notification
        uses: ./.github/actions/slack-notify
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
          priority: ${{ github.event.inputs.priority }}
          title: "[TEST] ${{ github.event.inputs.priority }} Notification Test"
          message: ${{ github.event.inputs.message }}
          workflow: test-slack-notifications
          status: success
          details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

#### Run Test Sequence

1. **Test P0 (Critical):**
   - Go to Actions → "Test Slack Notifications" → Run workflow
   - Priority: `P0`
   - Message: `Testing critical alert with @channel mention`
   - Click "Run workflow"
   - **Expected Result in #workflow-alerts:**
     - 🚨 Red message with "CRITICAL" badge
     - `@channel` mention visible
     - All fields populated
     - "View Details" button present
   - **Verify:** Click "View Details" button links to workflow run

1. **Test P1 (High):**
   - Run workflow again
   - Priority: `P1`
   - Message: `Testing high priority alert with @here mention`
   - **Expected Result:**
     - ⚠️ Orange message with "HIGH PRIORITY" badge
     - `@here` mention visible
     - Proper formatting

1. **Test P2 (Medium):**
   - Run workflow again
   - Priority: `P2`
   - Message: `Testing medium priority alert with no mention`
   - **Expected Result:**
     - ⚠️ Yellow message with "MEDIUM" badge
     - **No** mention (should not notify anyone)
     - Message delivered silently

1. **Test P3 (Low):**
   - Run workflow again
   - Priority: `P3`
   - Message: `Testing low priority - should not appear in Slack`
   - **Expected Result:**
     - **No message in Slack** (this is correct!)
     - Workflow completes successfully
     - Check workflow logs confirm P3 was skipped

#### Validation Checklist

After all tests complete, verify:

- [ ] P0 message appeared with @channel mention
- [ ] P1 message appeared with @here mention
- [ ] P2 message appeared with no mention
- [ ] P3 did NOT appear in Slack
- [ ] All colors correct (P0=red, P1=orange, P2=yellow)
- [ ] Status icons displayed correctly (✅ ❌ ⚠️)
- [ ] "View Details" button links to correct workflow run
- [ ] Message formatting clean and readable
- [ ] No error messages in workflow logs

---

### Test 2: Daily Summary Workflow Test

Test the automated daily performance summary.

#### Manual Trigger Test

1. **Navigate to Actions:**
   - Go to:
     <https://github.com/ivviiviivvi/.github/actions/workflows/slack-daily-summary.yml>

1. **Run Workflow Manually:**
   - Click "Run workflow" dropdown
   - Branch: `main`
   - Click "Run workflow" button

1. **Monitor Execution:**
   - Click on the running workflow
   - Watch the "Post Daily Summary to Slack" step
   - Should complete in ~30 seconds

1. **Check #workflow-metrics Channel:**
   - **Expected Message:**

     ```
     📊 Workflow System - Daily Summary
     Period: Yesterday (Feb 16, 2026)

     Overall Performance
     • Total Runs: XX
     • Successful: XX (XX%)
     • Failed: X (X%)
     • Status: ✅ Excellent (≥98%)

     Breakdown by Workflow
     ✅ issue-triage: X/X (100%)
     ✅ auto-assign-reviewers: X/X (100%)
     ...

     [View Dashboard →]
     ```

1. **Verify Content:**
   - [ ] Summary includes yesterday's data
   - [ ] Total runs count is accurate
   - [ ] Success rate calculation correct
   - [ ] All 4 workflows listed
   - [ ] Status emoji appropriate for success rate
   - [ ] "View Dashboard" button works

#### Schedule Test

To verify the scheduled run works:

1. **Check Cron Schedule:**
   - Schedule is: `0 9 * * *` (9:00 AM UTC daily)
   - Convert to your timezone for monitoring

1. **Monitor First Scheduled Run:**
   - Wait for 9:00 AM UTC the next day
   - Check Actions tab at 9:05 AM UTC
   - Confirm "slack-daily-summary" workflow ran
   - Check #workflow-metrics for message

1. **Verify Timing:**
   - [ ] Workflow triggered at exactly 9:00 AM UTC
   - [ ] Message appeared in Slack within 1 minute
   - [ ] No errors in workflow logs

---

### Test 3: Integration Test with Real Workflows

Test that actual workflow failures trigger correct notifications.

#### Simulate Workflow Failure

**Option A: Force a Failure (Recommended for Testing)**

1. **Create Test Issue:**
   - Create a new issue with incomplete information
   - Do NOT add required labels
   - Wait for issue-triage workflow to run

1. **Manually Fail a Workflow Run:**
   - Go to Actions → Pick a workflow
   - Manually cancel a run
   - This should trigger a notification

**Option B: Temporary Configuration Change**

1. **Edit a Workflow File (in a test branch):**

   ```yaml
   # Add this step to force failure
   - name: Force Failure for Testing
     run: exit 1
   ```

1. **Commit and Push:**
   - Push to test branch
   - Trigger the workflow
   - Should fail and send notification

1. **Verify Notification:**
   - Check #workflow-alerts for failure notification
   - Priority should be P1 or P2 depending on workflow
   - Verify @here mention if P1

1. **Revert Changes:**
   - Remove the failure step
   - Push fix
   - Verify success notification (or no notification if P3)

#### Integration Checklist

- [ ] Real workflow failure triggers notification
- [ ] Notification priority matches severity
- [ ] Mentions work correctly
- [ ] "View Details" links to actual failed run
- [ ] Message clearly describes the failure
- [ ] No duplicate notifications

---

## ✅ Part 3: Final Validation Checklist

### Pre-Deployment Verification

Before deploying to production, confirm all items:

#### Slack Configuration

- [ ] #workflow-alerts channel exists and has members
- [ ] #workflow-metrics channel exists and has members
- [ ] Webhook for #workflow-alerts created and tested
- [ ] Webhook for #workflow-metrics created and tested
- [ ] Bot display names and icons configured
- [ ] Bot has permission to post in both channels

#### GitHub Configuration

- [ ] `SLACK_WEBHOOK_ALERTS` secret added to repository
- [ ] `SLACK_WEBHOOK_METRICS` secret added to repository
- [ ] Secrets contain correct webhook URLs
- [ ] Secrets are accessible to workflows (check permissions)

#### Code Validation

- [ ] `.github/actions/slack-notify/action.yml` exists and has no syntax errors
- [ ] `.github/workflows/slack-daily-summary.yml` exists and has no syntax
      errors
- [ ] All priority levels (P0, P1, P2, P3) tested successfully
- [ ] Daily summary workflow tested manually
- [ ] Integration with real workflows tested

#### Testing Results

- [ ] P0 sends with @channel mention ✅
- [ ] P1 sends with @here mention ✅
- [ ] P2 sends with no mention ✅
- [ ] P3 does NOT send to Slack ✅
- [ ] Colors correct (red, orange, yellow, white) ✅
- [ ] Status icons display properly ✅
- [ ] "View Details" buttons link correctly ✅
- [ ] Daily summary calculates metrics correctly ✅
- [ ] Daily summary scheduled run works ✅
- [ ] No duplicate notifications ✅

#### Documentation

- [ ] Training materials created and reviewed
- [ ] Configuration guide (this document) complete
- [ ] Team notified of go-live date and time
- [ ] Launch announcement drafted

#### Team Readiness

- [ ] Training session scheduled (Feb 17, 2:00 PM UTC)
- [ ] All team members invited to both Slack channels
- [ ] On-call rotation defined for P0 alerts
- [ ] Escalation procedure documented

---

## 🚀 Part 4: Production Deployment

### Deployment Steps (February 18, 2026)

#### Step 1: Pre-Deployment Announcement (9:00 AM UTC)

Post in #workflow-alerts:

```
🚀 Slack Integration Deployment - TODAY at 2:00 PM UTC

Hello team! 👋

Today we're deploying the Slack notification integration for our workflow system.

What to expect:
• Real-time workflow notifications in this channel
• Daily performance summaries in #workflow-metrics
• Priority-based alerts (P0/P1/P2)

Training session:
📅 Today at 2:00 PM UTC (30 minutes before go-live)
📍 Zoom link: [insert link]
📝 Materials: docs/SLACK_INTEGRATION_TRAINING.md

Please join both channels:
• #workflow-alerts (you're here! ✅)
• #workflow-metrics

Questions? Reply in thread or DM @workflow-team

See you at training! 🎓
```

#### Step 2: Conduct Training (2:00 PM UTC)

- Follow [SLACK_INTEGRATION_TRAINING.md](SLACK_INTEGRATION_TRAINING.md)
- 15-minute session covering all priority levels
- Live demo of test notifications
- Q&A

#### Step 3: Enable Production Notifications (2:30 PM UTC)

**Currently, the integration is ready but not yet used by production
workflows.**

To enable, update each production workflow to use the slack-notify action:

**Example for issue-triage.yml:**

Add this step to the workflow (after existing steps):

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: ./.github/actions/slack-notify
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
    priority: P1
    title: "Issue Triage Workflow Failed"
    message: "The issue triage workflow encountered an error and failed to complete."
    workflow: issue-triage
    status: failure
    details-url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Repeat for all workflows:**

- issue-triage.yml (P1 on failure)
- auto-assign-reviewers.yml (P1 on failure)
- status-sync.yml (P2 on failure)
- stale-management.yml (P2 on failure)
- workflow-metrics.yml (P3 on success, P2 on failure)

#### Step 4: Monitor First Hour (2:30-3:30 PM UTC)

- Watch #workflow-alerts for any notifications
- Monitor GitHub Actions runs
- Check for errors in workflow logs
- Respond to team questions immediately

#### Step 5: Post-Deployment Announcement (3:30 PM UTC)

Post in #workflow-alerts:

```
✅ Slack Integration - DEPLOYED

The Slack notification system is now live! 🎉

What's working:
• Real-time workflow alerts in #workflow-alerts
• Daily summaries in #workflow-metrics at 9 AM UTC
• Priority-based routing (P0/P1/P2)

Please report any issues or unexpected behavior in this thread.

Thank you for your patience during deployment! 🙏
```

---

## 🔧 Part 5: Troubleshooting

### Common Issues and Solutions

#### Issue: Notifications Not Appearing

**Symptoms:**

- Workflow completes but no Slack message
- No errors in workflow logs

**Solutions:**

1. **Check webhook URL:**
   - Verify secret is correct in GitHub settings

   - Test webhook with curl:

     ```bash
     curl -X POST -H 'Content-type: application/json' \
       --data '{"text":"Test message"}' \
       YOUR_WEBHOOK_URL
     ```

1. **Check Slack app permissions:**
   - Go to <https://api.slack.com/apps>
   - Select your app
   - Verify "Incoming Webhooks" is enabled
   - Ensure webhook is associated with correct channel

1. **Check workflow logs:**
   - Look for "Send notification" step
   - Check for curl errors
   - Verify P3 wasn't used (P3 skips Slack intentionally)

#### Issue: Wrong Priority/Mentions

**Symptoms:**

- P1 doesn't have @here mention
- P2 has mention when it shouldn't

**Solutions:**

1. **Check priority input:**
   - Verify workflow is passing correct priority (P0, P1, P2, P3)
   - Case-sensitive: must be uppercase "P1" not "p1"

1. **Check action code:**
   - Verify `.github/actions/slack-notify/action.yml` has correct logic
   - Lines 35-50 should have mention logic

#### Issue: Duplicate Notifications

**Symptoms:**

- Same notification appears 2+ times
- Team reports spam

**Solutions:**

1. **Check for multiple failure steps:**
   - Verify only one notification step per failure condition
   - Use `if: failure()` carefully

1. **Check for workflow retries:**
   - GitHub Actions may retry failed steps
   - Add `max-attempts: 1` to notification step

#### Issue: Daily Summary Not Running

**Symptoms:**

- No summary at 9 AM UTC
- Workflow doesn't trigger on schedule

**Solutions:**

1. **Check cron schedule:**
   - Verify schedule is: `0 9 * * *`
   - Remember GitHub Actions uses UTC

1. **Check repository activity:**
   - Scheduled workflows may not run if repo inactive >60 days
   - Manual trigger once to reactivate

1. **Check workflow permissions:**
   - Verify workflow has `contents: read` permission

#### Issue: Broken "View Details" Links

**Symptoms:**

- Button links to wrong page
- 404 error when clicked

**Solutions:**

1. **Check details-url input:**
   - Should be:
     `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}`
   - Verify no typos

1. **Check repository visibility:**
   - If private repo, ensure user has access
   - Public repos should work for everyone

---

## 📊 Part 6: Monitoring and Metrics

### Week 1 Monitoring (Feb 18-21)

Track these metrics daily:

| Metric                     | Target   | How to Measure                                 |
| -------------------------- | -------- | ---------------------------------------------- |
| Notification delivery rate | >99%     | Workflows with notifications / total workflows |
| Team channel adoption      | >80%     | Members in #workflow-alerts / total team       |
| P1 alert response time     | \<30 min | Time from notification to first response       |
| False positive rate        | \<5%     | False alarms / total notifications             |
| Team satisfaction          | >8/10    | Survey on Friday                               |

### Daily Checklist

**9:00 AM UTC:**

- [ ] Check daily summary arrived in #workflow-metrics
- [ ] Verify metrics are accurate
- [ ] Review any failures from yesterday

**Throughout Day:**

- [ ] Monitor #workflow-alerts for notifications
- [ ] Respond to team questions
- [ ] Document any issues or feedback

**5:00 PM UTC:**

- [ ] Review day's notifications
- [ ] Calculate response times
- [ ] Note any patterns or trends

### Weekly Review (Friday, Feb 21)

1. **Collect metrics:**
   - Total notifications sent
   - Breakdown by priority (P0/P1/P2)
   - Response times
   - False positives

1. **Gather feedback:**
   - Send survey to team
   - Review Slack thread comments
   - Hold 15-minute retrospective

1. **Make adjustments:**
   - Tune priority thresholds if needed
   - Update notification content
   - Improve documentation

1. **Document learnings:**
   - Update this guide
   - Share successes
   - Plan improvements

---

## 📚 Additional Resources

### Related Documentation

- [Week 5 Implementation Guide](WEEK5_SLACK_INTEGRATION_GUIDE.md)
- [Slack Integration Training](SLACK_INTEGRATION_TRAINING.md)
- [Month 2 Kickoff Plan](MONTH2_KICKOFF_PLAN.md)

### External Links

- [Slack Incoming Webhooks Documentation](https://api.slack.com/messaging/webhooks)
- [GitHub Actions Documentation](https://docs.github.com/actions)<!-- link:docs.github_actions_root -->
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)

### Contact

- **Slack:** #workflow-alerts or @workflow-team
- **GitHub:** Open issue with `workflow-notifications` label
- **Email:** <workflow-team@your-org.com>

---

## ✅ Configuration Complete

Once all sections are verified, you're ready for production deployment on
**February 18, 2026 at 2:30 PM UTC**.

**Pre-Flight Checklist:**

- [ ] All secrets configured
- [ ] All tests passed
- [ ] Team notified
- [ ] Training scheduled
- [ ] Monitoring plan ready

**GO / NO-GO Decision Criteria:**

- ✅ All tests passed with no errors
- ✅ Team >80% trained
- ✅ Escalation procedure in place
- ✅ Rollback plan ready
- ✅ Stakeholder approval received

---

_Configuration Guide Version 1.0 - February 17, 2026_

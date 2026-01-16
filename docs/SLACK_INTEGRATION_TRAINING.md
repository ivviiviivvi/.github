# Slack Integration Training Guide

## Week 5 - Workflow Notifications System

**Date:** February 17, 2026\
**Duration:** 15 minutes\
**Audience:** All team
members\
**Format:** Live demo + hands-on

---

## 🎯 Training Objectives

By the end of this session, you will be able to:

1. **Understand** how Slack notifications enhance workflow visibility
1. **Recognize** different priority levels and their meaning
1. **Respond** appropriately to workflow alerts
1. **Access** detailed information from notifications
1. **Customize** your notification preferences

---

## 📋 Agenda (15 minutes)

| Time      | Topic                          | Format       |
| --------- | ------------------------------ | ------------ |
| 0-2 min   | Introduction & Benefits        | Presentation |
| 2-5 min   | Priority System Overview       | Presentation |
| 5-8 min   | Live Demo: All Priority Levels | Demo         |
| 8-10 min  | Daily Summary Walkthrough      | Demo         |
| 10-13 min | Hands-On: Test Notifications   | Practice     |
| 13-15 min | Q&A & Resources                | Discussion   |

---

## Part 1: Introduction (2 minutes)

### What's New?

Starting today, our GitHub workflow system will send **real-time notifications**
to Slack when important events occur. This means:

- ✅ **Faster response times** to critical issues
- ✅ **Better visibility** into workflow health
- ✅ **Reduced context switching** (stay in Slack)
- ✅ **Team awareness** of system status

### New Slack Channels

We've created two dedicated channels:

1. **#workflow-alerts** 🚨
   - Real-time workflow notifications
   - Priority-based alerts (P0, P1, P2)
   - Critical issues and failures
   - **Action Required:** Join this channel now!

1. **#workflow-metrics** 📊
   - Daily performance summaries
   - Success rate reports
   - Trend analysis
   - **Action Required:** Join for daily updates!

**👉 Please join both channels now if you haven't already.**

---

## Part 2: Priority System (3 minutes)

### Understanding Priority Levels

Our notification system uses **four priority levels** to help you focus on what
matters most:

#### 🔴 P0 - Critical (@channel)

**When:** System failures, security incidents, critical bugs

**Characteristics:**

- Red color in Slack
- `@channel` mention (notifies everyone)
- Requires immediate attention
- Example: Workflow completely failed, security vulnerability detected

**Your Action:**

- **Drop what you're doing**
- Respond within 5 minutes
- Coordinate in thread

**Example Message:**

```
🚨 CRITICAL: issue-triage workflow failed
@channel

Workflow: issue-triage
Status: ❌ Failed
Message: Workflow failed - unable to process incoming issues

The issue-triage workflow has encountered a critical failure. All new issues are not being triaged automatically.

[View Details →]
```

#### 🟠 P1 - High (@here)

**When:** Important failures, degraded performance, high-impact bugs

**Characteristics:**

- Orange color in Slack
- `@here` mention (notifies active users)
- Needs attention within 30 minutes
- Example: Auto-assignment workflow failing, reviewer assignment broken

**Your Action:**

- **Pause current work**
- Respond within 30 minutes
- Assign owner in thread

**Example Message:**

```
⚠️ HIGH PRIORITY: auto-assign-reviewers workflow failed
@here

Workflow: auto-assign-reviewers
Status: ❌ Failed
Message: Unable to assign reviewers - CODEOWNERS file may have issues

The reviewer assignment workflow is failing. PRs are not getting automatic reviewer assignments.

[View Details →]
```

#### 🟡 P2 - Medium (No mention)

**When:** Non-critical issues, warnings, recoverable errors

**Characteristics:**

- Yellow color in Slack
- No mention (silent notification)
- Review within 4 hours
- Example: Stale detection ran but found edge cases, partial workflow success

**Your Action:**

- **Review when available**
- Add to backlog if needed
- Comment in thread

**Example Message:**

```
⚠️ MEDIUM: status-sync workflow completed with warnings

Workflow: status-sync
Status: ⚠️ Warning
Message: Some PRs could not be synced - check for permission issues

The status sync workflow completed but encountered some issues. Most PRs were processed successfully.

[View Details →]
```

#### ⚪ P3 - Low (Dashboard only)

**When:** Informational, successful completions, routine operations

**Characteristics:**

- **Not sent to Slack** (reduces noise)
- Viewable in dashboard only
- No immediate action needed
- Example: All workflows succeeded, routine maintenance completed

**Your Action:**

- **None required**
- Available in daily summary
- Check dashboard if curious

---

## Part 3: Live Demo - All Priority Levels (3 minutes)

### Demo Scenario: Simulating Each Priority

I'll now trigger test notifications for each priority level so you can see
exactly what they look like in Slack.

#### Test 1: P0 Critical Alert

**Trigger:** Simulate critical workflow failure

**What You'll See:**

- Message appears in #workflow-alerts
- `@channel` mention notifies everyone
- Red color and alert emoji 🚨
- "View Details" button links to GitHub Actions run

**Expected Slack Message:**

```
🚨 CRITICAL: [TEST] Critical failure simulation
@channel

Workflow: test-notifications
Status: ❌ Failed
Message: This is a test of P0 critical alerts

This is a test message to demonstrate P0 critical priority notifications.

[View Details →]
```

#### Test 2: P1 High Priority

**Trigger:** Simulate important failure

**What You'll See:**

- Message appears in #workflow-alerts
- `@here` mention notifies active users
- Orange color and warning emoji ⚠️

**Expected Slack Message:**

```
⚠️ HIGH PRIORITY: [TEST] Important failure simulation
@here

Workflow: test-notifications
Status: ❌ Failed
Message: This is a test of P1 high priority alerts

This is a test message to demonstrate P1 high priority notifications.

[View Details →]
```

#### Test 3: P2 Medium Priority

**Trigger:** Simulate warning condition

**What You'll See:**

- Message appears in #workflow-alerts
- No mention (silent)
- Yellow color

**Expected Slack Message:**

```
⚠️ MEDIUM: [TEST] Warning condition simulation

Workflow: test-notifications
Status: ⚠️ Warning
Message: This is a test of P2 medium priority alerts

This is a test message to demonstrate P2 medium priority notifications.

[View Details →]
```

#### Test 4: P3 Low Priority

**Trigger:** Simulate successful completion

**What You'll See:**

- **Nothing in Slack!** (by design)
- Will appear in daily summary
- Available in GitHub Actions dashboard

---

## Part 4: Daily Summary (2 minutes)

### Morning Performance Report

Every day at **9:00 AM UTC**, you'll receive a comprehensive summary in
**#workflow-metrics**:

**Example Daily Summary:**

```
📊 Workflow System - Daily Summary
Period: Yesterday (Jan 16, 2026)

Overall Performance
• Total Runs: 47
• Successful: 46 (97.9%)
• Failed: 1 (2.1%)
• Status: ✅ Excellent (≥98%)

Breakdown by Workflow
✅ issue-triage: 12/12 (100%)
✅ auto-assign-reviewers: 10/10 (100%)
✅ status-sync: 15/15 (100%)
⚠️ stale-management: 9/10 (90%)

[View Dashboard →]
```

### Reading the Summary

**Status Indicators:**

- ✅ Green (≥98%): Excellent performance
- ⚠️ Orange (95-97%): Good but watch
- ⚠️ Red (\<95%): Needs attention

**What to Do:**

- **Green:** Keep going, all good!
- **Orange:** Monitor today for trends
- **Red:** Review failures and take action

---

## Part 5: Hands-On Practice (3 minutes)

### Exercise: Test Your Understanding

I'll now trigger a test notification. Your task:

1. **Watch #workflow-alerts** for the notification
1. **Identify the priority level** (P0, P1, or P2)
1. **Determine appropriate response time**
1. **Click "View Details"** to see the GitHub Actions run
1. **Post in thread** acknowledging you saw it

**Ready? Here we go!**

_\[Instructor triggers test notification\]_

**Debrief Questions:**

- What priority level was it?
- What was your expected response time?
- Did the "View Details" button work?
- Any questions about the format?

---

## Part 6: Q&A & Resources (2 minutes)

### Common Questions

**Q: Will I be overwhelmed with notifications?**\
A: No! P3 (routine)
notifications don't go to Slack, and we've tuned thresholds to minimize false
positives. Average: 2-3 notifications per day.

**Q: Can I mute notifications?**\
A: You can mute #workflow-alerts if needed,
but we recommend at least keeping it unmuted during work hours. Critical P0
alerts are rare (1-2 per month).

**Q: What if I miss a notification?**\
A: All notifications are in Slack
history, and the daily summary at 9 AM UTC recaps everything. Also available in
GitHub Actions dashboard.

**Q: How do I customize notification preferences?**\
A: Slack channel
notification settings allow per-channel customization. We recommend:

- #workflow-alerts: All messages
- #workflow-metrics: Mentions only (or mute)

**Q: Who responds to P0 alerts?**\
A: On-call rotation (see CODEOWNERS). But
`@channel` means everyone sees it for awareness.

**Q: What if notification is wrong/noisy?**\
A: Report in #workflow-alerts
thread with "false positive" tag. We'll tune thresholds weekly.

### Resources

**Documentation:**

- 📘 [Week 5 Implementation Guide](WEEK5_SLACK_INTEGRATION_GUIDE.md)
- 📘 [Slack Notification Action](../.github/actions/slack-notify/action.yml)
- 📘 [Daily Summary Workflow](../.github/workflows/slack-daily-summary.yml)

**Support Channels:**

- #workflow-alerts - Technical issues
- #workflow-metrics - Performance questions
- @workflow-team - Direct questions

**Quick Reference Card:**

| Priority | Color     | Mention  | Response Time | Typical Cause     |
| -------- | --------- | -------- | ------------- | ----------------- |
| P0       | 🔴 Red    | @channel | 5 minutes     | Critical failure  |
| P1       | 🟠 Orange | @here    | 30 minutes    | Important failure |
| P2       | 🟡 Yellow | None     | 4 hours       | Warning/partial   |
| P3       | ⚪ White  | None     | N/A           | Success/info      |

---

## 🎓 Training Complete

### Key Takeaways

1. ✅ **Join both channels**: #workflow-alerts and #workflow-metrics
1. ✅ **Understand priorities**: P0 critical, P1 high, P2 medium, P3
   dashboard-only
1. ✅ **Know response times**: P0 = 5 min, P1 = 30 min, P2 = 4 hours
1. ✅ **Use "View Details"**: Links to GitHub Actions for full context
1. ✅ **Check daily summary**: 9 AM UTC recap in #workflow-metrics

### Next Steps

1. **Join the channels** if you haven't already
1. **Test yourself** by watching for notifications today
1. **Bookmark** this training guide for reference
1. **Share feedback** after first week (survey coming Friday)

### Survey (End of Week)

On Friday, February 21, you'll receive a quick 3-minute survey:

- How helpful are the notifications?
- Are priority levels appropriate?
- Any false positives?
- Suggestions for improvement?

---

## 📊 Training Effectiveness Metrics

We'll track:

- % team members who joined channels (target: >80%)
- Average response time to P1 alerts (target: \<30 min)
- Notification accuracy (target: >95% true positives)
- Team satisfaction (target: >8/10)

---

## 🆘 Getting Help

**During Training:**

- Raise hand for questions
- Use Slack reactions for quick feedback
- Test notifications in real-time

**After Training:**

- Post in #workflow-alerts for technical issues
- DM @workflow-team for private questions
- Check documentation in /workspace/docs/

---

**Thank you for attending!** 🎉

The Slack integration goes live **today at 2:00 PM UTC**. Watch for your first
notifications!

---

_Training Guide Version 1.0 - February 17, 2026_

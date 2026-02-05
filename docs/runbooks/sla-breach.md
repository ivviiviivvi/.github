# SLA Breach Response Runbook

## Overview

This runbook provides guidance for responding to SLA breaches detected by the
automated SLA monitoring system.

## SLA Thresholds

### Response Time

| Priority | Threshold | Action                 |
| -------- | --------- | ---------------------- |
| P0       | 1 hour    | Immediate escalation   |
| P1       | 4 hours   | High priority response |
| P2       | 24 hours  | Standard response      |
| P3       | 72 hours  | Low priority           |

### Resolution Time

| Priority | Threshold | Action              |
| -------- | --------- | ------------------- |
| P0       | 4 hours   | All hands on deck   |
| P1       | 24 hours  | Dedicated responder |
| P2       | 72 hours  | Normal queue        |
| P3       | 168 hours | Backlog             |

### Success Rate

| Level    | Threshold | Action           |
| -------- | --------- | ---------------- |
| Target   | 95%       | Maintain         |
| Warning  | 90%       | Investigate      |
| Critical | 80%       | Immediate action |

## Detection

SLA breaches are automatically detected by the
[SLA Monitoring Workflow](../.github/workflows/sla-monitoring.yml) which runs
every 30 minutes.

### Alert Channels

- **Slack**: #sla-alerts channel
- **PagerDuty**: For critical breaches (P0/P1)
- **GitHub Issue**: Auto-created for tracking

## Response Steps

### 1. Acknowledge the Alert

- [ ] Check the alert details in Slack/PagerDuty
- [ ] Review the auto-created GitHub issue
- [ ] Identify which SLA metric is breached

### 2. Triage

- [ ] Determine the root cause of the breach
- [ ] Identify affected issues/PRs
- [ ] Assess if breach is ongoing or resolved

### 3. Remediation

For **Response Time** breaches:

- [ ] Review unacknowledged issues/PRs
- [ ] Assign owners to orphaned items
- [ ] Prioritize based on severity

For **Resolution Time** breaches:

- [ ] Check for blocked items
- [ ] Remove blockers or escalate
- [ ] Consider breaking down large items

For **Success Rate** breaches:

- [ ] Analyze recent failures
- [ ] Identify common failure patterns
- [ ] Fix systemic issues

### 4. Recovery

- [ ] Verify SLA metrics return to acceptable levels
- [ ] Update the tracking issue with resolution
- [ ] Document any process improvements

## Escalation

| Breach Duration | Action                 |
| --------------- | ---------------------- |
| \< 1 hour       | Team lead notification |
| 1-4 hours       | Engineering manager    |
| > 4 hours       | Director escalation    |

## Prevention

### Proactive Measures

1. **Monitor trends** - Watch for SLA metrics approaching thresholds
1. **Balance workload** - Use intelligent routing to distribute work
1. **Automate** - Reduce manual steps where possible
1. **Review regularly** - Weekly SLA review meetings

### Process Improvements

- Consider adjusting thresholds if consistently breached
- Add automation for common manual tasks
- Improve documentation for faster resolution
- Implement better triage processes

## Metrics to Track

- Time to acknowledge
- Time to first response
- Time to resolution
- First-touch resolution rate
- Escalation rate

## Related Links

- [SLA Thresholds Config](../automation/config/sla-thresholds.yml)
- [SLA Monitoring Workflow](../.github/workflows/sla-monitoring.yml)
- [Incident Response Runbook](./incident-response.md)

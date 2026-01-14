# Monitoring & Observability Guide

> **Comprehensive guide to monitoring workflows, collecting metrics, and managing alerts**

## Table of Contents

- [Overview](#overview)
- [Monitoring Infrastructure](#monitoring-infrastructure)
- [Workflow Failure Alerts](#workflow-failure-alerts)
- [Metrics Collection](#metrics-collection)
- [Usage Monitoring](#usage-monitoring)
- [Dashboard Access](#dashboard-access)
- [Alert Thresholds](#alert-thresholds)
- [Runbooks](#runbooks)
- [Troubleshooting](#troubleshooting)

---

## Overview

This organization maintains a comprehensive monitoring and observability system to ensure:

- **Workflow Health**: Real-time failure detection and alerting
- **Resource Management**: GitHub Actions minutes tracking and budget alerts
- **Performance Metrics**: Success rates, duration trends, and optimization opportunities
- **Proactive Response**: Automated alerts with runbooks for common issues

### Key Metrics Tracked

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Workflow Success Rate | >80% | <75% |
| Average Workflow Duration | <30 min | >45 min |
| Test Coverage | >80% | <70% |
| GitHub Actions Minutes Used | <80% of quota | >90% |
| Security Scan Findings | 0 critical | >0 critical |

---

## Monitoring Infrastructure

### Active Monitoring Workflows

#### 1. Alert on Workflow Failure

**File**: `.github/workflows/alert-on-workflow-failure.yml`

**Purpose**: Immediate notification when critical workflows fail

**Triggers**:

- `workflow_run` completion for monitored workflows:
  - generate-walkthrough
  - agentsphere-deployment
  - build-pages-site
  - generate-pages-index
  - deploy-to-pages-live
  - docker-build-push
  - collect-deployment-metadata

**Actions Taken**:

1. Logs failure details to console
2. Posts alert to GitHub Discussion #1
3. Includes workflow name, repository, and run link

**Usage**:

```bash
# Manually trigger alert check
gh workflow run alert-on-workflow-failure.yml
```

#### 2. Metrics Collection

**File**: `.github/workflows/metrics-collection.yml`

**Purpose**: Periodic collection of workflow metrics

**Schedule**: Every 6 hours (0 */6* **)

**Data Collected**:

- Workflow run counts (success, failure, cancelled)
- Average workflow durations
- Most frequently failing workflows
- Resource consumption trends
- API rate limit status

**Storage**: `metrics/` directory with timestamped JSON files

**Usage**:

```bash
# Trigger immediate metrics collection
gh workflow run metrics-collection.yml

# View latest metrics
cat metrics/$(ls -t metrics/*.json | head -1)
```

#### 3. Metrics Dashboard

**File**: `.github/workflows/metrics-dashboard.yml`

**Purpose**: Generate visual dashboard from collected metrics

**Schedule**: Daily at midnight UTC (0 0 ** *)

**Generated Artifacts**:

- `metrics-dashboard.html` - Interactive HTML dashboard
- `metrics-report.json` - Raw data for custom analysis
- Trend charts (success rates, durations, coverage)

**Access**:

- Dashboard published to GitHub Pages (if enabled)
- Artifacts available in workflow run

**Usage**:

```bash
# Generate dashboard immediately
gh workflow run metrics-dashboard.yml

# Download dashboard artifact
gh run download $(gh run list -w metrics-dashboard.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

#### 4. Usage Monitoring

**File**: `.github/workflows/usage-monitoring.yml`

**Purpose**: Track GitHub Actions minutes consumption

**Schedule**:

- Daily at 6 AM UTC (0 6 ** *)
- Weekly summary on Mondays at 8 AM UTC (0 8 ** 1)

**Reports Generated**:

- Daily usage reports
- Weekly trend summaries
- Monthly consumption analysis
- Budget alert notifications

**Alert Threshold**: 80% of included minutes (configurable)

**Usage**:

```bash
# Run usage report
gh workflow run usage-monitoring.yml -f report_type=daily

# Generate weekly summary
gh workflow run usage-monitoring.yml -f report_type=weekly

# Custom alert threshold
gh workflow run usage-monitoring.yml -f alert_threshold=90
```

---

## Workflow Failure Alerts

### How It Works

1. **Workflow Completes**: Any monitored workflow finishes
2. **Status Check**: Alert workflow checks `conclusion == 'failure'`
3. **Notification Sent**: If failed, alert posted to:
   - Console output (visible in Actions tab)
   - GitHub Discussion #1 (🚨 Workflow Failure Alert)
4. **Team Notified**: Subscribed team members receive notification

### Monitored Workflows

Current workflows monitored for failures:

- **Deployment**: agentsphere-deployment, build-pages-site, deploy-to-pages-live
- **Content Generation**: generate-walkthrough, generate-pages-index
- **Build Processes**: docker-build-push
- **Metadata**: collect-deployment-metadata

### Adding Workflows to Monitor

Edit `.github/workflows/alert-on-workflow-failure.yml`:

```yaml
on:
  workflow_run:
    workflows:
      [
        # ... existing workflows ...
        your-new-workflow-name,  # Add here
      ]
    types: [completed]
```

### Example Alert

```markdown
🚨 Workflow Failure Alert

Workflow: agentsphere-deployment
Repo: ivviiviivvi/.github
Run: https://github.com/ivviiviivvi/.github/actions/runs/123456789
```

---

## Metrics Collection

### Data Structure

Metrics are stored in `metrics/` directory:

```
metrics/
├── baseline-metrics.json          # Latest baseline
├── workflow-metrics-YYYYMMDD.json # Daily snapshots
└── trends/
    ├── success-rates.json
    ├── duration-trends.json
    └── coverage-history.json
```

### Metrics Schema

```json
{
  "timestamp": "2025-01-XX 06:00:00 UTC",
  "workflows": {
    "total_runs": 1234,
    "successful": 1000,
    "failed": 34,
    "cancelled": 200,
    "success_rate": 81.0
  },
  "performance": {
    "average_duration_seconds": 1200,
    "p95_duration_seconds": 1800,
    "slowest_workflow": "integration-tests"
  },
  "coverage": {
    "current": 82.5,
    "trend": "+2.5%",
    "below_threshold": false
  },
  "security": {
    "critical_findings": 0,
    "high_findings": 2,
    "medium_findings": 5
  }
}
```

### Accessing Metrics

**Via GitHub CLI**:

```bash
# View latest metrics
gh api -H "Accept: application/vnd.github.v3.raw" \
  /repos/ivviiviivvi/.github/contents/metrics/baseline-metrics.json | jq .

# Download metrics history
gh api /repos/ivviiviivvi/.github/contents/metrics \
  --jq '.[] | select(.name | endswith(".json")) | .download_url' | \
  xargs -n1 curl -O
```

**Via Raw API**:

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://raw.githubusercontent.com/ivviiviivvi/.github/main/metrics/baseline-metrics.json
```

**Via Web Interface**:

Navigate to: `https://github.com/ivviiviivvi/.github/tree/main/metrics`

---

## Usage Monitoring

### Budget Tracking

GitHub Actions minutes are tracked against included quota:

| Plan | Included Minutes | Alert at 80% | Alert at 90% |
|------|------------------|--------------|--------------|
| Free | 2,000/month | 1,600 min | 1,800 min |
| Team | 3,000/month | 2,400 min | 2,700 min |
| Enterprise | 50,000/month | 40,000 min | 45,000 min |

### Usage Reports

**Daily Report** (generated at 6 AM UTC):

```
📊 GitHub Actions Usage Report - 2025-01-XX

Total Minutes Used: 12,450 / 50,000 (24.9%)
Included Minutes Remaining: 37,550
Percentage Used: 25%
Status: ✅ Normal (below 80% threshold)

Top Consumers:
1. test-coverage.yml: 3,200 minutes (25.7%)
2. integration-tests.yml: 2,800 minutes (22.5%)
3. docker-build-push.yml: 1,900 minutes (15.3%)
```

**Weekly Summary** (Mondays at 8 AM UTC):

```
📈 Weekly Summary - Week of 2025-01-20

Total Usage: 8,750 minutes
Average Daily: 1,250 minutes
Trend: +5% vs last week
Projected Monthly: 37,500 minutes (75% of quota)

Warning: On current trajectory, will exceed 90% threshold by month end.
Recommendation: Review test-coverage.yml optimization opportunities.
```

### Alert Configuration

Alerts triggered when:

- **80% threshold**: Warning notification (monitoring continues)
- **90% threshold**: Critical alert (requires immediate action)
- **100% quota**: Usage restricted, workflows may fail

**Receiving Alerts**:

1. Subscribe to GitHub Discussion #1
2. Watch the repository for notifications
3. Check `.github/reports/usage/` for detailed reports

**Adjusting Thresholds**:

```bash
# Set custom alert threshold (1-100)
gh workflow run usage-monitoring.yml -f alert_threshold=85
```

---

## Dashboard Access

### Metrics Dashboard

**URL** (if GitHub Pages enabled):
`https://ivviiviivvi.github.io/.github/metrics-dashboard.html`

**Features**:

- Interactive charts (success rates, durations, coverage)
- Trend analysis (7-day, 30-day, 90-day)
- Workflow health scores
- Resource consumption breakdown
- Export to CSV/JSON

**Updating**:

- Automatically refreshed daily (midnight UTC)
- Manually trigger: `gh workflow run metrics-dashboard.yml`

### Alternative Access

**Download Latest Dashboard**:

```bash
# Get latest dashboard artifact
gh run download $(gh run list -w metrics-dashboard.yml --limit 1 --json databaseId -q '.[0].databaseId')

# Open in browser
open metrics-dashboard.html
```

**View in Repository**:

Navigate to: `Actions > Metrics Dashboard > [Latest Run] > Artifacts`

---

## Alert Thresholds

### Configured Thresholds

| Alert | Threshold | Severity | Action Required |
|-------|-----------|----------|-----------------|
| Workflow Failure | Any critical workflow fails | 🔴 Critical | Investigate immediately |
| Success Rate | <75% overall | 🟠 High | Review failing workflows within 4 hours |
| Average Duration | >45 minutes | 🟡 Medium | Optimize within 48 hours |
| Test Coverage | <70% | 🟡 Medium | Add tests within 1 week |
| Usage Quota | >90% | 🟠 High | Optimize or purchase more minutes |
| Security Findings | >0 critical | 🔴 Critical | Patch within 24 hours |
| Security Findings | >5 high | 🟠 High | Remediate within 1 week |

### Escalation Path

1. **Automated Alert** → GitHub Discussion #1
2. **Team Notification** → Subscribed members notified
3. **Severity Assessment** → Use runbooks below
4. **Resolution** → Document in post-mortem (if critical)

---

## Runbooks

### Runbook: Workflow Failure

**Trigger**: Alert in Discussion #1 - "🚨 Workflow Failure Alert"

**Steps**:

1. **Assess Impact**:
   - Click the run link in alert
   - Review error logs
   - Determine if user-facing service affected

2. **Quick Triage**:

   ```bash
   # View recent failures
   gh run list --workflow <workflow-name> --status failure --limit 5
   
   # Download logs
   gh run view <run-id> --log-failed
   ```

3. **Common Causes**:
   - **Flaky Tests**: Re-run workflow
   - **Rate Limiting**: Wait and retry
   - **Dependency Issues**: Check upstream services
   - **Code Errors**: Review recent commits
   - **Resource Exhaustion**: Check runner capacity

4. **Resolution**:
   - Fix identified issue
   - Re-run workflow to verify
   - Update discussion with resolution

5. **Prevention**:
   - Add tests if regression
   - Update documentation if config issue
   - Implement retry logic if transient

### Runbook: High Usage (>90%)

**Trigger**: Usage monitoring alert - "Critical: 90% quota exceeded"

**Steps**:

1. **Identify Top Consumers**:

   ```bash
   # View usage report
   cat .github/reports/usage/latest-usage.json | jq '.top_consumers'
   ```

2. **Optimization Strategies**:
   - **Cancel redundant runs**: Enable `concurrency` in workflows
   - **Reduce test matrix**: Limit to essential OS/version combos
   - **Use caching**: Add `cache` to setup actions
   - **Optimize build times**: Parallelize jobs
   - **Schedule appropriately**: Avoid overlapping cron jobs

3. **Example Optimization**:

   ```yaml
   # Add concurrency to prevent duplicate runs
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   
   # Enable caching
   - uses: actions/setup-python@v5
     with:
       python-version: '3.12'
       cache: 'pip'  # Enable pip caching
   ```

4. **Immediate Actions**:
   - Disable non-critical scheduled workflows
   - Reduce cron frequency (e.g., hourly → daily)
   - Defer integration tests to manual trigger

5. **Long-term**:
   - Request quota increase from GitHub
   - Consider self-hosted runners for heavy workloads

### Runbook: Low Success Rate (<75%)

**Trigger**: Metrics collection detects success rate below threshold

**Steps**:

1. **Identify Failing Workflows**:

   ```bash
   # View metrics
   cat metrics/baseline-metrics.json | jq '.workflows.by_name | to_entries | sort_by(.value.failure_rate) | reverse'
   ```

2. **Root Cause Analysis**:
   - Are failures isolated to one workflow?
   - Are failures recent or ongoing?
   - Do logs show consistent error patterns?

3. **Common Patterns**:
   - **Flaky Tests**: Add retries, increase timeouts
   - **External Dependencies**: Mock or add fallbacks
   - **Resource Constraints**: Increase `timeout-minutes`
   - **Race Conditions**: Add synchronization

4. **Resolution**:
   - Fix identified issues
   - Add monitoring for early detection
   - Update tests to be more reliable

### Runbook: Test Coverage Drop

**Trigger**: Coverage falls below 70% (CI enforcement threshold)

**Steps**:

1. **Identify Uncovered Code**:

   ```bash
   # View coverage report
   open htmlcov/index.html
   
   # Find files with low coverage
   coverage report --skip-covered --show-missing
   ```

2. **Prioritize Testing**:
   - Critical paths: 100% coverage required
   - Security-related: 100% coverage required
   - Core functionality: 80%+ coverage
   - Utilities: 70%+ coverage

3. **Add Tests**:
   - Use `pytest` with appropriate markers
   - Follow `docs/guides/testing-best-practices.md`
   - Run locally before pushing: `pytest tests/ --cov`

4. **Verification**:

   ```bash
   # Check if coverage improved
   pytest tests/ --cov --cov-report=term-missing
   ```

---

## Troubleshooting

### Issue: Alerts Not Received

**Symptoms**: Workflow fails but no alert in Discussion

**Causes**:

1. Workflow not in monitored list
2. Discussion #1 doesn't exist
3. Permissions issue

**Solutions**:

```bash
# Verify workflow is monitored
grep "workflows:" .github/workflows/alert-on-workflow-failure.yml

# Check if Discussion #1 exists
gh api /repos/ivviiviivvi/.github/discussions?per_page=1

# Verify permissions
grep "permissions:" .github/workflows/alert-on-workflow-failure.yml
```

### Issue: Metrics Not Collecting

**Symptoms**: `metrics/` directory not updating

**Causes**:

1. Workflow disabled
2. Schedule not triggering
3. Permission error (contents:write)

**Solutions**:

```bash
# Check workflow status
gh workflow view metrics-collection.yml

# Trigger manually
gh workflow run metrics-collection.yml

# Verify last run
gh run list --workflow metrics-collection.yml --limit 1
```

### Issue: Dashboard Not Updating

**Symptoms**: Dashboard shows stale data

**Causes**:

1. Metrics collection failing
2. Dashboard generation failing
3. GitHub Pages not configured

**Solutions**:

```bash
# Check metrics collection
gh run list --workflow metrics-collection.yml --status failure

# Regenerate dashboard
gh workflow run metrics-dashboard.yml

# View dashboard logs
gh run view $(gh run list -w metrics-dashboard.yml --limit 1 --json databaseId -q '.[0].databaseId') --log
```

### Issue: False Positive Alerts

**Symptoms**: Alert triggered for expected behavior

**Causes**:

1. Threshold too sensitive
2. Workflow includes expected failures (e.g., test matrix)
3. Maintenance window

**Solutions**:

- Adjust thresholds in usage-monitoring.yml
- Exclude specific workflows from alerting
- Document expected failures

### Issue: High Usage but No Alerts

**Symptoms**: Usage >80% but no alert received

**Causes**:

1. Usage monitoring workflow disabled
2. Alert threshold set too high
3. Schedule not running

**Solutions**:

```bash
# Check usage monitoring status
gh workflow view usage-monitoring.yml

# Verify schedule
grep "cron:" .github/workflows/usage-monitoring.yml

# Trigger manual check
gh workflow run usage-monitoring.yml -f alert_threshold=80
```

---

## Best Practices

### Monitoring

- **Subscribe to Discussion #1** for real-time alerts
- **Review dashboards weekly** to identify trends
- **Act on alerts within SLA** per severity
- **Document resolutions** in post-mortems

### Metrics

- **Check metrics regularly**: Daily review of key indicators
- **Investigate anomalies**: Sudden changes warrant investigation
- **Track trends**: Look for gradual degradation
- **Set realistic targets**: Adjust thresholds based on project needs

### Usage

- **Monitor quota early in month**: Avoid end-of-month surprises
- **Optimize proactively**: Don't wait for alerts
- **Use caching**: Dramatically reduces minutes consumed
- **Cancel redundant runs**: Enable concurrency groups

### Alerting

- **Tune thresholds**: Balance noise vs missed issues
- **Update runbooks**: Keep resolution steps current
- **Test alerts**: Periodically verify alert delivery
- **Escalate appropriately**: Critical issues need immediate attention

---

## Additional Resources

### Documentation

- [Testing Best Practices](testing-best-practices.md)
- [Workflow Optimization Guide](../COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md)
- [GitHub Actions Documentation](https://docs.github.com/actions)

### Workflows

- [Alert on Failure](../../.github/workflows/alert-on-workflow-failure.yml)
- [Metrics Collection](../../.github/workflows/metrics-collection.yml)
- [Metrics Dashboard](../../.github/workflows/metrics-dashboard.yml)
- [Usage Monitoring](../../.github/workflows/usage-monitoring.yml)

### Tools

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login

# View all workflows
gh workflow list

# View recent runs
gh run list --limit 20

# Watch workflow in real-time
gh run watch
```

---

## Questions or Feedback?

- **Issues**: Open an issue in this repository
- **Discussions**: Post in GitHub Discussions
- **Urgent**: Tag in Discussion #1 for immediate attention

---

_Last Updated: 2025-01-XX_
_Maintained by: DevOps Team_

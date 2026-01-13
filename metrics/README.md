# Workflow Metrics

This directory contains automated metrics tracking for all 76 GitHub Actions workflows.

## Files

### Automated Updates
- **`workflow-metrics.json`** - Updated every 6 hours with latest workflow performance data
- **`metrics-summary.md`** - Human-readable summary of key metrics (auto-generated)

### Manual Tracking
- **`baseline-metrics.json`** - Baseline metrics captured during optimization project
- **`progress-log.md`** - Week 1 implementation progress report

## Metrics Collected

The automated metrics collection tracks:

- **Success Rate**: % of workflow runs that complete successfully
- **Average Duration**: Mean execution time for successful runs
- **Total Runs**: Number of recent runs analyzed (last 20 per workflow)
- **Cache Hit Rate**: % of cache restore operations that succeed (where applicable)
- **Active Workflows**: Workflows that have run recently

## Viewing Metrics

### Quick Summary
See `metrics-summary.md` for a human-readable overview updated every 6 hours.

### Detailed Data
View `workflow-metrics.json` for complete metrics including:
```json
{
  "collected_at": "2025-12-23T21:00:00Z",
  "summary": {
    "total_workflows": 76,
    "workflows_with_runs": 45,
    "total_runs_analyzed": 850,
    "overall_success_rate": 94.2,
    "avg_workflow_duration_min": 6.8
  },
  "workflows": [...]
}
```

### Command Line
Pretty print specific metrics:
```bash
# Top 10 most active workflows
cat metrics/workflow-metrics.json | jq '.workflows[:10]'

# Workflows with success rate < 90%
cat metrics/workflow-metrics.json | jq '.workflows[] | select(.success_rate < 90)'

# Average duration by workflow
cat metrics/workflow-metrics.json | jq '.workflows[] | {name, avg_duration_min}'
```

## Metric Collection Workflow

The metrics are collected by `.github/workflows/metrics-collection.yml`:

- **Schedule**: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- **Manual Trigger**: Can be run manually via workflow_dispatch
- **Duration**: ~5-10 minutes to collect all metrics
- **API Usage**: Uses GitHub Actions API with built-in GITHUB_TOKEN

## Baseline Comparison

Compare current metrics against baseline:
```bash
# Success rate improvement
echo "Baseline: $(cat metrics/baseline-metrics.json | jq .baseline_metrics.success_rate_percent)%"
echo "Current: $(cat metrics/workflow-metrics.json | jq .summary.overall_success_rate)%"

# Avg build time improvement
echo "Baseline: $(cat metrics/baseline-metrics.json | jq .baseline_metrics.avg_build_time_minutes) min"
echo "Current: $(cat metrics/workflow-metrics.json | jq .summary.avg_workflow_duration_min) min"
```

## Interpreting Metrics

### Success Rate
- **>95%**: Excellent - workflows are reliable
- **90-95%**: Good - minor issues may exist
- **80-90%**: Fair - investigate failures
- **<80%**: Poor - immediate attention needed

### Average Duration
- **<5 min**: Fast - good developer experience
- **5-10 min**: Moderate - acceptable for most workflows
- **10-20 min**: Slow - consider optimization
- **>20 min**: Very slow - requires optimization

### Cache Hit Rate
- **>80%**: Excellent - caching is effective
- **60-80%**: Good - room for improvement
- **40-60%**: Fair - review cache configuration
- **<40%**: Poor - caching may not be working

## Monitoring Trends

Track metrics over time by checking git history:
```bash
# See metrics changes over time
git log -p metrics/workflow-metrics.json

# Compare metrics from 1 week ago
git show HEAD~7:metrics/workflow-metrics.json
```

## Automation

The metrics collection is fully automated:
1. Runs every 6 hours via cron schedule
2. Collects data from GitHub Actions API
3. Generates JSON and Markdown reports
4. Commits changes back to repository
5. No manual intervention required

## Privacy & Security

- ✅ Uses built-in GITHUB_TOKEN (no secrets needed)
- ✅ Only reads public workflow data
- ✅ No sensitive information collected
- ✅ All data stays in repository
- ✅ Commits use github-actions[bot] account

## Troubleshooting

**Metrics not updating?**
- Check `.github/workflows/metrics-collection.yml` workflow runs
- Verify workflow has `contents: write` permission
- Check for API rate limits

**Missing workflow data?**
- Workflow may not have run recently (last 20 runs checked)
- Check if workflow is disabled
- Verify workflow has completed at least one run

**Incorrect metrics?**
- GitHub API may have delays (~5 minutes)
- Re-run metrics collection manually
- Check workflow logs for errors

## Future Enhancements

Planned improvements:
- [ ] Cost tracking per workflow
- [ ] Failure rate trending
- [ ] Alert on success rate drops
- [ ] Cache efficiency improvements
- [ ] Visual dashboard (graphs)
- [ ] Slack/email notifications

---

**Last Updated**: 2025-12-23  
**Maintained By**: Workflow Optimization Team  
**Auto-Updated**: Every 6 hours via GitHub Actions

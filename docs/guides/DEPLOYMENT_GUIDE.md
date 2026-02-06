# Deployment Guide

Complete guide for deploying Month 1-3 workflow automation.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environments](#environments)
- [Deployment Process](#deployment-process)
- [Health Checks](#health-checks)
- [Rollback Procedures](#rollback-procedures)
- [Troubleshooting](#troubleshooting)

## Overview

This guide covers deploying the complete workflow automation system with:

- **Phased rollout**: Canary → Progressive → Full deployment
- **Automated health checks**: Continuous monitoring during deployment
- **Automatic rollback**: Revert on failure detection
- **Multi-environment support**: Staging, production, development

## Prerequisites

### Required Tools

- **Python 3.11+**: For deployment scripts
- **GitHub CLI (`gh`)**: For GitHub API access
- **Git**: For repository operations
- **PyYAML, Requests**: Python dependencies

```bash
# Install Python dependencies
pip install requests pyyaml
```

### Required Permissions

- **GitHub Admin**: Write access to target repositories
- **Actions permissions**: Enable GitHub Actions
- **Secret management**: Configure required secrets

### Required Secrets

Configure these in GitHub repository settings or as environment variables:

- `GITHUB_TOKEN`: GitHub API token with repo and workflow permissions
- `SLACK_WEBHOOK_URL`: Slack webhook for notifications (Month 2+)
- `PAGERDUTY_TOKEN`: PagerDuty API token (production only)

## Environments

### Staging

- **Purpose**: Pre-production testing
- **Repositories**: 3 test repositories
- **Rollout**: 33% canary, 67% progressive
- **Health checks**: 3 minutes, 80% success threshold
- **Features**: All features enabled

### Production

- **Purpose**: Live production environment
- **Repositories**: 5+ production repositories
- **Rollout**: 10% canary, 40% progressive (conservative)
- **Health checks**: 10 minutes, 90% success threshold
- **Features**: Auto-merge and proactive maintenance disabled initially

### Development

- **Purpose**: Local testing
- **Repositories**: 1 repository
- **Rollout**: 100% immediate deployment
- **Health checks**: 1 minute, 50% success threshold

Configuration: `automation/deployment/environments.yml`

## Deployment Process

### Step 1: Environment Validation

Validate environment before deployment:

```bash
cd automation/deployment

# Staging
./deploy.py --env staging --month 1 --dry-run

# Production
export GITHUB_TOKEN="your-token-here"
export SLACK_WEBHOOK_URL="your-webhook-url"
./deploy.py --env production --month 1 --dry-run
```

Checks performed:

- ✅ GitHub token validity
- ✅ Repository access
- ✅ Workflow files present
- ✅ Required secrets configured

### Step 2: Canary Deployment

Deploy to canary repositories (10% of total):

```bash
# Deploy with specific canary repos
./deploy.py \
  --env production \
  --month 1 \
  --canary-repos "org/repo1,org/repo2"

# Or let it select automatically
./deploy.py --env production --month 1
```

**Canary phase:**

1. Deploy workflows to canary repositories
1. Health check for 3 minutes (staging) or 10 minutes (production)
1. Monitor success rate (must be ≥ 80% staging, ≥ 90% production)
1. Abort if health checks fail

### Step 3: Progressive Rollout

Deploy to additional repositories (40-50%):

Automatically proceeds if canary succeeds.

**Progressive phase:**

1. Deploy to 40-50% of remaining repositories
1. Health check for 4 minutes (staging) or 10 minutes (production)
1. Monitor success rate
1. Rollback if failures detected

### Step 4: Full Deployment

Deploy to all remaining repositories:

Automatically proceeds if progressive rollout succeeds.

**Full phase:**

1. Deploy to 100% of repositories
1. Final health check for 5 minutes (staging) or 10 minutes (production)
1. Save deployment log

### Step 5: Post-Deployment Validation

Run comprehensive health checks:

```bash
# Check specific repository
./health_checks.py --repo org/repo

# Check entire environment
./health_checks.py --env production

# Check specific workflows
./health_checks.py --repo org/repo --workflows issue-triage,auto-assign
```

## Health Checks

### Automated Health Checks

Health checks run automatically during deployment:

- **Interval**: Every 30-60 seconds
- **Duration**: 3-10 minutes per phase
- **Metrics**: Success rate, workflow execution, error rates

### Manual Health Checks

Run health checks anytime:

```bash
# Check all workflows in repository
./health_checks.py --repo {{ORG_NAME}}/.github

# Check specific workflows
./health_checks.py \
  --repo {{ORG_NAME}}/.github \
  --workflows issue-triage,auto-assign,status-sync

# Check entire environment
./health_checks.py --env production --output health-report.json
```

**Health status:**

- **✅ Healthy**: Success rate ≥ 95%
- **⚠️ Degraded**: Success rate 85-95%
- **❌ Unhealthy**: Success rate \< 85%

### Health Check Reports

Results saved to JSON:

```json
{
  "repo": "org/repo",
  "timestamp": "2025-01-01T12:00:00Z",
  "overall_health": "healthy",
  "workflows": {
    "issue-triage": {
      "status": "healthy",
      "runs": 24,
      "successful": 23,
      "success_rate": 0.958
    }
  },
  "metrics": {
    "total_runs": 120,
    "success_rate": 0.975,
    "avg_duration_seconds": 45.2
  }
}
```

## Rollback Procedures

### Automatic Rollback

Rollback triggers automatically if:

- Health check success rate \< 85% (production: \< 90%)
- Critical workflow failures detected
- SLA breach detected

### Manual Rollback

#### Rollback Entire Deployment

```bash
# Dry run (show what would be done)
./rollback.py --deployment-id 20250101_120000 --dry-run

# Execute rollback
./rollback.py --deployment-id 20250101_120000 --execute
```

#### Rollback Specific Repository

```bash
# Rollback to specific commit
./rollback.py \
  --repo org/repo \
  --to-commit abc123def456 \
  --execute
```

### Rollback Process

1. **Load deployment log**: Get list of deployed repositories
1. **Revert workflows**: Restore previous workflow versions
1. **Verify rollback**: Run health checks
1. **Save rollback log**: Document rollback operation

### Rollback Logs

Saved to `automation/deployment/logs/rollback_{deployment_id}.json`:

```json
{
  "deployment_id": "20250101_120000",
  "rollback_timestamp": "2025-01-01T12:30:00Z",
  "repositories": 5,
  "successful": 5,
  "deployments": [...]
}
```

## Troubleshooting

### Deployment Failures

#### Problem: Environment validation fails

**Symptoms:**

- "GitHub token invalid"
- "Cannot access repository"

**Solutions:**

1. Verify `GITHUB_TOKEN` is set and valid
1. Check token has `repo` and `workflow` permissions
1. Verify repository access: `gh repo view org/repo`

#### Problem: Canary deployment fails

**Symptoms:**

- Health checks fail during canary phase
- Success rate \< 80%

**Solutions:**

1. Check workflow syntax: `gh workflow list`
1. Review workflow runs: `gh run list --workflow issue-triage.yml`
1. Check workflow logs: `gh run view <run-id> --log`
1. Validate secrets are configured

#### Problem: Progressive/full deployment fails

**Symptoms:**

- Health checks fail after initial success
- Increased error rate

**Solutions:**

1. Run manual health checks: `./health_checks.py --env production`
1. Review deployment log: `automation/deployment/logs/{deployment_id}.json`
1. Rollback if issues persist: `./rollback.py --deployment-id <id> --execute`

### Health Check Issues

#### Problem: Health checks show "degraded" status

**Symptoms:**

- Success rate 85-95%
- Some workflows failing

**Solutions:**

1. Identify failing workflows:

   ```bash
   ./health_checks.py --repo org/repo --output report.json
   cat report.json | jq '.workflows'
   ```

1. Check specific workflow:

   ```bash
   gh run list --workflow <workflow-name>.yml --limit 20
   ```

1. Review workflow configuration and secrets

#### Problem: Health checks timeout

**Symptoms:**

- Health checks take too long
- "Timeout waiting for workflow completion"

**Solutions:**

1. Increase timeout in `environments.yml`:

   ```yaml
   health_check_duration: 600  # 10 minutes
   ```

1. Check for workflow performance issues

1. Review GitHub Actions status:
   [status.github.com](https://www.githubstatus.com/)

### Rollback Issues

#### Problem: Rollback fails

**Symptoms:**

- "Failed to revert file"
- "No previous version found"

**Solutions:**

1. Check commit history:

   ```bash
   git log --oneline .github/workflows/<workflow>.yml
   ```

1. Manually revert if needed:

   ```bash
   git revert <commit-sha>
   git push
   ```

1. Verify repository permissions

#### Problem: Partial rollback

**Symptoms:**

- Some repositories rolled back, others failed
- Mixed workflow versions

**Solutions:**

1. Check rollback log for failed repositories

1. Manually rollback failed repositories:

   ```bash
   ./rollback.py --repo org/failed-repo --to-commit <sha> --execute
   ```

1. Run health checks to verify state

## Best Practices

### Before Deployment

1. **Test in staging first**: Always deploy to staging before production
1. **Review changelog**: Understand what's changing
1. **Backup configuration**: Save current workflow files
1. **Schedule appropriately**: Deploy during low-activity periods
1. **Notify team**: Inform stakeholders of deployment

### During Deployment

1. **Monitor health checks**: Watch for degradation
1. **Check Slack notifications**: Monitor alerts
1. **Be ready to rollback**: Keep rollback command ready
1. **Review logs**: Check workflow execution logs
1. **Communicate**: Update team on progress

### After Deployment

1. **Run comprehensive health checks**: Validate all workflows
1. **Monitor for 24 hours**: Watch for delayed issues
1. **Review metrics**: Compare pre/post deployment
1. **Document issues**: Note any problems encountered
1. **Update runbooks**: Improve documentation

## Emergency Procedures

### Critical Failure

If workflows cause production issues:

```bash
# Immediate rollback
./rollback.py --deployment-id <latest-id> --execute

# Disable workflows via GitHub UI if needed
gh workflow disable <workflow-name>.yml --repo org/repo

# Notify team
echo "URGENT: Workflows rolled back due to critical failure" | \
  curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"$TEXT\"}" $SLACK_WEBHOOK_URL
```

### SLA Breach

If success rate drops below SLA:

1. **Trigger rollback**: Use automatic rollback or manual rollback script
1. **Disable problematic workflows**: Disable specific failing workflows
1. **Alert on-call**: Page on-call engineer
1. **Investigate root cause**: Review logs and metrics
1. **Document incident**: Create incident report

## Deployment Checklist

### Pre-Deployment

- [ ] Code reviewed and approved
- [ ] Staging deployment successful
- [ ] Health checks passing in staging
- [ ] Team notified
- [ ] Rollback plan prepared
- [ ] Secrets configured
- [ ] Backup of current workflows

### During Deployment

- [ ] Environment validation passed
- [ ] Canary deployment successful
- [ ] Health checks passing
- [ ] Progressive rollout successful
- [ ] Full deployment complete
- [ ] Post-deployment health checks passed

### Post-Deployment

- [ ] All workflows healthy
- [ ] Metrics within expected ranges
- [ ] No SLA breaches
- [ ] Team notified of completion
- [ ] Deployment documented
- [ ] Lessons learned captured

## Additional Resources

- **GitHub Actions Documentation**:
  [docs.github.com/actions](https://docs.github.com/actions)<!-- link:docs.github_actions_root -->
- **Workflow Syntax**:
  [docs.github.com/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)
- **API Reference**: [docs.github.com/rest](https://docs.github.com/rest)
- **Status Page**: [status.github.com](https://www.githubstatus.com/)

## Support

For deployment issues:

1. Check [troubleshooting](#troubleshooting) section
1. Review deployment logs in `automation/deployment/logs/`
1. Run health checks: `./health_checks.py --env production`
1. Contact DevOps team via Slack: `#devops-support`
1. Page on-call for critical issues: PagerDuty

______________________________________________________________________

**Last Updated**: 2025-01-01

**Maintained By**: DevOps Team

**Version**: 1.0.0

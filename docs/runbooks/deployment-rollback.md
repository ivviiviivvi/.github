# Deployment Rollback Runbook

## Overview

This runbook provides step-by-step instructions for rolling back a problematic
deployment.

## When to Rollback

Consider rollback when:

- Production service is degraded or down
- Critical bugs affecting users
- Security vulnerabilities discovered
- Performance significantly degraded
- Data integrity issues

## Pre-Rollback Checklist

- [ ] Confirm the issue is deployment-related
- [ ] Identify the last known good deployment
- [ ] Notify stakeholders of planned rollback
- [ ] Ensure rollback won't cause data loss

## Rollback Procedures

### GitHub Actions Workflow Rollback

1. **Identify the problematic deployment**

   ```bash
   gh run list --workflow=deploy.yml --limit=10
   ```

1. **Find the last successful deployment**

   ```bash
   gh run list --workflow=deploy.yml --status=success --limit=5
   ```

1. **Trigger rollback workflow** (if available)

   ```bash
   gh workflow run rollback.yml -f target_version=<version>
   ```

### Manual Git Rollback

1. **Identify the commit to rollback to**

   ```bash
   git log --oneline -20
   ```

1. **Create rollback branch**

   ```bash
   git checkout -b rollback/$(date +%Y%m%d-%H%M%S)
   git revert <problematic-commit>
   ```

1. **Create and merge rollback PR**

   ```bash
   gh pr create --title "Rollback: <description>" --body "Rolling back due to <reason>"
   ```

### Container/Kubernetes Rollback

1. **Check deployment history**

   ```bash
   kubectl rollout history deployment/<name>
   ```

1. **Rollback to previous version**

   ```bash
   kubectl rollout undo deployment/<name>
   ```

1. **Verify rollback**

   ```bash
   kubectl rollout status deployment/<name>
   ```

## Post-Rollback Steps

### Immediate Actions

- [ ] Verify service is restored
- [ ] Check monitoring dashboards
- [ ] Confirm user impact is mitigated
- [ ] Update status page

### Follow-up Actions

- [ ] Create incident report
- [ ] Document root cause
- [ ] Plan fix for the issue
- [ ] Schedule post-mortem

## Communication Template

### Initial Notification

```text
Subject: [ACTION] Deployment Rollback in Progress

Team,

We are rolling back the recent deployment to <service> due to <brief reason>.

- Impact: <description>
- ETA for rollback: <time>
- Next update: <time>

Please stand by for further updates.
```

### Resolution Notification

```text
Subject: [RESOLVED] Deployment Rollback Complete

Team,

The rollback has been completed successfully.

- Service status: Restored
- Rollback completed at: <time>
- Root cause investigation: In progress

We will share findings in the post-mortem scheduled for <date>.
```

## Rollback Prevention

### Best Practices

1. **Feature flags** - Use feature flags for easy disable
1. **Canary deployments** - Gradual rollout to detect issues early
1. **Automated testing** - Comprehensive test coverage
1. **Monitoring** - Alert on anomalies post-deployment
1. **Blue-green deployments** - Quick switch between versions

### Pre-deployment Checklist

- [ ] All tests passing
- [ ] Code review approved
- [ ] Security scan clean
- [ ] Performance impact assessed
- [ ] Rollback plan documented

## Related Links

- [Auto-Merge Workflow](../../.github/workflows/auto-merge.yml)
- [Incident Response Runbook](./incident-response.md)
- [SLA Breach Runbook](./sla-breach.md)

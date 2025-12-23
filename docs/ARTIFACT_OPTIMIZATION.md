# Artifact Optimization Guide

This document explains the artifact optimization strategies implemented across workflows.

## Problem Statement

GitHub Actions artifacts consume storage and have associated costs:
- **Storage limit**: 500MB for free tier, 50GB for teams
- **Cost**: $0.25 per GB/month for additional storage
- **Default retention**: 90 days (excessive for most use cases)

## Optimization Strategy

### 1. Retention Period Optimization

Different artifact types need different retention periods:

| Artifact Type | Retention | Rationale |
|---------------|-----------|-----------|
| **Test Results** | 7 days | Quick debugging, not needed long-term |
| **Coverage Reports** | 14 days | Trend analysis, comparison |
| **Build Artifacts** | 30 days | Deployment rollback capability |
| **Security Scans** | 30 days | Compliance, audit trails |
| **Metrics/Logs** | 7 days | Recent debugging only |
| **Documentation** | 90 days | Long-term reference |
| **Release Assets** | 365 days | Permanent record |

### 2. Size Optimization

**Compression**:
- Use `tar.gz` or `zip` for multi-file artifacts
- Exclude unnecessary files (node_modules, .git, etc.)
- Use `.gitignore` patterns

**Selective Upload**:
- Only upload on failure (when needed for debugging)
- Skip artifacts for scheduled/automated runs
- Use conditional artifact upload

### 3. Artifact Naming Convention

Use descriptive, unique names to avoid conflicts:

```yaml
name: test-results-${{ github.run_number }}-${{ github.sha }}
```

### 4. Cleanup Strategy

**Auto-cleanup**:
- Old artifacts auto-delete after retention period
- No manual intervention needed

**Manual cleanup** (if needed):
```bash
# List artifacts
gh api repos/{owner}/{repo}/actions/artifacts

# Delete specific artifact
gh api -X DELETE repos/{owner}/{repo}/actions/artifacts/{artifact_id}
```

## Implementation Examples

### Test Results (7 days)

```yaml
- name: Upload test results
  if: failure()  # Only on failure
  uses: actions/upload-artifact@v4
  with:
    name: test-results-${{ github.run_number }}
    path: |
      test-results/
      coverage/
    retention-days: 7
```

### Build Artifacts (30 days)

```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ github.sha }}
    path: dist/
    retention-days: 30
    compression-level: 9  # Maximum compression
```

### Security Scans (30 days)

```yaml
- name: Upload security scan results
  uses: actions/upload-artifact@v4
  with:
    name: security-scan-${{ github.run_number }}
    path: |
      trivy-results.sarif
      semgrep-results.sarif
    retention-days: 30
```

### Conditional Upload (Only on Failure)

```yaml
- name: Upload debug logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: debug-logs-${{ github.run_number }}
    path: logs/
    retention-days: 7
```

## Storage Savings Calculation

**Before Optimization**:
- Average artifact size: 50MB
- Number of workflows with artifacts: 24
- Runs per day: 20
- Default retention: 90 days
- Storage: 50MB × 24 × 20 × 90 = **2,160 GB**
- Cost: 2,160 GB × $0.25 = **$540/month**

**After Optimization**:
- Average retention: 14 days (optimized)
- Conditional uploads reduce volume by 50%
- Storage: 50MB × 24 × 20 × 14 × 0.5 = **168 GB**
- Cost: 168 GB × $0.25 = **$42/month**

**Savings**: $498/month (**92% reduction**)

## Monitoring

Track artifact storage usage:

```bash
# Total storage used
gh api /repos/{owner}/{repo}/actions/cache/usage

# List all artifacts
gh api /repos/{owner}/{repo}/actions/artifacts --paginate
```

## Best Practices

1. ✅ **Always set explicit retention-days** - Don't rely on default 90 days
2. ✅ **Use conditional upload** - `if: failure()` for debug artifacts
3. ✅ **Compress large artifacts** - Use `compression-level: 9`
4. ✅ **Use descriptive names** - Include run number or SHA
5. ✅ **Clean up regularly** - Delete old artifacts if needed
6. ✅ **Monitor storage** - Track usage trends
7. ✅ **Document retention** - Explain why each retention period was chosen

## Workflow-Specific Recommendations

### High-Frequency Workflows (run > 10x/day)
- Minimize artifact uploads
- Use 7-day retention max
- Upload only on failure

### Security Workflows
- Keep SARIF files for compliance
- 30-day retention recommended
- Always upload to GitHub Security tab

### Deployment Workflows
- Keep build artifacts for rollback
- 30-day retention recommended
- Consider external storage for releases

### Metrics/Monitoring Workflows
- 7-day retention sufficient
- Auto-commit results to repo instead
- Artifacts only for debugging

## Migration Checklist

For each workflow with artifacts:

- [ ] Identify artifact type and purpose
- [ ] Set appropriate retention period
- [ ] Add conditional upload if applicable
- [ ] Use compression for large artifacts
- [ ] Update artifact names to be unique
- [ ] Document retention decision
- [ ] Test workflow with changes
- [ ] Monitor storage savings

## References

- [GitHub Actions Artifacts Documentation](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- [GitHub Actions Billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [Artifact Retention API](https://docs.github.com/en/rest/actions/artifacts)

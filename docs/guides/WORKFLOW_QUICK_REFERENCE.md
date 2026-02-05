# Workflow Optimization Quick Reference Guide

## 🚀 Quick Start

### Most Common Tasks

#### 1. Add Caching to Your Workflow

```yaml
# For Python
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: "pip" # ⭐ Add this line

# For Node.js
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm" # ⭐ Add this line

# For Ruby
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: "3.1"
    bundler-cache: true # ⭐ Add this line
```

#### 2. Pin Actions to Commit SHA

```yaml
# ❌ INSECURE
uses: aquasecurity/trivy-action@master

# ✅ SECURE
uses: aquasecurity/trivy-action@915b19bbe73b92a6cf82a1bc12b087c9a19a5fe2  # v0.28.0
```

#### 3. Set Minimal Permissions

```yaml
permissions:
  contents: read # ⭐ Always start with minimal
  pull-requests: write # ⭐ Only add what you need
```

#### 4. Add Timeout Protection

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10 # ⭐ Prevent hanging jobs
```

#### 5. Implement Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true # ⭐ Cancel redundant runs
```

______________________________________________________________________

## 📊 Performance Cheat Sheet

### Optimization Impact Reference

| Technique              | Time Saved | Effort | Priority  |
| ---------------------- | ---------- | ------ | --------- |
| Add dependency caching | 30-60%     | Low    | 🔴 High   |
| Enable build caching   | 40-70%     | Medium | 🔴 High   |
| Parallel job execution | 50-75%     | Medium | 🟡 Medium |
| Smart path filters     | 80-90%\*   | Low    | 🔴 High   |
| Matrix strategy        | 60-80%     | Medium | 🟡 Medium |
| Reusable workflows     | 20-30%     | High   | 🟢 Low    |

\*Reduces unnecessary runs

### Cache Key Patterns

```yaml
# ✅ GOOD - Specific and accurate
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

# ⚠️ OKAY - Less specific
key: ${{ runner.os }}-pip-${{ github.sha }}

# ❌ BAD - Too generic (cache pollution)
key: ${{ runner.os }}-pip-cache
```

______________________________________________________________________

## 🔒 Security Quick Checks

### Pre-Commit Checklist

- [ ] All actions pinned to commit SHA or specific version?
- [ ] Permissions set to minimum required?
- [ ] Timeout configured for all jobs?
- [ ] No secrets in code or logs?
- [ ] Input validation for user inputs?
- [ ] Path filters to avoid unnecessary runs?

### Action Pinning Helper

```bash
# Get commit SHA for an action
gh api repos/actions/checkout/commits/main --jq '.sha'

# Or use this one-liner to pin all actions
# (Review before committing!)
sed -i 's/@v4/@11bd71901bbe5b1630ceea73d27597364c9af683 # v4/g' workflow.yml
```

______________________________________________________________________

## 💰 Cost Optimization Tips

### Runner Cost Comparison (per minute)

| Runner         | Cost   | Use When               |
| -------------- | ------ | ---------------------- |
| ubuntu-latest  | $0.008 | Default choice         |
| windows-latest | $0.016 | Windows-specific needs |
| macos-latest   | $0.080 | macOS-specific needs   |

**Rule**: Always use ubuntu unless platform-specific testing required

### Cost-Saving Patterns

#### 1. Path-based Triggering

```yaml
on:
  push:
    paths:
      - "src/**" # Only code changes
      - "**.py" # Only Python files
      - "!docs/**" # Ignore docs
```

**Savings**: 50-80% reduction in unnecessary runs

#### 2. Concurrency Limits

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Savings**: Prevents parallel duplicate runs

#### 3. Artifact Retention

```yaml
- uses: actions/upload-artifact@v4
  with:
    retention-days: 7 # Instead of default 90
```

**Savings**: Reduces storage costs

#### 4. Conditional Job Execution

```yaml
jobs:
  expensive-job:
    if: github.ref == 'refs/heads/main' # Only on main branch
```

**Savings**: Avoids expensive operations on feature branches

______________________________________________________________________

## 🎯 Common Patterns

### Pattern 1: Multi-Stage Pipeline

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: test # Wait for tests
    runs-on: ubuntu-latest
    steps:
      - run: npm build

  deploy:
    needs: build # Wait for build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: deploy.sh
```

### Pattern 2: Matrix Testing

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
        exclude:
          - os: macos-latest # Skip expensive combinations
            node-version: 16
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### Pattern 3: Reusable Workflow

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm test
```

```yaml
# Consumer workflow
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "20"
```

______________________________________________________________________

## 🔍 Troubleshooting

### Common Issues

#### Cache Not Working?

```yaml
# Check cache key includes all dependency files
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
#                                         ↑
#                            Use ** to include subdirectories
```

#### Workflow Not Triggering?

```yaml
# Check path filters are correct
paths:
  - "src/**" # Includes src/foo/bar.py ✅
  - "src/*" # Only src/bar.py (not subdirs) ❌
```

#### Permission Denied?

```yaml
# Add required permission
permissions:
  contents: write # For git push
  packages: write # For docker push
```

#### Timeout Too Short?

```yaml
# Increase timeout for slow jobs
timeout-minutes: 30 # Increase from default 360
```

#### Action Version Conflict?

```yaml
# Use exact commit SHA
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
# Not: @v4 or @main
```

______________________________________________________________________

## 📈 Metrics to Track

### Key Performance Indicators

```yaml
# Add to your workflow summary
- name: Report metrics
  run: |
    echo "## Workflow Metrics" >> $GITHUB_STEP_SUMMARY
    echo "- **Duration**: ${{ github.event.workflow_run.run_duration_ms }}ms" >> $GITHUB_STEP_SUMMARY
    echo "- **Conclusion**: ${{ github.event.workflow_run.conclusion }}" >> $GITHUB_STEP_SUMMARY
```

### Track Over Time

- Average build time (target: \<5 min)
- Success rate (target: >95%)
- Cache hit rate (target: >70%)
- Cost per commit (target: \<$0.10)

______________________________________________________________________

## 🛠️ Useful Scripts

### 1. Find Unpinned Actions

```bash
#!/bin/bash
# find-unpinned-actions.sh
grep -r "@master\|@main" .github/workflows/ | grep -v "^#"
```

### 2. Analyze Workflow Run Times

```bash
#!/bin/bash
# analyze-workflow-times.sh
gh run list --limit 100 --json name,conclusion,startedAt,updatedAt \
  --jq '.[] | select(.conclusion=="success") | {name, duration: (((.updatedAt | fromdateiso8601) - (.startedAt | fromdateiso8601)) | floor)}' \
  | jq -s 'group_by(.name) | map({name: .[0].name, avg_duration: (map(.duration) | add / length), runs: length})'
```

### 3. Check Workflow Costs

```bash
#!/bin/bash
# estimate-workflow-costs.sh
# Ubuntu: $0.008/min, Windows: $0.016/min, macOS: $0.080/min
gh api /repos/:owner/:repo/actions/runs --paginate \
  --jq '.workflow_runs[] | select(.created_at > "2024-01-01") | {name, run_started_at, updated_at, os: .run_attempt}' \
  | jq -s 'group_by(.name) | map({workflow: .[0].name, total_minutes: (map(((.updated_at | fromdateiso8601) - (.run_started_at | fromdateiso8601)) / 60) | add), estimated_cost: ((map(((.updated_at | fromdateiso8601) - (.run_started_at | fromdateiso8601)) / 60) | add) * 0.008)})'
```

______________________________________________________________________

## 📚 Learning Resources

### Official Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)<!-- link:docs.github_actions -->
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)<!-- link:docs.github_actions_workflow_syntax -->
- [Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)<!-- link:docs.github_actions_hardening -->

### Best Practices

- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices-for-github-actions)
- [Caching Dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)<!-- link:docs.github_actions_caching -->
- [Security Hardening](https://docs.github.com/en/actions/security-guides)

### Community

- [GitHub Actions Community](https://github.com/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [r/github](https://reddit.com/r/github)

______________________________________________________________________

## 🎓 Workflow Optimization Levels

### Level 1: Beginner

- ✅ Pin all actions to versions
- ✅ Add timeout-minutes
- ✅ Set minimal permissions
- ✅ Use concurrency control
- ✅ Add basic caching

### Level 2: Intermediate

- ✅ Implement path filters
- ✅ Use matrix strategies
- ✅ Extract reusable workflows
- ✅ Add retry logic
- ✅ Optimize artifact storage

### Level 3: Advanced

- ✅ Smart test selection
- ✅ Progressive deployments
- ✅ Custom composite actions
- ✅ ML-powered optimization
- ✅ Comprehensive monitoring

______________________________________________________________________

## 🚨 Emergency Procedures

### Workflow Disabled/Failing?

**1. Check Status Page**

```
https://www.githubstatus.com/
```

**2. View Logs**

```bash
gh run view --log
```

**3. Re-run Failed Jobs**

```bash
gh run rerun <run-id> --failed
```

**4. Disable Workflow Temporarily**

```bash
# Via UI: Actions → Workflows → [Workflow] → ⋯ → Disable workflow
```

### Rollback Workflow Changes

```bash
# Revert workflow file
git checkout HEAD~1 -- .github/workflows/failing-workflow.yml
git commit -m "revert: rollback workflow changes"
git push
```

______________________________________________________________________

## 📞 Getting Help

### Internal Resources

- **Documentation**: See `WORKFLOW_GUIDE.md`
- **Security**: See `WORKFLOW_SECURITY_AUDIT.md`
- **Roadmap**: See `WORKFLOW_OPTIMIZATION_ROADMAP.md`
- **Analysis**: See `COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md`

### External Support

- GitHub Support: https://support.github.com/
- GitHub Community: https://github.community/
- Stack Overflow: Tag `github-actions`

______________________________________________________________________

## ✅ Quick Wins (Do These First!)

### 10-Minute Wins

1. [ ] Add `cache: 'pip'` to Python workflows
1. [ ] Add `cache: 'npm'` to Node.js workflows
1. [ ] Pin the 3 unpinned Trivy actions
1. [ ] Add `timeout-minutes` to workflows missing it

### 30-Minute Wins

5. [ ] Add path filters to reduce unnecessary runs
1. [ ] Review and minimize workflow permissions
1. [ ] Add concurrency controls where missing
1. [ ] Set appropriate artifact retention days

### 1-Hour Wins

9. [ ] Extract app detection to reusable workflow
1. [ ] Create workflow documentation
1. [ ] Set up basic metrics tracking
1. [ ] Add input validation to user-triggered workflows

______________________________________________________________________

## 🎯 Workflow Optimization Scorecard

Rate your workflow on each dimension (1-5):

**Performance** (Speed & Efficiency)

- [ ] Caching implemented (all dependencies)
- [ ] Parallel execution where possible
- [ ] Minimal dependencies installed
- [ ] Smart test selection
- [ ] Build artifacts cached

**Security** (Protection & Safety)

- [ ] All actions pinned to commit SHA
- [ ] Minimal permissions configured
- [ ] Input validation implemented
- [ ] Secrets properly managed
- [ ] CODEOWNERS includes workflows

**Cost** (Resource Optimization)

- [ ] Ubuntu runner used (unless necessary)
- [ ] Path filters implemented
- [ ] Concurrency controls active
- [ ] Artifact retention optimized
- [ ] Unnecessary runs prevented

**Reliability** (Stability & Resilience)

- [ ] Timeout limits configured
- [ ] Retry logic for flaky operations
- [ ] Error handling comprehensive
- [ ] Rollback procedures documented
- [ ] Monitoring and alerts active

**Maintainability** (Ease of Updates)

- [ ] Well documented
- [ ] Follows conventions
- [ ] DRY principle applied
- [ ] Reusable components extracted
- [ ] Clear ownership

**Total Score**: \_\_/25

- **20-25**: Excellent! 🌟
- **15-19**: Very Good 👍
- **10-14**: Good (room for improvement) ⚠️
- **5-9**: Needs attention 🔧
- **0-4**: Requires immediate action 🚨

______________________________________________________________________

**Version**: 1.0\
**Last Updated**: 2025-12-23\
**Feedback**: Open an issue or
PR to improve this guide!

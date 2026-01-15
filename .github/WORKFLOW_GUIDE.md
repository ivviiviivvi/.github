# Workflow Developer Guide

## Quick Start for Contributors

Welcome! This guide helps you work with our 76 GitHub Actions workflows
efficiently.

### Our Workflows Organized by Category

**CI/CD** (10 workflows): Testing, linting, building

- `ci.yml`, `ci-advanced.yml`, `code-coverage.yml`, `build-pages-site.yml`, etc.

**Security** (8 workflows): Scanning, auditing, vulnerability detection

- `security-scan.yml`, `codeql-analysis.yml`, `scan-for-secrets.yml`,
  `semgrep.yml`, etc.

**Deployment** (12 workflows): Pages, Docker, AgentSphere

- `deploy-to-pages-live.yml`, `docker-build-push.yml`,
  `agentsphere-deployment.yml`, etc.

**Automation** (20 workflows): Labeling, assignment, merging

- `auto-assign.yml`, `auto-merge.yml`, `auto-labeler.yml`,
  `badge-management.yml`, etc.

**Monitoring** (8 workflows): Health checks, metrics, reporting

- `health-check-live-apps.yml`, `usage-monitoring.yml`, `repo-metrics.yml`, etc.

**AI Integration** (10 workflows): Gemini, Claude, OpenAI workflows

- `gemini-review.yml`, `claude-code-review.yml`, `jules.yml`, etc.

**Maintenance** (8 workflows): Cleanup, versioning, documentation

- `branch-cleanup-notify.yml`, `version-bump.yml`, `link-checker.yml`, etc.

---

## Adding or Modifying a Workflow

### Best Practices Checklist

Before creating or modifying a workflow, ensure:

- [ ] **Pin all actions** to commit SHAs or specific versions (never `@master`
      or `@main`)
- [ ] **Set minimal permissions** explicitly (never use default permissions)
- [ ] **Add timeout-minutes** to all jobs (prevent hanging jobs)
- [ ] **Implement concurrency control** (prevent redundant runs)
- [ ] **Enable dependency caching** (faster builds)
- [ ] **Use path filters** to avoid unnecessary runs
- [ ] **Add clear job and step names** for easy debugging

### Workflow Template

```yaml
name: My New Workflow

on:
  push:
    branches: [main, master]
    paths: # Only run when relevant files change
      - "src/**"
      - "tests/**"

concurrency: # Cancel in-progress runs
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions: # Minimal permissions
  contents: read

jobs:
  my-job:
    runs-on: ubuntu-latest
    timeout-minutes: 10 # Prevent hanging

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip" # Enable caching

      - name: Your steps here
        run: echo "Hello World"
```

---

## Common Tasks

### Adding Caching

**For Python workflows:**

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: "pip" # ⭐ Add this line
```

**For Node.js workflows:**

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm" # ⭐ Add this line
```

**For Ruby workflows:**

```yaml
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: "3.1"
    bundler-cache: true # ⭐ Add this line
```

**For Go workflows:**

```yaml
- uses: actions/setup-go@v4
  with:
    go-version: "1.21"
    cache: true # ⭐ Add this line
```

### Pinning Actions to Versions

**❌ INSECURE (never do this):**

```yaml
uses: actions/checkout@master
uses: aquasecurity/trivy-action@main
```

**✅ SECURE (always do this):**

```yaml
# Option 1: Pin to specific version
uses: actions/checkout@v4

# Option 2: Pin to commit SHA (most secure)
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

### Setting Minimal Permissions

**❌ BAD (too permissive):**

```yaml
permissions: write-all
```

**✅ GOOD (minimal and explicit):**

```yaml
permissions:
  contents: read # Read repository contents
  pull-requests: write # Comment on PRs (if needed)
```

### Adding Path Filters

**Without filters (runs on every push):**

```yaml
on:
  push:
    branches: [main]
```

**With filters (only runs when relevant files change):**

```yaml
on:
  push:
    branches: [main]
    paths:
      - "src/**" # Any file in src/
      - "**.py" # Any Python file
      - "requirements.txt" # Specific file
      - "!docs/**" # Exclude docs/
```

---

## Debugging Workflows

### Common Issues and Solutions

#### 1. Cache Not Working?

**Problem:** Cache isn't being restored

**Check:**

```yaml
# Make sure hashFiles pattern matches your dependency files
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
#                                         ↑
#                            Use ** to include subdirectories
```

#### 2. Workflow Not Triggering?

**Problem:** Workflow doesn't run when expected

**Check:**

- Path filters: `paths:` must match changed files
- Branch filters: `branches:` must match your branch name
- Event type: Correct `on:` event (push, pull_request, etc.)

#### 3. Permission Denied?

**Problem:** Job fails with permission error

**Add required permission:**

```yaml
permissions:
  contents: write # For git push
  packages: write # For docker push
  pull-requests: write # For PR comments
```

#### 4. Timeout?

**Problem:** Job times out

**Solution:**

```yaml
jobs:
  my-job:
    timeout-minutes: 30 # Increase timeout
```

#### 5. Secret Not Available?

**Problem:** Secret is undefined or empty

**Check:**

- Secret exists in repository/organization settings
- Secret name matches exactly (case-sensitive)
- Workflow has permission to access it

### Testing Workflows Locally

Use [act](https://github.com/nektos/act) to test workflows locally:

```bash
# Install act
brew install act  # macOS
# or: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Test a workflow
act -W .github/workflows/ci.yml

# Test with specific event
act push -W .github/workflows/ci.yml

# List available workflows
act -l
```

### Viewing Workflow Logs

```bash
# List recent runs
gh run list --limit 10

# View specific workflow runs
gh run list --workflow=ci.yml

# View logs
gh run view <run-id> --log

# Re-run failed jobs
gh run rerun <run-id> --failed
```

---

## Security Best Practices

### 1. Never Commit Secrets

**❌ NEVER:**

```yaml
env:
  API_KEY: "my-secret-key-12345" # NEVER!
```

**✅ ALWAYS:**

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }} # Use GitHub Secrets
```

### 2. Use Minimal Permissions

Always specify minimum required permissions:

```yaml
permissions:
  contents: read # Start with read-only
```

Add more only if needed:

```yaml
permissions:
  contents: read
  pull-requests: write # Only if PR comments needed
```

### 3. Pin Action Versions

Security best practice: pin to commit SHA:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

### 4. Validate User Input

If workflow accepts manual input, validate it:

```yaml
- name: Validate input
  run: |
    if [[ ! "${{ inputs.version }}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo "Invalid version format"
      exit 1
    fi
```

---

## Performance Optimization

### Enable Caching

Caching saves 30-40% on build times:

- Python: `cache: 'pip'`
- Node.js: `cache: 'npm'`
- Ruby: `bundler-cache: true`
- Go: `cache: true`

### Use Path Filters

Only run workflows when relevant files change:

```yaml
paths:
  - "src/**"
  - "!docs/**" # Exclude docs
```

### Cancel Redundant Runs

Prevent multiple runs of same workflow:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Use Matrix Strategy

Run tests in parallel:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
  max-parallel: 3
```

---

## Getting Help

### Internal Resources

- **Quick Reference**:
  [`WORKFLOW_QUICK_REFERENCE.md`](WORKFLOW_QUICK_REFERENCE.md) - Copy-paste
  solutions
- **Security Audit**: [`WORKFLOW_SECURITY_AUDIT.md`](WORKFLOW_SECURITY_AUDIT.md)
  \- Security best practices
- **Implementation Guide**:
  [`NEXT_STEPS_IMPLEMENTATION.md`](NEXT_STEPS_IMPLEMENTATION.md) - Step-by-step
  optimization
- **Full Analysis**:
  [`COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md`](COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md)
  \- Complete review

### External Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)<!-- link:docs.github_actions -->
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)<!-- link:docs.github_actions_workflow_syntax -->
- [Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)<!-- link:docs.github_actions_hardening -->
- [Caching Dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)<!-- link:docs.github_actions_caching -->

### Getting Support

1. **Check existing workflows** - Look for similar patterns in our 76 workflows
1. **Use the quick reference** - Most common patterns are documented
1. **Test locally with act** - Faster iteration than push-and-wait
1. **Ask in PR** - Tag reviewers for workflow-specific questions

---

## Workflow Review Checklist

Before submitting a PR with workflow changes:

- [ ] All actions pinned to versions (no `@master`/`@main`)
- [ ] Minimal permissions specified
- [ ] Timeout added to jobs
- [ ] Concurrency control implemented
- [ ] Caching enabled (if applicable)
- [ ] Path filters added (if applicable)
- [ ] Clear step names
- [ ] Tested locally with `act` (if possible)
- [ ] No hardcoded secrets
- [ ] Documentation updated (if needed)

---

## Examples from Our Repository

### Example 1: Simple CI Workflow

See `.github/workflows/ci.yml` for a well-structured CI workflow with:

- ✅ Pinned actions
- ✅ Minimal permissions
- ✅ Timeout configured
- ✅ Caching enabled
- ✅ Path filters
- ✅ Concurrency control

### Example 2: Security Scanning

See `.github/workflows/security-scan.yml` for security scanning with:

- ✅ Multiple security tools
- ✅ SARIF upload to Security tab
- ✅ Matrix strategy for multiple languages

### Example 3: Deployment

See `.github/workflows/docker-build-push.yml` for deployment with:

- ✅ Conditional execution
- ✅ Multi-platform builds
- ✅ Artifact generation
- ✅ Security scanning

---

## Conventions

### Naming

- Workflow files: `kebab-case.yml`
- Job names: `lowercase-with-dashes`
- Step names: "Title Case With Spaces"

### Organization

- Group related jobs in same workflow
- One workflow per main purpose
- Use reusable workflows for common patterns

### Comments

Add comments for complex logic:

```yaml
# Check if this is a production deployment
- name: Check environment
  run: |
    # Only deploy to prod on main branch
    if [ "${{ github.ref }}" = "refs/heads/main" ]; then
      echo "env=production" >> $GITHUB_OUTPUT
    fi
```

---

**Questions?** Check the [Quick Reference](WORKFLOW_QUICK_REFERENCE.md) or open
an issue!

**Last Updated**: 2025-12-23\
**Maintained By**: Workflow Optimization Team

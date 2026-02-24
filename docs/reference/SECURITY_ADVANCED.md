# Advanced Security Configuration

Comprehensive guide for implementing advanced security measures in your
repository.

## Table of Contents

- [Secret Scanning](#secret-scanning)
- [Dependency Security](#dependency-security)
- [Code Scanning](#code-scanning)
- [Container Security](#container-security)
- [Access Control](#access-control)
- [Audit Logging](#audit-logging)
- [Security Automation](#security-automation)

______________________________________________________________________

## Secret Scanning

### Enable GitHub Secret Scanning

1. Navigate to repository **Settings** → **Security & analysis**
1. Enable **Secret scanning**
1. Enable **Push protection**

### Configure Secret Detection

Create `.secrets.baseline` for pre-commit hooks:

```bash
detect-secrets scan > .secrets.baseline
```

### Prevent Secrets in Code

**.gitignore** additions:

```
# Environment variables
.env
.env.local
.env.*.local

# Credentials
credentials.json
secrets.yaml
*.key
*.pem
*.p12

# AWS
.aws/

# SSH keys
id_rsa
id_ed25519
```

### Use Environment Variables

**Bad**:

```javascript
const apiKey = "sk_live_abc123..."; // Don't do this!
```

**Good**:

```javascript
const apiKey = process.env.API_KEY;
```

### Rotate Compromised Secrets

```bash
# 1. Revoke compromised credentials immediately
# 2. Update secrets in your secret manager
# 3. Update environment variables
# 4. Restart services
# 5. Audit access logs
```

______________________________________________________________________

## Dependency Security

### Dependency Scanning

Enabled workflows:

- **Dependabot**: `dependabot.yml`
- **Renovate**: `renovate.json`
- **Dependency Review**: `.github/workflows/dependency-review.yml`

### Security Advisories

Monitor security advisories:

```bash
# GitHub CLI
gh api repos/OWNER/REPO/dependabot/alerts

# Check specific package
npm audit
pip-audit
cargo audit
```

### Update Strategy

1. **Critical vulnerabilities**: Immediate update
1. **High severity**: Within 7 days
1. **Medium severity**: Within 30 days
1. **Low severity**: Next release cycle

### Lock Files

**Always commit lock files**:

- `package-lock.json` (npm)
- `yarn.lock` (Yarn)
- `pnpm-lock.yaml` (pnpm)
- `Pipfile.lock` (Python)
- `Gemfile.lock` (Ruby)
- `go.sum` (Go)
- `Cargo.lock` (Rust)

### Supply Chain Security

```yaml
# .github/workflows/supply-chain-security.yml
name: Supply Chain Security

on: [push, pull_request]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: spdx-json

      - name: Scan SBOM
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.spdx.json
```

______________________________________________________________________

## Code Scanning

### CodeQL Configuration

**Advanced `.github/codeql/codeql-config.yml`**:

```yaml
name: "CodeQL Config"

queries:
  - uses: security-extended
  - uses: security-and-quality

paths-ignore:
  - "node_modules"
  - "dist"
  - "build"
  - "vendor"
  - "**/*.test.js"
  - "**/*.spec.ts"

paths:
  - "src"
  - "lib"

query-filters:
  - exclude:
      id: js/unused-local-variable

languages:
  - javascript
  - python
  - go
```

### Custom CodeQL Queries

Create custom queries in `.github/codeql/queries/`:

```ql
/**
 * @name Hardcoded credentials
 * @kind problem
 * @id custom/hardcoded-credentials
 */

import javascript

from StringLiteral str
where str.getValue().regexpMatch("(?i).*(password|api[_-]?key|secret).*")
  and str.getValue().length() > 10
select str, "Potential hardcoded credential"
```

### SARIF Upload

```yaml
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
    category: custom-analysis
```

______________________________________________________________________

## Container Security

### Image Scanning

**Trivy Scanning**:

```yaml
- name: Scan Docker Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: "myimage:latest"
    format: "sarif"
    output: "trivy-results.sarif"
    severity: "CRITICAL,HIGH"
    exit-code: "1"
```

**Snyk Container Scan**:

```yaml
- name: Snyk Container Scan
  uses: snyk/actions/docker@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    image: myimage:latest
    args: --severity-threshold=high
```

### Runtime Security

**Falco Rules** for container runtime security:

```yaml
# /etc/falco/falco_rules.local.yaml
- rule: Unauthorized Process in Container
  desc: Detect unauthorized process execution
  condition: >
    spawned_process and container
    and not proc.name in (node, python, java)
  output: >
    Unauthorized process in container
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING
```

### Container Hardening

```dockerfile
# Use distroless for minimal attack surface
FROM gcr.io/distroless/nodejs:18

# Run as non-root
USER nonroot:nonroot

# Read-only root filesystem
# Set in docker run: --read-only

# Drop all capabilities
# Set in docker run: --cap-drop=ALL

# No new privileges
# Set in docker run: --security-opt=no-new-privileges
```

______________________________________________________________________

## Access Control

### Repository Permissions

**Principle of Least Privilege**:

- **Admin**: Only 1-2 trusted maintainers
- **Write**: Core contributors
- **Read**: Everyone else
- **No access**: Revoke inactive users

### Branch Protection

See `BRANCH_PROTECTION.md` for detailed rules.

**Essential protections**:

```yaml
# Via GitHub API
{
  "required_status_checks":
    { "strict": true, "contexts": ["ci/tests", "security/scan"] },
  "enforce_admins": true,
  "required_pull_request_reviews":
    {
      "dismissal_restrictions": {},
      "dismiss_stale_reviews": true,
      "require_code_owner_reviews": true,
      "required_approving_review_count": 2,
    },
  "restrictions": null,
  "required_signatures": true,
}
```

### CODEOWNERS Enforcement

```
# Require security team review for security-sensitive files
/src/auth/ @security-team
/config/secrets/ @security-team
*.key @security-team
SECURITY.md @security-team
```

### SSH Key Management

**Best Practices**:

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add passphrase protection
# Use SSH agent for convenience
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Regularly rotate keys (every 90-180 days)
# Remove old keys from GitHub
```

### GPG Commit Signing

```bash
# Generate GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Export public key
gpg --armor --export KEY_ID

# Add to GitHub: Settings → SSH and GPG keys

# Configure Git
git config --global user.signingkey KEY_ID
git config --global commit.gpgsign true

# Sign commits
git commit -S -m "feat: add feature"
```

______________________________________________________________________

## Audit Logging

### GitHub Audit Log

**Access audit log**:

```bash
# Using GitHub CLI
gh api /orgs/ORG/audit-log

# Filter by event type
gh api "/orgs/ORG/audit-log?phrase=action:repo.create"
```

### Monitor Critical Events

- Repository created/deleted
- User added/removed
- Permission changes
- Secret access
- Deploy key changes
- Webhook modifications

### Export Audit Logs

```bash
# Export for compliance
gh api /orgs/ORG/audit-log \
  --paginate \
  --jq '.[] | select(.created_at >= "2024-01-01")' \
  > audit-log-2024.json
```

### Third-Party Monitoring

Integrate with:

- **Datadog**: Security monitoring
- **Splunk**: Log aggregation
- **Elasticsearch**: Search and analytics
- **CloudTrail**: AWS infrastructure
- **Azure Monitor**: Azure infrastructure

______________________________________________________________________

## Security Automation

### Security Workflow

```yaml
name: Security Checks

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: "0 0 * * 0" # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      # 1. Secret scanning
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      # 2. Dependency audit
      - name: Audit dependencies
        run: |
          npm audit --audit-level=moderate
          pip-audit

      # 3. License check
      - name: Check licenses
        uses: fossas/fossa-action@main
        with:
          api-key: ${{ secrets.FOSSA_API_KEY }}

      # 4. SAST scanning
      - name: SAST with Semgrep
        uses: returntocorp/semgrep-action@v1

      # 5. Infrastructure as Code scanning
      - name: Scan IaC
        uses: bridgecrewio/checkov-action@master
        with:
          directory: infrastructure/
          framework: terraform

      # 6. API security testing
      - name: API Security Test
        uses: stackhawk/hawkscan-action@v2
        with:
          apiKey: ${{ secrets.HAWK_API_KEY }}
```

### Automated Dependency Updates

**Auto-merge safe updates**:

```yaml
name: Auto-merge Dependabot

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v1

      - name: Auto-merge patch updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

### Security Notifications

**Slack Integration**:

```yaml
- name: Notify security team
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "🚨 Security check failed in ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Security Alert*\nCheck: ${{ github.workflow }}\nBranch: ${{ github.ref }}"
            }
          }
        ]
      }
```

______________________________________________________________________

## Security Checklist

### Repository Setup

- [ ] Enable secret scanning
- [ ] Enable push protection
- [ ] Configure Dependabot
- [ ] Set up CodeQL
- [ ] Add SECURITY.md
- [ ] Configure branch protection
- [ ] Require signed commits
- [ ] Enable 2FA for all users

### CI/CD Pipeline

- [ ] Scan for secrets
- [ ] Audit dependencies
- [ ] Run SAST tools
- [ ] Scan containers
- [ ] Check licenses
- [ ] Verify signatures

### Access Control

- [ ] Review permissions quarterly
- [ ] Remove inactive users
- [ ] Audit CODEOWNERS
- [ ] Rotate secrets regularly
- [ ] Monitor audit logs

### Incident Response

- [ ] Document response plan
- [ ] Designate security contacts
- [ ] Set up alerting
- [ ] Practice incident drills
- [ ] Maintain runbooks

______________________________________________________________________

## Security Tools Comparison

| Tool           | Purpose       | Cost       | Best For               |
| -------------- | ------------- | ---------- | ---------------------- |
| **CodeQL**     | SAST          | Free (OSS) | Code analysis          |
| **Dependabot** | Dependencies  | Free       | Dependency updates     |
| **Snyk**       | Multi-purpose | Paid       | Comprehensive scanning |
| **Trivy**      | Container     | Free       | Container scanning     |
| **Semgrep**    | SAST          | Free tier  | Custom rules           |
| **FOSSA**      | License       | Paid       | License compliance     |
| **SonarQube**  | Code quality  | Paid       | Quality + security     |
| **Checkmarx**  | SAST          | Paid       | Enterprise             |

______________________________________________________________________

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GitHub Security Features](https://docs.github.com/en/code-security)<!-- link:docs.github_code_security -->
- [SLSA Framework](https://slsa.dev/)

______________________________________________________________________

**Last Updated**: 2024-11-08

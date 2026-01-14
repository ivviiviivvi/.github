# Security Best Practices Guide

> **Comprehensive security guidelines for the ivviiviivvi/.github organization**

**Last Updated:** 2026-01-14

---

## Table of Contents

- [Overview](#overview)
- [Security Disclosure](#security-disclosure)
- [Secret Management](#secret-management)
- [PII and Sensitive Data](#pii-and-sensitive-data)
- [GitHub Actions Security](#github-actions-security)
- [Dependency Security](#dependency-security)
- [Security Tools](#security-tools)
- [Incident Response](#incident-response)

---

## Overview

This guide provides comprehensive security best practices for all repositories
in the ivviiviivvi organization. All contributors must follow these guidelines
to maintain the security posture of our projects.

### Security Principles

1. **Defense in Depth**: Multiple layers of security controls
1. **Least Privilege**: Minimal necessary permissions
1. **Fail Securely**: Security-first error handling
1. **Privacy by Design**: PII protection built-in
1. **Continuous Monitoring**: Ongoing security validation

---

## Security Disclosure

### How to Report Security Issues

**🔴 MANDATORY: All security issues MUST be reported privately**

1. **Navigate to Security Advisories**:
   - Go to: <https://github.com/ivviiviivvi/.github/security/advisories/new>

1. **Fill Out the Advisory Form**:
   - Provide detailed description of the vulnerability
   - Include steps to reproduce
   - Assess potential impact
   - Suggest mitigation if known

1. **Wait for Response**:
   - Security team will acknowledge within 48 hours
   - We will work with you to validate and fix the issue
   - Credit will be provided in security advisories

### Why Private Disclosure?

- **Protect Users**: Prevent exploitation before fix is available
- **Coordinated Response**: Allow time for proper fix and testing
- **Responsible Practice**: Industry standard for security issues
- **Legal Protection**: Avoid potential legal issues from public disclosure

### What Qualifies as a Security Issue?

✅ **Report Privately**:

- Authentication/authorization bypasses
- Data exposure or leaks
- Code injection vulnerabilities
- Denial of service vulnerabilities
- Cryptographic weaknesses
- Privilege escalation
- Cross-site scripting (XSS)
- SQL injection
- Remote code execution

❌ **Not Security Issues** (use bug reports):

- Feature requests
- Performance issues
- Documentation errors
- Non-security bugs

---

## Secret Management

### Secret Scanning

We use multiple tools to prevent secrets from being committed:

#### detect-secrets

**Local Scanning:**

```bash
# Scan all files
detect-secrets scan --all-files

# Update baseline after reviewing findings
detect-secrets scan --update .secrets.baseline

# Audit findings
detect-secrets audit .secrets.baseline
```

**Pre-commit Hook:**

The `detect-secrets` pre-commit hook automatically scans staged files:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ["--baseline", ".secrets.baseline"]
```

#### GitHub Secret Scanning

Enabled for all repositories:

- Automatically detects known secret patterns
- Alerts repository administrators
- Blocks pushes with detected secrets (if push protection enabled)

### Managing Secrets Baseline

The `.secrets.baseline` file contains known false positives:

**Updating Baseline:**

```bash
# After resolving findings, update baseline
detect-secrets scan --update .secrets.baseline

# Review changes
git diff .secrets.baseline

# Commit if changes are valid
git add .secrets.baseline
git commit -m "chore: update secrets baseline"
```

**Auditing Process:**

1. Run: `detect-secrets audit .secrets.baseline`
1. For each finding:
   - Press `y` if it's a real secret (remove it!)
   - Press `n` if it's a false positive (keep in baseline)
   - Press `s` to skip decision
1. Save changes when done

### Environment Variables

**✅ DO:**

- Store secrets in environment variables
- Use GitHub Secrets for Actions
- Use secret management services (Vault, AWS Secrets Manager)
- Document required environment variables (without values)

**❌ DON'T:**

- Hardcode secrets in code
- Commit `.env` files with secrets
- Include secrets in logs
- Share secrets in issue comments

### Rotating Compromised Secrets

If a secret is committed:

1. **Immediately Rotate**: Change the secret in all systems
1. **Remove from History**: Use `git filter-repo` or BFG Repo-Cleaner
1. **Force Push**: Update remote repository
1. **Notify Team**: Inform all contributors of the breach
1. **Update Baseline**: Remove from `.secrets.baseline` if present
1. **Audit Access**: Check for unauthorized access using the secret

---

## PII and Sensitive Data

### What is PII?

Personal Identifiable Information (PII) includes:

- 🔴 **Full names** (when combined with other info)
- 🔴 **Email addresses**
- 🔴 **Phone numbers**
- 🔴 **Physical addresses**
- 🔴 **IP addresses** (in some contexts)
- 🔴 **Social security numbers**
- 🔴 **Driver's license numbers**
- 🔴 **Credit card numbers**
- 🔴 **Biometric data**
- 🔴 **Medical information**

### PII Handling Guidelines

**When Reporting Bugs:**

✅ **Safe to Include:**

- General error messages
- Stack traces (sanitized)
- Configuration examples
- Code snippets (without secrets)
- Non-sensitive logs

❌ **Never Include:**

- Real user data
- Customer information
- Authentication credentials
- API keys or tokens
- Personal emails or phone numbers
- Internal system details

### Sanitizing Logs

**Example of Proper Sanitization:**

```log
# ❌ WRONG - Contains PII and secrets
2024-01-14 10:30:45 [ERROR] Login failed for user john.doe@example.com
2024-01-14 10:30:45 [DEBUG] API Key: sk_live_51abc123xyz789
2024-01-14 10:30:45 [INFO] Connecting to database at 192.168.1.100:5432

# ✅ CORRECT - Sanitized
2024-01-14 10:30:45 [ERROR] Login failed for user [REDACTED_EMAIL]
2024-01-14 10:30:45 [DEBUG] API Key: [REDACTED_API_KEY]
2024-01-14 10:30:45 [INFO] Connecting to database at [REDACTED_IP]:5432
```

**Sanitization Checklist:**

- [ ] Replace emails with `[REDACTED_EMAIL]`
- [ ] Replace passwords with `[REDACTED_PASSWORD]`
- [ ] Replace API keys with `[REDACTED_API_KEY]`
- [ ] Replace tokens with `[REDACTED_TOKEN]`
- [ ] Replace IP addresses with `[REDACTED_IP]`
- [ ] Replace usernames with `[REDACTED_USER]`
- [ ] Replace customer IDs with `[REDACTED_ID]`

---

## GitHub Actions Security

### SHA Pinning

**✅ BEST PRACTICE: Pin Actions to Full Commit SHAs**

We use [Ratchet](https://github.com/sethvargo/ratchet) to maintain SHA pinning:

```yaml
# ✅ CORRECT - SHA pinned with ratchet comment
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # ratchet:actions/checkout@v4.2.2

# ❌ WRONG - Semantic version only
- uses: actions/checkout@v4

# ❌ WRONG - SHA without context
- uses: actions/checkout@11bd719
```

**Why SHA Pinning?**

- **Immutability**: Tags can be moved, SHAs cannot
- **Security**: Prevents malicious tag updates
- **Reproducibility**: Exact version is always used
- **Auditability**: Clear what code is running

**Updating Pinned Actions:**

```bash
# Install ratchet
go install github.com/sethvargo/ratchet@latest

# Update all workflows
ratchet update .github/workflows/*.yml

# Commit updates
git add .github/workflows/
git commit -m "chore: update action SHA pins"
```

### Secrets in Actions

**✅ DO:**

- Use GitHub Secrets for sensitive values
- Use minimal scope for tokens
- Rotate secrets regularly
- Use environment-specific secrets

**❌ DON'T:**

- Echo secrets in logs
- Pass secrets as command-line arguments
- Store secrets in workflow files
- Use personal access tokens unnecessarily

**Example:**

```yaml
# ✅ CORRECT
- name: Deploy
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
  run: |
    # Token is in environment, not visible in logs
    ./deploy.sh

# ❌ WRONG
- name: Deploy
  run: |
    # Token will appear in logs!
    ./deploy.sh --token=${{ secrets.API_TOKEN }}
```

### Workflow Permissions

**Principle of Least Privilege:**

```yaml
# Minimal permissions
permissions:
  contents: read

# Specific permissions only
permissions:
  contents: write
  pull-requests: write
  issues: read

# Avoid unless necessary
permissions: write-all
```

---

## Dependency Security

### Dependabot Configuration

Dependabot automatically creates PRs for dependency updates:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### Version Pinning Strategy

**Pre-commit Hooks:**

```yaml
# Pin to specific versions
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.5.0 # ✅ Specific version
  hooks:
    - id: trailing-whitespace

# Avoid floating versions
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: master # ❌ Mutable reference
```

**Python Dependencies:**

```txt
# requirements.txt
requests==2.31.0        # ✅ Exact version
black~=23.0             # ✅ Compatible version
pytest>=7.0,<8.0        # ✅ Range with upper bound
Django                   # ❌ Unpinned
```

### Auditing Dependencies

**Python:**

```bash
# Install pip-audit
pip install pip-audit

# Scan for vulnerabilities
pip-audit

# Scan requirements file
pip-audit -r requirements.txt
```

**Node.js:**

```bash
# Audit npm dependencies
npm audit

# Fix automatically fixable issues
npm audit fix

# Review manual fixes
npm audit fix --force
```

---

## Security Tools

### Pre-commit Hooks

Security-focused hooks in `.pre-commit-config.yaml`:

```yaml
# Secret detection
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ["--baseline", ".secrets.baseline"]

# Python security
- repo: https://github.com/PyCQA/bandit
  rev: 1.7.5
  hooks:
    - id: bandit
      args: ["-c", ".bandit"]

# Dependency security
- repo: https://github.com/pyupio/safety
  rev: 2.3.5
  hooks:
    - id: safety
      args: ["--ignore", "51457"]
```

### GitHub Security Features

Enable these features for all repositories:

- ✅ **Secret Scanning**: Detects committed secrets
- ✅ **Push Protection**: Blocks secret pushes
- ✅ **Dependabot Alerts**: Vulnerability notifications
- ✅ **Dependabot Security Updates**: Auto-fix PRs
- ✅ **Code Scanning**: SAST with CodeQL
- ✅ **Private Vulnerability Reporting**: Responsible disclosure

### Regular Security Audits

**Monthly Tasks:**

- [ ] Review Dependabot alerts
- [ ] Update pinned action SHAs
- [ ] Audit secrets baseline
- [ ] Review access permissions
- [ ] Check security advisory feed

**Quarterly Tasks:**

- [ ] Full security assessment
- [ ] Update security policies
- [ ] Security training review
- [ ] Incident response drill
- [ ] Third-party audit (if applicable)

---

## Incident Response

### Security Incident Process

1. **Detection & Reporting**
   - Security tool alerts
   - User reports
   - Internal discovery

1. **Initial Assessment**
   - Validate the issue
   - Assess severity and impact
   - Determine scope

1. **Containment**
   - Isolate affected systems
   - Rotate compromised credentials
   - Block malicious access

1. **Eradication**
   - Remove vulnerabilities
   - Apply patches
   - Verify fix

1. **Recovery**
   - Restore services
   - Monitor for recurrence
   - Verify normal operation

1. **Post-Incident**
   - Document lessons learned
   - Update security measures
   - Notify affected parties
   - Publish security advisory

### Severity Levels

**🔴 CRITICAL**

- Data breach
- Remote code execution
- Authentication bypass
- Response: Immediate (within hours)

**🟠 HIGH**

- Privilege escalation
- SQL injection
- Unvalidated redirects
- Response: Within 24 hours

**🟡 MEDIUM**

- Information disclosure
- Missing security headers
- Weak cryptography
- Response: Within 1 week

**🟢 LOW**

- Security hardening opportunities
- Minor configuration issues
- Documentation gaps
- Response: Next security review

---

## Additional Resources

### Documentation

- [SECURITY.md](../SECURITY.md) - Security disclosure policy
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [Dependency Management Guide](dependency-management.md) - Dependency best
  practices

### External Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Tools

- [detect-secrets](https://github.com/Yelp/detect-secrets) - Secret scanning
- [Ratchet](https://github.com/sethvargo/ratchet) - Action SHA pinning
- [pip-audit](https://github.com/pypa/pip-audit) - Python vulnerability scanning
- [Bandit](https://github.com/PyCQA/bandit) - Python security linter

---

## Questions or Concerns?

- **Security Issues**: Use
  [private security advisory](https://github.com/ivviiviivvi/.github/security/advisories/new)
- **General Questions**: Open a
  [discussion](https://github.com/ivviiviivvi/.github/discussions)
- **Documentation Improvements**: Submit a [pull request](../CONTRIBUTING.md)

---

**Remember: Security is everyone's responsibility. When in doubt, ask!**

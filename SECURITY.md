# Security Policy

## Supported Versions

We take security seriously and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

**Note:** Only the latest major version receives security updates. Please upgrade to the latest version to ensure you have the latest security patches.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

We strongly encourage responsible disclosure of security vulnerabilities. If you discover a security issue, please report it privately using one of the following methods:

### Preferred Method: GitHub Security Advisories

1. Navigate to the repository's **Security** tab
2. Click **"Report a vulnerability"**
3. Fill out the advisory form with details about the vulnerability
4. Submit the report

GitHub Security Advisories allow us to:
- Discuss the vulnerability privately
- Collaborate on a fix
- Publish a CVE if needed
- Credit you for the discovery

**Report URL:** [https://github.com/ivviiviivvi/.github/security/advisories/new](https://github.com/ivviiviivvi/.github/security/advisories/new)

### Alternative: Security Contact Email

If you prefer email or cannot use GitHub Security Advisories, email us at:

**📧 security@ivviiviivvi.com**

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

## Response Timeline

We are committed to responding quickly to security reports:

| Timeline | Action |
|----------|--------|
| **Within 24 hours** | Acknowledgment of your report |
| **Within 72 hours** | Initial assessment and severity classification |
| **Within 7 days** | Detailed response with remediation plan |
| **Within 30 days** | Fix deployed (for critical/high severity issues) |

Response times may vary based on:
- Severity of the vulnerability
- Complexity of the fix
- Need for coordinated disclosure with other parties

## Vulnerability Disclosure Process

1. **Report Received** - We acknowledge receipt within 24 hours
2. **Assessment** - We evaluate severity and impact (72 hours)
3. **Remediation** - We develop and test a fix
4. **Disclosure** - We coordinate disclosure timing with you
5. **Release** - We deploy the fix and publish an advisory
6. **Credit** - We publicly credit you (unless you prefer anonymity)

## Severity Classification

We use the [CVSS 3.1](https://www.first.org/cvss/calculator/3.1) scoring system:

- **Critical (9.0-10.0)**: Immediate action required
- **High (7.0-8.9)**: Urgent fix needed
- **Medium (4.0-6.9)**: Important fix needed
- **Low (0.1-3.9)**: Minor issue

## Bug Bounty Program

**Status:** Coming Soon

We are planning to launch a bug bounty program to reward security researchers who responsibly disclose vulnerabilities. Details will be published here when available.

Interested in participating? Watch this repository or contact us at security@ivviiviivvi.com.

## Security Scanning Tools

We use the following automated security tools to detect vulnerabilities:

### Secret Detection
- **[TruffleHog](https://github.com/trufflesecurity/trufflehog)** - Scans for secrets, API keys, tokens
- **[Gitleaks](https://github.com/gitleaks/gitleaks)** - Detects hardcoded credentials and sensitive data
- **[detect-secrets](https://github.com/Yelp/detect-secrets)** - Prevents secrets from entering the codebase

### Dependency Scanning
- **[Dependabot](https://github.com/dependabot)** - Automated dependency updates and security patches
- **[GitHub Advanced Security](https://docs.github.com/en/code-security)** - Dependency vulnerability scanning

### Code Analysis
- **[CodeQL](https://codeql.github.com/)** - Semantic code analysis for security vulnerabilities
- **[Semgrep](https://semgrep.dev/)** - Static analysis for security patterns

## Security Workflows

Our security workflows run automatically on every push and pull request:

- **🔒 Secret Scanning** - [`.github/workflows/security-scan.yml`](.github/workflows/security-scan.yml)
- **🔍 Code Scanning (CodeQL)** - [`.github/workflows/codeql.yml`](.github/workflows/codeql.yml)
- **📦 Dependency Review** - [`.github/workflows/dependency-review.yml`](.github/workflows/dependency-review.yml)

View all security workflows: [Security Workflows](.github/workflows/)

## Security Best Practices

When contributing to this project:

- ✅ Never commit secrets, API keys, passwords, or tokens
- ✅ Use environment variables or secrets management for sensitive data
- ✅ Keep dependencies up to date
- ✅ Follow secure coding practices
- ✅ Review our [CONTRIBUTING.md](CONTRIBUTING.md) guidelines
- ✅ Run security checks locally before pushing

## Security Contacts

- **General Security Issues:** security@ivviiviivvi.com
- **Security Team:** @ivviiviivvi/security
- **Emergency Contact:** [Create a private security advisory](https://github.com/ivviiviivvi/.github/security/advisories/new)

## Hall of Fame

We thank the following researchers for responsibly disclosing security vulnerabilities:

<!-- This section will be populated as researchers report vulnerabilities -->
*No vulnerabilities reported yet.*

---

**Last Updated:** January 12, 2026

For general questions about this policy, please contact security@ivviiviivvi.com.

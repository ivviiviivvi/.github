# Security Policy

## Supported Versions

We take security seriously. Please report security vulnerabilities responsibly.

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public issue
2. **Email** the security concern to the repository maintainers
3. **Include** as much information as possible:
   - Type of vulnerability
   - Full paths of affected source files
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue

## Response Process

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a detailed response within 7 days indicating next steps
- We will work on a fix and keep you informed of progress
- Once the vulnerability is fixed, we will publicly disclose the issue (crediting you if desired)

## Automated Secret Scanning

We use automated secret scanning to protect against accidental credential exposure in code and video walkthroughs.

### Scanning Tools

Our repository is continuously monitored by three complementary secret detection tools:

1. **TruffleHog** - Entropy-based secret detection and regex pattern matching
2. **Gitleaks** - High-speed secret scanning with customizable rules
3. **detect-secrets** - Baseline-driven secret detection with plugin support

### Scan Schedule

- **Daily**: Automated scans run at 2:00 AM UTC
- **On Push**: Scans trigger on commits to main/master branches
- **On PR**: Pull requests are scanned before merge
- **Manual**: Workflows can be triggered on-demand via workflow_dispatch

### Workflows

- **Code Scanning** (`.github/workflows/scan-for-secrets.yml`): Scans all code files for hardcoded secrets
- **Video Scanning** (`.github/workflows/safeguard-5-secret-scanning.yml`): OCR analysis of video frames for visible credentials

### Configuration Files

Secret scanning can be customized using:

- `.gitleaks.toml` - Configure Gitleaks rules and allowlists
- `.secrets.baseline` - Manage detect-secrets baseline for known false positives

### What Happens When Secrets Are Detected

1. **Automated Issue Creation**: A security alert issue is created with scan details
2. **Workflow Failure**: The scan workflow fails to block merges
3. **Artifact Upload**: Detailed scan results are uploaded for review
4. **PR Blocking**: Pull requests are automatically blocked until secrets are removed

### Reviewing Scan Results

1. Check the automated issue for high-level summary
2. Download scan result artifacts from the workflow run
3. Review each detection to determine if it's a true positive or false positive
4. Update configuration files to suppress false positives if needed

### Responding to Secret Detections

If real secrets are detected:

1. **Immediately rotate** the exposed credentials
2. **Remove secrets** from the current codebase
3. **Clean git history** using tools like [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) or git-filter-repo
4. **Update documentation** and processes to prevent recurrence
5. **Re-record videos** if secrets appeared in walkthrough recordings

### Scan Results

All scan results are tracked in security alert issues with the `security` and `secrets` labels. Regular clean scans indicate the repository is free from hardcoded credentials.

## Security Best Practices

When contributing, please:

- Never commit sensitive information (API keys, passwords, tokens)
- Use environment variables for configuration secrets
- Keep dependencies up to date
- Follow secure coding practices
- Review video recordings before publishing to ensure no secrets are visible

## Disclosure Policy

We follow responsible disclosure practices:

- Security issues are fixed before public disclosure
- Contributors who report security issues are credited (unless they prefer anonymity)
- We coordinate disclosure with affected parties when applicable

Thank you for helping keep our projects secure!

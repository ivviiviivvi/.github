# Security Policy

## Reporting Security Vulnerabilities

We take the security of this project seriously. If you discover a security
vulnerability, please report it responsibly.

### How to Report

**ALL security vulnerabilities must be reported privately** through our
[Security Advisory](https://github.com/ivviiviivvi/.github/security/advisories/new)
page.

**DO NOT** create a public issue for ANY security vulnerabilities.

**Why private disclosure?**

- Protects users while we develop a fix
- Prevents exploitation by malicious actors
- Allows coordinated disclosure with affected parties
- Follows industry-standard responsible disclosure practices

**For non-security bugs and enhancements**, please use our regular
[issue templates](https://github.com/ivviiviivvi/.github/issues/new/choose).

## What to Include in Your Report

When reporting a security vulnerability, please include:

1. **Description**: Detailed description of the vulnerability
1. **Type**: Category of vulnerability (e.g., XSS, SQL Injection,
   Authentication)
1. **Severity**: Your assessment of the severity (Critical, High, Medium, Low)
1. **Impact**: Who or what is affected
1. **Steps to Reproduce**: Clear reproduction steps
1. **Proof of Concept**: If applicable (be responsible)
1. **Affected Versions**: Which versions are vulnerable
1. **Suggested Fix**: If you have recommendations

## Security Response Timeline

We are committed to addressing security issues promptly:

- **Critical vulnerabilities**: Response within 24 hours, patch within 7 days
- **High severity**: Response within 48 hours, patch within 14 days
- **Medium severity**: Response within 5 days, patch within 30 days
- **Low severity**: Response within 14 days, patch in next release

## Supported Versions

We provide security updates for the following versions:

| Version | Supported |
| ------- | --------- |
| Latest  | ✅ Yes    |
| \< 1.0  | ❌ No     |

## Security Best Practices

When contributing to this project:

1. **No Hardcoded Secrets**: Never commit API keys, passwords, or credentials
1. **Input Validation**: Always validate and sanitize user input
1. **Dependency Security**: Keep dependencies up to date
1. **Secure Coding**: Follow secure coding practices
1. **Security Testing**: Include security tests where appropriate
1. **Code Review**: All code must be reviewed before merging

## Security Features

This repository includes:

- **Dependabot**: Automated dependency updates
- **CodeQL**: Automated security scanning
- **Secret Scanning**: Detection of committed secrets
- **Branch Protection**: Required reviews and checks

## Contact

For security-related questions or concerns, contact:

- **Security Team**: Create a private security advisory
- **Email**: (if you have a dedicated security email)

## Bug Bounty Program

We do not currently have a bug bounty program. However, we deeply appreciate
responsible disclosure and will publicly acknowledge contributors who help
improve our security.

## Acknowledgments

We thank the following researchers for responsibly disclosing security issues:

- (Names will be added as issues are resolved)

---

**Last Updated**: 2024-12-31

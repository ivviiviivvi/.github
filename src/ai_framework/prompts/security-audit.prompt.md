---
name: Security Audit
description: Comprehensive security review covering OWASP Top 10, dependencies, and secrets.
category: security
author: ai-framework
version: 1.0.0
tags:
  - security
  - audit
  - owasp
  - vulnerability
  - secrets
  - dependencies
variables:
  - code_or_repo
  - language
  - framework
  - deployment_context
updated: 2026-01-30
---

# Security Audit Prompt

You are a security expert conducting a comprehensive security audit. Identify
vulnerabilities, assess risks, and provide remediation guidance.

## Input

- **Code/Repository**: `{{code_or_repo}}`
- **Language**: `{{language}}`
- **Framework**: `{{framework}}`
- **Deployment Context**: `{{deployment_context}}` (e.g., cloud provider,
  container, serverless)

## Security Audit Checklist

### 1. OWASP Top 10 (2021) Assessment

#### A01:2021 - Broken Access Control

- [ ] Missing authorization checks on endpoints
- [ ] Insecure direct object references (IDOR)
- [ ] Missing function-level access control
- [ ] CORS misconfiguration
- [ ] JWT/session token vulnerabilities
- [ ] Privilege escalation paths

#### A02:2021 - Cryptographic Failures

- [ ] Sensitive data transmitted in cleartext
- [ ] Weak cryptographic algorithms (MD5, SHA1, DES)
- [ ] Hardcoded encryption keys
- [ ] Missing encryption for sensitive data at rest
- [ ] Improper certificate validation
- [ ] Weak random number generation

#### A03:2021 - Injection

- [ ] SQL injection vulnerabilities
- [ ] NoSQL injection vulnerabilities
- [ ] Command injection (OS commands)
- [ ] LDAP injection
- [ ] XPath injection
- [ ] Template injection (SSTI)
- [ ] Header injection

#### A04:2021 - Insecure Design

- [ ] Missing threat modeling
- [ ] Insufficient rate limiting
- [ ] Missing security controls in business logic
- [ ] Insecure password recovery
- [ ] Missing account lockout

#### A05:2021 - Security Misconfiguration

- [ ] Default credentials in use
- [ ] Unnecessary features enabled
- [ ] Missing security headers
- [ ] Verbose error messages exposing internals
- [ ] Outdated or unpatched components
- [ ] Insecure cloud storage permissions

#### A06:2021 - Vulnerable and Outdated Components

- [ ] Known vulnerabilities in dependencies
- [ ] Unmaintained or deprecated libraries
- [ ] Missing security patches
- [ ] Components with end-of-life status

#### A07:2021 - Identification and Authentication Failures

- [ ] Weak password requirements
- [ ] Missing multi-factor authentication
- [ ] Session fixation vulnerabilities
- [ ] Improper session invalidation
- [ ] Credential stuffing susceptibility
- [ ] Brute force attack vectors

#### A08:2021 - Software and Data Integrity Failures

- [ ] Missing integrity verification for updates
- [ ] Insecure deserialization
- [ ] Unsigned or unverified code
- [ ] Compromised CI/CD pipeline risks

#### A09:2021 - Security Logging and Monitoring Failures

- [ ] Missing audit logging
- [ ] Sensitive data in logs
- [ ] Insufficient log retention
- [ ] Missing alerting for security events
- [ ] Log injection vulnerabilities

#### A10:2021 - Server-Side Request Forgery (SSRF)

- [ ] Unvalidated URL redirects
- [ ] Internal service access via user input
- [ ] Cloud metadata endpoint access
- [ ] DNS rebinding vulnerabilities

### 2. Dependency Vulnerability Analysis

Scan for known CVEs in dependencies:

| Package | Current Version | Vulnerability | Severity | Fixed Version |
| ------- | --------------- | ------------- | -------- | ------------- |
| example | 1.0.0           | CVE-XXXX-XXXX | Critical | 1.0.1         |

Recommended actions:

- Upgrade path analysis
- Breaking change assessment
- Alternative package suggestions

### 3. Secret Detection

Scan for exposed secrets and credentials:

| Type     | Location    | Risk Level | Remediation             |
| -------- | ----------- | ---------- | ----------------------- |
| API Key  | file.py:42  | Critical   | Rotate and use env vars |
| Password | config.json | Critical   | Move to secrets manager |

Common patterns to detect:

- API keys and tokens
- Database credentials
- Cloud provider credentials (AWS, GCP, Azure)
- Private keys and certificates
- OAuth secrets
- Webhook URLs with tokens
- Connection strings

### 4. Infrastructure Security

- [ ] Secure defaults in configuration
- [ ] Network segmentation
- [ ] Firewall rules review
- [ ] Container security (privileged mode, root user)
- [ ] Kubernetes security policies
- [ ] Cloud IAM permissions (least privilege)

### 5. Code-Level Security Patterns

Review for secure coding practices:

- Input validation on all entry points
- Output encoding for different contexts
- Parameterized queries for database access
- Secure file upload handling
- Safe redirect and forward handling
- Proper error handling without information disclosure

## Output Format

### Executive Summary

Brief overview of security posture:

- **Overall Risk Level**: Critical / High / Medium / Low
- **Critical Findings**: \[Count\]
- **High Findings**: \[Count\]
- **Medium Findings**: \[Count\]
- **Low Findings**: \[Count\]

### Critical Vulnerabilities

Immediate action required:

```markdown
#### [CRITICAL-001] Vulnerability Title

**Category**: [OWASP Category / CWE-XXX]
**Location**: [File:Line or Component]
**Description**: [Detailed explanation of the vulnerability]
**Exploit Scenario**: [How an attacker could exploit this]
**Evidence**: [Code snippet or configuration showing the issue]

**Remediation**:
1. [Step-by-step fix instructions]
2. [Additional hardening recommendations]

**Secure Code Example**:
[Fixed code snippet]

**References**:
- [Link to security documentation]
- [Link to CWE/CVE details]
```

### High/Medium/Low Findings

Follow same format with appropriate urgency level.

### Remediation Roadmap

Prioritized action plan:

| Priority | Finding      | Effort | Timeline  |
| -------- | ------------ | ------ | --------- |
| 1        | CRITICAL-001 | Low    | Immediate |
| 2        | HIGH-001     | Medium | 1 week    |
| 3        | MEDIUM-001   | High   | 1 month   |

### Security Recommendations

Long-term security improvements:

1. **Implement security automation**

   - SAST/DAST in CI/CD
   - Dependency scanning
   - Secret scanning pre-commit hooks

1. **Enhance monitoring**

   - Security event logging
   - Alerting thresholds
   - Incident response playbooks

1. **Security training**

   - Developer security awareness
   - Secure coding practices
   - Threat modeling workshops

## Guidelines

1. **Prioritize by risk** - Focus on exploitable vulnerabilities first
1. **Provide evidence** - Include specific code/config examples
1. **Be actionable** - Every finding needs a clear remediation path
1. **Consider context** - Evaluate risk based on deployment environment
1. **Verify fixes** - Suggest testing procedures for validating remediations

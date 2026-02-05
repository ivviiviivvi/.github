# Governance Reference Guide

This document consolidates governance best practices for the ivviiviivvi
organization, derived from the system-governance-framework.

## Repository Settings Checklist

### Branch Protection Rules

Navigate to: Settings > Branches > Add branch protection rule

**Required Settings:**

- [x] Require pull request reviews before merging
- [x] Require review from code owners (CODEOWNERS file)
- [x] Require status checks to pass (CI workflow)
- [x] Require branches to be up to date
- [x] Restrict pushes to main branch
- [x] Require linear history (optional, recommended)

### Security Settings

Navigate to: Settings > Security

**Required Settings:**

- [x] Enable Dependabot alerts
- [x] Enable Dependabot security updates
- [x] Enable secret scanning
- [x] Enable code scanning (CodeQL)
- [x] Enable push protection for secrets

### Repository Features

**Enable:**

- [x] Issues
- [x] Discussions (for community questions)
- [x] Projects (for task management)
- [x] Wiki (optional)

______________________________________________________________________

## Quality Gates

### Pre-commit Hooks

Essential hooks for code quality:

| Hook                      | Purpose                        |
| ------------------------- | ------------------------------ |
| `trailing-whitespace`     | Remove trailing whitespace     |
| `end-of-file-fixer`       | Ensure files end with newline  |
| `check-yaml`              | Validate YAML syntax           |
| `check-json`              | Validate JSON syntax           |
| `check-toml`              | Validate TOML syntax           |
| `check-added-large-files` | Prevent large files (>1MB)     |
| `detect-private-key`      | Prevent committing secrets     |
| `check-merge-conflict`    | Detect merge conflicts         |
| `check-case-conflict`     | Cross-platform filename safety |
| `check-symlinks`          | Detect broken symlinks         |
| `mixed-line-ending`       | Consistent LF line endings     |

### CI Workflow Requirements

Every repository should have:

1. **Linting** - Code style validation
1. **Testing** - Unit and integration tests
1. **Security Scanning** - SAST tools (Semgrep, CodeQL)
1. **Dependency Review** - Check for vulnerabilities
1. **Coverage** - Minimum 80% code coverage

______________________________________________________________________

## Security Response Timeline

| Phase            | Timeline        | Actions                              |
| ---------------- | --------------- | ------------------------------------ |
| Initial Response | 5 business days | Acknowledge report, assign owner     |
| Status Updates   | Every 10 days   | Progress update to reporter          |
| Resolution       | 90 days max     | Fix deployed or workaround provided  |
| Disclosure       | After fix       | Coordinated disclosure with reporter |

______________________________________________________________________

## Issue & PR Standards

### Issue Labels (Required)

| Category | Labels                                                                  |
| -------- | ----------------------------------------------------------------------- |
| Type     | `bug`, `enhancement`, `documentation`, `question`                       |
| Priority | `priority/critical`, `priority/high`, `priority/medium`, `priority/low` |
| Status   | `status/in-progress`, `status/blocked`, `status/needs-review`           |
| Size     | `size/xs`, `size/s`, `size/m`, `size/l`, `size/xl`                      |

### PR Requirements

- [ ] Descriptive title (conventional commits format)
- [ ] Links to related issues
- [ ] Description of changes
- [ ] Testing checklist completed
- [ ] No merge conflicts
- [ ] CI checks passing
- [ ] Code owner approval

______________________________________________________________________

## AI Agent Guidelines

For AI-assisted development, use the handoff templates in `.github/templates/`:

- `AI_HANDOFF_HEADER.md` - Document metadata and constraints
- `AI_HANDOFF_FOOTER.md` - Change tracking and validation

### Key Principles

1. **Read First** - Review entire document before modifications
1. **Preserve Intent** - Maintain original purpose and scope
1. **Cross-Reference** - Check related documents for consistency
1. **Document Changes** - Track all modifications
1. **Validate Impact** - Test before committing

______________________________________________________________________

## Community Health Files

### Required Files

| File               | Location        | Purpose                 |
| ------------------ | --------------- | ----------------------- |
| README.md          | Root            | Project overview        |
| CONTRIBUTING.md    | Root or .github | Contribution guidelines |
| CODE_OF_CONDUCT.md | Root or .github | Community standards     |
| SECURITY.md        | .github         | Vulnerability reporting |
| CODEOWNERS         | .github         | Code ownership          |
| LICENSE            | Root            | Legal terms             |

### Optional Files

| File          | Purpose                 |
| ------------- | ----------------------- |
| SUPPORT.md    | Support channels        |
| FUNDING.yml   | Sponsorship options     |
| GOVERNANCE.md | Decision-making process |

______________________________________________________________________

## Metrics & Health

### Repository Health Score

Monitor these metrics:

1. **Response Time** - Time to first response on issues/PRs
1. **Merge Time** - PR open to merge duration
1. **Issue Resolution** - Time to close issues
1. **Test Coverage** - Percentage of code covered
1. **Dependency Freshness** - Age of dependencies

### SLA Targets

| Metric                 | Target                   |
| ---------------------- | ------------------------ |
| Issue response         | \< 48 hours              |
| PR review              | \< 72 hours              |
| Security vulnerability | \< 5 days acknowledgment |
| Stale issue threshold  | 90 days                  |
| Stale PR threshold     | 30 days                  |

______________________________________________________________________

## Related Resources

- [REUSABLE_WORKFLOWS.md](./REUSABLE_WORKFLOWS.md) - Reusable GitHub Actions
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](../SECURITY.md) - Security policy
- [CODEOWNERS](../CODEOWNERS) - Code ownership

______________________________________________________________________

_This document consolidates content from the system-governance-framework
repository._

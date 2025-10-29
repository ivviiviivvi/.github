# Repository Setup Checklist

This checklist ensures all new repositories in the organization are configured with best practices.

## Initial Setup

### Basic Configuration
- [ ] Repository created with descriptive name
- [ ] Repository description added
- [ ] Topics/tags added for discoverability
- [ ] README.md created with project overview
- [ ] LICENSE file added (MIT or organization standard)
- [ ] .gitignore configured for language/framework

### Access Control
- [ ] Repository visibility set (public/private/internal)
- [ ] Teams assigned with appropriate permissions
- [ ] Required teams added as code owners
- [ ] Individual access granted as needed

### Branch Protection
- [ ] Default branch set (main/master)
- [ ] Branch protection rules applied to default branch
- [ ] Require pull request reviews enabled
- [ ] Require status checks enabled
- [ ] Force push disabled
- [ ] Branch deletion disabled

## Community Health Files

### Documentation
- [ ] README.md with project overview, setup, and usage
- [ ] CONTRIBUTING.md (if not inherited from .github)
- [ ] CODE_OF_CONDUCT.md (if not inherited from .github)
- [ ] SECURITY.md with security policy
- [ ] CHANGELOG.md for version history

### Templates
- [ ] Issue templates configured (or inherited)
- [ ] Pull request template configured (or inherited)
- [ ] Discussion templates (if using Discussions)

## CI/CD Configuration

### GitHub Actions
- [ ] .github/workflows directory created
- [ ] CI workflow configured (build, test, lint)
- [ ] Security scanning workflow added
- [ ] Deployment workflow configured (if applicable)
- [ ] Required secrets added to repository

### Status Checks
- [ ] All required workflows added to branch protection
- [ ] Status checks configured to block merge on failure
- [ ] Code coverage reporting configured

## Security

### Dependabot
- [ ] Dependabot enabled for version updates
- [ ] Dependabot enabled for security updates
- [ ] Auto-merge configured for minor/patch updates

### Code Scanning
- [ ] CodeQL analysis enabled
- [ ] Secret scanning enabled
- [ ] Vulnerability alerts enabled
- [ ] Security policy (SECURITY.md) in place

### Secrets Management
- [ ] Repository secrets configured
- [ ] Environment secrets configured (if using environments)
- [ ] No hardcoded secrets in codebase
- [ ] Secret rotation policy documented

## Integrations

### Required Integrations
- [ ] Code quality tools connected (SonarCloud, CodeClimate, etc.)
- [ ] Monitoring/observability tools integrated
- [ ] Issue tracking connected (if external)
- [ ] Communication tools integrated (Slack, Teams, etc.)

### Webhooks
- [ ] Required webhooks configured
- [ ] Webhook secrets stored securely
- [ ] Webhook deliveries monitored

## Project Management

### Issues and Projects
- [ ] Repository added to organization project board
- [ ] Issue labels created/synced
- [ ] Milestones created (if applicable)
- [ ] Saved replies configured (optional)

### Automation
- [ ] Stale bot configured
- [ ] Auto-labeling configured
- [ ] Auto-assignment configured
- [ ] Project board automation enabled

## Documentation

### Code Documentation
- [ ] Inline code comments for complex logic
- [ ] API documentation generated (if applicable)
- [ ] Architecture diagrams created (if applicable)
- [ ] Database schemas documented (if applicable)

### GitHub Pages (if applicable)
- [ ] GitHub Pages enabled
- [ ] Documentation site configured
- [ ] Custom domain configured (if needed)
- [ ] Deployment workflow configured

## Compliance and Governance

### Audit
- [ ] Repository audit log reviewed
- [ ] Compliance requirements documented
- [ ] Data classification applied
- [ ] Retention policy documented

### Code Owners
- [ ] CODEOWNERS file created
- [ ] Teams/individuals assigned as code owners
- [ ] Code owner reviews required in branch protection

## Final Verification

- [ ] All CI/CD workflows passing
- [ ] Security alerts reviewed and addressed
- [ ] Documentation complete and accurate
- [ ] Team members have appropriate access
- [ ] Repository settings reviewed
- [ ] First commit made and PR merged successfully

## Notes

Add any repository-specific notes or exceptions here:

---

**Completed by:** _________________  
**Date:** _________________  
**Reviewed by:** _________________

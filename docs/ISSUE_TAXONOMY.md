# Issue Taxonomy and Classification System

> **Comprehensive classification system for all organizational issues**

This document defines the exhaustive taxonomy for issues across the Ivviiviivvi organization. Use this as a reference when creating, labeling, and organizing issues.

## Table of Contents

- [Primary Categories](#primary-categories)
- [Issue Types](#issue-types)
- [Priority Levels](#priority-levels)
- [Status Workflow](#status-workflow)
- [Special Issue Categories](#special-issue-categories)
- [Cross-Cutting Concerns](#cross-cutting-concerns)

## Primary Categories

### 1. Development Issues

#### 1.1 Feature Development
- **New Features**: Net-new functionality additions
- **Feature Enhancements**: Improvements to existing features
- **Feature Deprecation**: Phasing out old features
- **Feature Requests**: User-submitted feature proposals

#### 1.2 Bug Management
- **Critical Bugs**: System-breaking issues requiring immediate attention
- **High Priority Bugs**: Significant issues affecting core functionality
- **Medium Priority Bugs**: Issues affecting non-critical features
- **Low Priority Bugs**: Minor issues with workarounds
- **Regression Bugs**: Previously working features that broke

#### 1.3 Technical Debt
- **Code Refactoring**: Improving code quality without changing behavior
- **Architecture Improvements**: Structural enhancements
- **Performance Optimization**: Speed and efficiency improvements
- **Dependency Updates**: Library and framework updates
- **Code Cleanup**: Removing deprecated or unused code

### 2. Documentation Issues

#### 2.1 Documentation Types
- **API Documentation**: Endpoint and interface documentation
- **User Documentation**: End-user guides and tutorials
- **Developer Documentation**: Contributing guides and technical docs
- **Architecture Documentation**: System design and ADRs
- **Process Documentation**: Workflow and procedure guides

#### 2.2 Documentation Tasks
- **Documentation Gaps**: Missing documentation identification
- **Documentation Updates**: Keeping docs current with code
- **Documentation Errors**: Fixing inaccuracies
- **Documentation Improvements**: Enhancing clarity and completeness

### 3. Infrastructure & DevOps

#### 3.1 CI/CD Issues
- **Workflow Optimization**: Improving GitHub Actions performance
- **Build Issues**: Compilation and build failures
- **Deployment Issues**: Release and deployment problems
- **Testing Infrastructure**: Test suite improvements

#### 3.2 Infrastructure Management
- **Server Configuration**: Infrastructure setup and changes
- **Monitoring & Observability**: Metrics and logging improvements
- **Security Infrastructure**: Security tooling and hardening
- **Performance Infrastructure**: Caching, CDN, optimization

### 4. Security & Compliance

#### 4.1 Security Issues
- **Vulnerabilities**: Security flaws requiring patches
- **Security Enhancements**: Proactive security improvements
- **Dependency Vulnerabilities**: Third-party security issues
- **Security Audits**: Systematic security reviews

#### 4.2 Compliance Issues
- **License Compliance**: License audit and management
- **Data Privacy**: GDPR, CCPA, and privacy compliance
- **Accessibility**: WCAG and accessibility compliance
- **Regulatory Compliance**: Industry-specific requirements

### 5. Community & Operations

#### 5.1 Community Management
- **Community Health**: Repository health metrics
- **Contributor Experience**: Onboarding and contribution UX
- **Communication**: Announcements and updates
- **Community Events**: Meetups, sprints, discussions

#### 5.2 Operational Issues
- **Repository Administration**: Settings and configuration
- **Team Management**: Access control and permissions
- **Process Improvements**: Workflow and procedure enhancements
- **Automation**: Automating repetitive tasks

### 6. Research & Planning

#### 6.1 Research Issues
- **Technology Research**: Evaluating new tools and frameworks
- **Competitive Analysis**: Studying similar solutions
- **User Research**: Understanding user needs and pain points
- **Performance Research**: Benchmarking and analysis

#### 6.2 Planning Issues
- **Epic Planning**: Large initiative planning
- **Sprint Planning**: Iteration planning
- **Roadmap Planning**: Long-term strategy
- **Resource Planning**: Capacity and allocation

## Issue Types

### By Nature

1. **Task**: Actionable work items with clear completion criteria
2. **Bug**: Defects in existing functionality
3. **Enhancement**: Improvements to existing features
4. **Feature**: New functionality additions
5. **Question**: Requests for information or clarification
6. **Discussion**: Topics requiring team input and consensus
7. **Epic**: Large initiatives spanning multiple issues
8. **Spike**: Time-boxed research or investigation

### By Scope

1. **Single Repository**: Issues affecting one repository
2. **Multi-Repository**: Issues spanning multiple repositories
3. **Organization-Wide**: Issues affecting the entire organization
4. **External**: Issues requiring external coordination

## Priority Levels

### P0 - Critical
- System down or unusable
- Security vulnerabilities actively exploited
- Data loss or corruption
- Legal or compliance violations
- **SLA**: Immediate response, resolution within 4 hours

### P1 - High
- Major functionality broken
- Significant user impact
- Security vulnerabilities discovered
- Blocking other work
- **SLA**: Response within 4 hours, resolution within 24 hours

### P2 - Medium
- Moderate functionality issues
- Some user impact
- Important but not urgent improvements
- **SLA**: Response within 1 business day, resolution within 1 week

### P3 - Low
- Minor issues with workarounds
- Nice-to-have enhancements
- Documentation improvements
- **SLA**: Response within 3 business days, resolution as capacity allows

### P4 - Backlog
- Future considerations
- Ideas and proposals
- Low-impact improvements
- **SLA**: Reviewed quarterly, prioritized as needed

## Status Workflow

### Status Labels

1. **Triage**: New issues awaiting initial review
2. **Backlog**: Accepted issues not yet scheduled
3. **Todo**: Scheduled for upcoming work
4. **In Progress**: Actively being worked on
5. **In Review**: Under code review or testing
6. **Blocked**: Waiting on external dependency
7. **Done**: Completed and closed
8. **Won't Fix**: Decided not to address
9. **Duplicate**: Already addressed in another issue

### Status Transitions

```
Triage → Backlog → Todo → In Progress → In Review → Done
         ↓                     ↓           ↓
    Won't Fix              Blocked    Need Info
         ↓                     ↓           ↓
       Done              In Progress   Triage
```

## Special Issue Categories

### Meta Issues

Issues about the issue tracking system itself:
- Issue template improvements
- Label taxonomy updates
- Workflow process changes
- Automation enhancements

### Tracking Issues

Large initiatives broken down into multiple sub-issues:
- Epic tracking with child issue links
- Milestone tracking across repositories
- Project board coordination
- Release planning aggregation

### Automated Issues

Issues created by automation:
- Dependabot security alerts
- Stale issue notifications
- Health check failures
- Scheduled maintenance tasks

### External Integration Issues

Issues from external systems:
- Sentry error reports
- Customer support tickets
- Security scan results
- Monitoring alerts

## Cross-Cutting Concerns

### Quality Attributes

Issues can have multiple quality attribute labels:
- **Performance**: Speed and efficiency concerns
- **Scalability**: Growth and capacity concerns
- **Reliability**: Stability and availability concerns
- **Security**: Safety and protection concerns
- **Usability**: User experience concerns
- **Maintainability**: Code quality concerns
- **Accessibility**: Universal access concerns

### Affected Components

Tag issues with affected system components:
- Frontend/UI
- Backend/API
- Database
- Infrastructure
- Documentation
- Testing
- Build/Deploy

### Stakeholder Types

Identify who is affected:
- End Users
- Contributors
- Maintainers
- Administrators
- External Partners

## Issue Creation Guidelines

### Required Information

Every issue should include:
1. **Clear Title**: Descriptive and searchable
2. **Description**: What, why, and context
3. **Acceptance Criteria**: Definition of done
4. **Labels**: Proper classification
5. **Assignee**: Responsible party (if known)
6. **Milestone**: Target release (if applicable)
7. **Project**: Board tracking (if applicable)

### Optional Information

Additional helpful details:
- Screenshots/recordings
- Error logs and stack traces
- Reproduction steps
- Environment details
- Related issues/PRs
- External references

### Best Practices

1. **One Issue, One Topic**: Keep issues focused
2. **Search First**: Avoid duplicates
3. **Use Templates**: Leverage issue templates
4. **Link Relationships**: Connect related issues
5. **Update Status**: Keep issues current
6. **Close When Done**: Don't leave stale issues open

## Issue Labels Reference

See [LABELS.md](LABELS.md) for the complete label taxonomy and usage guidelines.

## Automation and Integration

### Automated Workflows

- **Triage Bot**: Auto-labels based on content
- **Stale Issue Management**: Closes inactive issues
- **Dependency Updates**: Creates update issues
- **Security Alerts**: Creates vulnerability issues
- **Health Checks**: Creates monitoring issues

### Project Integration

Issues automatically sync with:
- GitHub Projects (v2)
- Milestones and releases
- Pull requests
- Discussions
- Wiki documentation

## Metrics and Reporting

### Key Metrics

Track these issue metrics:
- Time to triage
- Time to resolution
- Issue backlog size
- Issue velocity
- Bug escape rate
- Reopened issue rate

### Regular Reviews

- **Daily**: P0/P1 issues
- **Weekly**: P2 issues and new triage
- **Monthly**: Backlog grooming
- **Quarterly**: Taxonomy and process review

## References

- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [Project Planning Guide](PROJECT_PLANNING.md)
- [Label Standards](LABELS.md)
- [Contributing Guidelines](CONTRIBUTING.md)

---

**Last Updated**: 2025-12-28  
**Maintained By**: @ivviiviivvi organization maintainers

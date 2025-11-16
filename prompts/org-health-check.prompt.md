---
mode: 'agent'
description: 'Performs a comprehensive health check of the organization, repositories, workflows, and security posture'
model: 'gpt-4o'
tools: ['github']
---

You are performing a comprehensive health check for the ivi374forivi GitHub organization.

## Health Check Areas

### 1. Repository Health
For each repository, assess:
- **Activity**: Recent commits, issues, PRs
- **Maintenance**: Stale issues/PRs, outdated dependencies
- **Documentation**: README quality, missing docs
- **Configuration**: Branch protection, required checks
- **Community**: Issue templates, PR templates, CONTRIBUTING.md

### 2. Security Posture
Evaluate:
- **Dependabot**: Enabled and configured
- **CodeQL**: Analysis workflows present
- **Secrets**: Secret scanning enabled (if available)
- **Vulnerabilities**: Open security alerts
- **Access**: Team permissions and access levels
- **Policies**: SECURITY.md presence and quality

### 3. CI/CD Health
Review:
- **Workflows**: Active and functional
- **Success Rate**: Percentage of successful runs
- **Performance**: Average execution time
- **Coverage**: Test coverage metrics
- **Deployments**: Deployment frequency and success rate

### 4. Community Engagement
Analyze:
- **Contributors**: Number and diversity
- **Issues**: Open vs closed ratio, response time
- **Pull Requests**: Merge rate, review time
- **Discussions**: Activity level (if enabled)
- **Documentation**: Quality and completeness

### 5. Compliance
Check adherence to:
- **AI GitHub Management Protocol**: 8 modules implementation
- **Organization Standards**: Templates, labels, workflows
- **Best Practices**: Security, testing, documentation
- **Licensing**: Proper license files
- **Code of Conduct**: Present and enforced

## Report Format

Generate a report with:

### Executive Summary
- Overall health score (0-100)
- Critical issues requiring immediate attention
- Key recommendations
- Trends (improving/declining)

### Repository-Level Findings
For each repository:
- Health score
- Active issues and PRs
- Security alerts
- Missing configurations
- Recommendations

### Organization-Level Findings
- Access control audit
- Team structure review
- Policy compliance
- Integration health
- Resource utilization

### Action Items
Prioritized list of:
- Critical fixes (do immediately)
- High priority improvements (do this week)
- Medium priority enhancements (do this month)
- Low priority optimizations (backlog)

### Metrics Dashboard
Key metrics:
- Total repositories
- Active vs archived
- Average health score
- Open security alerts
- Stale issues/PRs
- Workflow success rate
- Average PR review time
- Contributor count

## Implementation

1. **Gather Data**: Use GitHub API to collect metrics
2. **Analyze**: Compare against best practices and organization standards
3. **Score**: Calculate health scores for each area
4. **Report**: Generate comprehensive report with visualizations
5. **Recommend**: Provide actionable recommendations with priorities

## Usage

This prompt should be run:
- Monthly for routine health checks
- Before major organizational changes
- After onboarding new repositories
- When investigating performance issues
- For compliance audits

## Output

Provide:
1. Markdown report with all findings
2. Summary statistics
3. Prioritized action items
4. Trend analysis (if historical data available)
5. Comparison against industry benchmarks (if applicable)

# Team Structure

This document outlines the recommended team structure, responsibilities, and access management for the organization.

## Overview

A well-defined team structure ensures proper access control, efficient code review, and clear ownership of different parts of the codebase. This document describes the recommended team hierarchy and how to manage it.

## Recommended Team Hierarchy

### Leadership Team (@ivviiviivvi/leadership)

**Purpose**: Executive oversight and strategic decisions

**Responsibilities**:
- Final approval on major changes
- Strategic direction and roadmap
- Policy and governance decisions
- Community guidelines and enforcement
- Budget and resource allocation

**Members**:
- Organization owners
- Project leads
- Product managers

**Repository Access**: Admin on all repositories

**CODEOWNERS Patterns**:
```
* @ivviiviivvi/leadership
*.md @ivviiviivvi/leadership
/docs/ @ivviiviivvi/leadership
```

---

### Engineering Team (@ivviiviivvi/engineering)

**Purpose**: Code development and technical implementation

**Responsibilities**:
- Writing and reviewing code
- Technical architecture decisions
- Code quality and best practices
- Bug fixes and feature implementation
- Technical documentation

**Members**:
- Software engineers
- Senior developers
- Technical leads

**Repository Access**: Write on engineering repositories

**CODEOWNERS Patterns**:
```
/src/ @ivviiviivvi/engineering
*.py @ivviiviivvi/engineering
*.js @ivviiviivvi/engineering
*.ts @ivviiviivvi/engineering
*.java @ivviiviivvi/engineering
*.go @ivviiviivvi/engineering
/docs/ @ivviiviivvi/engineering
```

---

### DevOps Team (@ivviiviivvi/devops)

**Purpose**: Infrastructure, CI/CD, and deployment automation

**Responsibilities**:
- GitHub Actions workflows
- Infrastructure as code
- CI/CD pipeline management
- Deployment automation
- Monitoring and alerting
- Container orchestration
- Cloud infrastructure

**Members**:
- DevOps engineers
- Site reliability engineers
- Platform engineers

**Repository Access**: Write on infrastructure repositories, Admin on workflow configurations

**CODEOWNERS Patterns**:
```
/.github/workflows/ @ivviiviivvi/devops
/infrastructure/ @ivviiviivvi/devops
*.yml @ivviiviivvi/devops
*.yaml @ivviiviivvi/devops
Dockerfile @ivviiviivvi/devops
docker-compose.yml @ivviiviivvi/devops
.dockerignore @ivviiviivvi/devops
```

---

### Security Team (@ivviiviivvi/security)

**Purpose**: Security oversight and vulnerability management

**Responsibilities**:
- Security policy enforcement
- Vulnerability assessment and remediation
- Security code reviews
- Dependency security monitoring
- Incident response
- Security training and awareness

**Members**:
- Security engineers
- Security analysts
- Compliance specialists

**Repository Access**: Write on all repositories (for security patches), Admin on security policies

**CODEOWNERS Patterns**:
```
/SECURITY.md @ivviiviivvi/security
/.github/SECURITY.md @ivviiviivvi/security
/.github/workflows/codeql*.yml @ivviiviivvi/security
/.github/workflows/security-*.yml @ivviiviivvi/security
/.github/workflows/scan-*.yml @ivviiviivvi/security
```

---

### QA Team (@ivviiviivvi/qa) [Optional]

**Purpose**: Quality assurance and testing

**Responsibilities**:
- Test planning and execution
- Test automation
- Quality metrics tracking
- Bug validation
- Performance testing

**Members**:
- QA engineers
- Test automation engineers
- Performance testers

**Repository Access**: Read on all repositories, Write on test repositories

**CODEOWNERS Patterns**:
```
/tests/ @ivviiviivvi/qa
/e2e/ @ivviiviivvi/qa
*test*.py @ivviiviivvi/qa
```

---

### Frontend Team (@ivviiviivvi/frontend) [Optional]

**Purpose**: Frontend development and UI/UX implementation

**Responsibilities**:
- Frontend code development
- UI component library
- User interface implementation
- Frontend performance
- Accessibility

**Members**:
- Frontend developers
- UI engineers

**Repository Access**: Write on frontend repositories

**CODEOWNERS Patterns**:
```
/frontend/ @ivviiviivvi/frontend
/ui/ @ivviiviivvi/frontend
*.tsx @ivviiviivvi/frontend
*.jsx @ivviiviivvi/frontend
*.css @ivviiviivvi/frontend
*.scss @ivviiviivvi/frontend
```

---

### Backend Team (@ivviiviivvi/backend) [Optional]

**Purpose**: Backend development and API implementation

**Responsibilities**:
- Backend code development
- API design and implementation
- Database schema design
- Business logic implementation
- Backend performance

**Members**:
- Backend developers
- API engineers

**Repository Access**: Write on backend repositories

**CODEOWNERS Patterns**:
```
/backend/ @ivviiviivvi/backend
/api/ @ivviiviivvi/backend
/services/ @ivviiviivvi/backend
```

---

## Permission Levels

### Read
- View code and discussions
- Clone repositories
- Create issues
- Comment on issues and PRs

### Triage
- Read access plus:
- Manage issues and PRs
- Apply labels
- Assign issues

### Write
- Triage access plus:
- Push to branches
- Create pull requests
- Merge PRs (if not protected)

### Maintain
- Write access plus:
- Manage repository settings
- Manage webhooks
- Manage releases

### Admin
- Full access including:
- Delete repository
- Manage teams and permissions
- Manage branch protections
- Manage security settings

## Creating Teams

### Via GitHub Web Interface

1. Go to **Organization Settings** → **Teams**
2. Click **New team**
3. Enter team name (e.g., `engineering`)
4. Set team description
5. Choose parent team (if applicable)
6. Set team visibility (Visible or Secret)
7. Click **Create team**

### Via GitHub CLI

```bash
# Create a team (replace {org} with your organization name)
gh api orgs/{org}/teams \
  -f name="engineering" \
  -f description="Engineering team responsible for code development" \
  -f privacy="closed"

# Add member to team (replace {org} and {username})
gh api orgs/{org}/teams/engineering/memberships/{username} \
  -X PUT \
  -f role="member"
```

**Note**: Replace `{org}` with your organization name and `{username}` with the GitHub username.

### Via Terraform

```hcl
resource "github_team" "engineering" {
  name        = "engineering"
  description = "Engineering team"
  privacy     = "closed"
}

resource "github_team_membership" "engineering_member" {
  team_id  = github_team.engineering.id
  username = "username"
  role     = "member"
}
```

## Assigning Teams to Repositories

### Via GitHub Web Interface

1. Go to **Repository Settings** → **Collaborators and teams**
2. Click **Add teams**
3. Select team
4. Choose permission level
5. Click **Add {team} to this repository**

### Via GitHub CLI

```bash
# Add team to repository with write access
# Replace {owner} with organization/user name and {repo} with repository name
gh api repos/{owner}/{repo}/teams/engineering \
  -X PUT \
  -f permission="push"
```

**Note**: Replace `{owner}` and `{repo}` with your actual organization and repository names.

## Review Assignment

### Round Robin Assignment

Configure automatic reviewer assignment based on team membership:

1. Go to **Repository Settings** → **Code review assignment**
2. Enable **Auto assignment**
3. Choose **Round robin** or **Load balance**
4. Select teams for assignment
5. Set number of reviewers

### Via .github/auto_assign.yml

```yaml
# .github/auto_assign.yml
reviewers:
  - engineering
  - devops

numberOfReviewers: 2
```

## Team Synchronization

For organizations using external identity providers (e.g., Azure AD, Okta):

1. Go to **Organization Settings** → **Teams**
2. Select team
3. Click **Settings**
4. Configure **Identity Provider Groups**
5. Map external groups to GitHub teams

## Access Request Process

### For Team Members

1. **Identify Required Access**
   - Determine which team you need to join
   - Understand the access level needed

2. **Submit Request**
   - Open an issue using the appropriate template
   - Tag team lead or organization admin
   - Provide justification for access

3. **Wait for Approval**
   - Team lead reviews request
   - Access granted if approved
   - You'll receive notification via GitHub

### For Team Leads

1. **Review Access Requests**
   - Verify requestor's identity
   - Confirm access is appropriate
   - Check with other team leads if needed

2. **Grant or Deny Access**
   - Add member to team if approved
   - Document reason for denial if rejected
   - Notify requestor of decision

3. **Set Appropriate Permissions**
   - Assign correct permission level
   - Add to specific repositories if needed
   - Review access periodically

## Access Reviews

### Quarterly Access Review

Every quarter, team leads should:

1. Review current team membership
2. Verify all members still require access
3. Remove inactive or departed members
4. Update permission levels as needed
5. Document changes in audit log

### Automated Review Reminders

Set up GitHub Actions workflow to remind team leads:

```yaml
# .github/workflows/access-review.yml
name: Quarterly Access Review Reminder

on:
  schedule:
    - cron: '0 0 1 */3 *'  # First day of every quarter

jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - name: Create access review issue
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Quarterly Access Review - Q' + Math.ceil((new Date().getMonth() + 1) / 3),
              body: '## Quarterly Access Review\n\nPlease review team memberships and permissions.',
              labels: ['access-review', 'security']
            });
```

## Best Practices

### Team Management

1. **Clear Responsibilities**: Define clear roles and responsibilities for each team
2. **Least Privilege**: Grant minimum necessary access
3. **Regular Reviews**: Audit team membership quarterly
4. **Documentation**: Keep team documentation up to date
5. **Offboarding**: Remove access immediately when members leave

### CODEOWNERS

1. **Specific Patterns**: Use specific patterns for better coverage
2. **Multiple Owners**: Assign backup owners for critical paths
3. **Team-Based**: Use teams rather than individuals
4. **Regular Updates**: Review CODEOWNERS file regularly
5. **Test Coverage**: Ensure all important paths have owners

### Review Process

1. **Balanced Workload**: Distribute reviews evenly across team
2. **Expertise Matching**: Assign reviewers based on expertise
3. **Response Time**: Set SLAs for code reviews
4. **Multiple Reviewers**: Require multiple reviewers for critical changes
5. **Continuous Improvement**: Gather feedback on review process

## Troubleshooting

### Issue: Team members can't push to repository

**Solution**:
- Verify team has Write permission on repository
- Check branch protection rules
- Ensure member is in correct team

### Issue: CODEOWNERS not working

**Solution**:
- Verify file is in repository root or .github/
- Check file syntax
- Ensure teams exist and members are added
- Enable "Require review from code owners" in branch protection

### Issue: Too many review requests

**Solution**:
- Adjust number of required reviewers
- Use load balancing for review assignment
- Split responsibilities across more teams
- Configure review assignment algorithms

## Resources

- [GitHub Docs - Teams](https://docs.github.com/en/organizations/organizing-members-into-teams)
- [GitHub Docs - CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Docs - Repository Permission Levels](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/repository-roles-for-an-organization)

---

**Last Updated**: 2024-12-31

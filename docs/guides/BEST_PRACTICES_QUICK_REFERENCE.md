# Quick Reference: Using GitHub Best Practices Sessions

## Overview

This repository includes comprehensive templates and guides for GitHub best
practices:

- **Discussion Templates** - For community engagement
- **Enhanced Issue Templates** - For structured requests
- **Best Practices Sessions Guide** - For running effective sessions

## Quick Links

- 📖 [Complete Sessions Guide](./GITHUB_BEST_PRACTICES_SESSIONS.md)
- 📚 [Best Practices Overview](./BEST_PRACTICES.md)
- 💬 [Discussion Templates](../../.github/DISCUSSION_TEMPLATE/)
- 🎫 [Issue Templates](../../.github/ISSUE_TEMPLATE/)

---

## Discussion Templates

Located in `.github/DISCUSSION_TEMPLATE/`, these templates structure community
discussions:

### 1. General Q&A (`general-qa.yml`)

**Use for**: Asking questions and getting answers from the community

**Example Topics**:

- "How do I optimize my GitHub Actions cache?"
- "What's the best way to structure a monorepo?"
- "How can I improve PR review turnaround time?"

### 2. Ideas & Feature Proposals (`ideas.yml`)

**Use for**: Sharing ideas for new features or improvements

**Example Topics**:

- "Add automated dependency vulnerability reporting"
- "Create reusable workflow for container scanning"
- "Implement automated changelog generation"

### 3. Show and Tell (`show-and-tell.yml`)

**Use for**: Showcasing projects, implementations, or findings

**Example Topics**:

- "Our journey to 100% test coverage"
- "Custom GitHub Action for database migrations"
- "How we reduced CI time by 60%"

### 4. Best Practices (`best-practices.yml`)

**Use for**: Discussing and improving development practices

**Example Topics**:

- "Should we enforce conventional commits?"
- "Best practices for secret management"
- "Code review guidelines and standards"

### 5. Help Wanted (`help-wanted.yml`)

**Use for**: Requesting or offering help

**Example Topics**:

- "Need help debugging GitHub Actions workflow"
- "Looking for collaborators on security audit"
- "Offering to help teams set up CodeQL"

---

## Enhanced Issue Templates

Located in `.github/ISSUE_TEMPLATE/`, these templates facilitate structured
requests:

### Best Practices Review (`best-practices-review.yml`)

**Use for**: Requesting a comprehensive repository review

**When to use**:

- Quarterly health checks
- Before major releases
- After security incidents
- For new repositories
- When preparing for compliance audits

**What it covers**:

- Security & compliance
- Code quality
- Documentation
- Community health
- CI/CD automation

### Community Health Check (`community-health-check.yml`)

**Use for**: Evaluating community health files and practices

**When to use**:

- Preparing to open source a project
- Low contributor engagement
- After community feedback
- Regular quarterly reviews
- When standards change

**What it covers**:

- Community health files (README, CONTRIBUTING, etc.)
- Issue and PR templates
- Discussion setup
- Contributor guidelines
- Inclusivity and accessibility

---

## Running Best Practices Sessions

### Quick Start (30-minute Knowledge Share)

**Week 1: Plan**

```bash
# 1. Choose a topic
Topic: "GitHub Actions Caching Best Practices"

# 2. Set objectives
- Understand when to use caching
- Learn cache configuration options
- See practical examples

# 3. Schedule session
Duration: 30 minutes
Attendees: Development teams
```

**Week 2: Prepare**

```bash
# 1. Create simple presentation
- 10 slides with key concepts
- 2-3 live demo examples
- Links to documentation

# 2. Test your demo
- Create test repository
- Run through examples
- Time yourself

# 3. Send invite
Subject: "Knowledge Share: GitHub Actions Caching"
Include: Agenda, pre-reading (optional), meeting link
```

**Week 3: Execute**

```markdown
## Session Agenda

1. Welcome & Intro (3 min)
2. Caching Overview (7 min)
   - What is caching?
   - When to use it
   - Key benefits
3. Live Demo (15 min)
   - Basic cache setup
   - Cache keys and paths
   - Common patterns
4. Q&A & Discussion (5 min)
```

**Week 4: Follow-up**

```markdown
## Session Summary

**Topic**: GitHub Actions Caching
**Date**: 2024-12-25
**Attendees**: 12 developers

### Key Takeaways

- Caching can reduce build times by 40-60%
- Use cache keys based on dependency files
- Set appropriate cache expiration

### Action Items

- [ ] Add caching to top 5 workflows - @team-lead
- [ ] Document caching patterns - @dev1
- [ ] Create reusable cache action - @dev2

### Resources

- [Actions Cache Docs](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Example Repository](https://github.com/org/cache-examples)
```

### Session Templates by Goal

#### Goal: Educate Team on New Feature

**Session Type**: Knowledge Share (30-60 min) **Template**:
[Knowledge Share Template](./GITHUB_BEST_PRACTICES_SESSIONS.md#template-1-knowledge-share-session)

#### Goal: Improve Repository Health

**Session Type**: Repository Health Review (60-90 min) **Template**:
[Repository Review Template](./GITHUB_BEST_PRACTICES_SESSIONS.md#template-2-repository-health-review)

#### Goal: Optimize CI/CD Performance

**Session Type**: Workflow Optimization Workshop (2-4 hours) **Template**:
[Workshop Template](./GITHUB_BEST_PRACTICES_SESSIONS.md#template-3-workflow-optimization-workshop)

#### Goal: Train New Team Members

**Session Type**: Onboarding & Training (60-120 min) **Template**:
[Training Template](./GITHUB_BEST_PRACTICES_SESSIONS.md#5-onboarding--training-sessions-60-120-minutes)

---

## Real-World Examples

### Example 1: Security Audit Session

**Situation**: Recent security vulnerability found in dependency

**Actions Taken**:

1. Scheduled Security & Compliance Session (90 min)
1. Reviewed all repositories for similar issues
1. Implemented automated dependency scanning
1. Created security response playbook
1. Trained team on security practices

**Results**:

- 100% repository coverage with security scanning
- 24-hour average response time to security alerts
- Zero critical vulnerabilities in production

### Example 2: Workflow Optimization Workshop

**Situation**: CI/CD pipelines taking 45+ minutes, high costs

**Actions Taken**:

1. Ran Workflow Optimization Workshop (3 hours)
1. Analyzed current workflows and bottlenecks
1. Implemented caching and parallelization
1. Optimized test strategies
1. Set up monitoring and alerts

**Results**:

- Reduced average build time to 15 minutes (67% improvement)
- Cut CI/CD costs by 55%
- Improved developer experience and velocity
- Documented optimization patterns for other teams

### Example 3: Community Health Initiative

**Situation**: Low external contributions, unclear contribution process

**Actions Taken**:

1. Created Community Health Check issue
1. Reviewed all community health files
1. Updated templates and documentation
1. Ran onboarding sessions for contributors
1. Set up welcoming automation

**Results**:

- 200% increase in external contributions
- Improved contributor retention
- Clearer contribution pathways
- More inclusive and welcoming environment

---

## Tips for Success

### DO's ✅

- **Start Small**: Begin with 30-minute knowledge shares
- **Be Practical**: Use real examples from your projects
- **Encourage Participation**: Make it interactive
- **Follow Up**: Track action items and measure impact
- **Iterate**: Improve based on feedback

### DON'Ts ❌

- **Don't Lecture**: Keep it conversational
- **Don't Skip Prep**: Preparation shows respect for attendees' time
- **Don't Ignore Feedback**: Use it to improve
- **Don't Overcomplicate**: Simple and actionable is better
- **Don't Forget Action Items**: Sessions without actions waste time

---

## Common Questions

### Q: How often should we run sessions?

**A**: Start with monthly knowledge shares, quarterly reviews. Adjust based on
team size and needs.

### Q: Who should facilitate sessions?

**A**: Anyone with relevant expertise. Rotate facilitation to build skills
across the team.

### Q: What if nobody attends?

**A**: Start small with your immediate team. Build value and word will spread.
Make attendance optional but valuable.

### Q: How do we measure success?

**A**: Track attendance, action item completion, measurable improvements (build
times, security scores, contributor satisfaction).

### Q: Can we customize the templates?

**A**: Absolutely! These templates are starting points. Adapt them to your
organization's needs.

### Q: What if we don't have time for workshops?

**A**: Start with 30-minute sessions during lunch or coffee breaks. Small,
consistent sessions beat rare large workshops.

---

## Getting Help

Need assistance?

- 💬
  [Start a Discussion](https://github.com/ivi374forivi/.github/discussions)<!-- link:github.legacy_discussions -->
  using our discussion templates
- 🎫 [Open an Issue](https://github.com/ivi374forivi/.github/issues/new/choose)
  for template improvements
- 📖 Review the [Complete Sessions Guide](./GITHUB_BEST_PRACTICES_SESSIONS.md)
- 📚 Check the [Best Practices Guide](./BEST_PRACTICES.md)

---

## Contributing

Found these templates helpful? Have improvements to suggest?

- Share your session experiences in
  [Show and Tell discussions](https://github.com/ivi374forivi/.github/discussions)<!-- link:github.legacy_discussions -->
- Propose new templates or improvements
- Document your use cases and lessons learned
- Help others by answering questions

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

**Last Updated**: 2024-12-25 **Version**: 1.0

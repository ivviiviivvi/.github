# Contributor Workflow Guide

> **Step-by-step guide for contributors on how to participate in this project**

## Table of Contents

- [Quick Start](#quick-start)
- [Before You Start](#before-you-start)
- [Contribution Process](#contribution-process)
- [Workflow Stages](#workflow-stages)
- [Best Practices](#best-practices)
- [Getting Help](#getting-help)

______________________________________________________________________

## Quick Start

### 5-Minute Contribution Path

```
1. Check Discussions for ideas → 2 minutes
2. Find or create an issue → 1 minute
3. Comment to claim it → 30 seconds
4. Fork and create branch → 1 minute
5. Make changes → (your work)
6. Open PR with template → 30 seconds
```

### First-Time Contributors

**Welcome!** 👋 Here's your fastest path to contributing:

1. Look for issues labeled
   [`good-first-issue`](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3A%22good-first-issue%22)
1. Comment "I'd like to work on this"
1. Wait for assignment (usually within 24 hours)
1. Follow the
   [development setup guide](../guides/DEVELOPMENT_ENVIRONMENT_SETUP.md)
1. Make your changes
1. Open a pull request

______________________________________________________________________

## Before You Start

### Required Reading

- [ ] [Code of Conduct](../governance/CODE_OF_CONDUCT.md) - Our community
  standards
- [ ] [Contributing Guidelines](../governance/CONTRIBUTING.md) - Detailed
  contribution rules
- [ ] [Development Setup](../guides/DEVELOPMENT_ENVIRONMENT_SETUP.md) -
  Environment configuration

### Recommended Reading

- [ ] [Workflow Design](WORKFLOW_DESIGN.md) - How our process works
- [ ] [Labels Guide](../reference/LABELS.md) - Understanding issue/PR labels
- [ ] [GitHub Best Practices Sessions](../guides/GITHUB_BEST_PRACTICES_SESSIONS.md)

### Prerequisites

- **GitHub Account**: With 2FA enabled (security requirement)
- **Git Installed**: Version 2.30 or higher
- **Development Environment**: Appropriate for your contribution type
- **Communication**: Ability to respond to feedback within reasonable time

______________________________________________________________________

## Contribution Process

### Phase 1: Idea Exploration (Optional)

**When to use**: You have an idea but aren't sure if it fits

**Steps**:

1. **Search existing discussions**

   - Check if your idea is already discussed
   - Look for similar or duplicate topics
   - Review closed discussions for context

1. **Create a discussion** (if needed)

   - Go to
     [Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions)
   - Choose appropriate category:
     - **Ideas**: New features or enhancements
     - **Q&A**: Questions about the project
     - **General**: Other topics
   - Use a clear, descriptive title
   - Provide context and rationale

1. **Gather feedback**

   - Engage with community responses
   - Refine your idea based on input
   - Work toward consensus

1. **Convert to issue** (if approved)

   - Maintainer will convert discussion to issue
   - Or you can create one with discussion reference
   - Issue will be labeled and prioritized

**Typical Timeline**: 3-7 days for feedback

### Phase 2: Issue Selection

**When to use**: Ready to start coding

**Steps**:

1. **Browse available issues**

   - [All open issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)
   - [Good first issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3A%22good-first-issue%22)
   - [Help wanted](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3A%22help-wanted%22)
   - [Backlog items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3A%22status%3A+backlog%22)

1. **Read the issue carefully**

   - Understand the requirements
   - Check for linked discussions or related issues
   - Review any acceptance criteria
   - Note priority and type labels

1. **Claim the issue**

   - Comment: "I'd like to work on this issue"
   - Explain your approach (if complex)
   - Ask clarifying questions if needed
   - Wait for assignment (don't start work yet)

1. **Get assigned**

   - Maintainer will assign you
   - Issue labeled `status: in-progress`
   - You'll receive a notification

**Typical Timeline**: Assignment within 24-48 hours

### Phase 3: Development

**When to use**: Issue is assigned to you

**Steps**:

1. **Fork the repository**

   ```bash
   # Click "Fork" button on GitHub
   # Clone your fork
   git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
   cd REPO-NAME

   # Add upstream remote
   git remote add upstream https://github.com/{{ORG_NAME}}/REPO-NAME.git
   ```

1. **Create a feature branch**

   ```bash
   # Update main branch
   git checkout main
   git pull upstream main

   # Create feature branch
   git checkout -b feature/issue-123-description
   # Or: fix/issue-123-description
   # Or: docs/issue-123-description
   ```

1. **Make your changes**

   - Follow coding standards (see instructions)
   - Write/update tests
   - Add/update documentation
   - Commit frequently with clear messages

1. **Commit with conventional format**

   ```bash
   git commit -m "feat: add new feature for issue #123"
   # Or: fix:, docs:, test:, refactor:, style:, chore:
   ```

1. **Keep branch updated**

   ```bash
   # Regularly sync with upstream
   git fetch upstream
   git rebase upstream/main
   ```

**Typical Timeline**: Varies by issue complexity

### Phase 4: Pull Request

**When to use**: Changes are ready for review

**Steps**:

1. **Push to your fork**

   ```bash
   git push origin feature/issue-123-description
   ```

1. **Create pull request**

   - Go to GitHub and click "Compare & pull request"
   - Use clear, descriptive title
   - Format: `feat: add authentication system (fixes #123)`
   - Fill out PR template completely
   - Link related issue: `Closes #123`

1. **PR checklist** (from template)

   - [ ] Code follows project style
   - [ ] Self-reviewed code
   - [ ] Added/updated tests
   - [ ] Tests pass locally
   - [ ] Updated documentation
   - [ ] No security issues
   - [ ] Pre-commit hooks pass

1. **Submit as draft** (optional)

   - If work-in-progress
   - Mark as "Ready for review" when done
   - Draft PRs run basic checks only

1. **Respond to automation**

   - Auto-labeling will add labels
   - Reviewers will be auto-assigned
   - CI checks will run automatically

**Typical Timeline**: Reviews within 24-48 hours

### Phase 5: Review Process

**When to use**: PR is open and under review

**Steps**:

1. **Wait for automated checks**

   - CI/CD pipeline runs
   - Security scans execute
   - Code coverage calculated
   - All must pass before merge

1. **Address failing checks**

   - Fix any CI failures
   - Resolve linting issues
   - Fix failing tests
   - Address security findings

1. **Respond to review comments**

   - Check notifications regularly
   - Answer questions promptly
   - Make requested changes
   - Mark conversations as resolved
   - Push new commits to same branch

1. **Request re-review** (if needed)

   - After making substantial changes
   - Click "Request review" button
   - Notify reviewers in comment

1. **Approval received**

   - At least 1 approval required
   - Must be from CODEOWNERS
   - All checks must pass
   - Auto-merge may be enabled

**Typical Timeline**: 1-3 review iterations

### Phase 6: Merge & Completion

**When to use**: PR is approved and checks pass

**Steps**:

1. **Final checks**

   - Ensure branch is up-to-date
   - All conversations resolved
   - All CI checks green
   - Required approvals received

1. **Merge**

   - Maintainer or auto-merge will merge
   - Branch deleted automatically
   - Linked issues auto-closed

1. **Celebrate!** 🎉

   - Your contribution is live
   - Thank you for contributing!
   - You'll be credited in release notes

1. **After merge**

   - Delete your local branch

   ```bash
   git checkout main
   git branch -d feature/issue-123-description
   git pull upstream main
   ```

**Typical Timeline**: Merge within hours of approval

______________________________________________________________________

## Workflow Stages

### Status Labels Explained

| Label                 | Meaning                    | Your Action                |
| --------------------- | -------------------------- | -------------------------- |
| `needs-triage`        | Awaiting maintainer review | Wait for triage            |
| `status: backlog`     | Ready to be picked up      | Comment to claim           |
| `status: in-progress` | Someone is working on it   | Wait or help if offered    |
| `status: in-review`   | PR under review            | Respond to feedback        |
| `status: blocked`     | Waiting on something       | Check comments for blocker |
| `status: done`        | Completed and merged       | Celebrate!                 |

### Priority Labels Explained

| Label                | Meaning                   | Timeline |
| -------------------- | ------------------------- | -------- |
| `priority: critical` | Urgent, breaking issues   | ASAP     |
| `priority: high`     | Important, should be next | Days     |
| `priority: medium`   | Normal priority           | Weeks    |
| `priority: low`      | Nice to have              | Months   |

______________________________________________________________________

## Best Practices

### Communication

✅ **Do**:

- Be respectful and professional
- Ask questions early if unclear
- Provide regular updates on progress
- Respond to feedback within 48 hours
- Use clear, concise language

❌ **Don't**:

- Start work before being assigned
- Go silent for extended periods
- Ignore review feedback
- Make scope creep changes
- Take on multiple issues simultaneously (at first)

### Code Quality

✅ **Do**:

- Follow existing code style
- Write tests for new features
- Update documentation
- Use meaningful commit messages
- Keep PRs focused and small

❌ **Don't**:

- Submit untested code
- Mix multiple changes in one PR
- Ignore linting errors
- Leave debugging code
- Skip documentation updates

### Issue Management

✅ **Do**:

- Read issues completely
- Ask clarifying questions
- Report blockers immediately
- Update if you can't continue
- Reference related issues/PRs

❌ **Don't**:

- Assume requirements
- Work on issues assigned to others
- Let issues sit idle
- Ignore maintainer feedback
- Close issues without resolution

### Pull Requests

✅ **Do**:

- Fill out template completely
- Link to related issue
- Include tests and docs
- Respond to all review comments
- Keep PR description updated

❌ **Don't**:

- Submit incomplete work
- Force push after reviews
- Ignore CI failures
- Make unrelated changes
- Merge without approval

______________________________________________________________________

## Getting Help

### When Stuck

1. **Check documentation first**

   - README
   - Contributing guide
   - Development setup
   - Existing code/tests

1. **Search for similar issues/PRs**

   - May have been solved before
   - Learn from others' approaches

1. **Ask in the issue**

   - Comment with your question
   - Explain what you've tried
   - Include relevant details

1. **Join discussions**

   - [Q&A Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions/categories/q-a)
   - General community help

1. **Contact maintainers**

   - As a last resort
   - For urgent/sensitive matters
   - Via issue mention: @{{ORG_NAME}}/maintainers

### Common Issues

#### "I don't know where to start"

→ Look for `good-first-issue` labels

#### "Issue is too complex"

→ Ask maintainer to break it down or try a simpler one

#### "CI keeps failing"

→ Check logs, run checks locally, ask for help

#### "No response to my PR"

→ Ping maintainers after 72 hours

#### "I made a mistake"

→ It's OK! Everyone does. Ask how to fix it

______________________________________________________________________

## Quick Reference

### Useful Commands

```bash
# Fork workflow
git clone https://github.com/YOUR-USERNAME/REPO.git
git remote add upstream https://github.com/{{ORG_NAME}}/REPO.git

# Update branch
git fetch upstream
git rebase upstream/main

# Commit format
git commit -m "type: description (fixes #123)"

# Force push after rebase
git push --force-with-lease origin branch-name
```

### Helpful Links

- [Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)
- [Pull Requests](https://github.com/%7B%7BORG_NAME%7D%7D/.github/pulls)
- [Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions)
- [Code of Conduct](../governance/CODE_OF_CONDUCT.md)
- [Contributing Guide](../governance/CONTRIBUTING.md)
- [Development Setup](../guides/DEVELOPMENT_ENVIRONMENT_SETUP.md)

______________________________________________________________________

**Thank you for contributing!** 🙏

Your contributions make this project better for everyone.

______________________________________________________________________

_Last Updated: January 15, 2026_

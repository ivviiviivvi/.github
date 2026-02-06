# Maintainer Workflow Guide

> **Comprehensive guide for maintainers managing discussions, issues, and pull
> requests**

## Table of Contents

- [Overview](#overview)
- [Daily Responsibilities](#daily-responsibilities)
- [Discussion Management](#discussion-management)
- [Issue Management](#issue-management)
- [Pull Request Management](#pull-request-management)
- [Automation Tools](#automation-tools)
- [Best Practices](#best-practices)
- [Escalation Procedures](#escalation-procedures)

______________________________________________________________________

## Overview

As a maintainer, you're responsible for:

- **Guiding contributors** through the contribution process
- **Maintaining quality** through reviews and standards enforcement
- **Managing workflow** from idea to deployment
- **Fostering community** through engagement and support
- **Ensuring security** through vigilant review practices

### Maintainer Permissions

You have access to:

- ✅ Triage issues and PRs
- ✅ Assign and unassign
- ✅ Apply labels
- ✅ Merge pull requests
- ✅ Close issues
- ✅ Manage discussions
- ✅ Configure automation

______________________________________________________________________

## Daily Responsibilities

### Morning Routine (15-30 minutes)

1. **Check notifications**

   - Review overnight activity
   - Prioritize urgent items
   - Note items needing response

1. **Triage new items**

   - Issues with `needs-triage` label
   - New discussions
   - Stale item alerts
   - Security advisories

1. **Review dashboards**

   - [Open PRs awaiting review](https://github.com/%7B%7BORG_NAME%7D%7D/.github/pulls?q=is%3Apr+is%3Aopen+label%3Aawaiting-review)
   - [Issues needing triage](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage)
   - [Blocked items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22status%3A+blocked%22)
   - [Critical items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22priority%3A+critical%22)

### Throughout the Day

1. **Respond to mentions**

   - Answer questions
   - Provide guidance
   - Unblock contributors

1. **Review pull requests**

   - Approve or request changes
   - Merge when ready
   - Provide constructive feedback

1. **Monitor automation**

   - Check workflow runs
   - Address failures
   - Review auto-applied labels

### End of Day (5-10 minutes)

1. **Quick review**

   - Any urgent items still open?
   - All critical items addressed?
   - Any contributors waiting >24hrs?

1. **Update project boards** (if used)

   - Move cards appropriately
   - Update status

______________________________________________________________________

## Discussion Management

### Triage Process

**Goal**: Classify and guide discussions toward resolution

#### Step 1: Initial Review

When a new discussion is created:

1. **Read thoroughly**

   - Understand the topic
   - Check for duplicates
   - Assess actionability

1. **Categorize** (if needed)

   - Move to appropriate category
   - Add relevant labels if available

1. **Respond within 48 hours**

   ```markdown
   Thanks for starting this discussion, @username!

   [Provide initial thoughts/guidance]

   [Ask clarifying questions if needed]

   [Suggest next steps]
   ```

#### Step 2: Guide Discussion

1. **Facilitate conversation**

   - Ask probing questions
   - Connect related discussions
   - Moderate if needed

1. **Build consensus**

   - Summarize key points
   - Identify agreement/disagreement
   - Guide toward decision

1. **Track actionable items**

   - Note features to build
   - Bugs to fix
   - Documentation to add

#### Step 3: Resolution

**Convert to Issue** (if actionable):

```markdown
Great discussion! I'm converting this to an issue for tracking.

**Summary**: [Brief summary]
**Action Items**: [What will be done]

See #123 for the issue.
```

Then:

- Create issue with clear requirements
- Link to discussion
- Close discussion as "answered"
- Thank participants

**Mark as Answered** (if resolved):

- Mark the best answer
- Add closing comment
- Lock if no further discussion needed

**Close** (if not actionable):

```markdown
Thank you for this discussion. After consideration, we've decided this isn't something we'll pursue because [reason].

Feel free to continue the conversation or open a new discussion if circumstances change.
```

### Discussion SLAs

| Priority          | Response Time | Resolution Target |
| ----------------- | ------------- | ----------------- |
| Security-related  | 4 hours       | 24 hours          |
| Critical features | 24 hours      | 7 days            |
| General           | 48 hours      | 30 days           |
| Questions         | 72 hours      | When answered     |

______________________________________________________________________

## Issue Management

### Triage Process (REQUIRED within 48 hours)

**Goal**: Classify, prioritize, and prepare issues for work

#### Step 1: Validate Issue

1. **Check template usage**

   - Is template filled out?
   - Is information complete?
   - Are reproduction steps clear?

1. **Verify issue**

   - Can you reproduce it?
   - Is it actually a bug/feature?
   - Is it in scope for the project?

1. **Check for duplicates**

   - Search existing issues
   - Link if duplicate
   - Close with reference

#### Step 2: Label Appropriately

**Required Labels**:

- **Type**: `type: bug`, `type: feature`, `type: documentation`, etc.
- **Priority**: `priority: critical`, `priority: high`, `priority: medium`,
  `priority: low`
- **Status**: `status: backlog` (after triage)

**Optional Labels**:

- **Area**: `area: frontend`, `area: backend`, etc.
- **Size**: `size: small`, `size: medium`, `size: large`
- **Special**: `good-first-issue`, `help-wanted`, etc.

#### Step 3: Set Priority

**Critical** (`priority: critical`):

- Production down
- Security vulnerability
- Data loss
- Widespread breakage

**High** (`priority: high`):

- Blocking workflows
- Significant degradation
- Important features
- Breaking changes needed

**Medium** (`priority: medium`):

- Standard features
- Non-blocking bugs
- Performance improvements
- Good enhancements

**Low** (`priority: low`):

- Nice-to-haves
- Minor improvements
- Edge cases
- Future considerations

#### Step 4: Add Context

```markdown
## Triage Notes

**Priority**: High - Blocking user workflows
**Complexity**: Medium - Requires backend changes
**Dependencies**: None
**Acceptance Criteria**:

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests added
- [ ] Documentation updated

**Notes**:

- Consider X approach
- Related to #456
- May need discussion with team
```

#### Step 5: Remove `needs-triage` Label

Automation will do this when:

- Type label added
- Priority label added
- Status label added

Or remove manually after complete triage.

### Assignment Process

**When contributor requests assignment**:

1. **Check contributor**

   - First-time contributor? → Recommend `good-first-issue`
   - History of contributions? → Can handle more complex
   - Already assigned to other issues? → Ask to complete those first

1. **Assign issue**

   ```bash
   # Via GitHub UI: click "Assignees" → select user
   ```

1. **Update labels**

   - Remove `status: backlog`
   - Add `status: in-progress`
   - Automation will handle this

1. **Provide guidance**

   ```markdown
   Assigned to you, @username! 🎉

   **Next Steps**:

   1. Review acceptance criteria
   2. Ask any questions
   3. Create a feature branch
   4. Open a draft PR when ready
   5. Link the PR to this issue

   **Resources**:

   - [Development Setup](../guides/DEVELOPMENT_ENVIRONMENT_SETUP.md)
   - [Contributing Guide](../governance/CONTRIBUTING.md)

   Let us know if you need help!
   ```

### Monitoring In-Progress Issues

**Weekly check**:

- Issues in-progress > 14 days without activity
- Automation will warn at 14 days
- Automation will unassign at 21 days

**Your action if warned**:

- Check in with assignee
- Offer help if blocked
- Reassign if not actively working

### Closing Issues

**When PR is merged**:

- Automation closes linked issues
- Verify closure is appropriate
- Add to release notes if significant

**When closing without PR**:

```markdown
Closing this issue because [reason].

[Provide explanation]
[Link to relevant discussion/PR if applicable]
[Offer alternatives if applicable]

Feel free to reopen if circumstances change.
```

______________________________________________________________________

## Pull Request Management

### Review Priorities

Review PRs in this order:

1. **Critical fixes** (`priority: critical`)
1. **Security patches** (`type: security`)
1. **Breaking changes** (`breaking-change`)
1. **Ready PRs from active contributors**
1. **Draft PRs** (quick feedback only)
1. **First-time contributor PRs** (encourage and guide)

### Review Process

#### Step 1: Initial Assessment

1. **Automated checks**

   - Are CI checks passing?
   - Are security scans clear?
   - Is code coverage acceptable?

1. **PR metadata**

   - Is template filled out?
   - Is issue linked?
   - Are changes described clearly?

1. **Size check**

   - Is PR reasonably sized?
   - If too large, suggest splitting

#### Step 2: Code Review

**Review for**:

✅ **Correctness**:

- Does it solve the problem?
- Are edge cases handled?
- Is error handling appropriate?

✅ **Quality**:

- Follows coding standards?
- Is code readable?
- Are names meaningful?
- Is complexity reasonable?

✅ **Testing**:

- Are tests included?
- Do tests cover edge cases?
- Are tests meaningful?

✅ **Documentation**:

- Are changes documented?
- Are comments helpful?
- Is README updated?

✅ **Security**:

- No secrets exposed?
- Input validated?
- Security best practices followed?

✅ **Performance**:

- No obvious performance issues?
- Database queries efficient?
- Resources properly managed?

#### Step 3: Provide Feedback

**For changes needed**:

```markdown
Thanks for this PR, @username! Great work on [positive aspect].

I have a few suggestions:

**Required Changes**:

- [ ] [File:line] [Specific issue and how to fix]
- [ ] [General issue with examples]

**Optional Improvements**:

- Consider [suggestion] to [benefit]
- You might want to [alternative approach]

**Questions**:

- Why did you choose [approach]?
- Have you considered [alternative]?

Let me know if you have questions!
```

**For approval**:

```markdown
Excellent work, @username! 🎉

Code looks good and all checks are passing. Approving!

**Highlights**:

- [Particularly good aspect]
- [Another strong point]

Thanks for contributing!
```

#### Step 4: Merge Decision

**Merge when**:

- ✅ At least 1 approval from CODEOWNERS
- ✅ All CI checks pass
- ✅ No merge conflicts
- ✅ No requested changes outstanding
- ✅ Branch is up to date

**Merge methods**:

- **Squash and merge**: Most common, clean history
- **Rebase and merge**: For clean commit history preservation
- **Merge commit**: For feature branches with meaningful commits

**After merge**:

- Automation deletes branch
- Automation closes linked issues
- Verify everything completed correctly

### Handling Difficult Situations

**PR author is unresponsive**:

1. Comment asking for update
1. Wait 7 days
1. If no response, close with explanation
1. Offer to reopen when ready

**PR has extensive changes requested**:

1. Provide clear, actionable feedback
1. Offer to pair program if helpful
1. Consider taking over if critical and author stuck

**PR is contentious**:

1. Facilitate discussion
1. Seek consensus
1. Make final decision if needed
1. Document reasoning

______________________________________________________________________

## Automation Tools

### Available Automations

| Workflow                | Purpose                       | When It Runs              |
| ----------------------- | ----------------------------- | ------------------------- |
| `issue-triage`          | Auto-label and track SLA      | Issue opened, daily check |
| `auto-assign-reviewers` | Assign based on CODEOWNERS    | PR ready for review       |
| `status-sync`           | Sync issue/PR statuses        | Status changes            |
| `stale-management`      | Handle inactive items         | Daily                     |
| `auto-labeler`          | Apply labels based on content | Issue/PR opened           |
| `pr-quality-checks`     | Run CI, linting, tests        | PR opened/updated         |
| `auto-enable-merge`     | Enable auto-merge when ready  | PR approved               |

### Monitoring Automation

**Check workflow runs**:

- [Actions tab](https://github.com/%7B%7BORG_NAME%7D%7D/.github/actions)
- Failed runs notify maintainers
- Review logs for issues

**Adjust automation**:

- Edit workflow files in `.github/workflows/`
- Update label configs in `.github/labels.yml`
- Modify CODEOWNERS as team changes

______________________________________________________________________

## Best Practices

### Communication

✅ **Do**:

- Be welcoming and encouraging
- Provide constructive feedback
- Explain the "why" behind decisions
- Thank contributors regularly
- Respond within SLAs

❌ **Don't**:

- Be dismissive or harsh
- Make assumptions about skill level
- Let things go silent
- Forget to celebrate wins

### Decision Making

✅ **Do**:

- Seek input from team
- Document decisions
- Consider long-term implications
- Be consistent
- Explain reasoning

❌ **Don't**:

- Make arbitrary decisions
- Change standards without notice
- Ignore community feedback
- Rush important decisions

### Quality Standards

✅ **Do**:

- Maintain high standards
- Apply standards consistently
- Help contributors meet standards
- Update standards as project evolves

❌ **Don't**:

- Accept subpar code
- Have different standards for different people
- Change standards retroactively
- Make standards impossible to meet

______________________________________________________________________

## Escalation Procedures

### When to Escalate

**Technical disagreements**:

- Can't reach consensus on approach
- Security concerns
- Architectural decisions

**Community issues**:

- Code of Conduct violations
- Harassment or abuse
- Toxic behavior

**Resource constraints**:

- Too many open items
- Contributors waiting too long
- Burnout concerns

### How to Escalate

1. **Technical**: Bring to maintainers meeting or discussion
1. **Community**: Contact organization admins immediately
1. **Resources**: Discuss with team lead

______________________________________________________________________

## Quick Reference

### Common Commands

```bash
# Assign issue
# Via UI: Assignees → select user

# Add label
# Via UI: Labels → select label

# Merge PR
# Via UI: Merge button → select method

# Close issue
# Via UI: Close issue button
```

### Useful Filters

- [Needs triage](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage)
- [Awaiting review](https://github.com/%7B%7BORG_NAME%7D%7D/.github/pulls?q=is%3Apr+is%3Aopen+label%3Aawaiting-review)
- [Blocked items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22status%3A+blocked%22)
- [Critical](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22priority%3A+critical%22)
- [Stale](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3Astale)

### Key Documents

- [Workflow Design](WORKFLOW_DESIGN.md)
- [Labels Guide](../reference/LABELS.md)
- [Governance](../governance/GOVERNANCE.md)
- [Contributing Guide](../governance/CONTRIBUTING.md)

______________________________________________________________________

**Thank you for being a maintainer!** 🙏

Your work makes this project successful.

______________________________________________________________________

_Last Updated: January 15, 2026_

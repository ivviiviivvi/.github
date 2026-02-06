# GitHub Projects Automation Rules Setup Guide

> **Complete guide to configuring automation rules for all 7 projects**

## Overview

GitHub Projects V2 automation rules must be configured through the GitHub UI.
This guide provides step-by-step instructions for setting up all automation
rules across the 7 projects.

**Time Required:** ~30 minutes per project (3.5 hours total)

______________________________________________________________________

## Quick Access Links

- **Project #8**:
  [AI Framework Development](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/8)
- **Project #9**:
  [Documentation & Knowledge](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/9)
- **Project #10**:
  [Workflow Automation](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/10)
- **Project #11**:
  [Security & Compliance](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/11)
- **Project #12**:
  [Infrastructure & DevOps](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/12)
- **Project #13**:
  [Community & Support](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/13)
- **Project #14**:
  [Product Roadmap](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/14)

______________________________________________________________________

## General Setup Instructions

### Accessing Automation Settings

1. Navigate to the project
1. Click the **⋮** (three dots) menu in the top-right
1. Select **"Workflows"**
1. Click **"+ New workflow"**

### Workflow Types

- **Item added to project** - Triggers when an item is added
- **Item reopened** - Triggers when an item is reopened
- **Item closed** - Triggers when an item is closed
- **Pull request merged** - Triggers when a PR is merged
- **Pull request approved** - Triggers when a PR is approved

### Actions Available

- **Set field value** - Update a custom field
- **Archive item** - Archive the item
- **Convert to draft** - Convert PR to draft

______________________________________________________________________

## Project #8: AI Framework Development

### Automation Rules

#### Rule 1: New Items → Planned Status

- **Trigger:** Item added to project
- **Action:** Set "Status" to "🎯 Planned"

#### Rule 2: PR Approved → Code Review

- **Trigger:** Pull request approved
- **Action:** Set "Status" to "👀 Code Review"

#### Rule 3: PR Merged → Deployed

- **Trigger:** Pull request merged
- **Action:** Set "Status" to "🚀 Deployed"

#### Rule 4: Item Closed → Documentation or Completed

- **Trigger:** Item closed
- **Action:** Set "Status" to "✔️ Completed"

#### Rule 5: Auto-assign Language

- **Trigger:** Item added to project
- **Condition:** If label contains "python"
- **Action:** Set "Language" to "Python"

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/8
2. Click ⋮ → Workflows
3. For each rule above:
   - Click "+ New workflow"
   - Select the trigger
   - Add conditions if needed
   - Select the action
   - Choose field and value
   - Click "Save workflow"
```

______________________________________________________________________

## Project #9: Documentation & Knowledge

### Automation Rules

#### Rule 1: New Docs → Draft Status

- **Trigger:** Item added to project
- **Action:** Set "Status" to "📝 Draft"

#### Rule 2: PR Approved → Ready for Review

- **Trigger:** Pull request approved
- **Action:** Set "Status" to "👀 In Review"

#### Rule 3: PR Merged → Published

- **Trigger:** Pull request merged
- **Action:** Set "Status" to "✅ Published"
- **Additional:** Set "Last Updated" to today

#### Rule 4: Set Document Type by Path

- **Trigger:** Item added to project
- **Condition:** If file path contains "docs/"
- **Action:** Set "Document Type" to "Technical Documentation"

#### Rule 5: Mark Outdated Docs

- **Trigger:** Manual review (not automated)
- **Note:** Requires periodic manual review of "Last Updated" field

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/9
2. Click ⋮ → Workflows
3. For each rule above:
   - Click "+ New workflow"
   - Select the trigger
   - Add conditions if needed
   - Select the action
   - Choose field and value
   - Click "Save workflow"
```

______________________________________________________________________

## Project #10: Workflow Automation

### Automation Rules

#### Rule 1: New Workflows → Ideation

- **Trigger:** Item added to project
- **Action:** Set "Workflow Status" to "💡 Ideation"

#### Rule 2: PR Created → In Development

- **Trigger:** Item becomes pull request
- **Action:** Set "Workflow Status" to "🏗️ In Development"

#### Rule 3: PR Approved → Testing

- **Trigger:** Pull request approved
- **Action:** Set "Workflow Status" to "🧪 Testing"

#### Rule 4: PR Merged → Active

- **Trigger:** Pull request merged
- **Action:** Set "Workflow Status" to "✅ Active"

#### Rule 5: Track SLA Violations

- **Trigger:** Manual review (scheduled)
- **Note:** Requires periodic check of SLA Target vs actual performance

#### Rule 6: Set Workflow Type by Label

- **Trigger:** Item added to project
- **Condition:** If label is "ci/cd"
- **Action:** Set "Workflow Type" to "CI/CD Pipeline"

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/10
2. Click ⋮ → Workflows
3. Follow standard workflow creation steps
```

______________________________________________________________________

## Project #11: Security & Compliance

### Automation Rules

#### Rule 1: New Security Issues → Reported

- **Trigger:** Item added to project
- **Action:** Set "Security Status" to "🔍 Reported"

#### Rule 2: High Severity Auto-Prioritize

- **Trigger:** Item added to project
- **Condition:** If label is "security" AND "critical"
- **Action:** Set "Severity" to "🔴 Critical"

#### Rule 3: In Progress on Assignment

- **Trigger:** Item assigned to someone
- **Action:** Set "Security Status" to "🔧 In Progress"

#### Rule 4: PR Approved → Ready for Deploy

- **Trigger:** Pull request approved
- **Action:** Set "Security Status" to "✅ Fixed (Testing)"

#### Rule 5: PR Merged → Resolved

- **Trigger:** Pull request merged
- **Action:** Set "Security Status" to "✔️ Resolved"

#### Rule 6: Set CVSS Score

- **Trigger:** Manual (requires analysis)
- **Note:** CVSS scores must be calculated and entered manually

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/11
2. Click ⋮ → Workflows
3. Follow standard workflow creation steps
```

______________________________________________________________________

## Project #12: Infrastructure & DevOps

### Automation Rules

#### Rule 1: New Items → Proposed

- **Trigger:** Item added to project
- **Action:** Set "Deployment Status" to "📋 Proposed"

#### Rule 2: PR Created → In Development

- **Trigger:** Item becomes pull request
- **Action:** Set "Deployment Status" to "🔧 In Development"

#### Rule 3: PR Approved → Ready to Deploy

- **Trigger:** Pull request approved
- **Action:** Set "Deployment Status" to "✅ Ready to Deploy"

#### Rule 4: PR Merged → Deployed

- **Trigger:** Pull request merged
- **Action:** Set "Deployment Status" to "🚀 Deployed"
- **Additional:** Set "Last Deployed" to today

#### Rule 5: Set Environment by Label

- **Trigger:** Item added to project
- **Condition:** If label is "production"
- **Action:** Set "Environment" to "Production"

#### Rule 6: High Priority Infrastructure

- **Trigger:** Item added to project
- **Condition:** If label contains "incident" OR "outage"
- **Action:** Set "Priority" to "🔥 Critical"

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/12
2. Click ⋮ → Workflows
3. Follow standard workflow creation steps
```

______________________________________________________________________

## Project #13: Community & Support

### Automation Rules

#### Rule 1: New Items → Triage

- **Trigger:** Item added to project
- **Action:** Set "Support Status" to "📥 Triage"

#### Rule 2: Assigned → In Progress

- **Trigger:** Item assigned to someone
- **Action:** Set "Support Status" to "💬 In Progress"
- **Additional:** Set "First Response" to today

#### Rule 3: PR Approved → Ready

- **Trigger:** Pull request approved
- **Action:** Set "Support Status" to "✅ Ready"

#### Rule 4: Closed → Resolved

- **Trigger:** Item closed
- **Action:** Set "Support Status" to "✔️ Resolved"
- **Additional:** Set "Resolution Date" to today

#### Rule 5: Good First Issue Auto-Tag

- **Trigger:** Item added to project
- **Condition:** If label is "good first issue"
- **Action:** Set "Engagement Type" to "Contribution Opportunity"

#### Rule 6: Response Time SLA

- **Trigger:** Manual review (scheduled)
- **Note:** Check Response Time field against SLA targets

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/13
2. Click ⋮ → Workflows
3. Follow standard workflow creation steps
```

______________________________________________________________________

## Project #14: Product Roadmap

### Automation Rules

#### Rule 1: New Features → Backlog

- **Trigger:** Item added to project
- **Action:** Set "Roadmap Status" to "📋 Backlog"

#### Rule 2: Planned Items → Set Timeline

- **Trigger:** Status changed to "📅 Planned"
- **Action:** Require "Timeline" and "Target Date" fields

#### Rule 3: In Progress → Set Priority

- **Trigger:** Status changed to "🚧 In Progress"
- **Action:** Ensure "Priority" is set

#### Rule 4: PR Merged → In Progress or Completed

- **Trigger:** Pull request merged
- **Action:** Set "Roadmap Status" to "🚧 In Progress"

#### Rule 5: Item Closed → Completed

- **Trigger:** Item closed
- **Action:** Set "Roadmap Status" to "✅ Completed"

#### Rule 6: High Priority Features

- **Trigger:** Item added to project
- **Condition:** If label is "priority" OR "urgent"
- **Action:** Set "Priority" to "⚡ High"

**Setup Steps:**

```
1. Go to https://github.com/orgs/{{ORG_NAME}}/projects/14
2. Click ⋮ → Workflows
3. Follow standard workflow creation steps
```

______________________________________________________________________

## Automation Best Practices

### General Guidelines

1. **Start Simple**: Begin with basic status transitions
1. **Test First**: Create one rule, test it, then add more
1. **Document Changes**: Note what each rule does
1. **Review Regularly**: Check if rules are working as expected
1. **Iterate**: Adjust rules based on team usage patterns

### Common Patterns

**Status Progression:**

```
New → In Progress → Review → Complete
```

**PR Workflow:**

```
Draft → In Development → Review → Testing → Deployed
```

**Priority Escalation:**

```
If (critical label OR high severity) → Set Priority High
```

### Testing Your Rules

1. **Create a test issue**
1. **Add it to the project**
1. **Verify the automation triggered**
1. **Check field values were set correctly**
1. **Close the test issue**

______________________________________________________________________

## Troubleshooting

### Rule Not Triggering

**Possible Causes:**

- Workflow is disabled
- Conditions don't match
- Field values don't exist
- Permission issues

**Solutions:**

1. Check workflow is enabled (toggle in UI)
1. Review conditions and test values
1. Verify field options exist
1. Ensure proper org permissions

### Wrong Field Value Set

**Solutions:**

1. Edit the workflow
1. Update the field value selection
1. Test with a new item

### Multiple Rules Conflicting

**Solutions:**

1. Review rule order (rules run in sequence)
1. Make conditions more specific
1. Consider combining rules
1. Disable conflicting rules

______________________________________________________________________

## Verification Checklist

After setting up automation for each project:

- [ ] All workflows are enabled
- [ ] Test each trigger type with a dummy issue
- [ ] Verify field values are set correctly
- [ ] Check no conflicting rules exist
- [ ] Document any manual workflows needed
- [ ] Train team on how automation works

______________________________________________________________________

## Next Steps

1. **Start with Project #8** (AI Framework Development)
1. **Set up all 5-6 rules** for that project
1. **Test thoroughly** with real issues
1. **Repeat for remaining projects**
1. **Document any custom rules** your team needs
1. **Review after 1 week** of usage

______________________________________________________________________

## Additional Resources

- [GitHub Projects Automation Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Project Implementation Guide](../../../../docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md)
- [Project Deployment Guide](../../../../docs/guides/GITHUB_PROJECTS_DEPLOYMENT.md)

______________________________________________________________________

**Questions or Issues?**

- Open an issue in the repository
- Check the GitHub Projects documentation
- Reach out to the project maintainers

______________________________________________________________________

_Created: 2026-01-18_

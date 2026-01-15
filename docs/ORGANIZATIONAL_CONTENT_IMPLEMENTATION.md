# Organizational Content Implementation Guide

> **Step-by-step guide to deploying comprehensive organizational content**

This guide walks you through implementing the complete organizational content
framework across your repositories.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Phase 1: Planning](#phase-1-planning)
- [Phase 2: Initial Setup](#phase-2-initial-setup)
- [Phase 3: Content Deployment](#phase-3-content-deployment)
- [Phase 4: Customization](#phase-4-customization)
- [Phase 5: Training & Rollout](#phase-5-training--rollout)
- [Phase 6: Monitoring & Iteration](#phase-6-monitoring--iteration)
- [Troubleshooting](#troubleshooting)

## Overview

### What You're Implementing

This guide helps you deploy:

- **Issue Management System** - 20+ issue types with taxonomy
- **Discussion Framework** - 12 categories with engagement strategy
- **Project Boards** - 10 templates for different workflows
- **Wiki Structure** - Complete documentation hierarchy

### Timeline

| Phase                  | Duration  | Effort Level |
| ---------------------- | --------- | ------------ |
| Planning               | 2-4 hours | Low          |
| Initial Setup          | 1-2 hours | Low          |
| Content Deployment     | 2-4 hours | Medium       |
| Customization          | 4-8 hours | Medium-High  |
| Training & Rollout     | 1-2 days  | Medium       |
| Monitoring & Iteration | Ongoing   | Low          |

**Total Initial Setup**: 1-2 days\
**To Full Maturity**: 2-4 weeks

### Team Roles

| Role                    | Responsibilities            | Time Commitment |
| ----------------------- | --------------------------- | --------------- |
| **Project Lead**        | Overall coordination        | 4-8 hours       |
| **Documentation Owner** | Wiki setup and maintenance  | 4-6 hours       |
| **Community Manager**   | Discussions and engagement  | 3-5 hours       |
| **Project Manager**     | Project board configuration | 2-4 hours       |
| **Developers**          | Issue triage and labeling   | 1-2 hours       |

## Prerequisites

### Required Access

- [ ] Organization owner or admin access
- [ ] Repository admin access for target repos
- [ ] GitHub CLI (`gh`) installed
- [ ] Git configured locally

### Required Knowledge

- [ ] Basic GitHub features understanding
- [ ] Markdown formatting
- [ ] Git basics
- [ ] Your organization's workflows

### Recommended Reading

Before starting, read:

1. [Master Index](ORGANIZATIONAL_CONTENT_INDEX.md) - 20 min
1. [Issue Taxonomy](ISSUE_TAXONOMY.md) - 25 min
1. [Discussion Guide](DISCUSSION_GUIDE.md) - 40 min
1. [Projects Guide](PROJECTS_GUIDE.md) - 50 min
1. [Wiki Guide](WIKI_GUIDE.md) - 60 min

**Total**: ~3 hours (can be spread over days)

## Phase 1: Planning

### Step 1.1: Assess Current State

**Audit your current setup** (30 minutes):

```bash
# Check enabled features across org
for repo in $(gh repo list YOUR_ORG --limit 100 --json name -q '.[].name'); do
  echo "=== $repo ==="
  gh repo view YOUR_ORG/$repo --json hasIssuesEnabled,hasDiscussionsEnabled,hasProjectsEnabled,hasWikiEnabled
done
```

Document:

- [ ] Which repositories have which features enabled
- [ ] Current issue/discussion/project usage
- [ ] Existing wiki content
- [ ] Active community size

### Step 1.2: Define Scope

**Decide what to implement** (30 minutes):

| Feature     | Priority        | Repositories | Notes |
| ----------- | --------------- | ------------ | ----- |
| Issues      | High/Medium/Low | List repos   |       |
| Discussions | High/Medium/Low | List repos   |       |
| Projects    | High/Medium/Low | List repos   |       |
| Wikis       | High/Medium/Low | List repos   |       |

**Recommendation**: Start with 2-3 pilot repositories before organization-wide
rollout.

### Step 1.3: Customize Strategy

**Adapt framework to your needs** (1 hour):

Review each guide and note:

- [ ] Which templates need customization
- [ ] Which categories/types are relevant
- [ ] What terminology to use
- [ ] Integration with existing tools

### Step 1.4: Create Implementation Plan

**Timeline and milestones** (30 minutes):

```markdown
## Implementation Timeline

### Week 1: Setup

- [ ] Enable features
- [ ] Deploy templates
- [ ] Initial customization

### Week 2: Content Creation

- [ ] Create initial issues
- [ ] Start first discussions
- [ ] Set up project boards

### Week 3: Training

- [ ] Team training sessions
- [ ] Documentation review
- [ ] Q&A sessions

### Week 4: Rollout

- [ ] Organization-wide announcement
- [ ] Monitor adoption
- [ ] Collect feedback
```

## Phase 2: Initial Setup

### Step 2.1: Enable Features

**Enable on pilot repositories** (15 minutes):

```bash
# For each pilot repo
REPO="YOUR_ORG/your-repo"

# Enable all features
gh repo edit $REPO \
  --enable-issues \
  --enable-discussions \
  --enable-projects \
  --enable-wiki

# Verify
gh repo view $REPO --json hasIssuesEnabled,hasDiscussionsEnabled,hasProjectsEnabled,hasWikiEnabled
```

### Step 2.2: Configure Repository Settings

**Adjust settings for optimal usage** (15 minutes):

For each repository:

1. **Issues**:
   - Enable issue templates
   - Disable blank issues (optional)
   - Set up labels (see Step 2.3)

1. **Discussions**:
   - Enable discussions
   - Create categories (see Step 3.2)
   - Set category settings

1. **Projects**:
   - Enable projects v2
   - Create initial project (see Step 3.3)

1. **Wiki**:
   - Enable wiki
   - Restrict editing (optional)

### Step 2.3: Set Up Labels

**Create standard label set** (20 minutes):

```bash
# Use the GitHub CLI with label file
gh label create --repo $REPO \
  --name "P0-Critical" \
  --color "B60205" \
  --description "Critical priority - immediate attention"

gh label create --repo $REPO \
  --name "P1-High" \
  --color "D93F0B" \
  --description "High priority - address soon"

# Or use a labels sync tool
cat > labels.yml << EOF
- name: "P0-Critical"
  color: "B60205"
  description: "Critical priority - immediate attention"
- name: "P1-High"
  color: "D93F0B"
  description: "High priority - address soon"
# ... add all labels
EOF

# Apply labels
gh label sync --repo $REPO --file labels.yml
```

See [LABELS.md](LABELS.md) for complete label list.

### Step 2.4: Clone Templates

**Copy template files to repository** (15 minutes):

```bash
# Clone the .github repo
git clone https://github.com/YOUR_ORG/.github.git

# Copy templates to target repo
cd your-target-repo

# Copy issue templates
cp -r ../.github/ISSUE_TEMPLATE .github/

# Copy discussion starters (for reference)
cp -r ../.github/discussion-starters .github/

# Copy project templates (for reference)
cp -r ../.github/project-templates .github/

# Copy wiki templates (for reference)
cp -r ../.github/wiki-templates .github/

# Commit
git add .github
git commit -m "chore: add organizational content templates"
git push
```

## Phase 3: Content Deployment

### Step 3.1: Deploy Initial Issues

**Create foundational tracking issues** (30 minutes):

**Option A: Use Automation Workflow**

```bash
# Dry run first
gh workflow run create-organizational-content.yml \
  -f content_type=issues \
  -f target_repo=YOUR_ORG/your-repo \
  -f dry_run=true

# Wait for workflow to complete, review output

# Deploy for real
gh workflow run create-organizational-content.yml \
  -f content_type=issues \
  -f target_repo=YOUR_ORG/your-repo \
  -f dry_run=false
```

**Option B: Manual Creation**

Select 5-10 most important issues from the [Issue Taxonomy](ISSUE_TAXONOMY.md)
and create manually.

**Recommended Initial Issues**:

1. Documentation Audit
1. Security Hardening
1. Testing Coverage
1. Community Health
1. Onboarding Improvement

### Step 3.2: Set Up Discussions

**Create discussion categories** (30 minutes):

In repository settings → Discussions:

1. **Create Categories**:
   - 📢 Announcements (read-only)
   - 💡 Ideas & Feature Proposals
   - ❓ Q&A
   - 🏆 Show and Tell
   - 🎯 Best Practices
   - 🐛 Troubleshooting & Support

1. **Configure Each Category**:
   - Set appropriate format (Discussion/Q&A/Announcement)
   - Write category descriptions
   - Set moderation policies

1. **Create Initial Discussions**:

   ```bash
   # Welcome discussion
   gh discussion create \
     --repo YOUR_ORG/your-repo \
     --category "General" \
     --title "👋 Welcome to Our Community!" \
     --body-file .github/discussion-starters/welcome.md

   # Best practices discussion
   gh discussion create \
     --repo YOUR_ORG/your-repo \
     --category "Best Practices" \
     --title "🎯 Best Practices Discussion" \
     --body-file .github/discussion-starters/best-practices.md
   ```

### Step 3.3: Create Project Boards

**Set up initial projects** (45 minutes):

**Using GitHub Web UI** (Projects v2 CLI support is limited):

1. **Create Product Roadmap Project**:
   - Go to organization → Projects → New project
   - Choose "Roadmap" template or blank
   - Add custom fields from
     [product-roadmap.json](.github/project-templates/product-roadmap.json)
   - Set up views (Roadmap, By Status, By Priority)

1. **Create Bug Triage Project**:
   - Create new project
   - Add custom fields from
     [bug-triage.json](.github/project-templates/bug-triage.json)
   - Set up board view grouped by priority

1. **Link to Repository**:
   - Add repository to project
   - Set up auto-add workflows
   - Configure status automations

### Step 3.4: Initialize Wiki

**Create initial wiki structure** (45 minutes):

```bash
# Clone wiki repo
git clone https://github.com/YOUR_ORG/your-repo.wiki.git

cd your-repo.wiki

# Copy templates
cp ../.github/wiki-templates/Home.md .
cp ../.github/wiki-templates/Installation.md .
cp ../.github/wiki-templates/FAQ.md .
cp ../.github/wiki-templates/_Sidebar.md .

# Customize placeholders
# Edit each file and replace {{PLACEHOLDERS}} with actual values

# Example customization
sed -i 's/{{PROJECT_NAME}}/YourProject/g' *.md
sed -i 's/{{PROJECT_DESCRIPTION}}/Your project description/g' *.md

# Commit and push
git add .
git commit -m "Initialize wiki from templates"
git push
```

**Verify**: Visit `https://github.com/YOUR_ORG/your-repo/wiki`

## Phase 4: Customization

### Step 4.1: Tailor Issue Taxonomy

**Adapt to your workflow** (1-2 hours):

1. **Review Issue Types**:
   - Remove irrelevant types
   - Add domain-specific types
   - Adjust priority levels

1. **Customize Templates**:
   - Edit `.github/ISSUE_TEMPLATE/*.yml`
   - Adjust fields and options
   - Update descriptions

1. **Define Your SLAs**:
   - Set realistic response times
   - Define escalation procedures
   - Document in taxonomy

### Step 4.2: Customize Discussions

**Adapt categories to your community** (1 hour):

1. **Adjust Categories**:
   - Add/remove categories
   - Rename for your terminology
   - Reorder by importance

1. **Create Custom Starters**:
   - Write domain-specific templates
   - Add recurring discussion topics
   - Prepare FAQ content

1. **Set Moderation Policies**:
   - Define response expectations
   - Assign category moderators
   - Create escalation procedures

### Step 4.3: Configure Projects

**Customize for your workflows** (2 hours):

1. **Adjust Project Templates**:
   - Modify custom fields
   - Change status options
   - Add/remove columns

1. **Set Up Automations**:
   - Auto-add items based on labels
   - Auto-set field values
   - Status transitions

1. **Create Views**:
   - Team-specific views
   - Sprint/milestone views
   - Leadership dashboards

### Step 4.4: Organize Wiki

**Structure for your content** (1-2 hours):

1. **Plan Wiki Structure**:
   - Identify main sections
   - Plan page hierarchy
   - Design navigation

1. **Customize Templates**:
   - Adjust page templates
   - Add domain-specific sections
   - Create custom templates

1. **Create Content Plan**:
   - List pages to create
   - Assign content owners
   - Set deadlines

## Phase 5: Training & Rollout

### Step 5.1: Create Training Materials

**Prepare team for new system** (2-3 hours):

1. **Quick Reference Guides**:
   - One-pagers for each feature
   - Common workflows
   - Where to find what

1. **Video Walkthroughs**:
   - Screen recordings of key tasks
   - 2-5 minutes each
   - Upload to YouTube or internal platform

1. **FAQ Document**:
   - Anticipated questions
   - Answers with examples
   - Links to detailed docs

### Step 5.2: Conduct Training Sessions

**Train the team** (2-4 hours total):

**Session 1: Issues & Projects** (60 min)

- Overview of issue taxonomy
- How to create and label issues
- Using project boards
- Q&A

**Session 2: Discussions & Wiki** (60 min)

- Discussion categories and when to use
- How to start discussions
- Wiki structure and editing
- Q&A

**Session 3: Best Practices** (60 min)

- Do's and don'ts
- Real examples
- Workflows and integration
- Q&A

### Step 5.3: Rollout Communication

**Announce to organization** (1 hour):

1. **Create Announcement**:

   ```markdown
   # 🎉 New Organizational Content Framework

   We're excited to announce a comprehensive new framework for issues, discussions, projects, and wikis!

   ## What's New

   - Structured issue taxonomy
   - Discussion categories for community engagement
   - Project templates for better tracking
   - Organized wiki for documentation

   ## Resources

   - [Master Index](ORGANIZATIONAL_CONTENT_INDEX.md) - Start here
   - [Quick Start](ORGANIZATIONAL_CONTENT_QUICK_START.md) - Quick walkthroughs
   - [Summary](ORGANIZATIONAL_CONTENT_SUMMARY.md) - Common questions

   ## Getting Help

   - Ask in #org-content-help Slack channel
   - Comment on this discussion
   - Attend office hours (Fridays 2-3pm)

   We're here to help! 🚀
   ```

1. **Distribution Channels**:
   - [ ] GitHub Discussions announcement
   - [ ] Slack/Teams announcement
   - [ ] Email to organization
   - [ ] Mention in team meetings
   - [ ] Update README files

### Step 5.4: Establish Support

**Help team during transition** (ongoing):

1. **Office Hours**:
   - Weekly drop-in sessions
   - First 2-4 weeks
   - Record and share

1. **Slack Channel**:
   - Dedicated help channel
   - Monitor actively
   - Build FAQ from questions

1. **Documentation**:
   - Keep docs updated
   - Add examples from real use
   - Iterate based on feedback

## Phase 6: Monitoring & Iteration

### Step 6.1: Track Metrics

**Monitor adoption and usage** (weekly):

```bash
# Issue metrics
gh issue list --repo YOUR_ORG/your-repo --state all --json number,state,labels | \
  jq 'group_by(.state) | map({state: .[0].state, count: length})'

# Discussion metrics
gh api repos/YOUR_ORG/your-repo/discussions | \
  jq '.[] | {category: .category.name, comments: .comments.totalCount}'

# Project metrics (via web UI)
# Check project insights tab
```

**Key Metrics**:

- Issue creation rate
- Response times
- Discussion participation
- Project velocity
- Wiki page views

### Step 6.2: Collect Feedback

**Learn what works** (monthly):

1. **Surveys**:
   - Monthly pulse surveys
   - Specific feature feedback
   - Improvement suggestions

1. **Retrospectives**:
   - Monthly retro meeting
   - Review what's working
   - Identify pain points

1. **Usage Analysis**:
   - Most/least used features
   - Common workflows
   - Bottlenecks

### Step 6.3: Iterate

**Continuously improve** (ongoing):

1. **Monthly Reviews**:
   - [ ] Review metrics
   - [ ] Analyze feedback
   - [ ] Identify improvements
   - [ ] Update documentation

1. **Quarterly Updates**:
   - [ ] Major taxonomy updates
   - [ ] New templates
   - [ ] Process improvements
   - [ ] Training refreshers

1. **Annual Assessment**:
   - [ ] Full system review
   - [ ] ROI analysis
   - [ ] Strategic adjustments
   - [ ] Long-term roadmap

## Troubleshooting

### Common Issues

#### "Features won't enable"

**Cause**: Insufficient permissions\
**Solution**: Ensure organization
owner/admin access

#### "Templates not showing"

**Cause**: Not in `.github` directory or wrong format\
**Solution**: Verify file
location and YAML syntax

#### "Low adoption rate"

**Cause**: Lack of training or unclear value\
**Solution**: More training,
better communication, leadership buy-in

#### "Too complex for our needs"

**Cause**: Over-engineering\
**Solution**: Start smaller, use only what you
need, simplify

#### "Duplicates across repos"

**Cause**: Lack of coordination\
**Solution**: Use org-level projects,
cross-repo discussions

### Getting Help

- 📖 Review documentation guides
- 💬 Ask in Discussions
- 📧 Contact org maintainers
- 🤝 Community support channels

## Success Checklist

### Week 1

- [ ] Features enabled on pilot repos
- [ ] Labels configured
- [ ] Initial issues created
- [ ] Discussion categories set up
- [ ] First project board created
- [ ] Wiki initialized

### Month 1

- [ ] Training completed
- [ ] Organization announced
- [ ] Active usage started
- [ ] Feedback collected
- [ ] First iteration complete

### Quarter 1

- [ ] Full adoption across pilot repos
- [ ] Metrics showing value
- [ ] Community engagement strong
- [ ] Documentation complete and current
- [ ] Ready for org-wide rollout

## Next Steps

After successful pilot:

1. **Expand to More Repositories**:
   - Apply learnings
   - Streamline process
   - Automate where possible

1. **Enhance Automation**:
   - More workflow automations
   - Integration with other tools
   - Reporting dashboards

1. **Community Building**:
   - Foster engagement
   - Recognize contributors
   - Build culture

1. **Continuous Improvement**:
   - Regular reviews
   - Keep current with GitHub features
   - Adapt to changing needs

---

**Remember**: This is a journey, not a destination. Start small, learn, iterate,
and grow! 🚀

**Questions?** See [Master Index](ORGANIZATIONAL_CONTENT_INDEX.md) or ask in
Discussions.

# GitHub Wiki Guide

> **Comprehensive guide for creating and maintaining GitHub Wikis in the
> Ivviiviivvi organization**

This guide provides an exhaustive framework for leveraging GitHub Wikis as a
knowledge management and documentation platform across all organization
repositories.

## Table of Contents

- [Overview](#overview)
- [Wiki Structure](#wiki-structure)
- [Content Types](#content-types)
- [Wiki Templates](#wiki-templates)
- [Maintenance & Governance](#maintenance--governance)
- [Integration with Repository](#integration-with-repository)
- [Migration & Backup](#migration--backup)

## Overview

GitHub Wikis provide collaborative documentation with:

- **Git-based versioning** for all content
- **Markdown formatting** for easy writing
- **No PR required** for quick updates (when enabled)
- **Full-text search** across all pages
- **Sidebar navigation** for organization
- **Page history** and diff viewing

### When to Use Wiki vs Docs Folder

| Wiki                              | Docs Folder (`/docs`)                      |
| --------------------------------- | ------------------------------------------ |
| Community-editable knowledge base | Official, version-controlled documentation |
| Frequently updated content        | Stable, release-tied documentation         |
| Collaborative how-tos and guides  | API references and specifications          |
| FAQs and troubleshooting          | Architecture and design documents          |
| Process documentation             | Legal and compliance docs                  |
| Quick reference                   | Code-reviewed documentation                |

**General Rule**: Use wikis for living documentation that benefits from
community contribution. Use `/docs` for official documentation that requires
review.

## Wiki Structure

### Recommended Organization

```
Wiki Home
├── Getting Started
│   ├── Installation
│   ├── Quick Start
│   ├── First Steps
│   └── Tutorials
│       ├── Beginner Tutorial
│       ├── Intermediate Tutorial
│       └── Advanced Tutorial
├── Guides
│   ├── User Guides
│   │   ├── Feature A Guide
│   │   ├── Feature B Guide
│   │   └── Feature C Guide
│   ├── Developer Guides
│   │   ├── Development Setup
│   │   ├── Code Style
│   │   ├── Testing
│   │   └── Debugging
│   └── Admin Guides
│       ├── Deployment
│       ├── Configuration
│       └── Monitoring
├── Reference
│   ├── API Reference
│   ├── CLI Reference
│   ├── Configuration Reference
│   └── Glossary
├── How-To
│   ├── Common Tasks
│   ├── Troubleshooting
│   ├── Recipes
│   └── Tips & Tricks
├── Architecture
│   ├── System Overview
│   ├── Component Diagrams
│   ├── Data Models
│   └── Decision Records
├── Contributing
│   ├── Contribution Guidelines
│   ├── Code Review Process
│   ├── Release Process
│   └── Community
├── FAQ
│   ├── General Questions
│   ├── Technical Questions
│   ├── Business Questions
│   └── Community Questions
└── Resources
    ├── External Links
    ├── Related Projects
    ├── Publications
    └── Videos & Talks
```

### Sidebar Template

Create `_Sidebar.md` for navigation:

```markdown
## Navigation

**Getting Started**

- [[Home]]
- [[Installation]]
- [[Quick Start]]
- [[Tutorials]]

**Guides**

- [[User Guide]]
- [[Developer Guide]]
- [[Admin Guide]]

**Reference**

- [[API Reference]]
- [[CLI Reference]]
- [[Configuration]]

**How-To**

- [[Common Tasks]]
- [[Troubleshooting]]
- [[FAQ]]

**Contributing**

- [[How to Contribute]]
- [[Code Review]]

**Resources**

- [[External Links]]
- [[Glossary]]

---

📝 [[Edit this page|_Sidebar]]
```

### Footer Template

Create `_Footer.md` for consistent footers:

```markdown
---

📚 **Ivviiviivvi Organization** | [Main Repo](https://github.com/{{ORG_NAME}}/.github) | [Discussions](https://github.com/orgs/{{ORG_NAME}}/discussions)

Last updated: {{date}} | [Edit this page]({{page_url}}) | [View history]({{history_url}})

---

Licensed under [MIT License](../../LICENSE) | [Code of Conduct](../governance/CODE_OF_CONDUCT.md) | [Security Policy](../governance/SECURITY.md)
```

## Content Types

### 1. Home Page

**Purpose**: Entry point and overview

**Template**:

```markdown
# Project Name Wiki

> **Quick Description**: One-sentence description of the project

Welcome to the [Project Name] wiki! This is the community-maintained knowledge base for our project.

## 🚀 Quick Links

- **[[Installation]]** - Get up and running
- **[[Quick Start]]** - Your first 5 minutes
- **[[User Guide]]** - Complete usage documentation
- **[[FAQ]]** - Frequently asked questions
- **[[Troubleshooting]]** - Common issues and solutions

## 📖 Documentation Sections

### For Users

- [[Installation]] - Setup instructions
- [[User Guide]] - Feature documentation
- [[Tutorials]] - Step-by-step guides
- [[Recipes]] - Common use cases

### For Developers

- [[Development Setup]] - Contributor environment
- [[Architecture]] - System design
- [[API Reference]] - Programmatic interface
- [[Contributing]] - How to contribute

### For Administrators

- [[Deployment Guide]] - Production deployment
- [[Configuration]] - Settings and options
- [[Monitoring]] - Observability setup
- [[Security]] - Security considerations

## 🆘 Getting Help

- 💬 [[Discussions|https://github.com/org/repo/discussions]] - Ask questions
- 🐛 [[Issues|https://github.com/org/repo/issues]] - Report bugs
- 💡 [[Feature Requests|https://github.com/org/repo/issues/new?template=feature_request.md]] - Suggest features
- 📧 [[Contact]] - Reach the team

## 🤝 Contributing to This Wiki

This wiki is community-maintained. See [[Wiki Contribution Guide]] for how to help improve it.

## 📊 Project Stats

- **Version**: v1.2.3
- **Contributors**: 42
- **Stars**: 1.2k
- **Last Release**: 2025-01-15

## 🔗 External Resources

- [Official Website](https://example.com)
- [Blog](https://blog.example.com)
- [Community Forum](https://forum.example.com)
- [Twitter](https://twitter.com/project)
```

### 2. Installation Guide

**Template**:

````markdown
# Installation

> **Prerequisites**: List what's needed before installation

## Quick Install

The fastest way to get started:

```bash
# One-line install command
curl -sSL https://get.project.com | bash
```
````

## Detailed Installation

### 1. System Requirements

| Component | Minimum                            | Recommended   |
| --------- | ---------------------------------- | ------------- |
| OS        | Linux 4.x, macOS 10.14, Windows 10 | Latest stable |
| RAM       | 2 GB                               | 4 GB          |
| Disk      | 500 MB                             | 2 GB          |
| Network   | Internet connection                | High-speed    |

### 2. Install Dependencies

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y dependency1 dependency2
```

#### macOS

```bash
brew install dependency1 dependency2
```

#### Windows

```powershell
choco install dependency1 dependency2
```

### 3. Install Project

Choose your preferred method:

#### Option A: Package Manager

```bash
npm install -g project-name
# or
pip install project-name
# or
brew install project-name
```

#### Option B: From Source

```bash
git clone https://github.com/org/repo.git
cd repo
make install
```

#### Option C: Download Binary

1. Go to [Releases](https://github.com/org/repo/releases)
1. Download the binary for your OS
1. Extract and add to PATH

### 4. Verify Installation

```bash
project-name --version
# Should output: project-name v1.2.3
```

### 5. Initial Configuration

```bash
project-name init
# Follow the prompts
```

## Platform-Specific Notes

### Linux

- \[Additional Linux setup\]

### macOS

- \[Additional macOS setup\]

### Windows

- \[Additional Windows setup\]

## Docker Installation

```bash
docker pull org/project:latest
docker run -p 8080:8080 org/project
```

See \[\[Docker Guide\]\] for details.

## Troubleshooting Installation

**Problem**: Error message X **Solution**: Do Y

**Problem**: Error message Z **Solution**: Do W

See \[\[Troubleshooting\]\] for more help.

## Next Steps

After installation:

1. \[\[Quick Start\]\] - Get started immediately
1. \[\[Configuration\]\] - Customize your setup
1. \[\[First Tutorial\]\] - Build your first project

````

### 3. Tutorial Template

**Template**:
```markdown
# Tutorial: [Tutorial Name]

> **Level**: Beginner | Intermediate | Advanced
> **Time**: ~30 minutes
> **Prerequisites**: [[Installation]], [[Quick Start]]

## What You'll Learn

By the end of this tutorial, you'll be able to:
- [ ] Learning objective 1
- [ ] Learning objective 2
- [ ] Learning objective 3

## Prerequisites

Before starting, ensure you have:
- Prerequisite 1
- Prerequisite 2
- Prerequisite 3

## Step 1: [First Step]

**Goal**: Explain what this step accomplishes

### Instructions

1. Do this thing
2. Then do this other thing
3. Finally, do this

### Code Example

```language
// Code snippet
const example = "code";
````

### Expected Output

```
Expected output here
```

### ✅ Checkpoint

At this point, you should have:

- [ ] Achievement 1
- [ ] Achievement 2

## Step 2: \[Second Step\]

\[Repeat structure\]

## Step 3: \[Third Step\]

\[Repeat structure\]

## Putting It All Together

Now that we've completed all steps:

```language
// Complete working example
const full = "example";
```

## Next Steps

- \[\[Related Tutorial\]\]
- \[\[Advanced Topic\]\]
- \[\[Reference Documentation\]\]

## Troubleshooting

**Issue**: Common problem\
**Solution**: How to fix

## Additional Resources

- \[External resource 1\]
- \[External resource 2\]

````

### 4. How-To Guide Template

**Template**:
```markdown
# How To: [Task Name]

> **Quick Summary**: One-sentence description of what this guide helps you do

## When to Use This

Use this guide when you need to:
- Scenario 1
- Scenario 2
- Scenario 3

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Quick Solution

For experienced users, here's the TL;DR:

```bash
command-here --options
````

## Detailed Steps

### Method 1: \[Recommended Method\]

**Best for**: Explanation of when to use this method

1. **Step 1**: Explanation

   ```bash
   command
   ```

1. **Step 2**: Explanation

   ```bash
   command
   ```

1. **Step 3**: Explanation

   ```bash
   command
   ```

### Method 2: \[Alternative Method\]

**Best for**: Explanation of when to use this method

\[Same structure as Method 1\]

## Verification

To verify it worked:

```bash
verification-command
```

You should see:

```
Expected output
```

## Common Pitfalls

### Pitfall 1

**Problem**: Description **Solution**: How to avoid

### Pitfall 2

**Problem**: Description **Solution**: How to avoid

## Related How-Tos

- \[\[Related Task 1\]\]
- \[\[Related Task 2\]\]

## See Also

- \[\[Reference Documentation\]\]
- \[\[Troubleshooting\]\]

````

### 5. Reference Documentation Template

**Template**:
```markdown
# [Component] Reference

> **Quick Description**: Brief description of the component

## Overview

High-level overview of what this component does.

## Syntax

````

basic-syntax-pattern

```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param1 | string | Yes | - | Description |
| param2 | number | No | 0 | Description |
| param3 | boolean | No | false | Description |

## Options

### Option 1

**Type**: `string`
**Default**: `"default"`
**Description**: What this option does

**Example**:
```

example-usage

````

### Option 2

[Same structure]

## Return Value

**Type**: `ReturnType`
**Description**: What is returned

## Examples

### Basic Example

```language
// Simple example
code here
````

**Output**:

```
output here
```

### Advanced Example

```language
// Complex example
code here
```

### Real-World Example

```language
// Practical example
code here
```

## Error Handling

| Error Code | Description       | Solution   |
| ---------- | ----------------- | ---------- |
| ERR001     | Error description | How to fix |
| ERR002     | Error description | How to fix |

## Performance Considerations

- Performance tip 1
- Performance tip 2

## Security Considerations

⚠️ **Important Security Note**: Security consideration

## Related

- \[\[Related Component 1\]\]
- \[\[Related Component 2\]\]

## See Also

- External documentation link

````

### 6. FAQ Template

**Template**:
```markdown
# Frequently Asked Questions

> **Search this page**: Use Ctrl/Cmd+F to search for keywords

## Table of Contents

- [General Questions](#general-questions)
- [Technical Questions](#technical-questions)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Business & Licensing](#business--licensing)

## General Questions

### What is [Project]?

[Project] is... [answer]

### Why should I use [Project]?

You should use [Project] if... [answer]

### Is [Project] free?

Yes/No. [Detailed answer with license info]

### Who maintains [Project]?

[Project] is maintained by... [answer]

## Technical Questions

### What technologies does [Project] use?

[Project] is built with:
- Technology 1
- Technology 2
- Technology 3

See [[Architecture]] for details.

### What are the system requirements?

See [[Installation#System-Requirements]] for complete requirements.

### Can I use [Project] with [Other Tool]?

Yes/No. [Explanation and guidance]

### How do I [common task]?

See [[How To: Common Task]] for a complete guide.

## Troubleshooting

### [Project] won't start

**Symptoms**: Describe symptoms
**Cause**: Common causes
**Solution**: Step-by-step solution

See [[Troubleshooting]] for more issues.

### Error: "[Common Error Message]"

**Cause**: Why this happens
**Solution**: How to fix

### Performance is slow

**Possible causes**:
1. Cause 1 - [[Fix]]
2. Cause 2 - [[Fix]]
3. Cause 3 - [[Fix]]

## Contributing

### How can I contribute?

See [[Contributing]] for complete guidelines.

### I found a bug. What should I do?

Please [open an issue](https://github.com/{{ORG_NAME}}/.github/issues/new?template=bug_report.yml)<!-- link:github.bug_report --> with:
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### I have a feature request

Great! Please [open a feature request](https://github.com/{{ORG_NAME}}/.github/issues/new?template=feature_request.yml)<!-- link:github.feature_request --> and describe:
- What problem it solves
- How you envision it working
- Any alternatives you've considered

## Business & Licensing

### What license is [Project] under?

[Project] is licensed under [License]. See [LICENSE](../../LICENSE) for details.

### Can I use [Project] commercially?

Yes/No. [Explanation]

### How can I support the project?

You can support [Project] by:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📖 Improving documentation
- 💰 [[Sponsoring|FUNDING.yml]]

## Still Have Questions?

- 💬 [[Discussions|link]] - Ask the community
- 📧 [[Contact]] - Email the team
- 🐦 [[Twitter|link]] - Follow for updates

---

**Don't see your question?** [Ask it in Discussions](https://github.com/{{ORG_NAME}}/.github/discussions)<!-- link:github.discussions -->
````

### 7. Troubleshooting Guide Template

**Template**:

````markdown
# Troubleshooting Guide

> **Quick Search**: Use Ctrl/Cmd+F to find your issue

## Getting Help

If you can't find your issue here:

1. Search [existing issues](https://github.com/{{ORG_NAME}}/.github/issues)<!-- link:github.issues -->
2. Ask in [Discussions](https://github.com/{{ORG_NAME}}/.github/discussions)<!-- link:github.discussions -->
3. [Open a new issue](https://github.com/{{ORG_NAME}}/.github/issues/new/choose)<!-- link:github.issues_new -->

## Diagnostic Steps

Before troubleshooting specific issues, gather diagnostic information:

```bash
# Check version
project-name --version

# Check configuration
project-name config list

# Run diagnostics
project-name doctor

# Check logs
cat ~/.project/logs/latest.log
```
````

## Common Issues

### Installation Issues

#### Issue: "Command not found"

**Symptoms**: Running `project-name` results in "command not found"

**Causes**:

- Project not installed
- Project not in PATH

**Solutions**:

1. **Verify installation**:

   ```bash
   which project-name
   ```

1. **Add to PATH**:

   ```bash
   export PATH="$PATH:/path/to/project/bin"
   ```

1. **Reinstall**:

   ```bash
   # Reinstall command
   ```

See \[\[Installation\]\] for help.

#### Issue: "Permission denied"

**Symptoms**: Installation fails with permission error

**Solution**:

```bash
# Don't use sudo with package managers
# Instead, fix permissions
sudo chown -R $(whoami) /install/directory
```

### Runtime Issues

#### Issue: "Connection refused"

**Symptoms**: Cannot connect to server

**Diagnosis**:

```bash
# Check if service is running
ps aux | grep project-name

# Check port availability
netstat -an | grep 8080
```

**Solutions**:

1. **Start the service**:

   ```bash
   project-name start
   ```

1. **Check port configuration**:

   ```bash
   project-name config get port
   ```

1. **Check firewall**:

   ```bash
   # Platform-specific firewall commands
   ```

#### Issue: High memory usage

**Symptoms**: System becomes slow, out of memory errors

**Diagnosis**:

```bash
# Check memory usage
project-name stats

# Profile memory
project-name profile --memory
```

**Solutions**:

1. **Increase memory limit**:

   ```bash
   project-name config set max-memory 4GB
   ```

1. **Enable memory optimization**:

   ```bash
   project-name optimize --memory
   ```

1. **Check for memory leaks**: See \[\[Performance Tuning#Memory\]\]

### Configuration Issues

#### Issue: Settings not taking effect

**Symptoms**: Configuration changes don't work

**Checklist**:

- [ ] Configuration file in correct location
- [ ] Correct syntax (YAML, JSON, etc.)
- [ ] Service restarted after changes
- [ ] No conflicting settings

**Debug**:

```bash
# Validate configuration
project-name config validate

# Show loaded configuration
project-name config show
```

## Platform-Specific Issues

### Linux

#### Issue: \[Linux-specific issue\]

\[Solution\]

### macOS

#### Issue: \[macOS-specific issue\]

\[Solution\]

### Windows

#### Issue: \[Windows-specific issue\]

\[Solution\]

## Error Messages

### "Error: ECONNREFUSED"

**Meaning**: Connection was refused by the server

**Common causes**:

1. Service not running
1. Wrong port
1. Firewall blocking

**Solutions**: See \[\[Runtime Issues#Connection refused\]\]

### "Error: ENOENT"

**Meaning**: File or directory not found

**Common causes**:

1. Incorrect file path
1. File doesn't exist
1. Permissions issue

**Solutions**:

```bash
# Check file exists
ls -la /path/to/file

# Check permissions
ls -ld /path/to/directory
```

## Performance Issues

### Slow startup

**Diagnosis**:

```bash
# Profile startup
project-name start --profile
```

**Solutions**:

1. Disable unnecessary plugins
1. Increase startup timeout
1. Check disk I/O

See \[\[Performance Tuning#Startup\]\]

### Slow operations

**Diagnosis**:

```bash
# Enable verbose logging
project-name --verbose operation

# Profile operation
project-name profile operation
```

**Solutions**:

- Enable caching
- Optimize database queries
- Increase resources

## Getting More Help

### Enable Debug Logging

```bash
# Enable debug mode
export DEBUG=*
project-name operation

# Or via config
project-name config set log-level debug
```

### Collect Diagnostic Information

```bash
# Generate diagnostic report
project-name diagnose > diagnostic.txt
```

Include this when asking for help!

### Community Support

- 💬 [Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions) -
  Ask the community
- 🐛 [Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues) - Report
  bugs
- 📧 [Email](mailto:support@example.com) - Private support

## See Also

- \[\[FAQ\]\]
- \[\[Installation\]\]
- \[\[Configuration\]\]
- \[\[Performance Tuning\]\]

````

### 8. Architecture Documentation Template

**Template**:
```markdown
# Architecture Overview

> **Last Updated**: 2025-12-28
> **Status**: Current

## System Overview

[High-level description of the system]

````

┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │ Client │──────▶│ Server
│──────▶│ Database │ └─────────────┘ └─────────────┘ └─────────────┘

```

## Components

### Component 1: [Name]

**Purpose**: What this component does

**Responsibilities**:
- Responsibility 1
- Responsibility 2
- Responsibility 3

**Technologies**:
- Technology A
- Technology B

**Interfaces**:
- Interface 1: Description
- Interface 2: Description

**Dependencies**:
- Depends on Component X
- Depends on Service Y

### Component 2: [Name]

[Same structure]

## Data Flow

```

User Request → API Gateway → Auth Service → Business Logic → Database ↓ Response
← Transform ← Query Result

````

### Request Flow

1. User sends request to API Gateway
2. API Gateway validates and routes
3. Auth Service authenticates request
4. Business Logic processes request
5. Data Layer queries database
6. Response flows back through layers

## Data Models

### Entity 1

```typescript
interface Entity1 {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}
````

**Relationships**:

- Has many Entity2
- Belongs to Entity3

## Infrastructure

### Production Environment

```
┌──────────────────────────────────────────┐
│              Load Balancer                │
└────────────┬────────────┬────────────────┘
             │            │
      ┌──────▼──────┐ ┌──▼──────────┐
      │  Server 1   │ │  Server 2   │
      └──────┬──────┘ └──┬──────────┘
             │            │
        ┌────▼────────────▼─────┐
        │  Database Cluster     │
        └───────────────────────┘
```

### Technology Stack

**Frontend**:

- Framework: React
- State: Redux
- UI: Material-UI

**Backend**:

- Runtime: Node.js
- Framework: Express
- ORM: TypeORM

**Database**:

- Primary: PostgreSQL
- Cache: Redis
- Search: Elasticsearch

**Infrastructure**:

- Cloud: AWS
- Containers: Docker
- Orchestration: Kubernetes

## Security

### Authentication & Authorization

- Authentication: JWT tokens
- Authorization: Role-based access control (RBAC)
- Session: Redis-backed sessions

### Data Protection

- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Secrets management: AWS Secrets Manager

## Scalability

### Horizontal Scaling

- Stateless application servers
- Database read replicas
- Distributed caching

### Performance Optimization

- Caching strategy: Multi-level cache
- Database indexing: See \[\[Database Schema\]\]
- CDN: CloudFront for static assets

## Monitoring & Observability

### Metrics

- Application metrics: Prometheus
- Infrastructure metrics: CloudWatch
- Business metrics: Custom dashboards

### Logging

- Centralized logging: ELK Stack
- Log levels: ERROR, WARN, INFO, DEBUG
- Log retention: 30 days

### Tracing

- Distributed tracing: Jaeger
- APM: New Relic

## Deployment

### CI/CD Pipeline

```
Code → Build → Test → Stage → Production
         ↓      ↓       ↓        ↓
       Static  Unit   Integration  E2E
       Analysis Test    Test      Test
```

### Deployment Strategy

- Strategy: Blue-green deployment
- Rollback: Automated on health check failure
- Canary: 10% traffic for 30 minutes

## Design Decisions

See \[\[Architecture Decision Records\]\] for detailed decision history.

### ADR 001: Why we chose Technology X

**Context**: Problem description

**Decision**: What we decided

**Rationale**: Why we decided this

**Consequences**: Impact of the decision

## Further Reading

- \[\[API Reference\]\]
- \[\[Database Schema\]\]
- \[\[Security Architecture\]\]
- \[\[Deployment Guide\]\]

````

## Maintenance & Governance

### Content Ownership

```markdown
# Wiki Maintenance

## Content Owners

| Section | Owner | Last Review |
|---------|-------|-------------|
| Getting Started | @user1 | 2025-01-15 |
| API Reference | @user2 | 2025-01-10 |
| Troubleshooting | @user3 | 2025-01-20 |

## Review Schedule

- **Monthly**: Home, Installation, Quick Start
- **Quarterly**: Guides, How-Tos
- **Yearly**: Architecture, Reference

## Update Process

1. Make changes
2. Update "Last Updated" date
3. Notify content owner
4. Add to changelog
````

### Quality Standards

**All wiki pages must**:

- [ ] Have clear title
- [ ] Include "Last Updated" date
- [ ] Use proper heading hierarchy (H1 → H2 → H3)
- [ ] Include table of contents for long pages
- [ ] Link to related pages
- [ ] Include examples
- [ ] Be free of spelling/grammar errors

### Style Guide

See \[\[Wiki Style Guide\]\] for:

- Formatting standards
- Voice and tone
- Terminology
- Code block conventions

## Integration with Repository

### Linking Between Wiki and Repo

**From Wiki to Repo**:

```markdown
[README](https://github.com/org/repo/blob/main/README.md)
[Issue #123](https://github.com/org/repo/issues/123)
[Pull Request #456](https://github.com/org/repo/pull/456)
```

**From Repo to Wiki**:

```markdown
[Wiki Home](https://github.com/org/repo/wiki)
[Installation Guide](https://github.com/org/repo/wiki/Installation)
```

### Automated Updates

Use GitHub Actions to:

- Auto-generate API reference from code
- Update version numbers
- Sync changelog
- Validate links

Example workflow:

```yaml
name: Update Wiki
on:
  push:
    branches: [main]
    paths:
      - "docs/**"

jobs:
  sync-wiki:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout wiki
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository }}.wiki

      - name: Update content
        run: |
          # Update wiki content from docs

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Auto-update from repo"
          git push
```

## Migration & Backup

### Backup Strategy

**Manual Backup**:

```bash
# Clone wiki as git repository
git clone https://github.com/org/repo.wiki.git

# Create backup
tar -czf wiki-backup-$(date +%Y%m%d).tar.gz repo.wiki/
```

**Automated Backup**:

```yaml
# .github/workflows/wiki-backup.yml
name: Wiki Backup
on:
  schedule:
    - cron: "0 0 * * 0" # Weekly on Sunday

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Clone wiki
        run: git clone https://github.com/${{ github.repository }}.wiki.git

      - name: Create backup
        run: tar -czf wiki-backup-$(date +%Y%m%d).tar.gz *.wiki/

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: wiki-backup
          path: wiki-backup-*.tar.gz
          retention-days: 90
```

### Migration to Documentation Site

To migrate wiki to a documentation site (MkDocs, Docusaurus, etc.):

```bash
# 1. Clone wiki
git clone https://github.com/org/repo.wiki.git

# 2. Convert wiki markdown to site format
# (May need conversion for internal links)

# 3. Copy to docs site
cp -r repo.wiki/docs/* docs-site/docs/

# 4. Update internal links
find docs-site -name "*.md" -exec sed -i 's/\[\[\(.*\)\]\]/[\1](\1.md)/g' {} \;

# 5. Build and deploy docs site
cd docs-site
mkdocs build
mkdocs gh-deploy
```

## Wiki Search & Discovery

### Search Optimization

**Make content searchable**:

- Use descriptive titles
- Include keywords in first paragraph
- Use proper headings for structure
- Include synonyms and alternate terms

**Search tips**:

```
installation ubuntu      # Multiple keywords
"exact phrase"           # Exact match
installation -windows    # Exclude term
```

### Cross-Linking Strategy

**Every page should link to**:

- Related pages (at least 2-3)
- Parent/overview page
- Next logical page
- Home page (via sidebar)

**Link text best practices**:

- ✅ "See \[\[Installation Guide\]\]"
- ✅ "Learn about \[\[API Authentication\]\]"
- ❌ "Click \[\[here\]\]"
- ❌ "\[\[Link\]\]"

## Resources

- [GitHub Wiki Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis)<!-- link:docs.github_wikis -->
- [Markdown Guide](https://www.markdownguide.org/)
- \[\[Documentation Standards\]\]
- \[\[Style Guide\]\]

______________________________________________________________________

**Last Updated**: 2025-12-28\
**Maintained By**: @{{ORG_NAME}} documentation
team

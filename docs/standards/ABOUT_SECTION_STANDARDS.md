# About Section Standards

## Overview

This document defines the standards for repository "About" sections across the
{{ORG_NAME}} organization. A complete About section is essential for
discoverability, professionalism, and clear communication of a repository's
purpose.

## Required Elements

Every repository must have a complete About section that includes:

### 1. Repository Description

**Location**: Repository Settings → General → Description

**Requirements**:

- **Length**: 50-160 characters (ideal for GitHub's display)
- **Clarity**: Clear, concise, and descriptive
- **Accuracy**: Accurately reflects the repository's purpose
- **Keywords**: Includes 2-3 key terms for searchability

**Format**:

```
[What it is] - [What it does] - [Key benefit/feature]
```

**Examples**:

- ✅ **Good**: "Organization policies repository - Community health files, AI
  framework (26+ agents), and workflow automation for the {{ORG_NAME}}
  organization"
- ✅ **Good**: "Python automation toolkit - Streamlines CI/CD workflows with
  pre-built GitHub Actions templates"
- ❌ **Bad**: "My project" (too vague)
- ❌ **Bad**: "This is a repository for storing code" (not descriptive)

### 2. Website URL

**Location**: Repository Settings → General → Website

**Requirements**:

- Link to primary documentation, demo, or project homepage
- Must be HTTPS
- Must be functional and maintained
- Prefer organization-owned domains when available

**Priority Order**:

1. Official project documentation site
1. GitHub Pages site
1. Live demo/application
1. Organization website
1. Related documentation

**Examples**:

- ✅ `https://docs.example.com`
- ✅ `https://demo.example.com`
- ✅ `https://{{ORG_NAME}}.github.io/project-name`

### 3. Topics (Tags)

**Location**: Repository Settings → General → Topics

**Requirements**:

- **Minimum**: 3 topics
- **Maximum**: 20 topics (GitHub limit)
- **Recommended**: 5-10 topics for optimal discoverability

**Topic Categories**:

1. **Primary Technology** (1-2 topics)

   - Programming language: `python`, `typescript`, `javascript`, `go`, `rust`
   - Framework/platform: `nodejs`, `react`, `docker`, `github-actions`

1. **Purpose/Domain** (2-3 topics)

   - `automation`, `ci-cd`, `devops`, `documentation`, `governance`
   - `security`, `testing`, `deployment`, `monitoring`

1. **Organization/Type** (1-2 topics)

   - `github-organization`, `community-health`, `workflow-templates`
   - `ai-framework`, `mcp-server`, `github-app`

1. **Features/Capabilities** (1-3 topics)

   - `pre-commit-hooks`, `code-quality`, `automated-testing`
   - `schema-org`, `semantic-versioning`, `project-management`

**Examples**:

```yaml
# Good topic sets
Repository: .github
Topics:
  - github
  - organization-policies
  - community-health
  - ai-framework
  - automation
  - workflows
  - governance
  - documentation

Repository: python-automation-toolkit
Topics:
  - python
  - automation
  - ci-cd
  - github-actions
  - devops
  - workflow-templates
```

### 4. Social Preview Image

**Location**: Repository Settings → General → Social preview

**Requirements**:

- **Dimensions**: 1280×640px (2:1 aspect ratio)
- **Format**: PNG or JPG
- **File size**: Under 1MB
- **Content**:
  - Repository name or logo
  - Brief tagline or key feature
  - Organization branding (if applicable)
  - High contrast for readability

**When to Set**:

- ✅ Required for all public repositories
- ✅ Required for flagship/showcase repositories
- ⚠️ Optional for internal tooling repositories
- ⚠️ Optional for archived repositories

### 5. Ontological Title

**Definition**: A structured, semantic title that clearly defines what the
repository IS in ontological terms (its essence and classification).

**Location**:

- Repository name (GitHub URL)
- `name` field in `.schema-org/repository.jsonld`
- Documented in README.md frontmatter or header

**Format**:

```
[Domain/Category] [Type] [Specific Purpose]
```

**Requirements**:

- **Clarity**: Immediately conveys what the thing IS, not just what it does
- **Classification**: Places the repository in a clear category/domain
- **Specificity**: Distinguishes from similar repositories
- **Consistency**: Follows organization-wide naming patterns

**Examples**:

| Repository Name           | Ontological Title                    | Explanation                                         |
| ------------------------- | ------------------------------------ | --------------------------------------------------- |
| `.github`                 | "Organization Governance Repository" | It IS a governance repository (not just "policies") |
| `python-ci-toolkit`       | "Python CI/CD Automation Library"    | It IS a library (not just "toolkit")                |
| `react-component-library` | "React UI Component Library"         | It IS a component library (specific type)           |
| `api-gateway-service`     | "Microservice API Gateway"           | It IS a microservice (architectural type)           |
| `docs-site`               | "Technical Documentation Portal"     | It IS a portal (not just "site")                    |

**Ontological Title Hierarchy**:

1. **Primary Classification** (What domain/category?)

   - Library, Framework, Application, Service, Tool, Repository, Portal, System

1. **Technology/Language** (What technology stack?)

   - Python, TypeScript, React, Docker, Kubernetes, GitHub

1. **Function/Purpose** (What specific purpose?)

   - CI/CD, Testing, Monitoring, Documentation, Authentication, Data Processing

**Bad Examples** (Too vague/unclear):

- ❌ "Utilities" (What kind? What domain?)
- ❌ "Helper Functions" (Too generic)
- ❌ "Project" (Not descriptive at all)
- ❌ "Code" (Meaningless classification)

## Validation Checklist

Use this checklist to ensure About section completeness:

### Pre-Deployment Checklist

- [ ] **Description**: 50-160 characters, clear and keyword-rich
- [ ] **Website URL**: Set, functional, HTTPS, and relevant
- [ ] **Topics**: 5-10 topics covering technology, purpose, and features
- [ ] **Social Preview**: Custom image set (for public repos)
- [ ] **Ontological Title**: Defined in schema.org and documentation
- [ ] **README.md**: Reflects the ontological title and About info
- [ ] **LICENSE**: Present and matches About section claims

### Audit Process

Run automated audit:

```bash
# Using the Completionism Specialist workflow
gh workflow run bio-description-completions.yml

# Or manually check with GitHub CLI
gh repo view --json description,url,topics,openGraphImageUrl
```

### Quarterly Review

- [ ] Description still accurate
- [ ] Website URL still functional
- [ ] Topics still relevant (remove outdated, add new)
- [ ] Social preview still represents the project
- [ ] Ontological title still accurate

## Integration with Other Standards

### Schema.org Integration

The About section metadata should be synchronized with
`.schema-org/repository.jsonld`:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareSourceCode",
  "name": "[Ontological Title]",
  "alternateName": "[Repository Name]",
  "description": "[Repository Description]",
  "url": "[Website URL]",
  "keywords": ["topic1", "topic2", "topic3"],
  "image": "[Social Preview URL]"
}
```

### README Integration

The README.md should reflect About section information:

```markdown
# [Repository Name]

> **Ontological Title**: [Title from About section]

[Repository Description]

**Topics**: `topic1` `topic2` `topic3` `topic4` `topic5`

**Website**: [URL]
```

## Enforcement

### Automated Checks

1. **Bio-Description Completions Workflow**

   - Runs weekly on all repositories
   - Flags incomplete About sections
   - Creates GitHub issues for resolution

1. **Pre-commit Hooks** (repository-level)

   - Validates schema.org synchronization
   - Checks README matches About metadata

1. **Completionism Specialist Agent**

   - Audits all repositories quarterly
   - Provides comprehensive completion reports

### Manual Review

1. **New Repository Setup**

   - About section completed before first release
   - Verified in `docs/REPOSITORY_SETUP_CHECKLIST.md`

1. **Repository Transfers**

   - About section updated to reflect new ownership
   - Topics updated for new organizational context

1. **Major Version Releases**

   - Description updated if purpose has evolved
   - Topics refreshed to reflect current capabilities

## Resources

### Related Documentation

- [Repository Setup Checklist](../runbooks/REPOSITORY_SETUP_CHECKLIST.md)
- [README Template Standards](./README_TEMPLATE_STANDARDS.md)
- [Schema.org Implementation Guide](../guides/SCHEMA_ORG_SEMVER_GUIDE.md)
- [Completionism Specialist Agent](../../src/ai_framework/agents/completionism-specialist.agent.md)

### Tools

- **GitHub CLI**:
  `gh repo edit --description "..." --homepage "..." --topics "topic1,topic2"`
- **Schema.org Validator**: `python scripts/validate-schema-org.py`
- **Metadata Sync Script**: `npm run sync:metadata`

### Examples

See these repositories for reference:

- [{{ORG_NAME}}/.github](https://github.com/%7B%7BORG_NAME%7D%7D/.github)<!-- link:github.dotgithub -->
  \- Organization policies
- [Example compliance-complete repo](https://github.com/%7B%7BORG_NAME%7D%7D/) -
  Full example

______________________________________________________________________

**Version**: 1.0.0\
**Last Updated**: 2026-01-21\
**Maintained By**:
Organization Governance Team\
**Questions?**
[Open a Discussion](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->

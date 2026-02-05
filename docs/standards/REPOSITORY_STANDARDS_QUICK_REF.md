# Repository Standards Quick Reference

> **Quick guide to About sections, ontological titles, and README structure**

## 🎯 At a Glance

Every repository must have:

1. **Complete About Section** (GitHub Settings)
1. **Ontological Title** (What it IS, not just what it does)
1. **README with Problem → Approach → Outcome** narrative

______________________________________________________________________

## 📋 About Section Checklist

Configure in **Repository Settings → General**:

### ✅ Description

- **Length**: 50-160 characters
- **Format**: `[What it is] - [What it does] - [Key benefit]`
- **Example**:
  `"Python CI/CD library - Streamlines workflows with pre-built templates"`

### ✅ Website URL

- Link to docs, demo, or homepage
- Must be HTTPS and functional
- **Example**: `https://docs.example.com`

### ✅ Topics (5-10 recommended)

```yaml
Categories:
  - Primary Tech: python, typescript, javascript
  - Purpose: automation, ci-cd, documentation
  - Type: library, framework, service
  - Features: github-actions, pre-commit-hooks
```

### ✅ Social Preview (Public Repos)

- **Size**: 1280×640px (2:1 ratio)
- **Format**: PNG or JPG, under 1MB
- Includes repo name, tagline, branding

### ✅ Ontological Title

- **Location**: Schema.org file, README header
- **Format**: `[Domain] [Type] [Purpose]`
- **Example**: `"Python CI/CD Automation Library"`

______________________________________________________________________

## 🏷️ Ontological Title Guide

### What It Is

A semantic classification that defines what the repository **IS** (its essence),
not just what it does.

### Format

```
[Domain/Category] [Type] [Specific Purpose]
```

### Examples

| Repo Name        | ❌ Bad Title    | ✅ Good Title (Ontological)          |
| ---------------- | --------------- | ------------------------------------ |
| `python-toolkit` | "Toolkit"       | "Python CI/CD Automation Library"    |
| `.github`        | "Policies"      | "Organization Governance Repository" |
| `api-gateway`    | "Gateway"       | "Microservice API Gateway"           |
| `docs-site`      | "Documentation" | "Technical Documentation Portal"     |

### Title Hierarchy

1. **Classification**: Library, Framework, Application, Service, Tool,
   Repository, Portal, System
1. **Technology**: Python, TypeScript, React, Docker, Kubernetes
1. **Purpose**: CI/CD, Testing, Monitoring, Documentation, Authentication

### Where to Use It

- `.schema-org/repository.jsonld` → `identifier.value`
- `README.md` → Header metadata
- Repository documentation

______________________________________________________________________

## 📄 README Structure

Every README must follow this structure:

```markdown
# [Project Name]

> **Ontological Title**: [Semantic classification]

[Badges]

[One-sentence description]

---

## 📋 Problem
[What problem does this solve? Why does it exist?]

## 🎯 Approach
[How does this solve it? What's the strategy?]

## ✨ Outcome
[What can users achieve? What are the results?]

---

## 🚀 Quick Start
[5 steps maximum to first success]

## 📚 Documentation
[Links to detailed docs]

## 🤝 Contributing
[How to contribute]

## 📄 License
[License info]
```

### The Problem → Approach → Outcome Framework

#### 📋 Problem (2-4 paragraphs)

- **The Challenge**: Describe the pain point
- **Why It Matters**: Explain the impact
- **Current Limitations**: What's missing?

#### 🎯 Approach (2-4 paragraphs)

- **Solution Overview**: High-level strategy
- **Key Features**: How features address the problem
- **Architecture**: Technical approach (optional)

#### ✨ Outcome (2-4 paragraphs)

- **What You Get**: Immediate benefits
- **Real-World Impact**: Concrete examples with metrics
- **Success Metrics**: Quantifiable improvements

______________________________________________________________________

## 🚀 Quick Commands

### Update Repository About Section

```bash
# Set description, homepage, and topics
gh repo edit \
  --description "Your 50-160 char description" \
  --homepage "https://your-site.com" \
  --add-topic "topic1" \
  --add-topic "topic2" \
  --add-topic "topic3"
```

### Check Current Settings

```bash
# View current metadata
gh repo view --json description,url,topics,openGraphImageUrl

# Verify repository.jsonld
cat .schema-org/repository.jsonld | jq
```

### Validate Standards Compliance

```bash
# Run schema.org validation
python scripts/validate-schema-org.py

# Check README structure (if script exists)
npm run lint:markdown

# Run completionism audit
gh workflow run bio-description-completions.yml
```

### Create README from Template

```bash
# Copy minimal template
cp docs/templates/README-minimal.md README.md

# Edit with your project info
$EDITOR README.md
```

______________________________________________________________________

## 📊 Compliance Checklist

Use this before finalizing a new repository:

- [ ] **Description**: 50-160 chars, clear, keyword-rich
- [ ] **Website**: Set, HTTPS, functional
- [ ] **Topics**: 5-10 topics covering tech, purpose, features
- [ ] **Social Preview**: Custom image (if public repo)
- [ ] **Ontological Title**: Defined in schema.org
- [ ] **Ontological Title**: In README header
- [ ] **README Problem Section**: Complete with 2-4 paragraphs
- [ ] **README Approach Section**: Complete with 2-4 paragraphs
- [ ] **README Outcome Section**: Complete with 2-4 paragraphs
- [ ] **Quick Start**: Maximum 5 steps
- [ ] **Documentation Links**: All functional
- [ ] **License**: Present and correct
- [ ] **Contributing**: Link to CONTRIBUTING.md
- [ ] **Code of Conduct**: Link to CODE_OF_CONDUCT.md

______________________________________________________________________

## 📚 Full Documentation

- **[About Section Standards](standards/ABOUT_SECTION_STANDARDS.md)** - Complete
  guide (9,000+ words)
- **[README Template Standards](standards/README_TEMPLATE_STANDARDS.md)** -
  Complete guide (16,000+ words)
- **[README Minimal Template](templates/README-minimal.md)** - Basic template
- **[Repository Setup Checklist](REPOSITORY_SETUP_CHECKLIST.md)** - Complete
  setup guide

______________________________________________________________________

## 🎯 Examples

### Well-Formed About Section

```yaml
Description: "Organization policies repository - Community health files, AI framework (26+ agents), and workflow automation"
Website: "https://github.com/ivviiviivvi/.github"
Topics:
  - github
  - organization-policies
  - community-health
  - ai-framework
  - automation
  - workflows
  - governance
  - documentation
Ontological Title: "Organization Governance Repository"
```

### Well-Formed README Header

```markdown
# .github

> **Ontological Title**: Organization Governance Repository

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](actions)

Organization policies repository - Community health files, AI framework (26+ agents), and workflow automation

---

## 📋 Problem

### The Challenge

Managing organization-wide policies and community health files across...
```

______________________________________________________________________

## ❓ FAQ

### Q: Why do we need an ontological title?

**A**: It provides semantic clarity about what something **IS** (its essence and
classification), making it immediately understandable to both humans and AI
tools. "Utilities" is vague; "Python CI/CD Automation Library" is clear.

### Q: Can I skip the Problem → Approach → Outcome structure?

**A**: No, it's required for all repositories. This narrative framework ensures
every README tells a complete story that's easy to understand and follow.

### Q: What if my repository doesn't have metrics for the Outcome section?

**A**: Focus on qualitative benefits and use cases. As you gather data, add
quantitative metrics in future updates.

### Q: How often should I review these standards?

**A**: Review About section quarterly. Update README when purpose evolves or
major features are added.

### Q: Who enforces these standards?

**A**: Automated checks (Completionism Specialist workflow, pre-commit hooks)
flag issues. Repository setup checklist ensures compliance for new repos.

______________________________________________________________________

## 🆘 Need Help?

- **Questions?**
  [Open a Discussion](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->
- **Issues?**
  [Report a Problem](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->
- **Documentation**: See [Full Standards](standards/)

______________________________________________________________________

**Version**: 1.0.0\
**Last Updated**: 2026-01-21\
**Maintained By**:
Organization Governance Team

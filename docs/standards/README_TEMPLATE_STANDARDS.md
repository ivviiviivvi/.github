# README Template Standards

## Overview

This document defines the standard README structure for all repositories in the
{{ORG_NAME}} organization. Every README must follow the **Problem → Approach →
Outcome** narrative framework to ensure clarity, consistency, and effective
communication.

## The Problem → Approach → Outcome Framework

### Core Principle

Every README should tell a complete story that answers three fundamental
questions:

1. **Problem**: What problem does this solve? Why does it exist?
1. **Approach**: How does this solve the problem? What's the method/strategy?
1. **Outcome**: What can users achieve? What are the results/benefits?

### Why This Framework?

- **Clarity**: Readers immediately understand the purpose and value
- **Context**: Provides the "why" before the "how"
- **Engagement**: Creates a narrative that readers can follow
- **Professionalism**: Demonstrates thoughtful design and clear communication
- **Discoverability**: Search engines and AI tools can better understand the
  content

## README Structure

### Required Sections

Every README must include these sections in this order:

```markdown
# [Project Name]

> **Ontological Title**: [Semantic classification - see ABOUT_SECTION_STANDARDS.md]

[![Badges Section - Status, Version, etc.]]

[Brief one-sentence description matching the repository About section]

---

## 📋 Problem

[2-4 paragraphs describing the problem this project addresses]

## 🎯 Approach

[2-4 paragraphs describing how this project solves the problem]

## ✨ Outcome

[2-4 paragraphs describing what users can achieve with this project]

---

## 🚀 Quick Start

[Minimal steps to get started - 3-5 steps maximum]

## 📚 Documentation

[Links to detailed documentation]

## 🤝 Contributing

[Link to CONTRIBUTING.md or brief contribution guidelines]

## 📄 License

[License information with link to LICENSE file]

---

**Version**: [Current Version]  
**Last Updated**: [Date]  
**Maintained By**: [Team/Organization]
```

## Detailed Section Guidelines

### 1. Header Section

```markdown
# [Project Name]

> **Ontological Title**: [Semantic classification]

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

[One-sentence description - matches repository About section]
```

**Requirements**:

- Project name matches repository name
- Ontological title clearly states what this IS (not just what it does)
- Badges are functional and relevant (version, license, build status minimum)
- One-sentence description is identical to repository description

**Example**:

```markdown
# python-automation-toolkit

> **Ontological Title**: Python CI/CD Automation Library

[![Version](https://img.shields.io/badge/version-2.1.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/org/repo/ci.yml)](https://github.com/org/repo/actions)

Python automation toolkit - Streamlines CI/CD workflows with pre-built GitHub Actions templates
```

### 2. Problem Section

**Purpose**: Explain the pain point, gap, or need that motivated this project.

**Structure**:

```markdown
## 📋 Problem

### The Challenge

[1-2 paragraphs describing the problem domain and current pain points]

### Why It Matters

[1-2 paragraphs explaining the impact and importance of solving this problem]

### Current Limitations

[Optional: Bullet points of existing solution limitations, if relevant]
```

**Guidelines**:

- Start with the user's perspective
- Be specific about the problem
- Avoid solutions in this section (save for Approach)
- Use empathy and understanding
- Connect to reader's likely experiences

**Example**:

```markdown
## 📋 Problem

### The Challenge

Setting up consistent CI/CD workflows across multiple Python projects is time-consuming and error-prone. Development teams often copy-paste workflow configurations between projects, leading to inconsistencies, outdated practices, and maintenance nightmares. When a security vulnerability or best practice update emerges, teams must manually update dozens of workflows across their repositories.

### Why It Matters

Inconsistent CI/CD configurations lead to:
- **Security vulnerabilities** from outdated dependency scanning
- **Wasted time** debugging workflow failures
- **Inconsistent quality** across projects
- **Slow onboarding** for new projects
- **Technical debt** that compounds over time

For organizations managing 10+ Python repositories, this problem multiplies exponentially, consuming hundreds of developer hours annually.
```

### 3. Approach Section

**Purpose**: Explain HOW this project solves the problem - the strategy,
architecture, and key features.

**Structure**:

```markdown
## 🎯 Approach

### Solution Overview

[1-2 paragraphs describing the high-level approach and core strategy]

### Key Features

- **Feature 1**: [Brief description of feature and how it addresses the problem]
- **Feature 2**: [Brief description]
- **Feature 3**: [Brief description]

### Architecture/Design

[Optional: 1-2 paragraphs on technical approach, architecture, or design decisions]
```

**Guidelines**:

- Focus on strategy, not implementation details
- Explain design decisions and trade-offs
- Highlight what makes this approach unique or effective
- Connect features back to the problem
- Use clear, jargon-free language when possible

**Example**:

```markdown
## 🎯 Approach

### Solution Overview

The Python Automation Toolkit provides a curated library of reusable GitHub Actions workflows designed specifically for Python projects. Instead of writing workflows from scratch, teams can import pre-built, battle-tested workflows that follow current best practices. Each workflow is parameterized for customization while maintaining consistent core functionality.

### Key Features

- **Reusable Workflows**: Import tested workflows with a single line, reducing configuration time from hours to minutes
- **Automatic Updates**: Central workflow maintenance means security patches and improvements propagate automatically
- **Smart Defaults**: Sensible configurations work out-of-the-box for 80% of use cases
- **Flexible Customization**: Override any parameter to meet specific project needs
- **Comprehensive Testing**: Pre-commit hooks, unit tests, integration tests, and security scanning included
- **Documentation Integration**: Automatic documentation generation and deployment

### Architecture

Built on GitHub Actions' reusable workflow feature, the toolkit centralizes workflow definitions in a single repository. Projects reference these workflows using the `uses` keyword, creating a single source of truth. Version pinning ensures stability while allowing opt-in updates.
```

### 4. Outcome Section

**Purpose**: Describe what users can ACHIEVE - the concrete results, benefits,
and capabilities.

**Structure**:

```markdown
## ✨ Outcome

### What You Get

[1-2 paragraphs describing the immediate benefits and capabilities]

### Real-World Impact

[1-2 paragraphs with specific examples, metrics, or use cases]

### Success Metrics

[Optional: Quantifiable improvements - time saved, errors reduced, etc.]
```

**Guidelines**:

- Focus on user benefits, not features
- Use concrete examples and specific scenarios
- Include metrics when available (time saved, errors prevented, etc.)
- Paint a picture of success
- Connect back to the original problem

**Example**:

```markdown
## ✨ Outcome

### What You Get

With the Python Automation Toolkit, teams can set up comprehensive CI/CD for a new Python project in under 5 minutes. Simply add a single workflow file that references the toolkit, and your project immediately gets: automated testing on every push, security scanning, code quality checks, dependency updates, and one-command deployments.

### Real-World Impact

Organizations using the toolkit report:
- **90% reduction** in time spent on CI/CD setup (from 4 hours to 20 minutes per project)
- **Zero security vulnerabilities** from outdated scanning tools
- **Consistent quality** across all Python repositories
- **Faster onboarding** for new projects (minutes vs. days)
- **Reduced maintenance burden** (update once, deploy everywhere)

Example: A team managing 15 Python microservices reduced their annual CI/CD maintenance from an estimated 200 developer hours to less than 20 hours - a 10x improvement.

### Success Metrics

- ⚡ **95% faster setup** compared to manual workflow creation
- 🛡️ **100% consistency** across all projects using the toolkit
- 📉 **85% fewer workflow-related issues** in production
- 🎯 **Zero configuration** needed for standard Python projects
```

### 5. Quick Start Section

**Purpose**: Get users to their first success as quickly as possible.

**Requirements**:

- Maximum 5 steps
- Each step is a single, clear action
- Assumes minimal prior knowledge
- Links to detailed docs for next steps

**Structure**:

````markdown
## 🚀 Quick Start

Get up and running in 5 minutes:

1. **Install/Setup**
   ```bash
   [Single command to install or setup]
````

2. **Configure**

   ```bash
   [Minimal required configuration]
   ```

1. **Run/Deploy**

   ```bash
   [Command to run or deploy]
   ```

1. **Verify**

   ```bash
   [How to confirm it's working]
   ```

1. **Next Steps**

   - \[Link to detailed docs\]
   - \[Link to examples\]
   - \[Link to tutorials\]

**Need help?** See [Documentation](#-documentation) or [open an issue](link).

````

**Example**:
```markdown
## 🚀 Quick Start

Get up and running in 5 minutes:

1. **Create workflow file**
   ```bash
   mkdir -p .github/workflows
   touch .github/workflows/ci.yml
````

2. **Add toolkit reference**

   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on: [push, pull_request]
   jobs:
     test:
       uses: {{ORG_NAME}}/python-automation-toolkit/.github/workflows/python-ci.yml@v2
   ```

1. **Commit and push**

   ```bash
   git add .github/workflows/ci.yml
   git commit -m "Add CI workflow"
   git push
   ```

1. **Watch it run**

   - Go to Actions tab in your repository
   - See your tests running automatically

1. **Customize (optional)**

   - See [Configuration Guide](docs/CONFIGURATION.md) for parameters
   - See [Examples](examples/) for common customizations

**Need help?** Check our [Documentation](docs/) or
[open an issue](https://github.com/%7B%7BORG_NAME%7D%7D/python-automation-toolkit/issues).

````

### 6. Documentation Section

**Purpose**: Point to detailed documentation and resources.

**Structure**:
```markdown
## 📚 Documentation

### Core Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Detailed setup guide
- **[Configuration Reference](docs/CONFIGURATION.md)** - All configuration options
- **[API Documentation](docs/API.md)** - Full API reference (if applicable)
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Technical deep dive

### Additional Resources

- **[Examples](examples/)** - Real-world usage examples
- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Changelog](CHANGELOG.md)** - Version history and updates
- **[Roadmap](docs/ROADMAP.md)** - Future plans and features

### Community

- [GitHub Discussions](link) - Ask questions and share ideas
- [Contributing Guide](../governance/CONTRIBUTING.md) - How to contribute
- [Code of Conduct](../governance/CODE_OF_CONDUCT.md) - Community standards
````

### 7. Contributing Section

**Structure**:

````markdown
## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: [Open an issue](link) for bugs or feature requests
2. **Submit PRs**: Fork, create a branch, and submit a pull request
3. **Improve Docs**: Documentation improvements are always appreciated
4. **Share Feedback**: Tell us what's working and what's not

See our [Contributing Guide](../governance/CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/org/repo.git
cd repo

# Install dependencies
[installation commands]

# Run tests
[test commands]
````

**Code of Conduct**: Please read and follow our
[Code of Conduct](../governance/CODE_OF_CONDUCT.md).

````

### 8. License Section

**Structure**:
```markdown
## 📄 License

This project is licensed under the [MIT License](../../LICENSE).

Copyright © 2026 [Organization Name]
````

### 9. Footer Section

**Structure**:

```markdown
---

**Version**: 1.0.0  
**Last Updated**: 2026-01-21  
**Maintained By**: [Team Name or Organization]  
**Questions?** [Open a Discussion](link) | [Report an Issue](link) | [View Documentation](link)
```

## README Quality Checklist

Use this checklist to ensure your README meets standards:

### Narrative Flow

- [ ] Problem section explains the pain point clearly
- [ ] Approach section describes the solution strategy
- [ ] Outcome section demonstrates concrete benefits
- [ ] Narrative flows logically from problem to outcome

### Completeness

- [ ] All required sections are present
- [ ] Ontological title is defined
- [ ] Badges are functional and relevant
- [ ] Quick Start is under 5 steps
- [ ] Documentation links are valid

### Quality

- [ ] Free of typos and grammatical errors
- [ ] Code examples are tested and working
- [ ] Links are functional and up-to-date
- [ ] Formatting is consistent
- [ ] Images/diagrams (if any) are clear and relevant

### Accessibility

- [ ] Clear headings hierarchy (H1 → H2 → H3)
- [ ] Alt text for images
- [ ] Code blocks have language specified
- [ ] Links have descriptive text

### Maintenance

- [ ] Version number is current
- [ ] Last updated date is accurate
- [ ] Changelog is linked
- [ ] Contact/support information is current

## Anti-Patterns to Avoid

### ❌ Don't Do This:

1. **Starting with installation** (Start with problem/context)
1. **Feature lists without context** (Explain why features matter)
1. **Technical jargon without explanation** (Use clear language)
1. **Missing the "why"** (Always explain purpose and value)
1. **Outdated information** (Keep README current with code)
1. **Generic or vague descriptions** (Be specific and concrete)
1. **Missing quick start** (Users need a fast path to success)
1. **Broken links or examples** (Test everything before committing)

### ✅ Do This Instead:

1. **Lead with problem and context**
1. **Explain features with benefits**
1. **Use clear, jargon-free language**
1. **Always include the "why"**
1. **Keep documentation synced with code**
1. **Use specific examples and metrics**
1. **Provide multiple entry points** (quick start, deep dive docs)
1. **Test all links and examples**

## Examples

### Minimal README Template

See [docs/templates/README-minimal.md](../templates/README-minimal.md)

### Comprehensive README Template

See
[docs/templates/README-comprehensive.md](../templates/README-comprehensive.md)

### Real-World Examples

- [{{ORG_NAME}}/.github](https://github.com/%7B%7BORG_NAME%7D%7D/.github)<!-- link:github.dotgithub -->
  \- Organization policies (comprehensive)
- [Example: python-toolkit](link) - Python library (standard)
- [Example: microservice](link) - Service/application (service-focused)

## Tools and Automation

### Validation

```bash
# Check README structure
python scripts/validate-readme.py

# Lint markdown
npm run lint:markdown

# Check links
npm run check-links
```

### Templates

```bash
# Create new README from template
npm run create:readme [template-type]

# Available templates: minimal, standard, comprehensive
```

## Resources

### Related Documentation

- [About Section Standards](./ABOUT_SECTION_STANDARDS.md)
- [Schema.org Implementation](../guides/SCHEMA_ORG_SEMVER_GUIDE.md)
- [Repository Setup Checklist](../runbooks/REPOSITORY_SETUP_CHECKLIST.md)

### Tools

- [Markdown Linter](https://github.com/DavidAnson/markdownlint)
- [Link Checker](https://github.com/tcort/markdown-link-check)
- [Badge Generator](https://shields.io/)

### Further Reading

- [Art of README](https://github.com/hackergrrl/art-of-readme)
- [Make a README](https://www.makeareadme.com/)
- [Awesome README](https://github.com/matiassingers/awesome-readme)

______________________________________________________________________

**Version**: 1.0.0\
**Last Updated**: 2026-01-21\
**Maintained By**:
Organization Governance Team\
**Questions?**
[Open a Discussion](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->

# Custom Instructions Setup Guide

> **Complete guide to configuring and using GitHub Copilot custom instructions
> for consistent, high-quality code**

## Table of Contents

- [Overview](#overview)
- [What Are Custom Instructions?](#what-are-custom-instructions)
- [Benefits](#benefits)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Methods](#installation-methods)
- [Available Instructions](#available-instructions)
  - [By Category](#by-category)
  - [By Technology](#by-technology)
- [How Instructions Work](#how-instructions-work)
- [Using Instructions](#using-instructions)
- [Creating Custom Instructions](#creating-custom-instructions)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

______________________________________________________________________

## Overview

Custom instructions enable GitHub Copilot to follow your organization's coding
standards, best practices, and architectural patterns automatically. When you
work on files that match specified patterns, Copilot applies the relevant
instructions to generate code that aligns with your team's conventions.

This guide covers:

- Understanding how custom instructions enhance Copilot
- Installing and configuring instructions for your projects
- Leveraging the 100+ instructions available in this organization
- Creating your own custom instructions

______________________________________________________________________

## What Are Custom Instructions?

**Custom Instructions** are files that tell GitHub Copilot about:

- **Coding standards**: Style guidelines, naming conventions, formatting rules
- **Best practices**: Security patterns, performance optimizations, error
  handling
- **Framework conventions**: How to use specific libraries and frameworks
- **Architectural patterns**: Project structure, design patterns, module
  organization
- **Technology-specific rules**: Language idioms, ecosystem tools, testing
  approaches

### Key Features

- **Automatic Application**: Instructions apply based on file patterns (e.g.,
  all `.py` files get Python instructions)
- **Context-Aware**: Different instructions for different parts of your codebase
- **Cumulative**: Multiple instructions can apply to the same file
- **Organization-Wide**: Share standards across all repositories
- **Flexible**: Override at repository or project level

______________________________________________________________________

## Benefits

### For Developers

- **Consistent Code Quality**: Copilot generates code following your standards
- **Faster Onboarding**: New team members learn patterns through generated code
- **Reduced Review Time**: Less back-and-forth on style and convention issues
- **Better Suggestions**: More relevant completions based on your practices

### For Teams

- **Standardization**: Enforce coding standards across the organization
- **Knowledge Sharing**: Codify best practices in reusable instructions
- **Quality Assurance**: Reduce bugs through consistent patterns
- **Productivity**: Less time discussing style, more time building features

### For Organizations

- **Governance**: Ensure compliance with security and quality standards
- **Scalability**: Apply best practices automatically as teams grow
- **Maintainability**: Consistent codebases are easier to maintain
- **Training**: Built-in teaching tool for best practices

______________________________________________________________________

## Getting Started

### Prerequisites

Before setting up custom instructions, ensure you have:

1. **GitHub Copilot** subscription (Individual, Business, or Enterprise)
1. **VS Code** or **VS Code Insiders** (version 1.80 or later)
1. **GitHub Copilot Extension** installed and activated
1. **Repository access** to this `.github` organization repository

### Installation Methods

#### Option 1: Quick Install via URL (Recommended)

Each instruction file has an "Install in VS Code" badge that automatically
installs it:

1. Browse the
   [`instructions/`](https://github.com/github/awesome-copilot/tree/main/instructions/)<!-- link:github.awesome_copilot_instructions -->
   directory
1. Open an instruction file (e.g., `python.instructions.md`)
1. Click the **"Install in VS Code"** badge at the top
1. Follow the VS Code prompts to complete installation

**Example badges:**

- ![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square)
- ![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square)

#### Option 2: Repository-Level Installation

To apply instructions to a specific repository:

1. **Create instructions directory** in your repository:

   ```bash
   mkdir -p .github/copilot-instructions
   ```

1. **Copy instruction files**:

   ```bash
   # Copy all instructions
   cp /path/to/.github/instructions/*.instructions.md .github/copilot-instructions/

   # Or copy specific instructions
   cp /path/to/.github/instructions/python.instructions.md .github/copilot-instructions/
   cp /path/to/.github/instructions/reactjs.instructions.md .github/copilot-instructions/
   ```

1. **Commit and push**:

   ```bash
   git add .github/copilot-instructions/
   git commit -m "chore: add GitHub Copilot custom instructions"
   git push
   ```

#### Option 3: Organization-Wide Installation

For GitHub Enterprise, instructions in this `.github` repository automatically
apply to all organization repositories that don't have their own instructions.

**Setup:**

1. Ensure this repository is the organization's `.github` repository
1. Place instructions in the `instructions/` directory
1. All organization repositories inherit these instructions
1. Repositories can override by providing their own instructions

#### Option 4: User-Level Installation

To apply instructions globally for your user account:

1. **Open VS Code Settings** (`Cmd/Ctrl + ,`)
1. Search for **"Copilot Instructions"**
1. Click **"Edit in settings.json"**
1. Add instruction file paths:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": "/path/to/instructions/python.instructions.md"
    },
    {
      "file": "/path/to/instructions/reactjs.instructions.md"
    }
  ]
}
```

______________________________________________________________________

## Available Instructions

This organization provides **100+ custom instructions** covering frameworks,
languages, tools, and platforms.

### By Category

#### Frontend Development

- **Angular**: Component architecture, RxJS patterns, testing
- **React**: Hooks, state management, component patterns
- **Vue**: Composition API, Pinia, TypeScript integration
- **Svelte**: Reactive declarations, stores, SvelteKit
- **Astro**: Islands architecture, content collections
- **Next.js**: App Router, Server Components, data fetching

#### Backend Development

- **ASP.NET**: REST APIs, Entity Framework, dependency injection
- **Express.js**: Middleware patterns, error handling, routing
- **FastAPI**: Type hints, async patterns, dependency injection
- **Spring Boot**: Annotations, JPA, security configuration
- **Rails**: ActiveRecord, conventions, testing

#### Mobile Development

- **React Native**: Navigation, native modules, performance
- **Flutter**: Widget composition, state management, platform channels
- **SwiftUI**: View composition, data flow, async patterns
- **Kotlin Android**: Jetpack Compose, coroutines, architecture components

#### Cloud Platforms

- **Azure**: ARM templates, Bicep, Azure Functions, Logic Apps
- **AWS**: CloudFormation, Lambda, CDK
- **Google Cloud**: Terraform, Cloud Functions, GKE

#### DevOps & Infrastructure

- **Terraform**: Module structure, state management, best practices
- **Ansible**: Playbook organization, role structure, idempotency
- **GitHub Actions**: Workflow patterns, security, reusable workflows
- **Azure DevOps**: Pipeline YAML, artifact management

#### Databases

- **PostgreSQL**: Query optimization, indexing, migrations
- **MongoDB**: Schema design, aggregation pipelines
- **SQL Server**: T-SQL patterns, stored procedures
- **Redis**: Caching strategies, data structures

#### Languages

- **Python**: PEP 8, type hints, async patterns, testing
- **TypeScript**: Strict typing, utility types, decorators
- **Java**: Naming conventions, streams, Optional usage
- **C#**: LINQ, async/await, null handling
- **Go**: Error handling, interfaces, goroutines
- **Rust**: Ownership, lifetimes, error handling

#### Testing

- **Jest**: Test organization, mocking, coverage
- **pytest**: Fixtures, parametrization, plugins
- **JUnit**: Assertions, test lifecycle, extensions
- **Cypress**: E2E patterns, custom commands
- **Playwright**: Page objects, fixtures, screenshots

#### Security

- **OWASP**: SQL injection prevention, XSS protection
- **Secrets Management**: Environment variables, vault usage
- **Authentication**: JWT, OAuth2, session management
- **Input Validation**: Sanitization, schema validation

### By Technology

The
[`instructions/`](https://github.com/github/awesome-copilot/tree/main/instructions/)<!-- link:github.awesome_copilot_instructions -->
directory contains instructions for:

- **109 technologies** across multiple domains
- **Languages**: Python, TypeScript, Java, C#, Go, Rust, Ruby, PHP, Swift,
  Kotlin, Scala, Elixir, Clojure
- **Frameworks**: React, Angular, Vue, Express, FastAPI, Spring Boot, Django,
  Rails, Laravel
- **Platforms**: Azure, AWS, Google Cloud, Vercel, Netlify
- **Tools**: Docker, Kubernetes, Terraform, Ansible, GitHub Actions
- **Databases**: PostgreSQL, MongoDB, MySQL, Redis, Elasticsearch

**Browse all instructions:**
[`instructions/`](https://github.com/github/awesome-copilot/tree/main/instructions/)<!-- link:github.awesome_copilot_instructions -->

______________________________________________________________________

## How Instructions Work

### File Pattern Matching

Instructions use **glob patterns** to specify which files they apply to:

```yaml
---
description: "Python best practices and conventions"
applyTo: "**.py"
---
```

**Common patterns:**

- `**.py` - All Python files
- `**.ts, **.tsx` - TypeScript and TSX files
- `**/tests/**.js` - JavaScript test files
- `src/components/**.jsx` - React components in src/components

### Instruction Priority

When multiple instructions apply to a file:

1. **Repository instructions** (most specific) - `.github/copilot-instructions/`
1. **Organization instructions** - From organization's `.github` repository
1. **User instructions** (least specific) - From VS Code settings

### Instruction Format

Instructions use Markdown with YAML frontmatter:

```markdown
---
description: "Brief description of what these instructions cover"
applyTo: "**.py, **/python/**"
---

# Instruction Title

## Category 1

- Rule 1
- Rule 2

## Category 2

- Rule 3
- Rule 4

## Code Examples

\`\`\`python

# Good example

def example():
pass
\`\`\`
```

______________________________________________________________________

## Using Instructions

### Automatic Application

Once installed, instructions automatically enhance Copilot suggestions:

1. **Open a file** that matches an instruction's pattern
1. **Start typing** or use Copilot Chat
1. **Copilot applies** relevant instructions automatically
1. **Generated code** follows your standards

### Verifying Instructions

To check which instructions apply to a file:

1. Open the file in VS Code
1. Open Copilot Chat
1. Ask: "What custom instructions apply to this file?"

### Manual Override

To temporarily ignore instructions:

```
@workspace /new Create a function without applying custom instructions
```

Or specify different conventions:

```
@workspace Generate code following Google's style guide instead
```

______________________________________________________________________

## Creating Custom Instructions

### Step 1: Identify Standards

Document the conventions you want to enforce:

- Coding style (formatting, naming)
- Architectural patterns (MVC, layered, microservices)
- Error handling strategies
- Testing approaches
- Security requirements
- Performance considerations

### Step 2: Create Instruction File

Create a `.instructions.md` file in the `instructions/` directory:

```bash
touch .github/copilot-instructions/my-project.instructions.md
```

### Step 3: Write Instructions

Follow the standard format:

```markdown
---
description: "Custom instructions for MyProject"
applyTo: "src/myproject/**.py"
---

# MyProject Python Standards

## Naming Conventions

- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Prefix private methods with underscore: `_private_method`

## Error Handling

- Always use custom exception classes
- Include error context in exception messages
- Log all exceptions with appropriate severity

## Testing

- Write tests for all public functions
- Use pytest fixtures for setup/teardown
- Aim for 80% code coverage

## Code Examples

\`\`\`python

# Good: Clear naming and error handling

class DataProcessor:
def process_data(self, data: dict) -> dict:
try:
return self.\_transform_data(data)
except ValueError as e:
logger.error(f"Data processing failed: {e}")
raise ProcessingError(f"Invalid data format: {e}")

    def _transform_data(self, data: dict) -> dict:
        # Private implementation
        pass

\`\`\`
```

### Step 4: Test Instructions

1. Create a test file matching the pattern
1. Ask Copilot to generate code
1. Verify the code follows your instructions
1. Iterate on the instructions based on results

### Step 5: Share with Team

1. Commit the instruction file
1. Document in your team's onboarding materials
1. Add to repository's CONTRIBUTING.md
1. Share installation instructions with team members

______________________________________________________________________

## Best Practices

### Writing Instructions

- **Be specific**: Provide clear, actionable guidelines
- **Include examples**: Show good and bad code examples
- **Explain why**: Justify conventions so developers understand
- **Keep focused**: One instruction file per topic or technology
- **Update regularly**: Keep instructions current with evolving standards

### Organization

- **Consistent naming**: Use descriptive file names (e.g.,
  `python-web-api.instructions.md`)
- **Logical grouping**: Group related instructions together
- **Clear patterns**: Use specific file patterns to avoid conflicts
- **Documentation**: Maintain a README listing all instructions

### Maintenance

- **Version control**: Track changes to understand evolution
- **Review process**: Have senior developers review instruction changes
- **Feedback loop**: Collect developer feedback on instruction effectiveness
- **Periodic audit**: Ensure instructions stay relevant and accurate
- **Deprecation**: Remove outdated instructions and update references

### Security

- **No secrets**: Never include API keys, passwords, or tokens
- **Security-first**: Include security best practices in all instructions
- **Input validation**: Emphasize validation and sanitization
- **Least privilege**: Encourage minimal permission approaches
- **Audit logging**: Include logging guidelines for sensitive operations

______________________________________________________________________

## Troubleshooting

### Instructions Not Applying

**Problem**: Copilot doesn't seem to follow your instructions

**Solutions**:

1. Verify file pattern matches your files
1. Check instruction file has correct YAML frontmatter
1. Ensure file is in correct location (`.github/copilot-instructions/`)
1. Restart VS Code to reload instructions
1. Check for syntax errors in the instruction file
1. Verify GitHub Copilot is enabled for the file type

### Conflicting Instructions

**Problem**: Multiple instructions provide conflicting guidance

**Solutions**:

1. Make file patterns more specific to reduce overlap
1. Merge related instructions into a single file
1. Use repository-level instructions to override organization-level ones
1. Clearly document precedence in your team guide

### Instructions Too Strict

**Problem**: Instructions limit Copilot's creativity

**Solutions**:

1. Focus on essential standards, not every detail
1. Provide guidelines rather than strict rules
1. Allow flexibility for edge cases
1. Include "prefer X but Y is acceptable" language
1. Periodically review and relax overly restrictive rules

### Performance Issues

**Problem**: Copilot seems slower with instructions

**Solutions**:

1. Reduce instruction file size (keep under 1000 lines)
1. Remove redundant or obvious guidelines
1. Use multiple smaller files instead of one large file
1. Focus on high-impact conventions
1. Profile to identify specific slow instructions

______________________________________________________________________

## Additional Resources

### Documentation

- [GitHub Copilot Documentation](https://docs.github.com/copilot)<!-- link:docs.github_copilot -->
- [VS Code Copilot Settings](https://code.visualstudio.com/docs/copilot/copilot-settings)
- [Awesome Copilot Repository](https://github.com/github/awesome-copilot)<!-- link:github.awesome_copilot -->

### Organization Resources

- [Instructions Directory](https://github.com/github/awesome-copilot/tree/main/instructions/)<!-- link:github.awesome_copilot_instructions -->
  \- Browse all 100+ instructions
- [Instructions Documentation](README.instructions.md) - Detailed guide to
  instructions
- [Agent Architecture Guide](AGENT_ARCHITECTURE_GUIDE.md) - Using instructions
  with agents
- [Collections](../ai_framework/collections/) - Bundled instructions by theme

### Templates

- [Instruction Template](https://github.com/github/awesome-copilot/blob/main/instructions/instructions.instructions.md)
  \- Blank template for new instructions
- [Python Template](https://github.com/github/awesome-copilot/blob/main/instructions/python.instructions.md)<!-- link:github.awesome_copilot_python_instruction -->
  \- Example Python instructions
- [TypeScript Template](https://github.com/github/awesome-copilot/blob/main/instructions/typescript-5-es2022.instructions.md)<!-- link:github.awesome_copilot_typescript_instruction -->
  \- Example TypeScript instructions

### Community

- [GitHub Discussions](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->
  \- Share instruction ideas
- [Issue Tracker](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
  \- Report issues or request features
- [Contributing Guide](../governance/CONTRIBUTING.md) - Contribute new
  instructions

______________________________________________________________________

## Next Steps

1. **Browse available instructions** in the
   [`instructions/`](https://github.com/github/awesome-copilot/tree/main/instructions/)<!-- link:github.awesome_copilot_instructions -->
   directory
1. **Install instructions** for your primary technologies
1. **Test with Copilot** on a sample project
1. **Create custom instructions** for your team's specific needs
1. **Share with your team** and gather feedback
1. **Iterate and improve** based on real-world usage

______________________________________________________________________

**Questions or Feedback?**

- Check the [Troubleshooting](#troubleshooting) section
- Review related guides: [MCP Server Setup](MCP_SERVER_SETUP.md) |
  [Development Environment Setup](DEVELOPMENT_ENVIRONMENT_SETUP.md)
- Open an issue or discussion in this repository
- Reach out to your GitHub Copilot administrator

______________________________________________________________________

_Last Updated: 2025-12-31_

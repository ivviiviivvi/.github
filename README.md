# ivi374forivi Organization

> **Default Community Health Files and Configurations**

Welcome to the **ivi374forivi** organization! We believe in open collaboration,
transparent development, and building innovative solutions through high-quality
software and inclusive community practices.

## 📖 About This Repository

This is the special `.github` repository for our organization. It serves as the
central hub for:

- **Default community health files** that apply to all repositories
- **Standardized templates** for issues and pull requests
- **Reusable workflow templates** for CI/CD and automation
- **Organization-wide configuration** and documentation standards
- **Living Document System** - AI-driven governance and management protocols

When a repository in our organization doesn't have its own community health file
s, GitHub automatically uses the defaults from this repository.

> **Is this the right repository for these functions?** See our [Repository Purp
ose Analysis](REPOSITORY_PURPOSE_ANALYSIS.md) for a detailed explanation of why
this `.github` repository is the appropriate location for organization-wide gove
rnance, templates, and the Living Document System.

## 🎯 Our Mission

At **ivi374forivi**, we are committed to:

- **Openness**: Developing in the open with transparency
- **Collaboration**: Welcoming diverse perspectives and contributors
- **Quality**: Delivering well-tested, documented, and maintainable software
- **Respect**: Maintaining an inclusive environment for all
- **Innovation**: Encouraging experimentation and creative problem-solving
- **Sustainability**: Building projects supported by healthy communities

Read our complete vision in the [Manifesto](MANIFESTO.md).

### Commit Message Format

We follow conventional commit format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

**Examples**:
- `feat: add user authentication`
- `fix: resolve memory leak in data processor`
- `docs: update API documentation`

### Viewing Commit Reports

Commit tracking runs automatically on:
- Every push to `main` or `develop` branches
- Every pull request update

Weekly reports are generated every Monday and stored in the `reports/` directory
.

## 🗂️ What's Inside

### 🤖 GitHub Copilot Customizations

This repository includes comprehensive GitHub Copilot customizations from the [g
ithub/awesome-copilot](https://github.com/github/awesome-copilot) repository for
 organization-wide implementation:

#### Custom Agents
- **Location**: `agents/` directory
- **Purpose**: Specialized GitHub Copilot agents that integrate with MCP servers
 for enhanced capabilities
- **Examples**: CSharpExpert, Terraform, ADR Generator, and partner integrations

#### Instructions
- **Location**: `instructions/` directory
- **Purpose**: Comprehensive coding standards and best practices that apply to s
pecific file patterns
- **Coverage**: Multiple frameworks and languages (Angular, React, Python, .NET,
 Azure, etc.)
- **Usage**: Instructions automatically apply based on file patterns

#### Prompts
- **Location**: `prompts/` directory
- **Purpose**: Task-specific prompts for code generation, documentation, and pro
blem-solving
- **Usage**: Access via `/` commands in GitHub Copilot Chat (e.g., `/awesome-cop
ilot create-readme`)

#### Chat Modes
- **Location**: `chatmodes/` directory
- **Purpose**: Specialized AI personas for different roles (architect, DBA, secu
rity expert, etc.)
- **Usage**: Activate modes for specialized assistance tailored to specific cont
exts

#### Collections
- **Location**: `collections/` directory
- **Purpose**: Curated collections of prompts, instructions, and chat modes orga
nized by theme
- **Examples**: Azure Cloud Development, Frontend Web Dev, Security Best Practic
es

For detailed documentation on each component, see the `docs/` directory:
- [Agents Documentation](docs/README.agents.md)
- [Instructions Documentation](docs/README.instructions.md)
- [Prompts Documentation](docs/README.prompts.md)
- [Chat Modes Documentation](docs/README.chatmodes.md)
- [Collections Documentation](docs/README.collections.md)

### Community Health Files

These files establish standards for community interaction and contribution acros
s all repositories:

| File | Purpose |
|------|---------|
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Standards for respectful community
interaction |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guidelines for contributing to our projec
ts |
| [SECURITY.md](SECURITY.md) | Security policy and vulnerability reporting |
| [SUPPORT.md](SUPPORT.md) | How to get help and support |
| [LICENSE](LICENSE) | MIT License for our projects |
| [FUNDING.yml](FUNDING.yml) | Funding and sponsorship configuration |
| [GOVERNANCE.md](GOVERNANCE.md) | Project governance and decision-making |
| [MANIFESTO.md](MANIFESTO.md) | Our core principles and values |

### Issue Templates

Comprehensive templates to help contributors submit high-quality issues:

- **Bug Reports** - Both classic markdown and modern form-based templates
- **Feature Requests** - Structured templates for proposing new features
- **Documentation** - Template for documentation improvements
- **Questions** - Template for asking questions

Configuration: [ISSUE_TEMPLATE/config.yml](ISSUE_TEMPLATE/config.yml)

### Pull Request Templates

Specialized templates for different types of contributions:

- **Default Template** - [PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md)
- **Bug Fix** - [PULL_REQUEST_TEMPLATE/bug_fix.md](PULL_REQUEST_TEMPLATE/bug_fix
.md)
- **Feature** - [PULL_REQUEST_TEMPLATE/feature.md](PULL_REQUEST_TEMPLATE/feature
.md)
- **Documentation** - [PULL_REQUEST_TEMPLATE/documentation.md](PULL_REQUEST_TEMP
LATE/documentation.md)
- **Refactoring** - [PULL_REQUEST_TEMPLATE/refactoring.md](PULL_REQUEST_TEMPLATE
/refactoring.md)
- **Performance** - [PULL_REQUEST_TEMPLATE/performance.md](PULL_REQUEST_TEMPLATE
/performance.md)

💡 **Tip**: Select a specific template by adding `?template=<name>.md` to the PR
URL

### Workflow Templates

Reusable GitHub Actions workflows ready to use in any repository:

| Template | Purpose | Use Case |
|----------|---------|----------|
| [ci.yml](workflow-templates/ci.yml) | Basic CI pipeline | Building and testing
 code |
| [security-scan.yml](workflow-templates/security-scan.yml) | CodeQL analysis |
Vulnerability scanning |
| [stale-management.yml](workflow-templates/stale-management.yml) | Stale issue/
PR management | Keeping repositories clean |
| [dependency-updates.yml](workflow-templates/dependency-updates.yml) | Automate
d updates | Managing dependencies |
| [deployment.yml](workflow-templates/deployment.yml) | Deployment pipeline | St
aging and production releases |

### Automation Configuration

- **[dependabot.yml](dependabot.yml)** - Organization-wide Dependabot configurat
ion for:
  - npm (JavaScript/Node.js)
  - pip (Python)
  - GitHub Actions
  - Docker
  - Go modules
  - Composer (PHP)

### Documentation & Guides

Comprehensive guides for maintaining high-quality repositories:

| Document | Description |
|----------|-------------|
| [AI_IMPLEMENTATION_GUIDE.md](AI_IMPLEMENTATION_GUIDE.md) | AI-driven organizat
ion management guide |
| [REPOSITORY_PURPOSE_ANALYSIS.md](REPOSITORY_PURPOSE_ANALYSIS.md) | Analysis of
 repository appropriateness for function set |
| [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) | Branch protection rules and con
figuration |
| [REPOSITORY_SETUP_CHECKLIST.md](REPOSITORY_SETUP_CHECKLIST.md) | New repositor
y setup checklist |
| [LABELS.md](LABELS.md) | Standard label set for consistent tagging |
| [TESTING.md](TESTING.md) | Testing standards and best practices |
| [for-ai-implementation.txt](for-ai-implementation.txt) | Complete AI GitHub ma
nagement protocol |

### Organization Profile

The [profile/README.md](profile/README.md) file is displayed on our organization
's public profile page.

## 🚀 Getting Started

### For New Repositories

1. **Automatic Inheritance**: New repositories automatically inherit community h
ealth files from this repository if they don't have their own versions.

2. **Using Workflow Templates**:
   - Navigate to **Actions → New workflow** in your repository
   - Look for templates in the "By your organization" section
   - Select, customize, and commit the workflow

3. **Setup Checklist**: Follow the [Repository Setup Checklist](REPOSITORY_SETUP
_CHECKLIST.md) for comprehensive guidance.

### For Existing Repositories

1. **Adopt Standards**: Review organization standards from this repository
2. **Enable Workflows**: Copy desired workflow templates to `.github/workflows/`
 in your repo
3. **Configure Dependabot**: Copy [dependabot.yml](dependabot.yml) to `.github/`
 in your repository
4. **Apply Labels**: Use [LABELS.md](LABELS.md) to standardize issue labels
5. **Enable Branch Protection**: Follow [BRANCH_PROTECTION.md](BRANCH_PROTECTION
.md) guidelines

### Customizing Templates

Individual repositories can override these defaults by creating their own versio
ns of any file. The repository-level file will take precedence over the organiza
tion default.

## 📁 Repository Structure

```
.github/
├── .github/
│   ├── copilot-instructions.md             # Copilot code review instructions
│   └── workflows/                          # GitHub Actions workflows
├── profile/
│   └── README.md                           # Organization profile page
├── ISSUE_TEMPLATE/
│   ├── config.yml                          # Issue template configuration
│   ├── bug_report.md                       # Bug report (markdown)
│   ├── bug_report_form.yml                 # Bug report (form-based)
│   ├── feature_request.md                  # Feature request (markdown)
│   ├── feature_request_form.yml            # Feature request (form-based)
│   ├── documentation.md                    # Documentation issues
│   └── question.md                         # Question template
├── PULL_REQUEST_TEMPLATE/
│   ├── bug_fix.md                          # Bug fix PR template
│   ├── feature.md                          # Feature PR template
│   ├── documentation.md                    # Documentation PR template
│   ├── refactoring.md                      # Refactoring PR template
│   └── performance.md                      # Performance PR template
├── workflow-templates/
│   ├── ci.yml                              # CI workflow template
│   ├── ci.properties.json                  # CI metadata
│   ├── security-scan.yml                   # Security scanning workflow
│   ├── security-scan.properties.json       # Security scan metadata
│   ├── stale-management.yml                # Stale issue/PR workflow
│   ├── stale-management.properties.json    # Stale management metadata
│   ├── dependency-updates.yml              # Dependency update workflow
│   ├── dependency-updates.properties.json  # Dependency update metadata
│   ├── deployment.yml                      # Deployment workflow
│   └── deployment.properties.json          # Deployment metadata
├── agents/                                 # GitHub Copilot custom agents
├── chatmodes/                              # GitHub Copilot chat modes
├── collections/                            # Curated Copilot collections
├── docs/                                   # Copilot customization docs
├── instructions/                           # Copilot coding instructions
├── prompts/                                # GitHub Copilot prompts
├── AI_IMPLEMENTATION_GUIDE.md              # AI management implementation guide
├── BRANCH_PROTECTION.md                    # Branch protection guide
├── CODE_OF_CONDUCT.md                      # Code of conduct
├── CONTRIBUTING.md                         # Contributing guidelines
├── FUNDING.yml                             # Funding configuration
├── GOVERNANCE.md                           # Governance model
├── LABELS.md                               # Standard labels
├── LICENSE                                 # MIT License
├── MANIFESTO.md                            # Organization manifesto
├── PULL_REQUEST_TEMPLATE.md                # Default PR template
├── REPOSITORY_SETUP_CHECKLIST.md           # New repo checklist
├── SECURITY.md                             # Security policy
├── SUPPORT.md                              # Support information
├── TESTING.md                              # Testing standards
├── REPOSITORY_PURPOSE_ANALYSIS.md           # Repository appropriateness analys
is
├── dependabot.yml                          # Dependabot configuration
└── for-ai-implementation.txt               # AI management protocol
```

## 🤖 AI-Driven Organization Management

This organization implements an advanced AI-driven GitHub management system with
 8 core modules:

1. **Organization & Repository Administration** - Setup, access control, and bra
nch protection
2. **Project Management & Workflow Automation** - Boards, issues, labels, and au
tomation
3. **CI/CD & Development Lifecycle** - Build pipelines, testing, and deployment
4. **Security & Compliance Operations** - Vulnerability management and complianc
e
5. **Documentation & Knowledge Base** - Maintaining comprehensive documentation
6. **Ecosystem Integration & Architecture** - Monitoring service dependencies
7. **Observability & System Health** - Analytics and system monitoring
8. **Strategic Analysis & Risk Mitigation** - Proactive risk identification

Read the full protocol: [for-ai-implementation.txt](for-ai-implementation.txt) |
 [Implementation Guide](AI_IMPLEMENTATION_GUIDE.md)

## 🛠️ Key Features

### Automated Security

- **Dependabot**: Automatic dependency updates across multiple ecosystems
- **CodeQL Analysis**: Continuous security scanning for vulnerabilities
- **Branch Protection**: Enforced protection rules on production branches
- **Secret Scanning**: Detection of hardcoded secrets (where enabled)

### Quality Assurance

- **Standardized Templates**: Consistent issue and PR formats
- **Code Review Guidelines**: Built into PR templates
- **Testing Standards**: Documented in [TESTING.md](TESTING.md)
- **Contribution Guidelines**: Clear expectations in [CONTRIBUTING.md](CONTRIBUT
ING.md)

### Developer Experience

- **Workflow Templates**: Ready-to-use CI/CD pipelines
- **Stale Issue Management**: Automated cleanup of inactive items
- **Comprehensive Documentation**: Setup guides and best practices
- **Label Standards**: Consistent categorization across repositories

## 🤝 Contributing

We welcome contributions from everyone! Here's how to get started:

1. **Read the Guidelines**: Check [CONTRIBUTING.md](CONTRIBUTING.md) for detaile
d instructions
2. **Follow the Code of Conduct**: All interactions must follow our [CODE_OF_CON
DUCT.md](CODE_OF_CONDUCT.md)
3. **Use Templates**: Submit issues and PRs using our templates
4. **Ask Questions**: Don't hesitate to open a question issue or discussion

### Improving This Repository

To enhance our organization's GitHub management:

- Propose changes via pull requests
- Use appropriate PR templates
- Ensure changes align with our AI GitHub Management Protocol
- Update documentation when adding new features

## 📚 Resources

### GitHub Documentation

- [About default community health files](https://docs.github.com/en/communities/
setting-up-your-project-for-healthy-contributions/creating-a-default-community-h
ealth-file)
- [About organization profiles](https://docs.github.com/en/organizations/collabo
rating-with-groups-in-organizations/customizing-your-organizations-profile)
- [Creating workflow templates](https://docs.github.com/en/actions/using-workflo
ws/creating-starter-workflows-for-your-organization)
- [Dependabot configuration](https://docs.github.com/en/code-security/dependabot
/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

### Organization Documentation

- [Manifesto](MANIFESTO.md) - Our core principles and values
- [Governance](GOVERNANCE.md) - How we make decisions
- [Support](SUPPORT.md) - Getting help
- [Security](SECURITY.md) - Reporting vulnerabilities

## 📄 License

This repository and all default community health files are provided under the [M
IT License](LICENSE).

## 💬 Support

Need help? Have questions?

- 📖 Check our [Support Documentation](SUPPORT.md) for detailed guidance
- 🐛 Report issues using our [issue templates](ISSUE_TEMPLATE/)
- 📧 Contact repository maintainers through GitHub
- 💬 For general discussions, check if [GitHub Discussions](https://github.com/or
gs/ivi374forivi/discussions) are enabled

---

**Built with ❤️ by the ivi374forivi community**
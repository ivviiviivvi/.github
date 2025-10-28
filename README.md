# .github

This is the special `.github` repository for the **ivi374forivi** organization. It provides default community health files and configurations that apply to all repositories in the organization.

## What's Inside

### Organization Profile

The `profile/README.md` file displays on the organization's public profile page, introducing visitors to the organization.

### Community Health Files

These files provide default templates for all repositories in the organization:

- **CODE_OF_CONDUCT.md** - Defines standards for community interaction
- **CONTRIBUTING.md** - Guidelines for contributing to projects
- **SECURITY.md** - Security policy and vulnerability reporting process
- **SUPPORT.md** - How to get help and support
- **FUNDING.yml** - Funding and sponsorship configuration

### Issue and Pull Request Templates

- **ISSUE_TEMPLATE/** - Templates for creating issues (bug reports, feature requests)
- **PULL_REQUEST_TEMPLATE.md** - Template for pull requests

### Workflow Templates

The `workflow-templates/` directory contains reusable GitHub Actions workflow templates that can be used across repositories.

## How It Works

When a repository in the organization doesn't have its own community health files, GitHub automatically uses the files from this `.github` repository as defaults.

## Customization

Individual repositories can override these defaults by creating their own versions of these files.

## Learn More

- [About default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [About organization profiles](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
- [Creating workflow templates](https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization)

## Structure

```
.github/
├── profile/
│   └── README.md                    # Organization profile
├── ISSUE_TEMPLATE/
│   ├── config.yml                   # Issue template configuration
│   ├── bug_report.md                # Bug report template
│   └── feature_request.md           # Feature request template
├── workflow-templates/
│   ├── ci.yml                       # CI workflow template
│   └── ci.properties.json           # Workflow template metadata
├── CODE_OF_CONDUCT.md               # Code of conduct
├── CONTRIBUTING.md                  # Contributing guidelines
├── SECURITY.md                      # Security policy
├── SUPPORT.md                       # Support information
├── FUNDING.yml                      # Funding configuration
└── PULL_REQUEST_TEMPLATE.md         # Pull request template
```
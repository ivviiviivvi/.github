# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Repository Purpose

Organization-level `.github` repository for {{ORG_NAME}} providing:

- Default community health files inherited by all org repositories
- {{WORKFLOW_COUNT}} GitHub Actions workflows
- {{AGENT_COUNT}} production AI agents in `src/ai_framework/`
- GitHub Copilot customizations (instructions, prompts, chatmodes, collections)

## Essential Commands

### Setup

```bash
pip install -e ".[dev]"
pre-commit install
```

### Testing

```bash
# Full test suite with coverage (58% minimum required)
python -m pytest --cov=src/automation

# Single test file
python -m pytest tests/test_specific.py -v

# Run by marker
python -m pytest -m unit        # Unit tests only
python -m pytest -m integration # Integration tests
python -m pytest -m critical    # Critical tests
```

### Linting and Code Quality

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Python linting with ruff
ruff check .
ruff format .

# Type checking
mypy src/automation/

# Security scanning
bandit -r src/automation/scripts/
```

### Version Management

```bash
# Check version (in pyproject.toml)
grep "^version" pyproject.toml  # Currently 1.0.0

# Bump and sync versions
npm run version:bump:minor
npm run version:sync
```

## Architecture Overview

> **Note**: The nested `.github/.github/` structure is intentional and correct
> for organization-level `.github` repositories. GitHub looks for workflows in
> `.github/workflows/` relative to the repository root.

```
.github/
├── .config/               # ALL configs (devcontainer, vscode, jules, pre-commit)
├── .github/workflows/     # {{WORKFLOW_COUNT}} automation workflows
│   └── reusable/          # {{REUSABLE_TEMPLATE_COUNT}} reusable workflow templates
├── docs/                  # ALL documentation (304+ files)
│   ├── archive/           # Historical reports
│   ├── guides/            # How-to guides (includes extended CLAUDE.md)
│   └── registry/          # Workflow registry
├── src/
│   ├── ai_framework/      # AI agents, chatmodes, prompts
│   │   ├── agents/        # {{AGENT_COUNT}} production AI agents (*.agent.md)
│   │   ├── chatmodes/     # {{CHATMODE_COUNT}} chatmodes (*.chatmode.md)
│   │   ├── collections/   # Collection definitions
│   │   └── prompts/       # Prompt templates (*.prompt.md)
│   └── automation/        # Python automation scripts
│       ├── scripts/       # {{SCRIPT_COUNT}} Python automation scripts
│       │   └── utils/     # Utility scripts (update-action-pins.py, etc.)
│       └── project_meta/  # Project metadata and context handoffs
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml         # Python config (deps, pytest, coverage, ruff, mypy)
└── package.json           # npm config (version scripts)
```

## Key Patterns

### Workflow SHA Pinning

All GitHub Actions are SHA-pinned with ratchet comments:

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4
```

Update pins with:
`python src/automation/scripts/utils/update-action-pins.py --recursive`

### Centralized Version Management

Workflows use repository variables with fallbacks:

```yaml
python-version: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
node-version: ${{ vars.NODE_VERSION_DEFAULT || '20' }}
```

### FUNCTIONcalled Metadata

Workflows can have `.meta.json` sidecars with layer classification:

- `core` - Foundation, CI, reusable workflows
- `interface` - User-facing workflows
- `logic` - Validation workflows
- `application` - Deployment, release workflows

## Commit Convention

**Strictly enforced** via pre-commit hooks and CI:

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```

Examples:

- `feat(workflows): add auto-labeling for new PRs`
- `fix(ci): resolve CodeQL security alerts`
- `docs: update installation guide`

## Pre-commit Troubleshooting

If `mypy` fails on `types-all` dependency:

1. Remove `types-all` from `.config/pre-commit-rapid.yaml`
1. Run `pre-commit clean && pre-commit install`

If `mdformat` has dependency conflicts:

1. Ensure rev is `0.7.17` with `mdformat-gfm>=0.3.5`
1. Run
   `pre-commit autoupdate --repo https://github.com/executablebooks/mdformat`

## Key Files

| File                                                 | Purpose                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| `pyproject.toml`                                     | Python config (deps, pytest, coverage, ruff, mypy, bandit) |
| `.pre-commit-config.yaml`                            | Quality hooks (symlink to .config/pre-commit.yaml)         |
| `src/automation/scripts/utils/update-action-pins.py` | SHA pin updater                                            |
| `.github/WORKFLOW_STANDARDS.md`                      | Workflow conventions                                       |
| `docs/guides/CLAUDE.md`                              | Extended AI assistant guide with workflow catalog          |

## Runtime Requirements

- Python >= 3.9 (prefer 3.12)
- Node.js >= 20.0.0
- Dependencies: PyYAML, requests, PyGithub, jsonschema

## Branch Naming

Allowed patterns:

- `<lifecycle>/<type>/<component>` (e.g., `develop/feature/user-auth`)
- `fix/<description>` (e.g., `fix/workflow-bug`)
- `release/v<semver>` (e.g., `release/v1.2.0`)
- `dependabot/*` (automated dependency updates)

Lifecycles: develop, experimental, production, maintenance, deprecated, archive
Types: feature, bugfix, hotfix, enhancement, refactor, docs, test, chore

## Test Markers

```bash
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m critical      # Critical functionality
pytest -m month1        # Month 1 core workflow tests
pytest -m month2        # Month 2 feature tests (Slack, ML)
pytest -m month3        # Month 3 advanced automation tests
pytest -m security      # Security-focused tests
```

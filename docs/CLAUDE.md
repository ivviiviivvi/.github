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

### Testing

```bash
# Full test suite with coverage (58% minimum required)
python -m pytest --cov=src/automation --cov-report=html

# Single test file
python -m pytest tests/test_specific.py -v

# Run by marker
python -m pytest -m unit      # Unit tests only
python -m pytest -m integration  # Integration tests
python -m pytest -m critical  # Critical tests
```

### Linting & Code Quality

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

### Setup

```bash
pip install -e ".[dev]"
pip install pre-commit
pre-commit install
```

## Architecture Overview

```
.github/
├── .config/               # ALL configs (devcontainer, vscode, jules, pre-commit, etc.)
├── .github/workflows/     # {{WORKFLOW_COUNT}} automation workflows
│   └── reusable/          # {{REUSABLE_TEMPLATE_COUNT}} reusable workflow templates
├── docs/                  # ALL documentation
│   ├── archive/           # Historical reports and results
│   ├── registry/          # Workflow registry
│   ├── site/              # Jekyll site files
│   ├── CHANGELOG.md       # Version changelog
│   └── CLAUDE.md          # This file
├── src/
│   ├── ai_framework/      # AI agents, chatmodes, instructions, prompts
│   │   ├── agents/        # {{AGENT_COUNT}} production AI agents
│   │   ├── chatmodes/     # Copilot chat modes
│   │   ├── instructions/  # 100+ coding instructions
│   │   └── prompts/       # Task-specific prompts
│   └── automation/        # Python automation scripts
│       ├── scripts/       # {{SCRIPT_COUNT}} Python automation scripts
│       │   └── utils/     # Utility scripts (update-action-pins.py, etc.)
│       └── project_meta/  # Project metadata and context handoffs
├── tests/
│   ├── unit/
│   └── integration/
│
├── .gitignore             # Git config
├── LICENSE                # MIT license
├── README.md              # Project documentation
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

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
```

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
| `.github/VERSION_MANAGEMENT.md`                      | Centralized versioning docs                                |
| `.github/WORKFLOW_STANDARDS.md`                      | Workflow conventions                                       |

## Runtime Requirements

- Python >= 3.9 (prefer 3.12)
- Node.js >= 20.0.0
- Dependencies: PyYAML, requests, PyGithub, jsonschema

## Additional Documentation

See `docs/guides/CLAUDE.md` for comprehensive guide including:

- Full workflow catalog
- GitHub Copilot customization details
- Security & compliance information
- Detailed task examples

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Organization-level `.github` repository for ivviiviivvi providing:
- Default community health files inherited by all org repositories
- 98+ GitHub Actions workflows
- 26 production AI agents in `ai_framework/`
- GitHub Copilot customizations (instructions, prompts, chatmodes, collections)

## Essential Commands

### Testing
```bash
# Full test suite with coverage (80% minimum required)
python -m pytest --cov=automation --cov-report=html

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
mypy automation/

# Security scanning
bandit -r automation/scripts/
```

### Version Management
```bash
# Check version
cat VERSION  # Currently 1.0.0

# Bump and sync versions
npm run version:bump:minor
npm run version:sync
```

### Setup
```bash
pip install -r requirements.txt
pip install pre-commit
pre-commit install
```

## Architecture Overview

```
.github/
├── .github/workflows/     # 98+ automation workflows
│   └── reusable/          # 6 reusable workflow templates
├── ai_framework/
│   ├── agents/            # 26 production AI agents
│   ├── chatmodes/         # Copilot chat modes
│   ├── instructions/      # 100+ coding instructions
│   └── prompts/           # Task-specific prompts
├── automation/
│   └── scripts/           # 44 Python automation scripts
├── scripts/               # Utility scripts (update-action-pins.py, etc.)
├── tests/
│   ├── unit/
│   └── integration/
└── docs/                  # 133+ documentation files
```

## Key Patterns

### Workflow SHA Pinning
All GitHub Actions are SHA-pinned with ratchet comments:
```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4
```

Update pins with: `python scripts/update-action-pins.py --recursive`

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
1. Remove `types-all` from `.pre-commit-config-rapid.yaml`
2. Run `pre-commit clean && pre-commit install`

If `mdformat` has dependency conflicts:
1. Ensure rev is `0.7.17` with `mdformat-gfm>=0.3.5`
2. Run `pre-commit autoupdate --repo https://github.com/executablebooks/mdformat`

## Key Files

| File | Purpose |
|------|---------|
| `pytest.ini` | Test config (80% coverage, markers) |
| `.pre-commit-config.yaml` | Quality hooks (ruff, mypy, bandit, etc.) |
| `VERSION` | Source of truth for version (1.0.0) |
| `scripts/update-action-pins.py` | SHA pin updater |
| `.github/VERSION_MANAGEMENT.md` | Centralized versioning docs |
| `.github/WORKFLOW_STANDARDS.md` | Workflow conventions |

## Runtime Requirements

- Python >= 3.9 (prefer 3.11+)
- Node.js >= 20.0.0
- Dependencies: PyYAML, requests, PyGithub, jsonschema

## Additional Documentation

See `docs/guides/CLAUDE.md` for comprehensive guide including:
- Full workflow catalog
- GitHub Copilot customization details
- Security & compliance information
- Detailed task examples

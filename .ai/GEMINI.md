# {{ORG_NAME}} Organization Hub

## Project Overview

This is the centralized `.github` repository for the **{{ORG_NAME}}**
organization. It serves as the infrastructure backbone, providing
organization-wide defaults, governance policies, comprehensive workflow
automation, and a ready-to-deploy AI agent framework.

**Key Features:**

- **Centralized Infrastructure:** "Zero-config" inheritance for new
  repositories.
- **Workflow Automation:** 129 GitHub Actions workflows covering CI/CD,
  security, and maintenance.
- **AI Framework:** 32 production-ready AI agents, GitHub Copilot
  customizations, and an MCP Server framework supporting 11 languages.
- **Documentation:** Extensive guides, references, and reports (>300 files).

## Architecture & Structure

The repository follows a structured layout to manage its diverse
responsibilities:

- **`.config/`**: Configuration files for development tools (VS Code,
  pre-commit, linters).
- **`.github/workflows/`**: The core collection of 129 GitHub Actions workflows.
- **`docs/`**: Comprehensive documentation including guides, reports, and
  standards.
- **`src/ai_framework/`**: Source code for the AI agents, chat modes,
  instructions, and prompts.
- **`src/automation/`**: Python-based automation scripts and project metadata.
- **`tests/`**: Unit and integration tests for the automation scripts.
- **`workflow-templates/`**: Reusable workflow templates for other repositories.

## Development Stack

- **Languages:** Python (>=3.9), Node.js (>=20.0.0)
- **Python Tools:**
  - **Testing:** `pytest` (with coverage)
  - **Linting/Formatting:** `ruff`
  - **Type Checking:** `mypy`
  - **Security:** `bandit`
- **Node.js Tools:** Used primarily for version management and specific
  scripting tasks.
- **Git Hooks:** `pre-commit` framework for enforcing standards.

## Building and Running

### Prerequisites

- Python >= 3.9 (prefer 3.12)
- Node.js >= 20.0.0
- `pre-commit` installed

### Setup

1. **Install Dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

1. **Install Git Hooks:**

   ```bash
   pre-commit install
   ```

### Testing

Run the full test suite with coverage:

```bash
python -m pytest --cov=src/automation
```

### Linting & Formatting

Check for linting errors and format code:

```bash
ruff check .
ruff format .
```

### Version Management

Versioning is synchronized between `package.json` and `pyproject.toml`.

- **Bump Version:**
  ```bash
  npm run version:bump:minor  # or major/patch
  ```
- **Sync Version:**
  ```bash
  npm run version:sync
  ```

## Development Conventions

- **Commit Messages:** Follow Conventional Commits (e.g.,
  `feat(workflows): add auto-labeling`).
- **Code Style:** Adhere to `ruff` configuration (PEP 8 compatible with specific
  overrides).
- **Testing:** New functionality must include tests. Review `pyproject.toml` for
  test markers (e.g., `unit`, `integration`, `slow`).
- **Documentation:** Update documentation in `docs/` when changing features or
  policies.

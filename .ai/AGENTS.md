# Repository Guidelines

Global policy: /Users/4jp/AGENTS.md applies and cannot be overridden.

## Project Structure & Module Organization

- `.github/` org-level GitHub config: workflows, templates, CODEOWNERS, policy
  docs.
- `.config/` developer tooling config (pre-commit, devcontainer, VS Code).
- `docs/` long-form docs, guides, and reports.
- `src/ai_framework/` agent definitions, chatmodes, instructions, prompts
  (symlink `agents/`).
- `src/automation/` Python automation scripts and metadata; main scripts live in
  `src/automation/scripts/`.
- `tests/` pytest suites (`tests/unit/`, `tests/integration/`).
- Generated artifacts: `htmlcov/`, `coverage.xml`, `test-results/`.

## Build, Test, and Development Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit run --all-files
ruff check .
ruff format .
python -m pytest
```

- Run a focused suite: `pytest -m unit` or `pytest -m integration`.
- Version bump/sync (when releasing): `npm run version:bump:patch` then
  `npm run version:sync`.

## Coding Style & Naming Conventions

- Python uses 4-space indentation and ruff with 120-char lines.
- Prefer `snake_case` for modules/scripts and `PascalCase` for test classes.
- Test files follow `test_*.py` and live under `tests/`.

## Testing Guidelines

- Pytest is configured via `pyproject.toml` with coverage for `src/automation`
  and minimum 58%.
- Use markers (`unit`, `integration`, `slow`, `security`, etc.) to scope runs.

## Commit & Pull Request Guidelines

- Use Conventional Commits: `<type>(<scope>): <subject>`; types include `feat`,
  `fix`, `docs`, `refactor`, `test`, `chore`.
- The PR template in `.github/PULL_REQUEST_TEMPLATE.md` is required: include
  description, change type checklist, linked issues, testing steps, and
  screenshots for UI changes.
- Ensure pre-commit and CI checks pass before requesting review.

## Security & Configuration Tips

- Do not commit secrets; follow `SECURITY.md` and `.github/SECRETS.md`.
- Workflow changes should align with `.github/WORKFLOW_STANDARDS.md`.

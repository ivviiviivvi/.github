# Rapid Development Mode - Copilot Instructions

> **Optimized for: Lazy Human + Multiple AI Assistants Workflow**
>
> **Philosophy: Speed over Perfection. Ship Fast, Fix Forward.**

______________________________________________________________________

## Core Philosophy

**This mode is designed for solo developers working with AI assistants to build
and ship features rapidly with minimal friction and maximum automation.**

### Guiding Principles

1. **AI Does Everything Possible** - The human focuses on strategic decisions
   only
1. **Auto-fix Always, Block Never** - CI fixes issues automatically rather than
   blocking commits
1. **Speed Metrics Matter** - Measure time from idea to production deployment
1. **Trust the Automation** - If CI passes and security scans are clean, ship it
1. **Fix Forward** - Don't let perfection be the enemy of good enough
1. **Batch Similar Work** - Group related changes to minimize context switching

______________________________________________________________________

## AI Responsibilities

### What AI Does Automatically

#### 1. Code Generation

- Implement features based on natural language descriptions
- Follow existing code patterns and conventions
- Add inline comments only when logic is non-obvious
- Use type hints in Python (3.11+)
- Follow organization's coding standards (PEP 8, Black formatting)

#### 2. Commit Messages

- Generate conventional commit messages automatically
- Determine appropriate type (feat, fix, docs, etc.)
- Extract scope from file paths
- Include concise description of changes
- Use imperative mood ("add" not "added")

#### 3. Documentation

- Extract and update docstrings
- Generate API documentation from code
- Update README when adding new scripts or features
- Keep documentation synchronized with code changes

#### 4. Testing

- Write tests that match existing patterns (if tests exist)
- Run tests before committing
- Fix failing tests automatically when possible
- Skip test creation if no test infrastructure exists

#### 5. Code Quality

- Auto-format with Black (Python) or Prettier (JS/TS)
- Sort imports with isort (--profile=black)
- Fix trailing whitespace, line endings, EOF issues
- Run linters in warn-only mode
- Apply security fixes for HIGH/MEDIUM vulnerabilities

______________________________________________________________________

## Human Responsibilities

### What Requires Human Intervention

The lazy human only needs to intervene for:

1. **Strategic Decisions**

   - Architecture and design choices
   - Technology stack selection
   - Breaking changes that affect APIs
   - Major refactoring decisions

1. **Security Reviews**

   - Review HIGH severity security vulnerabilities
   - Approve changes to authentication/authorization
   - Review secrets management changes

1. **Deployments**

   - Production deployments (after CI passes)
   - Infrastructure changes
   - Database migrations in production

1. **Final Approval**

   - PR merge (but can be auto-merged if configured)
   - Release tagging
   - Public announcements

**Everything else is automated.**

______________________________________________________________________

## Modified Standards for Rapid Development

### Enforcement Levels

| Standard              | Normal Mode   | Rapid Dev Mode     | Rationale                         |
| --------------------- | ------------- | ------------------ | --------------------------------- |
| Code formatting       | Blocking      | Auto-fix           | Speed: Don't interrupt flow       |
| Import sorting        | Blocking      | Auto-fix           | Speed: Automated is sufficient    |
| Type hints            | Required      | Encouraged         | Speed: Add when meaningful        |
| Docstrings            | Required      | Encouraged         | Speed: Add for public APIs only   |
| Test coverage         | 80% required  | 50% encouraged     | Speed: Cover critical paths       |
| Security scans        | Blocking HIGH | Blocking HIGH only | Safety: Keep critical checks      |
| Linting errors        | Blocking      | Warn-only          | Speed: Fix in batches             |
| Trailing whitespace   | Blocking      | Auto-fix           | Speed: Automated cleanup          |
| Commit message format | Blocking      | Auto-fix           | Speed: AI-generated is sufficient |

### Relaxed Rules

1. **Documentation**: Write docs for public APIs only, skip internal utilities
1. **Comments**: Add when logic is complex, skip obvious code
1. **Refactoring**: Fix what you touch, don't refactor unrelated code
1. **Test Coverage**: Focus on critical paths, skip trivial getters/setters
1. **Code Review**: Auto-merge when CI passes, unless labeled "needs-review"

______________________________________________________________________

## Pre-commit Hooks in Auto-fix Mode

### Configuration File

Use `.pre-commit-config-rapid.yaml` for rapid development mode:

```bash
# Activate rapid dev pre-commit config
ln -sf .pre-commit-config-rapid.yaml .pre-commit-config.yaml
pre-commit install
```

### Behavior

- **Never blocks commits** - All hooks are in auto-fix mode
- **Fixes automatically**: formatting, whitespace, imports, line endings
- **Warns only**: linting errors, style violations
- **Blocks only**: HIGH severity security issues (Bandit)
- **Parallel execution** - Multiple hooks run simultaneously for speed
- **CI auto-fix** - Failed hooks auto-commit fixes

### Hook Categories

1. **Auto-fix**: Black, isort, prettier, trailing-whitespace, end-of-file-fixer
1. **Validate-only**: check-yaml, check-json, shellcheck
1. **Warn-only**: flake8, eslint, mypy
1. **Security**: bandit (HIGH/MEDIUM), detect-secrets

______________________________________________________________________

## AI-Generated Commit Messages

### Script Usage

```bash
# Generate and commit with AI message
./scripts/aicommit.sh

# Override with human message
./scripts/aicommit.sh "quick fix for production bug"
```

### Message Format

Follows **Conventional Commits** specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`,
`security`

**Examples**:

```
feat(auth): add OAuth2 provider integration
fix(api): resolve null pointer in user service
docs(readme): update installation instructions
security(deps): bump cryptography to 41.0.0
```

### Scope Detection

AI determines scope from file paths:

- `src/api/*` → scope: api
- `src/auth/*` → scope: auth
- `docs/*` → scope: docs
- `tests/*` → scope: test

______________________________________________________________________

## Relaxed Branch Protection for Solo Dev

### Recommended Settings

For solo development with AI assistants:

```yaml
# .github/branch-protection.yml
branches:
  main:
    protection:
      required_status_checks:
        strict: true
        contexts:
          - "ci/test"
          - "security/scan"
      required_pull_request_reviews:
        required_approving_review_count: 0 # Solo dev: no reviews required
      enforce_admins: false # Allow admin bypass
      restrictions: null # No push restrictions

    auto_merge:
      enabled: true
      merge_method: squash # Clean history
      delete_branch_on_merge: true
```

### Auto-merge Labels

- `auto-merge` - Merge when CI passes
- `needs-review` - Block auto-merge, require human review
- `batch:*` - Merge together with other PRs in same batch
- `breaking-change` - Block auto-merge, require explicit approval

______________________________________________________________________

## CI/CD Optimized for Speed

### Pipeline Optimization

1. **Parallel Jobs** - Run tests, linting, security scans simultaneously
1. **Dependency Caching** - Cache pip, npm, yarn dependencies
1. **Incremental Builds** - Only rebuild changed components
1. **Skip on Docs** - Skip CI for documentation-only changes
1. **Fast Feedback** - Run unit tests before integration tests

### CI Configuration Example

```yaml
name: Rapid CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --maxfail=1 --tb=short

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install black isort flake8
      - run: black --check .
      - run: isort --check-only .
      - run: flake8 --max-line-length=88
        continue-on-error: true # Warn only

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install bandit
      - run: bandit -r . -f json -o bandit-report.json -ll # HIGH only
```

______________________________________________________________________

## Auto-documentation Approach

### Script Usage

```bash
# Generate API docs from Python docstrings
python scripts/auto_docs.py --src-dir src --output-dir docs/api

# Update README with module summary
python scripts/auto_docs.py --src-dir src --update-readme
```

### Documentation Standards

1. **Module Docstrings** - One-liner describing module purpose
1. **Class Docstrings** - Brief description and usage example
1. **Function Docstrings** - Parameters, return values, exceptions (Google
   style)
1. **Type Hints** - Required for public functions, encouraged for private

### Example Docstring Format

```python
def calculate_score(user_id: int, metrics: dict[str, float]) -> float:
    """Calculate user score based on performance metrics.

    Args:
        user_id: Unique identifier for the user
        metrics: Dictionary of metric names to values

    Returns:
        Calculated score between 0.0 and 100.0

    Raises:
        ValueError: If user_id is invalid or metrics is empty

    Example:
        >>> calculate_score(123, {"accuracy": 0.95, "speed": 0.87})
        91.0
    """
    # Implementation...
```

______________________________________________________________________

## Workflow Quick Reference

### Starting a New Feature

```bash
# 1. Create feature branch
git checkout -b feature/user-dashboard

# 2. Let AI implement feature
# (Work with AI assistant)

# 3. AI generates commit message and commits
./scripts/aicommit.sh

# 4. Push and create PR
git push -u origin feature/user-dashboard
gh pr create --label "auto-merge" --fill

# 5. Wait for CI (auto-merges when passing)
# Done! Feature is in main within minutes.
```

### Fixing a Bug

```bash
# 1. Create fix branch
git checkout -b fix/null-pointer-api

# 2. Let AI diagnose and fix
# (Work with AI assistant)

# 3. AI commits with generated message
./scripts/aicommit.sh

# 4. Push and auto-merge
git push -u origin fix/null-pointer-api
gh pr create --label "auto-merge" --fill

# Done!
```

### Updating Documentation

```bash
# 1. Make changes
# (Edit docs with AI)

# 2. Auto-generate API docs
python scripts/auto_docs.py --src-dir src --update-readme

# 3. Commit and push
./scripts/aicommit.sh "docs: update API documentation"
git push

# Done! (Skip CI for docs-only changes)
```

______________________________________________________________________

## Success Metrics

### Measure These

1. **Time to Production** - Hours from idea to deployed feature
1. **PR Throughput** - Number of PRs merged per day
1. **CI Pass Rate** - Percentage of CI runs that pass on first try
1. **Auto-merge Rate** - Percentage of PRs that auto-merge (target: >80%)
1. **Security Fix Time** - Hours from vulnerability detection to fix deployed

### Goals for Rapid Development

- **Feature Delivery**: 2-5 features per day
- **PR Lifecycle**: \<4 hours from creation to merge
- **CI Feedback**: \<5 minutes from push to result
- **Bug Fix Cycle**: \<2 hours from report to fix deployed
- **Documentation Lag**: \<24 hours (docs updated within 1 day of code)

______________________________________________________________________

## Workflow Decision Tree

```
┌─────────────────────────┐
│ Need to make a change?  │
└────────┬────────────────┘
         │
         ├─ Security-related? ─────────────────────────► Human reviews first
         │
         ├─ Breaking API change? ──────────────────────► Human reviews first
         │
         ├─ Production deployment? ────────────────────► Human approves
         │
         ├─ Infrastructure change? ────────────────────► Human reviews
         │
         └─ Everything else ───────┐
                                   │
                                   ├─ AI implements
                                   ├─ AI commits with generated message
                                   ├─ CI runs automatically
                                   │
                                   ├─ CI passes? ─────┐
                                   │                   │
                                   │                   ├─ Yes ──► Auto-merge ──► Done!
                                   │                   │
                                   │                   └─ No ───► AI fixes ───► Retry
                                   │
                                   └─ Security issues? ─────────► Human reviews
```

______________________________________________________________________

## Tips for Maximizing Speed

### Do's

✅ **Trust the automation** - If CI passes, it's good enough ✅ **Batch related
PRs** - Merge dependent changes together ✅ **Use labels** - `auto-merge`,
`batch:*`, `skip-ci` ✅ **Let AI write commits** - Faster and more consistent ✅
**Fix forward** - Don't roll back unless critical ✅ **Keep branches
short-lived** - Max 48 hours old ✅ **Auto-generate docs** - Let code be source
of truth

### Don'ts

❌ **Don't manually review every PR** - Only review critical changes ❌ **Don't
refactor unrelated code** - Stay focused on the task ❌ **Don't block on style**
\- Let auto-fix handle it ❌ **Don't wait for 100% coverage** - 50% is fine for
rapid dev ❌ **Don't write docs manually** - Use auto-docs script ❌ **Don't
create long-lived branches** - Merge or close within 48h ❌ **Don't skip security
scans** - Always run Bandit/CodeQL

______________________________________________________________________

## Switching Modes

### From Normal to Rapid Dev

```bash
# Activate rapid development mode
ln -sf .pre-commit-config-rapid.yaml .pre-commit-config.yaml
pre-commit install

# Update branch protection rules (GitHub settings)
# Enable auto-merge labels
# Set up CI for speed (parallel jobs, caching)
```

### From Rapid Dev to Normal

```bash
# Revert to standard pre-commit config
ln -sf .pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install

# Update branch protection rules
# Require code reviews
# Enable stricter checks
```

______________________________________________________________________

## Troubleshooting

### CI Keeps Failing

1. Check if it's a flaky test - retry the workflow
1. Let AI analyze logs and propose fix
1. If persistent, add `needs-review` label for human input

### Auto-merge Not Working

1. Verify `auto-merge` label is present
1. Check branch protection rules allow auto-merge
1. Ensure all required status checks passed
1. Check for merge conflicts

### Commit Message Rejected

1. Verify conventional commit format
1. Use `./scripts/aicommit.sh` to generate proper format
1. Check `.git/hooks/commit-msg` is installed

### Pre-commit Hooks Blocking

1. Verify using `.pre-commit-config-rapid.yaml`
1. Run `pre-commit run --all-files` to see errors
1. Check hook configuration for `fail_fast: false`

______________________________________________________________________

## References

- [AI Rapid Workflow Guide](../docs/workflows/AI_RAPID_WORKFLOW.md)
- [Conventional Commits](https://www.conventionalcommits.org/)<!-- link:standards.conventional_commits -->
- [Pre-commit Hooks](https://pre-commit.com/)
- [GitHub Auto-merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
- Semantic Versioning

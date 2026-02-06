# Best Practices Guide

> **Comprehensive best practices for contributing to and maintaining the
> {{ORG_NAME}}/.github repository**

This guide consolidates best practices across all areas: code quality,
documentation, workflows, testing, security, and collaboration.

______________________________________________________________________

## Table of Contents

- [Code Quality](#code-quality)
- [Documentation](#documentation)
- [Testing](#testing)
- [Workflows & CI/CD](#workflows--cicd)
- [Security](#security)
- [Git & Version Control](#git--version-control)
- [Collaboration](#collaboration)
- [Performance](#performance)
- [Maintenance](#maintenance)

______________________________________________________________________

## Code Quality

### Python Code

#### ✅ Do

- **Use type hints** for all function parameters and return values

  ```python
  def process_data(items: List[str], threshold: int = 10) -> dict:
      return {"count": len(items)}
  ```

- **Write comprehensive docstrings** using Google or NumPy style

  ```python
  def calculate_average(numbers: List[float]) -> float:
      """
      Calculate the arithmetic mean of a list of numbers.

      Args:
          numbers: List of numeric values to average

      Returns:
          The arithmetic mean as a float

      Raises:
          ValueError: If the numbers list is empty
      """
      if not numbers:
          raise ValueError("Cannot calculate average of empty list")
      return sum(numbers) / len(numbers)
  ```

- **Follow PEP 8** naming conventions

  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

- **Use f-strings** for string formatting

  ```python
  name = "Alice"
  age = 30
  message = f"{name} is {age} years old"  # ✅ Good
  message = "%s is %d years old" % (name, age)  # ❌ Avoid
  ```

- **Handle errors explicitly**

  ```python
  try:
      result = risky_operation()
  except SpecificError as e:
      logger.error(f"Operation failed: {e}")
      raise
  ```

- **Use context managers** for resource management

  ```python
  with open('file.txt', 'r') as f:
      data = f.read()
  ```

#### ❌ Don't

- Don't use bare `except:` clauses

  ```python
  try:
      something()
  except:  # ❌ Too broad
      pass
  ```

- Don't ignore lint warnings without good reason

- Don't commit commented-out code

- Don't use mutable default arguments

  ```python
  def bad_function(items=[]):  # ❌ Mutable default
      items.append(1)
      return items

  def good_function(items=None):  # ✅ Correct
      if items is None:
          items = []
      items.append(1)
      return items
  ```

### Shell Scripts

#### ✅ Do

- **Use `set -e`** to exit on errors

  ```bash
  #!/bin/bash
  set -e  # Exit on any error
  set -u  # Error on undefined variables
  set -o pipefail  # Catch errors in pipelines
  ```

- **Quote variables** to handle spaces

  ```bash
  filename="my file.txt"
  cat "$filename"  # ✅ Handles spaces
  cat $filename    # ❌ Breaks with spaces
  ```

- **Use `[[` for conditionals**

  ```bash
  if [[ -f "$file" ]]; then  # ✅ Modern syntax
      echo "File exists"
  fi
  ```

- **Add usage functions**

  ```bash
  usage() {
      echo "Usage: $0 [OPTIONS] <arg>"
      echo "  -h, --help    Show this help"
      echo "  -v, --verbose Enable verbose output"
      exit 1
  }
  ```

#### ❌ Don't

- Don't use `cd` without error checking

  ```bash
  cd /path || exit 1  # ✅ Good
  cd /path            # ❌ Might fail silently
  ```

- Don't parse `ls` output

  ```bash
  # ❌ Bad
  for file in $(ls *.txt); do
      echo "$file"
  done

  # ✅ Good
  for file in *.txt; do
      echo "$file"
  done
  ```

______________________________________________________________________

## Documentation

### Writing Style

#### ✅ Do

- **Write for your audience** - assume basic technical knowledge but explain
  organization-specific concepts
- **Use active voice** - "Run the command" not "The command should be run"
- **Be concise** - remove unnecessary words
- **Use examples** liberally
- **Add context** - explain why, not just what
- **Link to related docs** - help readers find more information
- **Update dates** - add "Last Updated" footers
- **Use proper markdown** - headings, lists, code blocks with language tags

#### ❌ Don't

- Don't assume expert knowledge
- Don't use jargon without explanation
- Don't write walls of text (use lists, tables, code blocks)
- Don't forget to update existing docs when behavior changes
- Don't leave broken links

### Documentation Structure

**Every documentation file should have**:

1. **Title** (H1) - One per file
1. **Brief description** - What is this doc about?
1. **Table of contents** - For files >200 lines
1. **Clear sections** - Use H2 and H3 headings
1. **Code examples** - Show, don't just tell
1. **Troubleshooting** - Address common issues
1. **Related resources** - Link to other docs
1. **Footer** - Last updated date, maintainer

**Example structure**:

```markdown
# Title

> **Brief description with key takeaway**

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content with examples...

## Troubleshooting

Common issues and solutions...

## Related Resources

- [Other Guide](link.md)

---

_Last Updated: 2026-01-14_
_Maintained by: Team Name_
```

### Code Comments

#### ✅ Do

- **Explain why, not what**

  ```python
  # ✅ Good - explains reasoning
  # Use binary search because dataset can be millions of records
  result = binary_search(data, target)

  # ❌ Bad - states the obvious
  # Call binary search
  result = binary_search(data, target)
  ```

- **Document complex logic**

- **Add TODO comments** with tracking info

  ```python
  # TODO(username): Optimize this algorithm (Issue #123)
  ```

- **Use docstrings** for public APIs

#### ❌ Don't

- Don't comment obvious code
- Don't leave commented-out code
- Don't use comments to disable code long-term (use feature flags)

______________________________________________________________________

## Testing

### Test Coverage

**Coverage requirements**:

| Code Type          | Minimum Coverage |
| ------------------ | ---------------- |
| Security-critical  | 100%             |
| Core functionality | 80%              |
| Utilities          | 70%              |

#### ✅ Do

- **Write tests first** (TDD) for new features

- **Test behavior, not implementation**

  ```python
  # ✅ Good - tests behavior
  def test_user_can_login():
      response = login("user", "pass")
      assert response.status_code == 200
      assert "token" in response.json()

  # ❌ Bad - tests implementation
  def test_login_calls_auth_service():
      login("user", "pass")
      assert auth_service.authenticate.called
  ```

- **Use descriptive test names**

  ```python
  def test_empty_list_raises_value_error():  # ✅ Clear
      ...

  def test_1():  # ❌ Unclear
      ...
  ```

- **Use pytest markers**

  ```python
  @pytest.mark.unit
  @pytest.mark.security
  def test_ssrf_protection():
      ...
  ```

- **Use fixtures** for common setup

- **Parametrize** for multiple similar tests

  ```python
  @pytest.mark.parametrize("input,expected", [
      ("hello", "HELLO"),
      ("world", "WORLD"),
      ("", ""),
  ])
  def test_uppercase(input, expected):
      assert uppercase(input) == expected
  ```

#### ❌ Don't

- Don't test internal implementation details
- Don't create interdependent tests
- Don't skip tests without documenting why
- Don't commit failing tests
- Don't mock everything (test real interactions when safe)

### Test Organization

```
tests/
├── unit/              # Fast, isolated tests
│   ├── test_feature1.py
│   └── test_feature2.py
├── integration/       # Tests with external dependencies
│   └── test_workflow.py
├── conftest.py        # Shared fixtures
└── pytest.ini         # Configuration
```

______________________________________________________________________

## Workflows & CI/CD

### Workflow Design

#### ✅ Do

- **Pin actions to SHA**

  ```yaml
  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4
  ```

- **Set explicit permissions**

  ```yaml
  permissions:
    contents: read
    pull-requests: write
  ```

- **Add timeouts**

  ```yaml
  jobs:
    build:
      timeout-minutes: 10
  ```

- **Use concurrency groups**

  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```

- **Enable caching**

  ```yaml
  - uses: actions/setup-python@v5
    with:
      python-version: "3.11"
      cache: "pip"
  ```

- **Provide clear job names**

  ```yaml
  jobs:
    test-python-311: # ✅ Clear
      name: "Test with Python 3.11"
  ```

#### ❌ Don't

- Don't use `actions/checkout@v4` (use SHA)
- Don't grant excessive permissions
- Don't skip timeout configuration
- Don't allow unlimited concurrent runs
- Don't hardcode secrets in workflows
- Don't run expensive workflows on every push

### Reusable Workflows

**When to create reusable workflows**:

- Logic used in 3+ workflows
- Complex multi-step processes
- Organization-wide standards

**Example**:

```yaml
# .github/workflows/reusable/test.yml
name: Reusable Test

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@SHA
      - uses: actions/setup-python@SHA
        with:
          python-version: ${{ inputs.python-version }}
      - run: pytest
```

______________________________________________________________________

## Security

### Code Security

#### ✅ Do

- **Validate all inputs**

  ```python
  def process_url(url: str) -> dict:
      # Validate URL format
      if not url.startswith(('http://', 'https://')):
          raise ValueError("Invalid URL scheme")

      # Block private IPs
      if is_private_ip(url):
          raise ValueError("Private IP access denied")

      return fetch_url(url)
  ```

- **Use environment variables** for secrets

  ```python
  api_key = os.getenv('API_KEY')
  if not api_key:
      raise ValueError("API_KEY not set")
  ```

- **Sanitize output** before logging

  ```python
  logger.info(f"Processing file: {sanitize(filename)}")
  ```

- **Use latest security patches**

  ```bash
  pip install --upgrade package-name
  ```

#### ❌ Don't

- Don't hardcode secrets

  ```python
  API_KEY = "sk_live_abc123"  # ❌ NEVER do this  # pragma: allowlist secret
  ```

- Don't trust user input

- Don't log sensitive data

- Don't use `eval()` or `exec()`

- Don't run commands without validation

  ```python
  os.system(f"cat {user_input}")  # ❌ Command injection risk
  ```

### Workflow Security

#### ✅ Do

- **Pin actions to SHA**

- **Validate inputs**

  ```yaml
  on:
    workflow_dispatch:
      inputs:
        environment:
          type: choice
          options: [dev, staging, prod]
  ```

- **Use GITHUB_TOKEN** sparingly

- **Audit third-party actions**

#### ❌ Don't

- Don't use `pull_request_target` without extreme caution
- Don't expose secrets in logs
- Don't trust PR code in `pull_request_target` workflows
- Don't use `write-all` permissions

______________________________________________________________________

## Git & Version Control

### Commit Messages

#### ✅ Do

**Follow conventional commits**:

```
type(scope): brief description

Detailed explanation if needed.

Fixes #123
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding tests
- `refactor`: Code refactoring
- `chore`: Maintenance
- `ci`: CI/CD changes

**Examples**:

```bash
# Good commits
git commit -m "feat(auth): add OAuth2 support

Implements OAuth2 authentication flow with Google and GitHub providers.

Closes #456"

git commit -m "fix(crawler): prevent SSRF on private IPs

Blocks access to 127.0.0.1, 10.0.0.0/8, and other private ranges.

Fixes #789"

git commit -m "docs: update contribution guidelines"

# Bad commits
git commit -m "fixed stuff"           # ❌ Too vague
git commit -m "WIP"                   # ❌ Don't commit WIP
git commit -m "asdf"                  # ❌ Meaningless
```

#### ❌ Don't

- Don't commit work-in-progress
- Don't use vague messages
- Don't commit large unrelated changes together
- Don't forget to reference issues

### Branching Strategy

#### ✅ Do

- **Use descriptive branch names**

  ```bash
  git checkout -b feature/add-oauth
  git checkout -b fix/ssrf-vulnerability
  git checkout -b docs/update-testing-guide
  ```

- **Keep branches short-lived** (\< 1 week ideal)

- **Rebase before merging** to keep history clean

  ```bash
  git fetch origin
  git rebase origin/main
  ```

- **Delete merged branches**

  ```bash
  git branch -d feature/completed
  git push origin --delete feature/completed
  ```

#### ❌ Don't

- Don't use ambiguous branch names (`fix`, `update`, `new`)
- Don't keep branches open for months
- Don't force push to `main`
- Don't work directly on `main`

______________________________________________________________________

## Collaboration

### Pull Requests

#### ✅ Do

- **Write clear PR descriptions**

  ```markdown
  ## Description

  This PR adds OAuth2 authentication support.

  ## Changes

  - Added OAuth2 provider classes
  - Updated authentication middleware
  - Added tests for new providers

  ## Testing

  - ✅ All unit tests pass
  - ✅ Integration tests added
  - ✅ Manual testing completed

  Closes #456
  ```

- **Keep PRs focused** - one feature/fix per PR

- **Request reviews** from appropriate team members

- **Respond to feedback** promptly

- **Keep PRs small** (\< 400 lines ideal)

- **Link to issues**

- **Update documentation** with code changes

#### ❌ Don't

- Don't create giant PRs (>1000 lines)
- Don't mix unrelated changes
- Don't argue with reviewers (discuss respectfully)
- Don't force merge without approval
- Don't ignore failing CI checks

### Code Review

#### ✅ Do (as reviewer)

- **Be constructive and kind**

  ```
  ✅ "Consider using a dict here for O(1) lookups"
  ❌ "This is wrong"
  ```

- **Explain your reasoning**

- **Approve good work** promptly

- **Ask questions** if unclear

- **Suggest improvements** with examples

- **Focus on important issues**

#### ❌ Don't (as reviewer)

- Don't nitpick formatting (linters handle that)
- Don't block PRs for personal preferences
- Don't request changes without explanation
- Don't ignore security issues

______________________________________________________________________

## Performance

### Code Performance

#### ✅ Do

- **Profile before optimizing**

  ```python
  import cProfile
  cProfile.run('my_function()')
  ```

- **Use appropriate data structures**

  - `set` for membership testing
  - `dict` for key-value lookups
  - `deque` for queues

- **Cache expensive operations**

  ```python
  from functools import lru_cache

  @lru_cache(maxsize=128)
  def expensive_computation(n):
      ...
  ```

- **Use generators** for large datasets

  ```python
  def read_large_file(filename):
      with open(filename) as f:
          for line in f:  # Generator, doesn't load entire file
              yield line.strip()
  ```

#### ❌ Don't

- Don't optimize prematurely

- Don't sacrifice readability for minor gains

- Don't ignore algorithmic complexity

  ```python
  # ❌ O(n²) - quadratic time
  for i in items:
      if i in other_list:  # O(n) for each iteration
          ...

  # ✅ O(n) - linear time
  other_set = set(other_list)  # O(n) once
  for i in items:
      if i in other_set:  # O(1) for each iteration
          ...
  ```

### Workflow Performance

#### ✅ Do

- **Use caching** (dependencies, build artifacts)
- **Run jobs in parallel** when possible
- **Use concurrency** to cancel old runs
- **Limit workflow scope** with path filters

#### ❌ Don't

- Don't run tests on every file change
- Don't duplicate expensive operations
- Don't forget to timeout long-running jobs

______________________________________________________________________

## Maintenance

### Regular Tasks

**Weekly**:

- [ ] Review workflow health dashboard
- [ ] Check for failing workflows
- [ ] Review open pull requests
- [ ] Update documentation if needed

**Monthly**:

- [ ] Update dependencies
- [ ] Review security scan results
- [ ] Check test coverage trends
- [ ] Clean up old branches
- [ ] Update pinned actions

**Quarterly**:

- [ ] Full security audit
- [ ] Review and archive old issues
- [ ] Update organizational standards
- [ ] Review and optimize workflows
- [ ] Update documentation structure

### Technical Debt

#### ✅ Do

- **Document technical debt** with TODO/FIXME comments
- **Create issues** for known problems
- **Prioritize** based on impact
- **Plan regular debt reduction** sprints
- **Refactor incrementally**

#### ❌ Don't

- Don't ignore growing technical debt
- Don't defer all refactoring
- Don't create brittle workarounds
- Don't sacrifice quality for speed (long-term)

______________________________________________________________________

## Quick Reference Checklist

### Before Committing

- [ ] Tests pass locally (`pytest tests/ -v`)
- [ ] Linters pass (`flake8`, `black`, `mypy`)
- [ ] Coverage adequate (`pytest --cov`)
- [ ] Documentation updated
- [ ] Commit message follows convention
- [ ] No secrets or sensitive data
- [ ] Pre-commit hooks pass

### Before Creating PR

- [ ] Branch is up to date with `main`
- [ ] All commits are meaningful
- [ ] PR description is clear
- [ ] Linked to relevant issue(s)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] CI checks pass

### Before Merging PR

- [ ] All required approvals received
- [ ] CI checks pass
- [ ] No unresolved comments
- [ ] Branch is up to date
- [ ] Documentation reviewed
- [ ] Breaking changes communicated

______________________________________________________________________

## Additional Resources

- [New Contributor Guide](NEW_CONTRIBUTOR_GUIDE.md)
- [Testing Best Practices](testing-best-practices.md)
- [Monitoring Guide](monitoring.md)
- [Common Tasks Runbook](common-tasks-runbook.md)
- [Contributing Guidelines](../governance/CONTRIBUTING.md)

______________________________________________________________________

_Last Updated: 2026-01-14_ _Maintained by: Documentation Team_

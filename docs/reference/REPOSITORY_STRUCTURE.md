# Repository Structure Standards

This document defines the organization-wide standards for repository structure,
file naming, and content placement.

## Core Principles

### 1. Separation of Concerns

- **Source code** belongs in language-specific directories (`src/`, `lib/`,
  `pkg/`)
- **Documentation** belongs in `docs/`
- **Tests** belong in `tests/` or alongside source (language-dependent)
- **Configuration** belongs in root or `.config/`
- **CI/CD** belongs in `.github/`

### 2. Hierarchical Organization

```
repository/
├── .github/           # GitHub-specific (workflows, templates)
├── docs/              # All documentation
├── src/ or lib/       # Source code
├── tests/             # Test files
├── scripts/           # Utility scripts
└── [config files]     # Root-level configuration only
```

### 3. Progressive Disclosure

- Root directory shows only essential files
- Detailed content lives in subdirectories
- READMEs at each level explain that level's contents

### 4. Convention Over Configuration

- Follow language ecosystem conventions
- Use standard directory names
- Minimize custom organization patterns

______________________________________________________________________

## Standard Repository Layout

### Root Directory

The root should contain **only essential files** (max 15):

```
repository/
├── .github/                 # Required: GitHub configuration
├── .gitignore               # Required: Git ignore rules
├── LICENSE                  # Required: License file
├── README.md                # Required: Project overview
├── CHANGELOG.md             # Recommended: Version history
├── CONTRIBUTING.md          # Recommended: Contribution guide (or in docs/)
├── SECURITY.md              # Recommended: Security policy
├── pyproject.toml           # Language config (Python)
├── package.json             # Language config (Node.js)
├── go.mod                   # Language config (Go)
├── Cargo.toml               # Language config (Rust)
└── Makefile                 # Build automation (optional)
```

**Do NOT put in root:**

- Status reports (`*STATUS*.md`, `*COMPLETE*.md`)
- Test results (`test-results*.json`)
- Temporary files
- Build artifacts
- Multiple README variants

### Documentation Directory (`docs/`)

```
docs/
├── INDEX.md                 # Documentation index/table of contents
├── guides/                  # How-to guides and tutorials
│   ├── GETTING_STARTED.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
├── reference/               # Technical reference docs
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── CONFIGURATION.md
├── governance/              # Process and policy docs
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── DECISION_RECORDS.md
├── standards/               # Standards and specifications
│   └── [standard docs]
└── templates/               # Document templates
    └── [templates]
```

### GitHub Directory (`.github/`)

```
.github/
├── workflows/               # GitHub Actions workflows
│   ├── ci.yml
│   ├── release.yml
│   └── scheduled.yml
├── ISSUE_TEMPLATE/          # Issue templates
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md # PR template
├── CODEOWNERS               # Code ownership rules
├── dependabot.yml           # Dependency updates
├── scripts/                 # Workflow helper scripts
└── docs/                    # GitHub-specific docs
```

### Test Directory (`tests/`)

```
tests/
├── unit/                    # Unit tests
├── integration/             # Integration tests
├── e2e/                     # End-to-end tests
├── fixtures/                # Test data/fixtures
├── conftest.py              # Pytest configuration (Python)
└── README.md                # Test documentation
```

### Scripts Directory (`scripts/`)

```
scripts/
├── setup.sh                 # Environment setup
├── build.sh                 # Build automation
├── deploy.sh                # Deployment scripts
├── validate-*.sh            # Validation scripts
└── README.md                # Script documentation
```

### Archive Directory (`archive/`)

For historical/completed content:

```
archive/
├── README.md                # Archive index
├── deployment/              # Old deployment artifacts
├── status-reports/          # Completed status reports
├── test-results/            # Historical test results
└── [dated-subdirs]/         # Time-based archives
```

### Reports Directory (`reports/`)

For generated reports and analysis:

```
reports/
├── coverage/                # Code coverage reports
├── analysis/                # Analysis outputs
├── status/                  # Status reports
└── metrics/                 # Metrics and dashboards
```

______________________________________________________________________

## Language-Specific Layouts

### Python Projects

```
repository/
├── src/
│   └── package_name/        # Main package
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── conftest.py
│   └── test_module.py
├── docs/
├── pyproject.toml           # Project configuration
├── setup.py                 # Legacy setup (if needed)
└── requirements.txt         # Dependencies (if not using pyproject)
```

### Node.js Projects

```
repository/
├── src/                     # Source code
│   ├── index.js
│   └── components/
├── tests/ or __tests__/     # Tests
├── docs/
├── package.json             # Project configuration
├── tsconfig.json            # TypeScript config (if applicable)
└── .eslintrc.js             # Linting config
```

### Go Projects

```
repository/
├── cmd/                     # Main applications
│   └── app/
│       └── main.go
├── pkg/                     # Public packages
├── internal/                # Private packages
├── docs/
├── go.mod                   # Module definition
└── go.sum                   # Dependency checksums
```

### Java/Kotlin Projects

```
repository/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── docs/
├── build.gradle             # Gradle config
└── pom.xml                  # Maven config (alternative)
```

______________________________________________________________________

## File Naming Conventions

### Documentation Files

| Type      | Convention            | Example              |
| --------- | --------------------- | -------------------- |
| Guides    | UPPER_SNAKE_CASE.md   | `GETTING_STARTED.md` |
| Reference | UPPER_SNAKE_CASE.md   | `API_REFERENCE.md`   |
| Indexes   | INDEX.md or README.md | `docs/INDEX.md`      |

### Source Code Files

| Language              | Convention      | Example            |
| --------------------- | --------------- | ------------------ |
| Python                | snake_case.py   | `user_service.py`  |
| JavaScript/TypeScript | camelCase.js    | `userService.js`   |
| Go                    | lowercase.go    | `userservice.go`   |
| Java/Kotlin           | PascalCase.java | `UserService.java` |
| Rust                  | snake_case.rs   | `user_service.rs`  |

### Configuration Files

| Type     | Convention      | Example              |
| -------- | --------------- | -------------------- |
| Dotfiles | .filename       | `.gitignore`, `.env` |
| YAML     | kebab-case.yml  | `docker-compose.yml` |
| JSON     | kebab-case.json | `tsconfig.json`      |
| TOML     | kebab-case.toml | `pyproject.toml`     |

### Scripts

| Type    | Convention        | Example              |
| ------- | ----------------- | -------------------- |
| Shell   | kebab-case.sh     | `run-tests.sh`       |
| Python  | snake_case.py     | `run_migration.py`   |
| General | verb-noun pattern | `validate-schema.sh` |

______________________________________________________________________

## Content Placement Guidelines

### What Goes Where

| Content Type      | Location                        | Example                |
| ----------------- | ------------------------------- | ---------------------- |
| Project overview  | `README.md` (root)              | Features, installation |
| API documentation | `docs/reference/`               | API endpoints, schemas |
| User guides       | `docs/guides/`                  | Tutorials, how-tos     |
| Architecture      | `docs/reference/`               | System design          |
| Contributing      | `docs/governance/` or root      | Contribution guide     |
| Status reports    | `reports/status/` or `archive/` | Progress updates       |
| Test results      | `reports/` or `.gitignore`      | Coverage, results      |
| Build artifacts   | `.gitignore`                    | Never commit           |
| Secrets           | `.gitignore` + secrets manager  | Never commit           |

### Root Directory Rules

**DO include:**

- Essential config files (1 per tool/language)
- LICENSE, README.md, CHANGELOG.md
- Language manifest (package.json, pyproject.toml, etc.)
- .gitignore, .gitattributes

**DO NOT include:**

- Multiple status/completion files
- Test result files
- Temporary/generated files
- Deployment artifacts
- Multiple similar config files

______________________________________________________________________

## Anti-Patterns to Avoid

### 1. Root Directory Clutter

**Bad:**

```
repository/
├── README.md
├── STATUS.md
├── COMPLETE.md
├── PHASE1_DONE.md
├── test-results.json
├── test-results-2.json
└── ... (30+ files)
```

**Good:**

```
repository/
├── README.md
├── docs/
├── reports/
│   └── status/
└── archive/
```

### 2. Flat Documentation

**Bad:**

```
docs/
├── getting-started.md
├── api.md
├── deployment.md
├── contributing.md
├── architecture.md
├── troubleshooting.md
└── ... (20+ files at root)
```

**Good:**

```
docs/
├── INDEX.md
├── guides/
├── reference/
└── governance/
```

### 3. Mixed Content Types

**Bad:**

```
src/
├── app.py
├── test_app.py          # Tests mixed with source
├── README.md            # Docs mixed with source
└── config.json          # Config mixed with source
```

**Good:**

```
src/
└── app.py
tests/
└── test_app.py
docs/
└── README.md
config/
└── config.json
```

______________________________________________________________________

## Validation

Use the validation script to check compliance:

```bash
./scripts/validate-repository-structure.sh
```

The script checks:

- Required files exist (README, LICENSE, .gitignore)
- Recommended directories exist (docs/, tests/, .github/)
- Root directory is not cluttered
- File naming conventions are followed
- Build artifacts are gitignored

______________________________________________________________________

## Migration

For existing repositories, see
[REPOSITORY_ORGANIZATION_MIGRATION.md](./REPOSITORY_ORGANIZATION_MIGRATION.md).

______________________________________________________________________

## Related Documents

- [Quick Reference](./REPOSITORY_ORGANIZATION_QUICK_REF.md)
- [Migration Guide](./REPOSITORY_ORGANIZATION_MIGRATION.md)
- [Contributing Guidelines](../governance/CONTRIBUTING.md)

______________________________________________________________________

## Version History

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 1.0     | 2026-01-23 | Initial standards document |

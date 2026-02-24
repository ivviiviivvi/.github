# Repository Organization Quick Reference

Quick reference for repository structure standards. See
[REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md) for full details.

______________________________________________________________________

## Essential Checklist

### Required Files

- [ ] `README.md` - Project overview
- [ ] `LICENSE` - License file
- [ ] `.gitignore` - Git ignore rules
- [ ] `.github/` - GitHub configuration

### Recommended Structure

- [ ] `docs/` - Documentation
- [ ] `tests/` - Test files
- [ ] `scripts/` - Utility scripts
- [ ] `CHANGELOG.md` - Version history
- [ ] `CONTRIBUTING.md` - Contribution guide

______________________________________________________________________

## Quick Decision Tree

```
Where does this file go?
│
├─ Is it source code?
│  └─ src/ or lib/ or pkg/
│
├─ Is it a test?
│  └─ tests/
│
├─ Is it documentation?
│  ├─ How-to guide? → docs/guides/
│  ├─ Technical reference? → docs/reference/
│  ├─ Policy/governance? → docs/governance/
│  └─ General docs? → docs/
│
├─ Is it a script?
│  └─ scripts/
│
├─ Is it a GitHub workflow?
│  └─ .github/workflows/
│
├─ Is it a status report?
│  └─ reports/status/ or archive/status-reports/
│
├─ Is it a test result?
│  └─ reports/ or .gitignore (don't commit)
│
├─ Is it a build artifact?
│  └─ .gitignore (never commit)
│
└─ Is it a config file?
   ├─ Essential? → root (max 1 per tool)
   └─ Secondary? → .config/ or config/
```

______________________________________________________________________

## Standard Directory Structure

```
repository/
├── .github/
│   ├── workflows/           # CI/CD workflows
│   ├── ISSUE_TEMPLATE/      # Issue templates
│   ├── scripts/             # Workflow helper scripts
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docs/
│   ├── INDEX.md             # Documentation index
│   ├── guides/              # How-to guides
│   ├── reference/           # Technical docs
│   ├── governance/          # Policies
│   └── standards/           # Standards docs
│
├── src/ or lib/             # Source code
│
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data
│
├── scripts/                 # Utility scripts
│
├── reports/                 # Generated reports
│
├── archive/                 # Historical content
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
└── [language config]        # pyproject.toml, package.json, etc.
```

______________________________________________________________________

## File Naming Rules

| Type          | Convention          | Example              |
| ------------- | ------------------- | -------------------- |
| Docs          | UPPER_SNAKE_CASE.md | `GETTING_STARTED.md` |
| Python        | snake_case.py       | `user_service.py`    |
| JavaScript    | camelCase.js        | `userService.js`     |
| Shell scripts | kebab-case.sh       | `run-tests.sh`       |
| Config        | kebab-case.yml      | `docker-compose.yml` |
| Dotfiles      | .filename           | `.gitignore`         |

______________________________________________________________________

## Root Directory Rules

### Maximum 15 Essential Files

**Allowed:**

- README.md, LICENSE, CHANGELOG.md
- .gitignore, .gitattributes
- Language config (ONE of: pyproject.toml, package.json, go.mod, etc.)
- Build config (Makefile, Dockerfile)
- CONTRIBUTING.md, SECURITY.md

**Not Allowed:**

- `*STATUS*.md`, `*COMPLETE*.md`
- `test-results*.json`
- Multiple similar configs
- Temporary files
- Build artifacts

______________________________________________________________________

## Common Anti-Patterns

| Anti-Pattern              | Solution                     |
| ------------------------- | ---------------------------- |
| 30+ files in root         | Move to appropriate subdirs  |
| Tests in src/             | Move to tests/               |
| Docs scattered everywhere | Consolidate in docs/         |
| Status files in root      | Move to reports/ or archive/ |
| Build artifacts committed | Add to .gitignore            |

______________________________________________________________________

## Quick Cleanup Commands

```bash
# Move status files to archive
mkdir -p archive/status-reports
mv *STATUS*.md *COMPLETE*.md archive/status-reports/

# Move test results
mkdir -p reports
mv test-results*.json reports/

# Create missing directories
mkdir -p docs/{guides,reference,governance} tests scripts

# Validate structure
./scripts/validate-repository-structure.sh
```

______________________________________________________________________

## Validation

```bash
# Run validation script
./scripts/validate-repository-structure.sh

# Check for root clutter
ls -la | wc -l  # Should be < 20 items

# Find misplaced files
find . -maxdepth 1 -name "*STATUS*" -o -name "*COMPLETE*"
```

______________________________________________________________________

## Common Questions

**Q: Where do I put a new feature's documentation?** A: `docs/guides/` for
how-to, `docs/reference/` for technical details.

**Q: Can I have tests alongside source code?** A: Yes, for Python (`test_*.py`
next to modules) or JavaScript (`*.test.js`), but prefer `tests/` for clarity.

**Q: What about monorepo structures?** A: Each package follows these standards
within its directory.

**Q: How do I handle legacy files?** A: Move to `archive/` with a README
explaining the contents.

______________________________________________________________________

## Related Documents

- [Full Standards](./REPOSITORY_STRUCTURE.md) - Complete documentation
- [Migration Guide](./REPOSITORY_ORGANIZATION_MIGRATION.md) - How to migrate

# Repository Organization Migration Guide

Step-by-step guide for migrating existing repositories to organization
standards.

______________________________________________________________________

## Migration Levels

Choose your migration depth based on time and impact:

| Level         | Time      | Impact | What Changes               |
| ------------- | --------- | ------ | -------------------------- |
| Essential     | 30 min    | Low    | Add missing required files |
| Recommended   | 2-4 hours | Medium | Reorganize directories     |
| Comprehensive | 1-2 days  | High   | Full restructure           |

______________________________________________________________________

## Before You Start

### 1. Create a Backup Branch

```bash
git checkout -b backup/pre-migration-$(date +%Y%m%d)
git push origin backup/pre-migration-$(date +%Y%m%d)
git checkout main
```

### 2. Run Initial Assessment

```bash
# Count root files (should be < 20)
ls -la | wc -l

# Find status/completion files
find . -maxdepth 1 -name "*STATUS*" -o -name "*COMPLETE*" -o -name "*DONE*"

# Find test results in root
find . -maxdepth 1 -name "test-results*" -o -name "*.log"

# Check for missing essentials
[ -f README.md ] && echo "✓ README" || echo "✗ README missing"
[ -f LICENSE ] && echo "✓ LICENSE" || echo "✗ LICENSE missing"
[ -f .gitignore ] && echo "✓ .gitignore" || echo "✗ .gitignore missing"
[ -d .github ] && echo "✓ .github/" || echo "✗ .github/ missing"
[ -d docs ] && echo "✓ docs/" || echo "✗ docs/ missing"
[ -d tests ] && echo "✓ tests/" || echo "✗ tests/ missing"
```

______________________________________________________________________

## Essential Migration (30 minutes)

### Phase 1: Create Required Files

````bash
# Create README if missing
[ -f README.md ] || cat > README.md << 'EOF'
# Project Name

Brief description of the project.

## Installation

```bash
# Installation steps
````

## Usage

```bash
# Usage examples
```

## Contributing

See [CONTRIBUTING.md](../governance/CONTRIBUTING.md)

## License

See [LICENSE](../../LICENSE) EOF

# Create LICENSE if missing (MIT example)

\[ -f LICENSE \] || cat > LICENSE \<\< 'EOF' MIT License

Copyright (c) 2026 \[Organization\]

Permission is hereby granted, free of charge, to any person obtaining a copy...
EOF

# Create .gitignore if missing

\[ -f .gitignore \] || cat > .gitignore \<\< 'EOF'

# Build artifacts

dist/ build/ \*.egg-info/

# Dependencies

node_modules/ venv/ .venv/

# IDE

.idea/ .vscode/ \*.swp

# Environment

.env .env.local

# OS

.DS_Store Thumbs.db

# Test/coverage

.coverage htmlcov/ .pytest_cache/

# Logs

\*.log logs/ EOF

````

### Phase 2: Create Essential Directories

```bash
mkdir -p .github/workflows
mkdir -p docs
mkdir -p tests
mkdir -p scripts
````

### Commit Point

```bash
git add -A
git commit -m "chore: add essential repository structure

- Add README.md, LICENSE, .gitignore (if missing)
- Create standard directories: docs/, tests/, scripts/, .github/"
```

______________________________________________________________________

## Recommended Migration (2-4 hours)

### Phase 3: Move Status Files to Archive

```bash
# Create archive structure
mkdir -p archive/status-reports

# Move status/completion files
for pattern in "*STATUS*.md" "*COMPLETE*.md" "*DONE*.md" "*PHASE*.md"; do
  find . -maxdepth 1 -name "$pattern" -exec mv {} archive/status-reports/ \;
done

# Create archive README
cat > archive/README.md << 'EOF'
# Archive

Historical content moved from root directory.

## Contents

- `status-reports/` - Project status and completion reports
EOF
```

### Phase 4: Move Test Results

```bash
# Create reports directory
mkdir -p reports

# Move test result files
for pattern in "test-results*.json" "coverage*.json" "*.log"; do
  find . -maxdepth 1 -name "$pattern" -exec mv {} reports/ \;
done

# Or add to .gitignore if they shouldn't be committed
echo "test-results*.json" >> .gitignore
echo "coverage*.json" >> .gitignore
```

### Phase 5: Organize Documentation

```bash
# Create documentation structure
mkdir -p docs/{guides,reference,governance,standards}

# Move scattered docs to docs/
find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "LICENSE" ! -name "CHANGELOG.md" ! -name "CONTRIBUTING.md" ! -name "SECURITY.md" -exec mv {} docs/ \;

# Create documentation index
cat > docs/INDEX.md << 'EOF'
# Documentation Index

## Guides
- [Getting Started](guides/GETTING_STARTED.md)

## Reference
- [Repository Structure](reference/REPOSITORY_STRUCTURE.md)

## Governance
- [Contributing](../governance/CONTRIBUTING.md)
EOF
```

### Commit Point

```bash
git add -A
git commit -m "chore: reorganize repository structure

- Move status files to archive/status-reports/
- Move test results to reports/
- Organize documentation under docs/"
```

______________________________________________________________________

## Comprehensive Migration (1-2 days)

### Phase 6: Reorganize Source Code

Depends on your language:

**Python:**

```bash
mkdir -p src/package_name
mv *.py src/package_name/ 2>/dev/null || true
touch src/package_name/__init__.py
```

**Node.js:**

```bash
mkdir -p src
mv *.js *.ts src/ 2>/dev/null || true
```

### Phase 7: Reorganize Tests

```bash
mkdir -p tests/{unit,integration,fixtures}

# Move test files
mv test_*.py tests/unit/ 2>/dev/null || true
mv *_test.py tests/unit/ 2>/dev/null || true
mv *.test.js tests/unit/ 2>/dev/null || true

# Create conftest.py for Python
cat > tests/conftest.py << 'EOF'
"""Pytest configuration and fixtures."""
import pytest

# Add fixtures here
EOF
```

### Phase 8: Update Import Paths

After moving files, update imports:

```bash
# Find files with old imports (Python example)
grep -r "from old_module" src/
grep -r "import old_module" src/

# Update imports (use sed or manual editing)
```

### Phase 9: Update CI/CD Paths

Update workflow files to reflect new paths:

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: pytest tests/
```

### Commit Point

```bash
git add -A
git commit -m "refactor: comprehensive repository restructure

- Reorganize source code into src/
- Move tests to tests/{unit,integration}/
- Update imports and CI paths"
```

______________________________________________________________________

## Common Scenarios

### Scenario: Root Directory Clutter

**Problem:** 50+ files in root

**Solution:**

```bash
# 1. Identify file types
ls -la | awk '{print $NF}' | grep -v "^\\.$" | sort | uniq -c | sort -rn

# 2. Move by type
mv *STATUS*.md archive/status-reports/
mv test-*.json reports/
mv docs-*.md docs/
```

### Scenario: Tests Mixed with Source

**Problem:** `test_*.py` files alongside `*.py` source files

**Solution:**

```bash
# Create tests directory
mkdir -p tests/unit

# Move test files
find src/ -name "test_*.py" -exec mv {} tests/unit/ \;

# Update imports in test files
```

### Scenario: Multiple Documentation Locations

**Problem:** Docs in root, wiki/, documentation/, docs/

**Solution:**

```bash
# Consolidate to docs/
mkdir -p docs/legacy
mv wiki/* docs/legacy/ 2>/dev/null || true
mv documentation/* docs/ 2>/dev/null || true
rmdir wiki documentation 2>/dev/null || true
```

______________________________________________________________________

## Post-Migration Checklist

- [ ] All tests pass
- [ ] CI/CD workflows succeed
- [ ] Documentation links work
- [ ] README is accurate
- [ ] `.gitignore` covers new paths
- [ ] No broken imports
- [ ] Validation script passes

### Run Validation

```bash
./scripts/validate-repository-structure.sh
```

______________________________________________________________________

## Troubleshooting

### Broken Imports After Move

```bash
# Find broken imports (Python)
python -c "import package_name"

# Fix with sed
sed -i 's/old_path/new_path/g' src/**/*.py
```

### CI Failing After Move

1. Check workflow paths in `.github/workflows/`
1. Verify test paths
1. Check working directory assumptions

### Git History Concerns

The migration preserves history. To see file history after move:

```bash
git log --follow -- new/path/to/file.py
```

______________________________________________________________________

## Related Documents

- [Repository Structure Standards](./REPOSITORY_STRUCTURE.md)
- [Quick Reference](./REPOSITORY_ORGANIZATION_QUICK_REF.md)

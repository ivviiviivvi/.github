# Repository Organization Migration Guide

> **Step-by-step guide for applying organizational standards to existing repositories**

**Version**: 1.0.0  
**Last Updated**: 2026-01-20  
**Applies To**: All existing repositories

## Overview

This guide helps you migrate an existing repository to meet our
[Repository Structure Standards](./REPOSITORY_STRUCTURE.md). The process is
designed to be gradual and non-disruptive.

### Goals

- Improve repository organization without breaking functionality
- Make repositories easier to navigate and maintain
- Enable automated validation and quality gates
- Align with organization-wide standards

### Approach

1. **Assess Current State** - Understand what needs to change
2. **Plan Migration** - Prioritize and schedule changes
3. **Execute Changes** - Make incremental improvements
4. **Validate Results** - Verify compliance with standards

---

## Migration Levels

Choose the appropriate migration level for your repository:

### Level 1: Essential (Required)

**Time**: 30 minutes  
**Focus**: Critical files and structure

- ✅ Ensure README.md, LICENSE, .gitignore exist
- ✅ Add basic .github/ structure
- ✅ Update .gitignore for common artifacts
- ✅ Document any unique structure in README

### Level 2: Recommended (Strongly Advised)

**Time**: 2-4 hours  
**Focus**: Documentation and organization

- ✅ Create docs/ directory structure
- ✅ Move policy docs to docs/governance/
- ✅ Organize tests into tests/ directory
- ✅ Move scripts to scripts/ directory
- ✅ Add validation to CI/CD

### Level 3: Comprehensive (Best Practice)

**Time**: 1-2 days  
**Focus**: Complete reorganization

- ✅ Full directory restructure
- ✅ Clean up root directory completely
- ✅ Archive old content appropriately
- ✅ Update all internal links
- ✅ Add pre-commit hooks
- ✅ Create comprehensive documentation

---

## Step-by-Step Migration

### Phase 1: Assessment (15 minutes)

1. **Run the validation script**

```bash
# Clone organization standards repo (if not already done)
git clone https://github.com/ivviiviivvi/.github.git org-standards

# Copy validation script to your repo
cp org-standards/scripts/validate-repository-structure.sh ./scripts/

# Make executable
chmod +x scripts/validate-repository-structure.sh

# Run validation
./scripts/validate-repository-structure.sh > structure-report.txt

# Review report
cat structure-report.txt
```

2. **Document current structure**

```bash
# Generate structure report
tree -L 2 -a --dirsfirst > current-structure.txt

# Count root-level files
ls -1 | wc -l

# Identify problem areas
find . -maxdepth 1 -type f -name "*.md" | wc -l
```

3. **Create migration checklist**

Create `MIGRATION_CHECKLIST.md`:

```markdown
# Repository Organization Migration

## Current Issues
- [ ] Too many root-level files (count: XX)
- [ ] Status files in root
- [ ] Test results not gitignored
- [ ] No docs/ directory structure

## Level 1 (Essential) - Target: [Date]
- [ ] Add/verify README.md
- [ ] Add/verify LICENSE
- [ ] Update .gitignore
- [ ] Create .github/ structure

## Level 2 (Recommended) - Target: [Date]
- [ ] Create docs/ structure
- [ ] Move documentation
- [ ] Organize tests
- [ ] Add CI validation

## Level 3 (Optional) - Target: [Date]
- [ ] Complete reorganization
- [ ] Archive old content
- [ ] Update all links
```

### Phase 2: Backup and Preparation (15 minutes)

1. **Create backup branch**

```bash
# Create and push backup
git checkout -b backup/pre-organization-$(date +%Y%m%d)
git push origin backup/pre-organization-$(date +%Y%m%d)

# Return to main development branch
git checkout main
# or
git checkout develop
```

2. **Create working branch**

```bash
git checkout -b chore/repository-organization
```

3. **Document changes**

Create `docs/migration/organization-migration-plan.md` documenting:
- What will be moved
- New locations
- Migration timeline
- Team communication plan

### Phase 3: Essential Changes (Level 1)

#### 3.1: Verify Core Files (5 minutes)

```bash
# Check for required files
test -f README.md || echo "Need to create README.md"
test -f LICENSE || echo "Need to create LICENSE"
test -f .gitignore || echo "Need to create .gitignore"
```

**Action**: Create any missing core files using organization templates.

#### 3.2: Create Basic GitHub Structure (10 minutes)

```bash
# Create .github directory structure
mkdir -p .github/{workflows,ISSUE_TEMPLATE,PULL_REQUEST_TEMPLATE}

# Add CODEOWNERS if needed
cat > .github/CODEOWNERS << 'EOF'
# Default owners for everything in the repo
* @your-team

# Specific ownership examples
# /docs/ @docs-team
# *.js @frontend-team
EOF
```

#### 3.3: Update .gitignore (10 minutes)

Add common patterns to `.gitignore`:

```gitignore
# Build outputs
dist/
build/
target/
*.min.js
*.min.css

# Dependencies
node_modules/
venv/
.venv/

# Test outputs
coverage/
.nyc_output/
test-results*.json

# Logs
*.log
logs/

# Environment files
.env
.env.local
!.env.example

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Reports (generated)
reports/*.json
reports/**/*.html
!reports/README.md
```

**Commit point:**

```bash
git add .gitignore .github/
git commit -m "chore: add essential organizational structure

- Add .github/ directory structure
- Add CODEOWNERS file
- Update .gitignore with comprehensive patterns"
```

### Phase 4: Recommended Changes (Level 2)

#### 4.1: Create Documentation Structure (30 minutes)

```bash
# Create docs structure
mkdir -p docs/{guides,reference,architecture,governance,assets}

# Create README files
cat > docs/README.md << 'EOF'
# Documentation

This directory contains all project documentation.

## Structure

- `guides/` - How-to guides and tutorials
- `reference/` - Technical reference documentation
- `architecture/` - Architecture documentation and ADRs
- `governance/` - Policies and governance documents
- `assets/` - Images, diagrams, and other media

## Quick Links

- [Getting Started](guides/getting-started.md)
- [Contributing](governance/CONTRIBUTING.md)
- [API Reference](reference/api-reference.md)
EOF

# Create README in subdirectories
for dir in guides reference architecture governance; do
  echo "# $(basename $dir | sed 's/.*/\u&/')" > docs/$dir/README.md
  echo "" >> docs/$dir/README.md
  echo "Documentation for $(basename $dir)." >> docs/$dir/README.md
done
```

#### 4.2: Move Documentation Files (30 minutes)

```bash
# Move governance documents (if at root)
mv CONTRIBUTING.md docs/governance/ 2>/dev/null || true
mv CODE_OF_CONDUCT.md docs/governance/ 2>/dev/null || true
mv SECURITY.md docs/governance/ 2>/dev/null || true

# Create symlinks at root (for GitHub)
ln -s docs/governance/CONTRIBUTING.md CONTRIBUTING.md 2>/dev/null || true
ln -s docs/governance/CODE_OF_CONDUCT.md CODE_OF_CONDUCT.md 2>/dev/null || true
ln -s docs/governance/SECURITY.md SECURITY.md 2>/dev/null || true

# Move guides
mkdir -p docs/guides
# Example: mv GETTING_STARTED.md docs/guides/getting-started.md

# Move architecture docs
mkdir -p docs/architecture
# Example: mv ARCHITECTURE.md docs/architecture/overview.md
```

**Important**: Update internal links after moving files!

#### 4.3: Organize Root Directory (45 minutes)

```bash
# Create reports directory
mkdir -p reports/{status,monitoring,deployment}

# Move status files
mv *STATUS*.md reports/status/ 2>/dev/null || true
mv *COMPLETE.md reports/status/ 2>/dev/null || true

# Move monitoring files
mv MONITORING_*.md reports/monitoring/ 2>/dev/null || true

# Move deployment files
mv DEPLOYMENT_*.md reports/deployment/ 2>/dev/null || true

# Move test results
mkdir -p reports/tests
mv test-results*.json reports/tests/ 2>/dev/null || true

# Add reports README
cat > reports/README.md << 'EOF'
# Reports

This directory contains generated reports and status documents.

## Structure

- `status/` - Status reports and completion documents
- `monitoring/` - Monitoring checklists and logs
- `deployment/` - Deployment logs and summaries
- `tests/` - Test results and coverage reports

## Retention Policy

- Keep reports for 90 days
- Archive important reports to docs/reports/
- Automated cleanup runs monthly
EOF
```

#### 4.4: Organize Tests (30 minutes)

```bash
# Create test structure
mkdir -p tests/{unit,integration,e2e,fixtures}

# Move existing tests (adjust paths as needed)
# Example for Python:
# mv test_*.py tests/unit/ 2>/dev/null || true
# mv *_test.py tests/unit/ 2>/dev/null || true

# Add tests README
cat > tests/README.md << 'EOF'
# Tests

## Structure

- `unit/` - Unit tests
- `integration/` - Integration tests
- `e2e/` - End-to-end tests
- `fixtures/` - Test data and fixtures

## Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=html
```
EOF
```

#### 4.5: Organize Scripts (20 minutes)

```bash
# Create scripts structure
mkdir -p scripts/{build,deploy,setup,utils}

# Move existing scripts
# Adjust based on your repository
# mv build.sh scripts/build/ 2>/dev/null || true
# mv deploy.sh scripts/deploy/ 2>/dev/null || true

# Add scripts README
cat > scripts/README.md << 'EOF'
# Scripts

Utility scripts for building, deploying, and maintaining the project.

## Structure

- `build/` - Build scripts
- `deploy/` - Deployment scripts
- `setup/` - Environment setup
- `utils/` - Utility scripts

## Usage

All scripts should be executable and documented with usage information.
EOF

# Make scripts executable
find scripts -type f -name "*.sh" -exec chmod +x {} \;
```

**Commit point:**

```bash
git add docs/ reports/ tests/ scripts/
git commit -m "chore: organize repository structure

- Create docs/ directory structure
- Move documentation to appropriate locations
- Organize reports and status files
- Structure tests directory
- Organize scripts

BREAKING CHANGE: File locations have changed. Update bookmarks and links."
```

#### 4.6: Update Links and References (30 minutes)

```bash
# Find all markdown files
find . -name "*.md" -type f > md-files.txt

# Script to update links (example - adjust as needed)
cat > update-links.sh << 'EOF'
#!/bin/bash
# Update links in documentation

# Example replacements (adjust for your repository)
find . -name "*.md" -type f -exec sed -i 's|CONTRIBUTING.md|docs/governance/CONTRIBUTING.md|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|SECURITY.md|docs/governance/SECURITY.md|g' {} \;

echo "Links updated. Please review changes before committing."
EOF

chmod +x update-links.sh
./update-links.sh

# Manually review and fix any broken links
```

#### 4.7: Add CI Validation (20 minutes)

Create `.github/workflows/structure-validation.yml`:

```yaml
name: Repository Structure Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      
      - name: Make validation script executable
        run: chmod +x scripts/validate-repository-structure.sh
      
      - name: Run structure validation
        run: ./scripts/validate-repository-structure.sh
```

**Commit point:**

```bash
git add .github/workflows/structure-validation.yml
git commit -m "ci: add repository structure validation

- Add automated structure validation workflow
- Runs on push and PR to main/develop branches"
```

### Phase 5: Comprehensive Changes (Level 3)

#### 5.1: Archive Old Content (30 minutes)

```bash
# Create archive structure
mkdir -p archive/{deprecated,old-docs,historical}

# Add archive README
cat > archive/README.md << 'EOF'
# Archive

This directory contains deprecated and historical content.

## Retention Policy

Content is kept for historical reference:
- Deprecated features: 1 year
- Old documentation: 2 years
- Historical reports: Indefinitely (for compliance)

## Structure

- `deprecated/` - Deprecated features and code
- `old-docs/` - Superseded documentation
- `historical/` - Historical reports and data
EOF

# Move old content
# Example: mv old-feature/ archive/deprecated/
```

#### 5.2: Update README (30 minutes)

Update root `README.md` to reflect new structure:

```markdown
# Project Name

## Repository Structure

```
├── docs/              # Documentation
│   ├── guides/        # How-to guides
│   ├── reference/     # Technical reference
│   └── governance/    # Policies
├── src/               # Source code
├── tests/             # Tests
├── scripts/           # Build and utility scripts
├── reports/           # Generated reports
└── .github/           # GitHub configuration
```

## Quick Links

- [Documentation](docs/README.md)
- [Contributing](docs/governance/CONTRIBUTING.md)
- [API Reference](docs/reference/api-reference.md)
```

#### 5.3: Add Pre-commit Hooks (20 minutes)

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-structure
        name: Validate Repository Structure
        entry: scripts/validate-repository-structure.sh
        language: system
        pass_filenames: false
        stages: [commit]
```

Install hooks:

```bash
pip install pre-commit
pre-commit install
```

### Phase 6: Validation and Cleanup (30 minutes)

#### 6.1: Validate Changes

```bash
# Run validation script
./scripts/validate-repository-structure.sh

# Check for broken links
# Use a tool like markdown-link-check
npm install -g markdown-link-check
find docs -name "*.md" -exec markdown-link-check {} \;

# Verify builds still work
# Run your project's build command
# npm run build
# python setup.py build
# cargo build
```

#### 6.2: Clean Up

```bash
# Remove temporary files
rm md-files.txt update-links.sh

# Verify gitignore is working
git status | grep -i "reports/"
git status | grep -i "test-results"

# Clean up any accidentally tracked files
git rm --cached reports/*.json 2>/dev/null || true
```

#### 6.3: Final Commit

```bash
git add .
git commit -m "chore: complete repository organization migration

- Archive old content
- Update README with new structure
- Add pre-commit validation hooks
- Update all documentation links

Resolves #XXX"
```

### Phase 7: Review and Merge (Variable)

1. **Create Pull Request**

```bash
git push origin chore/repository-organization
# Create PR via GitHub UI or CLI
gh pr create --title "Repository Organization Migration" \
  --body "Applies organizational standards per REPOSITORY_STRUCTURE.md"
```

2. **Team Review**
   - Request reviews from team members
   - Address feedback
   - Update migration documentation based on lessons learned

3. **Merge Strategy**
   - For small repos: Squash and merge
   - For large repos: Regular merge to preserve history
   - Update main/develop branch protection rules if needed

4. **Post-Merge**

```bash
# Update local repo
git checkout main
git pull origin main

# Delete working branch
git branch -d chore/repository-organization
git push origin --delete chore/repository-organization

# Announce changes to team
# - Update team documentation
# - Send announcement email/message
# - Update onboarding materials
```

---

## Common Scenarios

### Scenario 1: Too Many Root Files

**Problem**: 50+ markdown files at root level

**Solution**:

```bash
# Categorize and move
mkdir -p docs/{reports,status,planning}

# Move by category
mv *STATUS*.md docs/reports/
mv *PLAN*.md docs/planning/
mv WEEK*.md docs/reports/

# Update CHANGELOG
echo "Files moved to docs/ subdirectories for better organization" >> CHANGELOG.md
```

### Scenario 2: Mixed Test Files

**Problem**: Tests scattered throughout source directories

**Solution**:

```bash
# Collect tests
find src -name "test_*.py" -o -name "*_test.py" > test-files.txt

# Move to tests/
mkdir -p tests/unit
while read file; do
  mv "$file" tests/unit/$(basename "$file")
done < test-files.txt

# Update test configuration
# Adjust pytest.ini, jest.config.js, etc.
```

### Scenario 3: Multiple Documentation Locations

**Problem**: Docs in README.md, wiki, docs/, and root directory

**Solution**:

1. Audit all documentation sources
2. Create comprehensive docs/INDEX.md
3. Consolidate to docs/ directory
4. Add migration notices to old locations
5. Update links systematically

```bash
# Create index
cat > docs/INDEX.md << 'EOF'
# Documentation Index

All documentation has been consolidated here.

## Previous Locations

- Wiki → docs/wiki/
- Root docs → docs/guides/
- Legacy → archive/old-docs/
EOF
```

---

## Troubleshooting

### Issue: Broken Links After Moving Files

**Solution**:

```bash
# Find all internal links
grep -r "\[.*\](.*\.md)" docs/ > links.txt

# Fix with sed (example)
sed -i 's|](guides/|](../guides/|g' docs/reference/*.md

# Or use a tool like replace-link
npm install -g markdown-link-updater
markdown-link-updater docs/
```

### Issue: CI/CD Breaks After Reorganization

**Solution**:

1. Update CI configuration files (.github/workflows/)
2. Update paths in build scripts
3. Update import paths in code
4. Test locally before pushing

```bash
# Test workflow locally
act -l  # List workflows
act push  # Run push event workflows
```

### Issue: Team Members Can't Find Files

**Solution**:

1. Create migration announcement
2. Update documentation index
3. Add redirects or notices in old locations
4. Hold team briefing
5. Update onboarding docs

---

## Post-Migration Checklist

- [ ] Validation script passes
- [ ] All tests pass
- [ ] Build succeeds
- [ ] CI/CD pipelines work
- [ ] Documentation is accessible
- [ ] Team is informed
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Links verified
- [ ] Old branches cleaned up
- [ ] Backup branches tagged

---

## Best Practices

1. **Go Gradual**: Don't reorganize everything at once
2. **Communicate Early**: Warn team about upcoming changes
3. **Test Thoroughly**: Verify builds and tests after each phase
4. **Document Everything**: Keep detailed migration notes
5. **Keep Backups**: Maintain backup branches
6. **Update Links**: Fix internal references immediately
7. **Use Automation**: Leverage scripts for repetitive tasks
8. **Validate Often**: Run validation after each major change

---

## Resources

- [Repository Structure Standards](./REPOSITORY_STRUCTURE.md)
- [Quick Reference](./REPOSITORY_ORGANIZATION_QUICK_REF.md)
- [Validation Script](../../scripts/validate-repository-structure.sh)
- [Version Control Standards](./VERSION_CONTROL_STANDARDS.md)

---

## Getting Help

- Review the [full standards document](./REPOSITORY_STRUCTURE.md)
- Check [common questions](./REPOSITORY_ORGANIZATION_QUICK_REF.md#common-questions)
- Open an issue with label `question` or `documentation`
- Ask in organization discussions

---

*Last Updated: 2026-01-20 | Version: 1.0.0*

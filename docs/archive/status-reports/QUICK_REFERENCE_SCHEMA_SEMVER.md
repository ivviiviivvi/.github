# Schema.org & Semver Quick Reference

## 📦 Version Commands

```bash
# Check current version
cat VERSION

# Bump version
npm run version:bump:major   # 1.0.0 → 2.0.0
npm run version:bump:minor   # 1.0.0 → 1.1.0  
npm run version:bump:patch   # 1.0.0 → 1.0.1

# Sync versions to all files
npm run version:sync
```

## 📊 Schema.org Commands

```bash
# Validate schemas
python scripts/validate-schema-org.py

# Update READMEs with schema info
./scripts/generate-schema-readme.sh

# View schemas
ls -la .schema-org/
```

## 🔄 Conventional Commits

```bash
# Format: <type>(<scope>): <description>

feat: add new feature         # Minor bump (1.0.0 → 1.1.0)
fix: resolve bug             # Patch bump (1.0.0 → 1.0.1)
feat!: breaking change       # Major bump (1.0.0 → 2.0.0)
docs: update documentation   # Patch bump
chore: maintenance task      # No version bump
```

## 📁 Key Files

```
VERSION                          # Source of truth: 1.0.0
package.json                     # Node.js package
.schema-org/
  ├── organization.jsonld        # Org metadata
  ├── repository.jsonld          # Repo metadata
  ├── ai-framework.jsonld        # AI framework
  └── documentation.jsonld       # Documentation
scripts/
  ├── sync-version.js            # Version sync
  ├── validate-schema-org.py     # Validation
  └── generate-schema-readme.sh  # README generator
```

## 🚀 Quick Start Workflow

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add awesome feature"

# 2. Before release, bump version
npm run version:bump:minor

# 3. Sync all version files
npm run version:sync

# 4. Validate everything
python scripts/validate-schema-org.py

# 5. Commit and push
git add .
git commit -m "chore: bump version to 1.1.0"
git push
```

## ✅ Pre-commit Checklist

- [ ] Used conventional commit message
- [ ] Version synced across all files
- [ ] Schema.org files validated
- [ ] Documentation updated if needed
- [ ] All tests passing

## 🔗 Quick Links

- 📖 [Complete Guide](docs/SCHEMA_ORG_SEMVER_GUIDE.md)
- 📊 [Implementation Summary](SCHEMA_ORG_SEMVER_IMPLEMENTATION.md)
- 🔧 [Semver Details](docs/reference/SEMANTIC_VERSIONING.md)
- 📁 [Schema.org Docs](.schema-org/README.md)

## 🆘 Troubleshooting

**Version mismatch?**

```bash
node scripts/sync-version.js
```

**Schema errors?**

```bash
python scripts/validate-schema-org.py
# Fix errors in .schema-org/*.jsonld
```

**Scripts not executable?**

```bash
chmod +x scripts/*.sh
```

______________________________________________________________________

**Version**: 1.0.0 | **Status**: ✅ Deployed | **Updated**: 2026-01-18

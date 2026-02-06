# Schema.org & Semantic Versioning Implementation Guide

**Status**: ✅ Deployed\
**Version**: 1.0.0\
**Last Updated**: 2026-01-18

This document describes the organization-wide implementation of schema.org
structured data and semantic versioning (semver) standards.

______________________________________________________________________

## Table of Contents

- [Overview](#overview)
- [Semantic Versioning](#semantic-versioning)
- [Schema.org Implementation](#schemaorg-implementation)
- [Directory Structure](#directory-structure)
- [Version Management](#version-management)
- [Schema.org Files](#schemaorg-files)
- [Automation Scripts](#automation-scripts)
- [GitHub Workflows](#github-workflows)
- [Usage Guide](#usage-guide)
- [Best Practices](#best-practices)
- [Validation](#validation)
- [Troubleshooting](#troubleshooting)

______________________________________________________________________

## Overview

### What is Semantic Versioning?

Semantic versioning (semver) is a versioning scheme using MAJOR.MINOR.PATCH
format:

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

Example: `1.2.3` where `1` is major, `2` is minor, `3` is patch

### What is Schema.org?

Schema.org is a collaborative project to create structured data vocabulary for
the web. It helps search engines, AI tools, and other applications understand
the content and context of repositories.

### Why Implement Both?

- **Semver**: Provides clear, predictable versioning for all projects
- **Schema.org**: Makes repositories machine-readable and discoverable
- **AI Integration**: Enables better AI understanding of codebases
- **Automation**: Facilitates automated version management and metadata updates

______________________________________________________________________

## Semantic Versioning

### Version Files

The repository maintains version information in multiple formats:

```
/workspace/
├── VERSION                 # Plain text version (source of truth)
├── package.json           # Node.js version and metadata
├── pyproject.toml         # Python version (if applicable)
├── Cargo.toml            # Rust version (if applicable)
└── .schema-org/          # Schema.org with version info
    ├── repository.jsonld
    ├── ai-framework.jsonld
    └── documentation.jsonld
```

### Version Format

All versions follow semantic versioning:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0           # Initial release
1.1.0           # Added new feature
1.1.1           # Bug fix
2.0.0           # Breaking change
2.0.0-alpha.1   # Pre-release
2.0.0+20260118  # With build metadata
```

### Version Bumping Rules

| Change Type     | Version Bump          | Conventional Commit            |
| --------------- | --------------------- | ------------------------------ |
| Breaking change | MAJOR (1.0.0 → 2.0.0) | `feat!:` or `BREAKING CHANGE:` |
| New feature     | MINOR (1.0.0 → 1.1.0) | `feat:`                        |
| Bug fix         | PATCH (1.0.0 → 1.0.1) | `fix:`                         |
| Documentation   | PATCH                 | `docs:`                        |
| Performance     | PATCH                 | `perf:`                        |
| Refactoring     | PATCH                 | `refactor:`                    |

### Conventional Commits

All commits should follow the
[Conventional Commits](https://www.conventionalcommits.org/)<!-- link:standards.conventional_commits -->
specification:

```bash
# Format
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

# Examples
feat: add schema.org support
feat(api)!: change authentication method
fix: resolve memory leak in processor
docs: update schema.org documentation
chore: bump version to 1.1.0
```

______________________________________________________________________

## Schema.org Implementation

### Structure

Schema.org files are located in `.schema-org/` directory:

```
.schema-org/
├── organization.jsonld      # Organization-level metadata
├── repository.jsonld        # Repository metadata
├── ai-framework.jsonld      # AI framework specifics
└── documentation.jsonld     # Documentation metadata
```

### Schema Types

We use the following schema.org types:

| File                   | Schema Type         | Purpose                  |
| ---------------------- | ------------------- | ------------------------ |
| `organization.jsonld`  | Organization        | Organization information |
| `repository.jsonld`    | SoftwareSourceCode  | Repository metadata      |
| `ai-framework.jsonld`  | SoftwareApplication | AI framework details     |
| `documentation.jsonld` | TechArticle         | Documentation metadata   |

### Key Properties

Each schema file includes:

- `@context`: Always `https://schema.org`
- `@type`: Schema.org type
- `@id`: Unique identifier (URL)
- `name`: Human-readable name
- `description`: Detailed description
- `version`: Current version (synced with semver)
- `dateModified`: Last update date
- `keywords`: Searchable keywords
- `programmingLanguage`: Languages used
- `license`: License information

______________________________________________________________________

## Directory Structure

```
.
├── VERSION                           # Source version file
├── package.json                      # Node.js package with version
├── .schema-org/                      # Schema.org metadata
│   ├── organization.jsonld           # Organization schema
│   ├── repository.jsonld             # Repository schema
│   ├── ai-framework.jsonld           # AI framework schema
│   └── documentation.jsonld          # Documentation schema
├── scripts/
│   ├── sync-version.js               # Version synchronization
│   ├── validate-schema-org.py        # Schema validation
│   └── generate-schema-readme.sh     # README generator
├── .github/workflows/
│   ├── version-bump.yml              # Version bump automation
│   ├── version-control-standards.yml # Version validation
│   └── schema-org-validation.yml     # Schema.org validation
└── docs/
    ├── SCHEMA_ORG_SEMVER_GUIDE.md   # This file
    └── reference/
        └── SEMANTIC_VERSIONING.md    # Detailed semver guide
```

______________________________________________________________________

## Version Management

### Manual Version Bump

```bash
# Using npm (recommended)
npm run version:bump:major   # 1.0.0 → 2.0.0
npm run version:bump:minor   # 1.0.0 → 1.1.0
npm run version:bump:patch   # 1.0.0 → 1.0.1

# Sync to all version files
npm run version:sync
```

### Automated Version Bump

Use GitHub Actions workflow:

```bash
# Trigger via GitHub UI
# Actions → Version Bump → Run workflow → Select bump type
```

Or via GitHub CLI:

```bash
gh workflow run version-bump.yml -f bump_type=minor
```

### Version Synchronization

After any manual version change, sync across all files:

```bash
node scripts/sync-version.js
```

This updates:

- ✅ `VERSION` file
- ✅ `package.json`
- ✅ `pyproject.toml` (if exists)
- ✅ `Cargo.toml` (if exists)
- ✅ All `.schema-org/*.jsonld` files

______________________________________________________________________

## Schema.org Files

### organization.jsonld

Organization-level metadata:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://github.com/{{ORG_NAME}}",
  "name": "{{ORG_NAME}}",
  "url": "https://github.com/{{ORG_NAME}}",
  "description": "...",
  "foundingDate": "2024",
  "contactPoint": { ... },
  "owns": [ ... ]
}
```

### repository.jsonld

Repository metadata:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareSourceCode",
  "@id": "https://github.com/{{ORG_NAME}}/.github",
  "name": ".github Repository",
  "version": "1.0.0",
  "codeRepository": "https://github.com/{{ORG_NAME}}/.github.git",
  "programmingLanguage": [...],
  "featureList": [...],
  "keywords": [...]
}
```

### ai-framework.jsonld

AI framework specifics:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "https://github.com/{{ORG_NAME}}/.github/tree/main/ai_framework",
  "name": "AI Framework",
  "version": "1.0.0",
  "applicationCategory": "DeveloperApplication",
  "featureList": [...],
  "hasPart": [...]
}
```

### documentation.jsonld

Documentation metadata:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "https://github.com/{{ORG_NAME}}/.github/tree/main/docs",
  "name": "Organization Documentation",
  "version": "1.0.0",
  "numberOfPages": 133,
  "hasPart": [...]
}
```

______________________________________________________________________

## Automation Scripts

### sync-version.js

Synchronizes version across all files:

```bash
node scripts/sync-version.js
```

**Features:**

- ✅ Reads from `package.json` (source of truth)
- ✅ Updates all version files
- ✅ Updates schema.org files
- ✅ Updates `dateModified` in schemas
- ✅ Provides detailed output

### validate-schema-org.py

Validates schema.org files:

```bash
python scripts/validate-schema-org.py
```

**Validation includes:**

- ✅ Valid JSON syntax
- ✅ Required fields present
- ✅ Valid @context and @type
- ✅ Valid URLs
- ✅ Semantic versioning compliance
- ✅ Schema.org standards

### generate-schema-readme.sh

Adds schema.org section to READMEs:

```bash
./scripts/generate-schema-readme.sh
```

**Updates:**

- ✅ Main README.md
- ✅ ai_framework/README.md
- ✅ docs/README.md (if exists)

______________________________________________________________________

## GitHub Workflows

### version-bump.yml

Automated version bumping:

```yaml
# Trigger: Manual workflow dispatch
# Inputs: bump_type (major, minor, patch)
# Actions:
#   - Reads current version
#   - Bumps version
#   - Updates all version files
#   - Commits changes
#   - Creates PR
```

### schema-org-validation.yml

Validates schema.org on PR:

```yaml
# Trigger: Pull request
# Actions:
#   - Runs validate-schema-org.py
#   - Comments on PR with results
#   - Fails CI if validation errors
```

### version-control-standards.yml

Validates branch names and commits:

```yaml
# Trigger: Pull request
# Actions:
#   - Validates branch naming
#   - Validates commit messages
#   - Checks conventional commits
```

______________________________________________________________________

## Usage Guide

### Initial Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

1. **Verify version files:**

   ```bash
   cat VERSION
   cat package.json | grep version
   ```

1. **Validate schema.org:**

   ```bash
   python scripts/validate-schema-org.py
   ```

### Daily Workflow

1. **Make changes following conventional commits:**

   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug"
   ```

1. **Before release, bump version:**

   ```bash
   npm run version:bump:minor
   npm run version:sync
   ```

1. **Validate everything:**

   ```bash
   python scripts/validate-schema-org.py
   pre-commit run --all-files
   ```

1. **Commit and push:**

   ```bash
   git add .
   git commit -m "chore: bump version to 1.1.0"
   git push
   ```

### Release Process

1. **Automated via GitHub Actions:**

   - Go to Actions → Version Bump
   - Run workflow with desired bump type
   - Workflow creates PR with changes
   - Review and merge PR

1. **Manual:**

   ```bash
   # Bump version
   npm run version:bump:minor

   # Sync all files
   npm run version:sync

   # Validate
   python scripts/validate-schema-org.py

   # Commit
   git add .
   git commit -m "chore: release v1.1.0"
   git tag v1.1.0
   git push --tags
   ```

______________________________________________________________________

## Best Practices

### Versioning

1. **Always use conventional commits** for automatic version determination
1. **Sync versions immediately** after manual changes
1. **Tag releases** with `vMAJOR.MINOR.PATCH` format
1. **Use pre-release versions** for testing: `1.0.0-alpha.1`
1. **Document breaking changes** in CHANGELOG.md

### Schema.org

1. **Keep schemas up-to-date** with version changes
1. **Validate before committing** using validation script
1. **Update dateModified** when making changes
1. **Use descriptive keywords** for better discoverability
1. **Link schemas properly** using @id and isPartOf

### Automation

1. **Let workflows handle version bumps** when possible
1. **Review automated PRs** before merging
1. **Monitor validation failures** in CI
1. **Keep scripts executable**: `chmod +x scripts/*.sh`

______________________________________________________________________

## Validation

### Pre-commit Validation

Validation runs automatically via pre-commit hooks:

```bash
pre-commit install
```

### Manual Validation

```bash
# Validate schema.org
python scripts/validate-schema-org.py

# Check version consistency
node scripts/sync-version.js

# Validate all files
pre-commit run --all-files
```

### CI Validation

All validations run automatically on:

- Pull requests
- Push to main branch
- Manual workflow dispatch

______________________________________________________________________

## Troubleshooting

### Version Mismatch

**Problem**: Versions are inconsistent across files

**Solution**:

```bash
node scripts/sync-version.js
```

### Schema.org Validation Errors

**Problem**: Schema validation fails

**Solution**:

1. Run validation to see errors:
   ```bash
   python scripts/validate-schema-org.py
   ```
1. Fix errors in `.schema-org/*.jsonld` files
1. Validate again

### Missing Version Files

**Problem**: `pyproject.toml` or `Cargo.toml` not found

**Solution**: This is normal if you don't use Python or Rust. The sync script
will skip these files.

### Permission Denied on Scripts

**Problem**: Cannot execute shell scripts

**Solution**:

```bash
chmod +x scripts/*.sh
```

### Schema.org URL Issues

**Problem**: Invalid URL errors in validation

**Solution**: Ensure all URLs are:

- Properly formatted: `https://example.com`
- Accessible (no 404s)
- Using HTTPS when possible

______________________________________________________________________

## Resources

### Documentation

- [Semantic Versioning Specification](https://semver.org/)<!-- link:standards.semver -->
- [Conventional Commits](https://www.conventionalcommits.org/)<!-- link:standards.conventional_commits -->
- [Schema.org Developer Guide](https://schema.org/docs/developers.html)
- [Schema.org SoftwareSourceCode](https://schema.org/SoftwareSourceCode)
- [Schema.org Organization](https://schema.org/Organization)

### Internal Docs

- SEMANTIC_VERSIONING.md - Detailed semver guide
- [AI_CODE_INTELLIGENCE.md](../architecture/AI_CODE_INTELLIGENCE.md) - AI
  integration
- [VERSION_CONTROL_STANDARDS.md](../reference/VERSION_CONTROL_STANDARDS.md) -
  Branch naming

### Tools

- [semver.org](https://semver.org/)<!-- link:standards.semver --> - Semantic
  versioning specification
- [schema.org](https://schema.org/) - Schema.org vocabulary
- [JSON-LD Playground](https://json-ld.org/playground/) - Test JSON-LD
- [Schema.org Validator](https://validator.schema.org/) - Validate schemas

______________________________________________________________________

## Contributing

When contributing, please:

1. ✅ Follow conventional commits
1. ✅ Validate schema.org before committing
1. ✅ Sync versions if you change them
1. ✅ Update documentation when needed
1. ✅ Run pre-commit hooks

______________________________________________________________________

## Support

Need help?

- 📖 Check [CONTRIBUTING.md](../governance/CONTRIBUTING.md)
- 💬 Start a
  [Discussion](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->
- 🐛 Open an
  [Issue](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- 📧 Contact maintainers via GitHub

______________________________________________________________________

**Version**: 1.0.0\
**Last Updated**: 2026-01-18\
**Maintained by**:
{{ORG_NAME}} organization

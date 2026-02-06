# Schema.org Implementation README

This directory contains schema.org structured data files for the repository.

## Files

- **organization.jsonld** - Organization-level metadata
- **repository.jsonld** - Repository metadata and version information
- **ai-framework.jsonld** - AI framework application metadata
- **documentation.jsonld** - Documentation metadata

## What is Schema.org?

Schema.org is a collaborative project to create structured data vocabulary for
the web. It helps:

- **Search Engines**: Better understand and index content
- **AI Tools**: Provide rich context for code understanding
- **Automated Tools**: Process metadata programmatically
- **Documentation**: Maintain machine-readable metadata

## Usage

### Validation

Validate all schema.org files:

```bash
python scripts/validate-schema-org.py
```

### Version Synchronization

When bumping versions, sync to all schema files:

```bash
npm run version:sync
```

Or manually:

```bash
node scripts/sync-version.js
```

### Manual Editing

When editing schema files:

1. Maintain valid JSON-LD format
1. Keep `@context` as `https://schema.org`
1. Update `dateModified` to current date
1. Validate after changes
1. Follow semantic versioning for `version` field

## Schema Types

### Organization

Type: `Organization`\
Purpose: Organization-wide information

Key fields:

- `name`: Organization name
- `url`: Organization URL
- `description`: What the organization does
- `contactPoint`: Support information
- `owns`: List of owned repositories

### Repository

Type: `SoftwareSourceCode`\
Purpose: Repository metadata and code information

Key fields:

- `name`: Repository name
- `version`: Current version (semver)
- `codeRepository`: Git repository URL
- `programmingLanguage`: Languages used
- `featureList`: Key features
- `keywords`: Searchable keywords

### AI Framework

Type: `SoftwareApplication`\
Purpose: AI framework application metadata

Key fields:

- `name`: Application name
- `version`: Current version
- `applicationCategory`: Type of application
- `featureList`: Framework features
- `hasPart`: Components (agents, MCP servers, etc.)

### Documentation

Type: `TechArticle`\
Purpose: Documentation metadata

Key fields:

- `name`: Documentation name
- `version`: Documentation version
- `description`: What the docs cover
- `hasPart`: Documentation sections
- `numberOfPages`: Page count

## Automation

### GitHub Workflows

Schema.org validation runs automatically on:

- Pull requests (when `.schema-org/**` files change)
- Push to main branch
- Manual workflow dispatch

### Pre-commit Hooks

Validation runs as part of pre-commit hooks:

```bash
pre-commit install
```

### CI/CD Integration

Schema validation is integrated into CI/CD:

```yaml
- name: Validate schemas
  run: python scripts/validate-schema-org.py
```

## Best Practices

1. ✅ **Always validate** before committing
1. ✅ **Keep versions synced** across all files
1. ✅ **Update dateModified** when making changes
1. ✅ **Use descriptive keywords** for discoverability
1. ✅ **Link entities properly** using `@id` and `isPartOf`
1. ✅ **Follow schema.org standards** for all fields
1. ✅ **Test in JSON-LD Playground** before committing

## Resources

- [Schema.org Documentation](https://schema.org/docs/documents.html)
- [JSON-LD Playground](https://json-ld.org/playground/)
- [Schema.org Validator](https://validator.schema.org/)
- [SoftwareSourceCode Schema](https://schema.org/SoftwareSourceCode)
- [Organization Schema](https://schema.org/Organization)

## Support

For questions or issues:

- 📖 See
  [SCHEMA_ORG_SEMVER_GUIDE.md](../../docs/guides/SCHEMA_ORG_SEMVER_GUIDE.md)
- 💬
  [Start a Discussion](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->
- 🐛
  [Open an Issue](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->

______________________________________________________________________

**Last Updated**: 2026-01-18\
**Version**: 1.0.0

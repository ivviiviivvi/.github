# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## \[Unreleased\]

### Added

- Comprehensive 246-line documentation INDEX.md organizing 133+ files (Phase 2.2)
- Comprehensive security best practices guide (850+ lines) (Phase 5.2)
- Dependency management guide (500+ lines) (Phase 5.3)
- Initial repository setup with comprehensive community health files
- GitHub Actions workflows for automation
- Issue and PR templates
- Security policies and scanning

### Changed

- Consolidated 12 duplicate documentation files with backward-compatible redirects (Phase 2.1)
- Reorganized documentation into clear hierarchy: guides/, governance/, workflows/, architecture/ (Phase 2.2)
- Resolved index.md/INDEX.md case conflict (renamed to walkthrough-gallery.md) (Phase 2.2)
- Enhanced bug report template with 8-point PII warning and log sanitization guide (Phase 5.1)
- Updated security policy to mandate private-only vulnerability disclosure (Phase 5.1)
- Consolidated documentation into structured docs/ subdirectories and centralized config files

### Removed

- Public security vulnerability disclosure template (Phase 5.1 - security risk mitigation)
- Obsolete guides/WORKFLOW_OPTIMIZATION_ROADMAP.md redirect (Phase 2.1)

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- N/A

---

## How to Update This Changelog

When making changes to the project, please update this changelog following these
guidelines:

### Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Example Entry

```markdown
## [1.0.0] - 2024-01-15

### Added

- New user authentication system
- API endpoint for user registration
- Email verification workflow

### Changed

- Updated database schema to support new user fields
- Improved error handling in API responses

### Fixed

- Fixed memory leak in background processing
- Resolved race condition in concurrent requests

### Security

- Patched XSS vulnerability in user input handling
```

### Version Format

- **\[Unreleased\]** - For upcoming changes that haven't been released yet
- **\[MAJOR.MINOR.PATCH\] - YYYY-MM-DD** - For released versions with date
  - MAJOR version for incompatible API changes
  - MINOR version for added functionality in a backwards compatible manner
  - PATCH version for backwards compatible bug fixes

### Best Practices

1. **Keep it current**: Update the changelog with every significant change
1. **Be descriptive**: Explain what changed and why
1. **Link issues**: Reference issue/PR numbers where applicable
1. **Group changes**: Keep similar changes together under the same category
1. **Date releases**: Always include the release date for version entries
1. **Link versions**: Add comparison links at the bottom of the file

### Comparison Links Template

```markdown
[Unreleased]: https://github.com/username/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/repo/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/username/repo/releases/tag/v0.9.0
```

---

<!-- Automated changelog generation will append below this line -->

---

## description: 'Organization-wide version control and documentation standards enforcement' applyTo: '\*\*'

# Version Control and Documentation Standards

## Version Control Standards

When working with version control:

1. **Semantic Versioning**: Use semantic versioning (MAJOR.MINOR.PATCH) for all
   releases

   - Format: `v1.0.0`, `v1.1.0`, `v2.0.0`
   - MAJOR: Breaking changes
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes (backward compatible)

1. **Branch Naming**: Follow hierarchical naming convention

   - Format: `<lifecycle-phase>/<feature-type>/<component>/<subcomponent>`
   - Examples:
     - `develop/feature/user-authentication/oauth-providers`
     - `production/hotfix/critical-security-fix`
     - `maintenance/v1.x/security-patches`
     - `archive/v1/legacy-implementation`
   - Use lowercase with hyphens only
   - Be descriptive but concise
   - Maximum 4 levels deep

1. **Commit Messages**: Follow Conventional Commits format

   - Format: `<type>(<scope>): <subject>`
   - Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
   - Breaking changes: Use `!` suffix or `BREAKING CHANGE:` footer
   - Examples:
     - `feat(auth): add OAuth2 authentication`
     - `fix: resolve memory leak in data processor`
     - `feat!: redesign API (BREAKING CHANGE)`

1. **Git Tags**: Tag all releases with annotated tags

   - Format: `v<MAJOR>.<MINOR>.<PATCH>`
   - Use annotated tags: `git tag -a v1.0.0 -m "Release version 1.0.0"`
   - Pre-release: `v1.0.0-alpha.1`, `v1.0.0-beta.1`, `v1.0.0-rc.1`

1. **Branch Types**:

   - `main`: Production-ready code (permanent)
   - `develop`: Integration branch (permanent)
   - `<lifecycle>/feature/*`: New features (temporary)
   - `<lifecycle>/bugfix/*`: Bug fixes (temporary)
   - `production/hotfix/*`: Critical production fixes (temporary)
   - `release/v*`: Release preparation (temporary)
   - `maintenance/v*`: Long-term support branches (long-lived)
   - `archive/*`: Historical reference (permanent)

## Markdown Documentation Standards

When writing markdown documentation:

1. **NO EMOJI**: Never use emoji or decorative Unicode characters in
   documentation

1. **Language**: Use American English spelling

   - color (not colour)
   - organize (not organise)
   - center (not centre)

1. **Headings**:

   - Use sentence case (not title case)
   - Only one H1 per document (the title)
   - Do not skip heading levels
   - No punctuation at end of headings

1. **Lists**:

   - Use hyphens (-) for unordered lists
   - Use sequential numbers for ordered lists
   - Indent nested items with 2 spaces

1. **Code Blocks**:

   - Always specify language for syntax highlighting
   - Examples: `bash, `javascript, \`\`\`python

1. **Links**:

   - Use descriptive link text (not "click here")
   - Use relative paths for internal links
   - Test all links to ensure they work

1. **Terminology**:

   - Use consistent terms throughout
   - repository (not repo in formal docs)
   - pull request (not PR in formal docs)
   - Git (capitalized)
   - GitHub (capitalized)

1. **Writing Style**:

   - Active voice preferred
   - Present tense for documentation
   - Second person for instructions
   - Use Oxford comma
   - Professional but approachable tone

1. **Document Structure**:

   - Start with title (H1) and brief description
   - Include table of contents for longer documents
   - End with "Last Updated" date
   - Use horizontal rules (---) to separate major sections

1. **Code Examples**:

   - Provide complete, runnable examples
   - Include comments to explain code
   - Use realistic placeholder values

## References

See these organization standards documents:

- [VERSION_CONTROL_STANDARDS.md](../VERSION_CONTROL_STANDARDS.md)
- [BRANCH_STRATEGY.md](../BRANCH_STRATEGY.md)
- [RELEASE_PROCESS.md](../RELEASE_PROCESS.md)
- [MARKDOWN_STYLE_GUIDE.md](../MARKDOWN_STYLE_GUIDE.md)
- [SEMANTIC_VERSIONING.md](../SEMANTIC_VERSIONING.md)
- [GIT_WORKFLOW.md](../GIT_WORKFLOW.md)

## Enforcement

When reviewing code or documentation:

1. Verify branch names follow naming conventions
1. Check commit messages follow Conventional Commits
1. Ensure documentation has no emoji
1. Verify markdown follows style guide
1. Check for consistent terminology
1. Validate semantic versioning is used correctly

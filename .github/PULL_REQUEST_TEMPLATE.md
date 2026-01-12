## Description

<!-- Provide a clear and concise description of your changes -->



## Type of Change

<!-- Check all that apply -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] ♻️ Code refactor (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Configuration change
- [ ] 🎨 Style/UI change

## Related Issues

<!-- Link related issues using GitHub's closing keywords -->
<!-- Examples: Closes #123, Fixes #456, Resolves #789 -->

- Closes #
- Related to #

## Changes Made

<!-- List the specific changes in this PR -->

- 
- 
- 

## Checklist

<!-- Check all items that apply. Add N/A if not applicable -->

### Code Quality
- [ ] My code follows the project's code style and conventions
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors
- [ ] I have removed any debugging code or console logs

### Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this change in a development/staging environment
- [ ] Edge cases have been considered and tested

### Documentation
- [ ] I have updated the documentation accordingly
- [ ] I have updated the README if needed
- [ ] I have added/updated code comments where necessary
- [ ] I have updated the CHANGELOG (if applicable)

### Security & Performance
- [ ] I have considered security implications of my changes
- [ ] No sensitive data (API keys, passwords, tokens) is exposed
- [ ] My changes do not introduce performance regressions
- [ ] I have reviewed the code for potential security vulnerabilities

### Pre-commit & CI
- [ ] Pre-commit hooks pass locally
- [ ] All CI/CD checks pass
- [ ] Linting passes without errors
- [ ] Code coverage has not decreased (or is justified)

## Screenshots / Video

<!-- If your changes include UI/UX updates, add screenshots or video here -->
<!-- Delete this section if not applicable -->

### Before


### After


## Reviewer Notes

<!-- Add any context or notes for reviewers -->
<!-- Highlight areas that need special attention -->
<!-- Mention any trade-offs or decisions made -->



## Testing Instructions

<!-- Provide step-by-step instructions for reviewers to test your changes -->

1. 
2. 
3. 

## Deployment Notes

<!-- Any special deployment considerations, migration steps, or configuration changes -->
<!-- Delete this section if not applicable -->



## Rollback Plan

<!-- How can this change be rolled back if needed? -->
<!-- Delete this section if not applicable -->



---

### Conventional Commit Reminder

Please ensure your commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Example:**
```
feat(auth): add OAuth2 authentication

Implements OAuth2 authentication flow with Google and GitHub providers.
Includes token refresh logic and secure session management.

Closes #123
```

---

### Contributing Guidelines

Please review our [CONTRIBUTING.md](../CONTRIBUTING.md) for code standards, branch naming conventions, and the full contribution workflow.

---

**For Reviewers:**
- [ ] Code is understandable and maintainable
- [ ] Changes align with project architecture
- [ ] Security considerations have been addressed
- [ ] Performance impact is acceptable
- [ ] Documentation is adequate
- [ ] Tests provide sufficient coverage

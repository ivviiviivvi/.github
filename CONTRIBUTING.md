# Contributing Guidelines

## Commit Guidelines

We follow a structured approach to tracking and managing commits in this project. Please adhere to these guidelines when contributing.

### Commit Message Format

We use conventional commit messages to maintain a clean and trackable history:

```
<type>: <subject>

<body>

<footer>
```

#### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries

#### Subject

The subject contains a succinct description of the change:

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No dot (.) at the end
- Keep it under 50 characters

#### Body (Optional)

Just as in the subject, use the imperative, present tense. The body should include the motivation for the change and contrast this with previous behavior.

#### Footer (Optional)

The footer should contain any information about Breaking Changes and is also the place to reference issues that this commit closes.

### Examples

#### Good Commit Messages

```
feat: add commit tracking workflow

This workflow automatically tracks all commits pushed to main and develop
branches. It generates statistics and validates commit messages.

Resolves: #4
```

```
fix: correct workflow syntax in commit-tracking.yml

The previous version had incorrect indentation in the YAML file.
```

```
docs: update README with commit tracking information
```

#### Bad Commit Messages

```
Updated stuff
```

```
fix
```

```
changing things that were broken
```

### Setting Up Commit Message Template

To use the provided commit message template:

```bash
git config commit.template .github/.gitmessage
```

This will set the template for your local repository.

### Commit Tracking

This repository includes automated commit tracking via GitHub Actions:

- **Commit Validation**: All commits are validated for proper format and meaningful content
- **Commit Statistics**: Statistics are generated for recent commit activity
- **Author Tracking**: Tracks contributions by different authors
- **Pull Request Tracking**: Monitors all commits in pull requests

### Pull Request Guidelines

When creating a pull request:

1. Ensure all commits follow the commit message format
2. Keep commits atomic - one logical change per commit
3. Squash "fix typo" or "address review comments" commits before merging
4. Reference relevant issues in commit messages or PR description

### Questions?

If you have questions about contributing, please open an issue for discussion.
Thank you for considering contributing to our projects! We welcome contributions from everyone.

## How to Contribute

### Reporting Issues

- Check if the issue already exists before creating a new one
- Use a clear and descriptive title
- Provide detailed information about the issue including:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment details (OS, version, etc.)

### Submitting Pull Requests

1. **Fork the repository** and create your branch from the default branch
2. **Make your changes** following the code style of the project
3. **Test your changes** to ensure they work as expected
4. **Commit your changes** with clear, descriptive commit messages
5. **Push to your fork** and submit a pull request

### Pull Request Guidelines

- Keep pull requests focused on a single feature or fix
- Write clear, concise commit messages
- Include tests for new features when applicable
- Update documentation as needed
- Ensure all tests pass before submitting
- Reference related issues in your PR description

### Code Style

- Follow the existing code style in the project
- Use meaningful variable and function names
- Comment complex logic
- Keep functions small and focused

### Testing

- Write tests for new features and bug fixes
- Ensure all existing tests pass
- Run the test suite before submitting your PR

## Code Review Process

All submissions require review before being merged. We aim to review pull requests promptly and provide constructive feedback.

## Community

- Be respectful and inclusive
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Help others when you can

## Questions?

If you have questions, please check our [Support documentation](SUPPORT.md) or open an issue for discussion.

Thank you for contributing! 🎉

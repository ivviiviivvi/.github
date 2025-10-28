# .github

This repository contains GitHub-specific configurations and workflows for tracking and managing project commits.

## Features

### 🔍 Commit Tracking

This repository includes comprehensive commit tracking functionality:

- **Automated Commit Validation**: Validates commit messages for quality and format
- **Commit Statistics**: Generates detailed statistics on commit activity
- **Weekly Reports**: Automatically generates weekly commit reports
- **Author Tracking**: Tracks contributions by different authors
- **Pull Request Monitoring**: Monitors and validates commits in pull requests

### 📁 What's Inside

- `.github/workflows/commit-tracking.yml` - Automated commit tracking workflow
- `.github/workflows/weekly-commit-report.yml` - Weekly commit report generation
- `.github/.gitmessage` - Commit message template
- `CONTRIBUTING.md` - Contribution guidelines with commit conventions

## Getting Started

### Using the Commit Message Template

To use the provided commit message template in your local repository:

```bash
git config commit.template .github/.gitmessage
```

### Commit Message Format

We follow conventional commit format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

**Examples**:
- `feat: add user authentication`
- `fix: resolve memory leak in data processor`
- `docs: update API documentation`

### Viewing Commit Reports

Commit tracking runs automatically on:
- Every push to `main` or `develop` branches
- Every pull request update

Weekly reports are generated every Monday and stored in the `reports/` directory.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on commit conventions and contribution workflow.

## Workflows

### Commit Tracking Workflow
- **Trigger**: Push to main/develop or PR updates
- **Actions**: Validates commits, generates statistics, creates summary

### Weekly Commit Report
- **Trigger**: Every Monday at 9:00 AM UTC (or manual trigger)
- **Actions**: Generates comprehensive weekly report and commits it to the repository

## License

This is a configuration repository for GitHub-specific settings.
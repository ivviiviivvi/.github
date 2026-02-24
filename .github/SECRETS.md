# Required Secrets Configuration

This document lists all secrets referenced by workflows in this repository.

> **Repository:** https://github.com/{{ORG_NAME}}/.github.git

## Secret Categories

### GitHub Authentication

| Secret               | Description                                     | Required |
| -------------------- | ----------------------------------------------- | -------- |
| `GITHUB_TOKEN`       | Auto-provided by GitHub Actions                 | Auto     |
| `GH_TOKEN`           | Personal Access Token with extended permissions | Yes      |
| `GH_PAT`             | Personal Access Token for cross-repo operations | Optional |
| `ADD_TO_PROJECT_PAT` | PAT for GitHub Projects automation              | Optional |

### AI/LLM Services

| Secret                    | Description                       | Required |
| ------------------------- | --------------------------------- | -------- |
| `CLAUDE_CODE_OAUTH_TOKEN` | Anthropic Claude Code OAuth token | Optional |
| `GEMINI_API_KEY`          | Google Gemini API key             | Optional |
| `GOOGLE_API_KEY`          | Google API key (for Gemini)       | Optional |
| `OPENAI_API_KEY`          | OpenAI API key                    | Optional |
| `GROK_API_KEY`            | xAI Grok API key                  | Optional |
| `PERPLEXITY_API_KEY`      | Perplexity AI API key             | Optional |

### GitHub Apps

| Secret            | Description                               | Required |
| ----------------- | ----------------------------------------- | -------- |
| `APP_PRIVATE_KEY` | GitHub App private key for authentication | Optional |

### Security & Scanning

| Secret              | Description                     | Required |
| ------------------- | ------------------------------- | -------- |
| `SEMGREP_APP_TOKEN` | Semgrep security scanning token | Optional |

### Notifications

| Secret                      | Description                         | Required |
| --------------------------- | ----------------------------------- | -------- |
| `SLACK_WEBHOOK_URL`         | Primary Slack webhook URL           | Optional |
| `SLACK_WEBHOOK`             | Alternative Slack webhook           | Optional |
| `SLACK_WEBHOOK_ALERTS`      | Slack webhook for alerts channel    | Optional |
| `SLACK_WEBHOOK_METRICS`     | Slack webhook for metrics channel   | Optional |
| `PAGERDUTY_INTEGRATION_KEY` | PagerDuty integration for incidents | Optional |

### Docker Registry

| Secret            | Description               | Required |
| ----------------- | ------------------------- | -------- |
| `DOCKER_USERNAME` | Docker Hub username       | Optional |
| `DOCKER_PASSWORD` | Docker Hub password/token | Optional |

### Email (SMTP)

| Secret              | Description                  | Required |
| ------------------- | ---------------------------- | -------- |
| `SMTP_SERVER`       | SMTP server hostname         | Optional |
| `SMTP_PORT`         | SMTP server port             | Optional |
| `SMTP_USERNAME`     | SMTP authentication username | Optional |
| `SMTP_PASSWORD`     | SMTP authentication password | Optional |
| `DIGEST_RECIPIENTS` | Email recipients for digests | Optional |

### Package Registries

| Secret      | Description                       | Required |
| ----------- | --------------------------------- | -------- |
| `NPM_TOKEN` | NPM registry authentication token | Optional |

### External Services

| Secret                     | Description                     | Required |
| -------------------------- | ------------------------------- | -------- |
| `AUTH_TOKEN`               | Generic authentication token    | Optional |
| `OP_SERVICE_ACCOUNT_TOKEN` | 1Password Service Account token | Optional |

## Setup Instructions

### Minimum Required Secrets

For basic functionality, configure these secrets:

1. **`GH_TOKEN`** - A GitHub Personal Access Token with these scopes:
   - `repo` (full control of private repositories)
   - `workflow` (update GitHub Action workflows)
   - `read:org` (read organization membership)

### AI-Powered Features

To enable AI code review and automation:

1. **Claude Code:** Set `CLAUDE_CODE_OAUTH_TOKEN`
1. **Gemini:** Set both `GEMINI_API_KEY` and `GOOGLE_API_KEY`
1. **OpenAI:** Set `OPENAI_API_KEY`

### Security Scanning

For Semgrep security scanning:

1. Create account at https://semgrep.dev
1. Generate app token
1. Set `SEMGREP_APP_TOKEN`

### Slack Notifications

For workflow notifications:

1. Create Slack App with Incoming Webhooks
1. Set `SLACK_WEBHOOK_URL` to primary channel webhook

## Validation

Run this command to check which secrets are configured:

```bash
gh secret list
```

## Adding Secrets

```bash
# Via GitHub CLI
gh secret set SECRET_NAME

# Or via GitHub UI
# Settings > Secrets and variables > Actions > New repository secret
```

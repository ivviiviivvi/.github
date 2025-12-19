# GitHub Copilot Actions Setup and Troubleshooting

## Overview

This document provides guidance on setting up and troubleshooting GitHub Copilot Actions in workflows, including AI-powered actions like Claude Code and Gemini CLI. These steps are essential to avoid content filtering policy blocks and ensure proper communication with AI endpoints.

## Prerequisites

Before using AI-powered GitHub Actions in your workflows, ensure you have:

1. **GitHub Copilot Actions Environment** properly configured
2. **Network/Firewall rules** allowing communication with required endpoints
3. **Required secrets and tokens** configured in your repository

## Setup Steps

### 1. Add GitHub Copilot Actions Setup Step

All workflows that use AI-powered actions (Claude, Gemini, etc.) should include the GitHub Copilot Actions setup step **before** running any AI action:

```yaml
steps:
  - name: Setup GitHub Copilot Actions Environment
    uses: github/copilot-actions-setup@v1

  - name: Checkout repository
    uses: actions/checkout@v4
    
  # Your AI-powered action steps here
  - name: Run Claude Code
    uses: anthropics/claude-code-action@v1
    with:
      claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### 2. Configure Firewall and Network Access

If your GitHub Actions runners are behind a firewall or security gateway, you must allow outbound access to the following endpoints:

#### Required Endpoints

Add these URLs/hosts to your firewall allow list:

- **GitHub Copilot endpoints**: See [GitHub Copilot Firewall Configuration](https://gh.io/copilot/firewall-config)
- **Anthropic AI endpoints** (for Claude):
  - `api.anthropic.com`
  - `*.anthropic.com`
- **Google AI endpoints** (for Gemini):
  - `generativelanguage.googleapis.com`
  - `aiplatform.googleapis.com`
  - `*.googleapis.com`

#### Network Requirements

Ensure your network infrastructure allows:
- **HTTPS (port 443)** outbound connections
- **WebSocket connections** for real-time AI interactions
- **TLS 1.2 or higher** for secure communications

### 3. Configure Security Gateway and Content Filtering

If your organization uses a security gateway that inspects outbound traffic:

1. **Disable SSL inspection** for AI endpoints (if possible) to prevent interference with encrypted communications
2. **Configure content filtering policies** to allow AI model requests and responses
3. **Whitelist AI provider domains** in your security appliance
4. **Coordinate with security administrators** to ensure AI traffic is not blocked by content filtering policies

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Output blocked by content filtering policy"

**Symptoms:**
- Workflow fails with exit code 1
- Error message mentions "content filtering policy"
- AI responses are blocked or filtered

**Solutions:**

1. **Verify GitHub Copilot Actions setup step is present:**
   ```yaml
   - name: Setup GitHub Copilot Actions Environment
     uses: github/copilot-actions-setup@v1
   ```

2. **Check firewall configuration:**
   - Follow [GitHub Copilot Actions Setup Steps](https://gh.io/copilot/actions-setup-steps)
   - Review [Firewall Configuration Guide](https://gh.io/copilot/firewall-config)

3. **Review security gateway settings:**
   - Ensure AI endpoints are not being blocked by content inspection
   - Disable SSL/TLS interception for AI provider domains
   - Check for DLP (Data Loss Prevention) policies that might interfere

4. **Verify network connectivity:**
   ```yaml
   - name: Test AI endpoint connectivity
     run: |
       curl -I https://api.anthropic.com
       curl -I https://generativelanguage.googleapis.com
   ```

#### Issue: Repeated AI Model Response Failures

**Symptoms:**
- Multiple retry attempts to get AI responses
- Timeout errors
- Connection refused or reset errors

**Solutions:**

1. **Check rate limits and quotas:**
   - Verify you haven't exceeded API rate limits
   - Check your subscription/billing status with AI providers

2. **Validate authentication tokens:**
   - Ensure secrets are correctly configured
   - Verify tokens haven't expired
   - Check token permissions are sufficient

3. **Review network latency:**
   - Increase timeout values if network latency is high
   - Consider using GitHub-hosted runners in regions closer to AI providers

#### Issue: npm or Playwright Not Available

**Symptoms:**
- Error: "npm: command not found"
- Playwright browser installation failures

**Solutions:**

1. **Add Node.js setup step:**
   ```yaml
   - name: Setup Node.js
     uses: actions/setup-node@v4
     with:
       node-version: '20'
   ```

2. **Install dependencies explicitly:**
   ```yaml
   - name: Install dependencies
     run: npm install
   ```

3. **For Playwright specifically:**
   ```yaml
   - name: Install Playwright browsers
     run: npx playwright install --with-deps
   ```

## Affected Workflows

The following workflows in this repository have been updated with GitHub Copilot Actions setup:

- `.github/workflows/claude.yml` - Claude Code integration
- `.github/workflows/claude-code-review.yml` - Automated PR reviews with Claude
- `.github/workflows/jules.yml` - Jules Agent with quota management
- `.github/workflows/gemini-review.yml` - Gemini PR reviews
- `.github/workflows/gemini-invoke.yml` - Gemini invocation
- `.github/workflows/gemini-triage.yml` - Gemini issue triage
- `.github/workflows/gemini-scheduled-triage.yml` - Scheduled Gemini triage

## Best Practices

### Workflow Configuration

1. **Always include setup step first:**
   ```yaml
   steps:
     - name: Setup GitHub Copilot Actions Environment
       uses: github/copilot-actions-setup@v1
     # ... other steps
   ```

2. **Add timeout values:**
   ```yaml
   jobs:
     ai-task:
       timeout-minutes: 10
   ```

3. **Implement retry logic:**
   ```yaml
   - name: Run AI action with retry
     uses: nick-invision/retry@v2
     with:
       timeout_minutes: 5
       max_attempts: 3
       command: |
         # Your AI action command
   ```

### Security Considerations

1. **Never commit secrets** - Always use GitHub Secrets
2. **Use least privilege** - Grant minimum required permissions
3. **Monitor usage** - Track AI API usage and costs
4. **Review logs** - Regularly check workflow logs for anomalies

### Network Configuration

1. **Document firewall rules** - Maintain up-to-date firewall documentation
2. **Test connectivity** - Regularly validate endpoint access
3. **Monitor network latency** - Track performance metrics
4. **Plan for redundancy** - Have fallback mechanisms for critical workflows

## Additional Resources

- [GitHub Copilot Actions Setup Steps](https://gh.io/copilot/actions-setup-steps)
- [GitHub Copilot Firewall Configuration](https://gh.io/copilot/firewall-config)
- [Claude Code Action Documentation](https://github.com/anthropics/claude-code-action)
- [Google Gemini CLI Documentation](https://github.com/google-github-actions/run-gemini-cli)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

If you continue to experience issues after following this guide:

1. **Check GitHub Status**: [https://www.githubstatus.com](https://www.githubstatus.com)
2. **Review AI Provider Status**:
   - Anthropic Status: [https://status.anthropic.com](https://status.anthropic.com)
   - Google Cloud Status: [https://status.cloud.google.com](https://status.cloud.google.com)
3. **Contact Support**: Open an issue in this repository with:
   - Workflow file name
   - Error messages
   - Workflow run ID
   - Steps already attempted

## Changelog

### 2024-12-18
- Initial documentation created
- Added GitHub Copilot Actions setup step to all AI-powered workflows
- Documented firewall configuration requirements
- Added troubleshooting guide for common issues

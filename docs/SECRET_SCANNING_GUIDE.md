# Secret Scanning Guide

This repository uses automated secret scanning to prevent accidental exposure of sensitive credentials and tokens. This guide explains how the system works and how to manage false positives.

## Overview

We use three complementary tools to scan for secrets:

1. **TruffleHog** - Entropy-based detection and regex patterns
2. **Gitleaks** - Fast, configurable secret scanner with custom rules
3. **detect-secrets** - Baseline-aware scanning with plugin system

## Workflows

### scan-for-secrets.yml

**Triggers:**
- Push to main/master branch
- Pull requests affecting code or video files
- Daily scheduled scan at 2 AM UTC
- Manual workflow dispatch

**What it does:**
- Scans code for secrets using all three tools
- Analyzes video files for exposed credentials using OCR
- Creates GitHub issues if secrets are detected
- Quarantines videos with secrets

### safeguard-5-secret-scanning.yml

**Triggers:**
- Changes to walkthrough videos or JSON configs
- Manual workflow dispatch

**What it does:**
- Pre-record code scanning before walkthrough generation
- Post-record video frame scanning
- Blocks PR merges if secrets are detected in videos
- Creates security alerts for found secrets

## Configuration Files

### .gitleaks.toml

Configuration for Gitleaks scanner that defines:
- **Allowlist paths**: Files that are known to contain example patterns
- **Allowlist regexes**: Patterns that are placeholders or examples
- **Stop words**: Common words that indicate examples
- **Custom rules**: Extended detection rules with allowlists

**Example allowlisted paths:**
- Workflow files that define patterns
- Documentation with examples
- Agent files describing patterns
- Test configurations

### .secrets.baseline

Baseline file for detect-secrets containing:
- Known false positives from documentation
- Plugin configuration
- File-specific findings that are verified safe

Generated with:
```bash
detect-secrets scan --all-files --force-use-all-plugins > .secrets.baseline
```

## Managing False Positives

### When a False Positive is Detected

1. **Verify it's actually a false positive** by checking:
   - Is it in documentation or examples?
   - Is it a pattern definition in the scanner itself?
   - Is it a placeholder like `xxx`, `example`, `your-token-here`?

2. **Update .gitleaks.toml** to allowlist:

```toml
# Add to allowlist.paths
paths = [
  '''path/to/file\.md''',
]

# Or add to allowlist.regexes
regexes = [
  '''your-false-positive-pattern''',
]
```

3. **Update .secrets.baseline** for detect-secrets:

```bash
# Regenerate baseline to include new false positives
detect-secrets scan --all-files --force-use-all-plugins > .secrets.baseline

# Or audit and update existing findings
detect-secrets audit .secrets.baseline
```

4. **Commit both files** to the repository
5. **Rerun the workflow** to verify the false positive is resolved

### Common False Positive Patterns

These are automatically allowlisted:

- **Documentation examples**: `ghp_xxx`, `AKIA...`
- **Placeholder text**: `your-token-here`, `replace-with`
- **Pattern definitions**: Regex patterns in workflow files
- **Example domains**: `example.com`, `localhost`
- **Test data**: Files in `test/`, `examples/` directories

## Real Secret Detection

### If Real Secrets Are Found

**IMMEDIATE ACTIONS:**

1. **🛑 DO NOT MERGE** - Stop any PR or push that contains secrets
2. **🔄 ROTATE CREDENTIALS** - Immediately invalidate and rotate the exposed credentials
3. **🗑️ REMOVE FROM HISTORY** - Use tools to remove secrets from git history:

   ```bash
   # Using BFG Repo-Cleaner
   bfg --delete-files secret-file.txt
   
   # Using git-filter-repo
   git filter-repo --path secret-file.txt --invert-paths
   ```

4. **📹 UPDATE VIDEOS** - If secrets appear in walkthrough videos:
   - Delete the video files
   - Re-record without exposing credentials
   - Use environment variables or dummy credentials
   
5. **📝 DOCUMENT** - Update this issue with:
   - What was exposed
   - Actions taken
   - Lessons learned

### Resources

- [GitHub Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)
- [Removing Sensitive Data from a Repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git-filter-repo](https://github.com/newren/git-filter-repo)

## Best Practices

### For Code

1. **Use environment variables** for secrets
2. **Use .env files** (add to .gitignore)
3. **Use secret management services** (GitHub Secrets, AWS Secrets Manager, etc.)
4. **Never commit** credentials, even temporarily
5. **Use pre-commit hooks** to catch secrets before commit

### For Videos

1. **Use dummy credentials** in demonstrations
2. **Blur sensitive areas** in post-processing
3. **Use environment variables** that aren't shown on screen
4. **Review frames** before publishing
5. **Keep terminal history clean** before recording

### For Documentation

1. **Use placeholders** like `xxx`, `your-token-here`
2. **Clearly mark examples** as examples
3. **Use ellipsis** for partial patterns (`AKIA...`)
4. **Avoid realistic-looking** fake credentials

## Troubleshooting

### Workflow Fails But No Secrets Found

If the workflow fails but all scanners report clean:

1. Check the workflow logs for the actual error
2. Common issues:
   - Python setup failure (missing requirements.txt)
   - Network issues during tool installation
   - Insufficient permissions
3. The issue may be created due to workflow failure, not secret detection

### Scanner Takes Too Long

If scanning is slow:

1. Adjust the scan frequency in workflow triggers
2. Limit paths scanned in workflow configuration
3. Use cached tool installations
4. Consider scanning only changed files in PRs

### Can't Regenerate Baseline

If detect-secrets baseline regeneration fails:

1. Ensure detect-secrets is installed: `pip install detect-secrets`
2. Check file permissions
3. Try clearing and regenerating: `rm .secrets.baseline && detect-secrets scan ...`
4. Update detect-secrets: `pip install --upgrade detect-secrets`

## Workflow Architecture

```
┌─────────────────────────────────────────────┐
│         Secret Scanning System              │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ TruffleHog   │  │  Gitleaks    │        │
│  │ (Entropy)    │  │ (.toml cfg)  │        │
│  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                │
│         └──────┬──────────┘                │
│                │                            │
│         ┌──────▼──────┐                     │
│         │ detect-     │                     │
│         │ secrets     │                     │
│         │ (.baseline) │                     │
│         └──────┬──────┘                     │
│                │                            │
│         ┌──────▼──────────┐                 │
│         │ Scan Results    │                 │
│         └──────┬──────────┘                 │
│                │                            │
│         ┌──────▼──────────┐                 │
│         │ Create Issue /  │                 │
│         │ Block Merge     │                 │
│         └─────────────────┘                 │
│                                             │
└─────────────────────────────────────────────┘
```

## Updating This Guide

When updating secret scanning configuration:

1. Update this guide with any new patterns or rules
2. Document new false positive categories
3. Add examples of resolved issues
4. Update troubleshooting section with new solutions

## Support

For questions or issues with secret scanning:

1. Check this guide first
2. Review workflow logs in GitHub Actions
3. Check `.gitleaks.toml` and `.secrets.baseline` configuration
4. Open an issue with the `security` label
5. Contact the security team: @security-team

---

**Last Updated**: 2025-12-25  
**Maintained By**: Security Team  
**Related Files**: 
- `.gitleaks.toml`
- `.secrets.baseline`
- `.github/workflows/scan-for-secrets.yml`
- `.github/workflows/safeguard-5-secret-scanning.yml`

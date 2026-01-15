# 🔐 Secrets Setup Guide for Autonomous Walkthrough Generation

> Comprehensive guide for configuring API keys and optional integrations

**Last Updated:** December 21, 2025 **Maintainer:** @4444JPP **Support:**
[GitHub Discussions](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [GitHub Token Setup](#github-token-setup)
- [Optional Integrations](#optional-integrations)
  - [OpenAI API](#openai-api-optional)
  - [Voice Cloning Services](#voice-cloning-services-optional)
  - [Storage Solutions](#storage-solutions-optional)
- [Environment Variables Reference](#environment-variables-reference)
- [Setting GitHub Secrets](#setting-github-secrets)
- [Workflow Permissions](#workflow-permissions)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [Cost Considerations](#cost-considerations)

---

## Prerequisites

Before setting up secrets, ensure you have:

### Required Access

- ✅ **Organization Owner** or **Admin** access to the Ivviiviivvi organization
- ✅ **GitHub CLI** installed (optional, for command-line setup)
- ✅ **Repository Admin** access (for repository-level secrets)

### System Requirements

- GitHub Actions enabled in your repository/organization
- Internet access for API services
- Valid payment method (for optional paid integrations)

### Knowledge Prerequisites

- Basic understanding of GitHub Secrets
- Familiarity with environment variables
- Understanding of API key management

---

## Quick Start

### Minimal Setup (Free Tier)

For basic walkthrough generation, you only need:

```yaml
# GitHub automatically provides this - no setup needed!
GITHUB_TOKEN
```

This enables:

- ✅ Basic video generation
- ✅ Standard voiceover
- ✅ Workflow artifacts
- ✅ PR creation and updates

### Enhanced Setup (Recommended)

For better quality and features:

1. **OpenAI API Key** - Enhanced voiceover quality
1. **Storage Solution** - Long-term video storage
1. **Permissions** - Workflow write permissions

Time to set up: ~15 minutes

---

## GitHub Token Setup

### Automatic Token (Default)

GitHub Actions automatically provides a `GITHUB_TOKEN` with standard
permissions.

**No configuration needed!** This token is used for:

- Creating pull requests
- Uploading workflow artifacts
- Accessing repository content
- Posting comments on issues

### Custom Token (Advanced)

For enhanced permissions, create a Personal Access Token (PAT):

#### Step 1: Generate PAT

1. Go to **GitHub Settings** → **Developer Settings** → **Personal Access
   Tokens** → **Tokens (classic)**
1. Click **Generate new token** → **Generate new token (classic)**
1. Name: `Walkthrough Generation Token`
1. Expiration: Choose based on your security policy (90 days recommended)
1. Select scopes:
   ```
   ✅ repo (all)
   ✅ workflow
   ✅ write:packages (if using GitHub Packages)
   ✅ read:org (for organization operations)
   ```
1. Click **Generate token**
1. **Copy the token immediately** (you won't see it again!)

#### Step 2: Add as Organization Secret

1. Go to **Organization Settings** → **Secrets and variables** → **Actions**
1. Click **New organization secret**
1. Name: `WALKTHROUGH_GITHUB_TOKEN`
1. Value: Paste your PAT
1. Repository access: Select which repositories can use this secret
1. Click **Add secret**

#### Step 3: Update Workflow

```yaml
# In your workflow file
env:
  GITHUB_TOKEN: ${{ secrets.WALKTHROUGH_GITHUB_TOKEN }}
```

---

## Optional Integrations

### OpenAI API (Optional)

Enhance voiceover quality with OpenAI's text-to-speech API.

#### Why Use OpenAI?

- 🎤 **Superior Voice Quality**: More natural-sounding narration
- 🗣️ **Multiple Voices**: Choose from various voice profiles
- 🌍 **Multiple Languages**: Support for 50+ languages
- 🎭 **Emotion & Tone**: Better expression and intonation

#### Cost Estimate

- **TTS (Text-to-Speech)**: ~$0.015 per 1,000 characters
- **Typical Walkthrough**: ~2,000-5,000 characters
- **Per Video Cost**: ~$0.03-$0.10

#### Setup Instructions

**Step 1: Create OpenAI Account**

1. Go to [platform.openai.com](https://platform.openai.com)
1. Sign up or log in
1. Go to **API Keys** section
1. Click **Create new secret key**
1. Name: `walkthrough-generation`
1. Copy the API key

**Step 2: Add to GitHub Secrets**

```bash
# Using GitHub CLI
gh secret set OPENAI_API_KEY --org ivviiviivvi --body "sk-..."

# Or via Web UI:
# Settings → Secrets and variables → Actions → New organization secret
```

**Step 3: Configure in Workflow**

```yaml
- name: Generate Walkthrough with OpenAI
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  with:
    voiceover-provider: openai
    voice-model: tts-1-hd
    voice-name: alloy # Options: alloy, echo, fable, onyx, nova, shimmer
```

#### OpenAI Voice Options

| Voice       | Characteristics            | Best For                |
| ----------- | -------------------------- | ----------------------- |
| **alloy**   | Neutral, clear             | Professional demos      |
| **echo**    | Warm, friendly             | User tutorials          |
| **fable**   | Expressive, British accent | Educational content     |
| **onyx**    | Deep, authoritative        | Technical documentation |
| **nova**    | Energetic, clear           | Marketing videos        |
| **shimmer** | Soft, calm                 | Onboarding guides       |

---

### Voice Cloning Services (Optional)

Use your own voice or a custom voice profile.

#### Supported Services

**1. ElevenLabs** (Recommended)

- Most natural voice cloning
- Low latency
- Enterprise features available

**2. Play.ht**

- Good quality
- Affordable pricing
- Fast turnaround

**3. Resemble.ai**

- High quality
- Voice marketplace
- Custom voice creation

#### Setup: ElevenLabs

**Step 1: Create Account & Voice**

1. Go to [elevenlabs.io](https://elevenlabs.io)
1. Sign up for an account
1. Go to **Voice Lab** → **Add Voice**
1. Options:
   - **Clone your voice**: Upload 1-5 minutes of clear audio
   - **Use stock voices**: Choose from voice library
1. Name your voice: `walkthrough-narrator`
1. Copy the **Voice ID**

**Step 2: Get API Key**

1. Go to **Profile** → **API Keys**
1. Click **Generate API Key**
1. Copy the key

**Step 3: Add Secrets**

```bash
# API Key
gh secret set ELEVENLABS_API_KEY --org ivviiviivvi

# Voice ID
gh secret set ELEVENLABS_VOICE_ID --org ivviiviivvi
```

**Step 4: Configure Workflow**

```yaml
env:
  ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY }}
  ELEVENLABS_VOICE_ID: ${{ secrets.ELEVENLABS_VOICE_ID }}
with:
  voiceover-provider: elevenlabs
  voice-stability: 0.75
  voice-similarity: 0.85
```

#### Cost Estimates - Voice Cloning

| Service     | Free Tier         | Paid Plans     | Per Character  |
| ----------- | ----------------- | -------------- | -------------- |
| ElevenLabs  | 10k chars/month   | From $5/month  | $0.18/1k chars |
| Play.ht     | 2,500 words/month | From $19/month | Variable       |
| Resemble.ai | 300 seconds free  | From $29/month | $0.006/second  |

---

### Storage Solutions (Optional)

Store walkthroughs long-term beyond GitHub's 90-day artifact retention.

#### Option 1: AWS S3

**Setup:**

1. Create S3 bucket
1. Create IAM user with S3 permissions
1. Generate access keys

**Add Secrets:**

```bash
gh secret set AWS_ACCESS_KEY_ID --org ivviiviivvi
gh secret set AWS_SECRET_ACCESS_KEY --org ivviiviivvi
gh secret set AWS_S3_BUCKET --org ivviiviivvi --body "walkthrough-videos"
gh secret set AWS_REGION --org ivviiviivvi --body "us-east-1"
```

**IAM Policy (Minimal Permissions):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:PutObjectAcl", "s3:GetObject"],
      "Resource": "arn:aws:s3:::walkthrough-videos/*"
    }
  ]
}
```

#### Option 2: Google Cloud Storage

**Setup:**

1. Create GCS bucket
1. Create service account
1. Download JSON key file

**Add Secret:**

```bash
# Upload the entire JSON key as a secret
gh secret set GCP_SERVICE_ACCOUNT_KEY --org ivviiviivvi < key.json
gh secret set GCS_BUCKET --org ivviiviivvi --body "walkthrough-videos"
```

#### Option 3: Azure Blob Storage

**Setup:**

1. Create storage account
1. Create container
1. Get connection string

**Add Secret:**

```bash
gh secret set AZURE_STORAGE_CONNECTION_STRING --org ivviiviivvi
gh secret set AZURE_CONTAINER --org ivviiviivvi --body "walkthroughs"
```

#### Option 4: GitHub Releases (Free!)

For permanent storage without external services:

```yaml
- name: Upload to Release
  uses: softprops/action-gh-release@v1
  with:
    files: walkthrough.mp4
    tag_name: walkthrough-${{ github.run_id }}
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Pros**: Free, no external service, permanent storage **Cons**: Clutters
releases, large files count against repository size

---

## Environment Variables Reference

### Required Variables

| Variable       | Description           | Default       | Where to Set |
| -------------- | --------------------- | ------------- | ------------ |
| `GITHUB_TOKEN` | GitHub authentication | Auto-provided | Automatic    |

### Optional Variables - Voiceover

| Variable              | Description      | Example       | Required For |
| --------------------- | ---------------- | ------------- | ------------ |
| `OPENAI_API_KEY`      | OpenAI API key   | `sk-proj-...` | OpenAI TTS   |
| `OPENAI_VOICE_MODEL`  | TTS model        | `tts-1-hd`    | OpenAI TTS   |
| `OPENAI_VOICE_NAME`   | Voice selection  | `alloy`       | OpenAI TTS   |
| `ELEVENLABS_API_KEY`  | ElevenLabs key   | `el_...`      | ElevenLabs   |
| `ELEVENLABS_VOICE_ID` | Voice profile ID | `21m00Tcm...` | ElevenLabs   |
| `PLAYHT_API_KEY`      | Play.ht API key  | `ph_...`      | Play.ht      |
| `PLAYHT_USER_ID`      | Play.ht user ID  | `user_...`    | Play.ht      |

### Optional Variables - Storage

| Variable                          | Description      | Example               | Required For |
| --------------------------------- | ---------------- | --------------------- | ------------ |
| `AWS_ACCESS_KEY_ID`               | AWS access key   | `AKIA...`             | AWS S3       |
| `AWS_SECRET_ACCESS_KEY`           | AWS secret key   | `secret`              | AWS S3       |
| `AWS_S3_BUCKET`                   | S3 bucket name   | `videos`              | AWS S3       |
| `AWS_REGION`                      | AWS region       | `us-east-1`           | AWS S3       |
| `GCP_SERVICE_ACCOUNT_KEY`         | GCP JSON key     | `{...}`               | Google Cloud |
| `GCS_BUCKET`                      | GCS bucket name  | `videos`              | Google Cloud |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure connection | `DefaultEndpoints...` | Azure        |
| `AZURE_CONTAINER`                 | Container name   | `walkthroughs`        | Azure        |

### Optional Variables - Customization

| Variable              | Description             | Example     | Default     |
| --------------------- | ----------------------- | ----------- | ----------- |
| `VIDEO_RESOLUTION`    | Output resolution       | `1920x1080` | `1920x1080` |
| `VIDEO_FPS`           | Frames per second       | `30`        | `30`        |
| `VIDEO_BITRATE`       | Video bitrate           | `5000k`     | `3000k`     |
| `AUDIO_BITRATE`       | Audio bitrate           | `192k`      | `128k`      |
| `RECORDING_DELAY`     | Initial delay (seconds) | `10`        | `5`         |
| `MASK_SENSITIVE_DATA` | Enable masking          | `true`      | `false`     |

---

## Setting GitHub Secrets

### Organization-Level Secrets (Recommended)

Share secrets across all repositories in the organization.

#### Via Web UI

1. Go to **Organization Settings**
1. Click **Secrets and variables** → **Actions**
1. Click **New organization secret**
1. Enter name and value
1. Select repository access:
   - **All repositories** (easiest)
   - **Private repositories** (more secure)
   - **Selected repositories** (most secure)
1. Click **Add secret**

#### Via GitHub CLI

```bash
# Set organization secret
gh secret set SECRET_NAME --org ivviiviivvi --body "secret-value"

# Set organization secret from file
gh secret set SECRET_NAME --org ivviiviivvi < secret-file.txt

# List organization secrets
gh secret list --org ivviiviivvi
```

### Repository-Level Secrets

For repository-specific configurations.

#### Via Web UI

1. Go to **Repository Settings**
1. Click **Secrets and variables** → **Actions**
1. Click **New repository secret**
1. Enter name and value
1. Click **Add secret**

#### Via GitHub CLI

```bash
# Set repository secret
gh secret set SECRET_NAME --repo ivviiviivvi/repository-name --body "value"

# Set from file
gh secret set SECRET_NAME --repo ivviiviivvi/repository-name < file.txt

# List repository secrets
gh secret list --repo ivviiviivvi/repository-name
```

### Environment-Level Secrets

For production vs. staging configurations.

#### Via Web UI

1. Go to **Repository Settings** → **Environments**
1. Create environment (e.g., `production`, `staging`)
1. Add secrets to specific environment
1. Configure environment protection rules

#### In Workflow

```yaml
jobs:
  generate:
    environment: production # Use production secrets
    steps:
      - name: Generate Walkthrough
        env:
          API_KEY: ${{ secrets.API_KEY }} # From production environment
```

---

## Workflow Permissions

### Configure Repository Permissions

**Step 1: Set Workflow Permissions**

1. Go to **Repository Settings** → **Actions** → **General**
1. Scroll to **Workflow permissions**
1. Select: **Read and write permissions**
1. Enable: **Allow GitHub Actions to create and approve pull requests**
1. Click **Save**

**Step 2: GITHUB_TOKEN Permissions in Workflow**

```yaml
permissions:
  contents: write # For creating releases
  pull-requests: write # For creating PRs
  issues: write # For commenting on issues
  actions: read # For reading workflow data
```

### Organization-Level Permissions

**Step 1: Configure Organization Settings**

1. Go to **Organization Settings** → **Actions** → **General**
1. Enable: **Allow all actions and reusable workflows**
1. Or: **Allow select actions and reusable workflows**
1. Configure: **Workflow permissions**

**Step 2: Review Security Settings**

Ensure workflows can:

- ✅ Create PRs
- ✅ Upload artifacts
- ✅ Post comments
- ✅ Create releases (optional)

---

## Troubleshooting

### Common Issues

#### Issue: "Bad credentials" or "401 Unauthorized"

**Symptoms:**

```
Error: HttpError: Bad credentials
```

**Solutions:**

1. **Check Token Expiration:**

   ```bash
   # Test token validity
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   ```

1. **Verify Secret Name:**
   - Ensure secret name matches workflow reference
   - Check for typos or case sensitivity

1. **Regenerate Token:**
   - Create new PAT with correct scopes
   - Update secret value

1. **Check Permissions:**
   - Verify token has required scopes
   - Check repository access settings

#### Issue: OpenAI API "Rate limit exceeded"

**Symptoms:**

```
Error: Rate limit reached for requests
```

**Solutions:**

1. **Check API Quota:**
   - Log into OpenAI dashboard
   - View usage and limits

1. **Add Retry Logic:**

   ```yaml
   - name: Generate with Retry
     uses: nick-fields/retry@v2
     with:
       timeout_minutes: 10
       max_attempts: 3
       command: npm run generate-walkthrough
   ```

1. **Upgrade Plan:**
   - Consider higher tier for more requests

#### Issue: "Secret not found"

**Symptoms:**

```
Error: Secret OPENAI_API_KEY not found
```

**Solutions:**

1. **Verify Secret Exists:**

   ```bash
   gh secret list --org ivviiviivvi
   ```

1. **Check Repository Access:**
   - Organization secret: verify repository is selected
   - Environment secret: ensure correct environment

1. **Check Secret Name:**
   - Must be UPPERCASE with underscores
   - No spaces or special characters

1. **Redeploy Secret:**

   ```bash
   gh secret set OPENAI_API_KEY --org ivviiviivvi --body "new-value"
   ```

#### Issue: "Workflow permission denied"

**Symptoms:**

```
Error: Resource not accessible by integration
```

**Solutions:**

1. **Update Workflow Permissions:**

   ```yaml
   permissions:
     contents: write
     pull-requests: write
   ```

1. **Repository Settings:**
   - Settings → Actions → Workflow permissions
   - Enable: Read and write permissions

1. **Organization Policy:**
   - Check organization-wide action policies
   - Ensure repository can use workflows

#### Issue: Voice cloning "Invalid voice ID"

**Symptoms:**

```
Error: Voice ID not found or access denied
```

**Solutions:**

1. **Verify Voice ID:**
   - Log into voice provider dashboard
   - Copy voice ID exactly

1. **Check API Key Permissions:**
   - Ensure API key has voice access
   - Verify voice is in your account

1. **Test API Connection:**

   ```bash
   curl -X GET https://api.elevenlabs.io/v1/voices \
     -H "xi-api-key: $ELEVENLABS_API_KEY"
   ```

#### Issue: S3 upload "Access Denied"

**Symptoms:**

```
Error: Access Denied when uploading to S3
```

**Solutions:**

1. **Check IAM Permissions:**
   - Verify policy includes `s3:PutObject`
   - Check bucket policy

1. **Verify Bucket Name:**
   - Ensure bucket exists
   - Check region is correct

1. **Test AWS Credentials:**

   ```bash
   aws s3 ls s3://your-bucket --profile test
   ```

---

## Security Best Practices

### Secret Management

#### Do's ✅

- ✅ **Use Organization Secrets**: Share secrets across repos securely
- ✅ **Rotate Regularly**: Change API keys every 90 days
- ✅ **Use Selected Repos**: Limit secret access to necessary repositories
- ✅ **Monitor Usage**: Review audit logs regularly
- ✅ **Use Environments**: Separate production from development
- ✅ **Principle of Least Privilege**: Grant minimum required permissions
- ✅ **Enable 2FA**: On all accounts with API keys

#### Don'ts ❌

- ❌ **Never Commit Secrets**: Don't put secrets in code or config files
- ❌ **No Logging**: Don't log secret values
- ❌ **No Sharing**: Don't share secrets via chat or email
- ❌ **No Broad Access**: Don't give secrets to all repositories
- ❌ **No Long Expiry**: Don't use tokens that never expire
- ❌ **No Production Data**: Don't use production credentials in walkthroughs

### Token Security

**PAT Best Practices:**

```yaml
# ✅ GOOD: Minimal scopes
scopes:
  - repo
  - workflow

# ❌ BAD: Excessive permissions
scopes:
  - admin:org        # Avoid if not needed
  - delete:packages  # Avoid if not needed
```

**Rotation Schedule:**

| Secret Type    | Rotation Frequency | Priority |
| -------------- | ------------------ | -------- |
| GitHub PAT     | 90 days            | High     |
| OpenAI API Key | 180 days           | Medium   |
| Voice API Keys | 180 days           | Medium   |
| Storage Keys   | 90 days            | High     |

### Audit & Monitoring

**Enable Audit Logging:**

1. Organization Settings → Audit log
1. Review secret access events
1. Monitor for unauthorized use
1. Set up alerts for suspicious activity

**Regular Reviews:**

- Monthly: Review active secrets
- Quarterly: Audit access permissions
- Annually: Complete security assessment

### Emergency Response

**If a Secret is Compromised:**

1. **Immediately Revoke**: Delete the compromised secret
1. **Generate New**: Create new API key/token
1. **Update GitHub**: Set new secret value
1. **Review Logs**: Check for unauthorized usage
1. **Notify Team**: Alert relevant stakeholders
1. **Document**: Record incident for future reference

---

## Cost Considerations

### Free Tier Capabilities

What you get for **$0/month**:

- ✅ Basic video generation
- ✅ Standard voiceover (local TTS)
- ✅ GitHub Actions (per plan limits)
- ✅ 90-day artifact retention
- ✅ Unlimited workflow runs (within minutes)

**Recommendation**: Start here to test the system!

### Paid Integration Costs

#### Monthly Cost Examples

**Scenario 1: Small Team (5 walkthroughs/month)**

```
GitHub Actions:     $0 (within free tier)
OpenAI TTS:         $0.50 (enhanced voice)
Storage:            $0 (GitHub artifacts)
-----------------------------------
Monthly Total:      ~$0.50
```

**Scenario 2: Active Team (20 walkthroughs/month)**

```
GitHub Actions:     $5 (extra minutes)
OpenAI TTS:         $2 (enhanced voice)
ElevenLabs:         $5 (voice cloning)
AWS S3:             $1 (long-term storage)
-----------------------------------
Monthly Total:      ~$13
```

**Scenario 3: Enterprise (100+ walkthroughs/month)**

```
GitHub Actions:     $50 (dedicated runners)
OpenAI TTS:         $10 (high volume)
ElevenLabs Pro:     $99 (unlimited voice)
AWS S3:             $10 (extensive storage)
-----------------------------------
Monthly Total:      ~$169
```

### Cost Optimization Tips

1. **Use Free Tier First**: Test before upgrading
1. **Batch Generation**: Generate multiple videos at once
1. **Optimize Duration**: Shorter videos = lower costs
1. **Cache Voices**: Reuse voice profiles
1. **Clean Up Artifacts**: Delete old videos
1. **Monitor Usage**: Set up billing alerts
1. **Self-hosted Runners**: For high-volume organizations

### Budget Planning

**Questions to Ask:**

- How many walkthroughs per month?
- Do you need premium voices?
- How long should videos be retained?
- Is long-term storage necessary?
- What's your GitHub Actions quota?

**Cost Calculator:**

```
Video Generation: Free
+ Voice Enhancement: $0.10 per video
+ Voice Cloning: $5 one-time + $0.50 per video
+ Storage: $0.023 per GB/month
+ GitHub Actions: $0.008 per minute (if over free tier)
= Total Cost Per Video: Calculate based on options selected
```

---

## Support & Resources

### Documentation

- 📋
  [Walkthrough Request Template](../.github/ISSUE_TEMPLATE/walkthrough-request.yml)
- 📢 [Announcement & Quick Start](./WALKTHROUGH_ANNOUNCEMENT.md)
- 🏗️ [System Architecture](./AI_IMPLEMENTATION_GUIDE.md)
- 🤝 [Contributing Guide](./CONTRIBUTING.md)

### Getting Help

- 💬 **GitHub Discussions**:
  [Ask the community](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->
- 🐛 **Bug Reports**: [File an issue](../.github/ISSUE_TEMPLATE/)
- 📧 **Direct Support**: Contact @4444JPP
- 📖 **Documentation Hub**: [View all docs](./)

### Community

- ⭐ Star the repository to show support
- 🔄 Share your walkthrough examples
- 💡 Submit feature requests
- 🤝 Contribute improvements

---

## Appendix

### Quick Reference Commands

```bash
# List secrets
gh secret list --org ivviiviivvi

# Set secret
gh secret set SECRET_NAME --org ivviiviivvi --body "value"

# Delete secret
gh secret delete SECRET_NAME --org ivviiviivvi

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Verify AWS credentials
aws sts get-caller-identity

# Test ElevenLabs key
curl -H "xi-api-key: $ELEVENLABS_API_KEY" \
  https://api.elevenlabs.io/v1/user
```

### Checklist: First-Time Setup

- [ ] GitHub Actions enabled
- [ ] Workflow permissions configured (read/write)
- [ ] GITHUB_TOKEN verified (automatic)
- [ ] (Optional) OpenAI API key added
- [ ] (Optional) Voice cloning service configured
- [ ] (Optional) Long-term storage configured
- [ ] Test walkthrough generated successfully
- [ ] Team members notified of new capability
- [ ] Documentation bookmarked for reference

---

**Last Updated:** December 21, 2025 **Version:** 1.0.0 **Feedback:**
[Submit suggestions](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->

---

✨ **Happy walkthrough generating!** If you found this guide helpful, please ⭐
star the repository!

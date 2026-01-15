# 🎥 Video Walkthrough Generation Guide

> **Autonomous Video Walkthrough System for the Ivviiviivvi Organization**

## Overview

The Video Walkthrough Generation system is a comprehensive GitHub Actions-based
infrastructure that automatically generates professional 1-minute video
walkthroughs with AI voiceover for all repositories in the Ivviiviivvi
organization. This system provides an automated way to create engaging video
documentation for onboarding, presentations, and project showcases.

### Key Features

✅ **Automatic Application Detection** - Supports React, Vue, Angular, Next.js,
Python (Flask/FastAPI/Django), Java (Spring Boot), and static sites ✅
**AI-Powered Voiceover** - Professional, casual, or technical narration styles ✅
**Automatic Subtitle Generation** - Accessibility-first approach ✅ **Zero Manual
Intervention** - Fully automated workflow execution ✅ **Intelligent PR
Creation** - Automatic pull requests with video artifacts ✅ **Organization-Wide
Deployment** - Single-command rollout to all repositories ✅ **Customizable
Settings** - Duration, style, focus areas, and more ✅ **90-Day Artifact
Retention** - Long-term storage of video walkthroughs

---

## How It Works

### 1. Automatic Triggers

The walkthrough generation workflow is automatically triggered by:

- **Manual Dispatch**: Run on-demand from the GitHub Actions tab
- **Code Changes**: Pushes to `main`, `master`, or `develop` branches
- **File Changes**: Updates to `.js`, `.jsx`, `.ts`, `.tsx`, `.py`, `.vue`,
  `.json`, `.html`, `.css`, `package.json`, `requirements.txt`, `pom.xml`, or
  `build.gradle`

### 2. Detection Phase

The system automatically detects your application type by analyzing:

- **Node.js Projects**: Checks `package.json` for framework signatures (React,
  Vue, Angular, Next.js)
- **Python Projects**: Scans `requirements.txt` or `setup.py` for Flask,
  FastAPI, or Django
- **Java Projects**: Looks for `pom.xml` (Maven) or `build.gradle` (Gradle)
- **Static Sites**: Falls back to static file serving if `index.html` exists

### 3. Environment Setup

The workflow automatically:

1. Installs system dependencies (FFmpeg, Xvfb, Chromium)
1. Sets up the appropriate runtime (Node.js 18, Python 3.10, Java)
1. Installs project dependencies (npm, pip, Maven, Gradle)
1. Configures headless browser environment

### 4. Application Execution

The system:

1. Starts your application in the background
1. Waits for it to become responsive (up to 2 minutes)
1. Verifies the application is accessible on the detected port
1. Captures logs for debugging if needed

### 5. Video Generation

The workflow:

1. Records the application screen at 1920x1080 resolution
1. Captures the specified duration (default: 60 seconds)
1. Generates AI voiceover based on the selected style
1. Creates subtitles automatically
1. Encodes video using H.264 for maximum compatibility

### 6. PR Creation

Finally, the system:

1. Creates a new branch with the naming pattern
   `walkthrough/update-{date}-{run_number}`
1. Commits the video and metadata files
1. Opens a pull request with detailed information
1. Uploads artifacts with 90-day retention

---

## Usage Instructions

### Manual Trigger (Recommended for First Use)

1. Navigate to your repository on GitHub
1. Click the **Actions** tab
1. Select **Generate Video Walkthrough** from the workflows list
1. Click **Run workflow**
1. Configure the optional inputs:
   - **Duration**: Video length in seconds (default: 60)
   - **Voiceover Style**: professional/casual/technical (default: professional)
   - **Focus Areas**: Comma-separated features to highlight (optional)
1. Click **Run workflow** to start

### Using the Reusable Workflow

Create a workflow file in your repository (`.github/workflows/walkthrough.yml`):

```yaml
name: Generate Walkthrough

on:
  workflow_dispatch:
  push:
    branches: [main, develop]

jobs:
  generate:
    uses: Ivviiviivvi/.github/.github/workflows/org-walkthrough-generator.yml@main
    with:
      duration: "60"
      voiceover_style: "professional"
      focus_areas: "authentication, dashboard, reporting"
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Automatic Triggers

Once installed, the workflow automatically runs when:

- You push code changes to `main`, `master`, or `develop` branches
- You modify any supported code files (see trigger conditions in config)

---

## Configuration Guide

### Global Configuration

Edit `.github/walkthrough-config.yml` to customize:

#### Basic Settings

```yaml
defaults:
  duration: 60 # Default video duration (seconds)
  voiceover_style: professional # professional, casual, technical
  framerate: 30 # Video frame rate
  artifact_retention_days: 90 # How long to keep artifacts
```

#### Detection Rules

Add or modify detection rules for your tech stack:

```yaml
detection_rules:
  nodejs:
    - framework: custom-framework
      indicators:
        - file: package.json
          contains: '"custom-framework"'
      default_port: 3000
      start_command: "npm run custom-start"
      install_command: "npm ci"
```

#### Output Settings

Configure output file naming and PR behavior:

```yaml
output:
  directory: "walkthroughs"
  video_filename_pattern: "{app_name}-walkthrough-{date}.mp4"
  metadata_filename_pattern: "{app_name}-metadata.json"
  include_in_pr: true
```

#### Exclusions

Exclude specific repositories:

```yaml
exclusions:
  exact:
    - ".github"
    - "docs"
  patterns:
    - "^test-.*"
    - ".*-archive$"
  topics:
    - "archived"
    - "deprecated"
```

### Per-Repository Configuration

Override global settings by creating `.github/walkthrough-config.yml` in your
repository:

```yaml
defaults:
  duration: 90
  voiceover_style: technical

custom_settings:
  app_port: 4000
  start_command: "npm run custom-start"
  focus_areas: "feature1, feature2, feature3"
```

---

## Supported Tech Stacks

### Node.js / JavaScript

| Framework       | Detected By                       | Default Port | Start Command   |
| --------------- | --------------------------------- | ------------ | --------------- |
| React           | `"react"` in package.json         | 3000         | `npm start`     |
| Vue             | `"vue"` in package.json           | 8080         | `npm run serve` |
| Angular         | `"@angular/core"` in package.json | 4200         | `npm start`     |
| Next.js         | `"next"` in package.json          | 3000         | `npm run dev`   |
| Generic Node.js | `package.json` exists             | 3000         | `npm start`     |

### Python

| Framework      | Detected By                   | Default Port | Start Command                |
| -------------- | ----------------------------- | ------------ | ---------------------------- |
| Flask          | `flask` in requirements.txt   | 5000         | `python app.py`              |
| FastAPI        | `fastapi` in requirements.txt | 8000         | `uvicorn main:app`           |
| Django         | `django` in requirements.txt  | 8000         | `python manage.py runserver` |
| Generic Python | `requirements.txt` exists     | 8000         | `python main.py`             |

### Java

| Framework | Detected By           | Default Port | Start Command         |
| --------- | --------------------- | ------------ | --------------------- |
| Maven     | `pom.xml` exists      | 8080         | `mvn spring-boot:run` |
| Gradle    | `build.gradle` exists | 8080         | `./gradlew bootRun`   |

### Static Sites

| Type        | Detected By         | Default Port | Start Command            |
| ----------- | ------------------- | ------------ | ------------------------ |
| Static HTML | `index.html` exists | 8000         | `python3 -m http.server` |

---

## Output Locations

### Artifacts Storage

All generated videos are stored in two locations:

1. **GitHub Actions Artifacts** (90-day retention)
   - Access via: Actions tab → Workflow run → Artifacts section
   - Format: `walkthrough-{repo-name}-{run-number}.zip`

1. **Repository Files** (Permanent via PR)
   - Location: `walkthroughs/` directory
   - Files:
     - `{app-name}-walkthrough-{date}.mp4` - The video file
     - `{app-name}-metadata.json` - Generation metadata

### Metadata Format

The metadata JSON file includes:

```json
{
  "repository": "Ivviiviivvi/my-app",
  "app_name": "my-app",
  "app_type": "react",
  "generation_date": "2025-12-21T01:54:00Z",
  "duration": 60,
  "voiceover_style": "professional",
  "focus_areas": "feature1, feature2",
  "port": "3000",
  "video_file": "my-app-walkthrough-20251221.mp4"
}
```

---

## Troubleshooting Guide

### Common Issues

#### 1. Application Fails to Start

**Symptoms**: Workflow fails during "Start application" step

**Solutions**:

- Check your application's dependencies are correctly specified
- Verify the start command works locally
- Review application logs in the workflow output
- Ensure environment variables are set if required

#### 2. Video Generation Fails

**Symptoms**: Workflow completes but no video is generated

**Solutions**:

- Verify FFmpeg is installed (handled automatically)
- Check if the application is actually running
- Increase the duration to allow more startup time
- Review the workflow logs for FFmpeg errors

#### 3. Application Not Detected

**Symptoms**: Workflow reports "unknown" application type

**Solutions**:

- Verify your project has the expected indicator files (`package.json`,
  `requirements.txt`, etc.)
- Check the detection rules in `walkthrough-config.yml`
- Add a custom detection rule for your framework
- Manually specify app type in repository config

#### 4. PR Creation Fails

**Symptoms**: Video generates but no PR is created

**Solutions**:

- Verify the workflow has `contents: write` and `pull-requests: write`
  permissions
- Check if there are already too many open PRs
- Ensure the branch doesn't already exist
- Review GitHub Actions permissions in repository settings

#### 5. Timeout Errors

**Symptoms**: Workflow fails with timeout error

**Solutions**:

- Increase `app_startup_timeout` in configuration
- Optimize your application's startup time
- Reduce video duration
- Check for dependency installation issues

### Debug Mode

Enable debug mode for detailed logging:

```yaml
# In .github/walkthrough-config.yml
advanced:
  debug_mode: true
  capture_app_logs: true
```

### Manual Debugging

Run the detection script locally:

```bash
# Test application detection
cd /path/to/your/repo

if [ -f "package.json" ]; then
  echo "Node.js project detected"
  grep -E '"react"|"vue"|"@angular/core"|"next"' package.json
elif [ -f "requirements.txt" ]; then
  echo "Python project detected"
  grep -iE "flask|fastapi|django" requirements.txt
fi
```

---

## Customization Options

### Voiceover Styles

#### Professional (Default)

- **Best for**: Business presentations, client demos, investor pitches
- **Characteristics**: Clear, formal, authoritative
- **Pace**: Moderate
- **Tone**: Business-appropriate

#### Casual

- **Best for**: Internal demos, team showcases, informal documentation
- **Characteristics**: Friendly, conversational, approachable
- **Pace**: Relaxed
- **Tone**: Conversational

#### Technical

- **Best for**: Developer documentation, technical reviews, deep dives
- **Characteristics**: Detailed, precise, comprehensive
- **Pace**: Measured and deliberate
- **Tone**: Technical and informative

### Video Quality Presets

Modify in configuration:

```yaml
quality:
  quality_preset: "high" # Options: low, medium, high, ultra

  # Custom encoding settings
  encoding:
    codec: libx264
    preset: fast # ultrafast, superfast, veryfast, faster, fast, medium, slow
    pixel_format: yuv420p
```

### Custom Focus Areas

Highlight specific features:

```yaml
# Via workflow dispatch
focus_areas: "authentication, dashboard, reporting, analytics"

# In repository config
custom_settings:
  focus_areas: "user management, data visualization, export functionality"
```

---

## Organization-Wide Deployment

### Using the Bootstrap Script

Deploy to all organization repositories:

```bash
# Navigate to scripts directory
cd scripts

# Run the bootstrap script
./bootstrap-walkthrough-org.sh

# With custom options
./bootstrap-walkthrough-org.sh --org Ivviiviivvi --token $GITHUB_TOKEN --dry-run
```

### Bootstrap Script Options

```bash
Options:
  --org NAME          Organization name (default: Ivviiviivvi)
  --token TOKEN       GitHub token for API access
  --exclude REPO      Exclude specific repository (can be used multiple times)
  --dry-run           Preview changes without making them
  --batch-size N      Process N repositories at a time (default: 5)
  --skip-archived     Skip archived repositories
  --help              Show this help message
```

### Manual Deployment

For individual repositories:

1. Copy workflow files to repository:

   ```bash
   cp .github/workflows/generate-walkthrough.yml /path/to/repo/.github/workflows/
   cp .github/walkthrough-config.yml /path/to/repo/.github/
   ```

1. Commit and push:

   ```bash
   git add .github/workflows/generate-walkthrough.yml .github/walkthrough-config.yml
   git commit -m "feat: add video walkthrough generation"
   git push
   ```

1. Create a PR manually or use GitHub CLI:

   ```bash
   gh pr create --title "Add video walkthrough generation" --body "Enables automatic video walkthrough generation for this repository"
   ```

---

## Advanced Topics

### Batch Processing

Enable batch mode to generate walkthroughs for multiple repositories:

```yaml
automation:
  batch_mode:
    enabled: true
    max_concurrent_jobs: 3
    retry_on_failure: true
    max_retries: 2
```

### Rate Limiting

Prevent excessive workflow runs:

```yaml
automation:
  rate_limiting:
    enabled: true
    max_runs_per_day: 10
    cooldown_minutes: 30
```

### Custom Notification Channels

Configure notifications:

```yaml
notifications:
  enabled: true
  channels:
    github_issues:
      enabled: true
      on_failure: true
      on_success: false
    pr_comments:
      enabled: true
      include_preview: true
```

### Monitoring & Analytics

Track generation metrics:

```yaml
monitoring:
  enabled: true
  metrics:
    - generation_time
    - video_size
    - app_startup_time
    - success_rate
  store_metrics: true
  metrics_file: "reports/walkthrough-metrics.json"
```

---

## Best Practices

### 1. Preparation

- **Test Locally First**: Ensure your application runs correctly before enabling
  automation
- **Optimize Startup**: Reduce application startup time for faster video
  generation
- **Set Environment Variables**: Use GitHub Secrets for sensitive configuration

### 2. Configuration

- **Use Descriptive Focus Areas**: Help the AI understand what to highlight
- **Choose Appropriate Duration**: 60-90 seconds is ideal for most applications
- **Select the Right Style**: Match voiceover style to your audience

### 3. Maintenance

- **Review Generated Videos**: Check quality periodically
- **Update Configuration**: Refine settings based on results
- **Monitor Metrics**: Track success rates and generation times
- **Clean Up Old Artifacts**: Remove outdated videos to save space

### 4. Organization-Wide

- **Establish Standards**: Define organization-wide defaults
- **Document Custom Settings**: Explain repository-specific configurations
- **Share Best Practices**: Create examples and templates
- **Regular Reviews**: Audit generated videos quarterly

---

## FAQ

### Q: How much does this cost?

**A**: The workflow uses GitHub Actions minutes. For public repositories, it's
free. For private repositories, it counts against your GitHub Actions quota.
Typical runs consume 10-15 minutes.

### Q: Can I use custom narration scripts?

**A**: Yes! Create a `walkthrough-script.txt` file in your repository root with
your custom narration.

### Q: What if my application requires authentication?

**A**: Set up test credentials using GitHub Secrets and configure your
application to use them during CI runs.

### Q: Can I generate videos for specific features only?

**A**: Yes, use the `focus_areas` parameter to specify which features to
highlight.

### Q: How do I exclude certain repositories?

**A**: Add them to the `exclusions` list in `.github/walkthrough-config.yml`.

### Q: Can I customize the video resolution?

**A**: Yes, modify the `resolution` settings in the configuration file.

### Q: What happens if video generation fails?

**A**: The workflow will log the error and continue. Check the workflow logs for
details. Failed runs don't create PRs.

### Q: Can I run this on schedule?

**A**: Yes, add a `schedule` trigger to the workflow:

```yaml
on:
  schedule:
    - cron: "0 0 * * 0" # Weekly on Sunday at midnight
```

### Q: How do I update the walkthrough for an existing repository?

**A**: Simply trigger the workflow manually or push a code change. The new video
will be added via a new PR.

### Q: Can I preview the video before creating a PR?

**A**: Yes, download the artifact from the workflow run before the PR is
created.

---

## Support & Resources

### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)<!-- link:docs.github_actions -->
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Workflow Configuration Reference](walkthrough-config.yml)

### Getting Help

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Organization**: Contact @4444JPP for organization-level support

### Contributing

Contributions are welcome! See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for
guidelines.

---

## Changelog

### Version 1.0.0 (2025-12-21)

- ✨ Initial release
- ✅ Support for Node.js, Python, Java, and static sites
- ✅ Automatic application detection
- ✅ AI voiceover generation
- ✅ Automatic PR creation
- ✅ Organization-wide deployment script
- ✅ Comprehensive configuration system
- ✅ 90-day artifact retention

---

**Built with ❤️ for the Ivviiviivvi Organization**

_Automated video walkthrough generation for modern software projects_

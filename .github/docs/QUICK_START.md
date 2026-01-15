# Quick-Start Guide: Application Walkthrough Generator

> **Generate professional video walkthroughs of your application in minutes**

Welcome! This guide will help you create your first automated application
walkthrough video in just 5 minutes.

## Getting Started in 5 Minutes

### Step 1: Navigate to Your Repository

1. Go to your repository on GitHub (e.g.,
   `github.com/ivviiviivvi/your-repo-name`)
1. Make sure your application has a working local development setup

### Step 2: Go to the Actions Tab

1. Click the **Actions** tab at the top of your repository
1. Look for "Generate Application Walkthrough" in the workflow list
1. Click on the workflow name

### Step 3: Select the Workflow

1. On the right side, click the **"Run workflow"** dropdown button
1. Select your branch (usually `main` or `develop`)

### Step 4: Configure Inputs

Fill in the workflow parameters:

- **Duration** (30-120 seconds)
  - Recommended: 60 seconds for general demos
  - Short demos: 30-45 seconds
  - Detailed walkthroughs: 90-120 seconds

- **Voiceover Style**
  - `professional` - Business presentations and client demos
  - `casual` - Team updates and informal explanations
  - `technical` - Deep-dives for developers

- **Focus Areas** (comma-separated)
  - Examples: `user authentication, dashboard, data visualization`
  - Be specific: `login form, create post button, user profile page`

- **Start Command** (optional)
  - React: `npm start`
  - Flask: `python app.py`
  - Vue: `npm run serve`
  - Leave blank to auto-detect

- **Port** (optional)
  - React default: `3000`
  - Flask default: `5000`
  - Vue default: `8080`
  - Leave blank to auto-detect

### Step 5: Run Workflow and Wait

1. Click the green **"Run workflow"** button
1. The page will refresh - click on your workflow run to see progress
1. Wait for completion (typically 10-15 minutes)

## What to Expect

### Execution Time

- **Small apps**: 8-12 minutes
- **Medium apps** (React/Vue/Angular): 10-15 minutes
- **Complex apps** (Full-stack): 15-20 minutes

### Generated Output

Your walkthrough will be available as:

- **Workflow artifact**: `walkthrough-video.mp4`
- **Location**: Actions tab → Your workflow run → Artifacts section
- **Duration**: Matches your configured duration (±5 seconds)
- **Format**: MP4, 1920x1080, 30fps

### Where to Find Generated Video

1. Go to the completed workflow run
1. Scroll down to the **Artifacts** section
1. Click **"walkthrough-video"** to download (ZIP file)
1. Extract the ZIP to get `walkthrough-video.mp4`

### How to Download and Share

- **Download**: Click artifact name → Save ZIP → Extract
- **Share**: Upload to YouTube, Vimeo, or your preferred platform
- **Embed**: Use in presentations, documentation, or README files
- **Storage**: Videos expire after 90 days (GitHub artifact retention)

## Customization Examples

### Example 1: Professional 60-Second Demo for Clients

**Use case**: Product demonstration for stakeholders

```yaml
Duration: 60 seconds
Voiceover Style: professional
Focus Areas: dashboard overview, key features, value proposition
```

**What you'll get**: Polished, business-focused walkthrough highlighting core
functionality and benefits.

---

### Example 2: Casual 90-Second Explainer for Team

**Use case**: Onboarding new team members

```yaml
Duration: 90 seconds
Voiceover Style: casual
Focus Areas: project structure, main components, development workflow
```

**What you'll get**: Friendly, approachable explanation of how the application
works and where things are located.

---

### Example 3: Technical 45-Second Deep-Dive for Developers

**Use case**: Code review or technical documentation

```yaml
Duration: 45 seconds
Voiceover Style: technical
Focus Areas: API endpoints, state management, database operations
```

**What you'll get**: Technical walkthrough focusing on implementation details,
architecture, and code structure.

---

## Common Questions

### Q: My app won't start

**A**: Troubleshooting steps:

1. Check your start command is correct
1. Verify dependencies are installed (`package.json`, `requirements.txt`)
1. Ensure environment variables are documented
1. Check if your app requires a database or external service
1. Review workflow logs for error messages

**Pro tip**: Test your start command locally first:

```bash
# React
npm install && npm start

# Flask
pip install -r requirements.txt && python app.py

# Vue
npm install && npm run serve
```

### Q: Can I preview before sharing?

**A**: Yes! Follow these steps:

1. Download the artifact from the completed workflow
1. Extract the ZIP file
1. Open `walkthrough-video.mp4` in any video player
1. Review the video before sharing with others

**Note**: You can re-run the workflow with different settings if needed.

### Q: How do I customize the voiceover?

**A**: Choose from three voice styles:

| Style          | Best For                    | Tone              | Speed           |
| -------------- | --------------------------- | ----------------- | --------------- |
| `professional` | Client demos, presentations | Formal, clear     | Moderate        |
| `casual`       | Team updates, tutorials     | Friendly, relaxed | Moderate        |
| `technical`    | Developer docs, reviews     | Precise, detailed | Slightly faster |

To change styles, simply select a different option when running the workflow.

### Q: What if my app uses a custom port?

**A**: Specify your port in the workflow inputs:

**Example configurations:**

- Custom Node.js app on port 8080: Enter `8080`
- Flask with custom config on 5001: Enter `5001`
- Multi-service app: Run the workflow separately for each service

**Advanced**: For apps with multiple services, focus on one service per
walkthrough or configure a proxy.

### Q: How long are videos stored?

**A**: Workflow artifacts are retained for **90 days** by default (GitHub's
standard retention period).

**Best practice**: Download and archive important walkthroughs in your own
storage or video platform.

### Q: Can I customize the video resolution?

**A**: Currently, videos are generated at **1920x1080 (Full HD)**. This works
well for:

- YouTube uploads
- Embedded documentation
- Presentation slides
- README files

### Q: What if the video doesn't capture what I need?

**A**: You can:

1. Re-run with more specific focus areas
1. Adjust the duration (longer = more coverage)
1. Break into multiple focused walkthroughs
1. Review logs to see what was captured

## Video Examples

### Sample Generated Walkthroughs

**React Todo App** (60 seconds, professional)

- Repository: `ivviiviivvi/example-react-todo`
- Focus: Task creation, editing, filtering
- [View artifact](#) | [Download](#)

**Python Flask API** (45 seconds, technical)

- Repository: `ivviiviivvi/example-flask-api`
- Focus: REST endpoints, authentication, database
- [View artifact](#) | [Download](#)

**Vue.js Dashboard** (90 seconds, casual)

- Repository: `ivviiviivvi/example-vue-dashboard`
- Focus: Charts, data visualization, user flow
- [View artifact](#) | [Download](#)

**Full-Stack E-commerce** (120 seconds, professional)

- Repository: `ivviiviivvi/example-fullstack-shop`
- Focus: Product browsing, cart, checkout flow
- [View artifact](#) | [Download](#)

_Note: Example videos are for demonstration purposes and may not always be
available._

## Getting Help

### FAQ and Documentation

- **Configuration Examples**: [Example Configs](../examples/)
- **Scheduled Automation**:
  [Automated Walkthrough Setup](../workflows/scheduled-walkthrough-generator.yml)
- **Organization Repository**:
  [ivviiviivvi/.github](https://github.com/ivviiviivvi/.github)<!-- link:github.dotgithub -->

### Support Channels

**GitHub Issues** - Report bugs or technical problems

- Go to: `github.com/ivviiviivvi/.github/issues`
- Use template: "Walkthrough Generator Issue"
- Include: Workflow run link, error logs, expected behavior

**Discussions** - Ask questions and share ideas

- Go to: `github.com/ivviiviivvi/.github/discussions`
- Category: "Q&A" for questions
- Category: "Show and Tell" for sharing your walkthroughs

**Direct Contact** - Organization maintainer

- GitHub:
  [@4444JPP](https://github.com/4444JPP)<!-- link:examples.sample_profile -->
- For: Urgent issues, security concerns, feature requests

### Response Times

- **Critical bugs**: 24 hours
- **General questions**: 2-3 business days
- **Feature requests**: Reviewed weekly

## Next Steps

✅ **You've completed the quick-start!**

**Now you can:**

1. 🎥 Generate your first walkthrough
1. 📝 Review example configurations for your app type
1. ⚙️ Set up scheduled automated walkthroughs
1. 🤝 Share your walkthroughs with the community

**Advanced topics:**

- [Example Configurations](../examples/README.md) - Templates for different app
  types
- [Scheduled Automation](../workflows/scheduled-walkthrough-generator.yml) -
  Automated recurring walkthroughs
- [Contributing](../../docs/CONTRIBUTING.md) - Help improve the system

---

**Questions?**
[Open a discussion](https://github.com/ivviiviivvi/.github/discussions)<!-- link:github.discussions -->.

**Found a bug?**
[Report it here](https://github.com/ivviiviivvi/.github/issues/new).

---

_Last updated: 2025-12-21 | Version: 1.0.0 | Maintained by @4444JPP_

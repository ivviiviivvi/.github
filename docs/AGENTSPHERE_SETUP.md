# AgentSphere Setup Guide

> **Automatic live demo deployment for your applications**

## Table of Contents

- [What is AgentSphere?](#what-is-agentsphere)
- [Why Use AgentSphere?](#why-use-agentsphere)
- [How Automatic Deployment Works](#how-automatic-deployment-works)
- [Accessing Live Demo Badges](#accessing-live-demo-badges)
- [Custom Configuration](#custom-configuration)
- [Sharing Live Demos](#sharing-live-demos)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)
- [Cost Considerations](#cost-considerations)
- [FAQ](#faq)

---

## What is AgentSphere?

**AgentSphere** is a cloud-based sandbox environment that automatically deploys
and hosts live demos of your applications. When you push code to your
repository, AgentSphere:

1. 🔍 Detects your application type (Node.js, Python, Vue, React, Java, Go, Ruby,
   .NET)
1. 🚀 Deploys your app to a secure sandbox environment
1. 🔗 Generates a unique demo URL
1. 📝 Updates your README with a "Live Demo" badge
1. 🔄 Keeps the demo synchronized with your latest code

---

## Why Use AgentSphere?

### Benefits

✅ **Instant Demos** - Share working demos instantly with stakeholders

✅ **Zero Configuration** - Works out of the box with auto-detection

✅ **Always Up-to-Date** - Automatically redeploys on code changes

✅ **Secure Sandboxing** - Isolated environments for each demo

✅ **Multiple Tech Stacks** - Supports 8+ languages and frameworks

✅ **Professional Badges** - Automatic README badge generation

### Use Cases

- **Showcase Projects** - Demonstrate functionality to potential users
- **Code Reviews** - Let reviewers test changes in real-time
- **Portfolio** - Live demos for job applications and interviews
- **Client Presentations** - Share working prototypes instantly
- **Bug Reports** - Provide live reproduction environments

---

## How Automatic Deployment Works

### Workflow Trigger Sequence

```
1. Developer pushes code to main branch
   ↓
2. AgentSphere Deployment workflow triggers
   ↓
3. Application type is auto-detected
   ↓
4. App is deployed to AgentSphere sandbox
   ↓
5. Live demo URL is generated
   ↓
6. README badge is created
   ↓
7. Pull request is opened with badge
```

### Supported Application Types

| Type        | Detection                     | Startup Commands                                |
| ----------- | ----------------------------- | ----------------------------------------------- |
| **Node.js** | `package.json`                | `npm start`, `npm run dev`, `npm run serve`     |
| **Python**  | `requirements.txt`, `Pipfile` | `python app.py`, `flask run`, `uvicorn app:app` |
| **Vue.js**  | `vue.config.js`               | `npm run serve`, `npm run dev`                  |
| **React**   | `src/App.jsx`, `src/App.tsx`  | `npm start`, `npm run dev`                      |
| **Java**    | `pom.xml`, `build.gradle`     | `java -jar`, `gradle bootRun`                   |
| **Go**      | `go.mod`, `main.go`           | `go run main.go`, `./main`                      |
| **Ruby**    | `Gemfile`                     | `bundle exec rails server`, `puma`              |
| **.NET**    | `*.csproj`, `*.sln`           | `dotnet run`                                    |

### Detection Logic

The workflow checks for specific files in your repository:

```yaml
Node.js: package.json exists
Python: requirements.txt OR Pipfile OR pyproject.toml exists
Vue.js: vue.config.js exists OR "vue" in package.json
React: src/App.jsx OR src/App.tsx exists
Java: pom.xml OR build.gradle exists
Go: go.mod OR main.go exists
Ruby: Gemfile exists
.NET: *.csproj OR *.sln exists
```

---

## Accessing Live Demo Badges

### Automatic Badge Insertion

When deployment succeeds, a pull request is automatically created with:

```markdown
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen?style=for-the-badge)](https://demo-yourrepo.agentsphere.dev)
```

The badge will be inserted based on your configuration:

- **`top`**: Very first line of README
- **`after-title`**: After the first heading (default)
- **`before-installation`**: Before installation section

### Manual Badge Creation

If you want to add the badge manually:

```markdown
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen?style=for-the-badge)](YOUR_DEMO_URL)
```

Customize the badge style:

- `flat` - Flat badge
- `flat-square` - Flat square badge
- `for-the-badge` - Large, bold badge (recommended)
- `plastic` - Plastic-style badge
- `social` - Social media style badge

---

## Custom Configuration

### Repository-Specific Overrides

Create `.agentsphere.yml` in your repository root to override defaults:

```yaml
# .agentsphere.yml
enabled: true

startup_command: "npm run custom-start"
build_command: "npm run custom-build"
port: 3000

environment:
  NODE_ENV: "production"
  API_URL: "https://api.example.com"
  CUSTOM_VAR: "custom-value"

badge:
  style: "flat-square"
  color: "blue"
  position: "top"

access:
  visibility: "private"
  require_auth: true
```

### Custom Startup Commands

If auto-detection fails, specify a custom command:

```yaml
# Via GitHub Actions manual dispatch
workflow_dispatch:
  inputs:
    custom_command: "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
```

Or in `.agentsphere.yml`:

```yaml
startup_command: "bundle exec rails server -b 0.0.0.0"
```

---

## Sharing Live Demos

### Public Demos

By default, demos are publicly accessible:

```
Demo URL: https://demo-owner-repo.agentsphere.dev
```

Share this URL with team members, stakeholders, clients, job recruiters, and
open source contributors.

### Private Demos

For private demos, configure access control:

```yaml
access:
  visibility: "private"
  require_auth: true
```

---

## Troubleshooting

### Demo Not Starting

**Problem**: Demo URL returns 502 or 503 error

**Solutions**:

1. Check workflow logs for deployment errors
1. Verify startup command is correct
1. Ensure all dependencies are installed
1. Check port configuration matches application

### Wrong Application Type Detected

**Problem**: Workflow detects wrong tech stack

**Solutions**:

1. Create `.agentsphere.yml` with explicit `app_type`
1. Use manual workflow dispatch with custom command
1. Add detection files (e.g., `package.json` for Node.js)

### Badge Not Appearing

**Problem**: Pull request created but badge not in README

**Solutions**:

1. Check PR files for badge markdown
1. Merge the PR to apply changes
1. Verify README.md exists in repository
1. Check badge position configuration

---

## Performance Optimization

### Build Time Optimization

```yaml
# Cache dependencies
build_command: 'npm ci --prefer-offline'

# Skip dev dependencies
build_command: 'npm install --production'
```

### Startup Time Optimization

```yaml
# Use production mode
environment:
  NODE_ENV: "production"
  RAILS_ENV: "production"
```

---

## Cost Considerations

### Free Tier

AgentSphere offers a generous free tier:

- ✅ Unlimited public demos
- ✅ Up to 5 concurrent demos per organization
- ✅ 1GB storage per demo
- ✅ 100GB bandwidth per month

---

## FAQ

### Q: How long do demos stay active?

**A:** Demos remain active for 7 days of inactivity by default.

### Q: Can I use custom domains?

**A:** Yes, configure custom domains in `.agentsphere.yml`.

### Q: Are demos sandboxed securely?

**A:** Yes, each demo runs in an isolated container with network restrictions.

### Q: How do I disable AgentSphere for a repository?

**A:** Set `enabled: false` in `.agentsphere.yml` or remove the workflow file.

---

## Support

Need help? Contact:

- 💬 **GitHub**:
  [@4444JPP](https://github.com/4444JPP)<!-- link:examples.sample_profile -->
- 📚 **Documentation**: [GitHub Pages Setup](./GITHUB_PAGES_SETUP.md)
- 🐛 **Issues**:
  [Report a bug](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

---

**Last Updated**: 2025-12-21 **Version**: 1.0.0

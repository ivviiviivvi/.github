# AgentSphere & GitHub Pages Integration

> **Comprehensive system for autonomous walkthrough generation, live demos, and
> documentation gallery**

## 🎯 Overview

This implementation provides a complete solution for automatically deploying
live demos and showcasing application walkthroughs across all Ivviiviivvi
organization repositories.

## 📦 What's Included

### Part 1: AgentSphere Live Demo Integration

**Automatic deployment of applications to cloud sandbox environments**

- ✅ Auto-detection of 8+ tech stacks (Node.js, Python, Vue, React, Java, Go,
  Ruby, .NET)
- ✅ Automatic README badge generation
- ✅ Pull request creation with demo links
- ✅ Configurable startup commands and environment variables
- ✅ Health checks and auto-restart policies

**Files:**

- `.github/agentsphere-config.yml` - Centralized configuration
- `.github/workflows/agentsphere-deployment.yml` - Deployment workflow
- `docs/AGENTSPHERE_SETUP.md` - Setup documentation

### Part 2: GitHub Pages Static Site

**Beautiful, responsive walkthrough gallery with video playback**

- ✅ Responsive grid layout with dark mode
- ✅ Client-side search functionality
- ✅ Embedded video players with lazy loading
- ✅ Automatic site rebuilds every 6 hours
- ✅ 90-day retention for old builds

**Files:**

- `_config.yml` - Jekyll site configuration
- `docs/_layouts/default.html` - Main layout template
- `docs/_includes/walkthrough_gallery.html` - Gallery component
- `.github/workflows/build-pages-site.yml` - Build & deploy workflow
- `Gemfile` - Ruby dependencies

### Part 3: Index Generation & Metadata

**Automated collection of walkthrough data from all organization repositories**

- ✅ Scheduled GitHub API queries (every 6 hours)
- ✅ Automatic metadata aggregation
- ✅ Dynamic index page generation
- ✅ Support for custom metadata

**Files:**

- `.github/workflows/generate-pages-index.yml` - Index generation workflow
- `docs/_data/walkthroughs.yml` - Walkthrough metadata
- `docs/_data/repositories.yml` - Repository metadata
- `docs/_data/live_demos.yml` - Live demo metadata
- `docs/index.md` - Gallery homepage
- `docs/GITHUB_PAGES_SETUP.md` - Pages documentation

## 🚀 Quick Start

### For Repository Owners

**No configuration needed!** The system automatically:

1. Detects your application type when you push to main
1. Deploys to AgentSphere (if enabled)
1. Creates a PR with "Live Demo" badge
1. Adds your walkthrough to the gallery

### For Organization Admins

**Enable GitHub Pages:**

1. Go to repository Settings → Pages
1. Source: Deploy from a branch
1. Branch: `gh-pages` / `root`
1. Save

**Configure AgentSphere (optional):**

Edit `.github/agentsphere-config.yml` to customize:

- Enable/disable auto-deployment
- Modify tech stack detection
- Customize badge appearance
- Set access controls

## 📊 Workflow Sequence

```
Developer Push → Main Branch
         ↓
AgentSphere Deployment Workflow
         ↓
    App Type Detected
         ↓
  Deployed to Sandbox
         ↓
   Demo URL Generated
         ↓
  README Badge Added (PR)
         ↓
Generate Pages Index (every 6h)
         ↓
  Metadata Aggregated
         ↓
Build Pages Site
         ↓
  Jekyll Site Built
         ↓
 Deployed to GitHub Pages
         ↓
🎉 Live Demo + Video Gallery Updated!
```

## 🔧 Configuration

### AgentSphere Config

Modify `.github/agentsphere-config.yml`:

```yaml
enabled: true
global:
  startup_timeout: 60
  badge:
    style: "for-the-badge"
    color: "brightgreen"
    position: "after-title"
```

### Jekyll Config

Modify `_config.yml`:

```yaml
title: "Your Organization Walkthrough Gallery"
description: "Browse all walkthroughs"
gallery:
  videos_per_page: 12
  enable_search: true
```

### Repository Override

Create `.agentsphere.yml` in any repository:

```yaml
enabled: true
startup_command: "npm run custom-start"
port: 3000
environment:
  NODE_ENV: "production"
```

## 📖 Documentation

- **[AgentSphere Setup Guide](../AGENTSPHERE_SETUP.md)** - Complete deployment
  guide
- **[GitHub Pages Setup Guide](../GITHUB_PAGES_SETUP.md)** - Gallery
  customization

## 🧪 Testing

All files have been validated:

- ✅ YAML syntax validation
- ✅ HTML accessibility attributes
- ✅ No hardcoded secrets
- ✅ Pinned action versions
- ✅ Complete file structure

Run validation:

```bash
# Validate YAML files
python3 -c "import yaml; yaml.safe_load(open('.github/agentsphere-config.yml'))"
python3 -c "import yaml; yaml.safe_load(open('_config.yml'))"

# Check workflows
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/agentsphere-deployment.yml'))"
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/build-pages-site.yml'))"
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/generate-pages-index.yml'))"
```

## 📁 File Structure

```
.
├── .github/
│   ├── agentsphere-config.yml          # AgentSphere configuration
│   └── workflows/
│       ├── agentsphere-deployment.yml  # Auto-deployment workflow
│       ├── build-pages-site.yml        # Jekyll build & deploy
│       └── generate-pages-index.yml    # Index generation
├── docs/
│   ├── _layouts/
│   │   └── default.html                # Main page layout
│   ├── _includes/
│   │   └── walkthrough_gallery.html    # Gallery component
│   ├── _data/
│   │   ├── walkthroughs.yml            # Walkthrough metadata
│   │   ├── repositories.yml            # Repository metadata
│   │   └── live_demos.yml              # Live demo metadata
│   ├── index.md                        # Gallery homepage
│   ├── AGENTSPHERE_SETUP.md            # AgentSphere documentation
│   └── GITHUB_PAGES_SETUP.md           # GitHub Pages documentation
├── _config.yml                         # Jekyll configuration
├── Gemfile                             # Ruby dependencies
└── .gitignore                          # Updated with Jekyll excludes
```

## 🎨 Features

### AgentSphere Deployment

- 🔍 **Auto-Detection** - Supports 8+ tech stacks
- 🚀 **Zero Config** - Works out of the box
- 🔗 **Live Demos** - Instant sandbox environments
- 📝 **Auto-Badges** - Professional README badges
- 🔄 **Auto-Update** - Syncs with latest code

### GitHub Pages Gallery

- 📹 **Video Gallery** - Responsive grid layout
- 🔍 **Search** - Real-time client-side filtering
- 🎨 **Dark Mode** - Auto-detect & toggle
- 📱 **Mobile-Friendly** - Responsive design
- ⚡ **Fast Loading** - Lazy-loaded videos
- 🔗 **Live Demos** - Integrated demo links

### Automation

- ⏰ **Scheduled Updates** - Every 6 hours
- 🔄 **Auto-Commits** - No manual updates
- 📊 **Statistics** - Organization metrics
- 🧹 **Auto-Cleanup** - 90-day retention
- 🔔 **Notifications** - PR comments

## 🔒 Security

- ✅ No hardcoded secrets
- ✅ Pinned action versions (v4, v5)
- ✅ GitHub token authentication
- ✅ Sandboxed environments
- ✅ Network restrictions
- ✅ Rate limiting

## 🛠️ Troubleshooting

### AgentSphere Not Deploying

1. Check if `enabled: true` in config
1. Verify application type detection
1. Review workflow logs
1. Try manual dispatch with custom command

### Gallery Not Building

1. Enable GitHub Pages in settings
1. Check workflow runs in Actions tab
1. Verify Jekyll syntax in `_config.yml`
1. Review build logs

### Videos Not Showing

1. Wait for next scheduled index (up to 6 hours)
1. Manually trigger `generate-pages-index` workflow
1. Check video file locations
1. Verify file format (MP4, WebM, MOV)

## 🤝 Contributing

This system is ready for immediate deployment. To customize:

1. Fork the `.github` repository
1. Modify configuration files
1. Test locally with Jekyll
1. Submit PR with changes

## 📞 Support

- 💬 **GitHub**:
  [@4444JPP](https://github.com/4444JPP)<!-- link:examples.sample_profile -->
- 📚 **Documentation**: See `docs/` directory
- 🐛 **Issues**:
  [Report a bug](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

## 📜 License

This implementation is part of the Ivviiviivvi organization `.github`
repository.

---

**Status**: ✅ Ready for Deployment **Version**: 1.0.0 **Last Updated**:
2025-12-21 **Organization**: Ivviiviivvi **Maintainer**: @4444JPP

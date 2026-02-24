# GitHub Pages Setup Guide

> **Walkthrough gallery and documentation site for Ivviiviivvi organization**

## Table of Contents

- [What is GitHub Pages?](#what-is-github-pages)
- [How Automatic Site Building Works](#how-automatic-site-building-works)
- [Accessing the Walkthrough Gallery](#accessing-the-walkthrough-gallery)
- [Searching and Filtering](#searching-and-filtering)
- [Embedding Gallery in Organization Website](#embedding-gallery-in-organization-website)
- [Custom Domain Setup](#custom-domain-setup)
- [Site Analytics and Tracking](#site-analytics-and-tracking)
- [Customizing Site Appearance](#customizing-site-appearance)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)

______________________________________________________________________

## What is GitHub Pages?

**GitHub Pages** is a static site hosting service that automatically publishes a
website from this repository. For the Ivviiviivvi organization, it serves as:

📹 **Walkthrough Gallery** - Video gallery of all application walkthroughs 🚀
**Live Demo Directory** - Centralized listing of all live demos 📊 **Repository
Statistics** - Organization-wide metrics and insights 🔍 **Searchable Index** -
Find walkthroughs across all repositories 🎨 **Professional Showcase** -
Beautiful, responsive design with dark mode

______________________________________________________________________

## How Automatic Site Building Works

### Build Trigger Sequence

```
1. Walkthrough video generated in any repository
   ↓
2. Metadata uploaded to organization repository
   ↓
3. Generate Pages Index workflow runs (every 6 hours)
   ↓
4. Collects data from all organization repositories
   ↓
5. Build Pages Site workflow triggers
   ↓
6. Jekyll builds static site
   ↓
7. Site deployed to GitHub Pages
   ↓
8. Gallery updated with new walkthroughs
```

### Data Collection

The system automatically collects:

- **Walkthrough Videos** - From `/walkthroughs`, `/docs/walkthroughs`,
  `/.github/walkthroughs`
- **Live Demo URLs** - From README badges and AgentSphere deployments
- **Repository Metadata** - Names, descriptions, languages, stars
- **Video Metadata** - Titles, descriptions, tags, upload dates

### Update Frequency

- **Scheduled Updates**: Every 6 hours
- **On-Demand Updates**: Manual workflow dispatch
- **Event-Driven Updates**: When new repositories are created

______________________________________________________________________

## Accessing the Walkthrough Gallery

### Gallery URL

The gallery is available at:

```
https://{{ORG_NAME}}.github.io/.github/
```

### Gallery Features

✅ **Responsive Design** - Works on desktop, tablet, and mobile ✅ **Dark Mode** -
Automatic theme switching ✅ **Video Playback** - Embedded HTML5 video players ✅
**Lazy Loading** - Fast page load with progressive video loading ✅ **Search** -
Real-time client-side search ✅ **Metadata Display** - Repository name,
description, date, tags ✅ **Live Demo Links** - Direct links to AgentSphere
demos

______________________________________________________________________

## Searching and Filtering

### Search Functionality

The gallery includes powerful search capabilities:

**Search Fields:**

- Repository name
- Video title
- Description text
- Tags and categories

**How to Search:**

1. Type in the search bar at the top of the gallery
1. Results update in real-time as you type
1. Search is case-insensitive
1. Minimum 2 characters required

**Example Searches:**

```
"node" - Find all Node.js projects
"authentication" - Find auth-related walkthroughs
"react" - Find React applications
"api" - Find API projects
```

### Filtering (Coming Soon)

Future enhancements will include:

- Filter by programming language
- Filter by creation date
- Filter by repository stars
- Sort by name, date, or popularity

______________________________________________________________________

## Embedding Gallery in Organization Website

### Full Gallery Embed

Embed the entire gallery in your website:

```html
<iframe
  src="https://{{ORG_NAME}}.github.io/.github/"
  width="100%"
  height="800px"
  frameborder="0"
  title="Walkthrough Gallery"
></iframe>
```

### Single Video Embed

Embed a specific walkthrough video:

```html
<video controls width="640" height="360">
  <source src="VIDEO_DOWNLOAD_URL" type="video/mp4" />
  Your browser does not support the video tag.
</video>
```

### Responsive Embed

For responsive embedding that adapts to screen size:

```html
<div
  style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;"
>
  <iframe
    src="https://{{ORG_NAME}}.github.io/.github/"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
  ></iframe>
</div>
```

______________________________________________________________________

## Custom Domain Setup

### Configuring a Custom Domain

To use a custom domain (e.g., `walkthroughs.{{ORG_NAME}}.dev`):

**Step 1: Add CNAME Record**

Add a CNAME record in your DNS settings:

```
Type: CNAME
Name: walkthroughs
Value: {{ORG_NAME}}.github.io
TTL: 3600
```

**Step 2: Configure GitHub Pages**

1. Go to repository Settings → Pages
1. Enter custom domain: `walkthroughs.{{ORG_NAME}}.dev`
1. Enable "Enforce HTTPS"
1. Save settings

**Step 3: Update Jekyll Configuration**

Update `_config.yml`:

```yaml
url: "https://walkthroughs.{{ORG_NAME}}.dev"
baseurl: ""
```

**Step 4: Commit and Deploy**

Changes will take effect on next deployment (within 6 hours or trigger
manually).

______________________________________________________________________

## Site Analytics and Tracking

### Google Analytics Setup

Enable analytics in `_config.yml`:

```yaml
analytics:
  enabled: true
  provider: "google"
  tracking_id: "G-XXXXXXXXXX"
```

### Privacy-Friendly Analytics

For privacy-focused analytics, use alternatives like:

- **Plausible** - GDPR-compliant, lightweight
- **Fathom** - Privacy-first analytics
- **Simple Analytics** - No cookies, GDPR-friendly

Configuration example:

```yaml
analytics:
  enabled: true
  provider: "plausible"
  domain: "walkthroughs.{{ORG_NAME}}.dev"
```

______________________________________________________________________

## Customizing Site Appearance

### Theme Colors

Customize colors in `_config.yml`:

```yaml
theme_customization:
  primary_color: "#2ea44f"
  secondary_color: "#0969da"
  background_color: "#ffffff"
  text_color: "#24292f"
  header_gradient_start: "#2ea44f"
  header_gradient_end: "#0969da"
```

### Dark Mode Colors

Customize dark mode theme:

```yaml
theme_customization:
  dark_mode:
    enabled: true
    auto_detect: true
    background_color: "#0d1117"
    text_color: "#c9d1d9"
    primary_color: "#58a6ff"
```

### Logo and Branding

Add organization logo:

```yaml
organization:
  name: "Ivviiviivvi"
  logo_url: "/assets/images/logo.png"
  tagline: "Building innovative solutions"
```

### Custom CSS

Add custom styles by creating `assets/css/custom.css`:

```css
/* Custom styles */
.video-card {
  border-radius: 16px;
}

.video-card:hover {
  transform: translateY(-8px);
}
```

Include in `_config.yml`:

```yaml
custom_css:
  - "/assets/css/custom.css"
```

______________________________________________________________________

## FAQ

### Q: How often is the gallery updated?

**A:** The gallery updates automatically every 6 hours via scheduled workflow.
You can also trigger manual updates.

### Q: Can I add walkthroughs manually?

**A:** Yes, add video files to `/walkthroughs`, `/docs/walkthroughs`, or
`/.github/walkthroughs` in your repository. The next scheduled run will pick
them up.

### Q: What video formats are supported?

**A:** MP4, WebM, and MOV formats are supported. MP4 is recommended for best
compatibility.

### Q: How do I add metadata to walkthroughs?

**A:** Create a JSON file with the same name as your video:

```json
{
  "title": "My Awesome Walkthrough",
  "description": "Detailed walkthrough of feature X",
  "tags": ["tutorial", "feature-x", "demo"]
}
```

### Q: Can I exclude certain repositories from the gallery?

**A:** Yes, add `.nojekyll` file to the repository or configure exclusions in
`_config.yml`.

### Q: How do I change the site title?

**A:** Edit `_config.yml`:

```yaml
title: "Your Custom Title"
description: "Your custom description"
```

### Q: Can I customize the layout?

**A:** Yes, edit `docs/_layouts/default.html` to modify the page structure and
styling.

______________________________________________________________________

## Troubleshooting

### Site Not Building

**Problem**: GitHub Pages build fails

**Solutions**:

1. Check Actions tab for build errors
1. Verify `_config.yml` syntax is valid YAML
1. Ensure Jekyll version compatibility
1. Check for missing dependencies in Gemfile

### Videos Not Appearing

**Problem**: Videos uploaded but not showing in gallery

**Solutions**:

1. Check file location (must be in `/walkthroughs` or similar)
1. Verify file format is MP4, WebM, or MOV
1. Wait for next scheduled index generation (up to 6 hours)
1. Trigger manual index generation workflow

### Search Not Working

**Problem**: Search bar not filtering results

**Solutions**:

1. Clear browser cache
1. Check JavaScript console for errors
1. Verify walkthrough data file exists at `docs/_data/walkthroughs.yml`
1. Ensure data format is valid YAML

### Dark Mode Not Toggling

**Problem**: Theme toggle button doesn't work

**Solutions**:

1. Check browser localStorage permissions
1. Clear browser cache and localStorage
1. Try different browser
1. Verify JavaScript is enabled

### Custom Domain Not Working

**Problem**: Custom domain shows 404 error

**Solutions**:

1. Verify DNS CNAME record is correct
1. Wait for DNS propagation (up to 24 hours)
1. Check GitHub Pages settings
1. Ensure HTTPS is enforced
1. Verify `_config.yml` URL is correct

______________________________________________________________________

## Advanced Configuration

### Multiple Languages

Support multiple languages by creating language-specific data files:

```yaml
# _data/walkthroughs_en.yml
# _data/walkthroughs_es.yml
```

### Custom Metadata Fields

Extend walkthrough metadata:

```yaml
# docs/_data/walkthroughs.yml
- title: "My Walkthrough"
  repository: "{{ORG_NAME}}/myrepo"
  custom_field: "Custom Value"
  rating: 5
  views: 1234
```

### API Integration

Expose walkthrough data via API:

```yaml
# _data/api/walkthroughs.json
```

Access at: `https://{{ORG_NAME}}.github.io/.github/_data/api/walkthroughs.json`

______________________________________________________________________

## Support

Need help? Contact:

- 💬 **GitHub**:
  [@4444JPP](https://github.com/4444JPP)<!-- link:examples.sample_profile -->
- 📚 **Documentation**: AgentSphere Setup
- 🐛 **Issues**:
  [Report a bug](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- 📖 **Jekyll Docs**: https://jekyllrb.com/docs/

______________________________________________________________________

**Last Updated**: 2025-12-21 **Version**: 1.0.0

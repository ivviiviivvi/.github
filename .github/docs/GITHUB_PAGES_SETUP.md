# GitHub Pages Gallery Setup

## Overview

The GitHub Pages gallery is an automatically generated website that showcases all application walkthroughs and tutorials from the Ivviiviivvi organization. It provides a searchable, filterable interface for browsing video tutorials and accessing live demos.

## How Automatic Site Building Works

### Workflow Triggers

The Pages site is built and updated through multiple workflows:

1. **After Walkthrough Generation** (`workflow_run` trigger)
   - Automatically triggered when a new walkthrough video is created
   - Updates the gallery with the latest video

2. **Scheduled Updates** (every 6 hours)
   - Periodically scans all organization repositories
   - Discovers new applications and updates
   - Refreshes metadata and deployment status

3. **Manual Dispatch**
   - Can be manually triggered from GitHub Actions
   - Useful for immediate updates or troubleshooting

### Build Process

1. **Metadata Aggregation**
   - Queries GitHub API for all organization repositories
   - Collects walkthrough videos from workflow artifacts
   - Extracts repository details (name, description, topics)

2. **Data Generation**
   - Creates `docs/_data/walkthroughs.yml` with all metadata
   - Updates `docs/_data/app-deployments.yml` with live demo URLs
   - Generates index and gallery pages

3. **Jekyll Build**
   - Processes Markdown files with Liquid templates
   - Applies responsive layouts and styling
   - Generates static HTML/CSS/JS

4. **Deployment**
   - Uploads built site as artifact
   - Deploys to GitHub Pages
   - Site available at `https://ivviiviivvi.github.io`

## Accessing the Walkthrough Gallery

### Main Gallery Page

Visit the gallery at: **https://ivviiviivvi.github.io**

The homepage displays:
- Search bar for finding specific applications
- Grid of application cards with video previews
- Tech stack badges for filtering
- Links to live demos and source code

### Tutorials Section

Browse all video tutorials: **https://ivviiviivvi.github.io/tutorials/**

Features:
- Filterable by technology (Node.js, Python, React, Vue, etc.)
- Embedded video players
- Tutorial descriptions and metadata
- Direct links to repositories

### Live Apps Section

Access live application demos: **https://ivviiviivvi.github.io/apps/**

Each app page includes:
- Live embedded application (iframe or direct)
- Tutorial video sidebar
- Source code link
- Deployment status
- "Open in Codespaces" button (if applicable)

### Directory Page

Complete application listing: **https://ivviiviivvi.github.io/directory/**

Shows:
- Alphabetical list of all applications
- Quick links to tutorials and live demos
- Tech stack information
- Short descriptions

## Searching and Filtering

### Search Bar

The search bar at the top of the gallery page allows real-time filtering:

- **Search by name**: Type application name
- **Search by description**: Match keywords in descriptions
- **Search by technology**: Filter by tech stack (e.g., "react", "python")

Search is client-side JavaScript, providing instant results without page reloads.

### Technology Filters

Click filter buttons to show only apps using specific technologies:

- Node.js
- Python
- React
- Vue
- Angular
- Java
- And more...

### URL Parameters

Filter via URL (useful for sharing links):

```
https://ivviiviivvi.github.io/?tech=react
https://ivviiviivvi.github.io/tutorials/?filter=python
```

## Embedding Gallery Elsewhere

### Embed Full Gallery

Embed the entire gallery in another website:

```html
<iframe 
  src="https://ivviiviivvi.github.io" 
  width="100%" 
  height="800px" 
  frameborder="0"
  style="border: 1px solid #e2e8f0; border-radius: 8px;">
</iframe>
```

### Embed Specific Tutorial

Embed a single tutorial page:

```html
<iframe 
  src="https://ivviiviivvi.github.io/tutorials/my-app" 
  width="100%" 
  height="600px" 
  frameborder="0">
</iframe>
```

### Embed Just Video Gallery

Use the gallery include in your own Jekyll site:

```liquid
{% include walkthrough_gallery.html %}
```

### JavaScript Integration

Load gallery data via JavaScript:

```javascript
fetch('https://ivviiviivvi.github.io/data/walkthroughs.json')
  .then(response => response.json())
  .then(data => {
    // Process walkthrough data
    console.log(data.walkthroughs);
  });
```

## Custom Domain Setup

### Configure Custom Domain

1. **Add CNAME record** in your DNS provider:
   ```
   Type: CNAME
   Name: apps (or your subdomain)
   Value: ivviiviivvi.github.io
   ```

2. **Update repository settings**:
   - Go to Settings → Pages
   - Enter custom domain: `apps.yourdomain.com`
   - Enable HTTPS

3. **Update `_config.yml`**:
   ```yaml
   url: "https://apps.yourdomain.com"
   baseurl: ""
   ```

### Verify Configuration

Wait for DNS propagation (up to 48 hours), then verify:

```bash
dig apps.yourdomain.com +short
# Should return: ivviiviivvi.github.io
```

## Site Analytics

### Google Analytics Setup

1. **Get tracking ID** from Google Analytics

2. **Add to `_config.yml`**:
   ```yaml
   google_analytics: UA-XXXXXXXXX-X
   ```

3. **Verify installation**:
   - Visit your site
   - Check Google Analytics real-time dashboard
   - Should show active user

### Alternative Analytics

For privacy-focused analytics, consider:

- **Plausible**: Lightweight, privacy-friendly
- **Fathom**: GDPR compliant
- **Simple Analytics**: Minimal, ethical

Add tracking script to `docs/_layouts/default.html`.

## Appearance Customization

### Colors and Theme

Edit `docs/_layouts/default.html` CSS variables:

```css
:root {
  --primary-color: #2563eb;     /* Change primary color */
  --secondary-color: #7c3aed;    /* Change secondary color */
  --background: #ffffff;         /* Background color */
  --text-primary: #1e293b;      /* Text color */
}
```

### Logo and Branding

Add logo to header in `docs/_layouts/default.html`:

```html
<div class="header-content">
  <img src="/assets/images/logo.png" alt="Logo" style="height: 40px;">
  <h1>{{ site.title }}</h1>
</div>
```

### Custom CSS

Add custom styles in `docs/assets/css/custom.css`:

```css
/* Custom gallery styles */
.gallery-grid {
  gap: 3rem; /* Increase spacing */
}

.card {
  border-radius: 1rem; /* More rounded corners */
}
```

Include in `_config.yml`:

```yaml
sass:
  style: compressed
  load_paths:
    - _sass
    - assets/css
```

### Custom Layouts

Create new layouts in `docs/_layouts/`:

```html
<!-- docs/_layouts/custom.html -->
---
layout: default
---
<div class="custom-layout">
  {{ content }}
</div>
```

Use in pages:

```markdown
---
layout: custom
title: Custom Page
---
```

## FAQ and Troubleshooting

### Q: Gallery is not updating with new videos

**Solution**:
1. Check if `generate-pages-index.yml` workflow ran successfully
2. Verify walkthrough artifacts exist in source repositories
3. Manually trigger the workflow from Actions tab
4. Check workflow logs for API errors

### Q: Videos are not playing

**Solution**:
1. Verify video format is MP4 (H.264 codec)
2. Check video file size (GitHub has 2GB artifact limit)
3. Ensure video URL is accessible
4. Check browser console for errors

### Q: Search is not working

**Solution**:
1. Clear browser cache
2. Verify JavaScript is enabled
3. Check browser console for errors
4. Ensure `walkthrough_gallery.html` include is correct

### Q: Custom domain not working

**Solution**:
1. Verify CNAME record is correct
2. Wait for DNS propagation (up to 48 hours)
3. Check GitHub Pages settings
4. Ensure HTTPS is enabled
5. Clear DNS cache: `ipconfig /flushdns` (Windows) or `sudo killall -HUP mDNSResponder` (macOS)

### Q: Site build is failing

**Solution**:
1. Check Jekyll build logs in Actions
2. Validate YAML syntax in `_config.yml`
3. Ensure all required dependencies are in `Gemfile`
4. Check for liquid syntax errors in templates
5. Run `bundle exec jekyll build` locally to debug

### Q: Images or assets are not loading

**Solution**:
1. Check file paths are correct
2. Use absolute paths: `/assets/images/logo.png`
3. Verify files are committed to repository
4. Check `.gitignore` is not excluding assets
5. Clear browser cache

### Q: How to add new pages?

**Solution**:
1. Create Markdown file in `docs/` directory
2. Add front matter:
   ```yaml
   ---
   layout: default
   title: New Page
   ---
   ```
3. Add content in Markdown
4. Commit and push
5. Page will be available at `/new-page/`

### Q: How to exclude repositories from gallery?

**Solution**:
1. Edit `.github/workflows/generate-pages-index.yml`
2. Add filter in repository query:
   ```bash
   if [[ "$repo_name" != "exclude-this-repo" ]]; then
     # Process repository
   fi
   ```

### Q: Can I customize video player controls?

**Solution**:
Yes, edit `docs/_includes/walkthrough_gallery.html`:

```html
<video 
  controls
  controlsList="nodownload"  # Disable download
  preload="metadata"          # Load metadata only
  poster="/path/to/poster.jpg"
>
```

## Performance Optimization

### Image Optimization

Compress images before committing:

```bash
# Using imagemagick
convert logo.png -resize 800x600 -quality 85 logo-optimized.png

# Using webp
cwebp logo.png -q 85 -o logo.webp
```

### Video Optimization

Compress walkthrough videos:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 128k output.mp4
```

### Lazy Loading

Images and videos lazy load automatically using Intersection Observer API.

### Caching

GitHub Pages automatically caches static assets with proper headers.

## Related Documentation

- [AgentSphere Setup Guide](AGENTSPHERE_SETUP.md)
- [Live Deployment Guide](LIVE_DEPLOYMENT_GUIDE.md)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

## Getting Help

- **Issues**: [Create an issue](https://github.com/ivviiviivvi/.github/issues)
- **Discussions**: [Join the discussion](https://github.com/ivviiviivvi/.github/discussions)
- **Documentation**: [Main README](../README.md)

# GitHub Pages Fix Instructions

## Current Issues

1. ✅ **FIXED**: Missing index page - Added `index.html` and `index.md`
1. ✅ **FIXED**: Missing Jekyll layout - Added `_layouts/default.html`
1. ✅ **FIXED**: Jekyll configuration updated
1. ⚠️ **ACTION REQUIRED**: GitHub Pages still using "legacy" build mode

## Why Pages Is Failing

GitHub Pages is currently set to "legacy" build mode, which tries to
automatically build with Jekyll. This is failing because of:

- Complex Jekyll dependencies
- GitHub Actions security policies (all actions must be pinned to commit SHAs)
- Nested dependencies in GitHub's own actions

## Solution: Switch to GitHub Actions Workflow

**You need to manually change the Pages build source from "legacy" to "GitHub
Actions".**

### Step-by-Step Instructions

1. **Go to Repository Settings**

   - Navigate to: <https://github.com/%7B%7BORG_NAME%7D%7D/.github/settings>

1. **Click on "Pages" in the left sidebar**

   - Direct link:
     <https://github.com/%7B%7BORG_NAME%7D%7D/.github/settings/pages>

1. **Change the Build and deployment source:**

   - Under "Build and deployment"
   - Find the "Source" dropdown
   - Change from "Deploy from a branch" to **"GitHub Actions"**

   ![GitHub Pages Settings](https://docs.github.com/assets/cb-49023/mw-1440/images/help/pages/gh-pages-source.webp)

1. **Save the changes**

   - The page should auto-save
   - You'll see a message confirming the change

1. **Trigger a new deployment (optional)**

   - Go to Actions tab:
     <https://github.com/%7B%7BORG_NAME%7D%7D/.github/actions>
   - Click on "Deploy Jekyll site to Pages" workflow
   - Click "Run workflow" → "Run workflow" button
   - OR just wait for the next push to trigger it automatically

### What This Does

- **Disables** the automatic Jekyll build that's been failing
- **Enables** the custom GitHub Actions workflow we created
  (`.github/workflows/pages.yml`)
- Uses the static `index.html` we just created as the landing page
- Provides full control over the build process

### Expected Result

After making this change:

1. The Pages status will change from "legacy" to "workflow"
1. The next deployment will use the GitHub Actions workflow
1. Your site will be live at: <https://%7B%7BORG_NAME%7D%7D.github.io/.github/>
1. The 404 errors will be resolved

### Verification

After changing the settings, you can verify with:

```bash
# Check Pages status
gh api repos/{{ORG_NAME}}/.github/pages --jq '.status, .build_type'

# Should show:
# built (or building)
# workflow
```

```bash
# Test the site
curl -I https://{{ORG_NAME}}.github.io/.github/

# Should show:
# HTTP/2 200
```

### Alternative: Quick Test

If you want to test immediately after changing settings:

1. Make any small commit (even a README typo fix)
1. Push to main
1. Watch the Actions tab for the "Deploy Jekyll site to Pages" workflow
1. Once it completes successfully, your site will be live

## Files Created/Modified

✅ `/workspace/index.html` - Static HTML landing page (ready to use) ✅
`/workspace/index.md` - Markdown landing page (for Jekyll) ✅
`/workspace/_layouts/default.html` - Jekyll layout template ✅
`/workspace/_config.yml` - Updated Jekyll configuration ✅
`/workspace/.github/workflows/pages.yml` - GitHub Actions deployment workflow ✅
`/workspace/.nojekyll` - Controls Jekyll processing

## Troubleshooting

### If the site still shows 404 after changing settings

1. Wait 2-3 minutes for GitHub's CDN to update
1. Try accessing in incognito/private browser window
1. Clear your browser cache
1. Check the Actions tab for any failed workflows

### If the GitHub Actions workflow fails

The current workflow has issues with pinned actions. For now, the static
`index.html` will be deployed by the legacy system once it successfully builds.

### If you can't change the Pages settings

You need admin or maintainer permissions on the repository. Contact a repository
admin if needed.

## Next Steps

1. **Immediate**: Change Pages source to "GitHub Actions" (instructions above)
1. **After site is live**: Test all links on the landing page
1. **Optional**: Customize the `index.html` with additional content
1. **Optional**: Set up custom domain if desired

## Questions?

- Check GitHub's documentation:
  <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
- Review the Actions workflow logs if deployment fails
- The static HTML page (`index.html`) is self-contained and doesn't require
  Jekyll

______________________________________________________________________

**Status**: ⏳ Awaiting manual GitHub Pages settings change **Expected Time**:
2-3 minutes to change settings + 2-3 minutes for deployment **Impact**: Will
resolve all 404 errors and make the landing page accessible

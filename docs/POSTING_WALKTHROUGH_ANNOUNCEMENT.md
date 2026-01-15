# How to Post the Walkthrough Announcement Discussion

This guide explains how to post the walkthrough announcement as a GitHub
Discussion in the Ivviiviivvi organization.

## Quick Steps

1. **Navigate to Organization Discussions**
   - Go to: https://github.com/orgs/ivviiviivvi/discussions

1. **Create New Discussion**
   - Click the **"New discussion"** button
   - Select category: **Announcements**

1. **Fill in Details**
   - **Title**: `🎬 Introducing: Autonomous Walkthrough Generation for All Repos`
   - **Body**: Copy the entire contents of
     [`WALKTHROUGH_ANNOUNCEMENT.md`](./WALKTHROUGH_ANNOUNCEMENT.md)

1. **Post Discussion**
   - Click **"Start discussion"**
   - Pin the discussion (optional but recommended)
   - Lock the discussion to comments only (optional)

## Alternative: Using GitHub CLI

If you have the GitHub CLI installed and authenticated:

```bash
# Navigate to the repository
cd /path/to/.github

# Create the discussion
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /orgs/ivviiviivvi/discussions \
  -f title='🎬 Introducing: Autonomous Walkthrough Generation for All Repos' \
  -f body="$(cat docs/WALKTHROUGH_ANNOUNCEMENT.md)" \
  -f category_id='<CATEGORY_ID_FOR_ANNOUNCEMENTS>'
```

To find the category ID:

```bash
gh api /orgs/ivviiviivvi/discussion-categories
```

## After Posting

Once the discussion is posted:

1. **Share the link** with the team
1. **Update this file** with the discussion URL
1. **Pin the discussion** for visibility
1. **Monitor for questions** and respond promptly

## Discussion Link

Once posted, add the link here:

- **Discussion URL**: \[To be added after posting\]

## Notes

- The announcement content is maintained in
  [`WALKTHROUGH_ANNOUNCEMENT.md`](./WALKTHROUGH_ANNOUNCEMENT.md)
- Any updates to the announcement should be made in that file first
- Consider re-posting or updating the discussion if major changes are made to
  the system

---

**Posted by**: @4444JPP **Date Posted**: 2025-12-21 (Update this after actual
posting) **Discussion ID**: \[To be filled in after posting\]

# Testing the Commit Tracking System

This document provides instructions for testing the commit tracking functionality.

## Manual Testing

### Testing Commit Tracking Workflow

The commit tracking workflow runs automatically on pushes to `main` or `develop` branches and on pull request updates.

To test manually:

1. Make any change to a file
2. Commit with a meaningful message:
   ```bash
   git commit -m "test: verify commit tracking workflow"
   ```
3. Push to `main` or `develop` branch
4. Check the Actions tab in GitHub to see the workflow run
5. Review the workflow summary for commit statistics

### Testing Weekly Commit Report

The weekly report runs every Monday at 9:00 AM UTC, but can also be triggered manually:

1. Go to the Actions tab in GitHub
2. Select "Weekly Commit Report" workflow
3. Click "Run workflow"
4. Click the green "Run workflow" button to confirm
5. Wait for the workflow to complete
6. Check the `reports/` directory for the generated report

### Testing Setup Script

To test the setup script locally:

```bash
chmod +x setup.sh  # Make the script executable if needed
./setup.sh
```

This will configure your local git to use the commit message template.

After running the setup script, test it:

```bash
git commit
```

You should see the commit message template in your editor.

## Validation Checklist

- [ ] Commit tracking workflow runs on push to main/develop
- [ ] Commit tracking workflow runs on pull request updates
- [ ] Commit message validation catches empty messages
- [ ] Commit statistics are generated correctly
- [ ] Weekly report can be manually triggered
- [ ] Weekly report generates markdown files in reports/
- [ ] Setup script configures git template successfully
- [ ] Commit message template appears when committing

## Expected Behavior

### Commit Tracking Workflow

When triggered, the workflow should:
1. Checkout the repository with full history
2. Display current commit information (SHA, author, branch, message)
3. Show pull request commits (if applicable)
4. Validate the commit message is not empty
5. Generate statistics for last 10 commits
6. Show commit activity by author for last 30 days

### Weekly Commit Report

When triggered, the workflow should:
1. Generate a markdown report with:
   - Total commits in last 7 days
   - Commits grouped by author
   - Commit frequency by date
   - Recent commit list with details
2. Save the report to `reports/commit-report-YYYY-MM-DD.md`
3. Commit and push the report to the repository

## Troubleshooting

### Workflow doesn't run

- Check that workflows are enabled in repository settings
- Verify the branch name matches `main` or `develop`
- Check Actions tab for any error messages

### Setup script fails

- Ensure you're in the repository root directory
- Check that `.github/.gitmessage` file exists
- Verify you have git installed and configured

### Reports not generated

- Check workflow permissions (needs `contents: write`)
- Verify git config in workflow is correct
- Check for any errors in the workflow logs

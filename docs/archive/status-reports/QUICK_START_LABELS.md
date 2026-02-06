# How to Run the Label Sync Script

## Step 1: Install PyGithub

```bash
# Install pipx if you don't have it
brew install pipx

# Install PyGithub using pipx (creates isolated environment)
pipx install PyGithub

# OR use pip with break-system-packages flag
pip3 install --break-system-packages PyGithub
```

## Step 2: Set your GitHub token

```bash
export GITHUB_TOKEN=your_github_token_here
```

## Step 3: Run in dry-run mode first (safe - just shows what would change)

```bash
cd /Users/4jp/Workspace/{{ORG_NAME}}/.github
python3 scripts/sync_labels.py --org {{ORG_NAME}} --dry-run
```

## Step 4: If dry-run looks good, run it for real

```bash
python3 scripts/sync_labels.py --org {{ORG_NAME}}
```

## Alternative: Use gh CLI directly (no Python needed)

Create and run this script:

```bash
#!/bin/bash
ORG="{{ORG_NAME}}"

# Get all repos
repos=$(gh repo list "$ORG" --limit 1000 --json name -q '.[].name')

for repo in $repos; do
    echo "Processing $repo..."

    # Priority labels
    gh label create "priority: critical" --repo "$ORG/$repo" --color "d73a4a" --description "Critical priority" --force
    gh label create "priority: high" --repo "$ORG/$repo" --color "ff6b6b" --description "High priority" --force
    gh label create "priority: medium" --repo "$ORG/$repo" --color "ffa500" --description "Medium priority" --force
    gh label create "priority: low" --repo "$ORG/$repo" --color "0e8a16" --description "Low priority" --force

    # Type labels
    gh label create "bug" --repo "$ORG/$repo" --color "d73a4a" --description "Something isn't working" --force
    gh label create "enhancement" --repo "$ORG/$repo" --color "a2eeef" --description "New feature or request" --force
    gh label create "documentation" --repo "$ORG/$repo" --color "0075ca" --description "Improvements or additions to documentation" --force
    gh label create "security" --repo "$ORG/$repo" --color "d93f0b" --description "Security related" --force
    gh label create "task" --repo "$ORG/$repo" --color "d4c5f9" --description "General task or work item" --force
    gh label create "question" --repo "$ORG/$repo" --color "d876e3" --description "Further information is requested" --force

    # Status labels
    gh label create "triage" --repo "$ORG/$repo" --color "fbca04" --description "Needs triage" --force
    gh label create "in-progress" --repo "$ORG/$repo" --color "0052cc" --description "Work in progress" --force
    gh label create "blocked" --repo "$ORG/$repo" --color "b60205" --description "Blocked by dependency" --force
    gh label create "needs-review" --repo "$ORG/$repo" --color "6f42c1" --description "Ready for review" --force
    gh label create "approved" --repo "$ORG/$repo" --color "0e8a16" --description "Approved and ready to merge" --force

    # Additional labels
    gh label create "good first issue" --repo "$ORG/$repo" --color "7057ff" --description "Good for newcomers" --force
    gh label create "help wanted" --repo "$ORG/$repo" --color "008672" --description "Extra attention is needed" --force
done

echo "Done!"
```

Save this as `sync_labels.sh`, make it executable, and run it:

```bash
chmod +x sync_labels.sh
./sync_labels.sh
```

The `--force` flag will update existing labels or create them if they don't
exist.

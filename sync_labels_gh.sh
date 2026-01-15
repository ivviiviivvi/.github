#!/bin/bash
# Simple label sync using gh CLI
# Usage: ./sync_labels_gh.sh

ORG="ivviiviivvi"

echo "Fetching repositories from $ORG..."
repos=$(gh repo list "$ORG" --limit 1000 --json name,isArchived -q '.[] | select(.isArchived == false) | .name')

total=$(echo "$repos" | wc -l | tr -d ' ')
echo "Found $total active repositories"
echo ""

count=0
for repo in $repos; do
    count=$((count + 1))
    echo "[$count/$total] Processing $repo..."

    # Priority labels
    gh label create "priority: critical" --repo "$ORG/$repo" --color "d73a4a" --description "Critical priority" --force 2>/dev/null
    gh label create "priority: high" --repo "$ORG/$repo" --color "ff6b6b" --description "High priority" --force 2>/dev/null
    gh label create "priority: medium" --repo "$ORG/$repo" --color "ffa500" --description "Medium priority" --force 2>/dev/null
    gh label create "priority: low" --repo "$ORG/$repo" --color "0e8a16" --description "Low priority" --force 2>/dev/null

    # Type labels
    gh label create "bug" --repo "$ORG/$repo" --color "d73a4a" --description "Something isn't working" --force 2>/dev/null
    gh label create "enhancement" --repo "$ORG/$repo" --color "a2eeef" --description "New feature or request" --force 2>/dev/null
    gh label create "documentation" --repo "$ORG/$repo" --color "0075ca" --description "Improvements or additions to documentation" --force 2>/dev/null
    gh label create "security" --repo "$ORG/$repo" --color "d93f0b" --description "Security related" --force 2>/dev/null
    gh label create "task" --repo "$ORG/$repo" --color "d4c5f9" --description "General task or work item" --force 2>/dev/null
    gh label create "question" --repo "$ORG/$repo" --color "d876e3" --description "Further information is requested" --force 2>/dev/null

    # Status labels
    gh label create "triage" --repo "$ORG/$repo" --color "fbca04" --description "Needs triage" --force 2>/dev/null
    gh label create "in-progress" --repo "$ORG/$repo" --color "0052cc" --description "Work in progress" --force 2>/dev/null
    gh label create "blocked" --repo "$ORG/$repo" --color "b60205" --description "Blocked by dependency" --force 2>/dev/null
    gh label create "needs-review" --repo "$ORG/$repo" --color "6f42c1" --description "Ready for review" --force 2>/dev/null
    gh label create "approved" --repo "$ORG/$repo" --color "0e8a16" --description "Approved and ready to merge" --force 2>/dev/null
    gh label create "wontfix" --repo "$ORG/$repo" --color "ffffff" --description "This will not be worked on" --force 2>/dev/null
    gh label create "duplicate" --repo "$ORG/$repo" --color "cfd3d7" --description "This issue or pull request already exists" --force 2>/dev/null
    gh label create "invalid" --repo "$ORG/$repo" --color "e4e669" --description "This doesn't seem right" --force 2>/dev/null

    # Category labels
    gh label create "category: github-actions" --repo "$ORG/$repo" --color "2088ff" --description "Related to GitHub Actions workflows" --force 2>/dev/null
    gh label create "category: configuration" --repo "$ORG/$repo" --color "e99695" --description "Configuration files or settings" --force 2>/dev/null
    gh label create "category: dependencies" --repo "$ORG/$repo" --color "0366d6" --description "Dependency updates or issues" --force 2>/dev/null
    gh label create "category: automated" --repo "$ORG/$repo" --color "bfd4f2" --description "Automated processes or bots" --force 2>/dev/null

    # Additional labels
    gh label create "good first issue" --repo "$ORG/$repo" --color "7057ff" --description "Good for newcomers" --force 2>/dev/null
    gh label create "help wanted" --repo "$ORG/$repo" --color "008672" --description "Extra attention is needed" --force 2>/dev/null

    echo "  ✓ Labels synced"
done

echo ""
echo "============================================================"
echo "✅ Done! Labels synced across $total repositories"
echo "============================================================"

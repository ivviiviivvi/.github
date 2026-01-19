#!/bin/bash
# Recover a deleted branch using audit log
# Usage: ./recover-branch.sh <branch-name>

set -e

BRANCH_NAME="${1}"

if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Branch name required"
  echo "Usage: $0 <branch-name>"
  exit 1
fi

AUDIT_DIR=".github/branch-deletion-audit"

if [ ! -d "$AUDIT_DIR" ]; then
  echo "❌ Error: Audit directory not found. No deletion records available."
  exit 1
fi

echo "🔍 Searching for deletion record of: $BRANCH_NAME"

# Search all audit files for the branch
FOUND=false
for audit_file in "$AUDIT_DIR"/*.jsonl; do
  if [ -f "$audit_file" ]; then
    # Search for branch in audit file
    RECORD=$(grep "\"branch\":\"$BRANCH_NAME\"" "$audit_file" 2>/dev/null || echo "")
    if [ -n "$RECORD" ]; then
      FOUND=true
      echo ""
      echo "📋 Found deletion record in: $audit_file"
      echo "$RECORD" | jq '.' 2>/dev/null || echo "$RECORD"
      
      # Extract SHA
      TIP_SHA=$(echo "$RECORD" | jq -r '.tip_sha' 2>/dev/null || echo "unknown")
      
      if [ "$TIP_SHA" = "unknown" ] || [ -z "$TIP_SHA" ]; then
        echo ""
        echo "❌ Error: Could not extract tip SHA from record"
        exit 1
      fi
      
      if [ "$TIP_SHA" = "already-deleted" ]; then
        echo ""
        echo "❌ Error: Branch was already deleted when audit was created"
        echo "   No SHA available for recovery"
        exit 1
      fi
      
      echo ""
      echo "🔧 Recovery Options:"
      echo ""
      echo "1. Create new branch from tip SHA:"
      echo "   git fetch origin $TIP_SHA"
      echo "   git branch $BRANCH_NAME $TIP_SHA"
      echo "   git push origin $BRANCH_NAME"
      echo ""
      echo "2. View the commit:"
      echo "   git show $TIP_SHA"
      echo ""
      echo "3. Create patch file:"
      echo "   git format-patch -1 $TIP_SHA -o /tmp/"
      echo ""
      echo "4. Cherry-pick to current branch:"
      echo "   git cherry-pick $TIP_SHA"
      echo ""
      
      # Check if SHA exists in repository
      if git cat-file -e "$TIP_SHA" 2>/dev/null; then
        echo "✅ SHA exists in local repository - ready for recovery"
      else
        echo "⚠️  SHA not found locally. Try: git fetch origin $TIP_SHA"
      fi
      
      break
    fi
  fi
done

if [ "$FOUND" = false ]; then
  echo ""
  echo "❌ No deletion record found for branch: $BRANCH_NAME"
  echo ""
  echo "Available deleted branches:"
  for audit_file in "$AUDIT_DIR"/*.jsonl; do
    if [ -f "$audit_file" ]; then
      grep -o "\"branch\":\"[^\"]*\"" "$audit_file" 2>/dev/null | cut -d'"' -f4 | sort -u || true
    fi
  done
  exit 1
fi

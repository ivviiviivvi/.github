#!/usr/bin/env bash
#
# log-branch-deletion.sh - Capture branch metadata before deletion for recovery
#
# Usage: ./log-branch-deletion.sh <branch-name> <reason> [pr-number]
#
# Arguments:
#   branch-name  Name of the branch being deleted
#   reason       Why the branch is being deleted:
#                - stale-pr-no-tasks
#                - stale-pr-with-tasks
#                - merged-branch
#   pr-number    Optional: Associated PR number
#
# Output:
#   Appends JSONL record to .github/branch-deletion-audit/YYYY-MM-deletions.jsonl
#

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate arguments
if [ $# -lt 2 ]; then
    log_error "Usage: $0 <branch-name> <reason> [pr-number]"
    log_error "  reason: stale-pr-no-tasks | stale-pr-with-tasks | merged-branch"
    exit 1
fi

BRANCH_NAME="$1"
REASON="$2"
PR_NUMBER="${3:-}"

# Validate reason
case "$REASON" in
    stale-pr-no-tasks|stale-pr-with-tasks|merged-branch)
        ;;
    *)
        log_error "Invalid reason: $REASON"
        log_error "Valid reasons: stale-pr-no-tasks, stale-pr-with-tasks, merged-branch"
        exit 1
        ;;
esac

# Setup paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT_DIR="$REPO_ROOT/.github/branch-deletion-audit"
CURRENT_MONTH=$(date +%Y-%m)
LOG_FILE="$AUDIT_DIR/${CURRENT_MONTH}-deletions.jsonl"

# Ensure audit directory exists
mkdir -p "$AUDIT_DIR"

# Get branch tip SHA
log_info "Capturing metadata for branch: $BRANCH_NAME"

TIP_SHA=$(git ls-remote --heads origin "$BRANCH_NAME" 2>/dev/null | awk '{print $1}' || echo "")

if [ -z "$TIP_SHA" ]; then
    log_warn "Could not find remote branch: $BRANCH_NAME"
    # Try to get from local if available
    TIP_SHA=$(git rev-parse "refs/remotes/origin/$BRANCH_NAME" 2>/dev/null || echo "unknown")
fi

# Get commit details if we have a valid SHA
COMMIT_MESSAGE="unknown"
COMMIT_AUTHOR="unknown"

if [ "$TIP_SHA" != "unknown" ] && [ -n "$TIP_SHA" ]; then
    # Try to get commit message (may fail if commit not fetched)
    COMMIT_MESSAGE=$(git log -1 --format="%s" "$TIP_SHA" 2>/dev/null || echo "unknown")
    COMMIT_AUTHOR=$(git log -1 --format="%ae" "$TIP_SHA" 2>/dev/null || echo "unknown")
fi

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Escape special characters for JSON
escape_json() {
    local str="$1"
    # Escape backslashes, quotes, and control characters
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/\\r}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

BRANCH_ESCAPED=$(escape_json "$BRANCH_NAME")
MESSAGE_ESCAPED=$(escape_json "$COMMIT_MESSAGE")
AUTHOR_ESCAPED=$(escape_json "$COMMIT_AUTHOR")

# Build JSON record
JSON_RECORD=$(cat <<EOF
{"timestamp":"$TIMESTAMP","branch":"$BRANCH_ESCAPED","tip_sha":"$TIP_SHA","pr_number":"$PR_NUMBER","commit_message":"$MESSAGE_ESCAPED","commit_author":"$AUTHOR_ESCAPED","reason":"$REASON","deleted_by":"branch-lifecycle-workflow"}
EOF
)

# Append to log file
echo "$JSON_RECORD" >> "$LOG_FILE"

log_info "Audit record saved to: $LOG_FILE"
log_info "  Branch: $BRANCH_NAME"
log_info "  Tip SHA: $TIP_SHA"
log_info "  Reason: $REASON"
[ -n "$PR_NUMBER" ] && log_info "  PR: #$PR_NUMBER"

# Output for workflow consumption
echo "tip_sha=$TIP_SHA"
echo "audit_file=$LOG_FILE"

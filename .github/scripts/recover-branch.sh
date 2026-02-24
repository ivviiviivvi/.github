#!/usr/bin/env bash
#
# recover-branch.sh - Search audit logs and recover deleted branches
#
# Usage: ./recover-branch.sh <branch-name> [--execute]
#
# Arguments:
#   branch-name  Name of the branch to recover (supports partial match)
#   --execute    Actually execute the recovery commands (default: dry-run)
#
# Examples:
#   ./recover-branch.sh feature/payment     # Search and show recovery commands
#   ./recover-branch.sh feature/payment --execute  # Actually recover the branch
#

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_header() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}\n"
}

# Validate arguments
if [ $# -lt 1 ]; then
    log_error "Usage: $0 <branch-name> [--execute]"
    exit 1
fi

SEARCH_TERM="$1"
EXECUTE_MODE=false

if [ "${2:-}" = "--execute" ]; then
    EXECUTE_MODE=true
fi

# Setup paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT_DIR="$REPO_ROOT/.github/branch-deletion-audit"

# Check if audit directory exists
if [ ! -d "$AUDIT_DIR" ]; then
    log_error "Audit directory not found: $AUDIT_DIR"
    log_error "No branch deletion records available."
    exit 1
fi

# Search for branch in audit logs
print_header "Searching for: $SEARCH_TERM"

MATCHES=()
while IFS= read -r file; do
    if [ -f "$file" ]; then
        while IFS= read -r line; do
            if [ -n "$line" ]; then
                MATCHES+=("$line")
            fi
        done < <(grep -h "\"branch\":\"[^\"]*${SEARCH_TERM}[^\"]*\"" "$file" 2>/dev/null || true)
    fi
done < <(find "$AUDIT_DIR" -name "*.jsonl" -type f 2>/dev/null)

if [ ${#MATCHES[@]} -eq 0 ]; then
    log_warn "No matching branches found for: $SEARCH_TERM"
    echo ""
    echo "Tips:"
    echo "  - Try a partial branch name (e.g., 'feature' instead of 'feature/my-branch')"
    echo "  - Check available logs: ls -la $AUDIT_DIR"
    echo "  - Search all logs: grep -r 'search-term' $AUDIT_DIR"
    exit 1
fi

echo -e "${GREEN}Found ${#MATCHES[@]} matching record(s):${NC}\n"

# Display each match
for i in "${!MATCHES[@]}"; do
    RECORD="${MATCHES[$i]}"

    # Parse JSON fields (basic parsing without jq dependency)
    TIMESTAMP=$(echo "$RECORD" | sed 's/.*"timestamp":"\([^"]*\)".*/\1/')
    BRANCH=$(echo "$RECORD" | sed 's/.*"branch":"\([^"]*\)".*/\1/')
    TIP_SHA=$(echo "$RECORD" | sed 's/.*"tip_sha":"\([^"]*\)".*/\1/')
    PR_NUMBER=$(echo "$RECORD" | sed 's/.*"pr_number":"\([^"]*\)".*/\1/')
    COMMIT_MSG=$(echo "$RECORD" | sed 's/.*"commit_message":"\([^"]*\)".*/\1/')
    REASON=$(echo "$RECORD" | sed 's/.*"reason":"\([^"]*\)".*/\1/')

    echo -e "${BLUE}━━━ Match $((i+1)) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${CYAN}Branch:${NC}   $BRANCH"
    echo -e "  ${CYAN}Deleted:${NC}  $TIMESTAMP"
    echo -e "  ${CYAN}Tip SHA:${NC}  $TIP_SHA"
    [ -n "$PR_NUMBER" ] && echo -e "  ${CYAN}PR:${NC}       #$PR_NUMBER"
    echo -e "  ${CYAN}Reason:${NC}   $REASON"
    echo -e "  ${CYAN}Message:${NC}  $COMMIT_MSG"
    echo ""

    if [ "$TIP_SHA" != "unknown" ] && [ -n "$TIP_SHA" ]; then
        echo -e "  ${GREEN}Recovery Commands:${NC}"
        echo -e "    ${YELLOW}git fetch origin $TIP_SHA${NC}"
        echo -e "    ${YELLOW}git branch $BRANCH $TIP_SHA${NC}"
        echo -e "    ${YELLOW}git push origin $BRANCH${NC}"
        echo ""

        if [ "$EXECUTE_MODE" = true ]; then
            print_header "Executing Recovery for: $BRANCH"

            log_info "Fetching commit $TIP_SHA..."
            if git fetch origin "$TIP_SHA" 2>/dev/null; then
                log_info "Creating local branch $BRANCH..."
                if git branch "$BRANCH" "$TIP_SHA" 2>/dev/null; then
                    log_info "Pushing branch to origin..."
                    if git push origin "$BRANCH" 2>/dev/null; then
                        echo -e "\n${GREEN}✅ Branch successfully recovered: $BRANCH${NC}\n"
                    else
                        log_error "Failed to push branch to origin"
                    fi
                else
                    log_warn "Branch may already exist locally"
                fi
            else
                log_error "Failed to fetch commit. The commit may have been garbage collected."
                log_warn "Try: git fsck --lost-found to find dangling commits"
            fi
        fi
    else
        log_warn "  Cannot recover: tip SHA is unknown"
    fi
done

if [ "$EXECUTE_MODE" = false ] && [ ${#MATCHES[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}To execute recovery, run:${NC}"
    echo -e "  $0 \"$SEARCH_TERM\" --execute"
    echo ""
    echo -e "${YELLOW}Note:${NC} If the commit has been garbage collected, recovery may not be possible."
    echo "      GitHub retains commits for ~90 days after branch deletion."
fi

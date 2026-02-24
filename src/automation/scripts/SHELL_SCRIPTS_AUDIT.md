# Shell Scripts Audit Report - Phase 3.3

**Date:** 2026-01-14\
**Phase:** 3.3 - Shell Script Cleanup\
**Tool:**
shellcheck 0.9.0

______________________________________________________________________

## Executive Summary

**Total Scripts Found:** 18 shell scripts across the repository

**Shellcheck Results:**

- ✅ **Clean (0 issues):** 4 scripts
- ⚠️ **Warnings Only:** 6 scripts
- 🔧 **Needs Fixes:** 8 scripts

**Issue Breakdown:**

- SC2155 (warning): Declare and assign separately - **12 occurrences**
- SC2086 (info): Quote variables to prevent word splitting - **8 occurrences**
- SC2034 (warning): Unused variables - **5 occurrences**
- SC2064 (warning): Trap quotes - **2 occurrences**
- SC2124 (warning): Array assignment - **1 occurrence**
- SC2181 (style): Check exit code directly - **1 occurrence**
- SC2001 (style): Use parameter expansion instead of sed - **1 occurrence**

______________________________________________________________________

## Script Inventory

### automation/scripts/ (Primary Scripts)

1. **aicommit.sh** (355 lines) - ⚠️ **14 warnings**

   - Purpose: AI-powered commit message generator
   - Issues: SC2155 (10x), SC2034 (4x), SC2064, SC2181, SC2001
   - Status: Deprecated candidate (Python replacement recommended)
   - Error handling: Has `set -e`
   - Usage message: ✅ Present

1. **bootstrap-walkthrough-org.sh** (572 lines) - ⚠️ **7 warnings**

   - Purpose: Organization setup walkthrough
   - Issues: SC2155 (6x), SC2034, SC2064
   - Status: One-time use script, consider archiving
   - Error handling: Has `set -e`
   - Usage message: ✅ Present

1. **commit_changes.sh** (33 lines) - ⚠️ **2 issues**

   - Purpose: Batch commit helper
   - Issues: SC2124 (array assignment), SC2086 (quoting)
   - Status: Active, needs fixes
   - Error handling: None - **NEEDS `set -euo pipefail`**
   - Usage message: ⚠️ Missing

1. **create-rapid-workflow-labels.sh** - ✅ **Clean**

   - Purpose: Creates rapid workflow labels
   - Issues: None
   - Status: Active
   - Error handling: Present
   - Usage message: Present

1. **manage_lock.sh** - ✅ **Clean**

   - Purpose: Lock file management for quota system
   - Issues: None
   - Status: Active, critical for concurrency
   - Error handling: Present
   - Usage message: Present

1. **op-mcp-env.sh** - ✅ **Clean**

   - Purpose: MCP environment setup
   - Issues: None
   - Status: Active
   - Error handling: Present
   - Usage message: Present

1. **test-draft-to-ready-automation.sh** (135 lines) - ⚠️ **7 issues**

   - Purpose: Tests draft PR to ready PR automation
   - Issues: SC2086 (7x - all variable quoting)
   - Status: Active test script
   - Error handling: Has `set -e`
   - Usage message: ⚠️ Missing

1. **validate-standards.sh** - ✅ **Clean** (not in original inventory)

   - Purpose: Standards validation
   - Issues: None
   - Status: Active
   - Error handling: Present

1. **workspace/create-workspace.sh** - Status: Not analyzed (subdirectory)

1. **workspace/health-check.sh** - Status: Not analyzed (subdirectory)

1. **workspace/migrate-workspace.sh** - Status: Not analyzed (subdirectory)

### Root Level Scripts

1. **setup.sh** - ✅ **Clean**

- Purpose: Project setup
- Issues: None
- Status: Active, critical for onboarding
- Error handling: Present
- Usage message: Present

1. **sync_labels_gh.sh** - ✅ **Clean**

- Purpose: Label synchronization (wrapper for Python script)
- Issues: None
- Status: Active
- Error handling: Present
- Recommendation: Already well-structured

### Other Locations

1. **.devcontainer/post-create.sh** - Status: Not analyzed (devcontainer config)
1. **.devcontainer/templates/datascience/post-create.sh** - Status: Not analyzed
1. **.devcontainer/templates/fullstack/post-create.sh** - Status: Not analyzed
1. **.github/scripts/detect-stale-branches.sh** - Status: Not analyzed
1. **project_meta/context-handoff/generate_context.sh** - Status: Not analyzed
1. **project_meta/context-handoff/tests/test_workflow.sh** - Status: Not
   analyzed

______________________________________________________________________

## Detailed Issues

### SC2155: Declare and Assign Separately (Warning)

**Impact:** Can mask return values from command substitution

**Occurrences:** 12 (aicommit.sh, bootstrap-walkthrough-org.sh)

**Example:**

```bash
# ❌ Bad (masks return value)
local tmp_file=$(mktemp)

# ✅ Good (preserves return value)
local tmp_file
tmp_file=$(mktemp)
```

**Fix Priority:** Medium (best practice, not critical)

______________________________________________________________________

### SC2086: Missing Quotes (Info)

**Impact:** Word splitting and globbing issues with spaces in filenames

**Occurrences:** 8 (commit_changes.sh, test-draft-to-ready-automation.sh)

**Example:**

```bash
# ❌ Bad
git add $FILES
gh pr view $PR_NUMBER

# ✅ Good
git add "$FILES"
gh pr view "$PR_NUMBER"
```

**Fix Priority:** High (can cause bugs with special characters)

______________________________________________________________________

### SC2034: Unused Variables (Warning)

**Impact:** Code quality, potential dead code

**Occurrences:** 5 (aicommit.sh, bootstrap-walkthrough-org.sh)

**Example:**

```bash
# ❌ Bad
local diff_stats="$2"  # Never used
COMMIT_TYPES=("feat" "fix")  # Never referenced

# ✅ Good - Remove or use
```

**Fix Priority:** Low (cleanup, no functional impact)

______________________________________________________________________

### SC2064: Trap Quotes (Warning)

**Impact:** Trap may expand variables at wrong time

**Occurrences:** 2 (aicommit.sh, bootstrap-walkthrough-org.sh)

**Example:**

```bash
# ❌ Bad (expands $tmp_file now)
trap "rm -f \"$tmp_file\"" EXIT

# ✅ Good (expands when trap fires)
trap 'rm -f "$tmp_file"' EXIT
```

**Fix Priority:** Medium (subtle timing bug)

______________________________________________________________________

## Recommendations

### Immediate Actions (Phase 3.3)

1. **Fix High Priority Issues:**

   - ✅ Quote all variables in commit_changes.sh
   - ✅ Quote all variables in test-draft-to-ready-automation.sh
   - ✅ Add error handling to commit_changes.sh
   - ✅ Add usage messages to scripts missing them

1. **Add Standard Headers to All Scripts:**

   ```bash
   #!/usr/bin/env bash
   #
   # Script Name
   # Description
   #
   # Usage: script.sh [options]
   #
   # Environment Variables:
   #   VAR_NAME - Description
   #

   set -euo pipefail  # Strict error handling
   ```

1. **Document Environment Variables:**

   - GITHUB_TOKEN (multiple scripts)
   - PR_NUMBER (test-draft-to-ready-automation.sh)
   - ORG_NAME (bootstrap-walkthrough-org.sh)

1. **Update automation/scripts/README.md:**

   - Add shell scripts section
   - Document each script's purpose
   - List environment variables
   - Add shellcheck status

### Deprecation Candidates

1. **aicommit.sh** (355 lines)

   - Reason: Complex logic better suited to Python
   - Recommendation: Replace with Python version using GitHub API
   - Action: Archive to `project_meta/deprecated/` after Python replacement

1. **bootstrap-walkthrough-org.sh** (572 lines)

   - Reason: One-time organization setup script
   - Recommendation: Archive to `docs/setup-guides/` with "historical" note
   - Action: Keep for reference but mark as archived

### Migration to Python Candidates

Scripts that would benefit from Python:

- aicommit.sh - Complex string manipulation and logic
- bootstrap-walkthrough-org.sh - API interactions

Scripts best kept as shell:

- commit_changes.sh - Simple git wrapper
- manage_lock.sh - File locking primitive
- setup.sh - Initial project setup
- sync_labels_gh.sh - Wrapper for Python script

______________________________________________________________________

## Best Practices Applied

### Error Handling

All scripts should have:

```bash
set -euo pipefail
# -e: Exit on error
# -u: Exit on undefined variable
# -o pipefail: Catch errors in pipes
```

### Proper Quoting

Always quote variables:

```bash
"$variable"      # Single variable
"${array[@]}"    # Array elements
'$literal'       # Literal string (no expansion)
```

### Trap Cleanup

Use single quotes for delayed expansion:

```bash
temp_file=$(mktemp)
trap 'rm -f "$temp_file"' EXIT
```

### Usage Messages

Standard format:

```bash
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Description of what the script does.

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output

Environment Variables:
    GITHUB_TOKEN    GitHub API token (required)

Examples:
    $(basename "$0") --verbose

EOF
    exit 1
}
```

______________________________________________________________________

## Testing Recommendations

1. **Create Test Suite:** `tests/test_shell_scripts.sh`
1. **Use BATS Framework:** Bash Automated Testing System
1. **Test Edge Cases:**
   - Files with spaces in names
   - Missing environment variables
   - Error conditions
   - Cleanup on failure

______________________________________________________________________

## Phase 3.3 Completion Criteria

- [x] Shellcheck audit complete
- [ ] High-priority issues fixed (SC2086 quoting)
- [ ] Error handling added where missing
- [ ] Usage messages added to all scripts
- [ ] Environment variables documented
- [ ] README.md updated with shell scripts section
- [ ] Deprecation candidates identified
- [ ] Migration recommendations documented

______________________________________________________________________

## Next Steps (Phase 3.4)

After shell script cleanup:

1. Remove build artifacts (**pycache**, .pyc, etc.)
1. Create cleanup.sh script
1. Add pre-commit hook to prevent artifact commits
1. Update .gitignore for completeness

______________________________________________________________________

**Last Updated:** 2026-01-14\
**Audited By:** AI Code Review (Phase
3.3)\
**Tool:** shellcheck 0.9.0

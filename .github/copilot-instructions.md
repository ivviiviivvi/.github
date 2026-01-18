---
description: AI rules derived by SpecStory from the project AI interaction history
globs: *
---

## description: AI rules derived by SpecStory from the project AI interaction history globs: \*

## description: AI rules derived by SpecStory from the project AI interaction history globs: \*

## PROJECT OVERVIEW

## CODE STYLE

## FOLDER ORGANIZATION

## TECH STACK

## PROJECT-SPECIFIC STANDARDS

## WORKFLOW & RELEASE RULES

- The discussion/issue/PR workflow should follow GitHub best practices,
  standards, and protocols.
- Use discussions for exploration, issues for commitment, and PRs for
  implementation.
- Implement early quality gates at each transition.
- Ensure clear ownership for every item.
- Automate processes using GitHub Actions.

## REFERENCE EXAMPLES

## PROJECT DOCUMENTATION & CONTEXT SYSTEM

## DEBUGGING

- **Git Commit Issues:**
  - If commits are blocked due to pre-commit hook failures, especially with
    `mypy`, check for issues related to the `types-all` dependency in
    `.pre-commit-config-rapid.yaml`.
  - The `mypy` hook may fail if it tries to install `types-all`, which depends
    on a yanked/nonexistent stub package (`types-pkg-resources`).
  - To resolve:
    - Remove or narrow the `types-all` dependency in
      `.pre-commit-config-rapid.yaml` under the `mypy` hook. For example, delete
      `additional_dependencies: [types-all]` or replace it with only the stubs
      you actually need (e.g., `types-requests`, etc.).
    - Run `pre-commit clean && pre-commit install` (or just retry the commit;
      pre-commit will reinstall environments).
    - Optional: run `pre-commit autoupdate` to pull newer hook revisions, but
      the main issue is `types-all`.
  - After resolving the `types-all` issue, refresh the pre-commit environments
    and reinstall the hooks using: `pre-commit clean && pre-commit install`.
    Then, retry the commit.

- **Pre-commit Hook Failures:**
  - When pre-commit hooks fail, address the issues systematically:
    1. **Shell Scripts:** Ensure shell scripts have executable permissions
       (`chmod +x script_name.py`).
    1. **YAML Formatting:** Check `.bandit` for YAML syntax errors.
    1. **Markdown Formatting:** Use `mdformat` to fix markdown issues.
    1. **Python Linting:** Resolve `flake8` and `mypy` errors.
    1. **Shell Linting:** Address `shellcheck` issues.
    1. **Configuration Issues:** Resolve issues reported by `bandit` and
       `detect-secrets`.
  - For `detect-secrets` issues, try running `pre-commit autoupdate`.
  - If ESLint reports missing configuration, create an `.eslintrc.json` file.
    Example:
    ```json
    {
      "env": {
        "browser": true,
        "es2021": true,
        "node": true
      },
      "extends": "eslint:recommended",
      "parserOptions": {
        "ecmaVersion": 12,
        "sourceType": "module"
      },
      "rules": {}
    }
    ```
  - To auto-fix formatting issues, stage all changes (`git add -u`) before
    committing.
  - If pre-commit hooks are causing persistent issues, temporarily bypass them
    using
    `git commit --no-verify -m "chore: fix pre-commit hook configuration issues"`
    (use with caution).

- **Comprehensive Pre-commit Troubleshooting:**
  - If facing multiple pre-commit failures, follow these steps:
    1. **Identify the Issues:** Carefully examine the pre-commit output to
       pinpoint the specific errors. These often include:
       - YAML syntax errors (e.g., in `.bandit` or
         `.pre-commit-config-rapid.yaml`)
       - Markdown formatting problems.
       - Python linting errors (flake8, mypy).
       - Shell script permission issues.
       - Configuration problems flagged by bandit or detect-secrets.
    1. **Address Shell Script Permissions:** Use `chmod +x script_name.py` to
       grant execute permissions to the relevant scripts. Example:
       ```bash
       chmod +x automation/scripts/ecosystem_visualizer.py
       chmod +x automation/scripts/update_agent_docs.py
       chmod +x automation/scripts/mouthpiece_filter.py
       chmod +x project_meta/context-handoff/context_generator.py
       ```
    1. **Update pre-commit hooks:** Run `pre-commit autoupdate` to update
       `detect-secrets` and other hooks.
    1. **Fix YAML Configuration:** Correct any YAML syntax errors. For example,
       a minimal `.bandit` configuration may look like:
       ```yaml
       ---
       exclude_dirs:
         - /tests/
         - /test/
         - .venv/
         - venv/
       ```
    1. **Create ESLint Configuration (if missing):** If ESLint reports a missing
       configuration, create an `.eslintrc.json` file:
       ```json
       {
         "env": {
           "browser": true,
           "es2021": true,
           "node": true
         },
         "extends": "eslint:recommended",
         "parserOptions": {
           "ecmaVersion": 12,
           "sourceType": "module"
         },
         "rules": {}
       }
       ```
    1. **Auto-Fix Formatting Issues:** Stage all changes (`git add -u`) and
       recommit to allow pre-commit to auto-fix formatting issues (YAML,
       Markdown, etc.).
    1. **Run All pre-commit checks:** Use `pre-commit run --all-files || true`
       to attempt auto-fixing all issues.
    1. **Add auto-fixes:** Use `git add -A` to stage the auto-fixed changes.
    1. **Commit:** Use
       `git commit -m "chore: fix pre-commit issues and format code"` to commit
       the staged changes.
    1. **Bypass (If Necessary):** If pre-commit hooks persist, temporarily
       bypass them using
       `git commit --no-verify -m "chore: commit all changes (pre-commit fixes to follow)"`.
       **Use this as a last resort.**

- **Pre-commit Hook Dependency Conflict:**
  - When pre-commit hooks fail due to dependency conflicts, especially with
    `mdformat`, update to a compatible version that works with GFM plugins.
  - Specifically, ensure that the `mdformat` hook in
    `.pre-commit-config-rapid.yaml` is using a compatible revision and includes
    the necessary `additional_dependencies`.
  - Example:
    ```yaml
    # ...existing code...
    - repo: https://github.com/executablebooks/mdformat
      rev: 0.7.17 # Compatible with gfm plugins
      hooks:
        - id: mdformat
          additional_dependencies:
            - mdformat-gfm>=0.3.5
            - mdformat-tables
            - mdformat-toc
      args: [--wrap, "120"]
    # ...existing code...
    ```
  - **Resolution Steps:**
    1. **Examine Current Configuration:** Check the current `mdformat`
       configuration in `.pre-commit-config.yaml`.
    1. **Apply the Fix:** Update the `mdformat` configuration to use
       `rev: 0.7.17` and include `mdformat-gfm>=0.3.5`, `mdformat-tables`, and
       `mdformat-toc` in `additional_dependencies`. Ensure
       `args: [--wrap, '120']` is also present.
    1. **Check for Rapid Config:** If `.pre-commit-config-rapid.yaml` exists,
       apply the same fix to it.
    1. **Clean and Reinstall:** Run `pre-commit clean`, `pre-commit install`,
       and
       `pre-commit autoupdate --repo https://github.com/executablebooks/mdformat`.
    1. **Test the Fix:** Run `pre-commit run mdformat --all-files` and
       `pre-commit run --all-files` to verify the fix.
    1. **Update Documentation:** Remove any `--no-verify` workarounds from
       `docs/`, `CONTRIBUTING.md`, `README.md`, and `CLEANUP_ROADMAP.md`.
    1. **Commit the Fix:** Stage the changes and commit with the message:
       `fix: update mdformat to v0.7.17 for gfm plugin compatibility - Update mdformat from 1.0.0 to 0.7.17 - Maintains compatibility with mdformat-gfm>=0.3.5 - Fixes pre-commit hook dependency conflict - Resolves CLEANUP_ROADMAP Phase 1.1 - Closes #[issue-number] The previous version (1.0.0) was incompatible with mdformat-gfm plugins, forcing developers to use --no-verify and bypass quality gates. Testing: - ✅ pre-commit run --all-files passes - ✅ mdformat hook executes successfully - ✅ All markdown files formatted correctly`.

- **Directory Case Sensitivity Issues:**
  - To prevent future merge conflicts, standardize directory casing.
  - Consolidate directories to lowercase. Example: Consolidate `Jules` to
    `jules`.
  - Update all workflow references to use the lowercase directory name.
  - Add the uppercase directory name to `.gitignore`.

- **Bypassing Pre-commit Hooks:**
  - If pre-commit hooks are blocking commits, and the changes are minor (e.g.,
    formatting), you may bypass them temporarily using
    `git commit --no-verify -m "commit message"`.
  - **Use this with caution and only for non-functional changes.**

- **Repository Cleanup Guidelines:**
  - When cleaning the remote repository, review all deleted branches one at a
    time to ensure no valuable code is lost.
  - **Cleaning the Remote Repository:**
    1. **List all open PRs:** Use \`gh pr list --state open\` to identify
       currently open pull requests.
    1. **List all remote branches:** Use \`git branch -r\` to identify all
       remote branches.
    1. **Review PRs:** Examine each open PR to determine if it should be merged,
       closed, or requires additional work.
    1. **Review Branches:** Assess each remote branch to determine if it can be
       deleted (e.g., if it has been merged or is stale).
    1. **Close Unnecessary PRs:** Close PRs that are no longer needed,
       especially automated PRs with failing checks.

- **Deleting Remote Branches:**
  - To delete remote branches, use the command: \`git push origin --delete
    branch_name\` for each branch to be deleted.
  - Before deleting, ensure that the branch is not required or that the changes
    have been merged.

- **Verifying Clean State:**
  - To verify a clean state after branch deletion, use: \`git fetch --prune &&
    git branch -r\` to update the local list of remote branches and remove any
    that have been deleted.

- **Handling Commits Ahead:**
  - When a branch appears to be significantly ahead (e.g., 580+ commits),
    investigate to determine the nature of these commits. Often, these commits
    may consist of bulk automated changes rather than unique work.
  - Use \`git reflog --all --date=iso | grep -E "(branch_name)" | head -30\` to
    review the history of the branch.
  - Use \`git show 5e86f6b --stat\` (replace 5e86f6b with the commit id) to
    inspect changes associated with a specific commit.

- **Link Checking**
  - When checking the links in files, use the tool to validate they are working
    and remove any non-functional links.
- **Branch Review and Deletion**
  - Before deleting remote branches, perform a thorough review to prevent data
    loss:
    1.  **List all remote branches:** Use `git branch -r` to identify all remote
        branches.
    2.  **For each remote branch:**
        a.  **Examine the branch's commit history:** Use `git log --oneline
            --graph --decorate -20` or similar to understand the work done.
        b.  **Identify valuable commits:** Check if commits contain unique and
            valuable code or configurations.
        c.  **Cherry-pick or merge:** If valuable commits are found, cherry-pick
            them into the main branch or another appropriate branch.
        d.  **Confirm successful integration:** Verify the changes are now safely
            integrated into the main branch.
        e.  **Delete remote branch:** Use `git push origin --delete branch_name` to
            delete the remote branch.
    3.  **Verify Clean State:** Use `git fetch --prune && git branch -r` to
        update the local list of remote branches and remove any that have been
        deleted.

## FINAL DOs AND DON'Ts

## GitHub Copilot Enhancement Resources

**New to GitHub Copilot customizations?** This organization provides
comprehensive enhancements:

- 📘 [**Quick Start Guide**](../docs/COPILOT_QUICK_START.md) - Get up and running
  in 15 minutes
- 🔧 [**Custom Instructions Setup**](../docs/CUSTOM_INSTRUCTIONS_SETUP.md) -
  Configure coding standards (100+ available)
- 🔌 [**MCP Server Setup**](../docs/MCP_SERVER_SETUP.md) - Extend Copilot with
  Model Context Protocol (11 languages)
- 💻
  [**Development Environment Setup**](../docs/DEVELOPMENT_ENVIRONMENT_SETUP.md)
  \- Optimize your dev environment
- 📚 [**Complete Index**](../docs/COPILOT_ENHANCEMENTS_INDEX.md) - Browse all
  resources

---

The following instructions are only to be applied when performing a code review.

## README updates

- [ ] The new file should be added to the `README.md`.
- [ ] The "Workflow System" section should be updated with the new information.

## Prompt file guide

**Only apply to files that end in `.prompt.md`**

- [ ] The prompt has markdown front matter.
- [ ] The prompt has a `mode` field specified of either \`agent\` or \`ask\`.
- [ ] The prompt has a \`description\` field.
- [ ] The \`description\` field is not empty.
- [ ] The \`description\` field value is wrapped in single quotes.
- [ ] Encourage the use of \`tools\`, but it's not required.
- [ ] Strongly encourage the use of \`model\` to specify the model that the
      prompt is optimised for.

## Instruction file guide

**Only apply to files that end in `.instructions.md`**

- [ ] The instruction has markdown front matter.
- [ ] The instruction has a \`description\` field.
- [ ] The \`description\` field is not empty.
- [ ] The \`description\` field value is wrapped in single quotes.
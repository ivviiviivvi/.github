---

## description: AI rules derived by SpecStory from the project AI interaction history globs: \*

## description: AI rules derived by SpecStory from the project AI interaction history globs: \*

## PROJECT OVERVIEW

## CODE STYLE

## FOLDER ORGANIZATION

- To prevent future merge conflicts, standardize directory casing.
- Consolidate directories to lowercase. Example: Consolidate `Jules` to `jules`.
- Update all workflow references to use the lowercase directory name.
- Add the uppercase directory name to `.gitignore`.

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
- **Semantic Versioning (SemVer):** Use MAJOR.MINOR.PATCH format for versioning:
  - MAJOR version: for incompatible API changes
  - MINOR version: for backwards-compatible functionality additions
  - PATCH version: for backwards-compatible bug fixes

## REFERENCE EXAMPLES

## PROJECT DOCUMENTATION & CONTEXT SYSTEM

- **Schema.org Implementation:** ✅ **DEPLOYED** - Schema.org structured data is
  fully implemented:
  - Schema files located in `.schema-org/` directory
  - Organization, repository, AI framework, and documentation schemas
  - Automated validation via `scripts/validate-schema-org.py`
  - GitHub workflow for continuous validation
  - Version synchronization with semver
  - See [SCHEMA_ORG_SEMVER_GUIDE.md](../docs/SCHEMA_ORG_SEMVER_GUIDE.md) for
    details

- **Semantic Versioning (SemVer):** ✅ **DEPLOYED** - Organization-wide semver
  implementation:
  - VERSION file as source of truth (currently: 1.0.0)
  - package.json with version and scripts
  - Automated version sync via `scripts/sync-version.js`
  - Version bump workflows in GitHub Actions
  - Follows MAJOR.MINOR.PATCH format
  - Conventional commits for version determination
  - See
    [docs/reference/SEMANTIC_VERSIONING.md](../docs/reference/SEMANTIC_VERSIONING.md)

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
       configuration, create an `.eslintrc.eslintrc.json` file:
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

- **Master Org Token Security and Contextual Awareness:**
  - **Issue:** The "master-org-token-011726" personal access token (PAT) is
    being accessed by multiple repositories, raising security and access
    management concerns.
  - **Investigation Steps:**
    1. **Token Identification:** Identify all instances where the
       "master-org-token-011726" or "master-org-personal-access-token" is
       referenced.
    1. **Usage Analysis:** Analyze how the token is being used across the
       organization, including in GitHub workflows, scripts, and documentation.
    1. **Scope Determination:** Determine the scope of the issue by identifying
       all affected repositories and resources.
    1. **Secret Scanning:** Check for organization secrets or repository secrets
       configured with the token.
  - **Resolution Guidelines:**
    - **Comprehensive Analysis Document:** Create a detailed analysis document
      to address the contextual awareness issue, outlining the token's usage,
      affected areas, and proposed solutions.
    - **Token Rotation:** Rotate the "master-org-token-011726" PAT to mitigate
      potential security risks.
    - **Secure Token Storage:** Store tokens securely, preferably in 1Password,
      and limit token scopes to only the necessary permissions.
    - **Access Management Review:** Review and update access management policies
      to ensure proper control over sensitive resources.
  - **Reference Documentation:**
    - See
      [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../docs/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
      for comprehensive analysis
    - See [TOKEN_REGISTRY.md](../docs/TOKEN_REGISTRY.md) for token management
      guidelines
    - **Migration Plan:** Replace single master token with purpose-specific
      tokens by 2026-02-18
    - GitHub Personal Access Tokens (Classic) REQUIRE the Web UI.

- **1Password Authentication Troubleshooting:**
  - **Issue**: 1Password CLI shows as signed in, but still cannot access the
    vault and requires re-authentication.
  - **Root Cause**: Likely due to a missing integration between the 1Password
    CLI and the desktop app, or biometric lock settings.
  - **Solution**:
    1. **Open 1Password Desktop App:** Ensure the 1Password desktop application
       is running.
    1. **Enable CLI Integration:** Go to Settings -> Developer -> "Integrate
       with 1Password CLI" and ensure this option is turned ON.
    1. **Enable Biometric Unlock (Optional):** Enable "Connect with 1Password
       CLI" biometric unlock for added convenience.

- **Pylance Performance Issues**:
  - **Issue**: Pylance language server is continually running and consuming
    excessive resources.
  - **Troubleshooting**:
    1. **Check for Errors**: Use the `copilot_getErrors` tool to identify any
       errors or issues reported by Pylance. High number of errors (e.g. > 500)
       can indicate a configuration or code quality issue.
    1. **Optimize Pylance Settings**: Adjust Pylance settings in
       `.vscode/settings.json` to reduce analysis overhead. The following
       settings are recommended:
       ```json
       {
         "python.analysis.typeCheckingMode": "off", // Disable type checking to reduce overhead
         "python.analysis.diagnosticMode": "openFilesOnly", // Only analyze open files
         "python.analysis.exclude": [
           // Exclude common directories
           "**/node_modules/**",
           "**/__pycache__/**",
           "**/.venv/**",
           "**/dist/**",
           "**/build/**",
           "**/archive/**"
         ],
         "python.analysis.ignore": [
           // Ignore additional paths
           "**/archive/**",
           "**/node_modules/**"
         ],
         "python.analysis.autoSearchPaths": false, // Prevent automatic path searching
         "python.analysis.indexing": true, // Enable indexing
         "python.analysis.memory.keepLibraryAst": false // Reduce memory usage
       }
       ```
    1. **Selective Type Checking**: If type checking is desired, use
       `"python.analysis.typeCheckingMode": "basic"` in conjunction with
       `"python.analysis.diagnosticMode": "openFilesOnly"` for a balanced
       approach.
  - **Resolution Summary**:
    1. **Critical Syntax Errors**: All E9, F63, F7, F82 errors must be fixed.
    1. **Indentation errors**: Ensure all indentation errors are resolved,
       especially in `evaluate_repository.py`.
    1. **Missing imports**: Check and add missing imports, e.g., `Optional` to
       `generate_pilot_workflows.py`, `get_secret` to `validate-tokens.py`.
    1. **Line length violations**: Use Black formatter to reformat code and
       resolve line length issues.
    1. **Unused imports and variables**: Remove unused imports and variables.
    1. **Pylance Optimization**: Apply optimized Pylance settings to reduce
       resource consumption.
  - **Comprehensive Code Cleanup and Formatting**:
    1. **Apply Black Formatter**: Use Black with a line length of 79 characters
       to automatically format Python code and fix line length violations.
    1. **Address F-string Issues**: Remove the `f` prefix from f-strings that do
       not contain placeholders.
    1. **Remove Unused Imports and Variables**: Eliminate unnecessary imports
       and variables to improve code cleanliness.

## FINAL DOs AND DON'Ts

- Since the GitHub CLI token (`GITHUB_TOKEN`) lacks the \`project\` scope needed
  to create organization projects, use a Personal Access Token (PAT) instead.

- Single select options in GitHub Projects require a non-null "description"
  field in the GraphQL API request. Ensure that the script populating the single
  select options include this field. See `configure-github-projects.py` for an
  example.

- When working with the GraphQL API and GitHub Projects, the "Name cannot have a
  reserved value" error can occur if you attempt to create fields that have
  names that are already pre-defined or reserved. Avoid creating fields named
  "Status" or "Type" as these are often pre-defined or reserved.

- To avoid the error where custom field creation fails with "Variable $input of
  type CreateProjectV2FieldInput! was provided invalid value for
  singleSelectOptions.X.description (Expected value to not be null)", ensure
  that the python script includes logic to add an empty description to each
  options: e.g.,

  ```python
  # Add empty description to each option (required by API)
  options_with_desc = [
      {**opt, "description": ""} for opt in options
  ]

  variables = {
      "input": {
          "projectId": project_id,
          "dataType": "SINGLE_SELECT",
          "name": name,
          "singleSelectOptions": options_with_desc
  ```

- Here's the updated `PROJECTS_CONFIG` section in the
  `configure-github-projects.py` file:

  ```python
  # Project configurations
  PROJECTS_CONFIG = {
      "ai-framework": {
          "title": "🤖 AI Framework Development",
          "description": """Development and maintenance of the AI framework including:
  - 26+ specialized agents
  - MCP servers for 11 programming languages
  - 100+ custom instructions
  - Chat modes and collections
  - Automated tracking of agent lifecycle, testing, and deployment

  **Key Areas:**
  - Agent development and testing
  - MCP server implementation
  - Custom instructions authoring
  - Chat mode configuration
  - Framework enhancements and bug fixes""",
          "fields": {
              "Status": {
                  "type": "single_select",
                  "options": [
                      {"name": "🎯 Planned", "color": "GRAY", "description": ""},
                      {"name": "🔬 Research", "color": "BLUE", "description": ""},
                      {"name": "🏗️ In Development", "color": "YELLOW", "description": ""},
                      {"name": "🧪 Testing", "color": "ORANGE", "description": ""},
                      {"name": "👀 Code Review", "color": "PURPLE", "description": ""},
                      {"name": "✅ Ready to Deploy", "color": "GREEN", "description": ""},
                      {"name": "🚀 Deployed", "color": "GREEN", "description": ""},
                      {"name": "📝 Documentation", "color": "BLUE", "description": ""},
                      {"name": "⏸️ On Hold", "color": "GRAY", "description": ""},
                      {"name": "✔️ Completed", "color": "GREEN", "description": ""}
                  ]
              },
              "Priority": {
                  "type": "single_select",
                  "options": [
                      {"name": "🔥 Critical", "color": "RED", "description": ""},
                      {"name": "⚡ High", "color": "ORANGE", "description": ""},
                      {"name": "📊 Medium", "color": "YELLOW", "description": ""},
                      {"name": "🔽 Low", "color": "GRAY", "description": ""}
                  ]
              },
              "Type": {
                  "type": "single_select",
                  "options": [
                      {"name": "🤖 Agent", "color": "PURPLE", "description": ""},
                      {"name": "🔌 MCP Server", "color": "BLUE", "description": ""},
                      {"name": "📋 Custom Instructions", "color": "GREEN", "description": ""},
                      {"name": "💬 Chat Mode", "color": "PINK", "description": ""},
                      {"name": "📦 Collection", "color": "ORANGE", "description": ""},
                      {"name": "🔧 Framework Enhancement", "color": "YELLOW", "description": ""},
                      {"name": "🐛 Bug Fix", "color": "RED", "description": ""}
                  ]
              },
              "Language": {
                  "type": "single_select",
                  "options": [
                      {"name": "Python", "color": "BLUE", "description": ""},
                      {"name": "TypeScript", "color": "BLUE", "description": ""},
                      {"name": "Java", "color": "RED", "description": ""},
                      {"name": "C#", "color": "PURPLE", "description": ""},
                      {"name": "Go", "color": "BLUE", "description": ""},
                      {"name": "Rust", "color": "ORANGE", "description": ""}
                  ]
              },
              "Complexity": {
                  "type": "single_select",
                  "options": [
                      {"name": "🟢 Simple", "color": "GREEN", "description": ""},
                      {"name": "🟡 Moderate", "color": "YELLOW", "description": ""},
                      {"name": "🟠 Complex", "color": "ORANGE", "description": ""},
                      {"name": "🔴 Major", "color": "RED", "description": ""}
                  ]
              },
              "Dependencies": {"type": "text"},
              "Testing Status": {
                  "type": "single_select",
                  "options": [
                      {"name": "⏳ Not Started", "color": "GRAY", "description": ""},
                      {"name": "🧪 Unit Tests", "color": "YELLOW", "description": ""},
                      {"name": "🔗 Integration Tests", "color": "ORANGE", "description": ""},
                      {"name": "✅ All Tests Passing", "color": "GREEN", "description": ""}
                  ]
              }
          }
      },
      "documentation": {
          "title": "📚 Documentation &amp; Knowledge",
          "description": """Documentation ecosystem management across 133+ files:
  - Setup guides and quick starts
  - Architecture documentation
  - API references and technical guides
  - Tutorials and learning resources
  - Policy documents

  **Coverage:**
  - Core organizational policies
  - Workflow system documentation
  - AI framework guides
  - Development environment setup
  - Security and compliance docs""",
          "fields": {
              "Status": {
                  "type": "single_select",
                  "options": [
                      {"name": "📋 Backlog", "color": "GRAY", "description": ""},
                      {"name": "✍️ Writing", "color": "YELLOW", "description": ""},
                      {"name": "👀 Review", "color": "ORANGE", "description": ""},
                      {"name": "🔄 Revision", "color": "BLUE", "description": ""},
                      {"name": "✅ Approved", "color": "GREEN", "description": ""},
                      {"name": "📤 Published", "color": "GREEN", "description": ""},
                      {"name": "🔄 Needs Update", "color": "RED", "description": ""}
                  ]
              },
              "Priority": {
                  "type": "single_select",
                  "options": [
                      {"name": "🔥 Urgent", "color": "RED", "description": ""},
                      {"name": "⚡ High", "color": "ORANGE", "description": ""},
                      {"name": "📊 Medium", "color": "YELLOW", "description": ""},
                      {"name": "🔽 Low", "color": "GRAY", "description": ""}
                  ]
              },
              "Document Type": {
                  "type": "single_select",
                  "options": [
                      {"name": "📖 Guide", "color": "BLUE", "description": ""},
                      {"name": "🏛️ Architecture", "color": "PURPLE", "description": ""},
                      {"name": "🔧 Technical Reference", "color": "ORANGE", "description": ""},
                      {"name": "📚 Tutorial", "color": "GREEN", "description": ""},
                      {"name": "📋 Policy", "color": "RED", "description": ""},
                      {"name": "🎯 Quick Start", "color": "YELLOW", "description": ""}
                  ]
              },
              "Completeness": {
                  "type": "single_select",
                  "options": [
                      {"name": "🔴 Outline Only", "color": "RED", "description": ""},
                      {"name": "🟡 Draft", "color": "YELLOW", "description": ""},
                      {"name": "🟢 Complete", "color": "GREEN", "description": ""},
                      {"name": "⭐ Comprehensive", "color": "GREEN", "description": ""}
                  ]
              },
              "Last Updated": {"type": "date"},
              "Next Review Date": {"type": "date"},
              "Word Count": {"type": "number"}
          }
      }
  }
  ```

- **Master Org Token Security and Contextual Awareness:**
  - **Issue:** The "master-org-token-011726" personal access token (PAT) is
    being accessed by multiple repositories, raising security and access
    management concerns.
  - **Investigation Steps:**
    1. **Token Identification:** Identify all instances where the
       "master-org-token-011726" or "master-org-personal-access-token" is
       referenced.
    1. **Usage Analysis:** Analyze how the token is being used across the
       organization, including in GitHub workflows, scripts, and documentation.
    1. **Scope Determination:** Determine the scope of the issue by identifying
       all affected repositories and resources.
    1. **Secret Scanning:** Check for organization secrets or repository secrets
       configured with the token.
  - **Resolution Guidelines:**
    - **Comprehensive Analysis Document:** Create a detailed analysis document
      to address the contextual awareness issue, outlining the token's usage,
      affected areas, and proposed solutions.
    - **Token Rotation:** Rotate the "master-org-token-011726" PAT to mitigate
      potential security risks.
    - **Secure Token Storage:** Store tokens securely, preferably in 1Password,
      and limit token scopes to only the necessary permissions.
    - **Access Management Review:** Review and update access management policies
      to ensure proper control over sensitive resources.
  - **Reference Documentation:**
    - See
      [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../docs/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
      for comprehensive analysis
    - See [TOKEN_REGISTRY.md](../docs/TOKEN_REGISTRY.md) for token management
      guidelines
    - **Migration Plan:** Replace single master token with purpose-specific
      tokens by 2026-02-18
    - GitHub Personal Access Tokens (Classic) REQUIRE the Web UI.

- **Pylance Performance Issues**:
  - **Issue**: Pylance language server is continually running and consuming
    excessive resources.
  - **Troubleshooting**:
    1. **Check for Errors**: Use the `copilot_getErrors` tool to identify any
       errors or issues reported by Pylance. High number of errors (e.g. > 500)
       can indicate a configuration or code quality issue.
    1. **Optimize Pylance Settings**: Adjust Pylance settings in
       `.vscode/settings.json` to reduce analysis overhead. The following
       settings are recommended:
       ```json
       {
         "python.analysis.typeCheckingMode": "off", // Disable type checking to reduce overhead
         "python.analysis.diagnosticMode": "openFilesOnly", // Only analyze open files
         "python.analysis.exclude": [
           // Exclude common directories
           "**/node_modules/**",
           "**/__pycache__/**",
           "**/.venv/**",
           "**/dist/**",
           "**/build/**",
           "**/archive/**"
         ],
         "python.analysis.ignore": [
           // Ignore additional paths
           "**/archive/**",
           "**/node_modules/**"
         ],
         "python.analysis.autoSearchPaths": false, // Prevent automatic path searching
         "python.analysis.indexing": true, // Enable indexing
         "python.analysis.memory.keepLibraryAst": false // Reduce memory usage
       }
       ```
    1. **Selective Type Checking**: If type checking is desired, use
       `"python.analysis.typeCheckingMode": "basic"` in conjunction with
       `"python.analysis.diagnosticMode": "openFilesOnly"` for a balanced
       approach.
  - **Resolution Summary**:
    1. **Critical Syntax Errors**: All E9, F63, F7, F82 errors must be fixed.
    1. **Indentation errors**: Ensure all indentation errors are resolved,
       especially in `evaluate_repository.py`.
    1. **Missing imports**: Check and add missing imports, e.g., `Optional` to
       `generate_pilot_workflows.py`, `get_secret` to `validate-tokens.py`.
    1. **Line length violations**: Use Black formatter to reformat code and
       resolve line length issues.
    1. **Unused imports and variables**: Remove unused imports and variables.
    1. **Pylance Optimization**: Apply optimized Pylance settings to reduce
       resource consumption.
  - **Comprehensive Code Cleanup and Formatting**:
    1. **Apply Black Formatter**: Use Black with a line length of 79 characters
       to automatically format Python code and fix line length violations.
    1. **Address F-string Issues**: Remove the `f` prefix from f-strings that do
       not contain placeholders.
    1. **Remove Unused Imports and Variables**: Eliminate unnecessary imports
       and variables to improve code cleanliness.

## FINAL DOs AND DON'Ts

- Since the GitHub CLI token (`GITHUB_TOKEN`) lacks the \`project\` scope needed
  to create organization projects, use a Personal Access Token (PAT) instead.

- Single select options in GitHub Projects require a non-null "description"
  field in the GraphQL API request. Ensure that the script populating the single
  select options include this field. See `configure-github-projects.py` for an
  example.

- When working with the GraphQL API and GitHub Projects, the "Name cannot have a
  reserved value" error can occur if you attempt to create fields that have
  names that are already pre-defined or reserved. Avoid creating fields named
  "Status" or "Type" as these are often pre-defined or reserved.

- To avoid the error where custom field creation fails with "Variable $input of
  type CreateProjectV2FieldInput! was provided invalid value for
  singleSelectOptions.X.description (Expected value to not be null)", ensure
  that the python script includes logic to add an empty description to each
  options: e.g.,

  ```python
  # Add empty description to each option (required by API)
  options_with_desc = [
      {**opt, "description": ""} for opt in options
  ]

  variables = {
      "input": {
          "projectId": project_id,
          "dataType": "SINGLE_SELECT",
          "name": name,
          "singleSelectOptions": options_with_desc
  ```

- Here's the updated `PROJECTS_CONFIG` section in the
  `configure-github-projects.py` file:

  ```python
  # Project configurations
  PROJECTS_CONFIG = {
      "ai-framework": {
          "title": "🤖 AI Framework Development",
          "description": """Development and maintenance of the AI framework including:
  - 26+ specialized agents
  - MCP servers for 11 programming languages
  - 100+ custom instructions
  - Chat modes and collections
  - Automated tracking of agent lifecycle, testing, and deployment

  **Key Areas:**
  - Agent development and testing
  - MCP server implementation
  - Custom instructions authoring
  - Chat mode configuration
  - Framework enhancements and bug fixes""",
          "fields": {
              "Status": {
                  "type": "single_select",
                  "options": [
                      {"name": "🎯 Planned", "color": "GRAY", "description": ""},
                      {"name": "🔬 Research", "color": "BLUE", "description": ""},
                      {"name": "🏗️ In Development", "color": "YELLOW", "description": ""},
                      {"name": "🧪 Testing", "color": "ORANGE", "description": ""},
                      {"name": "👀 Code Review", "color": "PURPLE", "description": ""},
                      {"name": "✅ Ready to Deploy", "color": "GREEN", "description": ""},
                      {"name": "🚀 Deployed", "color": "GREEN", "description": ""},
                      {"name": "📝 Documentation", "color": "BLUE", "description": ""},
                      {"name": "⏸️ On Hold", "color": "GRAY", "description": ""},
                      {"name": "✔️ Completed", "color": "GREEN", "description": ""}
                  ]
              },
              "Priority": {
                  "type": "single_select",
                  "options": [
                      {"name": "🔥 Critical", "color": "RED", "description": ""},
                      {"name": "⚡ High", "color": "ORANGE", "description": ""},
                      {"name": "📊 Medium", "color": "YELLOW", "description": ""},
                      {"name": "🔽 Low", "color": "GRAY", "description": ""}
                  ]
              },
              "Type": {
                  "type": "single_select",
                  "options": [
                      {"name": "🤖 Agent", "color": "PURPLE", "description": ""},
                      {"name": "🔌 MCP Server", "color": "BLUE", "description": ""},
                      {"name": "📋 Custom Instructions", "color": "GREEN", "description": ""},
                      {"name": "💬 Chat Mode", "color": "PINK", "description": ""},
                      {"name": "📦 Collection", "color": "ORANGE", "description": ""},
                      {"name": "🔧 Framework Enhancement", "color": "YELLOW", "description": ""},
                      {"name": "🐛 Bug Fix", "color": "RED", "description": ""}
                  ]
              },
              "Language": {
                  "type": "single_select",
                  "options": [
                      {"name": "Python", "color": "BLUE", "description": ""},
                      {"name": "TypeScript", "color": "BLUE", "description": ""},
                      {"name
  ```

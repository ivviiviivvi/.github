"""Regression tests for repository-owned workflow policy contracts."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


def read(path: Path) -> str:
    """Return a repository text file."""
    return path.read_text(encoding="utf-8")


def test_changed_workflows_are_valid_yaml():
    """Every repaired workflow must remain syntactically valid YAML."""
    paths = [
        WORKFLOWS / "auto-pr-create.yml",
        WORKFLOWS / "demo-deployment.yml",
        WORKFLOWS / "gemini-review.yml",
        WORKFLOWS / "orchestrator.yml",
        WORKFLOWS / "pr-quality-checks.yml",
        WORKFLOWS / "pr-title-lint.yml",
        WORKFLOWS / "proactive-maintenance.yml",
        WORKFLOWS / "repository-bootstrap.yml",
        WORKFLOWS / "reusable" / "pr-batching.yml",
        WORKFLOWS / "version-control-standards.yml",
        WORKFLOWS / "welcome.yml",
    ]

    for path in paths:
        assert isinstance(yaml.safe_load(read(path)), dict), path


def test_first_interaction_uses_current_input_names():
    """The pinned first-interaction action exposes underscore input names."""
    workflow = read(WORKFLOWS / "welcome.yml")

    assert "repo_token:" in workflow
    assert "issue_message:" in workflow
    assert "pr_message:" in workflow
    assert "repo-token:" not in workflow
    assert "issue-message:" not in workflow
    assert "pr-message:" not in workflow


def test_automation_has_no_pr_title_or_branch_bypass():
    """Autonomous changes satisfy the same policy contract as human changes."""
    title_workflows = "\n".join(
        read(path)
        for path in [
            WORKFLOWS / "pr-title-lint.yml",
            WORKFLOWS / "pr-quality-checks.yml",
        ]
    )
    standards = read(WORKFLOWS / "version-control-standards.yml")

    assert "startsWith(github.event.pull_request.title, '[limen ')" not in title_workflows
    assert '"^limen/' not in standards
    assert "Skipping commit message validation for Limen" not in standards


def test_repo_owned_pr_producers_emit_compliant_metadata():
    """Repository-owned PR producers use conventional titles and branch shapes."""
    expected = {
        WORKFLOWS / "repository-bootstrap.yml": [
            'BRANCH_NAME="maintenance/chore/workflow-templates-',
            '--title "chore(workflows): add workflow templates"',
        ],
        WORKFLOWS / "orchestrator.yml": [
            'DAILY_BRANCH="maintenance/chore/daily-batch-',
            '--title "chore(automation): collect daily batch updates for ',
        ],
        WORKFLOWS / "proactive-maintenance.yml": [
            'BRANCH="maintenance/chore/dependency-updates-',
            '--title "chore(deps): update dependencies"',
        ],
        WORKFLOWS / "reusable" / "pr-batching.yml": [
            "default: maintenance/chore/",
            "title: `chore(automation): batch ${included.length} pull requests`,",
        ],
        ROOT / "src" / "automation" / "scripts" / "bootstrap-walkthrough-org.sh": [
            'branch_name="develop/feature/add-video-walkthrough-',
            '--title "feat(workflows): add video walkthrough generation"',
        ],
    }

    for path, fragments in expected.items():
        contents = read(path)
        for fragment in fragments:
            assert fragment in contents, (path, fragment)


def test_optional_gemini_review_skips_before_cli_without_auth():
    """Missing optional provider auth must not create a permanently red check."""
    workflow = read(WORKFLOWS / "gemini-review.yml")

    assert "id: gemini-availability" in workflow
    assert 'echo "available=false" >> "$GITHUB_OUTPUT"' in workflow
    assert "if: steps.gemini-availability.outputs.available == 'true'" in workflow
    assert "Optional review skipped: ${REASON}." in workflow


def test_batch_pr_outputs_enter_github_script_through_environment():
    """PR-controlled output cannot be interpolated into executable JavaScript."""
    workflow = read(WORKFLOWS / "reusable" / "pr-batching.yml")

    assert "INCLUDED_PRS: ${{ steps.create-batch.outputs.included }}" in workflow
    assert "JSON.parse(process.env.INCLUDED_PRS || '[]')" in workflow
    assert "JSON.parse('${{ steps.create-batch.outputs.included }}')" not in workflow


def test_volatile_agent_logs_are_local_runtime_state():
    """Ephemeral agent heartbeats cannot become product diffs."""
    assert "/logs/agents/" in read(ROOT / ".gitignore")


def test_dependency_review_uses_supported_action_inputs():
    """The dependency-review action receives only supported policy inputs."""
    workflow = read(WORKFLOWS / "dependency-review.yml")

    assert "deny-licenses:" not in workflow
    assert "warn-on-deprecated:" not in workflow


def test_demo_push_and_manual_inputs_preserve_reusable_workflow_types():
    """Push defaults and manual booleans must remain correctly typed at the call boundary."""
    workflow = read(WORKFLOWS / "demo-deployment.yml")

    assert "github.event.inputs['app-type']" in workflow
    assert "github.event.inputs['hosting-provider']" in workflow
    assert (
        "inject-badge: ${{ github.event_name != 'workflow_dispatch' || github.event.inputs['inject-badge'] == 'true' }}"
    ) in workflow
    assert "${{ inputs.app-type" not in workflow
    assert "${{ inputs.hosting-provider" not in workflow
    assert "&& github.event.inputs['inject-badge'] || true" not in workflow


def test_link_checker_ignore_patterns_are_valid_regexes():
    """Template placeholders must not make Lychee abort before checking links."""
    ignore_file = read(ROOT / ".config" / ".lycheeignore")

    for line in ignore_file.splitlines():
        pattern = line.strip()
        if pattern and not pattern.startswith("#"):
            re.compile(pattern)


def test_link_checker_handles_symlinks_and_disabled_assets_truthfully():
    """The full-doc scan must not resolve known aliases to impossible paths."""
    workflow = read(WORKFLOWS / "link-checker.yml")
    monitoring = read(ROOT / "docs" / "guides" / "monitoring.md")
    chatmodes = read(ROOT / "docs" / "guides" / "README.chatmodes.md")

    assert "--exclude-path 'CONTRIBUTING.md'" in workflow
    assert "if: vars.ENABLE_MARKDOWN_LINK_CHECKS == 'true'" in workflow
    assert "if: vars.ENABLE_SPELL_CHECK == 'true'" in workflow
    assert "metrics-collection.yml.disabled" in monitoring
    assert "csharp-dotnet-janitor.chatmode.md" in chatmodes
    assert "csharp-dotnet-codebase-cleanup.chatmode.md" not in chatmodes

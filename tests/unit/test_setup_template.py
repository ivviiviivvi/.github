"""Tests for setup_template.py — config parsing, count computation, replacement."""

import pytest
import yaml

from src.automation.scripts.setup_template import (
    build_variable_map,
    compute_dynamic_counts,
    is_jinja_line,
    load_config,
    replace_in_content,
    validate_remaining_placeholders,
)


@pytest.fixture
def tmp_repo(tmp_path):
    """Create a minimal repo structure for testing."""
    # Config file
    config_dir = tmp_path / ".config"
    config_dir.mkdir()
    config = {
        "org": {
            "name": "acme-corp",
            "display_name": "Acme Corporation",
            "website": "https://acme.example.com",
            "email_domain": "acme.example.com",
        },
        "repo": {"name": ".github", "npm_scope": "acme-corp"},
        "social": {"discord_invite": "acme123"},
        "product": {"name": "AcmeBot", "api_endpoint": "https://api.acme.example.com"},
        "teams": {
            "leadership": "leads",
            "engineering": "eng",
            "devops": "ops",
            "security": "sec",
        },
    }
    (config_dir / "template-config.yml").write_text(yaml.dump(config))

    # Workflows
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    for i in range(3):
        (wf_dir / f"wf-{i}.yml").write_text(f"name: workflow-{i}\n")
    reusable_dir = wf_dir / "reusable"
    reusable_dir.mkdir()
    (reusable_dir / "shared.yml").write_text("name: shared\n")

    # AI framework
    ai_dir = tmp_path / "src" / "ai_framework"
    (ai_dir / "agents").mkdir(parents=True)
    (ai_dir / "agents" / "bot.agent.md").write_text("# Agent\n")
    (ai_dir / "chatmodes").mkdir()
    (ai_dir / "chatmodes" / "helper.chatmode.md").write_text("# Chatmode\n")
    (ai_dir / "chatmodes" / "coder.chatmode.md").write_text("# Chatmode\n")
    (ai_dir / "prompts").mkdir()
    (ai_dir / "prompts" / "review.prompt.md").write_text("# Prompt\n")
    (ai_dir / "collections").mkdir()
    (ai_dir / "collections" / "default.collection.yml").write_text("name: default\n")

    # Scripts
    scripts_dir = tmp_path / "src" / "automation" / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "foo.py").write_text("print('hello')\n")
    (scripts_dir / "bar.py").write_text("print('world')\n")
    (scripts_dir / "__init__.py").write_text("")

    return tmp_path


@pytest.mark.unit
class TestLoadConfig:
    def test_loads_valid_config(self, tmp_repo):
        config = load_config(tmp_repo / ".config" / "template-config.yml")
        assert config["org"]["name"] == "acme-corp"
        assert config["teams"]["engineering"] == "eng"

    def test_missing_config_exits(self, tmp_path):
        with pytest.raises(SystemExit):
            load_config(tmp_path / "nonexistent.yml")


@pytest.mark.unit
class TestComputeDynamicCounts:
    def test_counts_match(self, tmp_repo):
        counts = compute_dynamic_counts(tmp_repo)
        assert counts["WORKFLOW_COUNT"] == "4"  # 3 standard + 1 reusable
        assert counts["REUSABLE_TEMPLATE_COUNT"] == "1"
        assert counts["AGENT_COUNT"] == "1"
        assert counts["CHATMODE_COUNT"] == "2"
        assert counts["PROMPT_COUNT"] == "1"
        assert counts["COLLECTION_COUNT"] == "1"
        assert counts["SCRIPT_COUNT"] == "2"  # excludes __init__.py

    def test_empty_repo(self, tmp_path):
        counts = compute_dynamic_counts(tmp_path)
        assert counts["WORKFLOW_COUNT"] == "0"
        assert counts["AGENT_COUNT"] == "0"
        assert counts["SCRIPT_COUNT"] == "0"


@pytest.mark.unit
class TestBuildVariableMap:
    def test_static_and_derived_vars(self, tmp_repo):
        config = load_config(tmp_repo / ".config" / "template-config.yml")
        counts = compute_dynamic_counts(tmp_repo)
        variables = build_variable_map(config, counts)

        assert variables["ORG_NAME"] == "acme-corp"
        assert variables["ORG_DISPLAY_NAME"] == "Acme Corporation"
        assert variables["ORG_GITHUB_URL"] == "https://github.com/acme-corp"
        assert variables["ORG_GITHUB_IO_URL"] == "https://acme-corp.github.io"
        assert variables["WORKFLOW_COUNT"] == "4"
        assert variables["TEAM_DEVOPS"] == "ops"

    def test_unconfigured_defaults(self):
        config = {"org": {"name": "{{ORG_NAME}}"}}
        counts = {"WORKFLOW_COUNT": "10"}
        variables = build_variable_map(config, counts)
        assert variables["ORG_NAME"] == "{{ORG_NAME}}"
        assert variables["WORKFLOW_COUNT"] == "10"


@pytest.mark.unit
class TestReplaceInContent:
    def test_basic_replacement(self):
        content = "Welcome to {{ORG_NAME}}! Visit {{ORG_WEBSITE}}."
        variables = {"ORG_NAME": "acme", "ORG_WEBSITE": "https://acme.com"}
        result = replace_in_content(content, variables)
        assert result == "Welcome to acme! Visit https://acme.com."

    def test_counts_only_mode(self):
        content = "We have {{WORKFLOW_COUNT}} workflows by {{ORG_NAME}}."
        variables = {"WORKFLOW_COUNT": "50", "ORG_NAME": "acme"}
        result = replace_in_content(content, variables, counts_only=True)
        assert result == "We have 50 workflows by {{ORG_NAME}}."

    def test_preserves_jinja_syntax(self):
        content = "{{change_type}}({{scope}}): {{message}}"
        variables = {"ORG_NAME": "acme"}
        result = replace_in_content(content, variables)
        assert result == content  # unchanged

    def test_multiple_per_line(self):
        content = "{{ORG_NAME}}/{{REPO_NAME}} at {{ORG_WEBSITE}}"
        variables = {"ORG_NAME": "acme", "REPO_NAME": ".github", "ORG_WEBSITE": "https://acme.com"}
        result = replace_in_content(content, variables)
        assert result == "acme/.github at https://acme.com"


@pytest.mark.unit
class TestIsJinjaLine:
    def test_commitizen_template(self):
        assert is_jinja_line("{{change_type}}({{scope}}): {{message}}")

    def test_normal_placeholder(self):
        assert not is_jinja_line("Welcome to {{ORG_NAME}}")


@pytest.mark.unit
class TestValidateRemainingPlaceholders:
    def test_finds_unreplaced(self, tmp_repo):
        test_file = tmp_repo / "README.md"
        test_file.write_text("# Welcome to {{ORG_NAME}}\nVisit {{ORG_WEBSITE}}.\n")
        results = validate_remaining_placeholders(tmp_repo)
        placeholders = {r[2] for r in results}
        assert "{{ORG_NAME}}" in placeholders
        assert "{{ORG_WEBSITE}}" in placeholders

    def test_ignores_non_template_vars(self, tmp_repo):
        test_file = tmp_repo / "workflow.yml"
        test_file.write_text("run: echo {{RANDOM_THING}}\n")
        results = validate_remaining_placeholders(tmp_repo)
        placeholders = {r[2] for r in results}
        assert "{{RANDOM_THING}}" not in placeholders

    def test_clean_repo(self, tmp_repo):
        # No files with known placeholders
        results = validate_remaining_placeholders(tmp_repo)
        # Only the config file itself has placeholders, and it's excluded
        found_vars = {r[2] for r in results}
        # The config file is excluded, so there should be no results from fixtures
        # (tmp_repo files don't contain our known placeholders)
        assert len(found_vars) == 0

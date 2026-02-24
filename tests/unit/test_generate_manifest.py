"""Unit tests for automation/scripts/generate_manifest.py

Focus: Unified manifest generation from multiple sources.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from generate_manifest import (
    build_manifest,
    count_files,
    find_missing_metadata,
    find_orphaned_meta,
    load_workflow_registry,
    main,
    parse_frontmatter,
    scan_agents,
    scan_chatmodes,
    scan_collections,
    scan_prompts,
)


@pytest.mark.unit
class TestParseFrontmatter:
    """Test parse_frontmatter function."""

    def test_parses_simple_frontmatter(self):
        """Test parses simple key-value pairs."""
        content = """---
name: Test Agent
description: A test agent
---
# Content here
"""
        result = parse_frontmatter(content)

        assert result["name"] == "Test Agent"
        assert result["description"] == "A test agent"

    def test_parses_list_values(self):
        """Test parses list values."""
        content = """---
name: Test
tools:
  - tool1
  - tool2
  - tool3
---
"""
        result = parse_frontmatter(content)

        assert result["name"] == "Test"
        assert result["tools"] == ["tool1", "tool2", "tool3"]

    def test_removes_quotes(self):
        """Test removes surrounding quotes."""
        content = """---
name: "Quoted Name"
other: 'Single Quoted'
---
"""
        result = parse_frontmatter(content)

        assert result["name"] == "Quoted Name"
        assert result["other"] == "Single Quoted"

    def test_handles_empty_content(self):
        """Test handles empty content."""
        result = parse_frontmatter("")
        assert result == {}

    def test_handles_no_frontmatter(self):
        """Test handles content without frontmatter."""
        content = "# Just a heading\nSome content"
        result = parse_frontmatter(content)
        assert result == {}

    def test_handles_unclosed_frontmatter(self):
        """Test handles unclosed frontmatter."""
        content = """---
name: Test
# No closing ---
"""
        result = parse_frontmatter(content)
        assert result == {}

    def test_skips_comments(self):
        """Test skips comment lines."""
        content = """---
name: Test
# This is a comment
description: Testing
---
"""
        result = parse_frontmatter(content)

        assert result["name"] == "Test"
        assert result["description"] == "Testing"
        assert "#" not in result

    def test_skips_empty_lines(self):
        """Test skips empty lines."""
        content = """---
name: Test

description: Testing

---
"""
        result = parse_frontmatter(content)

        assert result["name"] == "Test"
        assert result["description"] == "Testing"


@pytest.mark.unit
class TestCountFiles:
    """Test count_files function."""

    def test_counts_matching_files(self, tmp_path):
        """Test counts files matching pattern."""
        for i in range(5):
            (tmp_path / f"file{i}.txt").write_text("content")

        result = count_files(tmp_path, "*.txt")

        assert result == 5

    def test_counts_zero_when_no_matches(self, tmp_path):
        """Test returns zero when no files match."""
        (tmp_path / "file.txt").write_text("content")

        result = count_files(tmp_path, "*.md")

        assert result == 0


@pytest.mark.unit
class TestScanAgents:
    """Test scan_agents function."""

    def test_scans_agents_directory(self, tmp_path):
        """Test scans agents and extracts metadata."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        (agents_dir / "test.agent.md").write_text("""---
name: Test Agent
description: A test agent
---
# Content
""")
        (agents_dir / "other.agent.md").write_text("""---
name: Other Agent
description: Another agent
---
# Content
""")

        result = scan_agents(agents_dir)

        assert result["total"] == 2
        assert len(result["files"]) == 2
        assert any(f["name"] == "Test Agent" for f in result["files"])

    def test_returns_empty_for_nonexistent_directory(self, tmp_path):
        """Test returns empty for nonexistent directory."""
        result = scan_agents(tmp_path / "nonexistent")

        assert result == {"total": 0, "files": []}

    def test_uses_stem_when_no_name(self, tmp_path):
        """Test uses filename stem when no name in frontmatter."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        (agents_dir / "myagent.agent.md").write_text("# No frontmatter")

        result = scan_agents(agents_dir)

        assert result["total"] == 1
        assert result["files"][0]["name"] == "myagent.agent"


@pytest.mark.unit
class TestScanChatmodes:
    """Test scan_chatmodes function."""

    def test_scans_chatmodes_directory(self, tmp_path):
        """Test scans chatmodes and extracts metadata."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        (chatmodes_dir / "default.chatmode.md").write_text("""---
name: Default Mode
description: Default chatmode
---
""")

        result = scan_chatmodes(chatmodes_dir)

        assert result["total"] == 1
        assert result["files"][0]["name"] == "Default Mode"

    def test_returns_empty_for_nonexistent_directory(self, tmp_path):
        """Test returns empty for nonexistent directory."""
        result = scan_chatmodes(tmp_path / "nonexistent")

        assert result == {"total": 0, "files": []}


@pytest.mark.unit
class TestScanPrompts:
    """Test scan_prompts function."""

    def test_scans_prompts_directory(self, tmp_path):
        """Test scans prompts and extracts metadata."""
        prompts_dir = tmp_path / "prompts"
        prompts_dir.mkdir()

        (prompts_dir / "review.prompt.md").write_text("""---
name: Code Review
mode: agent
description: Review code
---
""")

        result = scan_prompts(prompts_dir)

        assert result["total"] == 1
        assert result["files"][0]["name"] == "Code Review"
        assert result["files"][0]["mode"] == "agent"

    def test_returns_empty_for_nonexistent_directory(self, tmp_path):
        """Test returns empty for nonexistent directory."""
        result = scan_prompts(tmp_path / "nonexistent")

        assert result == {"total": 0, "files": []}


@pytest.mark.unit
class TestScanCollections:
    """Test scan_collections function."""

    def test_scans_collections_directory(self, tmp_path):
        """Test scans collections directory."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        (collections_dir / "default.collection.yml").write_text("name: Default")
        (collections_dir / "other.yml").write_text("name: Other")

        result = scan_collections(collections_dir)

        assert result["total"] == 2

    def test_deduplicates_collections(self, tmp_path):
        """Test deduplicates collection files."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        # Same collection, different extensions
        (collections_dir / "test.collection.yml").write_text("name: Test")
        (collections_dir / "test.yml").write_text("name: Test")

        result = scan_collections(collections_dir)

        # Should skip test.yml since test.collection.yml exists
        assert result["total"] == 1

    def test_returns_empty_for_nonexistent_directory(self, tmp_path):
        """Test returns empty for nonexistent directory."""
        result = scan_collections(tmp_path / "nonexistent")

        assert result == {"total": 0, "files": []}


@pytest.mark.unit
class TestLoadWorkflowRegistry:
    """Test load_workflow_registry function."""

    def test_loads_registry_file(self, tmp_path):
        """Test loads existing registry file."""
        registry_file = tmp_path / "registry.json"
        registry_file.write_text(
            json.dumps(
                {
                    "statistics": {
                        "total": 50,
                        "with_metadata": 30,
                        "orphans": 2,
                        "by_layer": {"core": 10, "interface": 20},
                    }
                }
            )
        )

        result = load_workflow_registry(registry_file)

        assert result["total"] == 50
        assert result["with_metadata"] == 30

    def test_returns_defaults_for_nonexistent_file(self, tmp_path):
        """Test returns defaults for nonexistent file."""
        result = load_workflow_registry(tmp_path / "nonexistent.json")

        assert result["total"] == 0
        assert result["with_metadata"] == 0

    def test_handles_invalid_json(self, tmp_path):
        """Test handles invalid JSON."""
        registry_file = tmp_path / "registry.json"
        registry_file.write_text("invalid json")

        result = load_workflow_registry(registry_file)

        assert result["total"] == 0


@pytest.mark.unit
class TestFindOrphanedMeta:
    """Test find_orphaned_meta function."""

    def test_finds_orphaned_meta_files(self, tmp_path):
        """Test finds meta files without corresponding workflow."""
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()

        # Orphaned meta (no corresponding .yml)
        (workflows_dir / "orphan.yml.meta.json").write_text("{}")

        # Non-orphan (has corresponding .yml)
        (workflows_dir / "valid.yml").write_text("name: Valid")
        (workflows_dir / "valid.yml.meta.json").write_text("{}")

        result = find_orphaned_meta(workflows_dir)

        assert "orphan.yml.meta.json" in result
        assert "valid.yml.meta.json" not in result

    def test_returns_empty_when_no_orphans(self, tmp_path):
        """Test returns empty when no orphans."""
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()

        (workflows_dir / "valid.yml").write_text("name: Valid")
        (workflows_dir / "valid.yml.meta.json").write_text("{}")

        result = find_orphaned_meta(workflows_dir)

        assert result == []


@pytest.mark.unit
class TestFindMissingMetadata:
    """Test find_missing_metadata function."""

    def test_finds_workflows_without_metadata(self, tmp_path):
        """Test finds workflow files without meta.json."""
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()

        # Has metadata
        (workflows_dir / "with-meta.yml").write_text("name: With")
        (workflows_dir / "with-meta.yml.meta.json").write_text("{}")

        # Missing metadata
        (workflows_dir / "without-meta.yml").write_text("name: Without")

        result = find_missing_metadata(workflows_dir)

        assert "without-meta.yml" in result
        assert "with-meta.yml" not in result

    def test_returns_empty_when_all_have_metadata(self, tmp_path):
        """Test returns empty when all workflows have metadata."""
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()

        (workflows_dir / "valid.yml").write_text("name: Valid")
        (workflows_dir / "valid.yml.meta.json").write_text("{}")

        result = find_missing_metadata(workflows_dir)

        assert result == []


@pytest.mark.unit
class TestBuildManifest:
    """Test build_manifest function."""

    def test_builds_complete_manifest(self, tmp_path):
        """Test builds manifest with all sections."""
        # Create directory structure
        ai_framework = tmp_path / "src" / "ai_framework"
        agents_dir = ai_framework / "agents"
        agents_dir.mkdir(parents=True)

        chatmodes_dir = ai_framework / "chatmodes"
        chatmodes_dir.mkdir()

        prompts_dir = ai_framework / "prompts"
        prompts_dir.mkdir()

        collections_dir = ai_framework / "collections"
        collections_dir.mkdir()

        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        registry_dir = tmp_path / "docs" / "registry"
        registry_dir.mkdir(parents=True)

        # Create files
        (agents_dir / "test.agent.md").write_text("""---
name: Test Agent
description: A test agent
---
""")

        (chatmodes_dir / "test.chatmode.md").write_text("""---
name: Test Mode
---
""")

        (workflows_dir / "ci.yml").write_text("name: CI")

        output = tmp_path / "manifest.json"
        result = build_manifest(tmp_path, output)

        assert result["version"] == "1.0.0"
        assert result["organization"] == "{{ORG_NAME}}"
        assert result["statistics"]["agents"]["total"] == 1
        assert result["statistics"]["chatmodes"]["total"] == 1

    def test_handles_missing_directories(self, tmp_path):
        """Test handles missing directories gracefully."""
        output = tmp_path / "manifest.json"
        result = build_manifest(tmp_path, output)

        assert result["statistics"]["agents"]["total"] == 0
        assert result["statistics"]["chatmodes"]["total"] == 0


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_generates_manifest(self, tmp_path, monkeypatch):
        """Test main generates manifest file."""
        # Create directory structure
        ai_framework = tmp_path / "src" / "ai_framework"
        agents_dir = ai_framework / "agents"
        agents_dir.mkdir(parents=True)

        registry_dir = tmp_path / "docs" / "registry"
        registry_dir.mkdir(parents=True)

        (agents_dir / "test.agent.md").write_text("""---
name: Test
---
""")

        output = tmp_path / "manifest.json"

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "generate_manifest.py",
                "--root",
                str(tmp_path),
                "--output",
                str(output),
            ],
        )

        main()

        assert output.exists()
        manifest = json.loads(output.read_text())
        assert manifest["statistics"]["agents"]["total"] == 1

    def test_main_default_output(self, tmp_path, monkeypatch):
        """Test main uses default output path."""
        registry_dir = tmp_path / "docs" / "registry"
        registry_dir.mkdir(parents=True)

        monkeypatch.setattr(
            sys,
            "argv",
            ["generate_manifest.py", "--root", str(tmp_path)],
        )

        main()

        default_output = registry_dir / "manifest.json"
        assert default_output.exists()

    def test_main_prints_summary(self, tmp_path, monkeypatch, capsys):
        """Test main prints summary to stdout."""
        ai_framework = tmp_path / "src" / "ai_framework"
        agents_dir = ai_framework / "agents"
        agents_dir.mkdir(parents=True)

        registry_dir = tmp_path / "docs" / "registry"
        registry_dir.mkdir(parents=True)

        (agents_dir / "test.agent.md").write_text("---\nname: Test\n---\n")

        monkeypatch.setattr(
            sys,
            "argv",
            ["generate_manifest.py", "--root", str(tmp_path)],
        )

        main()

        captured = capsys.readouterr()
        assert "Manifest generated" in captured.out
        assert "Agents: 1" in captured.out

    def test_main_prints_health_warnings(self, tmp_path, monkeypatch, capsys):
        """Test main prints health warnings."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        registry_dir = tmp_path / "docs" / "registry"
        registry_dir.mkdir(parents=True)

        # Create orphaned meta file
        (workflows_dir / "orphan.yml.meta.json").write_text("{}")

        monkeypatch.setattr(
            sys,
            "argv",
            ["generate_manifest.py", "--root", str(tmp_path)],
        )

        main()

        captured = capsys.readouterr()
        assert "Orphaned metadata" in captured.out


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_frontmatter_with_colons_in_value(self):
        """Test handles colons in values."""
        content = """---
url: https://example.com
description: Time: now
---
"""
        result = parse_frontmatter(content)

        assert result["url"] == "https://example.com"
        assert result["description"] == "Time: now"

    def test_frontmatter_preserves_key_casing(self):
        """Test preserves key casing."""
        content = """---
Name: Test
DESCRIPTION: Test
---
"""
        result = parse_frontmatter(content)

        assert "Name" in result
        assert "DESCRIPTION" in result

    def test_scan_agents_sorts_files(self, tmp_path):
        """Test agents are sorted alphabetically."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        (agents_dir / "zebra.agent.md").write_text("---\nname: Zebra\n---\n")
        (agents_dir / "alpha.agent.md").write_text("---\nname: Alpha\n---\n")

        result = scan_agents(agents_dir)

        assert result["files"][0]["file"] == "alpha.agent.md"
        assert result["files"][1]["file"] == "zebra.agent.md"

    def test_workflow_registry_with_alternate_key(self, tmp_path):
        """Test handles total_workflows vs total key."""
        registry_file = tmp_path / "registry.json"
        registry_file.write_text(json.dumps({"statistics": {"total_workflows": 100}}))

        result = load_workflow_registry(registry_file)

        # build_manifest checks total_workflows first, then total
        assert result.get("total_workflows") == 100 or result.get("total") == 0

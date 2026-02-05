#!/usr/bin/env python3
"""Unit tests for automation/scripts/resolve_link_placeholders.py

Focus: Managed link resolution and placeholder replacement in Markdown files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from resolve_link_placeholders import (DEFAULT_EXCLUDES, LINK_WITH_COMMENT_RE,
                                       PLACEHOLDER_RE, UNANNOTATED_LINK_RE,
                                       _flatten_map, _parse_simple_yaml,
                                       build_agent_path_map,
                                       calculate_relative_path,
                                       is_internal_path, iter_markdown_files,
                                       load_link_map, main,
                                       migrate_broken_links, replace_links)


@pytest.mark.unit
class TestParseSimpleYaml:
    """Test _parse_simple_yaml function."""

    def test_parses_simple_yaml(self):
        """Test parses simple YAML."""
        text = """
key1: value1
key2: value2
"""
        result = _parse_simple_yaml(text)

        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_parses_nested_yaml(self):
        """Test parses nested YAML."""
        text = """
parent:
  child1: value1
  child2: value2
"""
        result = _parse_simple_yaml(text)

        assert "parent" in result
        assert result["parent"]["child1"] == "value1"

    def test_handles_comments(self):
        """Test handles comments."""
        text = """
# This is a comment
key: value
"""
        result = _parse_simple_yaml(text)

        assert result["key"] == "value"

    def test_handles_inline_comments(self):
        """Test handles inline comments."""
        text = """
key: value  # inline comment
"""
        result = _parse_simple_yaml(text)

        assert result["key"] == "value"

    def test_handles_empty_lines(self):
        """Test handles empty lines."""
        text = """

key1: value1

key2: value2

"""
        result = _parse_simple_yaml(text)

        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_handles_line_without_colon(self):
        """Test skips lines without colon."""
        text = """
key: value
invalid line
other: data
"""
        result = _parse_simple_yaml(text)

        assert result["key"] == "value"
        assert result["other"] == "data"


@pytest.mark.unit
class TestFlattenMap:
    """Test _flatten_map function."""

    def test_flattens_nested_dict(self):
        """Test flattens nested dictionary."""
        node = {"a": {"b": {"c": "value"}}}
        out = {}

        _flatten_map("", node, out)

        assert out["a.b.c"] == "value"

    def test_flattens_simple_dict(self):
        """Test flattens simple dictionary."""
        node = {"key": "value"}
        out = {}

        _flatten_map("", node, out)

        assert out["key"] == "value"

    def test_handles_prefix(self):
        """Test handles existing prefix."""
        node = {"child": "value"}
        out = {}

        _flatten_map("parent", node, out)

        assert out["parent.child"] == "value"

    def test_converts_non_string_values(self):
        """Test converts non-string values to strings."""
        node = {"number": 42, "bool": True}
        out = {}

        _flatten_map("", node, out)

        assert out["number"] == "42"
        assert out["bool"] == "True"


@pytest.mark.unit
class TestLoadLinkMap:
    """Test load_link_map function."""

    def test_loads_yaml_file(self, tmp_path):
        """Test loads YAML link map file."""
        yaml_content = """
github:
  discussions: https://github.com/org/repo/discussions
  issues: https://github.com/org/repo/issues
"""
        yaml_file = tmp_path / "links.yml"
        yaml_file.write_text(yaml_content)

        result = load_link_map(yaml_file)

        assert "github.discussions" in result
        assert "github.issues" in result

    def test_uses_yaml_library_if_available(self, tmp_path):
        """Test uses yaml library if available."""
        yaml_content = """
key: value
"""
        yaml_file = tmp_path / "links.yml"
        yaml_file.write_text(yaml_content)

        result = load_link_map(yaml_file)

        assert result["key"] == "value"


@pytest.mark.unit
class TestIsInternalPath:
    """Test is_internal_path function."""

    def test_internal_path(self):
        """Test identifies internal paths."""
        assert is_internal_path("internal.agents.foo") is True
        assert is_internal_path("internal.docs.guide") is True

    def test_external_path(self):
        """Test identifies external paths."""
        assert is_internal_path("github.discussions") is False
        assert is_internal_path("docs.api") is False


@pytest.mark.unit
class TestCalculateRelativePath:
    """Test calculate_relative_path function."""

    def test_calculates_relative_path(self, tmp_path):
        """Test calculates relative path between files."""
        from_file = tmp_path / "docs" / "guide.md"
        to_path = "src/module.py"

        result = calculate_relative_path(from_file, to_path, tmp_path)

        assert "../src/module.py" in result or "src/module.py" in result

    def test_same_directory(self, tmp_path):
        """Test calculates path in same directory."""
        from_file = tmp_path / "docs" / "guide.md"
        to_path = "docs/other.md"

        result = calculate_relative_path(from_file, to_path, tmp_path)

        assert "other.md" in result

    def test_normalizes_slashes(self, tmp_path):
        """Test normalizes backslashes to forward slashes."""
        from_file = tmp_path / "docs" / "guide.md"
        to_path = "src/module.py"

        result = calculate_relative_path(from_file, to_path, tmp_path)

        assert "\\" not in result


@pytest.mark.unit
class TestIterMarkdownFiles:
    """Test iter_markdown_files function."""

    def test_finds_markdown_files(self, tmp_path):
        """Test finds all markdown files."""
        (tmp_path / "doc1.md").write_text("# Doc 1")
        (tmp_path / "doc2.md").write_text("# Doc 2")
        (tmp_path / "readme.txt").write_text("Not markdown")

        files = list(iter_markdown_files(tmp_path, []))

        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)

    def test_excludes_directories(self, tmp_path):
        """Test excludes specified directories."""
        (tmp_path / "doc.md").write_text("# Doc")
        node_modules = tmp_path / "node_modules"
        node_modules.mkdir()
        (node_modules / "excluded.md").write_text("# Excluded")

        files = list(iter_markdown_files(tmp_path, ["node_modules"]))

        assert len(files) == 1
        assert files[0].name == "doc.md"

    def test_finds_nested_files(self, tmp_path):
        """Test finds nested markdown files."""
        nested = tmp_path / "docs" / "api"
        nested.mkdir(parents=True)
        (nested / "guide.md").write_text("# Guide")

        files = list(iter_markdown_files(tmp_path, []))

        assert len(files) == 1
        assert files[0].name == "guide.md"


@pytest.mark.unit
class TestReplaceLinks:
    """Test replace_links function."""

    @pytest.fixture
    def link_map(self):
        """Create sample link map."""
        return {
            "github.discussions": "https://github.com/org/repo/discussions",
            "github.issues": "https://github.com/org/repo/issues",
            "internal.agents.foo": "src/ai_framework/agents/foo.agent.md",
        }

    @pytest.fixture
    def reverse_map(self, link_map):
        """Create reverse link map."""
        return {v: k for k, v in link_map.items()}

    def test_updates_annotated_links(self, link_map, reverse_map):
        """Test updates annotated links."""
        text = "[Discussions](https://old-url.com)<!-- link:github.discussions -->"

        result, updated, annotated, missing = replace_links(text, link_map, reverse_map, annotate=False)

        assert updated == 1
        assert "https://github.com/org/repo/discussions" in result

    def test_handles_placeholder_links(self, link_map, reverse_map):
        """Test handles placeholder syntax."""
        text = "[Link]([[link:github.discussions]])"

        result, updated, annotated, missing = replace_links(text, link_map, reverse_map, annotate=False)

        assert updated == 1
        assert annotated == 1
        assert "https://github.com/org/repo/discussions" in result

    def test_annotates_existing_urls(self, link_map, reverse_map):
        """Test annotates existing URLs when enabled."""
        text = "[Discussions](https://github.com/org/repo/discussions)"

        result, updated, annotated, missing = replace_links(text, link_map, reverse_map, annotate=True)

        assert annotated == 1
        assert "<!-- link:github.discussions -->" in result

    def test_skips_code_fences(self, link_map, reverse_map):
        """Test skips content in code fences."""
        text = """```
[Link](https://github.com/org/repo/discussions)
```"""

        result, updated, annotated, missing = replace_links(text, link_map, reverse_map, annotate=True)

        assert annotated == 0
        assert result == text

    def test_handles_missing_keys(self, link_map, reverse_map):
        """Test handles missing link keys."""
        text = "[Link](url)<!-- link:nonexistent.key -->"

        result, updated, annotated, missing = replace_links(text, link_map, reverse_map, annotate=False)

        assert missing == 1

    def test_calculates_relative_path_for_internal(self, tmp_path):
        """Test calculates relative path for internal links."""
        link_map = {"internal.agents.foo": "src/agents/foo.agent.md"}
        reverse_map = {}
        text = "[Agent](url)<!-- link:internal.agents.foo -->"
        from_file = tmp_path / "docs" / "guide.md"

        result, updated, annotated, missing = replace_links(
            text,
            link_map,
            reverse_map,
            annotate=False,
            current_file=from_file,
            root=tmp_path,
        )

        assert updated == 1
        assert "../src/agents/foo.agent.md" in result or "src/agents" in result


@pytest.mark.unit
class TestBuildAgentPathMap:
    """Test build_agent_path_map function."""

    def test_builds_agent_map(self):
        """Test builds agent filename to key map."""
        link_map = {
            "internal.agents.foo": "src/agents/foo.agent.md",
            "internal.agents.bar": "src/agents/bar.agent.md",
            "github.issues": "https://github.com/issues",
        }

        result = build_agent_path_map(link_map)

        assert "foo.agent.md" in result
        assert result["foo.agent.md"] == "internal.agents.foo"
        assert "bar.agent.md" in result

    def test_excludes_non_agent_keys(self):
        """Test excludes non-agent keys."""
        link_map = {"github.issues": "https://github.com/issues"}

        result = build_agent_path_map(link_map)

        assert len(result) == 0


@pytest.mark.unit
class TestMigrateBrokenLinks:
    """Test migrate_broken_links function."""

    def test_migrates_broken_agent_links(self, tmp_path):
        """Test migrates broken relative agent links."""
        link_map = {"internal.agents.foo": "src/ai_framework/agents/foo.agent.md"}
        text = "[Foo Agent](../agents/foo.agent.md)"
        from_file = tmp_path / "docs" / "guide.md"

        result = migrate_broken_links(text, link_map, from_file, tmp_path)

        assert "<!-- link:internal.agents.foo -->" in result

    def test_ignores_unknown_agents(self, tmp_path):
        """Test ignores agents not in link map."""
        link_map = {}
        text = "[Unknown](../agents/unknown.agent.md)"
        from_file = tmp_path / "docs" / "guide.md"

        result = migrate_broken_links(text, link_map, from_file, tmp_path)

        assert result == text


@pytest.mark.unit
class TestRegexPatterns:
    """Test regex patterns."""

    def test_link_with_comment_pattern(self):
        """Test LINK_WITH_COMMENT_RE pattern."""
        text = "[Text](https://example.com)<!-- link:key.name -->"
        match = LINK_WITH_COMMENT_RE.search(text)

        assert match is not None
        assert match.group("key") == "key.name"
        assert match.group("url") == "https://example.com"

    def test_unannotated_link_pattern(self):
        """Test UNANNOTATED_LINK_RE pattern."""
        text = "[Text](https://example.com)"
        match = UNANNOTATED_LINK_RE.search(text)

        assert match is not None
        assert match.group("url") == "https://example.com"

    def test_placeholder_pattern(self):
        """Test PLACEHOLDER_RE pattern."""
        text = "[[link:key.name]]"
        match = PLACEHOLDER_RE.match(text)

        assert match is not None
        assert match.group("key") == "key.name"

    def test_image_link_pattern(self):
        """Test handles image links (![ prefix)."""
        text = "![Image](https://example.com/image.png)"
        match = UNANNOTATED_LINK_RE.search(text)

        assert match is not None


@pytest.mark.unit
class TestDefaultExcludes:
    """Test DEFAULT_EXCLUDES set."""

    def test_contains_common_excludes(self):
        """Test contains common excluded directories."""
        assert ".git" in DEFAULT_EXCLUDES
        assert "node_modules" in DEFAULT_EXCLUDES
        assert "vendor" in DEFAULT_EXCLUDES
        assert ".venv" in DEFAULT_EXCLUDES


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_missing_map_file(self, tmp_path, monkeypatch, capsys):
        """Test main exits when link map not found."""
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(tmp_path / "nonexistent.yml"),
                "--root",
                str(tmp_path),
            ],
        )

        result = main()

        assert result == 2
        captured = capsys.readouterr()
        assert "not found" in captured.err

    def test_main_dry_run(self, tmp_path, monkeypatch, capsys):
        """Test main in dry run mode (default)."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown file
        doc = tmp_path / "doc.md"
        doc.write_text("[Link](url)<!-- link:github.discussions -->")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
            ],
        )

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Managed link scan complete" in captured.out

    def test_main_write_mode(self, tmp_path, monkeypatch, capsys):
        """Test main with --write flag."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown file
        doc = tmp_path / "doc.md"
        doc.write_text("[Link](https://old.com)<!-- link:github.discussions -->")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
                "--write",
            ],
        )

        result = main()

        assert result == 0
        # File should be updated
        content = doc.read_text()
        assert "https://example.com" in content

    def test_main_check_mode_with_changes(self, tmp_path, monkeypatch, capsys):
        """Test main with --check flag when changes needed."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown file with outdated link
        doc = tmp_path / "doc.md"
        doc.write_text("[Link](https://old.com)<!-- link:github.discussions -->")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
                "--check",
            ],
        )

        result = main()

        assert result == 1  # Non-zero because changes needed

    def test_main_with_missing_keys(self, tmp_path, monkeypatch, capsys):
        """Test main reports missing keys."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown file with unknown key
        doc = tmp_path / "doc.md"
        doc.write_text("[Link](url)<!-- link:nonexistent.key -->")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
            ],
        )

        result = main()

        assert result == 1  # Non-zero because missing keys
        captured = capsys.readouterr()
        assert "Missing keys: 1" in captured.out

    def test_main_with_annotate_flag(self, tmp_path, monkeypatch, capsys):
        """Test main with --annotate flag."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown file with unannotated link
        doc = tmp_path / "doc.md"
        doc.write_text("[Link](https://example.com)")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
                "--annotate",
                "--write",
            ],
        )

        result = main()

        assert result == 0
        content = doc.read_text()
        assert "<!-- link:github.discussions -->" in content

    def test_main_with_exclude_flag(self, tmp_path, monkeypatch, capsys):
        """Test main with --exclude flag."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("github:\n  discussions: https://example.com")

        # Create markdown files
        (tmp_path / "doc.md").write_text("# Doc")
        excluded = tmp_path / "excluded"
        excluded.mkdir()
        (excluded / "hidden.md").write_text("# Hidden")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
                "--exclude",
                "excluded",
            ],
        )

        main()

        captured = capsys.readouterr()
        assert "Managed link scan complete" in captured.out

    def test_main_with_migrate_flag(self, tmp_path, monkeypatch, capsys):
        """Test main with --migrate flag."""
        # Create link map
        link_map = tmp_path / "links.yml"
        link_map.write_text("internal:\n  agents:\n    foo: src/ai_framework/agents/foo.agent.md")

        # Create markdown file with broken link
        doc = tmp_path / "doc.md"
        doc.write_text("[Agent](../agents/foo.agent.md)")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "resolve_link_placeholders.py",
                "--map",
                str(link_map),
                "--root",
                str(tmp_path),
                "--migrate",
                "--write",
            ],
        )

        result = main()

        assert result == 0

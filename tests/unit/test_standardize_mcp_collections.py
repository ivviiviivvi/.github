#!/usr/bin/env python3
"""Unit tests for automation/scripts/utils/standardize-mcp-collections.py

Focus: MCP collection frontmatter standardization.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

# Import the module with hyphenated filename
spec = importlib.util.spec_from_file_location(
    "standardize_mcp_collections",
    Path(__file__).parent.parent.parent / "src" / "automation" / "scripts" / "utils" / "standardize-mcp-collections.py",
)
standardize_mcp_collections = importlib.util.module_from_spec(spec)
sys.modules["standardize_mcp_collections"] = standardize_mcp_collections
spec.loader.exec_module(standardize_mcp_collections)


@pytest.mark.unit
class TestExtractInlineFrontmatter:
    """Test extract_inline_frontmatter function."""

    def test_extracts_valid_inline_frontmatter(self):
        """Test extracts valid inline frontmatter."""
        line = "## name: Test Collection description: A test tags: [] updated: 2024-01-15"

        result = standardize_mcp_collections.extract_inline_frontmatter(line)

        assert result["name"] == "Test Collection"
        assert result["description"] == "A test"
        assert result["tags"] == []
        assert result["updated"] == "2024-01-15"

    def test_returns_empty_for_invalid_format(self):
        """Test returns empty dict for invalid format."""
        line = "## This is not valid frontmatter"

        result = standardize_mcp_collections.extract_inline_frontmatter(line)

        assert result == {}

    def test_handles_escaped_brackets(self):
        """Test handles escaped brackets for empty tags."""
        line = r"## name: Test description: Desc tags: \[\] updated: 2024-01-01"

        result = standardize_mcp_collections.extract_inline_frontmatter(line)

        assert result["tags"] == []

    def test_returns_empty_for_missing_fields(self):
        """Test returns empty for missing required fields."""
        line = "## name: OnlyName"

        result = standardize_mcp_collections.extract_inline_frontmatter(line)

        assert result == {}


@pytest.mark.unit
class TestGetYmlFrontmatter:
    """Test get_yml_frontmatter function."""

    def test_extracts_yml_frontmatter(self, tmp_path):
        """Test extracts frontmatter from yml file."""
        yml_file = tmp_path / "test.collection.yml"
        yml_file.write_text("""---
name: Test Collection
description: A test collection
tags:
  - mcp
  - tools
updated: "2024-01-15"
---
# Content here
""")

        result = standardize_mcp_collections.get_yml_frontmatter(yml_file)

        assert result["name"] == "Test Collection"
        assert result["description"] == "A test collection"
        assert result["tags"] == ["mcp", "tools"]
        # YAML may parse as date or string depending on format
        assert str(result["updated"]) == "2024-01-15"

    def test_returns_empty_for_nonexistent_file(self, tmp_path):
        """Test returns empty for nonexistent file."""
        yml_file = tmp_path / "nonexistent.yml"

        result = standardize_mcp_collections.get_yml_frontmatter(yml_file)

        assert result == {}

    def test_returns_empty_for_no_frontmatter(self, tmp_path):
        """Test returns empty when file has no frontmatter."""
        yml_file = tmp_path / "test.yml"
        yml_file.write_text("# Just content, no frontmatter")

        result = standardize_mcp_collections.get_yml_frontmatter(yml_file)

        assert result == {}

    def test_returns_empty_for_unclosed_frontmatter(self, tmp_path):
        """Test returns empty for unclosed frontmatter."""
        yml_file = tmp_path / "test.yml"
        yml_file.write_text("""---
name: Test
# Never closed
""")

        result = standardize_mcp_collections.get_yml_frontmatter(yml_file)

        assert result == {}

    def test_handles_invalid_yaml(self, tmp_path):
        """Test handles invalid YAML gracefully."""
        yml_file = tmp_path / "test.yml"
        yml_file.write_text("""---
name: [invalid
  yaml: here
---
""")

        result = standardize_mcp_collections.get_yml_frontmatter(yml_file)

        assert result == {}


@pytest.mark.unit
class TestFixMdFrontmatter:
    """Test fix_md_frontmatter function."""

    def test_fixes_malformed_frontmatter(self, tmp_path):
        """Test fixes malformed frontmatter."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---

## name: Test description: A test tags: [] updated: 2024-01-15

Content goes here
""")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is True
        content = md_file.read_text()
        assert "name: Test" in content
        assert "description: A test" in content
        assert "tags: []" in content

    def test_returns_false_for_empty_file(self, tmp_path):
        """Test returns False for empty file."""
        md_file = tmp_path / "test.md"
        md_file.write_text("")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is False

    def test_returns_false_for_no_frontmatter_start(self, tmp_path):
        """Test returns False when file doesn't start with ---."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Just a heading\n\nContent")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is False

    def test_returns_false_for_short_file(self, tmp_path):
        """Test returns False for file with less than 3 lines."""
        md_file = tmp_path / "test.md"
        md_file.write_text("---\n---")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is False

    def test_returns_false_for_no_inline_comment(self, tmp_path):
        """Test returns False when no inline comment frontmatter."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---

name: Test
---
Content
""")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is False

    def test_uses_yml_frontmatter_when_available(self, tmp_path):
        """Test uses yml frontmatter when available."""
        yml_file = tmp_path / "test.collection.yml"
        yml_file.write_text("""---
name: YML Name
description: YML Description
tags:
  - yml-tag
updated: 2024-02-01
---
""")

        md_file = tmp_path / "test.md"
        md_file.write_text("""---

## name: MD Name description: MD Desc tags: [] updated: 2024-01-01

Content
""")

        result = standardize_mcp_collections.fix_md_frontmatter(md_file)

        assert result is True
        content = md_file.read_text()
        assert "name: YML Name" in content
        assert "description: YML Description" in content

    def test_adds_tags_section_when_present(self, tmp_path):
        """Test adds tags section when tags exist."""
        yml_file = tmp_path / "test.collection.yml"
        yml_file.write_text("""---
name: Test
description: Desc
tags:
  - tag1
  - tag2
updated: 2024-01-01
---
""")

        md_file = tmp_path / "test.md"
        md_file.write_text("""---

## name: X description: Y tags: [] updated: Z

Content
""")

        standardize_mcp_collections.fix_md_frontmatter(md_file)

        content = md_file.read_text()
        assert "tags:" in content
        assert "  - tag1" in content
        assert "  - tag2" in content


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_returns_1_when_directory_missing(self, tmp_path, monkeypatch, capsys):
        """Test returns 1 when collections directory is missing."""
        monkeypatch.chdir(tmp_path)

        result = standardize_mcp_collections.main()

        assert result == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.out

    def test_processes_md_files(self, tmp_path, monkeypatch, capsys):
        """Test processes .md files in collections directory."""
        collections_dir = tmp_path / "ai_framework" / "collections"
        collections_dir.mkdir(parents=True)

        # Create a file that won't be fixed (no inline frontmatter)
        test_file = collections_dir / "test.md"
        test_file.write_text("# Test\n\nContent")

        monkeypatch.chdir(tmp_path)

        result = standardize_mcp_collections.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Processing test.md" in captured.out

    def test_skips_special_files(self, tmp_path, monkeypatch, capsys):
        """Test skips INVENTORY.md, SCHEMA.md, README.md, TEMPLATE.md."""
        collections_dir = tmp_path / "ai_framework" / "collections"
        collections_dir.mkdir(parents=True)

        # Create special files
        for name in ["INVENTORY.md", "SCHEMA.md", "README.md", "TEMPLATE.md"]:
            (collections_dir / name).write_text("# Skip me")

        monkeypatch.chdir(tmp_path)

        result = standardize_mcp_collections.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "INVENTORY.md" not in captured.out
        assert "SCHEMA.md" not in captured.out
        assert "README.md" not in captured.out
        assert "TEMPLATE.md" not in captured.out

    def test_reports_fixed_count(self, tmp_path, monkeypatch, capsys):
        """Test reports the count of fixed files."""
        collections_dir = tmp_path / "ai_framework" / "collections"
        collections_dir.mkdir(parents=True)

        # Create fixable file
        test_file = collections_dir / "fixable.md"
        test_file.write_text("""---

## name: Test description: Desc tags: [] updated: 2024-01-01

Content
""")

        monkeypatch.chdir(tmp_path)

        result = standardize_mcp_collections.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Fixed 1 collection files" in captured.out

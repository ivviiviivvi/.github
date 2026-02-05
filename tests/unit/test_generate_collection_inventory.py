#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_collection_inventory.py

Focus: Frontmatter parsing and inventory generation for collection files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from generate_collection_inventory import main, parse_frontmatter


@pytest.mark.unit
class TestParseFrontmatter:
    """Test frontmatter parsing functionality."""

    def test_empty_input_returns_empty(self):
        """Test empty input returns empty dict."""
        result = parse_frontmatter([])
        assert result == {}

    def test_no_opening_delimiter(self):
        """Test missing opening --- returns empty."""
        lines = ["name: test", "---"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_no_closing_delimiter(self):
        """Test missing closing --- returns empty."""
        lines = ["---", "name: test"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_parses_simple_frontmatter(self):
        """Test parses key: value pairs."""
        lines = [
            "---",
            "name: MCP Collection",
            "description: A collection of MCP tools",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "MCP Collection"
        assert result["description"] == "A collection of MCP tools"

    def test_ignores_comments(self):
        """Test ignores comment lines."""
        lines = [
            "---",
            "# Comment line",
            "name: Collection",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert "name" in result
        assert "#" not in str(result.keys())

    def test_ignores_empty_lines(self):
        """Test skips empty lines."""
        lines = [
            "---",
            "",
            "name: Name",
            "",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Name"

    def test_parses_list_values(self):
        """Test parses YAML list format."""
        lines = [
            "---",
            "tools:",
            "  - tool1",
            "  - tool2",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["tools"] == ["tool1", "tool2"]

    def test_handles_mixed_content(self):
        """Test handles mix of scalars and lists."""
        lines = [
            "---",
            "name: Mixed",
            "tags:",
            "  - tag1",
            "  - tag2",
            "version: 1.0",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Mixed"
        assert result["tags"] == ["tag1", "tag2"]
        assert result["version"] == "1.0"


@pytest.mark.unit
class TestMainFunction:
    """Test main inventory generation function."""

    @pytest.fixture
    def mock_collections_dir(self, tmp_path):
        """Create mock collections directory."""
        collections_dir = tmp_path / "ai_framework" / "collections"
        collections_dir.mkdir(parents=True)
        return collections_dir

    @pytest.fixture
    def mock_output_path(self, tmp_path):
        """Create mock output path."""
        return tmp_path / "ai_framework" / "collections" / "INVENTORY.md"

    def test_creates_inventory_file(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test creates INVENTORY.md file."""
        collection = mock_collections_dir / "mcp-tools.md"
        collection.write_text("---\nname: MCP Tools\ndescription: Tools\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        assert mock_output_path.exists()

    def test_inventory_has_header(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test inventory has proper header."""
        collection = mock_collections_dir / "test.md"
        collection.write_text("---\nname: Test\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "# Collection Inventory" in content
        assert "| File | Name | Description | Tags |" in content

    def test_includes_collection_data(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test inventory includes collection data."""
        collection = mock_collections_dir / "utilities.md"
        collection.write_text("---\nname: Utilities\ndescription: Utility tools\ntags:\n  - util\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "utilities.md" in content
        assert "Utilities" in content
        assert "Utility tools" in content
        assert "util" in content

    def test_handles_md_files(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test processes .md files."""
        collection = mock_collections_dir / "markdown.md"
        collection.write_text("---\nname: MD Collection\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "markdown.md" in content

    def test_handles_yml_files(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test processes .yml files."""
        collection = mock_collections_dir / "config.yml"
        collection.write_text("---\nname: YAML Collection\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "config.yml" in content
        assert "YAML Collection" in content

    def test_handles_multiple_collections(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles multiple collection files."""
        for i in range(3):
            collection = mock_collections_dir / f"collection-{i}.md"
            collection.write_text(f"---\nname: Collection {i}\ndescription: Desc {i}\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        for i in range(3):
            assert f"collection-{i}.md" in content

    def test_handles_missing_tags(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles collections without tags."""
        collection = mock_collections_dir / "no-tags.md"
        collection.write_text("---\nname: No Tags\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "No Tags" in content

    def test_handles_string_tags(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles single string tag."""
        collection = mock_collections_dir / "single-tag.md"
        collection.write_text("---\nname: Single\ndescription: D\ntags: solo\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "solo" in content

    def test_joins_multiple_tags(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test joins multiple tags with comma."""
        collection = mock_collections_dir / "multi-tag.md"
        collection.write_text("---\nname: Multi\ndescription: D\ntags:\n  - a\n  - b\n  - c\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "a, b, c" in content

    def test_ignores_other_file_types(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test ignores non-md/yml files."""
        # Create various file types
        json_file = mock_collections_dir / "config.json"
        json_file.write_text('{"key": "value"}')

        txt_file = mock_collections_dir / "notes.txt"
        txt_file.write_text("Some notes")

        # Create valid collection
        collection = mock_collections_dir / "valid.md"
        collection.write_text("---\nname: Valid\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "valid.md" in content
        assert "config.json" not in content
        assert "notes.txt" not in content

    def test_empty_directory(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles empty directory."""
        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "# Collection Inventory" in content

    def test_files_sorted_alphabetically(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test files are sorted alphabetically."""
        for name in ["zebra", "alpha", "beta"]:
            collection = mock_collections_dir / f"{name}.md"
            collection.write_text(f"---\nname: {name}\ndescription: D\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        alpha_pos = content.find("alpha.md")
        beta_pos = content.find("beta.md")
        zebra_pos = content.find("zebra.md")

        assert alpha_pos < beta_pos < zebra_pos

    def test_handles_missing_name(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles collection with missing name."""
        collection = mock_collections_dir / "no-name.md"
        collection.write_text("---\ndescription: No name field\n---\n")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "no-name.md" in content
        # Should not fail, just have empty name

    def test_handles_no_frontmatter(self, mock_collections_dir, mock_output_path, monkeypatch):
        """Test handles files without frontmatter."""
        collection = mock_collections_dir / "no-fm.md"
        collection.write_text("# Just content\nNo frontmatter here")

        monkeypatch.setattr("generate_collection_inventory.COLLECTIONS_DIR", mock_collections_dir)
        monkeypatch.setattr("generate_collection_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "no-fm.md" in content

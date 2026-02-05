#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_chatmode_inventory.py

Focus: Frontmatter parsing and inventory generation for chatmode files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from generate_chatmode_inventory import main, parse_frontmatter


@pytest.mark.unit
class TestParseFrontmatter:
    """Test frontmatter parsing functionality."""

    def test_empty_input_returns_empty_dict(self):
        """Test empty input returns empty dict."""
        result = parse_frontmatter([])
        assert result == {}

    def test_missing_opening_delimiter(self):
        """Test missing opening --- returns empty dict."""
        lines = ["name: value", "---"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_missing_closing_delimiter(self):
        """Test missing closing --- returns empty dict."""
        lines = ["---", "name: value"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_parses_key_value_pairs(self):
        """Test parses simple key: value pairs."""
        lines = [
            "---",
            "name: Code Review Mode",
            "description: For reviewing code",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Code Review Mode"
        assert result["description"] == "For reviewing code"

    def test_ignores_comment_lines(self):
        """Test lines starting with # are ignored."""
        lines = [
            "---",
            "# Configuration comment",
            "name: Mode Name",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert "name" in result
        assert len(result) == 1

    def test_ignores_blank_lines(self):
        """Test empty lines are skipped."""
        lines = [
            "---",
            "",
            "name: Mode",
            "",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Mode"

    def test_parses_yaml_list(self):
        """Test parses YAML list format correctly."""
        lines = [
            "---",
            "tags:",
            "  - code-review",
            "  - analysis",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert "tags" in result
        assert result["tags"] == ["code-review", "analysis"]

    def test_handles_mixed_scalar_and_list(self):
        """Test handles both scalar and list values."""
        lines = [
            "---",
            "name: Mixed Mode",
            "tags:",
            "  - item1",
            "  - item2",
            "description: A description",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Mixed Mode"
        assert result["tags"] == ["item1", "item2"]
        assert result["description"] == "A description"


@pytest.mark.unit
class TestMainFunction:
    """Test main inventory generation function."""

    @pytest.fixture
    def mock_chatmodes_dir(self, tmp_path):
        """Create mock chatmodes directory."""
        chatmodes_dir = tmp_path / "ai_framework" / "chatmodes"
        chatmodes_dir.mkdir(parents=True)
        return chatmodes_dir

    @pytest.fixture
    def mock_output_path(self, tmp_path):
        """Create mock output path."""
        return tmp_path / "ai_framework" / "chatmodes" / "INVENTORY.md"

    def test_creates_inventory_file(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test creates INVENTORY.md file."""
        chatmode = mock_chatmodes_dir / "review.chatmode.md"
        chatmode.write_text("---\nname: Review Mode\ndescription: Review\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        assert mock_output_path.exists()

    def test_inventory_has_header(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test inventory file has proper header."""
        chatmode = mock_chatmodes_dir / "test.chatmode.md"
        chatmode.write_text("---\nname: Test\ndescription: Desc\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "# Chatmode Inventory" in content
        assert "| File | Name | Description | Tags |" in content

    def test_includes_chatmode_data(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test inventory includes chatmode data in table."""
        chatmode = mock_chatmodes_dir / "debug.chatmode.md"
        chatmode.write_text("---\nname: Debug Mode\ndescription: For debugging\ntags:\n  - debug\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "debug.chatmode.md" in content
        assert "Debug Mode" in content
        assert "For debugging" in content
        assert "debug" in content

    def test_handles_multiple_chatmodes(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test handles multiple chatmode files."""
        for i in range(3):
            chatmode = mock_chatmodes_dir / f"mode-{i}.chatmode.md"
            chatmode.write_text(f"---\nname: Mode {i}\ndescription: Description {i}\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        for i in range(3):
            assert f"mode-{i}.chatmode.md" in content
            assert f"Mode {i}" in content

    def test_handles_missing_tags(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test handles chatmodes without tags."""
        chatmode = mock_chatmodes_dir / "minimal.chatmode.md"
        chatmode.write_text("---\nname: Minimal\ndescription: No tags\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "Minimal" in content
        # Should not fail, just have empty tags column

    def test_handles_string_tags(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test handles single string tag."""
        chatmode = mock_chatmodes_dir / "single.chatmode.md"
        chatmode.write_text("---\nname: Single Tag\ndescription: One tag\ntags: solo\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "solo" in content

    def test_joins_multiple_tags(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test joins multiple tags with comma."""
        chatmode = mock_chatmodes_dir / "multi.chatmode.md"
        chatmode.write_text("---\nname: Multi\ndescription: Many tags\ntags:\n  - a\n  - b\n  - c\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "a, b, c" in content

    def test_only_processes_chatmode_files(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test only processes *.chatmode.md files."""
        # Create non-chatmode files
        readme = mock_chatmodes_dir / "README.md"
        readme.write_text("# Readme")

        # Create chatmode file
        chatmode = mock_chatmodes_dir / "valid.chatmode.md"
        chatmode.write_text("---\nname: Valid\ndescription: Desc\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "valid.chatmode.md" in content
        assert "README.md" not in content

    def test_empty_directory(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test handles empty directory."""
        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "# Chatmode Inventory" in content

    def test_files_sorted_alphabetically(self, mock_chatmodes_dir, mock_output_path, monkeypatch):
        """Test files are sorted alphabetically."""
        for name in ["zebra", "alpha", "beta"]:
            chatmode = mock_chatmodes_dir / f"{name}.chatmode.md"
            chatmode.write_text(f"---\nname: {name}\ndescription: D\n---\n")

        monkeypatch.setattr("generate_chatmode_inventory.CHATMODES_DIR", mock_chatmodes_dir)
        monkeypatch.setattr("generate_chatmode_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        alpha_pos = content.find("alpha.chatmode.md")
        beta_pos = content.find("beta.chatmode.md")
        zebra_pos = content.find("zebra.chatmode.md")

        assert alpha_pos < beta_pos < zebra_pos

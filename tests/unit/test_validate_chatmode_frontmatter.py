#!/usr/bin/env python3
"""Unit tests for automation/scripts/validate_chatmode_frontmatter.py

Focus: Chatmode frontmatter validation for ai_framework/chatmodes.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from validate_chatmode_frontmatter import (_parse_frontmatter,
                                           _remove_legacy_description, main)


@pytest.mark.unit
class TestParseFrontmatter:
    """Test _parse_frontmatter function."""

    def test_parses_valid_frontmatter(self):
        """Test parses valid frontmatter."""
        lines = [
            "---",
            "name: Test Chatmode",
            "description: A test chatmode",
            "tools:",
            "  - tool1",
            "---",
            "# Content",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "description" in frontmatter
        assert "tools" in frontmatter
        assert end_index == 5

    def test_returns_empty_for_no_start_marker(self):
        """Test returns empty when no start marker."""
        lines = ["# Just a heading", "Content here"]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert frontmatter == {}
        assert end_index == -1

    def test_returns_empty_for_empty_lines(self):
        """Test returns empty for empty lines list."""
        frontmatter, end_index = _parse_frontmatter([])

        assert frontmatter == {}
        assert end_index == -1

    def test_returns_empty_for_unclosed_frontmatter(self):
        """Test returns empty for unclosed frontmatter."""
        lines = ["---", "name: Test", "description: Desc"]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert frontmatter == {}
        assert end_index == -1

    def test_skips_comments_in_frontmatter(self):
        """Test skips comment lines in frontmatter."""
        lines = [
            "---",
            "# This is a comment",
            "name: Test",
            "---",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert len(frontmatter) == 1  # Only 'name', not the comment

    def test_skips_empty_lines_in_frontmatter(self):
        """Test skips empty lines in frontmatter."""
        lines = [
            "---",
            "",
            "name: Test",
            "",
            "description: Desc",
            "---",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "description" in frontmatter

    def test_handles_keys_without_values(self):
        """Test handles keys without values (list indicators)."""
        lines = [
            "---",
            "name: Test",
            "tools:",
            "---",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "tools" in frontmatter
        assert frontmatter["tools"] == ""


@pytest.mark.unit
class TestRemoveLegacyDescription:
    """Test _remove_legacy_description function."""

    def test_removes_legacy_description_line(self):
        """Test removes legacy ## description: line."""
        lines = [
            "---",
            "name: Test",
            "---",
            "# Content",
            "## description: Old description",
            "More content",
        ]

        updated, removed = _remove_legacy_description(lines, 2)

        assert removed is True
        assert "## description:" not in "\n".join(updated)

    def test_keeps_content_before_end_index(self):
        """Test keeps content before end_index."""
        lines = [
            "---",
            "name: Test",
            "## description: In frontmatter area",
            "---",
            "Content",
        ]

        updated, removed = _remove_legacy_description(lines, 3)

        # Should not remove because it's at index 2, not > 3
        assert removed is False
        assert len(updated) == len(lines)

    def test_returns_false_when_no_legacy_found(self):
        """Test returns False when no legacy description found."""
        lines = [
            "---",
            "name: Test",
            "---",
            "# Content",
        ]

        updated, removed = _remove_legacy_description(lines, 2)

        assert removed is False
        assert updated == lines


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_returns_1_for_missing_directory(self, monkeypatch, capsys):
        """Test returns 1 when chatmodes directory missing."""
        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", Path("nonexistent")):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Missing ai_framework/chatmodes" in captured.out

    def test_validates_valid_chatmodes(self, tmp_path, monkeypatch, capsys):
        """Test validates valid chatmodes successfully."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        chatmode = chatmodes_dir / "test.chatmode.md"
        chatmode.write_text("""---
name: Test
description: A test
tools:
  - tool1
---
# Test Content
""")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "validation passed" in captured.out

    def test_detects_missing_frontmatter(self, tmp_path, monkeypatch, capsys):
        """Test detects files with missing frontmatter."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        chatmode = chatmodes_dir / "bad.chatmode.md"
        chatmode.write_text("# No frontmatter here")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "missing or malformed frontmatter" in captured.out

    def test_detects_missing_required_keys(self, tmp_path, monkeypatch, capsys):
        """Test detects missing required keys."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        chatmode = chatmodes_dir / "incomplete.chatmode.md"
        chatmode.write_text("""---
name: Test
---
# Missing description and tools
""")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "missing keys" in captured.out

    def test_detects_legacy_description_line(self, tmp_path, monkeypatch, capsys):
        """Test detects legacy ## description: line."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        chatmode = chatmodes_dir / "legacy.chatmode.md"
        chatmode.write_text("""---
name: Test
description: In frontmatter
tools:
  - tool1
---
# Content

## description: Legacy description here
""")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "legacy '## description:'" in captured.out

    def test_fix_flag_removes_legacy_description(self, tmp_path, monkeypatch, capsys):
        """Test --fix flag removes legacy description lines."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        chatmode = chatmodes_dir / "fixme.chatmode.md"
        chatmode.write_text("""---
name: Test
description: In frontmatter
tools:
  - tool1
---
# Content

## description: Legacy to remove
""")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py", "--fix"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 0
        content = chatmode.read_text()
        assert "## description:" not in content

    def test_reports_multiple_failures(self, tmp_path, monkeypatch, capsys):
        """Test reports multiple validation failures."""
        chatmodes_dir = tmp_path / "chatmodes"
        chatmodes_dir.mkdir()

        (chatmodes_dir / "bad1.chatmode.md").write_text("# No frontmatter")
        (chatmodes_dir / "bad2.chatmode.md").write_text("""---
name: Only name
---
""")

        monkeypatch.setattr(sys, "argv", ["validate_chatmode_frontmatter.py"])
        with patch("validate_chatmode_frontmatter.CHATMODES_DIR", chatmodes_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "bad1.chatmode.md" in captured.out
        assert "bad2.chatmode.md" in captured.out

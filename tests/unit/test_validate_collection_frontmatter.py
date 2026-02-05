#!/usr/bin/env python3
"""Unit tests for automation/scripts/validate_collection_frontmatter.py

Focus: Collection frontmatter validation for ai_framework/collections.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from validate_collection_frontmatter import _parse_frontmatter, main


@pytest.mark.unit
class TestParseFrontmatter:
    """Test _parse_frontmatter function."""

    def test_parses_valid_frontmatter(self):
        """Test parses valid frontmatter."""
        lines = [
            "---",
            "name: Test Collection",
            "description: A test collection",
            "tags:",
            "  - tag1",
            "---",
            "# Content",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "description" in frontmatter
        assert "tags" in frontmatter
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
        assert len(frontmatter) == 1

    def test_handles_keys_without_values(self):
        """Test handles keys without values."""
        lines = [
            "---",
            "name: Test",
            "tags:",
            "---",
        ]

        frontmatter, end_index = _parse_frontmatter(lines)

        assert "tags" in frontmatter


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_returns_1_for_missing_directory(self, monkeypatch, capsys):
        """Test returns 1 when collections directory missing."""
        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", Path("nonexistent")):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Missing ai_framework/collections" in captured.out

    def test_validates_valid_collections(self, tmp_path, monkeypatch, capsys):
        """Test validates valid collections successfully."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "test.collection.md"
        collection.write_text("""---
name: Test
description: A test
tags: []
---
# Test Content
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "validation passed" in captured.out

    def test_validates_yml_files(self, tmp_path, monkeypatch, capsys):
        """Test validates .yml collection files."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "test.collection.yml"
        collection.write_text("""---
name: Test YML
description: A test yml
---
# Content
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        assert result == 0

    def test_skips_special_files(self, tmp_path, monkeypatch, capsys):
        """Test skips INVENTORY.md, SCHEMA.md, README.md."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        # Create special files without frontmatter
        for name in ["INVENTORY.md", "SCHEMA.md", "README.md"]:
            (collections_dir / name).write_text("# Skip me")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        # Should pass because special files are skipped
        assert result == 0

    def test_detects_missing_frontmatter(self, tmp_path, monkeypatch, capsys):
        """Test detects files with missing frontmatter."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "bad.collection.md"
        collection.write_text("# No frontmatter here")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "missing or malformed frontmatter" in captured.out

    def test_detects_missing_required_keys(self, tmp_path, monkeypatch, capsys):
        """Test detects missing required keys."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "incomplete.collection.md"
        collection.write_text("""---
name: Test
---
# Missing description
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "missing keys" in captured.out
        assert "description" in captured.out

    def test_validates_tags_only_if_value_available(self, tmp_path, monkeypatch, capsys):
        """Test tag validation only happens if frontmatter has actual values.

        Note: The simple _parse_frontmatter function only extracts keys, not values.
        Tag validation requires the actual value to be parsed.
        """
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        # This file has valid structure - parser finds the keys
        collection = collections_dir / "tagged.collection.md"
        collection.write_text("""---
name: Test
description: A test
tags:
  - some-tag
---
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            # Empty ALLOWED_TAGS means all tags pass (no validation)
            result = main()

        # Should pass because frontmatter keys are present
        assert result == 0

    def test_accepts_tags_in_allowed_list(self, tmp_path, monkeypatch, capsys):
        """Test accepts tags in allowed list."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "tagged.collection.md"
        collection.write_text("""---
name: Test
description: A test
tags:
  - valid-tag
---
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            with patch("validate_collection_frontmatter.ALLOWED_TAGS", {"valid-tag"}):
                result = main()

        assert result == 0

    def test_handles_string_tags(self, tmp_path, monkeypatch, capsys):
        """Test handles tags as string instead of list."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        collection = collections_dir / "string-tag.collection.md"
        collection.write_text("""---
name: Test
description: A test
tags: single-tag
---
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            # Empty ALLOWED_TAGS means all tags are valid
            result = main()

        assert result == 0

    def test_reports_multiple_failures(self, tmp_path, monkeypatch, capsys):
        """Test reports multiple validation failures."""
        collections_dir = tmp_path / "collections"
        collections_dir.mkdir()

        (collections_dir / "bad1.collection.md").write_text("# No frontmatter")
        (collections_dir / "bad2.collection.yml").write_text("""---
name: Only name
---
""")

        monkeypatch.setattr(sys, "argv", ["validate_collection_frontmatter.py"])
        with patch("validate_collection_frontmatter.COLLECTIONS_DIR", collections_dir):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "bad1.collection.md" in captured.out
        assert "bad2.collection.yml" in captured.out

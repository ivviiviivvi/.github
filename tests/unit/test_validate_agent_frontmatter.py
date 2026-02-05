#!/usr/bin/env python3
"""Unit tests for automation/scripts/validate_agent_frontmatter.py

Focus: YAML frontmatter parsing and validation for agent files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from validate_agent_frontmatter import REQUIRED_KEYS, _parse_frontmatter, main


@pytest.mark.unit
class TestParseFrontmatter:
    """Test frontmatter parsing functionality."""

    def test_valid_frontmatter_returns_dict(self):
        """Test parsing valid frontmatter returns dictionary."""
        lines = [
            "---",
            "name: Test Agent",
            "description: A test agent for validation",
            "---",
            "# Content",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "description" in frontmatter
        assert end_index == 3

    def test_empty_lines_returns_empty_dict(self):
        """Test empty input returns empty dict."""
        frontmatter, end_index = _parse_frontmatter([])

        assert frontmatter == {}
        assert end_index == -1

    def test_missing_opening_delimiter(self):
        """Test missing opening --- returns empty dict."""
        lines = [
            "name: Test Agent",
            "---",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert frontmatter == {}
        assert end_index == -1

    def test_missing_closing_delimiter(self):
        """Test missing closing --- returns empty dict."""
        lines = [
            "---",
            "name: Test Agent",
            "description: No closing delimiter",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert frontmatter == {}
        assert end_index == -1

    def test_empty_frontmatter_block(self):
        """Test empty frontmatter block returns empty dict."""
        lines = [
            "---",
            "---",
            "# Content",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert frontmatter == {}
        assert end_index == 1

    def test_ignores_comments(self):
        """Test comments in frontmatter are ignored."""
        lines = [
            "---",
            "# This is a comment",
            "name: Agent Name",
            "---",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "#" not in frontmatter

    def test_ignores_empty_lines(self):
        """Test empty lines in frontmatter are ignored."""
        lines = [
            "---",
            "",
            "name: Agent Name",
            "",
            "description: Test",
            "---",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert "description" in frontmatter

    def test_handles_key_with_empty_value(self):
        """Test key with empty value after colon."""
        lines = [
            "---",
            "name: ",
            "description: Has content",
            "---",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        assert "name" in frontmatter
        assert frontmatter["name"] == ""

    def test_handles_list_style_key(self):
        """Test key followed by list items (YAML pattern)."""
        lines = [
            "---",
            "tags:",
            "  - tag1",
            "  - tag2",
            "name: Agent",
            "---",
        ]
        frontmatter, end_index = _parse_frontmatter(lines)

        # The parser extracts keys, tags: without value gets empty string
        assert "tags" in frontmatter
        assert "name" in frontmatter


@pytest.mark.unit
class TestRequiredKeys:
    """Test required keys constant."""

    def test_required_keys_includes_name(self):
        """Test name is a required key."""
        assert "name" in REQUIRED_KEYS

    def test_required_keys_includes_description(self):
        """Test description is a required key."""
        assert "description" in REQUIRED_KEYS


@pytest.mark.unit
class TestMainFunction:
    """Test main validation function."""

    @pytest.fixture
    def mock_agents_dir(self, tmp_path):
        """Create mock agents directory with test files."""
        agents_dir = tmp_path / "ai_framework" / "agents"
        agents_dir.mkdir(parents=True)
        return agents_dir

    def test_main_returns_error_when_directory_missing(self, monkeypatch, capsys):
        """Test main returns 1 when agents directory is missing."""
        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            Path("/nonexistent/path"),
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Missing" in captured.out

    def test_main_returns_success_with_valid_files(self, mock_agents_dir, monkeypatch, capsys):
        """Test main returns 0 when all files have valid frontmatter."""
        # Create valid agent file
        agent_file = mock_agents_dir / "test.agent.md"
        agent_file.write_text("---\nname: Test Agent\ndescription: A test agent\n---\n# Content")

        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "passed" in captured.out

    def test_main_returns_error_with_missing_keys(self, mock_agents_dir, monkeypatch, capsys):
        """Test main returns 1 when required keys are missing."""
        # Create agent file missing description
        agent_file = mock_agents_dir / "incomplete.agent.md"
        agent_file.write_text("---\nname: Only Name\n---\n# Content")

        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "failed" in captured.out
        assert "description" in captured.out

    def test_main_returns_error_for_malformed_frontmatter(self, mock_agents_dir, monkeypatch, capsys):
        """Test main returns 1 for files with malformed frontmatter."""
        # Create agent file without frontmatter
        agent_file = mock_agents_dir / "no-frontmatter.agent.md"
        agent_file.write_text("# Just content, no frontmatter")

        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "malformed" in captured.out

    def test_main_handles_empty_directory(self, mock_agents_dir, monkeypatch, capsys):
        """Test main handles empty directory gracefully."""
        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        # No files to validate, should pass
        assert result == 0

    def test_main_validates_multiple_files(self, mock_agents_dir, monkeypatch, capsys):
        """Test main validates all agent files in directory."""
        # Create multiple valid agent files
        for i in range(3):
            agent_file = mock_agents_dir / f"agent-{i}.agent.md"
            agent_file.write_text(f"---\nname: Agent {i}\ndescription: Description {i}\n---\n")

        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        assert result == 0

    def test_main_ignores_non_agent_files(self, mock_agents_dir, monkeypatch, capsys):
        """Test main only validates *.agent.md files."""
        # Create non-agent files
        readme = mock_agents_dir / "README.md"
        readme.write_text("# Readme")

        other = mock_agents_dir / "other.md"
        other.write_text("No frontmatter here")

        # Create valid agent file
        agent_file = mock_agents_dir / "valid.agent.md"
        agent_file.write_text("---\nname: Valid\ndescription: Valid agent\n---\n")

        monkeypatch.setattr(
            "validate_agent_frontmatter.AGENTS_DIR",
            mock_agents_dir,
        )
        monkeypatch.setattr(sys, "argv", ["validate_agent_frontmatter.py"])

        result = main()

        # Should only validate agent files, which is valid
        assert result == 0

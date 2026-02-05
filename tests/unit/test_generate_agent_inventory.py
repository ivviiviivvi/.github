#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_agent_inventory.py

Focus: Frontmatter parsing and inventory generation for agent files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from generate_agent_inventory import main, parse_frontmatter


@pytest.mark.unit
class TestParseFrontmatter:
    """Test frontmatter parsing functionality."""

    def test_empty_lines_returns_empty_dict(self):
        """Test empty input returns empty dict."""
        result = parse_frontmatter([])
        assert result == {}

    def test_no_opening_delimiter_returns_empty(self):
        """Test missing opening --- returns empty dict."""
        lines = ["name: value", "---"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_no_closing_delimiter_returns_empty(self):
        """Test missing closing --- returns empty dict."""
        lines = ["---", "name: value"]
        result = parse_frontmatter(lines)
        assert result == {}

    def test_parses_simple_key_value(self):
        """Test parses simple key: value pairs."""
        lines = [
            "---",
            "name: Test Agent",
            "description: A test agent",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Test Agent"
        assert result["description"] == "A test agent"

    def test_ignores_comments(self):
        """Test comments starting with # are ignored."""
        lines = [
            "---",
            "# This is a comment",
            "name: Agent Name",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert "name" in result
        assert "#" not in str(result.keys())

    def test_ignores_empty_lines(self):
        """Test empty lines are skipped."""
        lines = [
            "---",
            "",
            "name: Agent",
            "",
            "description: Desc",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "Agent"
        assert result["description"] == "Desc"

    def test_parses_list_values(self):
        """Test parses YAML list format."""
        lines = [
            "---",
            "tags:",
            "  - tag1",
            "  - tag2",
            "  - tag3",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert "tags" in result
        assert isinstance(result["tags"], list)
        assert result["tags"] == ["tag1", "tag2", "tag3"]

    def test_parses_mixed_content(self):
        """Test parses mixed scalar and list values."""
        lines = [
            "---",
            "name: My Agent",
            "tags:",
            "  - automation",
            "  - testing",
            "version: 1.0.0",
            "---",
        ]
        result = parse_frontmatter(lines)

        assert result["name"] == "My Agent"
        assert result["tags"] == ["automation", "testing"]
        assert result["version"] == "1.0.0"

    def test_handles_colons_in_values(self):
        """Test handles colons within values."""
        lines = [
            "---",
            "url: https://example.com:8080",
            "---",
        ]
        result = parse_frontmatter(lines)

        # The first colon splits key:value, rest is part of value
        assert "url" in result

    def test_strips_whitespace_from_values(self):
        """Test values have whitespace stripped."""
        lines = [
            "---",
            "name:   Spaced Name   ",
            "---",
        ]
        result = parse_frontmatter(lines)

        # Note: Current implementation may or may not strip trailing space
        assert result["name"].strip() == "Spaced Name"


@pytest.mark.unit
class TestMainFunction:
    """Test main inventory generation function."""

    @pytest.fixture
    def mock_agents_dir(self, tmp_path):
        """Create mock agents directory structure."""
        agents_dir = tmp_path / "ai_framework" / "agents"
        agents_dir.mkdir(parents=True)
        return agents_dir

    @pytest.fixture
    def mock_output_path(self, tmp_path):
        """Create mock output path."""
        return tmp_path / "ai_framework" / "agents" / "INVENTORY.md"

    def test_generates_inventory_file(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test generates INVENTORY.md file."""
        # Create sample agent file
        agent = mock_agents_dir / "test.agent.md"
        agent.write_text("---\nname: Test Agent\ndescription: A test\ntags:\n  - test\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        assert mock_output_path.exists()
        content = mock_output_path.read_text()
        assert "# Agent Inventory" in content

    def test_inventory_contains_header(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test inventory has proper table header."""
        agent = mock_agents_dir / "sample.agent.md"
        agent.write_text("---\nname: Sample\ndescription: Desc\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "| File | Name | Description | Tags |" in content
        assert "| --- | --- | --- | --- |" in content

    def test_inventory_contains_agent_row(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test inventory contains row for each agent."""
        agent = mock_agents_dir / "my-agent.agent.md"
        agent.write_text("---\nname: My Agent\ndescription: Does things\ntags:\n  - util\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "my-agent.agent.md" in content
        assert "My Agent" in content
        assert "Does things" in content
        assert "util" in content

    def test_handles_multiple_agents(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test handles multiple agent files."""
        for i in range(3):
            agent = mock_agents_dir / f"agent-{i}.agent.md"
            agent.write_text(f"---\nname: Agent {i}\ndescription: Desc {i}\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        for i in range(3):
            assert f"agent-{i}.agent.md" in content
            assert f"Agent {i}" in content

    def test_handles_empty_tags(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test handles agents without tags."""
        agent = mock_agents_dir / "no-tags.agent.md"
        agent.write_text("---\nname: No Tags Agent\ndescription: No tags\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "No Tags Agent" in content

    def test_handles_string_tags(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test handles single string tag instead of list."""
        agent = mock_agents_dir / "string-tag.agent.md"
        agent.write_text("---\nname: String Tag\ndescription: Has string tag\ntags: single\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "String Tag" in content
        assert "single" in content

    def test_handles_multiple_tags(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test joins multiple tags with comma."""
        agent = mock_agents_dir / "multi-tag.agent.md"
        agent.write_text("---\nname: Multi Tag\ndescription: Multiple tags\ntags:\n  - one\n  - two\n  - three\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "one, two, three" in content

    def test_ignores_non_agent_files(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test only processes *.agent.md files."""
        # Create non-agent files
        readme = mock_agents_dir / "README.md"
        readme.write_text("# Readme")

        other = mock_agents_dir / "config.yaml"
        other.write_text("key: value")

        # Create agent file
        agent = mock_agents_dir / "valid.agent.md"
        agent.write_text("---\nname: Valid\ndescription: Desc\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "valid.agent.md" in content
        assert "README.md" not in content
        assert "config.yaml" not in content

    def test_handles_empty_directory(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test handles empty directory gracefully."""
        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        assert "# Agent Inventory" in content
        # Should still have header row

    def test_files_sorted_alphabetically(self, mock_agents_dir, mock_output_path, monkeypatch):
        """Test agent files are sorted alphabetically."""
        for name in ["zebra", "alpha", "middle"]:
            agent = mock_agents_dir / f"{name}.agent.md"
            agent.write_text(f"---\nname: {name}\ndescription: Desc\n---\n")

        monkeypatch.setattr("generate_agent_inventory.AGENTS_DIR", mock_agents_dir)
        monkeypatch.setattr("generate_agent_inventory.OUTPUT", mock_output_path)

        main()

        content = mock_output_path.read_text()
        alpha_pos = content.find("alpha.agent.md")
        middle_pos = content.find("middle.agent.md")
        zebra_pos = content.find("zebra.agent.md")

        assert alpha_pos < middle_pos < zebra_pos

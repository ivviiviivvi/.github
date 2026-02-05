#!/usr/bin/env python3
"""Unit tests for automation/scripts/update_agent_docs.py

Focus: Agent documentation table generation and README updates.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from update_agent_docs import extract_metadata, generate_table, main


@pytest.mark.unit
class TestExtractMetadata:
    """Test extract_metadata function."""

    def test_extracts_name_from_frontmatter(self, tmp_path):
        """Test extracts name from frontmatter."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("""---
name: Test Agent
description: 'A test agent'
---
# Test Agent

Content here
""")

        result = extract_metadata(str(agent_file))

        assert result["filename"] == "test.agent.md"
        assert result["description"] == "A test agent"

    def test_extracts_description_without_quotes(self, tmp_path):
        """Test extracts description without quotes."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("""---
name: Test Agent
description: A test agent without quotes
---
# Test Agent
""")

        result = extract_metadata(str(agent_file))

        assert result["description"] == "A test agent without quotes"

    def test_extracts_title_from_heading(self, tmp_path):
        """Test extracts title from markdown heading."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("""---
name: agent-name
---
# Agent Title Here

Content
""")

        result = extract_metadata(str(agent_file))

        assert result["title"] == "Agent Title Here"

    def test_uses_name_when_no_heading(self, tmp_path):
        """Test uses name when no heading present."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("""---
name: Agent Name
description: 'Description'
---
Content without heading
""")

        result = extract_metadata(str(agent_file))

        assert result["title"] == "Agent Name"

    def test_uses_filename_as_fallback(self, tmp_path):
        """Test uses filename when no name found."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("Just some content without frontmatter")

        result = extract_metadata(str(agent_file))

        assert result["title"] == "test.agent.md"
        assert result["filename"] == "test.agent.md"

    def test_returns_default_description_when_missing(self, tmp_path):
        """Test returns default description when missing."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("""---
name: Test
---
# Test
""")

        result = extract_metadata(str(agent_file))

        assert result["description"] == "No description available."

    def test_handles_read_error(self, tmp_path, capsys):
        """Test handles file read error gracefully."""
        result = extract_metadata(str(tmp_path / "nonexistent.agent.md"))

        assert "Error reading file" in result["description"]
        captured = capsys.readouterr()
        assert "Error reading" in captured.out


@pytest.mark.unit
class TestGenerateTable:
    """Test generate_table function."""

    def test_generates_markdown_table(self):
        """Test generates markdown table with headers."""
        agents = [{"filename": "test.agent.md", "title": "Test Agent", "description": "A test"}]

        result = generate_table(agents)

        assert "| Title | Description | MCP Servers |" in result
        assert "| ----- | ----------- | ----------- |" in result

    def test_sorts_agents_by_title(self):
        """Test sorts agents alphabetically by title."""
        agents = [
            {"filename": "c.agent.md", "title": "Charlie", "description": "Third"},
            {"filename": "a.agent.md", "title": "Alpha", "description": "First"},
            {"filename": "b.agent.md", "title": "Beta", "description": "Second"},
        ]

        result = generate_table(agents)

        alpha_pos = result.find("Alpha")
        beta_pos = result.find("Beta")
        charlie_pos = result.find("Charlie")

        assert alpha_pos < beta_pos < charlie_pos

    def test_includes_install_badge(self):
        """Test includes VS Code install badge."""
        agents = [{"filename": "test.agent.md", "title": "Test", "description": "Desc"}]

        result = generate_table(agents)

        assert "Install in VS Code" in result
        assert "img.shields.io/badge/VS_Code-Install" in result

    def test_includes_link_to_agent_file(self):
        """Test includes link to agent file."""
        agents = [{"filename": "test.agent.md", "title": "Test", "description": "Desc"}]

        result = generate_table(agents)

        assert "[Test](../agents/test.agent.md)" in result

    def test_handles_empty_agents_list(self):
        """Test handles empty agents list."""
        result = generate_table([])

        assert "| Title | Description | MCP Servers |" in result
        # Should only have header rows, no data rows
        lines = [l for l in result.strip().split("\n") if l.strip()]
        assert len(lines) == 2  # Header + separator


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_processes_agent_files(self, tmp_path, monkeypatch, capsys):
        """Test processes agent files in agents directory."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        # Create agent file
        agent_file = agents_dir / "test.agent.md"
        agent_file.write_text("""---
name: Test Agent
description: 'A test'
---
# Test Agent
""")

        # Create README with table marker
        readme = docs_dir / "README.agents.md"
        readme.write_text("""# Agents

| Title | Description | MCP Servers |
| ----- | ----------- | ----------- |
| Old | Old data | |
""")

        monkeypatch.chdir(tmp_path)
        with patch("update_agent_docs.AGENTS_DIR", "agents"):
            with patch("update_agent_docs.README_FILE", str(docs_dir / "README.agents.md")):
                main()

        captured = capsys.readouterr()
        assert "Updated" in captured.out

    def test_handles_missing_agents_dir(self, tmp_path, monkeypatch, capsys):
        """Test handles missing agents directory."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        readme = docs_dir / "README.agents.md"
        readme.write_text("""# Agents

| Title | Description | MCP Servers |
""")

        monkeypatch.chdir(tmp_path)
        with patch("update_agent_docs.AGENTS_DIR", "nonexistent"):
            with patch("update_agent_docs.README_FILE", str(readme)):
                main()

        # Should complete without error
        captured = capsys.readouterr()
        # Either updated or error message
        assert True  # No exception raised

    def test_handles_missing_table_marker(self, tmp_path, monkeypatch, capsys):
        """Test handles README without table marker."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        readme = docs_dir / "README.agents.md"
        readme.write_text("# Agents\n\nNo table here")

        monkeypatch.chdir(tmp_path)
        with patch("update_agent_docs.AGENTS_DIR", "agents"):
            with patch("update_agent_docs.README_FILE", str(readme)):
                main()

        captured = capsys.readouterr()
        assert "Could not find table header" in captured.out

    def test_only_processes_agent_md_files(self, tmp_path, monkeypatch):
        """Test only processes .agent.md files."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        # Create various files
        (agents_dir / "test.agent.md").write_text("---\nname: Test\n---\n# Test")
        (agents_dir / "other.md").write_text("# Not an agent")
        (agents_dir / "readme.txt").write_text("Not markdown")

        readme = docs_dir / "README.agents.md"
        readme.write_text("| Title | Description | MCP Servers |\n| ----- | ----------- | ----------- |")

        monkeypatch.chdir(tmp_path)
        with patch("update_agent_docs.AGENTS_DIR", "agents"):
            with patch("update_agent_docs.README_FILE", str(readme)):
                main()

        content = readme.read_text()
        assert "test.agent.md" in content
        assert "other.md" not in content
        assert "readme.txt" not in content

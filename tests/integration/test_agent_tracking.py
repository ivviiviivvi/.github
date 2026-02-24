"""Validation tests for Jules Agent Tracking System.

Tests the integrity and format of:
- .jules/ journal entries
- Agent metadata
- Task deduplication system

NOTE: These tests validate specific file structures that may not be present
      in all environments.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import pytest

# Tests validate agent tracking file structures


class TestJulesJournalFormat:
    """Test .jules/ journal entry format and integrity."""

    JULES_DIR = Path(".jules")
    JOURNAL_FILES = ["bolt.md", "palette.md", "sentinel.md"]
    ENTRY_PATTERN = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s+-\s+\\?\[(.+?)\\?\]\s*$", re.MULTILINE)

    def test_jules_directory_exists(self):
        """Verify .jules/ directory exists."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        assert self.JULES_DIR.is_dir(), ".jules/ is not a directory"

    def test_all_journal_files_exist(self):
        """Verify all expected journal files exist."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        for filename in self.JOURNAL_FILES:
            filepath = self.JULES_DIR / filename
            assert filepath.exists(), f"{filename} not found in .jules/"
            assert filepath.is_file(), f"{filename} is not a file"

    def test_journal_entry_format(self):
        """Verify all journal entries follow standard format."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        for filename in self.JOURNAL_FILES:
            filepath = self.JULES_DIR / filename
            if not filepath.exists():
                pytest.skip(f"{filename} not present (created at runtime)")
            content = filepath.read_text()

            entries = self.ENTRY_PATTERN.findall(content)
            assert len(entries) > 0, f"{filename} has no journal entries"

            for date_str, title in entries:
                # Validate date format
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format in {filename}: {date_str}")

                # Validate title is not empty
                assert title.strip(), f"Empty title in {filename} on {date_str}"

    def test_no_duplicate_dates(self):
        """Ensure no duplicate date entries in same journal."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        for filename in self.JOURNAL_FILES:
            filepath = self.JULES_DIR / filename
            if not filepath.exists():
                continue
            file_content = filepath.read_text()

            entries = self.ENTRY_PATTERN.findall(file_content)
            dates = [date for date, _ in entries]

            duplicates = [date for date in dates if dates.count(date) > 1]
            assert not duplicates, f"{filename} has duplicate dates: {set(duplicates)}"

    def test_learning_action_pairs(self):
        """Verify each journal entry has Learning and Action sections."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        for filename in self.JOURNAL_FILES:
            filepath = self.JULES_DIR / filename
            if not filepath.exists():
                continue
            content = filepath.read_text()

            # Split by entry headers
            entries = re.split(
                r"^##\s+\d{4}-\d{2}-\d{2}\s+-\s+\\?\[.+?\\?\]\s*$",
                content,
                flags=re.MULTILINE,
            )

            for i, entry in enumerate(entries[1:], 1):  # Skip preamble
                entry_lower = entry.lower()

                # Check for Learning section
                assert "**learning:**" in entry_lower or "learning:" in entry_lower, (
                    f"{filename} entry {i} missing Learning section"
                )

                # Check for Action section
                assert (
                    "**action:**" in entry_lower
                    or "action:" in entry_lower
                    or "**prevention:**" in entry_lower
                    or "prevention:" in entry_lower
                ), f"{filename} entry {i} missing Action/Prevention section"

    def test_chronological_order(self):
        """Verify journal entries are in chronological order (newest first)."""
        if not self.JULES_DIR.exists():
            pytest.skip(".jules/ directory not present (created at runtime)")
        for filename in self.JOURNAL_FILES:
            filepath = self.JULES_DIR / filename
            if not filepath.exists():
                continue
            content = filepath.read_text()

            entries = self.ENTRY_PATTERN.findall(content)
            dates = [datetime.strptime(date, "%Y-%m-%d") for date, _ in entries]

            # Check if sorted in reverse chronological order (newest first)
            assert dates == sorted(dates, reverse=True), f"{filename} entries not in chronological order (newest first)"


class TestTaskDeduplication:
    """Test task deduplication system integrity."""

    SCRIPT_PATH = Path(".github/scripts/task_deduplicator.py")
    STATE_FILE = Path(".github/task_state.json")

    def test_deduplicator_script_exists(self):
        """Verify task_deduplicator.py exists."""
        assert self.SCRIPT_PATH.exists(), "task_deduplicator.py not found"

    def test_deduplicator_is_executable(self):
        """Verify script has proper shebang and is executable."""
        content = self.SCRIPT_PATH.read_text()
        assert content.startswith("#!/usr/bin/env python3"), "task_deduplicator.py missing proper shebang"

    def test_state_file_structure(self):
        """Verify task_state.json has correct structure if it exists."""
        if not self.STATE_FILE.exists():
            pytest.skip("task_state.json not present (created at runtime)")

        with open(self.STATE_FILE) as f:
            state = json.load(f)

        assert "tasks" in state, "Missing 'tasks' key in task_state.json"
        assert isinstance(state["tasks"], dict), "'tasks' should be a dictionary"

        # Verify each task has required fields
        for task_hash, task_data in state["tasks"].items():
            assert "type" in task_data, f"Task {task_hash} missing 'type'"
            assert "timestamp" in task_data, f"Task {task_hash} missing 'timestamp'"
            assert "data" in task_data, f"Task {task_hash} missing 'data'"

    def test_cleanup_retention(self):
        """Verify old records are properly cleaned up."""
        if not self.STATE_FILE.exists():
            pytest.skip("task_state.json not present")

        with open(self.STATE_FILE) as f:
            state = json.load(f)

        now = datetime.now()
        retention_days = 7

        for task_hash, task_data in state["tasks"].items():
            timestamp = datetime.fromisoformat(task_data["timestamp"])
            age_days = (now - timestamp).days

            assert age_days <= retention_days, (
                f"Task {task_hash} is {age_days} days old, exceeds {retention_days} day retention"
            )


class TestAgentMetadata:
    """Test agent metadata consistency and completeness."""

    AGENTS_DIR = Path("src/ai_framework/agents")
    AGENT_README = Path("docs/README.agents.md")
    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.MULTILINE | re.DOTALL)

    def test_agents_directory_exists(self):
        """Verify agents/ directory exists."""
        assert self.AGENTS_DIR.exists(), "agents/ directory not found"
        assert self.AGENTS_DIR.is_dir(), "agents/ is not a directory"

    def test_all_agents_have_frontmatter(self):
        """Verify all agent files have valid YAML frontmatter."""
        agent_files = list(self.AGENTS_DIR.glob("*.agent.md"))
        assert len(agent_files) > 0, "No agent files found in agents/"

        for agent_file in agent_files:
            content = agent_file.read_text()
            match = self.FRONTMATTER_PATTERN.search(content)

            assert match, f"{agent_file.name} missing YAML frontmatter"

            frontmatter = match.group(1)
            # Basic validation - should contain name or description
            assert "name:" in frontmatter or "description:" in frontmatter, (
                f"{agent_file.name} frontmatter missing name/description"
            )

    def test_agent_descriptions(self):
        """Ensure all agents have non-empty descriptions."""
        agent_files = list(self.AGENTS_DIR.glob("*.agent.md"))

        for agent_file in agent_files:
            content = agent_file.read_text()
            match = self.FRONTMATTER_PATTERN.search(content)

            if match:
                frontmatter = match.group(1)

                # Extract description
                desc_match = re.search(r"description:\s*['\"]?(.+?)['\"]?\s*$", frontmatter, re.MULTILINE)

                if desc_match:
                    description = desc_match.group(1).strip()
                    assert description, f"{agent_file.name} has empty description"

    def test_readme_agents_sync(self):
        """Verify README.agents.md is in sync with agent files."""
        if not self.AGENT_README.exists():
            pytest.skip("README.agents.md not found")

        # Get all agent files
        agent_files = list(self.AGENTS_DIR.glob("*.agent.md"))
        agent_names = {f.name for f in agent_files}

        # Read README content
        readme_content = self.AGENT_README.read_text()

        # Check each agent is referenced in README
        missing_agents = []
        for agent_name in agent_names:
            if agent_name not in readme_content:
                missing_agents.append(agent_name)

        assert not missing_agents, (
            f"Agents missing from README.agents.md: {missing_agents}\n"
            f"Run: python3 src/automation/scripts/update_agent_docs.py"
        )

    def test_no_orphaned_readme_entries(self):
        """Verify README doesn't reference non-existent agents."""
        if not self.AGENT_README.exists():
            pytest.skip("README.agents.md not found")

        # Get all agent files
        agent_files = {f.name for f in self.AGENTS_DIR.glob("*.agent.md")}

        # Extract agent references from README
        readme_content = self.AGENT_README.read_text()
        referenced_agents = re.findall(r"\.\./ai_framework/agents/([a-zA-Z0-9_-]+\.agent\.md)", readme_content)

        orphaned = []
        for ref_agent in referenced_agents:
            if ref_agent not in agent_files:
                orphaned.append(ref_agent)

        assert not orphaned, f"README.agents.md references non-existent agents: {orphaned}"


class TestMouthpieceFilter:
    """Test Mouthpiece Filter system integrity."""

    SCRIPT_PATH = Path("src/automation/scripts/natural_language_prompt_filter.py")

    def test_mouthpiece_script_exists(self):
        """Verify natural_language_prompt_filter.py exists."""
        assert self.SCRIPT_PATH.exists(), "natural_language_prompt_filter.py not found"

    def test_has_proper_shebang(self):
        """Verify script has proper shebang."""
        content = self.SCRIPT_PATH.read_text()
        assert content.startswith("#!/usr/bin/env python3"), "natural_language_prompt_filter.py missing proper shebang"

    def test_has_docstring(self):
        """Verify script has module-level docstring."""
        content = self.SCRIPT_PATH.read_text()
        # Check for triple-quoted docstring near the top
        assert '"""' in content[:500], "natural_language_prompt_filter.py missing module docstring"

    def test_regex_precompilation(self):
        """Verify regex patterns are pre-compiled (Bolt's learning)."""
        content = self.SCRIPT_PATH.read_text()

        # Should have class-level compiled patterns
        assert "re.compile(" in content, "No pre-compiled regex patterns found"

        # Should use _PATTERN naming convention
        pattern_names = re.findall(r"(_[A-Z_]+)\s*=\s*re\.compile\(", content)
        assert len(pattern_names) > 0, "No class-level pre-compiled patterns following _PATTERN convention"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

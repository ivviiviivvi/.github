#!/usr/bin/env python3
"""Unit tests for automation/scripts/resolve_dependencies.py

Focus: Dependency resolution and conflict detection.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from resolve_dependencies import DependencyResolver, main


@pytest.mark.unit
class TestDependencyResolverInit:
    """Test DependencyResolver initialization."""

    def test_default_root_path(self):
        """Test uses current directory as default."""
        resolver = DependencyResolver()

        assert resolver.root_path == Path(".")

    def test_custom_root_path(self, tmp_path):
        """Test accepts custom root path."""
        resolver = DependencyResolver(tmp_path)

        assert resolver.root_path == tmp_path

    def test_initializes_empty_dependencies(self):
        """Test initializes with empty dependencies."""
        resolver = DependencyResolver()

        assert resolver.dependencies == {}
        assert resolver.conflicts == []


@pytest.mark.unit
class TestScanDependencies:
    """Test scan_dependencies method."""

    def test_scans_requirements_txt(self, tmp_path):
        """Test scans requirements.txt file."""
        (tmp_path / "requirements.txt").write_text("""
requests>=2.28.0
pytest==7.4.0
flask[async]>=2.0
# Comment line
numpy
""")

        resolver = DependencyResolver(tmp_path)
        result = resolver.scan_dependencies()

        deps = result[str(tmp_path / "requirements.txt")]
        assert "requests" in deps
        assert "pytest" in deps
        assert "flask" in deps
        assert "numpy" in deps

    def test_scans_package_json(self, tmp_path):
        """Test scans package.json file."""
        package_data = {
            "dependencies": {"express": "^4.18.0", "lodash": "^4.17.0"},
            "devDependencies": {"jest": "^29.0.0"},
        }
        (tmp_path / "package.json").write_text(json.dumps(package_data))

        resolver = DependencyResolver(tmp_path)
        result = resolver.scan_dependencies()

        deps = result[str(tmp_path / "package.json")]
        assert "express" in deps
        assert "lodash" in deps
        assert "jest" in deps

    def test_handles_missing_files(self, tmp_path):
        """Test handles missing dependency files."""
        resolver = DependencyResolver(tmp_path)
        result = resolver.scan_dependencies()

        assert result == {}

    def test_scans_multiple_files(self, tmp_path):
        """Test scans all present dependency files."""
        (tmp_path / "requirements.txt").write_text("requests\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"express": "1.0"}}')

        resolver = DependencyResolver(tmp_path)
        result = resolver.scan_dependencies()

        assert len(result) == 2


@pytest.mark.unit
class TestParseDependencyFile:
    """Test _parse_dependency_file method."""

    def test_parses_requirements_with_version_specifiers(self, tmp_path):
        """Test parses various version specifiers."""
        (tmp_path / "requirements.txt").write_text("""
package1==1.0.0
package2>=2.0.0
package3<=3.0.0
package4[extra]>=1.0
""")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "requirements.txt")

        assert "package1" in deps
        assert "package2" in deps
        assert "package3" in deps
        assert "package4" in deps

    def test_skips_comments_and_empty_lines(self, tmp_path):
        """Test skips comments and empty lines."""
        (tmp_path / "requirements.txt").write_text("""
# Comment
package1

# Another comment
package2
""")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "requirements.txt")

        assert len(deps) == 2
        assert "package1" in deps
        assert "package2" in deps

    def test_handles_invalid_package_json(self, tmp_path):
        """Test handles invalid package.json."""
        (tmp_path / "package.json").write_text("invalid json {")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "package.json")

        assert deps == []

    def test_handles_package_json_without_dependencies(self, tmp_path):
        """Test handles package.json with no dependencies."""
        (tmp_path / "package.json").write_text('{"name": "test"}')

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "package.json")

        assert deps == []


@pytest.mark.unit
class TestFindConflicts:
    """Test find_conflicts method."""

    def test_finds_multiple_declarations(self, tmp_path):
        """Test finds dependencies declared in multiple files."""
        (tmp_path / "requirements.txt").write_text("requests\nflask\n")
        (tmp_path / "package.json").write_text(
            '{"dependencies": {"requests": "1.0", "express": "1.0"}}'
        )

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        conflicts = resolver.find_conflicts()

        # 'requests' appears in both
        assert len(conflicts) == 1
        assert conflicts[0]["dependency"] == "requests"
        assert conflicts[0]["type"] == "multiple_declaration"

    def test_no_conflicts_when_unique(self, tmp_path):
        """Test no conflicts when deps are unique."""
        (tmp_path / "requirements.txt").write_text("flask\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"express": "1.0"}}')

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        conflicts = resolver.find_conflicts()

        assert conflicts == []

    def test_stores_conflicts_on_instance(self, tmp_path):
        """Test stores conflicts on resolver instance."""
        (tmp_path / "requirements.txt").write_text("shared\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"shared": "1.0"}}')

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        resolver.find_conflicts()

        assert len(resolver.conflicts) == 1


@pytest.mark.unit
class TestResolve:
    """Test resolve method."""

    def test_resolves_multiple_declaration(self, tmp_path):
        """Test resolves multiple declaration conflict."""
        resolver = DependencyResolver(tmp_path)
        conflict = {
            "type": "multiple_declaration",
            "dependency": "test",
            "files": ["a.txt", "b.json"],
            "severity": "warning",
        }

        result = resolver.resolve(conflict)

        assert result is True

    def test_returns_false_for_unknown_type(self, tmp_path):
        """Test returns False for unknown conflict type."""
        resolver = DependencyResolver(tmp_path)
        conflict = {
            "type": "unknown_conflict",
            "dependency": "test",
        }

        result = resolver.resolve(conflict)

        assert result is False


@pytest.mark.unit
class TestGenerateReport:
    """Test generate_report method."""

    def test_generates_markdown_report(self, tmp_path):
        """Test generates Markdown formatted report."""
        (tmp_path / "requirements.txt").write_text("flask\nrequests\n")

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        resolver.find_conflicts()
        report = resolver.generate_report()

        assert "# Dependency Analysis Report" in report
        assert "## Summary" in report

    def test_includes_file_counts(self, tmp_path):
        """Test includes file and dependency counts."""
        (tmp_path / "requirements.txt").write_text("flask\nrequests\n")

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        resolver.find_conflicts()
        report = resolver.generate_report()

        assert "Total files scanned: 1" in report
        assert "2 dependencies" in report

    def test_includes_conflicts_section(self, tmp_path):
        """Test includes conflicts in report."""
        (tmp_path / "requirements.txt").write_text("shared\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"shared": "1.0"}}')

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        resolver.find_conflicts()
        report = resolver.generate_report()

        assert "## Conflicts" in report
        assert "shared" in report

    def test_no_conflicts_section_when_none(self, tmp_path):
        """Test no conflicts section when none exist."""
        (tmp_path / "requirements.txt").write_text("flask\n")

        resolver = DependencyResolver(tmp_path)
        resolver.scan_dependencies()
        resolver.find_conflicts()
        report = resolver.generate_report()

        assert "## Conflicts" not in report


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_check_no_conflicts(self, tmp_path, monkeypatch, capsys):
        """Test main --check with no conflicts."""
        (tmp_path / "requirements.txt").write_text("flask\n")

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["resolve_dependencies.py", "--check"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "No conflicts found" in captured.out

    def test_main_check_with_conflicts(self, tmp_path, monkeypatch, capsys):
        """Test main --check with conflicts."""
        (tmp_path / "requirements.txt").write_text("shared\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"shared": "1.0"}}')

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["resolve_dependencies.py", "--check"])

        result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "1 dependency conflicts" in captured.out

    def test_main_resolve(self, tmp_path, monkeypatch, capsys):
        """Test main --resolve."""
        (tmp_path / "requirements.txt").write_text("shared\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"shared": "1.0"}}')

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["resolve_dependencies.py", "--resolve"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Resolved 1/1 conflicts" in captured.out

    def test_main_report(self, tmp_path, monkeypatch, capsys):
        """Test main --report."""
        (tmp_path / "requirements.txt").write_text("flask\n")

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["resolve_dependencies.py", "--report"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Dependency Analysis Report" in captured.out

    def test_main_no_args_shows_help(self, monkeypatch, capsys):
        """Test main without args shows help."""
        monkeypatch.setattr(sys, "argv", ["resolve_dependencies.py"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "--check" in captured.out or "--resolve" in captured.out


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases."""

    def test_handles_empty_requirements(self, tmp_path):
        """Test handles empty requirements.txt."""
        (tmp_path / "requirements.txt").write_text("")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "requirements.txt")

        assert deps == []

    def test_handles_whitespace_only_requirements(self, tmp_path):
        """Test handles whitespace-only requirements.txt."""
        (tmp_path / "requirements.txt").write_text("   \n\n   \n")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "requirements.txt")

        assert deps == []

    def test_handles_complex_version_specifiers(self, tmp_path):
        """Test handles complex version specifiers."""
        # The parser only handles ==, >=, <=, and [ - other specifiers are kept intact
        (tmp_path / "requirements.txt").write_text("""
package>=1.0,<2.0
other>=1.4.2
another<=1.5.0
""")

        resolver = DependencyResolver(tmp_path)
        deps = resolver._parse_dependency_file(tmp_path / "requirements.txt")

        assert "package" in deps
        assert "other" in deps
        assert "another" in deps

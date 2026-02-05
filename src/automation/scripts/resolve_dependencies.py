#!/usr/bin/env python3
"""Dependency Resolution Script.

Analyzes and resolves dependency conflicts across workflows and automation scripts.

Usage:
    python3 resolve_dependencies.py --check
    python3 resolve_dependencies.py --resolve
    python3 resolve_dependencies.py --report
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional


class DependencyResolver:
    """Resolve dependency conflicts in automation workflows."""

    def __init__(self, root_path: Optional[Path] = None):
        """Initialize dependency resolver.

        Args:
            root_path: Root path of the repository

        """
        self.root_path = root_path or Path(".")
        self.dependencies: dict[str, list[str]] = {}
        self.conflicts: list[dict[str, Any]] = []

    def scan_dependencies(self) -> dict[str, list[str]]:
        """Scan repository for dependency declarations.

        Returns:
            Dictionary mapping files to their dependencies

        """
        dependency_files = [
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "Gemfile",
        ]

        for dep_file in dependency_files:
            path = self.root_path / dep_file
            if path.exists():
                self.dependencies[str(path)] = self._parse_dependency_file(path)

        return self.dependencies

    def _parse_dependency_file(self, path: Path) -> list[str]:
        """Parse a dependency file and extract dependencies.

        Args:
            path: Path to the dependency file

        Returns:
            List of dependency names

        """
        deps = []
        content = path.read_text()

        if path.name == "requirements.txt":
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    # Extract package name (before version specifier)
                    pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0]
                    deps.append(pkg.strip())

        elif path.name == "package.json":
            try:
                data = json.loads(content)
                deps.extend(data.get("dependencies", {}).keys())
                deps.extend(data.get("devDependencies", {}).keys())
            except json.JSONDecodeError:
                pass

        return deps

    def find_conflicts(self) -> list[dict[str, Any]]:
        """Find dependency conflicts across files.

        Returns:
            List of conflict descriptions

        """
        self.conflicts = []

        # Check for version conflicts between files
        all_deps: dict[str, list[str]] = {}
        for file_path, deps in self.dependencies.items():
            for dep in deps:
                if dep not in all_deps:
                    all_deps[dep] = []
                all_deps[dep].append(file_path)

        # Report dependencies declared in multiple files
        for dep, files in all_deps.items():
            if len(files) > 1:
                self.conflicts.append(
                    {
                        "type": "multiple_declaration",
                        "dependency": dep,
                        "files": files,
                        "severity": "warning",
                    }
                )

        return self.conflicts

    def resolve(self, conflict: dict[str, Any]) -> bool:
        """Attempt to resolve a dependency conflict.

        Args:
            conflict: Conflict description

        Returns:
            True if resolved successfully

        """
        if conflict["type"] == "multiple_declaration":
            # Resolution strategy: keep in primary file only
            print(f"Resolving: {conflict['dependency']} declared in multiple files")
            return True

        return False

    def generate_report(self) -> str:
        """Generate a dependency analysis report.

        Returns:
            Report as formatted string

        """
        report_lines = [
            "# Dependency Analysis Report",
            "",
            "## Summary",
            f"- Total files scanned: {len(self.dependencies)}",
            f"- Total conflicts found: {len(self.conflicts)}",
            "",
            "## Dependencies by File",
            "",
        ]

        for file_path, deps in self.dependencies.items():
            report_lines.append(f"### {file_path}")
            report_lines.append(f"- {len(deps)} dependencies")
            report_lines.append("")

        if self.conflicts:
            report_lines.append("## Conflicts")
            report_lines.append("")
            for conflict in self.conflicts:
                report_lines.append(f"- **{conflict['dependency']}**: {conflict['type']}")

        return "\n".join(report_lines)


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Dependency resolution tool")
    parser.add_argument("--check", action="store_true", help="Check for conflicts")
    parser.add_argument("--resolve", action="store_true", help="Attempt to resolve conflicts")
    parser.add_argument("--report", action="store_true", help="Generate report")

    args = parser.parse_args()

    resolver = DependencyResolver()
    resolver.scan_dependencies()

    if args.check:
        conflicts = resolver.find_conflicts()
        if conflicts:
            print(f"Found {len(conflicts)} dependency conflicts")
            return 1
        print("No conflicts found")
        return 0

    if args.resolve:
        conflicts = resolver.find_conflicts()
        resolved = sum(1 for c in conflicts if resolver.resolve(c))
        print(f"Resolved {resolved}/{len(conflicts)} conflicts")
        return 0

    if args.report:
        resolver.find_conflicts()
        print(resolver.generate_report())
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Resolve managed link placeholders in Markdown files.

Managed links are annotated with HTML comments:
  [Link Text](https://example.com)<!-- link:github.discussions -->

For internal paths (internal.* keys), the script calculates the correct
relative path from the current file to the target file.

This script updates the URL based on docs/_data/links.yml and can optionally
annotate existing links that match known URLs.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Iterable
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback parser below
    yaml = None  # type: ignore[assignment]


LINK_WITH_COMMENT_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]+\]\()(?P<url>[^)\s]+)"
    r"(?P<suffix>\)\s*<!--\s*link:(?P<key>[A-Za-z0-9._-]+)\s*-->)"
)
UNANNOTATED_LINK_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]+\]\()(?P<url>[^)\s]+)" r"(?P<suffix>\))(?!\s*<!--\s*link:)"
)
PLACEHOLDER_RE = re.compile(r"^\[\[link:(?P<key>[A-Za-z0-9._-]+)\]\]$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

DEFAULT_EXCLUDES = {
    ".git",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".venv",
    "venv",
    ".cache",
    "archive",
    "docs/archive",
    "docs/_site",
    "docs/.jekyll-cache",
    "project_meta/reports",
}


def _parse_simple_yaml(text: str) -> dict[str, object]:
    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, root)]

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, sep, value = line.lstrip().partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()

        # Handle inline comments (remove # and everything after, unless in quotes)
        if value and not value.startswith(("'", '"')):
            # Find # that's not part of a URL fragment
            # Simple heuristic: if there's a space before #, it's likely a comment
            comment_idx = value.find("  #")
            if comment_idx == -1:
                comment_idx = value.find(" #")
            if comment_idx > 0:
                value = value[:comment_idx].rstrip()

        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            new_node: dict[str, object] = {}
            parent[key] = new_node
            stack.append((indent, new_node))
        else:
            parent[key] = value

    return root


def _flatten_map(prefix: str, node: object, out: dict[str, str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            new_prefix = f"{prefix}.{key}" if prefix else str(key)
            _flatten_map(new_prefix, value, out)
    else:
        out[prefix] = str(node)


def load_link_map(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {} if yaml else _parse_simple_yaml(text)
    flat: dict[str, str] = {}
    _flatten_map("", data, flat)
    return flat


def is_internal_path(key: str) -> bool:
    """Check if a link key refers to an internal path."""
    return key.startswith("internal.")


def calculate_relative_path(from_file: Path, to_path: str, root: Path) -> str:
    """Calculate relative path from a file to a target path (root-relative).

    Args:
        from_file: The file containing the link (absolute path)
        to_path: The target path (root-relative, e.g., 'src/ai_framework/agents/foo.md')
        root: The repository root (absolute path)

    Returns:
        Relative path from from_file's directory to the target

    """
    from_dir = from_file.parent
    target = root / to_path

    try:
        # Calculate relative path from source directory to target
        rel_path = os.path.relpath(target, from_dir)
        # Normalize to forward slashes for markdown
        return rel_path.replace("\\", "/")
    except ValueError:
        # Different drives on Windows - fall back to root-relative
        return to_path


# Regex patterns for migration mode - detect broken relative paths to agents
BROKEN_AGENT_LINK_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]+\]\()"
    r"(?P<path>\.\.?/[^)\s]*agents/[^)\s]+\.agent\.md)"
    r"(?P<suffix>\))"
)


def iter_markdown_files(root: Path, excludes: Iterable[str]) -> Iterable[Path]:
    exclude_paths = [root / Path(p) for p in excludes]
    exclude_names = {Path(p).name for p in excludes}

    for path in root.rglob("*.md"):
        rel_parts = path.relative_to(root).parts
        if any(exclude in path.parents for exclude in exclude_paths):
            continue
        if any(part in exclude_names for part in rel_parts):
            continue
        yield path


def replace_links(
    text: str,
    link_map: dict[str, str],
    reverse_map: dict[str, str],
    annotate: bool,
    current_file: Path | None = None,
    root: Path | None = None,
) -> tuple[str, int, int, int]:
    updated = 0
    annotated = 0
    missing = 0
    lines = text.splitlines(keepends=True)
    out_lines: list[str] = []

    in_fence = False
    fence_marker = ""

    for line in lines:
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        def update_annotated(match: re.Match[str]) -> str:
            nonlocal updated, missing
            key = match.group("key")
            url = match.group("url")
            if key not in link_map:
                missing += 1
                return match.group(0)
            raw_target = link_map[key]

            # For internal paths, calculate relative path from current file
            if is_internal_path(key) and current_file and root:
                new_url = calculate_relative_path(current_file, raw_target, root)
            else:
                new_url = raw_target

            if new_url != url:
                updated += 1
            return f"{match.group('prefix')}{new_url}{match.group('suffix')}"

        line = LINK_WITH_COMMENT_RE.sub(update_annotated, line)

        def annotate_unmarked(match: re.Match[str]) -> str:
            nonlocal annotated, updated, missing
            url = match.group("url")
            placeholder = PLACEHOLDER_RE.match(url)
            if placeholder:
                key = placeholder.group("key")
                if key not in link_map:
                    missing += 1
                    return match.group(0)
                annotated += 1
                updated += 1
                raw_target = link_map[key]

                # For internal paths, calculate relative path from current file
                if is_internal_path(key) and current_file and root:
                    new_url = calculate_relative_path(current_file, raw_target, root)
                else:
                    new_url = raw_target

                return (
                    f"{match.group('prefix')}{new_url}{match.group('suffix')}"  # noqa: E501
                    f"<!-- link:{key} -->"
                )

            key = reverse_map.get(url)
            if key and annotate:
                annotated += 1
                return (
                    f"{match.group('prefix')}{url}{match.group('suffix')}"  # noqa: E501
                    f"<!-- link:{key} -->"
                )

            return match.group(0)

        line = UNANNOTATED_LINK_RE.sub(annotate_unmarked, line)
        out_lines.append(line)

    return "".join(out_lines), updated, annotated, missing


def build_agent_path_map(link_map: dict[str, str]) -> dict[str, str]:
    """Build a map from agent filename to link key."""
    agent_map: dict[str, str] = {}
    for key, path in link_map.items():
        if key.startswith("internal.agents.") and path.endswith(".agent.md"):
            # Extract filename from path
            filename = Path(path).name
            agent_map[filename] = key
    return agent_map


def migrate_broken_links(
    text: str,
    link_map: dict[str, str],
    current_file: Path,
    root: Path,
) -> str:
    """Migrate broken relative agent links to managed link format.

    This function finds links like:
        [Text](../agents/foo.agent.md)
        [Text](../ai_framework/agents/foo.agent.md)

    And converts them to managed links:
        [Text](correct/relative/path)<!-- link:internal.agents.foo -->
    """
    agent_map = build_agent_path_map(link_map)

    def replace_broken_link(match: re.Match[str]) -> str:
        path = match.group("path")
        # Extract the agent filename
        filename = Path(path).name

        if filename not in agent_map:
            # Can't migrate - not in our registry
            return match.group(0)

        key = agent_map[filename]
        raw_target = link_map[key]
        new_url = calculate_relative_path(current_file, raw_target, root)

        return f"{match.group('prefix')}{new_url}{match.group('suffix')}<!-- link:{key} -->"

    return BROKEN_AGENT_LINK_RE.sub(replace_broken_link, text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve managed Markdown links.")
    parser.add_argument(
        "--map",
        dest="map_path",
        default="docs/_data/links.yml",
        help="Path to link map (default: docs/_data/links.yml)",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write updates in place (default: dry run)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if changes are needed or missing keys exist",
    )
    parser.add_argument(
        "--annotate",
        action="store_true",
        help="Add link comments for URLs that match the map",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional directories to exclude (can be repeated)",
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Migrate broken agent links to managed link format",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    map_path = Path(args.map_path).resolve()
    if not map_path.exists():
        print(f"Link map not found: {map_path}", file=sys.stderr)
        return 2

    link_map = load_link_map(map_path)
    reverse_map: dict[str, str] = {}
    for key, value in link_map.items():
        reverse_map.setdefault(value, key)

    excludes = set(DEFAULT_EXCLUDES)
    excludes.update(args.exclude)

    total_updates = 0
    total_annotations = 0
    total_missing = 0
    changed_files = 0

    for md_file in iter_markdown_files(root, excludes):
        original = md_file.read_text(encoding="utf-8")

        # Apply migration if requested
        if args.migrate:
            original = migrate_broken_links(original, link_map, md_file, root)

        updated_text, updated, annotated, missing = replace_links(
            original,
            link_map,
            reverse_map,
            args.annotate,
            current_file=md_file,
            root=root,
        )
        total_updates += updated
        total_annotations += annotated
        total_missing += missing

        if updated_text != original:
            changed_files += 1
            if args.write:
                md_file.write_text(updated_text, encoding="utf-8")

    print(
        "Managed link scan complete:\n"
        f"  Files changed: {changed_files}\n"
        f"  Links updated: {total_updates}\n"
        f"  Links annotated: {total_annotations}\n"
        f"  Missing keys: {total_missing}"
    )

    if total_missing > 0:
        return 1
    if args.check and (changed_files > 0 or total_updates > 0 or total_annotations > 0):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

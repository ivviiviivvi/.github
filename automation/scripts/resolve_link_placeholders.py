#!/usr/bin/env python3
"""
Resolve managed link placeholders in Markdown files.

Managed links are annotated with HTML comments:
  [Link Text](https://example.com)<!-- link:github.discussions -->

This script updates the URL based on docs/_data/links.yml and can optionally
annotate existing links that match known URLs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback parser below
    yaml = None


LINK_WITH_COMMENT_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]+\]\()(?P<url>[^)\s]+)(?P<suffix>\)\s*<!--\s*link:(?P<key>[A-Za-z0-9._-]+)\s*-->)"
)
UNANNOTATED_LINK_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]+\]\()(?P<url>[^)\s]+)(?P<suffix>\))(?!\s*<!--\s*link:)"
)
PLACEHOLDER_RE = re.compile(r"^\[\[link:(?P<key>[A-Za-z0-9._-]+)\]\]$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

DEFAULT_EXCLUDES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "docs/_site",
    "docs/.jekyll-cache",
    "project_meta/reports",
}


def _parse_simple_yaml(text: str) -> Dict[str, object]:
    root: Dict[str, object] = {}
    stack: list[Tuple[int, Dict[str, object]]] = [(-1, root)]

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
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            new_node: Dict[str, object] = {}
            parent[key] = new_node
            stack.append((indent, new_node))
        else:
            parent[key] = value

    return root


def _flatten_map(prefix: str, node: object, out: Dict[str, str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            new_prefix = f"{prefix}.{key}" if prefix else str(key)
            _flatten_map(new_prefix, value, out)
    else:
        out[prefix] = str(node)


def load_link_map(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if yaml:
        data = yaml.safe_load(text) or {}
    else:
        data = _parse_simple_yaml(text)
    flat: Dict[str, str] = {}
    _flatten_map("", data, flat)
    return flat


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
    link_map: Dict[str, str],
    reverse_map: Dict[str, str],
    annotate: bool,
) -> Tuple[str, int, int, int]:
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
            new_url = link_map[key]
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
                new_url = link_map[key]
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
    args = parser.parse_args()

    root = Path(args.root).resolve()
    map_path = Path(args.map_path).resolve()
    if not map_path.exists():
        print(f"Link map not found: {map_path}", file=sys.stderr)
        return 2

    link_map = load_link_map(map_path)
    reverse_map = {}
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
        updated_text, updated, annotated, missing = replace_links(
            original, link_map, reverse_map, args.annotate
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

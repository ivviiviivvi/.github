"""Validate chatmode frontmatter in ai_framework/chatmodes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CHATMODES_DIR = Path("ai_framework/chatmodes")
REQUIRED_KEYS = {"name", "description", "tools"}


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, -1
    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
    if end_index == -1:
        return {}, -1
    block = lines[1:end_index]
    frontmatter: dict[str, str] = {}
    for line in block:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^[a-z0-9_-]+:\s*$", line):
            key = line.split(":", 1)[0].strip()
            frontmatter[key] = ""
            continue
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                frontmatter.setdefault(key, "")
    return frontmatter, end_index


def _remove_legacy_description(
    lines: list[str], end_index: int
) -> tuple[list[str], bool]:
    updated = []
    removed = False
    for i, line in enumerate(lines):
        if i > end_index and line.lstrip().startswith("## description:"):
            removed = True
            continue
        updated.append(line)
    return updated, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate chatmode frontmatter.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Remove legacy '## description:' lines when frontmatter is present.",
    )
    args = parser.parse_args()

    if not CHATMODES_DIR.exists():
        print("Missing ai_framework/chatmodes directory.")
        return 1

    failures: list[str] = []
    for path in sorted(CHATMODES_DIR.glob("*.chatmode.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        frontmatter, end_index = _parse_frontmatter(lines)
        if end_index == -1:
            failures.append(f"{path}: missing or malformed frontmatter")
            continue
        if args.fix:
            updated_lines, removed = _remove_legacy_description(lines, end_index)
            if removed:
                path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
                lines = updated_lines
        missing = REQUIRED_KEYS - set(frontmatter.keys())
        if missing:
            failures.append(f"{path}: missing keys: {', '.join(sorted(missing))}")
        if any("## description:" in line for line in lines[end_index + 1 :]):
            failures.append(f"{path}: legacy '## description:' line present")

    if failures:
        print("Chatmode frontmatter validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Chatmode frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

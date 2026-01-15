"""Validate collection frontmatter in ai_framework/collections."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

COLLECTIONS_DIR = Path("ai_framework/collections")
REQUIRED_KEYS = {"name", "description"}
ALLOWED_TAGS: set[str] = set()


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate collection frontmatter.")
    args = parser.parse_args()

    if not COLLECTIONS_DIR.exists():
        print("Missing ai_framework/collections directory.")
        return 1

    failures: list[str] = []
    for path in sorted(COLLECTIONS_DIR.glob("*.*")):
        if path.name in {"INVENTORY.md", "SCHEMA.md", "README.md"}:
            continue
        if path.name.endswith(".md") or path.name.endswith(".yml"):
            lines = path.read_text(encoding="utf-8").splitlines()
            frontmatter, end_index = _parse_frontmatter(lines)
            if end_index == -1:
                failures.append(f"{path}: missing or malformed frontmatter")
                continue
            missing = REQUIRED_KEYS - set(frontmatter.keys())
            if missing:
                failures.append(f"{path}: missing keys: {', '.join(sorted(missing))}")
            tags = frontmatter.get("tags", [])
            if isinstance(tags, str):
                tags_list = [tags]
            else:
                tags_list = list(tags) if tags else []
            for tag in tags_list:
                if tag and tag not in ALLOWED_TAGS:
                    failures.append(f"{path}: tag not allowed: {tag}")

    if failures:
        print("Collection frontmatter validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Collection frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

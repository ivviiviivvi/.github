"""Validate agent frontmatter in ai_framework/agents."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

AGENTS_DIR = Path("ai_framework/agents")
REQUIRED_KEYS = {"name", "description"}


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
    parser = argparse.ArgumentParser(description="Validate agent frontmatter.")
    args = parser.parse_args()

    if not AGENTS_DIR.exists():
        print("Missing ai_framework/agents directory.")
        return 1

    failures: list[str] = []
    for path in sorted(AGENTS_DIR.glob("*.agent.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        frontmatter, end_index = _parse_frontmatter(lines)
        if end_index == -1:
            failures.append(f"{path}: missing or malformed frontmatter")
            continue
        missing = REQUIRED_KEYS - set(frontmatter.keys())
        if missing:
            failures.append(f"{path}: missing keys: {', '.join(sorted(missing))}")

    if failures:
        print("Agent frontmatter validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Agent frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

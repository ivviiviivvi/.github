"""Validate collection frontmatter in ai_framework/collections."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

COLLECTIONS_DIR = Path("src/ai_framework/collections")
REQUIRED_KEYS = {"name", "description"}
ALLOWED_TAGS: set[str] = set()
_DELIMITER_RE = re.compile(r"^(?:---|_{5,})$")
_KNOWN_KEYS = {"name", "description", "model", "tools", "tags", "updated"}
_INLINE_KEY_RE = re.compile(r"\b(" + "|".join(sorted(_KNOWN_KEYS)) + r"):", re.IGNORECASE)


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or not _DELIMITER_RE.match(lines[0].strip()):
        return {}, -1
    is_yaml = lines[0].strip() == "---"

    if is_yaml:
        # Standard YAML: require closing ---
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
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" in stripped:
                key = stripped.split(":", 1)[0].strip()
                if key:
                    frontmatter.setdefault(key, "")
        return frontmatter, end_index

    # Concatenated format (______): find end at closing delimiter or heading
    end_index = -1
    for i in range(1, len(lines)):
        stripped = lines[i].strip()
        if _DELIMITER_RE.match(stripped):
            end_index = i
            break
        if stripped.startswith("# ") and not stripped.startswith("## "):
            end_index = i
            break
    if end_index == -1:
        end_index = len(lines)
    block = lines[1:end_index]
    frontmatter = {}
    for line in block:
        cleaned = re.sub(r"^##\s+", "", line.strip())
        if not cleaned:
            continue
        found = _INLINE_KEY_RE.findall(cleaned)
        if found:
            for key in found:
                frontmatter.setdefault(key.lower(), "")
        elif ":" in cleaned:
            key = cleaned.split(":", 1)[0].strip()
            if key and not key.startswith("#"):
                frontmatter.setdefault(key, "")
    return frontmatter, end_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate collection frontmatter.")
    parser.parse_args()

    if not COLLECTIONS_DIR.exists():
        print("Missing src/ai_framework/collections directory.")
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
            tags: object = frontmatter.get("tags", [])
            if isinstance(tags, str):
                tags_list: list[str] = [tags]
            elif isinstance(tags, list):
                tags_list = tags
            else:
                tags_list = []
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

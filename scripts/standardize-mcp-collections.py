#!/usr/bin/env python3
"""Standardize MCP collection frontmatter.

This script fixes the frontmatter in all .md collection files to match
the YAML format used in .yml collection files.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def extract_inline_frontmatter(line: str) -> dict[str, Any]:
    """Extract frontmatter from inline comment format."""
    # Pattern: ## name: X description: Y tags: [] updated: Z
    pattern = r"##\s+name:\s+(.+?)\s+description:\s+(.+?)\s+tags:\s+(.+?)\s+updated:\s+(.+?)$"
    match = re.match(pattern, line)
    if not match:
        return {}

    name, description, tags, updated = match.groups()

    # Parse tags - they're in the format \[\] or with actual values
    tags_str = tags.strip()
    tags_list: list[str] = []
    if tags_str == r"\[\]" or tags_str == "[]":
        pass  # tags_list already initialized
    else:
        # Try to parse as list
        pass  # tags_list already initialized

    return {
        "name": name.strip(),
        "description": description.strip(),
        "tags": tags_list,
        "updated": updated.strip(),
    }


def get_yml_frontmatter(yml_path: Path) -> dict[str, Any]:
    """Get frontmatter from corresponding .yml file."""
    if not yml_path.exists():
        return {}

    content = yml_path.read_text(encoding="utf-8")

    # Extract the first YAML frontmatter block
    if not content.startswith("---\n"):
        return {}

    # Find the end of frontmatter
    end_idx = content.find("\n---\n", 4)
    if end_idx == -1:
        return {}

    yaml_content = content[4:end_idx]
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def fix_md_frontmatter(md_path: Path) -> bool:
    """Fix frontmatter in a .md collection file."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    if not lines:
        return False

    # Check if it has the malformed frontmatter
    if lines[0].strip() != "---":
        return False

    if len(lines) < 3:
        return False

    # Check for inline comment frontmatter
    if not lines[2].strip().startswith("##"):
        return False

    # Extract inline frontmatter
    inline_fm = extract_inline_frontmatter(lines[2].strip())
    if not inline_fm:
        return False

    # Get frontmatter from corresponding .yml file
    yml_path = md_path.with_suffix(".collection.yml")
    yml_fm = get_yml_frontmatter(yml_path)

    # Use .yml frontmatter if available, otherwise use inline
    frontmatter = yml_fm if yml_fm else inline_fm

    # Create proper YAML frontmatter
    yaml_lines = ["---\n"]
    yaml_lines.append(f"name: {frontmatter.get('name', 'Unknown')}\n")
    yaml_lines.append(f"description: {frontmatter.get('description', '')}\n")

    tags = frontmatter.get("tags", [])
    if tags:
        yaml_lines.append("tags:\n")
        for tag in tags:
            yaml_lines.append(f"  - {tag}\n")
    else:
        yaml_lines.append("tags: []\n")

    # Use today's date if not provided
    updated = frontmatter.get("updated")
    if not updated:
        updated = datetime.now().strftime("%Y-%m-%d")
    yaml_lines.append(f"updated: {updated}\n")
    yaml_lines.append("---\n")

    # Reconstruct the file
    new_lines = yaml_lines + ["\n"] + lines[4:]  # Skip old frontmatter (lines 0-3)

    new_content = "".join(new_lines)
    md_path.write_text(new_content, encoding="utf-8")

    return True


def main() -> int:
    """Main function."""
    collections_dir = Path("ai_framework/collections")

    if not collections_dir.exists():
        print(f"Error: {collections_dir} does not exist")
        return 1

    # Process all .md files except special ones
    skip_files = {"INVENTORY.md", "SCHEMA.md", "README.md", "TEMPLATE.md"}
    fixed_count = 0

    for md_file in sorted(collections_dir.glob("*.md")):
        if md_file.name in skip_files:
            continue

        print(f"Processing {md_file.name}...")
        if fix_md_frontmatter(md_file):
            print(f"  ✓ Fixed frontmatter in {md_file.name}")
            fixed_count += 1
        else:
            print(f"  ✗ Could not fix {md_file.name}")

    print(f"\nFixed {fixed_count} collection files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

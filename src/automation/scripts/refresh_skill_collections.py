"""Refresh and validate skill collections in ai_framework/collections.

This script scans all collection files (.md and .yml), validates their
frontmatter structure, and optionally regenerates the INVENTORY.md file.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# Default paths - relative to repository root
COLLECTIONS_DIR = Path("src/ai_framework/collections")
INVENTORY_FILE = COLLECTIONS_DIR / "INVENTORY.md"

# Required frontmatter keys for collections
REQUIRED_KEYS = {"name", "description"}

# Files to skip during validation
SKIP_FILES = {"INVENTORY.md", "SCHEMA.md", "README.md", ".DS_Store"}


class ValidationResult(NamedTuple):
    """Result of validating a single collection file."""

    path: Path
    valid: bool
    errors: list[str]
    warnings: list[str]
    frontmatter: dict[str, object]


def parse_frontmatter(content: str) -> tuple[dict[str, object], int]:
    """Parse YAML frontmatter from file content.

    Args:
        content: File content as string

    Returns:
        Tuple of (frontmatter dict, end line index) or ({}, -1) if no frontmatter

    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, -1

    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index == -1:
        return {}, -1

    data: dict[str, object] = {}
    i = 1
    while i < end_index:
        line = lines[i].rstrip()
        if not line or line.lstrip().startswith("#"):
            i += 1
            continue

        # Handle list values (key with empty value followed by items)
        if re.match(r"^[a-z0-9_-]+:\s*$", line):
            key = line.split(":", 1)[0].strip()
            values: list[str] = []
            j = i + 1
            while j < end_index and lines[j].startswith("  - "):
                values.append(lines[j].replace("  - ", "", 1).strip())
                j += 1
            data[key] = values
            i = j
            continue

        # Handle key: value pairs
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        i += 1

    return data, end_index


def validate_collection(path: Path) -> ValidationResult:
    """Validate a single collection file.

    Args:
        path: Path to the collection file

    Returns:
        ValidationResult with validation status and any errors/warnings

    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return ValidationResult(
            path=path,
            valid=False,
            errors=[f"Could not read file: {e}"],
            warnings=[],
            frontmatter={},
        )

    frontmatter, end_index = parse_frontmatter(content)

    if end_index == -1:
        errors.append("Missing or malformed frontmatter (no closing ---)")
        return ValidationResult(
            path=path,
            valid=False,
            errors=errors,
            warnings=warnings,
            frontmatter={},
        )

    # Check required keys
    missing_keys = REQUIRED_KEYS - set(frontmatter.keys())
    if missing_keys:
        errors.append(f"Missing required keys: {', '.join(sorted(missing_keys))}")

    # Check for empty required values
    for key in REQUIRED_KEYS:
        if key in frontmatter:
            value = frontmatter[key]
            if not value or (isinstance(value, str) and not value.strip()):
                warnings.append(f"Key '{key}' has empty value")

    # Check for paired .md and .yml files
    if path.suffix == ".yml":
        md_partner = path.with_suffix(".md")
        if not md_partner.exists():
            warnings.append(f"No matching .md file for {path.name}")
    elif path.suffix == ".md" and path.stem.endswith(".collection"):
        yml_partner = path.parent / f"{path.stem}.yml"
        if not yml_partner.exists():
            warnings.append(f"No matching .yml file for {path.name}")

    return ValidationResult(
        path=path,
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        frontmatter=frontmatter,
    )


def generate_inventory(results: list[ValidationResult]) -> str:
    """Generate INVENTORY.md content from validation results.

    Args:
        results: List of validation results for all collection files

    Returns:
        Generated markdown content for INVENTORY.md

    """
    lines = [
        "# Collection Inventory\n",
        "\n",
        "Auto-generated inventory of skill collections.\n",
        "\n",
        "| File | Name | Description | Tags | Status |\n",
        "| --- | --- | --- | --- | --- |\n",
    ]

    for result in sorted(results, key=lambda r: r.path.name):
        fm = result.frontmatter
        name = str(fm.get("name", ""))
        description = str(fm.get("description", ""))

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags_list = [tags]
        elif isinstance(tags, list):
            tags_list = [str(t) for t in tags]
        else:
            tags_list = []
        tags_text = ", ".join(tags_list)

        status = "Valid" if result.valid else "Invalid"
        if result.warnings:
            status = "Warning"

        lines.append(f"| `{result.path.name}` | {name} | {description} | {tags_text} | {status} |\n")

    return "".join(lines)


def main() -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Refresh and validate skill collections")
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=COLLECTIONS_DIR,
        help="Path to collections directory",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Regenerate INVENTORY.md even if validation fails",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed validation results",
    )
    args = parser.parse_args()

    collections_dir = args.collections_dir
    if not collections_dir.exists():
        print(f"Collections directory not found: {collections_dir}")
        return 1

    # Collect all collection files
    collection_files = []
    for pattern in ("*.md", "*.yml"):
        for path in collections_dir.glob(pattern):
            if path.name not in SKIP_FILES:
                collection_files.append(path)

    if not collection_files:
        print(f"No collection files found in {collections_dir}")
        return 1

    print(f"Validating {len(collection_files)} collection files...")

    # Validate all collections
    results: list[ValidationResult] = []
    total_errors = 0
    total_warnings = 0

    for path in sorted(collection_files):
        result = validate_collection(path)
        results.append(result)
        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

        if args.verbose or result.errors or result.warnings:
            status_icon = "PASS" if result.valid else "FAIL"
            print(f"\n{status_icon}: {path.name}")
            for error in result.errors:
                print(f"  ERROR: {error}")
            for warning in result.warnings:
                print(f"  WARNING: {warning}")

    # Summary
    print("\nValidation complete:")
    print(f"  Files checked: {len(results)}")
    print(f"  Valid: {sum(1 for r in results if r.valid)}")
    print(f"  Invalid: {sum(1 for r in results if not r.valid)}")
    print(f"  Total errors: {total_errors}")
    print(f"  Total warnings: {total_warnings}")

    # Determine if we should regenerate inventory
    should_regenerate = args.regenerate or (total_errors == 0)
    if should_regenerate:
        inventory_content = generate_inventory(results)
        inventory_path = collections_dir / "INVENTORY.md"
        inventory_path.write_text(inventory_content, encoding="utf-8")
        print(f"\nRegenerated: {inventory_path}")

    # Return exit code
    if total_errors > 0:
        return 1
    if args.strict and total_warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate skills across agents, chatmodes, and prompts.

This script validates skill definitions in the ai_framework directory,
checking for unique identifiers, collection membership, and broken references.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

# Default paths - relative to repository root
AI_FRAMEWORK_DIR = Path("src/ai_framework")
AGENTS_DIR = AI_FRAMEWORK_DIR / "agents"
CHATMODES_DIR = AI_FRAMEWORK_DIR / "chatmodes"
PROMPTS_DIR = AI_FRAMEWORK_DIR / "prompts"
COLLECTIONS_DIR = AI_FRAMEWORK_DIR / "collections"

# Files to skip during validation
SKIP_FILES = {"INVENTORY.md", "SCHEMA.md", "README.md", ".DS_Store", "INDEX.md"}


class SkillInfo(NamedTuple):
    """Information about a skill definition."""

    path: Path
    skill_type: str  # 'agent', 'chatmode', 'prompt'
    name: str
    identifier: str
    collection: str | None
    dependencies: list[str]


class ValidationResult(NamedTuple):
    """Result of skill validation."""

    valid: bool
    errors: list[str]
    warnings: list[str]
    skills: list[SkillInfo]


def parse_frontmatter(content: str) -> dict[str, object]:
    """Parse YAML frontmatter from file content.

    Args:
        content: File content as string

    Returns:
        Frontmatter dict or empty dict if no frontmatter

    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index == -1:
        return {}

    data: dict[str, object] = {}
    i = 1
    while i < end_index:
        line = lines[i].rstrip()
        if not line or line.lstrip().startswith("#"):
            i += 1
            continue

        # Handle list values
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

    return data


def extract_skill_info(path: Path, skill_type: str) -> SkillInfo | None:
    """Extract skill information from a file.

    Args:
        path: Path to the skill file
        skill_type: Type of skill ('agent', 'chatmode', 'prompt')

    Returns:
        SkillInfo or None if not a valid skill file

    """
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return None

    frontmatter = parse_frontmatter(content)
    if not frontmatter:
        return None

    name = str(frontmatter.get("name", path.stem))

    # Generate identifier from filename if not specified
    identifier = str(frontmatter.get("id", frontmatter.get("identifier", "")))
    if not identifier:
        # Use filename without extension as identifier
        identifier = path.stem.replace(f".{skill_type}", "")

    # Get collection membership
    collection = frontmatter.get("collection")
    if isinstance(collection, str):
        collection = collection.strip() or None
    else:
        collection = None

    # Get dependencies
    deps = frontmatter.get("dependencies", frontmatter.get("requires", []))
    if isinstance(deps, str):
        dependencies = [deps] if deps else []
    elif isinstance(deps, list):
        dependencies = [str(d) for d in deps]
    else:
        dependencies = []

    return SkillInfo(
        path=path,
        skill_type=skill_type,
        name=name,
        identifier=identifier,
        collection=collection,
        dependencies=dependencies,
    )


def collect_skills(base_dir: Path) -> list[SkillInfo]:
    """Collect all skill definitions from ai_framework.

    Args:
        base_dir: Base directory of ai_framework

    Returns:
        List of SkillInfo objects

    """
    skills: list[SkillInfo] = []

    # Collect agents
    agents_dir = base_dir / "agents"
    if agents_dir.exists():
        for path in agents_dir.glob("*.agent.md"):
            if path.name not in SKIP_FILES:
                skill = extract_skill_info(path, "agent")
                if skill:
                    skills.append(skill)

    # Collect chatmodes
    chatmodes_dir = base_dir / "chatmodes"
    if chatmodes_dir.exists():
        for path in chatmodes_dir.glob("*.chatmode.md"):
            if path.name not in SKIP_FILES:
                skill = extract_skill_info(path, "chatmode")
                if skill:
                    skills.append(skill)

    # Collect prompts
    prompts_dir = base_dir / "prompts"
    if prompts_dir.exists():
        for path in prompts_dir.glob("*.prompt.md"):
            if path.name not in SKIP_FILES:
                skill = extract_skill_info(path, "prompt")
                if skill:
                    skills.append(skill)

    return skills


def collect_collections(collections_dir: Path) -> set[str]:
    """Collect all valid collection names.

    Args:
        collections_dir: Path to collections directory

    Returns:
        Set of collection names

    """
    collections: set[str] = set()

    if not collections_dir.exists():
        return collections

    for path in collections_dir.glob("*.collection.yml"):
        if path.name not in SKIP_FILES:
            try:
                content = path.read_text(encoding="utf-8")
                frontmatter = parse_frontmatter(content)
                name = frontmatter.get("name", "")
                if isinstance(name, str) and name:
                    collections.add(name)
                # Also add the filename-based identifier
                collections.add(path.stem.replace(".collection", ""))
            except Exception:
                pass

    return collections


def validate_skills(
    skills: list[SkillInfo],
    collections: set[str],
    check_unique: bool = False,
    filter_collection: str | None = None,
) -> ValidationResult:
    """Validate skill definitions.

    Args:
        skills: List of skills to validate
        collections: Set of valid collection names
        check_unique: Whether to check for unique identifiers
        filter_collection: If specified, only validate skills in this collection

    Returns:
        ValidationResult with errors and warnings

    """
    errors: list[str] = []
    warnings: list[str] = []
    filtered_skills = skills

    # Filter by collection if specified
    if filter_collection:
        filtered_skills = [s for s in skills if s.collection == filter_collection]
        if not filtered_skills:
            warnings.append(f"No skills found in collection '{filter_collection}'")

    # Check for unique identifiers
    if check_unique:
        id_to_skills: dict[str, list[SkillInfo]] = defaultdict(list)
        for skill in filtered_skills:
            id_to_skills[skill.identifier].append(skill)

        for identifier, duplicates in id_to_skills.items():
            if len(duplicates) > 1:
                paths = [str(s.path.name) for s in duplicates]
                errors.append(f"Duplicate identifier '{identifier}': {', '.join(paths)}")

    # Check collection references
    for skill in filtered_skills:
        if skill.collection and skill.collection not in collections:
            warnings.append(f"{skill.path.name}: references unknown collection '{skill.collection}'")

    # Check dependencies (warn about potential broken references)
    all_identifiers = {s.identifier for s in skills}
    for skill in filtered_skills:
        for dep in skill.dependencies:
            if dep and dep not in all_identifiers:
                warnings.append(f"{skill.path.name}: depends on unknown skill '{dep}'")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        skills=filtered_skills,
    )


def main() -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Validate skills across agents, chatmodes, and prompts")
    parser.add_argument(
        "--framework-dir",
        type=Path,
        default=AI_FRAMEWORK_DIR,
        help="Path to ai_framework directory",
    )
    parser.add_argument(
        "--unique",
        action="store_true",
        help="Check for unique skill identifiers",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Filter validation to skills in this collection",
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
        help="Print detailed information about each skill",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all skills without validation",
    )
    args = parser.parse_args()

    framework_dir = args.framework_dir
    if not framework_dir.exists():
        print(f"AI framework directory not found: {framework_dir}")
        return 1

    # Collect all skills
    print(f"Scanning {framework_dir} for skill definitions...")
    skills = collect_skills(framework_dir)
    collections = collect_collections(framework_dir / "collections")

    print(f"Found {len(skills)} skills and {len(collections)} collections")

    # List mode - just print skills and exit
    if args.list:
        print("\nSkills:")
        for skill in sorted(skills, key=lambda s: (s.skill_type, s.identifier)):
            collection_info = f" [collection: {skill.collection}]" if skill.collection else ""
            print(f"  [{skill.skill_type}] {skill.identifier}: {skill.name}{collection_info}")
        return 0

    # Validate skills
    result = validate_skills(
        skills=skills,
        collections=collections,
        check_unique=args.unique,
        filter_collection=args.collection,
    )

    # Print results
    if args.verbose:
        print("\nValidated skills:")
        for skill in result.skills:
            print(f"  - {skill.path.name} ({skill.skill_type})")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  ERROR: {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  WARNING: {warning}")

    # Summary
    print("\nValidation summary:")
    print(f"  Skills validated: {len(result.skills)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")
    print(f"  Status: {'PASS' if result.valid else 'FAIL'}")

    # Return exit code
    if not result.valid:
        return 1
    if args.strict and result.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

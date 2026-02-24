#!/usr/bin/env python3
"""Validate workflow metadata sidecar files against the FUNCTIONcalled schema.

This tool validates .meta.json files that provide structured metadata
for GitHub Actions workflows following the FUNCTIONcalled naming convention.

Usage:
    python validate_workflow_meta.py workflow1.yml.meta.json workflow2.yml.meta.json
    python validate_workflow_meta.py --schema custom.schema.json file.meta.json
    python validate_workflow_meta.py --scan-dir .github/workflows/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Error: jsonschema package required. Install with: pip install jsonschema")
    sys.exit(1)


# Default schema path relative to this script
DEFAULT_SCHEMA = Path(__file__).parent.parent.parent / "standards" / "FUNCTIONcalled_Workflow_Sidecar.schema.json"


def load_schema(schema_path: Path) -> dict[str, Any]:
    """Load JSON schema from file."""
    try:
        with open(schema_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema file: {e}")
        sys.exit(1)


def validate_metadata(metadata_path: Path, validator: Draft202012Validator) -> tuple[bool, list[str]]:
    """Validate a metadata file against the schema.

    Returns:
        (is_valid, list of error messages)

    """
    errors: list[str] = []

    try:
        with open(metadata_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, [f"File not found: {metadata_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    # Validate against schema
    validation_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))

    for err in validation_errors:
        loc = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{loc}: {err.message}")

    # Additional workflow-specific validations
    if data.get("functioncalled"):
        fc = data["functioncalled"]

        # Validate layer
        valid_layers = {"core", "interface", "logic", "application"}
        if fc.get("layer") and fc["layer"] not in valid_layers:
            errors.append(f"functioncalled.layer: must be one of {valid_layers}")

        # Check canonical name format
        canonical = fc.get("canonical", "")
        if canonical:
            parts = canonical.split(".")
            if len(parts) < 3:
                errors.append("functioncalled.canonical: must have at least 3 parts (layer.role.domain[.ext])")
            elif parts[0] not in valid_layers:
                errors.append(f"functioncalled.canonical: first part must be a valid layer, got '{parts[0]}'")

    return len(errors) == 0, errors


def find_metadata_files(directory: Path) -> list[Path]:
    """Find all .meta.json files in a directory."""
    return sorted(directory.glob("**/*.meta.json"))


def main():
    parser = argparse.ArgumentParser(description="Validate FUNCTIONcalled workflow metadata sidecar files")
    parser.add_argument(
        "--schema", type=Path, default=DEFAULT_SCHEMA, help=f"Path to JSON schema file (default: {DEFAULT_SCHEMA})"
    )
    parser.add_argument("--scan-dir", type=Path, help="Directory to scan for .meta.json files")
    parser.add_argument("files", nargs="*", type=Path, help="Metadata files to validate")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only output errors")

    args = parser.parse_args()

    # Load schema
    schema = load_schema(args.schema)
    validator = Draft202012Validator(schema)

    # Collect files to validate
    files: list[Path] = []
    if args.scan_dir:
        files.extend(find_metadata_files(args.scan_dir))
    if args.files:
        files.extend(args.files)

    if not files:
        print("No metadata files to validate. Specify files or use --scan-dir")
        sys.exit(1)

    # Validate each file
    all_valid = True
    validated = 0
    failed = 0

    for filepath in files:
        is_valid, errors = validate_metadata(filepath, validator)
        validated += 1

        if is_valid:
            if not args.quiet:
                print(f"✅ {filepath}")
        else:
            all_valid = False
            failed += 1
            print(f"❌ {filepath}")
            for error in errors:
                print(f"   - {error}")

    # Summary
    print()
    if all_valid:
        print(f"✅ All {validated} metadata file(s) are valid")
    else:
        print(f"❌ {failed} of {validated} metadata file(s) have errors")
        sys.exit(1)


if __name__ == "__main__":
    main()

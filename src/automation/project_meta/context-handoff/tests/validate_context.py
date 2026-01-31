#!/usr/bin/env python3
"""Context Validation Utility.

Validates generated context payloads against schema requirements
and verifies token count targets are met.

Usage:
    python validate_context.py [context_file]
"""

import json
import sys
from pathlib import Path
from typing import Any


class ContextValidator:
    """Validate context payloads against schema and token requirements."""

    # Token count targets
    TARGETS = {"minimal": 500, "standard": 1200, "full": 2000}

    # Required fields by compression level
    REQUIRED_FIELDS = {
        "minimal": {
            "summary": ["phase", "progress"],
            "active": None,
            "failed": None,
            "next": None,
        },
        "standard": {
            "version": None,
            "handoff_id": None,
            "summary": [
                "project",
                "current_phase",
                "progress",
                "tasks_complete",
                "tasks_total",
            ],
            "execution_state": [
                "active_tasks",
                "blocked_tasks",
                "failed_tasks",
                "next_eligible",
            ],
            "critical_context": ["errors", "user_decisions", "warnings"],
            "dag_snapshot": [
                "phases_completed",
                "current_phase_progress",
                "critical_path",
            ],
        },
        "full": {
            "version": None,
            "handoff_id": None,
            "summary": [
                "project",
                "current_phase",
                "progress",
                "tasks_complete",
                "tasks_total",
            ],
            "execution_state": [
                "active_tasks",
                "blocked_tasks",
                "failed_tasks",
                "next_eligible",
            ],
            "critical_context": ["errors", "user_decisions", "warnings"],
            "dag_snapshot": [
                "phases_completed",
                "current_phase_progress",
                "critical_path",
            ],
            "file_state": ["artifacts", "required", "disk_mb"],
            "environment": ["os", "python", "packages"],
        },
    }

    def __init__(self, context_file: str):
        """Initialize validator with context file.

        Args:
            context_file: Path to context payload JSON file

        """
        self.context_file = Path(context_file)
        self.context = self._load_context()
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def _load_context(self) -> dict[str, Any]:
        """Load context from JSON file.

        Returns:
            Dictionary containing context payload

        Raises:
            FileNotFoundError: If context file doesn't exist
            json.JSONDecodeError: If file is not valid JSON

        """
        if not self.context_file.exists():
            raise FileNotFoundError(f"Context file not found: {self.context_file}")

        with open(self.context_file, encoding="utf-8") as f:
            return json.load(f)

    def detect_level(self) -> str:
        """Detect compression level from context structure.

        Returns:
            Detected compression level ('minimal', 'standard', or 'full')

        """
        if "version" in self.context:
            if "file_state" in self.context:
                return "full"
            return "standard"
        return "minimal"

    def validate_schema(self, level: str) -> bool:
        """Validate context against schema requirements.

        Args:
            level: Compression level to validate against

        Returns:
            True if schema is valid, False otherwise

        """
        if level not in self.REQUIRED_FIELDS:
            self.errors.append(f"Unknown compression level: {level}")
            return False

        required = self.REQUIRED_FIELDS[level]
        valid = True

        for field, subfields in required.items():
            if field not in self.context:
                self.errors.append(f"Missing required field: {field}")
                valid = False
                continue

            if subfields is not None:
                # Validate subfields
                for subfield in subfields:
                    if subfield not in self.context[field]:
                        self.errors.append(
                            f"Missing required subfield: {field}.{subfield}"
                        )
                        valid = False

        return valid

    def validate_token_count(self, level: str) -> bool:
        """Validate token count against target.

        Args:
            level: Compression level

        Returns:
            True if token count is within target, False otherwise

        """
        token_count = self.get_token_count()
        target = self.TARGETS[level]

        if token_count > target:
            self.warnings.append(
                f"Token count {token_count} exceeds target {target} by {token_count - target} tokens"
            )
            return False

        return True

    def get_token_count(self) -> int:
        """Estimate token count for context.

        Returns:
            Estimated token count (4 chars ≈ 1 token)

        """
        return len(json.dumps(self.context, separators=(",", ":"))) // 4

    def validate_data_types(self) -> bool:
        """Validate data types of fields.

        Returns:
            True if all data types are correct, False otherwise

        """
        valid = True

        # Check lists
        list_fields = {
            "minimal": ["active", "failed", "next"],
            "standard": [
                "execution_state.active_tasks",
                "execution_state.blocked_tasks",
                "execution_state.failed_tasks",
                "execution_state.next_eligible",
                "critical_context.errors",
                "critical_context.user_decisions",
                "critical_context.warnings",
                "dag_snapshot.phases_completed",
                "dag_snapshot.critical_path",
            ],
            "full": ["file_state.artifacts", "file_state.required"],
        }

        level = self.detect_level()
        for field_path in list_fields.get(level, []):
            value = self._get_nested_value(field_path)
            if value is not None and not isinstance(value, list):
                self.errors.append(f"Field {field_path} should be a list")
                valid = False

        return valid

    def _get_nested_value(self, field_path: str) -> Any:
        """Get nested value from context using dot notation.

        Args:
            field_path: Dot-separated field path (e.g., 'summary.progress')

        Returns:
            Value at field path or None if not found

        """
        parts = field_path.split(".")
        value = self.context
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        return value

    def validate_all(self) -> tuple[bool, list[str], list[str]]:
        """Run all validations.

        Returns:
            Tuple of (is_valid, errors, warnings)

        """
        level = self.detect_level()

        # Reset errors and warnings
        self.errors = []
        self.warnings = []

        # Run validations
        schema_valid = self.validate_schema(level)
        self.validate_token_count(level)
        types_valid = self.validate_data_types()

        is_valid = schema_valid and types_valid

        return is_valid, self.errors, self.warnings

    def print_report(self):
        """Print validation report."""
        level = self.detect_level()
        token_count = self.get_token_count()
        target = self.TARGETS[level]

        print("=" * 80)
        print("Context Validation Report")
        print("=" * 80)
        print(f"File:        {self.context_file}")
        print(f"Level:       {level}")
        print(f"Token count: {token_count} (target: ≤{target})")
        print("Status:      ", end="")

        is_valid, errors, warnings = self.validate_all()

        if is_valid and not warnings:
            print("✅ PASS")
        elif is_valid and warnings:
            print("⚠️  PASS WITH WARNINGS")
        else:
            print("❌ FAIL")

        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"  ❌ {error}")

        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")

        if is_valid and not errors and not warnings:
            print("\n✓ All validations passed")
            print(
                f"✓ Token efficiency: {(1 - token_count / 8500) * 100:.1f}% reduction from naive"
            )

        print("=" * 80)

        return is_valid


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate context payload against schema and token requirements"
    )
    parser.add_argument(
        "context_file",
        nargs="?",
        default="context_payload.json",
        help="Path to context payload JSON file (default: context_payload.json)",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    try:
        validator = ContextValidator(args.context_file)

        if args.json:
            # JSON output
            is_valid, errors, warnings = validator.validate_all()
            result = {
                "valid": is_valid,
                "level": validator.detect_level(),
                "token_count": validator.get_token_count(),
                "errors": errors,
                "warnings": warnings,
            }
            print(json.dumps(result, indent=2))
        else:
            # Human-readable output
            is_valid = validator.print_report()

        return 0 if is_valid else 1

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.context_file}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

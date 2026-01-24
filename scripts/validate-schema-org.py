#!/usr/bin/env python3
"""Schema.org Validator
Validates schema.org JSON-LD files against schema.org specifications.
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


class SchemaOrgValidator:
    """Validates schema.org JSON-LD documents."""

    REQUIRED_FIELDS = {
        "Organization": ["@context", "@type", "name", "url"],
        "SoftwareSourceCode": [
            "@context",
            "@type",
            "name",
            "codeRepository",
            "version",
        ],
        "SoftwareApplication": [
            "@context",
            "@type",
            "name",
            "applicationCategory",
            "version",
        ],
        "TechArticle": ["@context", "@type", "name", "description"],
    }

    VALID_CONTEXTS = ["https://schema.org", "http://schema.org"]

    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_file(self, filepath: Path) -> tuple[bool, list[str], list[str]]:
        """Validate a single JSON-LD file."""
        self.errors = []
        self.warnings = []

        if not filepath.exists():
            self.errors.append(f"File not found: {filepath}")
            return False, self.errors, self.warnings

        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, self.errors, self.warnings

        # Validate structure
        self._validate_context(data)
        self._validate_type(data)
        self._validate_required_fields(data)
        self._validate_urls(data)
        self._validate_version(data)

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_context(self, data: dict) -> None:
        """Validate @context field."""
        context = data.get("@context")
        if not context:
            self.errors.append("Missing required field: @context")
        elif context not in self.VALID_CONTEXTS:
            self.errors.append(f"Invalid @context: {context}. Expected one of: {', '.join(self.VALID_CONTEXTS)}")

    def _validate_type(self, data: dict) -> None:
        """Validate @type field."""
        schema_type = data.get("@type")
        if not schema_type:
            self.errors.append("Missing required field: @type")
        elif schema_type not in self.REQUIRED_FIELDS:
            self.warnings.append(f"Unknown @type: {schema_type}. Known types: {', '.join(self.REQUIRED_FIELDS.keys())}")

    def _validate_required_fields(self, data: dict) -> None:
        """Validate required fields for the type."""
        schema_type = data.get("@type")
        if not schema_type or schema_type not in self.REQUIRED_FIELDS:
            return

        required = self.REQUIRED_FIELDS[schema_type]
        for field in required:
            if field not in data:
                self.errors.append(f"Missing required field for {schema_type}: {field}")

    def _validate_urls(self, data: dict, path: str = "") -> None:
        """Validate URL fields."""
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, str) and key in [
                "url",
                "@id",
                "sameAs",
                "codeRepository",
            ]:
                if not self._is_valid_url(value):
                    self.errors.append(f"Invalid URL at {current_path}: {value}")
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self._validate_urls(item, f"{current_path}[{i}]")
                    elif isinstance(item, str) and key == "sameAs" and not self._is_valid_url(item):
                        self.errors.append(f"Invalid URL at {current_path}[{i}]: {item}")
            elif isinstance(value, dict):
                self._validate_urls(value, current_path)

    def _validate_version(self, data: dict) -> None:
        """Validate version field if present."""
        version = data.get("version")
        if version and not self._is_valid_semver(version):
            self.warnings.append(
                f"Version '{version}' does not follow semantic versioning (MAJOR.MINOR.PATCH)"  # noqa: E501
            )

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if string is a valid URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def _is_valid_semver(version: str) -> bool:
        """Check if version follows semantic versioning."""
        parts = version.split(".")
        if len(parts) != 3:
            return False

        try:
            # Check if all parts are integers
            [int(p.split("-")[0]) for p in parts]
            return True
        except ValueError:
            return False


def main():
    """Main validation function."""
    schema_dir = Path(__file__).parent.parent / ".schema-org"

    if not schema_dir.exists():
        print("❌ .schema-org directory not found")
        sys.exit(1)

    validator = SchemaOrgValidator()
    jsonld_files = list(schema_dir.glob("*.jsonld"))

    if not jsonld_files:
        print("⚠️  No .jsonld files found in .schema-org/")
        sys.exit(0)

    print(f"🔍 Validating {len(jsonld_files)} schema.org files...\n")

    all_valid = True
    for filepath in jsonld_files:
        print(f"📄 {filepath.name}")
        valid, errors, warnings = validator.validate_file(filepath)

        if errors:
            all_valid = False
            for error in errors:
                print(f"   ❌ {error}")

        if warnings:
            for warning in warnings:
                print(f"   ⚠️  {warning}")

        if valid and not warnings:
            print("   ✅ Valid")

        print()

    if all_valid:
        print("✨ All schema.org files are valid!")
        sys.exit(0)
    else:
        print("❌ Validation failed. Please fix the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

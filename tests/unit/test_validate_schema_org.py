#!/usr/bin/env python3
"""Unit tests for automation/scripts/utils/validate-schema-org.py

Focus: Schema.org JSON-LD validation.
"""

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Import the module with hyphenated filename
spec = importlib.util.spec_from_file_location(
    "validate_schema_org",
    Path(__file__).parent.parent.parent
    / "src"
    / "automation"
    / "scripts"
    / "utils"
    / "validate-schema-org.py",
)
validate_schema_org = importlib.util.module_from_spec(spec)
sys.modules["validate_schema_org"] = validate_schema_org
spec.loader.exec_module(validate_schema_org)


@pytest.mark.unit
class TestSchemaOrgValidatorInit:
    """Test SchemaOrgValidator initialization."""

    def test_initializes_empty_errors(self):
        """Test initializes with empty errors."""
        validator = validate_schema_org.SchemaOrgValidator()

        assert validator.errors == []
        assert validator.warnings == []


@pytest.mark.unit
class TestValidateFile:
    """Test validate_file method."""

    def test_validates_valid_file(self, tmp_path):
        """Test validates a valid JSON-LD file."""
        schema_file = tmp_path / "valid.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test Org",
            "url": "https://example.com",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, warnings = validator.validate_file(schema_file)

        assert valid is True
        assert len(errors) == 0

    def test_returns_error_for_nonexistent_file(self, tmp_path):
        """Test returns error for nonexistent file."""
        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, warnings = validator.validate_file(tmp_path / "missing.jsonld")

        assert valid is False
        assert any("not found" in e for e in errors)

    def test_returns_error_for_invalid_json(self, tmp_path):
        """Test returns error for invalid JSON."""
        schema_file = tmp_path / "invalid.jsonld"
        schema_file.write_text("not valid json {")

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, warnings = validator.validate_file(schema_file)

        assert valid is False
        assert any("Invalid JSON" in e for e in errors)


@pytest.mark.unit
class TestValidateContext:
    """Test _validate_context method."""

    def test_accepts_https_schema_org(self, tmp_path):
        """Test accepts https://schema.org context."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://test.com",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is True

    def test_accepts_http_schema_org(self, tmp_path):
        """Test accepts http://schema.org context."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "http://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://test.com",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is True

    def test_rejects_invalid_context(self, tmp_path):
        """Test rejects invalid context."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://invalid.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://test.com",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Invalid @context" in e for e in errors)

    def test_requires_context(self, tmp_path):
        """Test requires @context field."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@type": "Organization",
            "name": "Test",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Missing required field: @context" in e for e in errors)


@pytest.mark.unit
class TestValidateType:
    """Test _validate_type method."""

    def test_accepts_known_types(self, tmp_path):
        """Test accepts known schema types."""
        for schema_type in ["Organization", "SoftwareSourceCode", "SoftwareApplication", "TechArticle"]:
            schema_file = tmp_path / f"{schema_type.lower()}.jsonld"
            data = {
                "@context": "https://schema.org",
                "@type": schema_type,
                "name": "Test",
            }
            # Add required fields based on type
            if schema_type == "Organization":
                data["url"] = "https://test.com"
            elif schema_type == "SoftwareSourceCode":
                data["codeRepository"] = "https://github.com/test"
                data["version"] = "1.0.0"
            elif schema_type == "SoftwareApplication":
                data["applicationCategory"] = "Utility"
                data["version"] = "1.0.0"
            elif schema_type == "TechArticle":
                data["description"] = "Test article"

            schema_file.write_text(json.dumps(data))

            validator = validate_schema_org.SchemaOrgValidator()
            valid, errors, _ = validator.validate_file(schema_file)

            assert valid is True, f"Type {schema_type} should be valid"

    def test_warns_for_unknown_type(self, tmp_path):
        """Test warns for unknown schema type."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "UnknownType",
            "name": "Test",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, warnings = validator.validate_file(schema_file)

        # Valid because unknown type is just a warning
        assert any("Unknown @type" in w for w in warnings)

    def test_requires_type(self, tmp_path):
        """Test requires @type field."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "name": "Test",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Missing required field: @type" in e for e in errors)


@pytest.mark.unit
class TestValidateRequiredFields:
    """Test _validate_required_fields method."""

    def test_requires_organization_fields(self, tmp_path):
        """Test requires Organization fields."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            # Missing name and url
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("name" in e for e in errors)
        assert any("url" in e for e in errors)

    def test_requires_software_source_code_fields(self, tmp_path):
        """Test requires SoftwareSourceCode fields."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": "Test",
            # Missing codeRepository and version
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("codeRepository" in e for e in errors)
        assert any("version" in e for e in errors)


@pytest.mark.unit
class TestValidateUrls:
    """Test _validate_urls method."""

    def test_validates_url_fields(self, tmp_path):
        """Test validates URL fields."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://valid.com",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is True

    def test_rejects_invalid_urls(self, tmp_path):
        """Test rejects invalid URLs."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "not-a-valid-url",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Invalid URL" in e for e in errors)

    def test_validates_sameAs_urls(self, tmp_path):
        """Test validates sameAs array URLs."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://test.com",
            "sameAs": ["not-valid-url"],
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Invalid URL" in e and "sameAs" in e for e in errors)

    def test_validates_nested_urls(self, tmp_path):
        """Test validates URLs in nested objects."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test",
            "url": "https://test.com",
            "contactPoint": {
                "url": "invalid-nested-url",
            },
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, _ = validator.validate_file(schema_file)

        assert valid is False
        assert any("Invalid URL" in e and "contactPoint" in e for e in errors)


@pytest.mark.unit
class TestValidateVersion:
    """Test _validate_version method."""

    def test_accepts_valid_semver(self, tmp_path):
        """Test accepts valid semantic version."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": "Test",
            "codeRepository": "https://github.com/test",
            "version": "1.2.3",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, errors, warnings = validator.validate_file(schema_file)

        assert valid is True
        assert not any("version" in w.lower() for w in warnings)

    def test_accepts_semver_with_prerelease(self, tmp_path):
        """Test accepts semver with prerelease suffix."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": "Test",
            "codeRepository": "https://github.com/test",
            "version": "1.2.3-beta",
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, _, warnings = validator.validate_file(schema_file)

        assert valid is True

    def test_warns_for_non_semver(self, tmp_path):
        """Test warns for non-semver version."""
        schema_file = tmp_path / "test.jsonld"
        schema_file.write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": "Test",
            "codeRepository": "https://github.com/test",
            "version": "v1.0",  # Not 3 parts
        }))

        validator = validate_schema_org.SchemaOrgValidator()
        valid, _, warnings = validator.validate_file(schema_file)

        assert valid is True  # Still valid, just a warning
        assert any("semantic versioning" in w.lower() for w in warnings)


@pytest.mark.unit
class TestIsValidUrl:
    """Test _is_valid_url static method."""

    def test_accepts_https_url(self):
        """Test accepts https URLs."""
        assert validate_schema_org.SchemaOrgValidator._is_valid_url("https://example.com")

    def test_accepts_http_url(self):
        """Test accepts http URLs."""
        assert validate_schema_org.SchemaOrgValidator._is_valid_url("http://example.com")

    def test_rejects_no_scheme(self):
        """Test rejects URLs without scheme."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_url("example.com")

    def test_rejects_no_host(self):
        """Test rejects URLs without host."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_url("https://")

    def test_rejects_empty_string(self):
        """Test rejects empty string."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_url("")


@pytest.mark.unit
class TestIsValidSemver:
    """Test _is_valid_semver static method."""

    def test_accepts_valid_semver(self):
        """Test accepts valid semver."""
        assert validate_schema_org.SchemaOrgValidator._is_valid_semver("1.0.0")
        assert validate_schema_org.SchemaOrgValidator._is_valid_semver("0.1.0")
        assert validate_schema_org.SchemaOrgValidator._is_valid_semver("10.20.30")

    def test_accepts_semver_with_prerelease(self):
        """Test accepts semver with simple prerelease suffix."""
        # The validator only handles simple pre-release tags without dots
        assert validate_schema_org.SchemaOrgValidator._is_valid_semver("1.0.0-alpha")
        assert validate_schema_org.SchemaOrgValidator._is_valid_semver("1.0.0-beta")

    def test_rejects_two_parts(self):
        """Test rejects version with only two parts."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_semver("1.0")

    def test_rejects_four_parts(self):
        """Test rejects version with four parts."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_semver("1.0.0.0")

    def test_rejects_non_numeric(self):
        """Test rejects non-numeric parts."""
        assert not validate_schema_org.SchemaOrgValidator._is_valid_semver("a.b.c")


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_no_schema_dir(self, tmp_path, monkeypatch, capsys):
        """Test main exits when .schema-org dir is missing."""
        # Create a script without the schema directory
        script_dir = tmp_path / "utils"
        script_dir.mkdir(parents=True)

        # Patch __file__ to point to our temp location
        with patch.object(validate_schema_org, "__file__", str(script_dir / "validate-schema-org.py")):
            with pytest.raises(SystemExit) as exc:
                validate_schema_org.main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_main_no_jsonld_files(self, tmp_path, monkeypatch, capsys):
        """Test main exits when no .jsonld files found."""
        script_dir = tmp_path / "utils"
        script_dir.mkdir(parents=True)
        schema_dir = tmp_path / ".schema-org"
        schema_dir.mkdir()

        with patch.object(validate_schema_org, "__file__", str(script_dir / "validate-schema-org.py")):
            with pytest.raises(SystemExit) as exc:
                validate_schema_org.main()

            assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "No .jsonld files found" in captured.out

    def test_main_validates_files(self, tmp_path, capsys):
        """Test main validates all .jsonld files."""
        script_dir = tmp_path / "utils"
        script_dir.mkdir(parents=True)
        schema_dir = tmp_path / ".schema-org"
        schema_dir.mkdir()

        # Create a valid schema file
        (schema_dir / "org.jsonld").write_text(json.dumps({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Test Org",
            "url": "https://example.com",
        }))

        with patch.object(validate_schema_org, "__file__", str(script_dir / "validate-schema-org.py")):
            with pytest.raises(SystemExit) as exc:
                validate_schema_org.main()

            assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Valid" in captured.out

    def test_main_exits_1_on_errors(self, tmp_path, capsys):
        """Test main exits 1 when validation fails."""
        script_dir = tmp_path / "utils"
        script_dir.mkdir(parents=True)
        schema_dir = tmp_path / ".schema-org"
        schema_dir.mkdir()

        # Create an invalid schema file
        (schema_dir / "invalid.jsonld").write_text(json.dumps({
            "@context": "https://invalid.org",
            "@type": "Organization",
        }))

        with patch.object(validate_schema_org, "__file__", str(script_dir / "validate-schema-org.py")):
            with pytest.raises(SystemExit) as exc:
                validate_schema_org.main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Validation failed" in captured.out


@pytest.mark.unit
class TestRequiredFieldsConfig:
    """Test REQUIRED_FIELDS configuration."""

    def test_organization_required_fields(self):
        """Test Organization required fields."""
        required = validate_schema_org.SchemaOrgValidator.REQUIRED_FIELDS["Organization"]
        assert "@context" in required
        assert "@type" in required
        assert "name" in required
        assert "url" in required

    def test_software_source_code_required_fields(self):
        """Test SoftwareSourceCode required fields."""
        required = validate_schema_org.SchemaOrgValidator.REQUIRED_FIELDS["SoftwareSourceCode"]
        assert "@context" in required
        assert "@type" in required
        assert "name" in required
        assert "codeRepository" in required
        assert "version" in required

    def test_software_application_required_fields(self):
        """Test SoftwareApplication required fields."""
        required = validate_schema_org.SchemaOrgValidator.REQUIRED_FIELDS["SoftwareApplication"]
        assert "@context" in required
        assert "@type" in required
        assert "name" in required
        assert "applicationCategory" in required
        assert "version" in required

    def test_tech_article_required_fields(self):
        """Test TechArticle required fields."""
        required = validate_schema_org.SchemaOrgValidator.REQUIRED_FIELDS["TechArticle"]
        assert "@context" in required
        assert "@type" in required
        assert "name" in required
        assert "description" in required

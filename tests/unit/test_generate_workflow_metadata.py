"""Unit tests for automation/scripts/generate_workflow_metadata.py.

Focus: workflow classification, trigger parsing, metadata generation, and
repository-root side effects in main().
"""

import json
import sys
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

import generate_workflow_metadata as workflow_metadata


@pytest.mark.unit
class TestClassification:
    """Test workflow layer and role classification."""

    def test_classifies_reusable_workflows_as_core_layer(self):
        """Reusable workflow paths are always core layer workflows."""
        assert workflow_metadata.classify_layer(
            "Deploy helper",
            ".github/workflows/reusable/deploy.yml",
        ) == "core"

    @pytest.mark.parametrize(
        ("name", "filename", "expected_layer"),
        [
            ("CI", "ci.yml", "core"),
            ("Slack Notifications", "test-slack-notifications.yml", "interface"),
            ("Schema Validation", "validate-schema.yml", "logic"),
            ("Release Pages", "pages-release.yml", "application"),
        ],
    )
    def test_classifies_layers_from_name_and_filename(self, name, filename, expected_layer):
        """Layer rules match against both workflow names and filenames."""
        assert workflow_metadata.classify_layer(name, filename) == expected_layer

    @pytest.mark.parametrize(
        ("name", "filename", "expected_role"),
        [
            ("CodeQL Security Scan", "codeql.yml", "security"),
            ("Deploy Release", "publish.yml", "deployment"),
            ("Mutation Testing", "mutation-testing.yml", "testing"),
            ("Claude Review", "ai-review.yml", "ai"),
            ("Weekly Cleanup", "nightly-cleanup.yml", "maintenance"),
            ("Repository Workflow", "misc.yml", "general"),
        ],
    )
    def test_classifies_roles_from_name_and_filename(self, name, filename, expected_role):
        """Role patterns produce stable role categories with a general fallback."""
        assert workflow_metadata.classify_role(name, filename) == expected_role


@pytest.mark.unit
class TestTriggerExtraction:
    """Test workflow trigger extraction."""

    def test_extracts_string_and_list_triggers(self):
        """Simple trigger declarations are preserved."""
        assert workflow_metadata.extract_triggers({"on": "push"}) == ["push"]
        assert workflow_metadata.extract_triggers({"on": ["push", "workflow_dispatch"]}) == [
            "push",
            "workflow_dispatch",
        ]

    def test_extracts_valid_trigger_keys_from_dict(self):
        """Configured trigger dictionaries return only top-level event names."""
        workflow = {
            "on": {
                "push": {"branches": ["main"]},
                "workflow_call": {"inputs": {"name": {"type": "string"}}},
                "inputs": {"not": "a trigger"},
            }
        }

        assert workflow_metadata.extract_triggers(workflow) == ["push", "workflow_call"]

    def test_handles_pyyaml_boolean_on_key(self):
        """PyYAML may parse unquoted 'on' as True, and that key is supported."""
        workflow = {
            True: {
                "pull_request": {"branches": ["main"]},
                "schedule": [{"cron": "0 0 * * *"}],
            }
        }

        assert workflow_metadata.extract_triggers(workflow) == ["pull_request", "schedule"]

    def test_returns_empty_list_for_missing_or_unknown_triggers(self):
        """Missing and malformed trigger sections do not raise exceptions."""
        assert workflow_metadata.extract_triggers({}) == []
        assert workflow_metadata.extract_triggers({"on": 42}) == []
        assert workflow_metadata.extract_triggers({"on": {"inputs": {}}}) == []


@pytest.mark.unit
class TestMetadataHelpers:
    """Test helper functions used to build metadata documents."""

    def test_generates_description_from_role_triggers_and_jobs(self):
        """Descriptions include role-specific text, triggers, and job count."""
        workflow = {
            "on": ["push", "pull_request"],
            "jobs": {"lint": {}, "test": {}},
        }

        description = workflow_metadata.generate_description(workflow, "CI", "ci")

        assert description == (
            "Continuous integration workflow for building and testing. "
            "Triggered by push, pull_request, executes 2 job(s)."
        )

    def test_generates_subjects_from_layer_role_name_and_triggers(self):
        """Subjects combine structural metadata with name and trigger keywords."""
        subjects = workflow_metadata.generate_subjects(
            "PR Test Coverage",
            "core",
            "testing",
            ["schedule", "workflow_dispatch", "push", "pull_request"],
        )

        assert subjects == [
            "core",
            "coverage",
            "manual",
            "pr-triggered",
            "pull-request",
            "push-triggered",
            "scheduled",
            "testing",
        ]

    def test_generates_canonical_and_default_names(self):
        """Canonical names and titleized defaults are derived from filenames."""
        assert (
            workflow_metadata.generate_canonical_name("test-coverage.yml", "core", "testing")
            == "core.testing.test.yml"
        )
        assert workflow_metadata.generate_default_workflow_name("test-coverage.yml") == "Test Coverage"


@pytest.mark.unit
class TestGenerateMetadata:
    """Test complete metadata generation for a workflow file."""

    def test_generates_complete_metadata_for_workflow_file(self, tmp_path):
        """Generated metadata contains deterministic identifiers and derived fields."""
        workflow_file = tmp_path / "test-coverage.yml"
        workflow_file.write_text(
            """
name: Test Coverage
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
""".lstrip()
        )

        metadata = workflow_metadata.generate_metadata(workflow_file)

        expected_uuid = uuid.uuid5(
            workflow_metadata.UUID_NAMESPACE_URL,
            "workflow:test-coverage.yml",
        )
        assert metadata["profile"] == "full"
        assert metadata["name"] == "Test Coverage"
        assert metadata["identifier"] == f"urn:uuid:{expected_uuid}"
        assert metadata["functioncalled"] == {
            "canonical": "core.testing.test.yml",
            "layer": "core",
            "role": "testing",
            "domain": "test",
        }
        assert metadata["triggers"] == ["push", "workflow_dispatch"]
        assert "coverage" in metadata["dc:subject"]
        assert "manual" in metadata["dc:subject"]
        assert metadata["runtimePlatform"] == "GitHub Actions"
        assert metadata["dateCreated"].endswith("T00:00:00Z")
        assert metadata["dateModified"] == metadata["dateCreated"]

    def test_uses_default_name_when_workflow_name_is_missing(self, tmp_path):
        """Files without a name field get a human-readable default name."""
        workflow_file = tmp_path / "nightly-cleanup.yml"
        workflow_file.write_text(
            """
on: schedule
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - run: echo clean
""".lstrip()
        )

        metadata = workflow_metadata.generate_metadata(workflow_file)

        assert metadata["name"] == "Nightly Cleanup"
        assert metadata["functioncalled"]["role"] == "maintenance"
        assert metadata["triggers"] == ["schedule"]

    def test_returns_none_for_empty_missing_or_invalid_yaml(self, tmp_path, capsys):
        """Unreadable and invalid workflow files are reported as skipped metadata."""
        empty_file = tmp_path / "empty.yml"
        missing_file = tmp_path / "missing.yml"
        invalid_file = tmp_path / "invalid.yml"
        empty_file.write_text("")
        invalid_file.write_text("name: [unterminated")

        assert workflow_metadata.generate_metadata(empty_file) is None
        assert workflow_metadata.generate_metadata(missing_file) is None
        assert workflow_metadata.generate_metadata(invalid_file) is None

        output = capsys.readouterr().out
        assert "Error processing" in output
        assert str(missing_file) in output
        assert str(invalid_file) in output


@pytest.mark.unit
class TestMain:
    """Test main() file creation behavior."""

    def test_main_creates_missing_metadata_and_skips_existing_files(self, tmp_path, monkeypatch, capsys):
        """main() writes missing metadata, skips existing files, and handles reusable workflows."""
        workflows_dir = tmp_path / ".github" / "workflows"
        reusable_dir = workflows_dir / "reusable"
        reusable_dir.mkdir(parents=True)

        (workflows_dir / "ci.yml").write_text(
            """
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
""".lstrip()
        )
        existing_meta = workflows_dir / "security.yml.meta.json"
        (workflows_dir / "security.yml").write_text(
            """
name: Security Scan
on: workflow_dispatch
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - run: echo scan
""".lstrip()
        )
        existing_meta.write_text('{"existing": true}\n')
        (reusable_dir / "python-setup.yml").write_text(
            """
name: Python Setup
on:
  workflow_call:
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - run: echo setup
""".lstrip()
        )

        monkeypatch.chdir(tmp_path)

        workflow_metadata.main()

        ci_meta = workflows_dir / "ci.yml.meta.json"
        reusable_meta = reusable_dir / "python-setup.yml.meta.json"
        assert ci_meta.exists()
        assert reusable_meta.exists()
        assert json.loads(ci_meta.read_text())["name"] == "CI"
        assert json.loads(reusable_meta.read_text())["functioncalled"]["layer"] == "core"
        assert json.loads(existing_meta.read_text()) == {"existing": True}

        output = capsys.readouterr().out
        assert "Created 2, Skipped 1, Errors 0" in output

    def test_main_reports_missing_workflows_directory(self, tmp_path, monkeypatch, capsys):
        """main() prints an actionable message when run outside a repo root."""
        monkeypatch.chdir(tmp_path)

        workflow_metadata.main()

        output = capsys.readouterr().out
        assert ".github/workflows directory not found" in output
        assert "Run this script from the repository root" in output

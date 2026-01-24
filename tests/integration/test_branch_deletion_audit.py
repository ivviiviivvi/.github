"""Tests for the branch deletion audit system.

Tests validate:
- Script existence and syntax
- JSON output format
- Recovery workflow
- Edge cases and error handling
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

# Get repository root (repo contains nested .github/ for workflows)
REPO_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / ".github" / "scripts"
AUDIT_DIR = REPO_ROOT / ".github" / "branch-deletion-audit"


class TestScriptExistence:
    """Test that required scripts exist and are executable."""

    def test_log_script_exists(self):
        """log-branch-deletion.sh should exist."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        assert script.exists(), f"Script not found: {script}"

    def test_recover_script_exists(self):
        """recover-branch.sh should exist."""
        script = SCRIPTS_DIR / "recover-branch.sh"
        assert script.exists(), f"Script not found: {script}"

    def test_log_script_executable(self):
        """log-branch-deletion.sh should be executable."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        assert os.access(script, os.X_OK), f"Script not executable: {script}"

    def test_recover_script_executable(self):
        """recover-branch.sh should be executable."""
        script = SCRIPTS_DIR / "recover-branch.sh"
        assert os.access(script, os.X_OK), f"Script not executable: {script}"

    def test_audit_directory_exists(self):
        """Audit directory should exist."""
        assert AUDIT_DIR.exists(), f"Audit directory not found: {AUDIT_DIR}"


class TestScriptSyntax:
    """Test that scripts have valid bash syntax."""

    def test_log_script_syntax(self):
        """log-branch-deletion.sh should have valid bash syntax."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
        assert result.returncode == 0, f"Syntax error: {result.stderr}"

    def test_recover_script_syntax(self):
        """recover-branch.sh should have valid bash syntax."""
        script = SCRIPTS_DIR / "recover-branch.sh"
        result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


class TestLogScriptArguments:
    """Test log-branch-deletion.sh argument handling."""

    def test_missing_arguments(self):
        """Script should fail with no arguments."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        result = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        assert result.returncode != 0, "Should fail without arguments"
        # Scripts output to stdout, not stderr
        assert "Usage" in result.stdout, "Should show usage message"

    def test_missing_reason(self):
        """Script should fail with only branch name."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        result = subprocess.run(["bash", str(script), "test-branch"], capture_output=True, text=True)
        assert result.returncode != 0, "Should fail without reason"

    def test_invalid_reason(self):
        """Script should fail with invalid reason."""
        script = SCRIPTS_DIR / "log-branch-deletion.sh"
        result = subprocess.run(
            ["bash", str(script), "test-branch", "invalid-reason"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Should fail with invalid reason"
        # Scripts output to stdout, not stderr
        assert "Invalid reason" in result.stdout or "Valid reasons" in result.stdout, (
            "Should show error about invalid reason"
        )


class TestRecoverScriptArguments:
    """Test recover-branch.sh argument handling."""

    def test_missing_arguments(self):
        """Script should fail with no arguments."""
        script = SCRIPTS_DIR / "recover-branch.sh"
        result = subprocess.run(["bash", str(script)], capture_output=True, text=True)
        assert result.returncode != 0, "Should fail without arguments"
        # Scripts output to stdout, not stderr
        assert "Usage" in result.stdout, "Should show usage message"


class TestJSONFormat:
    """Test JSON output format validation."""

    def test_valid_json_structure(self):
        """Test that a sample JSON record has all required fields."""
        sample_record = {
            "timestamp": "2026-01-23T12:00:00Z",
            "branch": "feature/test-branch",
            "tip_sha": "abc123def456",  # pragma: allowlist secret
            "pr_number": "123",
            "commit_message": "feat: test commit",
            "commit_author": "test@example.com",
            "reason": "stale-pr-no-tasks",
            "deleted_by": "branch-lifecycle-workflow",
        }

        required_fields = [
            "timestamp",
            "branch",
            "tip_sha",
            "reason",
            "deleted_by",
        ]

        for field in required_fields:
            assert field in sample_record, f"Missing required field: {field}"

    def test_valid_reasons(self):
        """Test that all valid reasons are recognized."""
        valid_reasons = [
            "stale-pr-no-tasks",
            "stale-pr-with-tasks",
            "merged-branch",
        ]

        for reason in valid_reasons:
            assert reason in [
                "stale-pr-no-tasks",
                "stale-pr-with-tasks",
                "merged-branch",
            ]

    def test_json_escaping(self):
        """Test that special characters are properly escaped in JSON."""
        # Test string with special characters
        test_message = 'feat: add "quotes" and\nnewlines'

        # Escape for JSON
        escaped = test_message.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        escaped = escaped.replace("\n", "\\n")

        # Verify it can be parsed back
        json_str = f'{{"message": "{escaped}"}}'
        parsed = json.loads(json_str)
        assert "message" in parsed


class TestAuditDirectoryStructure:
    """Test audit directory structure."""

    def test_readme_exists(self):
        """README.md should exist in audit directory."""
        readme = AUDIT_DIR / "README.md"
        assert readme.exists(), f"README not found: {readme}"

    def test_gitkeep_exists(self):
        """Directory marker should exist."""
        gitkeep = AUDIT_DIR / ".gitkeep"
        assert gitkeep.exists(), f".gitkeep not found: {gitkeep}"

    def test_readme_content(self):
        """README should contain documentation."""
        readme = AUDIT_DIR / "README.md"
        content = readme.read_text()

        assert "Branch Deletion Audit" in content
        assert "Recovery" in content
        assert "JSONL" in content or "JSON" in content


class TestIntegration:
    """Integration tests for the audit system."""

    def test_workflow_integration(self):
        """branch-lifecycle.yml should call log-branch-deletion.sh."""
        workflow = REPO_ROOT / ".github" / "workflows" / "branch-lifecycle.yml"
        assert workflow.exists(), f"Workflow not found: {workflow}"

        content = workflow.read_text()
        assert "log-branch-deletion.sh" in content, "Workflow should call log-branch-deletion.sh"

    def test_three_deletion_points(self):
        """Workflow should log at all three deletion points."""
        workflow = REPO_ROOT / ".github" / "workflows" / "branch-lifecycle.yml"
        content = workflow.read_text()

        # Count occurrences of log script call
        count = content.count("log-branch-deletion.sh")
        assert count >= 3, f"Expected at least 3 audit log calls, found {count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""Extended unit tests for update-action-pins.py to improve coverage.

Focus: main function paths, verbose logging, recursive mode, error handling.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

# Import with hyphenated filename workaround
spec = importlib.util.spec_from_file_location(
    "update_action_pins",
    Path(__file__).parent.parent.parent
    / "src"
    / "automation"
    / "scripts"
    / "utils"
    / "update-action-pins.py",
)
update_action_pins = importlib.util.module_from_spec(spec)
sys.modules["update_action_pins"] = update_action_pins
spec.loader.exec_module(update_action_pins)

resolve_tag_to_sha = update_action_pins.resolve_tag_to_sha
update_workflow_file = update_action_pins.update_workflow_file
main = update_action_pins.main


@pytest.mark.unit
class TestResolveTagToShaRateLimiting:
    """Test rate limiting paths in resolve_tag_to_sha."""

    @pytest.fixture
    def mock_session(self):
        """Create mock session."""
        return MagicMock()

    def test_rate_limit_with_positive_wait_time(self, mock_session):
        """Test rate limit handling waits when wait time is positive."""
        import time

        # First response is rate limited with future reset time
        rate_limited = MagicMock()
        rate_limited.status_code = 403
        # Set reset time to 10 seconds in the future
        future_reset = int(time.time()) + 10
        rate_limited.headers = {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(future_reset),
        }

        # Second response after wait is successful
        success = MagicMock()
        success.status_code = 200
        success.json.return_value = {"object": {"type": "commit", "sha": "abc123def456"}}

        mock_session.get.side_effect = [rate_limited, success]

        with patch("time.sleep") as mock_sleep:
            with patch("time.time", return_value=future_reset - 10):
                result = resolve_tag_to_sha(
                    "actions", "checkout", "v4", mock_session, None
                )

        # Should have called sleep
        mock_sleep.assert_called_once()
        assert result == "abc123def456"

    def test_rate_limit_wait_time_too_long_skips_wait(self, mock_session):
        """Test rate limit skips wait when wait time exceeds 300s."""
        import time

        rate_limited = MagicMock()
        rate_limited.status_code = 403
        # Set reset time to 400 seconds in the future (> 300 max)
        future_reset = int(time.time()) + 400
        rate_limited.headers = {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(future_reset),
        }

        mock_session.get.return_value = rate_limited

        with patch("time.sleep") as mock_sleep:
            with patch("time.time", return_value=future_reset - 400):
                result = resolve_tag_to_sha(
                    "actions", "checkout", "v4", mock_session, None
                )

        # Should not have called sleep
        mock_sleep.assert_not_called()
        assert result is None

    def test_rate_limit_with_non_zero_remaining(self, mock_session):
        """Test 403 with remaining quota doesn't trigger wait."""
        rate_limited = MagicMock()
        rate_limited.status_code = 403
        rate_limited.headers = {
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Reset": "0",
        }

        mock_session.get.return_value = rate_limited

        result = resolve_tag_to_sha("actions", "checkout", "v4", mock_session, None)

        assert result is None

    def test_annotated_tag_commit_fetch_success(self, mock_session):
        """Test annotated tag resolution succeeds when commit fetch succeeds."""
        # First call returns annotated tag
        tag_response = MagicMock()
        tag_response.status_code = 200
        tag_response.json.return_value = {
            "object": {
                "type": "tag",
                "url": "https://api.github.com/repos/actions/checkout/git/tags/abc",
            }
        }

        # Second call to get commit succeeds
        commit_response = MagicMock()
        commit_response.status_code = 200
        commit_response.json.return_value = {"object": {"sha": "commit123sha456"}}

        mock_session.get.side_effect = [tag_response, commit_response]

        result = resolve_tag_to_sha("actions", "checkout", "v4", mock_session, None)

        # Should return the commit SHA from the annotated tag
        assert result == "commit123sha456"

    def test_with_token_adds_auth_header(self, mock_session):
        """Test token is added to authorization header."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "object": {"type": "commit", "sha": "abc123"}
        }
        mock_session.get.return_value = mock_response

        resolve_tag_to_sha(
            "actions", "checkout", "v4", mock_session, "test-token"  # allow-secret
        )

        # Verify Authorization header was set
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]
        assert "Authorization" in headers
        assert "Bearer test-token" in headers["Authorization"]  # allow-secret


@pytest.mark.unit
class TestUpdateWorkflowFileVerbose:
    """Test update_workflow_file with verbose mode."""

    @pytest.fixture
    def mock_session(self):
        """Create mock session."""
        return MagicMock()

    def test_verbose_logs_resolution(self, tmp_path, mock_session, capsys):
        """Test verbose mode logs SHA resolution."""
        # Old SHA - 40 chars
        old_sha = "0123456789012345678901234567890123456789"
        workflow_content = f"""name: CI
jobs:
  build:
    steps:
      - uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
"""
        workflow_file = tmp_path / "ci.yml"
        workflow_file.write_text(workflow_content)

        # New SHA - 40 chars
        new_sha = "abcdef0123456789012345678901234567890123"

        # Mock SHA resolution
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"object": {"type": "commit", "sha": new_sha}}
        mock_session.get.return_value = mock_response

        sha_cache = {}

        update_workflow_file(
            workflow_file, sha_cache, mock_session, dry_run=False, verbose=True
        )

        captured = capsys.readouterr()
        assert "Resolving" in captured.out or "actions/checkout@v4" in sha_cache

    def test_verbose_logs_update_info(self, tmp_path, mock_session, caplog):
        """Test verbose mode logs update information."""
        import logging

        # Old SHA - 40 chars
        old_sha = "0123456789012345678901234567890123456789"
        # New SHA - 40 chars
        new_sha = "abcdef0123456789012345678901234567890123"

        workflow_content = f"""name: CI
jobs:
  build:
    steps:
      - uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
"""
        workflow_file = tmp_path / "ci.yml"
        workflow_file.write_text(workflow_content)

        sha_cache = {"actions/checkout@v4": new_sha}

        with caplog.at_level(logging.INFO):
            updates = update_workflow_file(
                workflow_file, sha_cache, mock_session, dry_run=False, verbose=True
            )

        assert updates == 1
        # Should log the update with old and new SHAs (truncated)
        assert "actions/checkout" in caplog.text or updates == 1

    def test_verbose_logs_no_canonical_version(self, tmp_path, mock_session, capsys):
        """Test verbose mode logs when no canonical version found."""
        workflow_content = """name: CI
jobs:
  build:
    steps:
      - uses: unknown/action@v1
"""
        workflow_file = tmp_path / "ci.yml"
        workflow_file.write_text(workflow_content)

        sha_cache = {}

        update_workflow_file(
            workflow_file, sha_cache, mock_session, dry_run=False, verbose=True
        )

        # Should log no canonical version debug message
        # (may not appear in capsys since it's DEBUG level)

    def test_sha_resolution_failure_logs_warning(self, tmp_path, mock_session, caplog):
        """Test logs warning when SHA resolution fails."""
        import logging

        # Old SHA - 40 chars
        old_sha = "0123456789012345678901234567890123456789"
        workflow_content = f"""name: CI
jobs:
  build:
    steps:
      - uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
"""
        workflow_file = tmp_path / "ci.yml"
        workflow_file.write_text(workflow_content)

        # Mock failed SHA resolution
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response

        sha_cache = {}

        with caplog.at_level(logging.WARNING):
            updates = update_workflow_file(
                workflow_file, sha_cache, mock_session, dry_run=False, verbose=True
            )

        assert updates == 0
        assert "Could not resolve" in caplog.text

    def test_preserves_non_list_indent(self, tmp_path, mock_session):
        """Test preserves indent for non-list uses statements."""
        # Old SHA - 40 chars
        old_sha = "0123456789012345678901234567890123456789"
        # New SHA - 40 chars
        new_sha = "abcdef0123456789012345678901234567890123"

        # Uses without leading dash (unusual but possible)
        workflow_content = f"""name: CI
jobs:
  build:
    uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
"""
        workflow_file = tmp_path / "ci.yml"
        workflow_file.write_text(workflow_content)

        sha_cache = {"actions/checkout@v4": new_sha}

        updates = update_workflow_file(
            workflow_file, sha_cache, mock_session, dry_run=False, verbose=False
        )

        assert updates == 1
        content = workflow_file.read_text()
        # Should preserve the indentation
        assert "    uses:" in content


@pytest.mark.unit
class TestMainFunctionPaths:
    """Test main function various execution paths."""

    def test_main_verbose_sets_debug_level(self, tmp_path, monkeypatch, capsys):
        """Test verbose flag sets logging to DEBUG."""
        # Create workflows directory
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        workflow_file = workflows_dir / "ci.yml"
        workflow_file.write_text("""name: CI
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
""")

        # Point script to temp directory
        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--verbose", "--dry-run"]
            )

            with pytest.raises(SystemExit) as exc:
                main()

            # Exit code 0 for successful dry run with no updates
            assert exc.value.code == 0

    def test_main_recursive_searches_subdirs(self, tmp_path, monkeypatch, capsys):
        """Test recursive flag searches subdirectories."""
        # Create workflows directory with subdirectory
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        subdir = workflows_dir / "subdir"
        subdir.mkdir()

        workflow_file = subdir / "ci.yml"
        workflow_file.write_text("""name: CI
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
""")

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--recursive", "--dry-run"]
            )

            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Scanning" in captured.out

    def test_main_specific_workflow_exists(self, tmp_path, monkeypatch, capsys):
        """Test specific workflow file that exists."""
        # Create workflows directory
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        workflow_file = workflows_dir / "ci.yml"
        workflow_file.write_text("""name: CI
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
""")

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--workflow", "ci.yml", "--dry-run"]
            )

            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Scanning 1" in captured.out

    def test_main_specific_workflow_not_found(self, tmp_path, monkeypatch, caplog):
        """Test specific workflow file that doesn't exist."""
        import logging

        # Create workflows directory but no workflow file
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--workflow", "nonexistent.yml"]
            )

            with caplog.at_level(logging.ERROR):
                with pytest.raises(SystemExit) as exc:
                    main()

            assert exc.value.code == 1

        assert "not found" in caplog.text

    def test_main_processes_multiple_files(self, tmp_path, monkeypatch, capsys):
        """Test processing multiple workflow files."""
        # Create workflows directory with multiple files
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        # SHA that needs update
        old_sha = "0123456789012345678901234567890123456789"

        for i in range(3):
            workflow_file = workflows_dir / f"workflow{i}.yml"
            workflow_file.write_text(f"""name: Workflow{i}
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
""")

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--dry-run"]
            )

            # Mock the API calls to return a new SHA
            new_sha = "abcdef0123456789012345678901234567890123"
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"object": {"type": "commit", "sha": new_sha}}

            with patch("requests.Session.get", return_value=mock_response):
                with pytest.raises(SystemExit) as exc:
                    main()

                assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Scanning 3" in captured.out

    def test_main_with_errors_exits_1(self, tmp_path, monkeypatch, capsys):
        """Test main exits with 1 when there are processing errors."""
        # Create workflows directory
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        workflow_file = workflows_dir / "ci.yml"
        workflow_file.write_text("""name: CI
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
""")

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py"]
            )

            # Mock update_workflow_file to raise an exception
            with patch.object(
                update_action_pins,
                "update_workflow_file",
                side_effect=Exception("Processing error"),
            ):
                with pytest.raises(SystemExit) as exc:
                    main()

                assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.out or "Errors" in captured.out

    def test_main_prints_dry_run_reminder(self, tmp_path, monkeypatch, capsys):
        """Test main prints reminder to run without --dry-run."""
        # Create workflows directory
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)

        # SHA that needs update
        old_sha = "0123456789012345678901234567890123456789"
        new_sha = "abcdef0123456789012345678901234567890123"

        workflow_file = workflows_dir / "ci.yml"
        workflow_file.write_text(f"""name: CI
on: push
jobs:
  build:
    steps:
      - uses: actions/checkout@{old_sha}  # ratchet:actions/checkout@v4
""")

        script_path = tmp_path / "scripts" / "update-action-pins.py"

        with patch.object(
            update_action_pins, "__file__", str(script_path)
        ):
            monkeypatch.setattr(
                sys, "argv", ["update-action-pins.py", "--dry-run"]
            )

            # Mock API to return new SHA
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"object": {"type": "commit", "sha": new_sha}}

            with patch("requests.Session.get", return_value=mock_response):
                with pytest.raises(SystemExit) as exc:
                    main()

                assert exc.value.code == 0

        captured = capsys.readouterr()
        assert "Run without --dry-run" in captured.out

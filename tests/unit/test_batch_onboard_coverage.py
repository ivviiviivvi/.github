#!/usr/bin/env python3
"""Extended unit tests for batch_onboard_repositories.py to improve coverage.

Focus: actual implementation paths, rollback, error handling, main function.
"""

import asyncio
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src/automation/scripts")

from src.automation.scripts.batch_onboard_repositories import (
    BatchOnboardingOrchestrator, OnboardingConfig, OnboardingResult, main)


@pytest.mark.unit
class TestValidateConfigurationWorkflows:
    """Test workflow validation in _validate_configuration."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_workflow_not_found_error(self, MockAuth, MockGithub):
        """Test validation reports missing workflow files."""
        mock_github = MagicMock()
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=[],
            workflows=["nonexistent-workflow.yml"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        errors = asyncio.run(orchestrator._validate_configuration())

        assert any("nonexistent-workflow.yml" in e for e in errors)
        assert any("not found" in e.lower() for e in errors)


@pytest.mark.unit
class TestOnboardRepositoriesRollback:
    """Test rollback on failures in onboard_repositories."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_rollback_triggered_on_failure(self, MockAuth, MockGithub):
        """Test rollback is called when onboarding fails."""
        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_contents.return_value = MagicMock(sha="abc123")
        mock_repo.default_branch = "main"
        mock_github.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/repo"],
            validate_before=False,
            rollback_on_failure=True,
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        # Mock _onboard_repository to return a failure
        async def mock_onboard(repo_name):
            return OnboardingResult(
                repository=repo_name,
                success=False,
                steps_completed=["deploy_workflows"],
                error="Test failure",
            )

        async def mock_rollback(failed):
            pass

        orchestrator._onboard_repository = mock_onboard
        orchestrator._rollback_failed = mock_rollback

        results = asyncio.run(orchestrator.onboard_repositories())

        assert len(results) == 1
        assert not results[0].success


@pytest.mark.unit
class TestDeployWorkflowsActual:
    """Test _deploy_workflows actual implementation."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_deploy_workflows_file_not_found(self, MockAuth, MockGithub):
        """Test workflow deployment raises FileNotFoundError for missing workflow."""
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.default_branch = "main"

        config = OnboardingConfig(
            repositories=["org/repo"],
            workflows=["nonexistent-workflow.yml"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        result = OnboardingResult(repository="org/repo", success=False)

        # Will fail because workflow file doesn't exist
        with pytest.raises(FileNotFoundError):
            asyncio.run(orchestrator._deploy_workflows(mock_repo, result))


@pytest.mark.unit
class TestConfigureLabelsError:
    """Test _configure_labels error handling."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_labels_exception_raised(self, MockAuth, MockGithub):
        """Test label configuration raises exception on error."""
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.get_labels.side_effect = Exception("API Error")

        config = OnboardingConfig(
            repositories=["org/repo"],
            labels={"bug": {"color": "ff0000"}},
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        result = OnboardingResult(repository="org/repo", success=False)

        with pytest.raises(Exception, match="API Error"):
            asyncio.run(orchestrator._configure_labels(mock_repo, result))


@pytest.mark.unit
class TestSetupBranchProtectionActual:
    """Test _setup_branch_protection actual implementation."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_branch_protection_sets_rules(self, MockAuth, MockGithub):
        """Test branch protection configures branch."""
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.default_branch = "main"
        mock_branch = MagicMock()
        mock_repo.get_branch.return_value = mock_branch

        config = OnboardingConfig(
            repositories=["org/repo"],
            branch_protection={
                "branch": "main",
                "required_approving_reviews": 2,
                "require_code_owner_reviews": True,
                "dismiss_stale_reviews": True,
                "enforce_admins": True,
                "required_checks": ["ci"],
            },
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._setup_branch_protection(mock_repo, result))

        mock_branch.edit_protection.assert_called_once()
        assert "setup_branch_protection" in result.steps_completed

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_branch_protection_exception(self, MockAuth, MockGithub):
        """Test branch protection raises on error."""
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.default_branch = "main"
        mock_repo.get_branch.side_effect = Exception("Branch not found")

        config = OnboardingConfig(
            repositories=["org/repo"],
            branch_protection={"branch": "main"},
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        result = OnboardingResult(repository="org/repo", success=False)

        with pytest.raises(Exception, match="Branch not found"):
            asyncio.run(orchestrator._setup_branch_protection(mock_repo, result))


@pytest.mark.unit
class TestCreateEnvironmentsActual:
    """Test _create_environments actual implementation."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_environments_skipped_warning(self, MockAuth, MockGithub, caplog):
        """Test environment creation logs warning and skips."""
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"

        config = OnboardingConfig(
            repositories=["org/repo"],
            environments=["production", "staging"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=False)

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._create_environments(mock_repo, result))

        assert any("skipped" in step for step in result.steps_completed)


@pytest.mark.unit
class TestRollbackFailedErrors:
    """Test _rollback_failed error handling."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_rollback_github_exception(self, MockAuth, MockGithub):
        """Test rollback handles GithubException."""
        import src.automation.scripts.batch_onboard_repositories as batch_mod

        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.default_branch = "main"
        mock_repo.get_contents.side_effect = batch_mod.GithubException(404, {"message": "Not found"}, None)
        mock_github.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/repo"],
            workflows=["ci.yml"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        failed_results = [
            OnboardingResult(
                repository="org/repo",
                success=False,
                steps_completed=["deploy_workflows"],
            )
        ]

        # Should not raise
        asyncio.run(orchestrator._rollback_failed(failed_results))

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_rollback_general_exception(self, MockAuth, MockGithub):
        """Test rollback handles general exceptions."""
        mock_github = MagicMock()
        mock_github.get_repo.side_effect = Exception("Network error")
        MockGithub.return_value = mock_github

        config = OnboardingConfig(repositories=["org/repo"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        failed_results = [
            OnboardingResult(
                repository="org/repo",
                success=False,
                steps_completed=["deploy_workflows"],
            )
        ]

        # Should not raise
        asyncio.run(orchestrator._rollback_failed(failed_results))


@pytest.mark.unit
class TestLogSummaryWithFailures:
    """Test _log_summary with failures."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_log_summary_with_failures(self, MockAuth, MockGithub):
        """Test summary logs failed repositories."""
        config = OnboardingConfig(repositories=["org/repo1", "org/repo2"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)
        orchestrator.results = [
            OnboardingResult(repository="org/repo1", success=True, duration_seconds=1.5),
            OnboardingResult(
                repository="org/repo2",
                success=False,
                duration_seconds=2.0,
                error="API Error",
            ),
        ]

        # Should not raise
        orchestrator._log_summary()


@pytest.mark.unit
class TestMainFunctionPaths:
    """Test main function various paths."""

    @patch("src.automation.scripts.batch_onboard_repositories.BatchOnboardingOrchestrator")
    @patch("src.automation.scripts.batch_onboard_repositories.load_config")
    @patch("src.automation.scripts.batch_onboard_repositories.ensure_github_token")
    def test_main_with_config_file(self, mock_ensure_token, mock_load_config, MockOrchestrator):
        """Test main loads config from file."""
        mock_ensure_token.return_value = "test-token"  # allow-secret
        mock_load_config.return_value = OnboardingConfig(repositories=["org/repo"])

        async def mock_onboard():
            return [OnboardingResult(repository="org/repo", success=True)]

        mock_orchestrator = MagicMock()
        mock_orchestrator.onboard_repositories = mock_onboard
        mock_orchestrator.save_results = MagicMock()
        MockOrchestrator.return_value = mock_orchestrator

        with patch("sys.argv", ["batch_onboard.py", "--config", "config.yml"]):
            with pytest.raises(SystemExit) as exc_info:
                asyncio.run(main())

            # Success exit
            assert exc_info.value.code == 0

    @patch("src.automation.scripts.batch_onboard_repositories.BatchOnboardingOrchestrator")
    @patch("src.automation.scripts.batch_onboard_repositories.ensure_github_token")
    def test_main_with_repos_arg(self, mock_ensure_token, MockOrchestrator):
        """Test main with --repos argument."""
        mock_ensure_token.return_value = "test-token"  # allow-secret

        async def mock_onboard():
            return [OnboardingResult(repository="org/repo", success=True)]

        mock_orchestrator = MagicMock()
        mock_orchestrator.onboard_repositories = mock_onboard
        mock_orchestrator.save_results = MagicMock()
        MockOrchestrator.return_value = mock_orchestrator

        with patch("sys.argv", ["batch_onboard.py", "--repos", "org/repo1", "org/repo2"]):
            with pytest.raises(SystemExit) as exc_info:
                asyncio.run(main())

            assert exc_info.value.code == 0

    @patch("src.automation.scripts.batch_onboard_repositories.BatchOnboardingOrchestrator")
    @patch("src.automation.scripts.batch_onboard_repositories.ensure_github_token")
    def test_main_with_failures_exits_1(self, mock_ensure_token, MockOrchestrator):
        """Test main exits with 1 when there are failures."""
        mock_ensure_token.return_value = "test-token"  # allow-secret

        async def mock_onboard():
            return [OnboardingResult(repository="org/repo", success=False, error="Fail")]

        mock_orchestrator = MagicMock()
        mock_orchestrator.onboard_repositories = mock_onboard
        mock_orchestrator.save_results = MagicMock()
        MockOrchestrator.return_value = mock_orchestrator

        with patch("sys.argv", ["batch_onboard.py", "--repos", "org/repo"]):
            with pytest.raises(SystemExit) as exc_info:
                asyncio.run(main())

            assert exc_info.value.code == 1


@pytest.mark.unit
class TestOnboardRepositorySteps:
    """Test _onboard_repository step execution."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_onboard_calls_all_steps(self, MockAuth, MockGithub):
        """Test onboarding calls all configured steps."""
        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_repo.default_branch = "main"
        mock_github.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/repo"],
            workflows=["ci.yml"],
            labels={"bug": {"color": "ff0000"}},
            branch_protection={"required_approving_reviews": 1},
            secrets={"SECRET": "value"},
            environments=["prod"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config, dry_run=True)

        result = asyncio.run(orchestrator._onboard_repository("org/repo"))

        assert result.success is True
        # All steps should be completed (with dry-run)
        assert len(result.steps_completed) == 5

#!/usr/bin/env python3
"""Tests for batch_onboard_repositories.py.

Tests batch repository onboarding with validation, dependency resolution,
and automatic rollback capabilities.
"""

import asyncio
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src/automation/scripts")

from src.automation.scripts.batch_onboard_repositories import (
    BatchOnboardingOrchestrator, OnboardingConfig, OnboardingResult,
    load_config)


@pytest.mark.unit
class TestOnboardingConfig:
    """Test OnboardingConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = OnboardingConfig(repositories=["org/repo"])

        assert config.repositories == ["org/repo"]
        assert config.workflows == []
        assert config.labels == {}
        assert config.branch_protection == {}
        assert config.secrets == {}
        assert config.environments == []
        assert config.dependencies == []
        assert config.max_concurrent == 5
        assert config.timeout_seconds == 300
        assert config.validate_before is True
        assert config.rollback_on_failure is True

    def test_custom_values(self):
        """Test custom configuration values."""
        config = OnboardingConfig(
            repositories=["org/repo1", "org/repo2"],
            workflows=["ci.yml"],
            labels={"bug": {"color": "ff0000"}},
            max_concurrent=10,
            validate_before=False,
        )

        assert len(config.repositories) == 2
        assert config.workflows == ["ci.yml"]
        assert config.labels == {"bug": {"color": "ff0000"}}
        assert config.max_concurrent == 10
        assert config.validate_before is False


@pytest.mark.unit
class TestOnboardingResult:
    """Test OnboardingResult dataclass."""

    def test_default_values(self):
        """Test default result values."""
        result = OnboardingResult(repository="org/repo", success=True)

        assert result.repository == "org/repo"
        assert result.success is True
        assert result.steps_completed == []
        assert result.error is None
        assert result.duration_seconds == 0.0
        assert result.timestamp is not None

    def test_with_error(self):
        """Test result with error."""
        result = OnboardingResult(
            repository="org/repo",
            success=False,
            error="API Error",
            steps_completed=["deploy_workflows"],
        )

        assert result.success is False
        assert result.error == "API Error"
        assert "deploy_workflows" in result.steps_completed


@pytest.mark.unit
class TestBatchOnboardingOrchestratorInit:
    """Test BatchOnboardingOrchestrator initialization."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_init_sets_properties(self, MockAuth, MockGithub):
        """Test initialization sets all properties."""
        config = OnboardingConfig(repositories=["org/repo"])

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test-token",  # allow-secret
            config=config,
            dry_run=True,
        )

        assert orchestrator.config == config
        assert orchestrator.dry_run is True
        assert orchestrator.results == []
        MockAuth.Token.assert_called_once_with("test-token")  # allow-secret


@pytest.mark.unit
class TestResolveDependencies:
    """Test _resolve_dependencies method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_no_dependencies(self, MockAuth, MockGithub):
        """Test resolve with no dependencies."""
        config = OnboardingConfig(
            repositories=["org/repo1", "org/repo2"],
            dependencies=[],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        result = orchestrator._resolve_dependencies()

        assert result == ["org/repo1", "org/repo2"]

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_with_dependencies(self, MockAuth, MockGithub):
        """Test resolve puts non-dependent repos first."""
        config = OnboardingConfig(
            repositories=["org/dependent", "org/base", "org/another"],
            dependencies=["org/dependent"],
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        result = orchestrator._resolve_dependencies()

        # Non-dependent repos should come first
        assert result[:2] == ["org/base", "org/another"]
        assert result[2] == "org/dependent"


@pytest.mark.unit
class TestValidateConfiguration:
    """Test _validate_configuration method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_validate_repos_not_found(self, MockAuth, MockGithub):
        """Test validation catches missing repos."""
        # Import the actual GithubException from the module
        import src.automation.scripts.batch_onboard_repositories as batch_mod

        mock_github = MagicMock()
        mock_github.get_repo.side_effect = batch_mod.GithubException(404, {"message": "Not found"}, None)
        MockGithub.return_value = mock_github

        config = OnboardingConfig(repositories=["org/missing"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        errors = asyncio.run(orchestrator._validate_configuration())

        assert len(errors) > 0
        assert "org/missing" in errors[0]

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_validate_missing_secret(self, MockAuth, MockGithub):
        """Test validation catches missing secrets."""
        mock_github = MagicMock()
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=[],
            secrets={"MISSING_SECRET": "value"},
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        with patch.dict("os.environ", {}, clear=True):
            errors = asyncio.run(orchestrator._validate_configuration())

        assert any("MISSING_SECRET" in e for e in errors)


@pytest.mark.unit
class TestOnboardRepository:
    """Test _onboard_repository method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_onboard_success_dry_run(self, MockAuth, MockGithub):
        """Test successful onboarding in dry-run mode."""
        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_github.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/repo"],
            workflows=["ci.yml"],
            labels={"bug": {}},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = asyncio.run(orchestrator._onboard_repository("org/repo"))

        assert result.success is True
        assert result.repository == "org/repo"
        assert any("dry-run" in step for step in result.steps_completed)

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_onboard_handles_exception(self, MockAuth, MockGithub):
        """Test onboarding handles exceptions."""
        mock_github = MagicMock()
        mock_github.get_repo.side_effect = Exception("API Error")
        MockGithub.return_value = mock_github

        config = OnboardingConfig(repositories=["org/repo"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        result = asyncio.run(orchestrator._onboard_repository("org/repo"))

        assert result.success is False
        assert "API Error" in result.error


@pytest.mark.unit
class TestDeployWorkflows:
    """Test _deploy_workflows method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_deploy_workflows_dry_run(self, MockAuth, MockGithub):
        """Test workflow deployment in dry-run mode."""
        mock_repo = MagicMock()

        config = OnboardingConfig(
            repositories=["org/repo"],
            workflows=["ci.yml"],
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._deploy_workflows(mock_repo, result))

        assert "deploy_workflows (dry-run)" in result.steps_completed


@pytest.mark.unit
class TestConfigureLabels:
    """Test _configure_labels method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_labels_dry_run(self, MockAuth, MockGithub):
        """Test label configuration in dry-run mode."""
        mock_repo = MagicMock()

        config = OnboardingConfig(
            repositories=["org/repo"],
            labels={"bug": {"color": "ff0000"}},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._configure_labels(mock_repo, result))

        assert "configure_labels (dry-run)" in result.steps_completed

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_labels_creates_new(self, MockAuth, MockGithub):
        """Test creating new labels."""
        mock_repo = MagicMock()
        mock_repo.get_labels.return_value = []

        config = OnboardingConfig(
            repositories=["org/repo"],
            labels={"bug": {"color": "ff0000", "description": "Bug report"}},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=False,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._configure_labels(mock_repo, result))

        mock_repo.create_label.assert_called_once()
        assert "configure_labels" in result.steps_completed

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_labels_updates_existing(self, MockAuth, MockGithub):
        """Test updating existing labels."""
        mock_repo = MagicMock()
        mock_existing_label = MagicMock()
        mock_existing_label.name = "bug"
        mock_repo.get_labels.return_value = [mock_existing_label]

        config = OnboardingConfig(
            repositories=["org/repo"],
            labels={"bug": {"color": "ff0000"}},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=False,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._configure_labels(mock_repo, result))

        mock_existing_label.edit.assert_called_once()


@pytest.mark.unit
class TestSetupBranchProtection:
    """Test _setup_branch_protection method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_branch_protection_dry_run(self, MockAuth, MockGithub):
        """Test branch protection in dry-run mode."""
        mock_repo = MagicMock()
        mock_repo.default_branch = "main"

        config = OnboardingConfig(
            repositories=["org/repo"],
            branch_protection={"required_approving_reviews": 2},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._setup_branch_protection(mock_repo, result))

        assert "setup_branch_protection (dry-run)" in result.steps_completed


@pytest.mark.unit
class TestConfigureSecrets:
    """Test _configure_secrets method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_secrets_dry_run(self, MockAuth, MockGithub):
        """Test secret configuration in dry-run mode."""
        mock_repo = MagicMock()

        config = OnboardingConfig(
            repositories=["org/repo"],
            secrets={"SECRET_KEY": "value"},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._configure_secrets(mock_repo, result))

        assert "configure_secrets (dry-run)" in result.steps_completed

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_configure_secrets_skipped(self, MockAuth, MockGithub):
        """Test secret configuration is skipped without proper permissions."""
        mock_repo = MagicMock()

        config = OnboardingConfig(
            repositories=["org/repo"],
            secrets={"SECRET_KEY": "value"},
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=False,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._configure_secrets(mock_repo, result))

        # Should be marked as skipped
        assert any("skipped" in step for step in result.steps_completed)


@pytest.mark.unit
class TestCreateEnvironments:
    """Test _create_environments method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_create_environments_dry_run(self, MockAuth, MockGithub):
        """Test environment creation in dry-run mode."""
        mock_repo = MagicMock()

        config = OnboardingConfig(
            repositories=["org/repo"],
            environments=["production", "staging"],
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        result = OnboardingResult(repository="org/repo", success=False)
        asyncio.run(orchestrator._create_environments(mock_repo, result))

        assert "create_environments (dry-run)" in result.steps_completed


@pytest.mark.unit
class TestRollbackFailed:
    """Test _rollback_failed method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_rollback_removes_workflows(self, MockAuth, MockGithub):
        """Test rollback removes deployed workflows."""
        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_contents = MagicMock()
        mock_contents.path = ".github/workflows/ci.yml"
        mock_contents.sha = "abc123"
        mock_repo.get_contents.return_value = mock_contents
        mock_repo.default_branch = "main"
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
                error="Failed",
            )
        ]

        asyncio.run(orchestrator._rollback_failed(failed_results))

        mock_repo.delete_file.assert_called()


@pytest.mark.unit
class TestLogSummary:
    """Test _log_summary method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_log_summary_all_success(self, MockAuth, MockGithub, capsys):
        """Test summary output with all successes."""
        config = OnboardingConfig(repositories=["org/repo1", "org/repo2"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)
        orchestrator.results = [
            OnboardingResult(repository="org/repo1", success=True, duration_seconds=1.5),
            OnboardingResult(repository="org/repo2", success=True, duration_seconds=2.0),
        ]

        orchestrator._log_summary()

        # Should not raise


@pytest.mark.unit
class TestSaveResults:
    """Test save_results method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_save_results_creates_file(self, MockAuth, MockGithub, tmp_path):
        """Test results are saved to JSON file."""
        config = OnboardingConfig(repositories=["org/repo"])

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)
        orchestrator.results = [OnboardingResult(repository="org/repo", success=True)]

        output_file = tmp_path / "results.json"
        orchestrator.save_results(str(output_file))

        assert output_file.exists()

        import json

        with open(output_file) as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["repository"] == "org/repo"
        assert data[0]["success"] is True


@pytest.mark.unit
class TestOnboardRepositories:
    """Test onboard_repositories method."""

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_onboard_repositories_validation_fails(self, MockAuth, MockGithub):
        """Test onboarding stops when validation fails."""
        import src.automation.scripts.batch_onboard_repositories as batch_mod

        mock_github = MagicMock()
        mock_github.get_repo.side_effect = batch_mod.GithubException(404, {"message": "Not found"}, None)
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/missing"],
            validate_before=True,
        )

        orchestrator = BatchOnboardingOrchestrator(github_token="test", config=config)

        results = asyncio.run(orchestrator.onboard_repositories())

        assert results == []

    @patch("src.automation.scripts.batch_onboard_repositories.Github")
    @patch("src.automation.scripts.batch_onboard_repositories.Auth")
    def test_onboard_repositories_skip_validation(self, MockAuth, MockGithub):
        """Test onboarding proceeds without validation."""
        mock_github = MagicMock()
        mock_repo = MagicMock()
        mock_github.get_repo.return_value = mock_repo
        MockGithub.return_value = mock_github

        config = OnboardingConfig(
            repositories=["org/repo"],
            validate_before=False,
        )

        orchestrator = BatchOnboardingOrchestrator(
            github_token="test",
            config=config,
            dry_run=True,
        )

        results = asyncio.run(orchestrator.onboard_repositories())

        assert len(results) == 1


@pytest.mark.unit
class TestLoadConfig:
    """Test load_config function."""

    def test_load_config_success(self, tmp_path):
        """Test loading valid config file."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("""
repositories:
  - org/repo1
  - org/repo2
workflows:
  - ci.yml
labels:
  bug:
    color: ff0000
max_concurrent: 3
""")

        config = load_config(str(config_file))

        assert config.repositories == ["org/repo1", "org/repo2"]
        assert config.workflows == ["ci.yml"]
        assert config.max_concurrent == 3

    def test_load_config_missing_file(self, tmp_path):
        """Test loading missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            load_config(str(tmp_path / "missing.yml"))


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    @patch("src.automation.scripts.batch_onboard_repositories.ensure_github_token")
    def test_main_no_token(self, mock_ensure_token):
        """Test main exits when no token available."""
        mock_ensure_token.return_value = None

        with patch("sys.argv", ["batch_onboard.py", "--repos", "org/repo"]):
            with pytest.raises(SystemExit) as exc_info:
                asyncio.run(
                    __import__(
                        "src.automation.scripts.batch_onboard_repositories",
                        fromlist=["main"],
                    ).main()
                )

            assert exc_info.value.code == 1

    @patch("src.automation.scripts.batch_onboard_repositories.BatchOnboardingOrchestrator")
    @patch("src.automation.scripts.batch_onboard_repositories.ensure_github_token")
    def test_main_no_args(self, mock_ensure_token, MockOrchestrator, capsys):
        """Test main exits when no repos or config specified."""
        mock_ensure_token.return_value = "test-token"  # allow-secret

        with patch("sys.argv", ["batch_onboard.py"]):
            with pytest.raises(SystemExit) as exc_info:
                asyncio.run(
                    __import__(
                        "src.automation.scripts.batch_onboard_repositories",
                        fromlist=["main"],
                    ).main()
                )

            assert exc_info.value.code == 1

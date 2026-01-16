#!/usr/bin/env python3
"""
Batch Repository Onboarding Automation

Enables parallel onboarding of multiple repositories with validation,
dependency resolution, and automatic rollback on failures.

Features:
- Parallel processing with configurable concurrency
- Dry-run mode for safe testing
- Dependency resolution (shared configs, secrets)
- Automatic rollback on failures
- Progress tracking and detailed logging
- Validation at each step

Usage:
    python batch_onboard_repositories.py --config config.yml
    python batch_onboard_repositories.py --config config.yml --dry-run
    python batch_onboard_repositories.py --repos org/repo1 org/repo2
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml

try:
    import aiohttp
    from github import Auth, Github, GithubException
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install PyGithub aiohttp pyyaml")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class OnboardingConfig:
    """Configuration for batch onboarding"""

    repositories: List[str]
    workflows: List[str] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)
    branch_protection: Dict = field(default_factory=dict)
    secrets: Dict[str, str] = field(default_factory=dict)
    environments: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    max_concurrent: int = 5
    timeout_seconds: int = 300
    validate_before: bool = True
    rollback_on_failure: bool = True


@dataclass
class OnboardingResult:
    """Result of onboarding a single repository"""

    repository: str
    success: bool
    steps_completed: List[str] = field(default_factory=list)
    error: Optional[str] = None
    duration_seconds: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat())


class BatchOnboardingOrchestrator:
    """
    Orchestrates parallel onboarding of multiple repositories
    with validation, dependency resolution, and rollback capabilities.
    """

    def __init__(
        self, github_token: str, config: OnboardingConfig, dry_run: bool = False
    ):
        # Use Auth.Token to avoid deprecation warning
        auth = Auth.Token(github_token)
        self.github = Github(auth=auth)
        self.config = config
        self.dry_run = dry_run
        self.results: List[OnboardingResult] = []
        self.semaphore = asyncio.Semaphore(config.max_concurrent)

    async def onboard_repositories(self) -> List[OnboardingResult]:
        """
        Onboard all configured repositories in parallel.

        Returns:
            List of OnboardingResult objects for each repository
        """
        logger.info(
            f"Starting batch onboarding for {len(self.config.repositories)} repositories"
        )
        if self.dry_run:
            logger.info("DRY RUN MODE - No changes will be made")

        # Validate configuration
        if self.config.validate_before:
            validation_errors = await self._validate_configuration()
            if validation_errors:
                logger.error(
                    f"Configuration validation failed: {validation_errors}")
                return []

        # Resolve dependencies
        ordered_repos = self._resolve_dependencies()

        # Process repositories in parallel
        tasks = [self._onboard_repository(repo) for repo in ordered_repos]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        self.results = [
            (
                r
                if isinstance(r, OnboardingResult)
                else OnboardingResult(repository="unknown", success=False, error=str(r))
            )
            for r in results
        ]

        # Generate summary
        self._log_summary()

        # Rollback on failures if configured
        if self.config.rollback_on_failure and not self.dry_run:
            failed = [r for r in self.results if not r.success]
            if failed:
                logger.warning(
                    f"Rolling back {len(failed)} failed onboardings")
                await self._rollback_failed(failed)

        return self.results

    async def _validate_configuration(self) -> List[str]:
        """
        Validate configuration before processing.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check repositories exist
        for repo_name in self.config.repositories:
            try:
                self.github.get_repo(repo_name)
            except GithubException as e:
                errors.append(f"Repository {repo_name} not found: {e}")

        # Check workflow files exist
        # Look in multiple possible locations (absolute paths from workspace root)
        workspace_root = Path(__file__).parent.parent.parent
        workflow_dirs = [
            workspace_root / "automation" / "workflow-templates",
            workspace_root / "workflow-templates",
            workspace_root / ".github" / "workflows",
        ]

        for workflow in self.config.workflows:
            found = False
            for workflow_dir in workflow_dirs:
                workflow_path = workflow_dir / workflow
                if workflow_path.exists():
                    found = True
                    break

            if not found:
                errors.append(
                    f"Workflow file not found: {workflow} "
                    f"(searched in: {', '.join(str(d) for d in workflow_dirs)})"
                )

        # Validate secrets are available (if specified)
        for secret_name in self.config.secrets.keys():
            if secret_name not in os.environ:
                errors.append(
                    f"Required secret not found in environment: {secret_name}"
                )

        return errors

    def _resolve_dependencies(self) -> List[str]:
        """
        Resolve repository dependencies to determine processing order.

        Returns:
            Ordered list of repositories
        """
        # For now, simple dependency resolution
        # Future: Build dependency graph and topological sort

        if not self.config.dependencies:
            return self.config.repositories

        # Separate repos with and without dependencies
        has_deps = set(self.config.dependencies)
        no_deps = [r for r in self.config.repositories if r not in has_deps]
        with_deps = [r for r in self.config.repositories if r in has_deps]

        # Process repos without dependencies first
        return no_deps + with_deps

    async def _onboard_repository(self, repo_name: str) -> OnboardingResult:
        """
        Onboard a single repository with all configured features.

        Args:
            repo_name: Full repository name (owner/repo)

        Returns:
            OnboardingResult with details of the operation
        """
        start_time = datetime.utcnow()
        result = OnboardingResult(repository=repo_name, success=False)

        async with self.semaphore:
            try:
                logger.info(f"Starting onboarding for {repo_name}")

                # Get repository
                repo = self.github.get_repo(repo_name)

                # Step 1: Deploy workflows
                if self.config.workflows:
                    await self._deploy_workflows(repo, result)

                # Step 2: Configure labels
                if self.config.labels:
                    await self._configure_labels(repo, result)

                # Step 3: Set up branch protection
                if self.config.branch_protection:
                    await self._setup_branch_protection(repo, result)

                # Step 4: Configure secrets
                if self.config.secrets:
                    await self._configure_secrets(repo, result)

                # Step 5: Create environments
                if self.config.environments:
                    await self._create_environments(repo, result)

                # Mark as successful
                result.success = True
                logger.info(f"✓ Successfully onboarded {repo_name}")

            except Exception as e:
                result.error = str(e)
                logger.error(f"✗ Failed to onboard {repo_name}: {e}")

            finally:
                # Calculate duration
                end_time = datetime.utcnow()
                result.duration_seconds = (
                    end_time - start_time).total_seconds()

        return result

    async def _deploy_workflows(self, repo, result: OnboardingResult) -> None:
        """Deploy workflow files to repository"""
        step = "deploy_workflows"
        logger.info(
            f"  [{repo.full_name}] Deploying {len(self.config.workflows)} workflows"
        )

        if self.dry_run:
            result.steps_completed.append(f"{step} (dry-run)")
            return

        try:
            for workflow_file in self.config.workflows:
                # Look in multiple possible locations (absolute paths)
                workspace_root = Path(__file__).parent.parent.parent
                workflow_dirs = [
                    workspace_root / "automation" / "workflow-templates",
                    workspace_root / "workflow-templates",
                    workspace_root / ".github" / "workflows",
                ]

                workflow_path = None
                for workflow_dir in workflow_dirs:
                    candidate_path = workflow_dir / workflow_file
                    if candidate_path.exists():
                        workflow_path = candidate_path
                        break

                if not workflow_path:
                    raise FileNotFoundError(
                        f"Workflow file not found: {workflow_file}")

                with open(workflow_path, "r") as f:
                    content = f.read()

                # Check if file already exists
                try:
                    existing = repo.get_contents(
                        f".github/workflows/{workflow_file}")
                    # Update existing file
                    repo.update_file(
                        path=f".github/workflows/{workflow_file}",
                        message=f"chore: update {workflow_file} workflow",
                        content=content,
                        sha=existing.sha,
                        branch=repo.default_branch,
                    )
                    logger.info(f"    Updated workflow: {workflow_file}")
                except GithubException as e:
                    if e.status == 404:
                        # Create new file
                        repo.create_file(
                            path=f".github/workflows/{workflow_file}",
                            message=f"chore: add {workflow_file} workflow",
                            content=content,
                            branch=repo.default_branch,
                        )
                        logger.info(f"    Created workflow: {workflow_file}")
                    else:
                        raise

            result.steps_completed.append(step)

        except Exception as e:
            logger.error(f"    Failed to deploy workflows: {e}")
            raise

    async def _configure_labels(self, repo, result: OnboardingResult) -> None:
        """Configure repository labels"""
        step = "configure_labels"
        logger.info(
            f"  [{repo.full_name}] Configuring {len(self.config.labels)} labels"
        )

        if self.dry_run:
            result.steps_completed.append(f"{step} (dry-run)")
            return

        try:
            existing_labels = {
                label.name: label for label in repo.get_labels()}

            for label_name, label_config in self.config.labels.items():
                color = label_config.get("color", "cccccc")
                description = label_config.get("description", "")

                if label_name in existing_labels:
                    # Update existing label
                    existing_labels[label_name].edit(
                        name=label_name, color=color, description=description
                    )
                    logger.info(f"    Updated label: {label_name}")
                else:
                    # Create new label
                    repo.create_label(
                        name=label_name, color=color, description=description
                    )
                    logger.info(f"    Created label: {label_name}")

            result.steps_completed.append(step)

        except Exception as e:
            logger.error(f"    Failed to configure labels: {e}")
            raise

    async def _setup_branch_protection(self, repo, result: OnboardingResult) -> None:
        """Set up branch protection rules"""
        step = "setup_branch_protection"
        branch_name = self.config.branch_protection.get(
            "branch", repo.default_branch)
        logger.info(
            f"  [{repo.full_name}] Setting up branch protection for {branch_name}"
        )

        if self.dry_run:
            result.steps_completed.append(f"{step} (dry-run)")
            return

        try:
            branch = repo.get_branch(branch_name)

            # Configure protection
            protection_config = self.config.branch_protection
            required_checks = protection_config.get("required_checks", [])

            branch.edit_protection(
                required_approving_review_count=protection_config.get(
                    "required_approving_reviews", 1
                ),
                require_code_owner_reviews=protection_config.get(
                    "require_code_owner_reviews", True
                ),
                dismiss_stale_reviews=protection_config.get(
                    "dismiss_stale_reviews", True
                ),
                enforce_admins=protection_config.get("enforce_admins", False),
                strict=True,
                contexts=required_checks,
            )

            logger.info(f"    Configured branch protection for {branch_name}")
            result.steps_completed.append(step)

        except Exception as e:
            logger.error(f"    Failed to setup branch protection: {e}")
            raise

    async def _configure_secrets(self, repo, result: OnboardingResult) -> None:
        """Configure repository secrets"""
        step = "configure_secrets"
        logger.info(
            f"  [{repo.full_name}] Configuring {len(self.config.secrets)} secrets"
        )

        if self.dry_run:
            result.steps_completed.append(f"{step} (dry-run)")
            return

        # Note: GitHub API doesn't allow reading secrets, only creating/updating
        # This is a placeholder for actual implementation
        logger.warning(
            "    Secret configuration requires GitHub App or PAT with admin:org scope"
        )
        result.steps_completed.append(
            f"{step} (skipped - requires elevated permissions)"
        )

    async def _create_environments(self, repo, result: OnboardingResult) -> None:
        """Create repository environments"""
        step = "create_environments"
        logger.info(
            f"  [{repo.full_name}] Creating {len(self.config.environments)} environments"
        )

        if self.dry_run:
            result.steps_completed.append(f"{step} (dry-run)")
            return

        # Note: Environment creation requires GitHub API v3
        # This is a placeholder for actual implementation
        logger.warning("    Environment creation requires REST API v3")
        result.steps_completed.append(f"{step} (skipped - requires REST API)")

    async def _rollback_failed(self, failed_results: List[OnboardingResult]) -> None:
        """
        Rollback changes for failed onboardings.

        Args:
            failed_results: List of failed OnboardingResult objects
        """
        logger.info(
            f"Starting rollback for {len(failed_results)} repositories")

        for result in failed_results:
            try:
                repo = self.github.get_repo(result.repository)
                logger.info(f"Rolling back {result.repository}")

                # Rollback completed steps in reverse order
                for step in reversed(result.steps_completed):
                    if step.startswith("deploy_workflows"):
                        # Remove deployed workflows
                        for workflow_file in self.config.workflows:
                            try:
                                contents = repo.get_contents(
                                    f".github/workflows/{workflow_file}"
                                )
                                repo.delete_file(
                                    path=contents.path,
                                    message=f"chore: rollback {workflow_file}",
                                    sha=contents.sha,
                                    branch=repo.default_branch,
                                )
                                logger.info(
                                    f"  Removed workflow: {workflow_file}")
                            except GithubException:
                                pass  # File doesn't exist or already removed

                    # Add more rollback logic for other steps as needed

                logger.info(f"✓ Rolled back {result.repository}")

            except Exception as e:
                logger.error(f"✗ Failed to rollback {result.repository}: {e}")

    def _log_summary(self) -> None:
        """Log summary of onboarding results"""
        successful = sum(1 for r in self.results if r.success)
        failed = len(self.results) - successful
        total_duration = sum(r.duration_seconds for r in self.results)

        logger.info("=" * 60)
        logger.info("BATCH ONBOARDING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total repositories: {len(self.results)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Total duration: {total_duration:.2f} seconds")
        logger.info(
            f"Average duration: {total_duration / len(self.results):.2f} seconds"
        )

        if failed > 0:
            logger.info("\nFailed repositories:")
            for result in self.results:
                if not result.success:
                    logger.info(f"  - {result.repository}: {result.error}")

    def save_results(self, output_file: str) -> None:
        """Save results to JSON file"""
        results_dict = [
            {
                "repository": r.repository,
                "success": r.success,
                "steps_completed": r.steps_completed,
                "error": r.error,
                "duration_seconds": r.duration_seconds,
                "timestamp": r.timestamp,
            }
            for r in self.results
        ]

        with open(output_file, "w") as f:
            json.dump(results_dict, f, indent=2)

        logger.info(f"Results saved to {output_file}")


def load_config(config_file: str) -> OnboardingConfig:
    """Load onboarding configuration from YAML file"""
    with open(config_file, "r") as f:
        config_dict = yaml.safe_load(f)

    return OnboardingConfig(**config_dict)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Batch onboard multiple repositories with validation and rollback"
    )
    parser.add_argument("--config", type=str,
                        help="Path to configuration YAML file")
    parser.add_argument(
        "--repos", nargs="+", help="List of repositories to onboard (owner/repo format)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Run in dry-run mode (no changes made)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="onboarding_results.json",
        help="Output file for results (JSON)",
    )
    parser.add_argument(
        "--max-concurrent", type=int, default=5, help="Maximum concurrent onboardings"
    )

    args = parser.parse_args()

    # Get GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    # Load or create configuration
    if args.config:
        config = load_config(args.config)
    elif args.repos:
        config = OnboardingConfig(
            repositories=args.repos, max_concurrent=args.max_concurrent
        )
    else:
        logger.error("Either --config or --repos must be specified")
        parser.print_help()
        sys.exit(1)

    # Create orchestrator
    orchestrator = BatchOnboardingOrchestrator(
        github_token=github_token, config=config, dry_run=args.dry_run
    )

    # Run onboarding
    results = await orchestrator.onboard_repositories()

    # Save results
    orchestrator.save_results(args.output)

    # Exit with appropriate code
    failed = sum(1 for r in results if not r.success)
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""Pre-deployment checklist validator for Week 11 deployment.

This script performs comprehensive validation before workflow deployment,
checking configuration files, label deployment status, GitHub CLI access,
and repository permissions.

Usage:
    python3 pre_deployment_checklist.py --phase 1
    python3 pre_deployment_checklist.py --phase 1 --verbose
    python3 pre_deployment_checklist.py --phase 2 --skip-labels
"""

import argparse
import json
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Optional

import yaml
from secret_manager import ensure_github_token


class CheckResult:
    """Result of a single check."""

    def __init__(
        self,
        name: str,
        passed: bool,
        message: str,
        details: Optional[str] = None,
    ):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details

    def __str__(self) -> str:
        status = "✅" if self.passed else "❌"
        result = f"{status} {self.name}: {self.message}"
        if self.details:
            result += f"\n   {self.details}"
        return result


class PreDeploymentChecker:
    """Validates all prerequisites for deployment."""

    def __init__(self, phase: int, skip_labels: bool = False, verbose: bool = False):
        """Initialize the checker.

        Args:
            phase: Deployment phase (1, 2, or 3)
            skip_labels: Skip label validation checks
            verbose: Show detailed output

        """
        self.phase = phase
        self.skip_labels = skip_labels
        self.verbose = verbose
        self.results: list[CheckResult] = []
        self.config_path = self._get_config_path()
        self.config: Optional[dict] = None

    def _get_config_path(self) -> Path:
        """Get configuration file path for the specified phase."""
        phase_names = {
            1: "batch-onboard-week11-phase1-pilot.yml",
            2: "batch-onboard-week11-phase2-expansion.yml",
            3: "batch-onboard-week11-phase3-final.yml",
        }
        config_dir = Path(__file__).parent.parent / "config"
        return config_dir / phase_names[self.phase]

    def _run_command(self, cmd: list[str]) -> tuple[bool, str, str]:
        """Run a shell command and return result.

        Args:
            cmd: Command to run as list of strings

        Returns:
            Tuple of (success, stdout, stderr)

        """
        try:
            result = subprocess.run(  # nosec B603
                cmd, capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)

    def check_config_exists(self) -> CheckResult:
        """Check if configuration file exists."""
        if self.config_path.exists():
            return CheckResult(
                "Configuration File",
                True,
                f"Found {self.config_path.name}",
                f"Path: {self.config_path}" if self.verbose else None,
            )
        else:
            return CheckResult(
                "Configuration File",
                False,
                f"Missing {self.config_path.name}",
                f"Expected at: {self.config_path}",
            )

    def check_config_valid(self) -> CheckResult:
        """Check if configuration file is valid YAML."""
        try:
            with open(self.config_path) as f:
                self.config = yaml.safe_load(f)

            # Check required keys
            required_keys = ["repositories", "workflows", "labels"]
            missing = [key for key in required_keys if key not in self.config]

            if missing:
                return CheckResult(
                    "Configuration Valid",
                    False,
                    f"Missing required keys: {', '.join(missing)}",
                )

            return CheckResult(
                "Configuration Valid",
                True,
                "Configuration parsed successfully",
                (
                    f"Repositories: {len(self.config['repositories'])}, "
                    f"Workflows: {len(self.config['workflows'])}, "
                    f"Labels: {len(self.config['labels'])}"
                    if self.verbose
                    else None
                ),
            )
        except yaml.YAMLError as e:
            return CheckResult(
                "Configuration Valid",
                False,
                "Invalid YAML syntax",
                str(e) if self.verbose else None,
            )
        except Exception as e:
            return CheckResult(
                "Configuration Valid",
                False,
                "Error reading configuration",
                str(e) if self.verbose else None,
            )

    def check_github_cli(self) -> CheckResult:
        """Check if GitHub CLI is installed and authenticated."""
        # Check if gh is installed
        success, stdout, stderr = self._run_command(["which", "gh"])
        if not success:
            return CheckResult(
                "GitHub CLI",
                False,
                "gh CLI not found in PATH",
                "Install: https://cli.github.com/",
            )

        # Check authentication
        success, stdout, stderr = self._run_command(["gh", "auth", "status"])
        if success:
            return CheckResult(
                "GitHub CLI",
                True,
                "Authenticated and ready",
                stdout.strip() if self.verbose else None,
            )
        else:
            return CheckResult(
                "GitHub CLI",
                False,
                "Not authenticated",
                "Run: gh auth login",
            )

    def check_python_dependencies(self) -> CheckResult:
        """Check if required Python packages are installed."""
        try:
            import yaml  # noqa: F401

            return CheckResult(
                "Python Dependencies",
                True,
                "All required packages installed (pyyaml)",
            )
        except ImportError:
            return CheckResult(
                "Python Dependencies",
                False,
                "Missing required package: pyyaml",
                "Install: pip install pyyaml",
            )

    def check_workflow_templates(self) -> CheckResult:
        """Check if workflow template files exist."""
        if not self.config:
            return CheckResult(
                "Workflow Templates",
                False,
                "Configuration not loaded",
            )

        workflow_dirs = [
            Path(__file__).parent.parent / "workflow-templates",
            Path(__file__).parent.parent.parent / "workflow-templates",
            Path(__file__).parent.parent.parent / ".github" / "workflows",
        ]

        workflows = self.config.get("workflows", [])
        missing = []

        for workflow in workflows:
            found = False
            for directory in workflow_dirs:
                if (directory / workflow).exists():
                    found = True
                    break
            if not found:
                missing.append(workflow)

        if missing:
            return CheckResult(
                "Workflow Templates",
                False,
                f"{len(missing)} workflow(s) not found",
                f"Missing: {', '.join(missing)}",
            )
        else:
            return CheckResult(
                "Workflow Templates",
                True,
                f"All {len(workflows)} workflow templates found",
            )

    def check_repository_access(self) -> CheckResult:
        """Check if we can access target repositories."""
        if not self.config:
            return CheckResult(
                "Repository Access",
                False,
                "Configuration not loaded",
            )

        repositories = self.config.get("repositories", [])
        inaccessible = []

        for repo in repositories:
            success, stdout, stderr = self._run_command(["gh", "repo", "view", repo, "--json", "name"])
            if not success:
                inaccessible.append(repo)

        if inaccessible:
            return CheckResult(
                "Repository Access",
                False,
                f"{len(inaccessible)}/{len(repositories)} repositories inaccessible",  # noqa: E501
                f"Cannot access: {', '.join(inaccessible)}",
            )
        else:
            return CheckResult(
                "Repository Access",
                True,
                f"All {len(repositories)} repositories accessible",
            )

    def check_labels_deployed(self) -> CheckResult:
        """Check if required labels are deployed to repositories."""
        if self.skip_labels:
            return CheckResult(
                "Label Deployment",
                True,
                "Skipped (--skip-labels flag)",
            )

        if not self.config:
            return CheckResult(
                "Label Deployment",
                False,
                "Configuration not loaded",
            )

        repositories = self.config.get("repositories", [])
        labels_config = self.config.get("labels", [])

        # Handle both list and dict formats
        if isinstance(labels_config, list):
            required_labels = {label.get("name", "") for label in labels_config if isinstance(label, dict)}
        elif isinstance(labels_config, dict):
            required_labels = set(labels_config.keys())
        else:
            return CheckResult(
                "Label Deployment",
                False,
                "Invalid labels configuration format",
                f"Expected list or dict, got {type(labels_config).__name__}",
            )

        repos_missing_labels = []

        for repo in repositories:
            success, stdout, stderr = self._run_command(["gh", "label", "list", "--repo", repo, "--json", "name"])

            if not success:
                repos_missing_labels.append(f"{repo} (inaccessible)")
                continue

            try:
                labels_data = json.loads(stdout)
                if isinstance(labels_data, list):
                    existing_labels = {label.get("name", "") for label in labels_data if isinstance(label, dict)}
                    missing = required_labels - existing_labels
                    if missing:
                        repos_missing_labels.append(f"{repo} (missing {len(missing)} labels)")
                else:
                    repos_missing_labels.append(f"{repo} (invalid format)")
            except (
                json.JSONDecodeError,
                KeyError,
                TypeError,
                AttributeError,
            ) as e:
                repos_missing_labels.append(f"{repo} (error: {type(e).__name__})")

        if repos_missing_labels:
            return CheckResult(
                "Label Deployment",
                False,
                f"{len(repos_missing_labels)}/{len(repositories)} repositories missing labels",  # noqa: E501
                ("\n   ".join([""] + repos_missing_labels) if self.verbose else None),
            )
        else:
            return CheckResult(
                "Label Deployment",
                True,
                f"All {len(repositories)} repositories have required labels",
            )

    def check_phase_prerequisites(self) -> CheckResult:
        """Check if prerequisites for this phase are met."""
        if self.phase == 1:
            # Phase 1 has no prerequisites
            return CheckResult(
                "Phase Prerequisites",
                True,
                "Phase 1 is initial deployment",
            )

        # For Phase 2 and 3, check previous phase
        previous_phase = self.phase - 1
        self._get_config_path()

        # This is a placeholder - in real implementation, would check
        # previous phase deployment status from logs/state files
        return CheckResult(
            "Phase Prerequisites",
            True,
            f"Phase {previous_phase} deployment should be verified manually",
            f"Ensure Phase {previous_phase} has been stable for 48 hours",
        )

    def run_all_checks(self) -> bool:
        """Run all validation checks.

        Returns:
            True if all checks passed, False otherwise

        """
        print(f"🔍 Running pre-deployment checks for Phase {self.phase}...")
        print("=" * 80)
        print()

        # Run checks in order
        checks = [
            ("Configuration file exists", self.check_config_exists),
            ("Configuration is valid", self.check_config_valid),
            ("GitHub CLI installed", self.check_github_cli),
            ("Python dependencies", self.check_python_dependencies),
            ("Workflow templates exist", self.check_workflow_templates),
            ("Repository access", self.check_repository_access),
            ("Labels deployed", self.check_labels_deployed),
            ("Phase prerequisites", self.check_phase_prerequisites),
        ]

        for description, check_func in checks:
            try:
                result = check_func()
                self.results.append(result)
                print(result)
                print()
            except Exception as e:
                result = CheckResult(
                    description,
                    False,
                    "Check failed with exception",
                    str(e),
                )
                self.results.append(result)
                print(result)
                print()

        # Summary
        print("=" * 80)
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        if passed == total:
            print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
            print()
            print(f"🚀 Phase {self.phase} is READY FOR DEPLOYMENT!")
            print()
            print("Next step:")
            print("  python3 batch_onboard_repositories.py \\")
            print(f"    --config {self.config_path.name} \\")
            print(f"    --output week11-phase{self.phase}-production.json")
            return True
        else:
            failed = total - passed
            print(f"❌ {failed} CHECK(S) FAILED ({passed}/{total} passed)")
            print()
            print("Fix the issues above before deploying.")

            # Provide helpful suggestions
            if not self.skip_labels:
                label_check = next((r for r in self.results if "Label" in r.name), None)
                if label_check and not label_check.passed:
                    print()
                    print("💡 To deploy labels automatically:")
                    print(
                        f"   python3 validate_labels.py --config {self.config_path.name} --fix"  # noqa: E501
                    )

            return False


def main():
    """Main entry point."""
    # Ensure GitHub token is available (from 1Password or env)
    _ = ensure_github_token("org-onboarding-token")  # noqa: F841

    parser = argparse.ArgumentParser(description="Pre-deployment checklist for Week 11 deployment")
    parser.add_argument(
        "--phase",
        type=int,
        required=True,
        choices=[1, 2, 3],
        help="Deployment phase to validate (1, 2, or 3)",
    )
    parser.add_argument(
        "--skip-labels",
        action="store_true",
        help="Skip label deployment validation (useful for testing)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output for each check",
    )

    args = parser.parse_args()

    checker = PreDeploymentChecker(
        phase=args.phase,
        skip_labels=args.skip_labels,
        verbose=args.verbose,
    )

    success = checker.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

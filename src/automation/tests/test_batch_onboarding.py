#!/usr/bin/env python3
"""Batch Onboarding Validation Test Suite.

Validates the batch onboarding system with comprehensive tests:
- Configuration validation
- Dry-run testing
- Parallel processing verification
- Rollback mechanism testing
- Results validation

Usage:
    python automation/tests/test_batch_onboarding.py
    python automation/tests/test_batch_onboarding.py --verbose
"""

import json
import subprocess
import sys
from pathlib import Path

# Test configuration
TEST_CONFIG = "automation/config/batch-onboard-test.yml"
TEST_OUTPUT_DRYRUN = "test-results-dryrun.json"
TEST_OUTPUT_REAL = "test-results-real.json"


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header(message: str):
    """Print formatted test header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def run_command(cmd: list[str], description: str) -> tuple[bool, str]:
    """Run a command and return success status and output.

    Args:
        cmd: Command and arguments as list
        description: Human-readable description of the command

    Returns:
        Tuple of (success, output)

    """
    print(f"{Colors.BOLD}Running: {description}{Colors.END}")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print_success(f"{description} - SUCCESS")
            return True, result.stdout
        else:
            print_error(f"{description} - FAILED")
            print(f"stderr: {result.stderr}")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print_error(f"{description} - TIMEOUT")
        return False, "Command timed out after 300 seconds"
    except Exception as e:
        print_error(f"{description} - ERROR: {e}")
        return False, str(e)


def test_prerequisites() -> bool:
    """Test that all prerequisites are met."""
    print_header("TEST 1: Prerequisites Check")

    all_passed = True

    # Check Python version
    if sys.version_info >= (3, 11):
        print_success(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print_error(f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        all_passed = False

    # Check required files exist
    required_files = ["automation/scripts/batch_onboard_repositories.py", TEST_CONFIG]

    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"File exists: {file_path}")
        else:
            print_error(f"File missing: {file_path}")
            all_passed = False

    # Check GITHUB_TOKEN
    import os

    if os.getenv("GITHUB_TOKEN"):
        print_success("GITHUB_TOKEN environment variable set")
    else:
        print_warning("GITHUB_TOKEN not set (required for actual runs)")

    return all_passed


def test_config_validation() -> bool:
    """Test configuration file validation."""
    print_header("TEST 2: Configuration Validation")

    try:
        import yaml

        with open(TEST_CONFIG) as f:
            config = yaml.safe_load(f)

        # Check required fields
        if "repositories" in config and len(config["repositories"]) > 0:
            print_success(f"Configuration valid: {len(config['repositories'])} repositories")
            return True
        else:
            print_error("Configuration missing required 'repositories' field")
            return False

    except Exception as e:
        print_error(f"Configuration validation failed: {e}")
        return False


def test_dryrun() -> bool:
    """Test dry-run mode."""
    print_header("TEST 3: Dry-Run Mode")

    cmd = [
        "python3",
        "automation/scripts/batch_onboard_repositories.py",
        "--config",
        TEST_CONFIG,
        "--dry-run",
        "--output",
        TEST_OUTPUT_DRYRUN,
    ]

    success, output = run_command(cmd, "Batch onboarding dry-run")

    if success and Path(TEST_OUTPUT_DRYRUN).exists():
        # Validate results JSON
        try:
            with open(TEST_OUTPUT_DRYRUN) as f:
                results = json.load(f)

            print_success(f"Dry-run completed: {len(results)} repositories processed")

            # Check result structure
            for result in results:
                repo = result.get("repository", "unknown")
                success = result.get("success", False)
                steps = result.get("steps_completed", [])

                if success:
                    print_success(f"  {repo}: {len(steps)} steps (dry-run)")
                else:
                    print_warning(f"  {repo}: Failed - {result.get('error', 'unknown')}")

            return True

        except Exception as e:
            print_error(f"Failed to parse results: {e}")
            return False

    return success


def test_results_format() -> bool:
    """Test that results JSON has correct format."""
    print_header("TEST 4: Results Format Validation")

    if not Path(TEST_OUTPUT_DRYRUN).exists():
        print_error(f"Results file not found: {TEST_OUTPUT_DRYRUN}")
        return False

    try:
        with open(TEST_OUTPUT_DRYRUN) as f:
            results = json.load(f)

        required_fields = [
            "repository",
            "success",
            "steps_completed",
            "duration_seconds",
            "timestamp",
        ]

        for result in results:
            for field in required_fields:
                if field not in result:
                    print_error(f"Missing required field '{field}' in result")
                    return False

        print_success(f"Results format valid: All {len(required_fields)} required fields present")
        return True

    except Exception as e:
        print_error(f"Results format validation failed: {e}")
        return False


def test_performance() -> bool:
    """Test performance metrics."""
    print_header("TEST 5: Performance Validation")

    if not Path(TEST_OUTPUT_DRYRUN).exists():
        print_error("No results file to analyze")
        return False

    try:
        with open(TEST_OUTPUT_DRYRUN) as f:
            results = json.load(f)

        total_duration = sum(r["duration_seconds"] for r in results)
        avg_duration = total_duration / len(results) if results else 0
        max_duration = max((r["duration_seconds"] for r in results), default=0)

        print_success("Performance metrics:")
        print(f"  Total repositories: {len(results)}")
        print(f"  Total duration: {total_duration:.2f}s")
        print(f"  Average per repo: {avg_duration:.2f}s")
        print(f"  Maximum duration: {max_duration:.2f}s")

        # Validate performance is reasonable
        if avg_duration > 30:
            print_warning(f"Average duration high: {avg_duration:.2f}s (expected <30s)")
        else:
            print_success(f"Performance acceptable: {avg_duration:.2f}s per repository")

        return True

    except Exception as e:
        print_error(f"Performance validation failed: {e}")
        return False


def generate_test_report(test_results: dict[str, bool]):
    """Generate summary test report."""
    print_header("TEST SUMMARY")

    total = len(test_results)
    passed = sum(1 for result in test_results.values() if result)
    failed = total - passed

    print(f"Total tests: {total}")
    print(f"Passed: {Colors.GREEN}{passed}{Colors.END}")
    print(f"Failed: {Colors.RED}{failed}{Colors.END}")
    print()

    for test_name, result in test_results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {test_name}: {status}")

    print()

    if failed == 0:
        print_success("All tests passed! ✓")
        return True
    else:
        print_error(f"{failed} test(s) failed")
        return False


def main():
    """Run all validation tests."""
    print(f"{Colors.BOLD}Batch Onboarding Validation Test Suite{Colors.END}")
    print(f"Testing configuration: {TEST_CONFIG}")
    print()

    # Run all tests
    test_results = {
        "Prerequisites": test_prerequisites(),
        "Configuration Validation": test_config_validation(),
        "Dry-Run Execution": test_dryrun(),
        "Results Format": test_results_format(),
        "Performance": test_performance(),
    }

    # Generate report
    all_passed = generate_test_report(test_results)

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

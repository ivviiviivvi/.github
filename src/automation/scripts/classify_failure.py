#!/usr/bin/env python3
"""Failure Classification Script.

Classifies workflow failures into categories for automated remediation.

Usage:
    python3 classify_failure.py --log <log_file>
    python3 classify_failure.py --analyze <workflow_run_id>
"""

import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any


class FailureType(Enum):
    """Types of workflow failures."""

    TRANSIENT = "transient"
    PERMANENT = "permanent"
    DEPENDENCY = "dependency"
    CONFIGURATION = "configuration"
    RESOURCE = "resource"
    UNKNOWN = "unknown"


@dataclass
class FailureClassification:
    """Classification result for a failure."""

    failure_type: FailureType
    confidence: float
    description: str
    recommended_action: str
    retry_eligible: bool


class FailureClassifier:
    """Classify workflow failures for automated remediation."""

    # Patterns for transient failures (can be retried)
    TRANSIENT_PATTERNS = [
        r"timeout",
        r"rate limit",
        r"connection reset",
        r"temporary failure",
        r"service unavailable",
        r"503",
        r"429",
        r"ETIMEDOUT",
        r"ECONNRESET",
    ]

    # Patterns for permanent failures (require manual intervention)
    PERMANENT_PATTERNS = [
        r"permission denied",
        r"not found",
        r"invalid token",
        r"authentication failed",
        r"syntax error",
        r"type error",
        r"404",
        r"401",
        r"403",
    ]

    # Patterns for dependency failures
    DEPENDENCY_PATTERNS = [
        r"npm ERR!",
        r"pip install.*failed",
        r"package not found",
        r"version conflict",
        r"dependency resolution",
        r"could not resolve",
        r"ModuleNotFoundError",
    ]

    def __init__(self):
        """Initialize the classifier."""
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns for efficiency."""
        self.transient_re = re.compile("|".join(self.TRANSIENT_PATTERNS), re.IGNORECASE)
        self.permanent_re = re.compile("|".join(self.PERMANENT_PATTERNS), re.IGNORECASE)
        self.dependency_re = re.compile(
            "|".join(self.DEPENDENCY_PATTERNS), re.IGNORECASE
        )

    def classify(self, log_content: str) -> FailureClassification:
        """Classify a failure based on log content.

        Args:
            log_content: The log output from a failed workflow

        Returns:
            FailureClassification with type and recommended action

        """
        # Check for dependency failures first (most specific)
        if self.dependency_re.search(log_content):
            return FailureClassification(
                failure_type=FailureType.DEPENDENCY,
                confidence=0.85,
                description="Dependency resolution or installation failure",
                recommended_action="Update dependencies and retry",
                retry_eligible=True,
            )

        # Check for transient failures
        if self.transient_re.search(log_content):
            return FailureClassification(
                failure_type=FailureType.TRANSIENT,
                confidence=0.90,
                description="Temporary infrastructure or network issue",
                recommended_action="Automatic retry recommended",
                retry_eligible=True,
            )

        # Check for permanent failures
        if self.permanent_re.search(log_content):
            return FailureClassification(
                failure_type=FailureType.PERMANENT,
                confidence=0.80,
                description="Configuration or permission issue",
                recommended_action="Manual investigation required",
                retry_eligible=False,
            )

        # Unknown failure type
        return FailureClassification(
            failure_type=FailureType.UNKNOWN,
            confidence=0.50,
            description="Unable to classify failure automatically",
            recommended_action="Manual review needed",
            retry_eligible=False,
        )

    def analyze_workflow_run(self, run_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze a workflow run and provide classification.

        Args:
            run_data: Workflow run data from GitHub API

        Returns:
            Analysis results with classification and recommendations

        """
        logs = run_data.get("logs", "")
        classification = self.classify(logs)

        return {
            "run_id": run_data.get("id"),
            "workflow": run_data.get("name"),
            "classification": {
                "type": classification.failure_type.value,
                "confidence": classification.confidence,
                "description": classification.description,
            },
            "recommendation": {
                "action": classification.recommended_action,
                "retry_eligible": classification.retry_eligible,
            },
        }


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Classify workflow failures")
    parser.add_argument("--log", type=str, help="Path to log file to analyze")
    parser.add_argument("--analyze", type=str, help="Workflow run ID to analyze")
    parser.add_argument("--stdin", action="store_true", help="Read log from stdin")

    args = parser.parse_args()

    classifier = FailureClassifier()

    if args.log:
        from pathlib import Path

        log_content = Path(args.log).read_text()
        result = classifier.classify(log_content)
        print(f"Failure Type: {result.failure_type.value}")
        print(f"Confidence: {result.confidence:.0%}")
        print(f"Description: {result.description}")
        print(f"Recommended Action: {result.recommended_action}")
        print(f"Retry Eligible: {result.retry_eligible}")
        return 0

    if args.stdin:
        log_content = sys.stdin.read()
        result = classifier.classify(log_content)
        print(f"{result.failure_type.value}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

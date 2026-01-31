#!/usr/bin/env python3
"""Unit tests for automation/scripts/classify_failure.py

Focus: Workflow failure classification for automated remediation.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from classify_failure import (
    FailureClassification,
    FailureClassifier,
    FailureType,
    main,
)


@pytest.mark.unit
class TestFailureType:
    """Test FailureType enum."""

    def test_has_transient_type(self):
        """Test has transient failure type."""
        assert FailureType.TRANSIENT.value == "transient"

    def test_has_permanent_type(self):
        """Test has permanent failure type."""
        assert FailureType.PERMANENT.value == "permanent"

    def test_has_dependency_type(self):
        """Test has dependency failure type."""
        assert FailureType.DEPENDENCY.value == "dependency"

    def test_has_configuration_type(self):
        """Test has configuration failure type."""
        assert FailureType.CONFIGURATION.value == "configuration"

    def test_has_resource_type(self):
        """Test has resource failure type."""
        assert FailureType.RESOURCE.value == "resource"

    def test_has_unknown_type(self):
        """Test has unknown failure type."""
        assert FailureType.UNKNOWN.value == "unknown"


@pytest.mark.unit
class TestFailureClassification:
    """Test FailureClassification dataclass."""

    def test_creates_classification(self):
        """Test creates classification with all fields."""
        classification = FailureClassification(
            failure_type=FailureType.TRANSIENT,
            confidence=0.90,
            description="Temporary failure",
            recommended_action="Retry",
            retry_eligible=True,
        )

        assert classification.failure_type == FailureType.TRANSIENT
        assert classification.confidence == 0.90
        assert classification.description == "Temporary failure"
        assert classification.recommended_action == "Retry"
        assert classification.retry_eligible is True


@pytest.mark.unit
class TestFailureClassifierInit:
    """Test FailureClassifier initialization."""

    def test_compiles_patterns(self):
        """Test compiles regex patterns."""
        classifier = FailureClassifier()

        assert classifier.transient_re is not None
        assert classifier.permanent_re is not None
        assert classifier.dependency_re is not None


@pytest.mark.unit
class TestClassifyTransient:
    """Test transient failure classification."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_classifies_timeout(self, classifier):
        """Test classifies timeout as transient."""
        result = classifier.classify("Error: Request timeout after 30s")

        assert result.failure_type == FailureType.TRANSIENT
        assert result.retry_eligible is True

    def test_classifies_rate_limit(self, classifier):
        """Test classifies rate limit as transient."""
        result = classifier.classify("Error: API rate limit exceeded")

        assert result.failure_type == FailureType.TRANSIENT

    def test_classifies_connection_reset(self, classifier):
        """Test classifies connection reset as transient."""
        result = classifier.classify("ECONNRESET: Connection reset by peer")

        assert result.failure_type == FailureType.TRANSIENT

    def test_classifies_503_error(self, classifier):
        """Test classifies 503 as transient."""
        result = classifier.classify("HTTP Error 503: Service unavailable")

        assert result.failure_type == FailureType.TRANSIENT

    def test_classifies_429_error(self, classifier):
        """Test classifies 429 as transient."""
        result = classifier.classify("HTTP 429 Too Many Requests")

        assert result.failure_type == FailureType.TRANSIENT

    def test_classifies_etimedout(self, classifier):
        """Test classifies ETIMEDOUT as transient."""
        result = classifier.classify("Error: connect ETIMEDOUT 1.2.3.4:443")

        assert result.failure_type == FailureType.TRANSIENT

    def test_transient_has_high_confidence(self, classifier):
        """Test transient classification has high confidence."""
        result = classifier.classify("Connection timeout")

        assert result.confidence >= 0.85


@pytest.mark.unit
class TestClassifyPermanent:
    """Test permanent failure classification."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_classifies_permission_denied(self, classifier):
        """Test classifies permission denied as permanent."""
        result = classifier.classify("Error: Permission denied accessing resource")

        assert result.failure_type == FailureType.PERMANENT
        assert result.retry_eligible is False

    def test_classifies_not_found(self, classifier):
        """Test classifies not found as permanent."""
        result = classifier.classify("Error: File not found: /path/to/file")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_invalid_token(self, classifier):
        """Test classifies invalid token as permanent."""
        result = classifier.classify("Authentication failed: Invalid token")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_401_error(self, classifier):
        """Test classifies 401 as permanent."""
        result = classifier.classify("HTTP 401 Unauthorized")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_403_error(self, classifier):
        """Test classifies 403 as permanent."""
        result = classifier.classify("HTTP 403 Forbidden")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_404_error(self, classifier):
        """Test classifies 404 as permanent."""
        result = classifier.classify("HTTP 404 Not Found")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_syntax_error(self, classifier):
        """Test classifies syntax error as permanent."""
        # Pattern is "syntax error" (with space)
        result = classifier.classify("Error: syntax error at line 10")

        assert result.failure_type == FailureType.PERMANENT

    def test_classifies_type_error(self, classifier):
        """Test classifies type error as permanent."""
        # Pattern is "type error" (with space)
        result = classifier.classify("Error: type error - cannot read property")

        assert result.failure_type == FailureType.PERMANENT


@pytest.mark.unit
class TestClassifyDependency:
    """Test dependency failure classification."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_classifies_npm_error(self, classifier):
        """Test classifies npm error as dependency."""
        result = classifier.classify("npm ERR! code ERESOLVE")

        assert result.failure_type == FailureType.DEPENDENCY
        assert result.retry_eligible is True

    def test_classifies_pip_error(self, classifier):
        """Test classifies pip install error as dependency."""
        result = classifier.classify("ERROR: pip install package failed")

        assert result.failure_type == FailureType.DEPENDENCY

    def test_classifies_package_not_found(self, classifier):
        """Test classifies package not found as dependency."""
        result = classifier.classify("Error: package not found in registry")

        assert result.failure_type == FailureType.DEPENDENCY

    def test_classifies_version_conflict(self, classifier):
        """Test classifies version conflict as dependency."""
        result = classifier.classify("Error: Version conflict between packages")

        assert result.failure_type == FailureType.DEPENDENCY

    def test_classifies_module_not_found(self, classifier):
        """Test classifies ModuleNotFoundError as dependency."""
        result = classifier.classify("ModuleNotFoundError: No module named 'package'")

        assert result.failure_type == FailureType.DEPENDENCY

    def test_classifies_could_not_resolve(self, classifier):
        """Test classifies could not resolve as dependency."""
        result = classifier.classify("Error: Could not resolve dependency tree")

        assert result.failure_type == FailureType.DEPENDENCY


@pytest.mark.unit
class TestClassifyUnknown:
    """Test unknown failure classification."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_classifies_unknown_error(self, classifier):
        """Test classifies unrecognized error as unknown."""
        result = classifier.classify("Some completely random error message")

        assert result.failure_type == FailureType.UNKNOWN
        assert result.retry_eligible is False

    def test_unknown_has_low_confidence(self, classifier):
        """Test unknown classification has lower confidence."""
        result = classifier.classify("Random error")

        assert result.confidence == 0.50

    def test_empty_log_returns_unknown(self, classifier):
        """Test empty log returns unknown."""
        result = classifier.classify("")

        assert result.failure_type == FailureType.UNKNOWN


@pytest.mark.unit
class TestClassifyPrecedence:
    """Test classification precedence."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_dependency_takes_precedence(self, classifier):
        """Test dependency failures checked before transient."""
        # Log contains both dependency and transient patterns
        result = classifier.classify("npm ERR! timeout connecting to registry")

        # Should classify as dependency since it's checked first
        assert result.failure_type == FailureType.DEPENDENCY


@pytest.mark.unit
class TestAnalyzeWorkflowRun:
    """Test analyze_workflow_run method."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_analyzes_workflow_run(self, classifier):
        """Test analyzes workflow run data."""
        run_data = {
            "id": 12345,
            "name": "CI Pipeline",
            "logs": "Error: Connection timeout",
        }

        result = classifier.analyze_workflow_run(run_data)

        assert result["run_id"] == 12345
        assert result["workflow"] == "CI Pipeline"
        assert result["classification"]["type"] == "transient"
        assert result["recommendation"]["retry_eligible"] is True

    def test_handles_missing_logs(self, classifier):
        """Test handles missing logs in run data."""
        run_data = {"id": 123, "name": "Test"}

        result = classifier.analyze_workflow_run(run_data)

        assert result["classification"]["type"] == "unknown"

    def test_includes_confidence(self, classifier):
        """Test includes confidence score."""
        run_data = {"logs": "npm ERR! install failed"}

        result = classifier.analyze_workflow_run(run_data)

        assert "confidence" in result["classification"]


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_with_log_file(self, tmp_path, monkeypatch, capsys):
        """Test main with --log argument."""
        log_file = tmp_path / "error.log"
        log_file.write_text("Connection timeout error")

        monkeypatch.setattr(
            sys, "argv", ["classify_failure.py", "--log", str(log_file)]
        )

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "transient" in captured.out
        assert "Retry Eligible: True" in captured.out

    def test_main_with_stdin(self, monkeypatch, capsys):
        """Test main with --stdin argument."""
        from io import StringIO

        monkeypatch.setattr(sys, "argv", ["classify_failure.py", "--stdin"])
        monkeypatch.setattr(sys, "stdin", StringIO("npm ERR!"))

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "dependency" in captured.out

    def test_main_no_args_shows_help(self, monkeypatch, capsys):
        """Test main without args shows help."""
        monkeypatch.setattr(sys, "argv", ["classify_failure.py"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "--log" in captured.out

    def test_main_shows_all_details(self, tmp_path, monkeypatch, capsys):
        """Test main shows all classification details."""
        log_file = tmp_path / "error.log"
        log_file.write_text("HTTP 401 Unauthorized")

        monkeypatch.setattr(
            sys, "argv", ["classify_failure.py", "--log", str(log_file)]
        )

        main()

        captured = capsys.readouterr()
        assert "Failure Type:" in captured.out
        assert "Confidence:" in captured.out
        assert "Description:" in captured.out
        assert "Recommended Action:" in captured.out


@pytest.mark.unit
class TestPatternMatching:
    """Test pattern matching behavior."""

    @pytest.fixture
    def classifier(self):
        return FailureClassifier()

    def test_case_insensitive_matching(self, classifier):
        """Test patterns match case-insensitively."""
        result1 = classifier.classify("TIMEOUT ERROR")
        result2 = classifier.classify("timeout error")
        result3 = classifier.classify("Timeout Error")

        assert result1.failure_type == FailureType.TRANSIENT
        assert result2.failure_type == FailureType.TRANSIENT
        assert result3.failure_type == FailureType.TRANSIENT

    def test_matches_within_larger_text(self, classifier):
        """Test patterns match within larger log text."""
        long_log = """
        Step 1/10: Building image...
        Step 2/10: Running tests...
        Error: Connection timeout while fetching dependencies
        Step failed.
        """

        result = classifier.classify(long_log)

        assert result.failure_type == FailureType.TRANSIENT

    def test_multiline_log_analysis(self, classifier):
        """Test analyzes multi-line logs correctly."""
        multiline_log = "Line 1\nLine 2\nnpm ERR! code ERESOLVE\nLine 4"

        result = classifier.classify(multiline_log)

        assert result.failure_type == FailureType.DEPENDENCY

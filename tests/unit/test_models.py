#!/usr/bin/env python3
"""Unit tests for automation/scripts/models.py
Focus: Pydantic models, validators, enums, field constraints.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from models import (  # Enums; Auto-merge models; Routing models; Self-healing models; Maintenance models; Analytics models; SLA models; Incident models; Validation models; Audit models
    AnalyticsConfig,
    AuditLogEntry,
    AutoMergeConfig,
    AutoMergeEligibility,
    AutoMergeSafetyChecks,
    AvailabilityMetric,
    FailureClassification,
    FailureType,
    FeatureImportance,
    Incident,
    IncidentConfig,
    IncidentSeverity,
    IncidentStatus,
    MaintenanceConfig,
    MaintenanceTask,
    MaintenanceWindow,
    MergeStrategy,
    Priority,
    ResolutionTimeMetric,
    ResponseTimeMetric,
    RiskLevel,
    RoutingConfig,
    RoutingDecision,
    RoutingFactorScores,
    RunbookStep,
    SelfHealingConfig,
    SelfHealingResult,
    SLAMetrics,
    SLAThresholds,
    SuccessRateMetric,
    ValidationResult,
    ValidationSuite,
    WorkflowPrediction,
)


class TestEnums:
    """Test enum definitions."""

    def test_risk_level_values(self):
        """Test RiskLevel enum has expected values."""
        assert RiskLevel.LOW == "LOW"
        assert RiskLevel.MEDIUM == "MEDIUM"
        assert RiskLevel.HIGH == "HIGH"
        assert RiskLevel.CRITICAL == "CRITICAL"

    def test_failure_type_values(self):
        """Test FailureType enum has expected values."""
        assert FailureType.TRANSIENT == "transient"
        assert FailureType.PERMANENT == "permanent"
        assert FailureType.DEPENDENCY == "dependency"

    def test_priority_values(self):
        """Test Priority enum has expected values."""
        assert Priority.P0 == "P0"
        assert Priority.P1 == "P1"
        assert Priority.P2 == "P2"
        assert Priority.P3 == "P3"

    def test_merge_strategy_values(self):
        """Test MergeStrategy enum has expected values."""
        assert MergeStrategy.MERGE == "merge"
        assert MergeStrategy.SQUASH == "squash"
        assert MergeStrategy.REBASE == "rebase"

    def test_incident_severity_values(self):
        """Test IncidentSeverity enum has expected values."""
        assert IncidentSeverity.SEV1 == "SEV-1"
        assert IncidentSeverity.SEV2 == "SEV-2"
        assert IncidentSeverity.SEV3 == "SEV-3"
        assert IncidentSeverity.SEV4 == "SEV-4"

    def test_incident_status_values(self):
        """Test IncidentStatus enum has expected values."""
        assert IncidentStatus.OPEN == "OPEN"
        assert IncidentStatus.ACKNOWLEDGED == "ACKNOWLEDGED"
        assert IncidentStatus.INVESTIGATING == "INVESTIGATING"
        assert IncidentStatus.IDENTIFIED == "IDENTIFIED"
        assert IncidentStatus.MITIGATING == "MITIGATING"
        assert IncidentStatus.RESOLVED == "RESOLVED"
        assert IncidentStatus.CLOSED == "CLOSED"


class TestAutoMergeModels:
    """Test auto-merge related models."""

    def test_safety_checks_all_required(self):
        """Test AutoMergeSafetyChecks requires all fields."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )
        assert checks.all_tests_passed is True
        assert checks.reviews_approved is True

    def test_safety_checks_missing_field_raises(self):
        """Test AutoMergeSafetyChecks raises on missing field."""
        with pytest.raises(ValidationError):
            AutoMergeSafetyChecks(
                all_tests_passed=True,
                reviews_approved=True,
                # Missing other required fields
            )

    def test_eligibility_confidence_bounds(self):
        """Test confidence must be between 0 and 1."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )

        # Valid confidence
        eligibility = AutoMergeEligibility(
            pr_number=123,
            repository="owner/repo",
            eligible=True,
            checks_passed=checks,
            confidence=0.95,
        )
        assert eligibility.confidence == 0.95

        # Invalid confidence > 1
        with pytest.raises(ValidationError):
            AutoMergeEligibility(
                pr_number=123,
                repository="owner/repo",
                eligible=True,
                checks_passed=checks,
                confidence=1.5,
            )

        # Invalid confidence < 0
        with pytest.raises(ValidationError):
            AutoMergeEligibility(
                pr_number=123,
                repository="owner/repo",
                eligible=True,
                checks_passed=checks,
                confidence=-0.1,
            )

    def test_eligibility_timestamp_default(self):
        """Test eligibility timestamp has default."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )
        eligibility = AutoMergeEligibility(
            pr_number=123,
            repository="owner/repo",
            eligible=True,
            checks_passed=checks,
            confidence=0.9,
        )
        assert eligibility.timestamp is not None
        assert isinstance(eligibility.timestamp, datetime)

    def test_config_defaults(self):
        """Test AutoMergeConfig has sensible defaults."""
        config = AutoMergeConfig()
        assert config.enabled is True
        assert config.min_reviews == 1
        assert config.coverage_threshold == 80.0
        assert config.merge_strategy == MergeStrategy.SQUASH
        assert config.delete_branch is True

    def test_config_coverage_validator(self):
        """Test coverage threshold validator."""
        # Valid coverage
        config = AutoMergeConfig(coverage_threshold=75.0)
        assert config.coverage_threshold == 75.0

        # Invalid coverage > 100
        with pytest.raises(ValidationError):
            AutoMergeConfig(coverage_threshold=150.0)


class TestRoutingModels:
    """Test routing related models."""

    def test_factor_scores_bounds(self):
        """Test factor scores must be 0-1."""
        scores = RoutingFactorScores(
            expertise=0.8,
            workload=0.6,
            response_time=0.7,
            availability=0.9,
            performance=0.5,
        )
        assert scores.expertise == 0.8

        # Invalid score > 1
        with pytest.raises(ValidationError):
            RoutingFactorScores(
                expertise=1.5,
                workload=0.6,
                response_time=0.7,
                availability=0.9,
                performance=0.5,
            )

    def test_routing_decision_structure(self):
        """Test RoutingDecision structure."""
        scores = RoutingFactorScores(
            expertise=0.8,
            workload=0.6,
            response_time=0.7,
            availability=0.9,
            performance=0.5,
        )
        decision = RoutingDecision(
            issue_number=42,
            repository="owner/repo",
            assignee="user1",
            score=0.75,
            scores=scores,
            confidence=0.85,
        )
        assert decision.issue_number == 42
        assert decision.assignee == "user1"
        assert decision.fallback_used is False

    def test_routing_config_weight_validation(self):
        """Test routing factors must sum to 1.0."""
        # Valid weights
        config = RoutingConfig(
            factors={
                "expertise": 0.35,
                "workload": 0.25,
                "response_time": 0.20,
                "availability": 0.15,
                "performance": 0.05,
            }
        )
        assert sum(config.factors.values()) == pytest.approx(1.0)

        # Invalid weights (sum != 1.0)
        with pytest.raises(ValidationError) as exc_info:
            RoutingConfig(
                factors={
                    "expertise": 0.5,
                    "workload": 0.5,
                    "response_time": 0.5,
                    "availability": 0.5,
                    "performance": 0.5,
                }
            )
        assert "must sum to 1.0" in str(exc_info.value)


class TestSelfHealingModels:
    """Test self-healing related models."""

    def test_failure_classification(self):
        """Test FailureClassification structure."""
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.TRANSIENT,
            confidence=0.9,
            reason="Network timeout",
            priority=Priority.P2,
        )
        assert classification.run_id == 12345
        assert classification.failure_type == FailureType.TRANSIENT

    def test_self_healing_result(self):
        """Test SelfHealingResult structure."""
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.TRANSIENT,
            confidence=0.9,
            reason="Network timeout",
            priority=Priority.P2,
        )
        result = SelfHealingResult(
            run_id=12345,
            repository="owner/repo",
            classification=classification,
            strategy="retry",
            healed=True,
            resolution="Retry succeeded",
            retry_count=2,
        )
        assert result.healed is True
        assert result.retry_count == 2

    def test_self_healing_config_bounds(self):
        """Test SelfHealingConfig field bounds."""
        config = SelfHealingConfig(max_retry_attempts=5)
        assert config.max_retry_attempts == 5

        # Invalid max_retry > 10
        with pytest.raises(ValidationError):
            SelfHealingConfig(max_retry_attempts=15)

        # Invalid max_retry < 1
        with pytest.raises(ValidationError):
            SelfHealingConfig(max_retry_attempts=0)


class TestMaintenanceModels:
    """Test maintenance related models."""

    def test_maintenance_task(self):
        """Test MaintenanceTask structure."""
        task = MaintenanceTask(
            task_type="dependency_update",
            description="Update npm packages",
            priority=Priority.P2,
            estimated_duration=30,
            risk_level=RiskLevel.LOW,
        )
        assert task.task_type == "dependency_update"
        assert task.estimated_duration == 30

    def test_maintenance_window(self):
        """Test MaintenanceWindow structure."""
        window = MaintenanceWindow(
            task_type="cleanup",
            scheduled_time=datetime.now(timezone.utc),
            duration_minutes=60,
            impact_score=0.2,
            confidence=0.85,
            reasoning="Low traffic period",
        )
        assert window.duration_minutes == 60
        assert window.impact_score == 0.2

    def test_maintenance_config_defaults(self):
        """Test MaintenanceConfig defaults."""
        config = MaintenanceConfig()
        assert config.enabled is True
        assert config.preferred_hours == [2, 3, 4]
        assert config.preferred_days == [6, 0]
        assert config.stale_branch_days == 30


class TestSLAModels:
    """Test SLA related models."""

    def test_response_time_metric(self):
        """Test ResponseTimeMetric structure."""
        metric = ResponseTimeMetric(
            target_minutes=15,
            actual_minutes=12.5,
            met=True,
            breach_count=0,
        )
        assert metric.met is True
        assert metric.actual_minutes < metric.target_minutes

    def test_sla_metrics_structure(self):
        """Test SLAMetrics structure."""
        metrics = SLAMetrics(
            repository="owner/repo",
            time_window="24h",
            overall_compliance=98.5,
            response_time=ResponseTimeMetric(
                target_minutes=15, actual_minutes=10, met=True
            ),
            resolution_time=ResolutionTimeMetric(
                target_hours=24, actual_hours=12, met=True
            ),
            success_rate=SuccessRateMetric(
                target_percentage=95.0, actual_percentage=98.0, met=True
            ),
            availability=AvailabilityMetric(
                target_percentage=99.0,
                actual_percentage=99.5,
                met=True,
                downtime_minutes=7.2,
            ),
            trend="improving",
        )
        assert metrics.overall_compliance == 98.5
        assert metrics.trend == "improving"

    def test_sla_thresholds_by_priority(self):
        """Test SLAThresholds with different priorities."""
        p0_threshold = SLAThresholds(
            priority=Priority.P0,
            response_time_minutes=5,
            resolution_time_hours=4,
            success_rate_percentage=99.0,
            availability_percentage=99.9,
        )
        p3_threshold = SLAThresholds(
            priority=Priority.P3,
            response_time_minutes=240,
            resolution_time_hours=168,
            success_rate_percentage=90.0,
            availability_percentage=95.0,
        )
        # P0 should have stricter thresholds
        assert p0_threshold.response_time_minutes < p3_threshold.response_time_minutes
        assert (
            p0_threshold.availability_percentage > p3_threshold.availability_percentage
        )


class TestIncidentModels:
    """Test incident response models."""

    def test_runbook_step(self):
        """Test RunbookStep structure."""
        step = RunbookStep(
            name="Notify team",
            action="notify",
            params={"channel": "alerts", "message": "Incident detected"},
        )
        assert step.executed is False
        assert step.executed_at is None

    def test_incident_structure(self):
        """Test Incident structure."""
        incident = Incident(
            incident_id="INC-001",
            title="Production API Down",
            description="API returning 500 errors",
            severity=IncidentSeverity.SEV1,
            status=IncidentStatus.OPEN,
            source="workflow",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc),
        )
        assert incident.severity == IncidentSeverity.SEV1
        assert incident.status == IncidentStatus.OPEN
        assert incident.acknowledged_at is None

    def test_incident_dict_serialization(self):
        """Test Incident dict() handles enums."""
        incident = Incident(
            incident_id="INC-001",
            title="Test",
            description="Test incident",
            severity=IncidentSeverity.SEV2,
            status=IncidentStatus.INVESTIGATING,
            source="manual",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc),
        )
        d = incident.dict()
        assert d["severity"] == "SEV-2"
        assert d["status"] == "INVESTIGATING"

    def test_incident_config_defaults(self):
        """Test IncidentConfig defaults."""
        config = IncidentConfig()
        assert config.enabled is True
        assert config.create_github_issues is True
        assert config.auto_execute_runbooks is True


class TestValidationModels:
    """Test validation framework models."""

    def test_validation_result(self):
        """Test ValidationResult structure."""
        result = ValidationResult(
            capability="auto-merge",
            started_at=datetime.now(timezone.utc),
            passed=True,
            message="All checks passed",
        )
        assert result.passed is True
        assert result.errors == []

    def test_validation_suite(self):
        """Test ValidationSuite structure."""
        suite = ValidationSuite(
            repository="owner/repo",
            started_at=datetime.now(timezone.utc),
        )
        assert suite.passed == 0
        assert suite.failed == 0
        assert suite.results == []


class TestAuditModels:
    """Test audit logging models."""

    def test_audit_log_entry(self):
        """Test AuditLogEntry structure."""
        entry = AuditLogEntry(
            action="pr_merged",
            actor="github-bot",
            repository="owner/repo",
            details={"pr_number": 123},
            success=True,
        )
        assert entry.action == "pr_merged"
        assert entry.success is True
        assert entry.timestamp is not None

    def test_audit_log_optional_fields(self):
        """Test AuditLogEntry optional security fields."""
        entry = AuditLogEntry(
            action="api_call",
            actor="user",
            repository="owner/repo",
            success=True,
            ip_address="192.168.1.1",
            user_agent="Python/3.11",
            token_preview="ghp_xxxx",
        )
        assert entry.ip_address == "192.168.1.1"
        assert entry.token_preview == "ghp_xxxx"


class TestAnalyticsModels:
    """Test analytics ML models."""

    def test_workflow_prediction(self):
        """Test WorkflowPrediction structure."""
        prediction = WorkflowPrediction(
            workflow_id="ci-pipeline",
            run_id="12345",
            hour_of_day=14,
            day_of_week=2,
            run_attempt=1,
            commit_size=150,
            file_count=10,
            author_success_rate=0.95,
            author_avg_duration=300.0,
            review_count=2,
            approval_time_minutes=60.0,
            test_coverage=85.0,
            new_tests=5,
            success_probability=0.92,
            estimated_duration=180,
            risk_level=RiskLevel.LOW,
            confidence=0.88,
            recommendation="Proceed with merge",
        )
        assert prediction.success_probability == 0.92
        assert prediction.risk_level == RiskLevel.LOW

    def test_analytics_config_defaults(self):
        """Test AnalyticsConfig defaults."""
        config = AnalyticsConfig()
        assert config.enabled is True
        assert config.default_model == "random_forest"
        assert config.min_confidence == 0.6
        assert config.min_accuracy == 0.85

    def test_feature_importance(self):
        """Test FeatureImportance structure."""
        importance = FeatureImportance(
            model_name="random_forest",
            features={
                "commit_size": 0.25,
                "test_coverage": 0.20,
                "author_success_rate": 0.15,
            },
            top_features=["commit_size", "test_coverage", "author_success_rate"],
        )
        assert importance.features["commit_size"] == 0.25
        assert len(importance.top_features) == 3


class TestDatetimeSerialization:
    """Test datetime serialization in models."""

    def test_eligibility_json_encoding(self):
        """Test AutoMergeEligibility JSON encoding."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )
        eligibility = AutoMergeEligibility(
            pr_number=123,
            repository="owner/repo",
            eligible=True,
            checks_passed=checks,
            confidence=0.95,
        )
        json_data = eligibility.json()
        assert "timestamp" in json_data
        assert "T" in json_data  # ISO format contains T

    def test_sla_metrics_json_encoding(self):
        """Test SLAMetrics JSON encoding."""
        metrics = SLAMetrics(
            repository="owner/repo",
            time_window="24h",
            overall_compliance=98.5,
            response_time=ResponseTimeMetric(
                target_minutes=15, actual_minutes=10, met=True
            ),
            resolution_time=ResolutionTimeMetric(
                target_hours=24, actual_hours=12, met=True
            ),
            success_rate=SuccessRateMetric(
                target_percentage=95.0, actual_percentage=98.0, met=True
            ),
            availability=AvailabilityMetric(
                target_percentage=99.0,
                actual_percentage=99.5,
                met=True,
                downtime_minutes=7.2,
            ),
            trend="stable",
        )
        json_data = metrics.json()
        assert "timestamp" in json_data

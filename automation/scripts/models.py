"""
Data models for Month 3 advanced automation features.

This module defines the core data structures used across all Month 3 components:  # noqa: E501
- Auto-merge configuration and results
- Routing scores and decisions
- Self-healing classifications
- Maintenance schedules
- Analytics predictions
- SLA metrics

All models use Pydantic for validation and serialization.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class RiskLevel(str, Enum):
    """Risk level classification for predictions."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FailureType(str, Enum):
    """Failure classification types."""

    TRANSIENT = "transient"
    PERMANENT = "permanent"
    DEPENDENCY = "dependency"


class Priority(str, Enum):
    """Priority levels for SLA tracking."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class MergeStrategy(str, Enum):
    """Git merge strategies."""

    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"


# =============================================================================
# Auto-Merge Models
# =============================================================================


class AutoMergeSafetyChecks(BaseModel):
    """Safety check results for auto-merge eligibility."""

    all_tests_passed: bool = Field(..., description="All CI tests passed successfully")
    reviews_approved: bool = Field(..., description="Required reviews approved")
    no_conflicts: bool = Field(..., description="No merge conflicts present")
    branch_up_to_date: bool = Field(..., description="Branch is up-to-date with base")
    coverage_threshold_met: bool = Field(
        ..., description="Code coverage meets minimum threshold"
    )


class AutoMergeEligibility(BaseModel):
    """Auto-merge eligibility check result."""

    pr_number: int = Field(..., description="Pull request number")
    repository: str = Field(..., description="Repository full name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    eligible: bool = Field(..., description="Whether PR is eligible for auto-merge")
    checks_passed: AutoMergeSafetyChecks
    reasons: List[str] = Field(
        default_factory=list, description="Reasons if not eligible"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class AutoMergeConfig(BaseModel):
    """Auto-merge configuration."""

    enabled: bool = True
    min_reviews: int = Field(default=1, ge=0)
    coverage_threshold: float = Field(default=80.0, ge=0.0, le=100.0)
    required_checks: List[str] = Field(default_factory=list)
    merge_strategy: MergeStrategy = MergeStrategy.SQUASH
    delete_branch: bool = True
    notify_on_merge: bool = True
    notify_on_failure: bool = True

    @validator("coverage_threshold")
    def validate_coverage(cls, v):
        """Validate coverage threshold is reasonable."""
        if v < 0 or v > 100:
            raise ValueError("Coverage threshold must be between 0 and 100")
        return v


# =============================================================================
# Intelligent Routing Models
# =============================================================================


class RoutingFactorScores(BaseModel):
    """Individual routing factor scores."""

    expertise: float = Field(..., ge=0.0, le=1.0, description="Expertise score")
    workload: float = Field(..., ge=0.0, le=1.0, description="Workload score")
    response_time: float = Field(..., ge=0.0, le=1.0, description="Response time score")
    availability: float = Field(..., ge=0.0, le=1.0, description="Availability score")
    performance: float = Field(..., ge=0.0, le=1.0, description="Performance score")


class RoutingDecision(BaseModel):
    """Intelligent routing decision result."""

    issue_number: int = Field(..., description="Issue number")
    repository: str = Field(..., description="Repository full name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    assignee: str = Field(..., description="Selected assignee username")
    score: float = Field(..., ge=0.0, le=1.0, description="Overall assignment score")
    scores: RoutingFactorScores = Field(..., description="Individual factor scores")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Decision confidence")
    fallback_used: bool = Field(
        default=False, description="Whether fallback was triggered"
    )
    alternatives: List[Dict[str, float]] = Field(
        default_factory=list, description="Alternative assignees and scores"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class RoutingConfig(BaseModel):
    """Intelligent routing configuration."""

    enabled: bool = True
    factors: Dict[str, float] = Field(
        default={
            "expertise": 0.35,
            "workload": 0.25,
            "response_time": 0.20,
            "availability": 0.15,
            "performance": 0.05,
        }
    )
    max_assignments_per_user: int = Field(default=10, ge=1)
    fallback_strategy: List[str] = Field(default=["round_robin", "random"])
    exempt_labels: List[str] = Field(default_factory=list)

    @validator("factors")
    def validate_weights(cls, v):
        """Validate routing weights sum to 1.0."""
        total = sum(v.values())
        if not (0.99 <= total <= 1.01):  # Allow small floating point error
            raise ValueError(f"Routing factor weights must sum to 1.0, got {total}")
        return v


# =============================================================================
# Self-Healing Models
# =============================================================================


class FailureClassification(BaseModel):
    """Failure classification result."""

    run_id: int = Field(..., description="Workflow run ID")
    workflow_name: str = Field(..., description="Workflow name")
    failure_type: FailureType = Field(..., description="Failure type")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Classification confidence"
    )
    reason: str = Field(..., description="Classification reason")
    priority: Priority = Field(..., description="Failure priority")
    failed_jobs: List[str] = Field(
        default_factory=list, description="List of failed job names"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class SelfHealingResult(BaseModel):
    """Self-healing attempt result."""

    run_id: int = Field(..., description="Workflow run ID")
    repository: str = Field(..., description="Repository full name")
    classification: FailureClassification
    strategy: str = Field(..., description="Healing strategy used")
    healed: bool = Field(..., description="Whether healing was successful")
    resolution: str = Field(..., description="Resolution description")
    retry_count: int = Field(..., ge=0, description="Number of retries")
    actions_taken: List[str] = Field(
        default_factory=list, description="List of actions taken"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class SelfHealingConfig(BaseModel):
    """Self-healing configuration."""

    enabled: bool = True
    enable_auto_retry: bool = True
    max_retry_attempts: int = Field(default=3, ge=1, le=10)
    initial_retry_delay: int = Field(
        default=60, ge=1, description="Initial retry delay in seconds"
    )
    retry_backoff_multiplier: float = Field(
        default=2.0, ge=1.0, description="Backoff multiplier"
    )
    max_consecutive_failures: int = Field(
        default=3, ge=1, description="Max failures before marking permanent"
    )
    dependency_wait_time: int = Field(
        default=300, ge=1, description="Wait time for dependencies in seconds"
    )
    create_issues_for_failures: bool = True
    send_notifications: bool = True


# =============================================================================
# Proactive Maintenance Models
# =============================================================================


class MaintenanceTask(BaseModel):
    """Individual maintenance task."""

    task_type: str = Field(..., description="Type of task")
    description: str = Field(..., description="Task description")
    priority: Priority = Field(..., description="Task priority")
    estimated_duration: int = Field(..., ge=1, description="Duration in minutes")
    risk_level: RiskLevel = Field(..., description="Risk level")
    details: Dict = Field(default_factory=dict, description="Additional details")


class MaintenanceWindow(BaseModel):
    """Predicted maintenance window."""

    task_type: str = Field(..., description="Type of maintenance task")
    scheduled_time: datetime = Field(..., description="Scheduled start time")
    duration_minutes: int = Field(..., ge=1, description="Estimated duration")
    impact_score: float = Field(
        ..., ge=0.0, le=1.0, description="Impact score (lower is better)"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")
    alternatives: List[Dict] = Field(
        default_factory=list, description="Alternative time windows"
    )
    reasoning: str = Field(..., description="Scheduling rationale")
    tasks: List[MaintenanceTask] = Field(
        default_factory=list, description="Tasks to perform"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class MaintenanceConfig(BaseModel):
    """Proactive maintenance configuration."""

    enabled: bool = True
    timing_predictor: str = Field(
        default="ml", description="Timing method: ml or fixed"
    )

    # Preferred windows
    preferred_hours: List[int] = Field(default=[2, 3, 4], description="2-4 AM")
    preferred_days: List[int] = Field(default=[6, 0], description="Saturday, Sunday")
    avoid_dates: List[str] = Field(default_factory=list)

    # Task configuration
    dependency_updates_enabled: bool = True
    dependency_updates_frequency: str = "weekly"
    dependency_auto_merge: bool = False

    cleanup_enabled: bool = True
    cleanup_frequency: str = "daily"
    stale_branch_days: int = 30
    old_artifacts_days: int = 90

    optimization_enabled: bool = True
    optimization_frequency: str = "monthly"

    # Notification
    notify_before_minutes: int = 30
    notify_after: bool = True


# =============================================================================
# Enhanced Analytics Models
# =============================================================================


class WorkflowPrediction(BaseModel):
    """Enhanced ML prediction for workflow outcome."""

    workflow_id: str = Field(..., description="Workflow identifier")
    run_id: str = Field(..., description="Workflow run ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Input features
    hour_of_day: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    run_attempt: int = Field(..., ge=1)
    commit_size: int = Field(..., ge=0, description="Lines changed")
    file_count: int = Field(..., ge=0)
    author_success_rate: float = Field(..., ge=0.0, le=1.0)
    author_avg_duration: float = Field(..., ge=0.0, description="Seconds")
    review_count: int = Field(..., ge=0)
    approval_time_minutes: float = Field(..., ge=0.0)
    test_coverage: float = Field(..., ge=0.0, le=100.0)
    new_tests: int = Field(..., ge=0)

    # Predictions
    success_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Predicted success probability"
    )
    estimated_duration: int = Field(
        ..., ge=0, description="Estimated duration in seconds"
    )
    risk_level: RiskLevel = Field(..., description="Risk classification")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence")
    factors: Dict[str, float] = Field(
        default_factory=dict, description="Feature importance scores"
    )
    recommendation: str = Field(..., description="Recommended action")

    # Actual outcome (for training)
    actual_success: Optional[bool] = None
    actual_duration: Optional[int] = None

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


# =============================================================================
# SLA Monitoring Models
# =============================================================================


class ResponseTimeMetric(BaseModel):
    """Response time SLA metric."""

    target_minutes: int = Field(..., ge=0)
    actual_minutes: float = Field(..., ge=0.0)
    met: bool
    breach_count: int = Field(default=0, ge=0)


class ResolutionTimeMetric(BaseModel):
    """Resolution time SLA metric."""

    target_hours: int = Field(..., ge=0)
    actual_hours: float = Field(..., ge=0.0)
    met: bool
    breach_count: int = Field(default=0, ge=0)


class SuccessRateMetric(BaseModel):
    """Success rate SLA metric."""

    target_percentage: float = Field(..., ge=0.0, le=100.0)
    actual_percentage: float = Field(..., ge=0.0, le=100.0)
    met: bool


class AvailabilityMetric(BaseModel):
    """Availability SLA metric."""

    target_percentage: float = Field(..., ge=0.0, le=100.0)
    actual_percentage: float = Field(..., ge=0.0, le=100.0)
    met: bool
    downtime_minutes: float = Field(..., ge=0.0)


class ItemMetrics(BaseModel):
    """Simple metrics for a single item type (issues, PRs, workflows)."""

    item_type: str = Field(..., description="Type of items (issues, prs, workflows)")
    total_items: int = Field(default=0, ge=0)
    within_sla: int = Field(default=0, ge=0)
    breached: int = Field(default=0, ge=0)
    avg_response_time_minutes: float = Field(default=0.0, ge=0.0)
    avg_resolution_time_hours: float = Field(default=0.0, ge=0.0)
    success_rate_percentage: float = Field(default=100.0, ge=0.0, le=100.0)
    breaches: List["SLABreach"] = Field(
        default_factory=list, description="SLA breaches"
    )


class SLAMetrics(BaseModel):
    """Complete SLA metrics for a repository."""

    repository: str = Field(..., description="Repository full name")
    time_window: str = Field(..., description="Time window (e.g., '24h', '7d')")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    overall_compliance: float = Field(
        ..., ge=0.0, le=100.0, description="Overall compliance percentage"
    )

    response_time: ResponseTimeMetric
    resolution_time: ResolutionTimeMetric
    success_rate: SuccessRateMetric
    availability: AvailabilityMetric

    breaches: List[Dict] = Field(default_factory=list, description="SLA breach details")
    trend: str = Field(..., description="improving, stable, or degrading")

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class SLAThresholds(BaseModel):
    """SLA thresholds by priority level."""

    priority: Priority
    response_time_minutes: int = Field(..., ge=0)
    resolution_time_hours: int = Field(..., ge=0)
    success_rate_percentage: float = Field(..., ge=0.0, le=100.0)
    availability_percentage: float = Field(..., ge=0.0, le=100.0)

    class Config:
        """Example SLA thresholds."""

        schema_extra = {
            "examples": [
                {
                    "priority": "P0",
                    "response_time_minutes": 5,
                    "resolution_time_hours": 4,
                    "success_rate_percentage": 99.0,
                    "availability_percentage": 99.9,
                },
                {
                    "priority": "P1",
                    "response_time_minutes": 30,
                    "resolution_time_hours": 24,
                    "success_rate_percentage": 95.0,
                    "availability_percentage": 99.0,
                },
            ]
        }


# =============================================================================
# Audit Logging Models
# =============================================================================


class AuditLogEntry(BaseModel):
    """Audit log entry for security tracking."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str = Field(..., description="Action performed")
    actor: str = Field(..., description="Actor (user or bot)")
    repository: str = Field(..., description="Repository affected")
    details: Dict = Field(default_factory=dict, description="Action details")
    success: bool = Field(..., description="Whether action succeeded")

    # Security context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    token_preview: Optional[str] = Field(
        None, description="First 8 chars of token used"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


# =============================================================================
# Enhanced Analytics Models
# =============================================================================


class AnalyticsConfig(BaseModel):
    """Configuration for enhanced analytics ML model."""

    enabled: bool = True
    default_model: str = "random_forest"
    min_confidence: float = Field(0.6, ge=0.0, le=1.0)
    min_accuracy: float = Field(0.85, ge=0.0, le=1.0)
    training_lookback_days: int = Field(90, ge=1)
    retrain_schedule: str = "weekly"

    class Config:
        """Example analytics config."""

        schema_extra = {
            "example": {
                "enabled": True,
                "default_model": "random_forest",
                "min_confidence": 0.6,
                "min_accuracy": 0.85,
                "training_lookback_days": 90,
                "retrain_schedule": "weekly",
            }
        }


class AnalyticsPrediction(BaseModel):
    """Prediction result from ML model."""

    pr_number: int
    prediction: str = Field(..., description="Prediction outcome (merge/close)")
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_name: str
    features: Dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class FeatureImportance(BaseModel):
    """Feature importance analysis from ML model."""

    model_name: str
    features: Dict[str, float] = Field(..., description="Feature scores")
    top_features: List[str] = Field(default_factory=list, description="Top N features")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


# =============================================================================
# SLA Monitoring Models
# =============================================================================


class SLAConfig(BaseModel):
    """Configuration for SLA monitoring."""

    enabled: bool = True
    check_interval_minutes: int = Field(15, ge=1)
    thresholds: List["SLAThresholds"] = Field(default_factory=list)

    class Config:
        """Example SLA config."""

        schema_extra = {
            "example": {
                "enabled": True,
                "check_interval_minutes": 15,
                "thresholds": [],
            }
        }


class SLABreach(BaseModel):
    """Record of an SLA breach."""

    item_type: str = Field(..., description="Type of item (issue/pr/workflow)")
    item_number: int = Field(..., description="Item number")
    priority: Priority
    breach_type: str = Field(..., description="Type of breach")
    threshold_value: float = Field(..., description="SLA threshold")
    actual_value: float = Field(..., description="Actual value")
    breach_time: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False
    resolution_time: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class SLAReport(BaseModel):
    """Comprehensive SLA report."""

    repository: str
    period_start: datetime
    period_end: datetime
    metrics: Dict[str, SLAMetrics] = Field(default_factory=dict)
    total_breaches: int = 0
    compliance_percentage: float = 100.0
    trends: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


# ==================== Incident Response Models ====================


class IncidentSeverity(str, Enum):
    """Incident severity levels."""

    SEV1 = "SEV-1"  # Critical - Production down, data loss, security breach
    SEV2 = "SEV-2"  # High - Major feature broken, significant impact
    SEV3 = "SEV-3"  # Medium - Minor feature broken, workaround available
    SEV4 = "SEV-4"  # Low - Cosmetic issues, no user impact


class IncidentStatus(str, Enum):
    """Incident lifecycle status."""

    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    IDENTIFIED = "IDENTIFIED"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class RunbookStep(BaseModel):
    """Automated runbook step."""

    name: str
    action: str  # notify, create_issue, escalate, run_workflow, update_status
    params: Dict[str, Any] = Field(default_factory=dict)
    executed: bool = False
    executed_at: Optional[datetime] = None
    error: Optional[str] = None


class Incident(BaseModel):
    """Incident record."""

    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    source: str  # workflow, sla_breach, manual
    repository: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    time_to_resolution_minutes: Optional[float] = None
    runbook_steps: List[RunbookStep] = Field(default_factory=list)
    github_issue_number: Optional[int] = None

    def dict(self, **kwargs):
        """Override dict to handle enums properly."""
        d = super().dict(**kwargs)
        d["severity"] = self.severity.value
        d["status"] = self.status.value
        return d


class IncidentConfig(BaseModel):
    """Incident response configuration."""

    enabled: bool = True
    create_github_issues: bool = True
    auto_execute_runbooks: bool = True
    severity_keywords: Dict[str, List[str]] = Field(default_factory=dict)
    escalation_rules: Dict[str, Dict] = Field(default_factory=dict)
    notification_channels: Dict[str, List[str]] = Field(default_factory=dict)


class PostIncidentReport(BaseModel):
    """Post-incident analysis report."""

    incident_id: str
    incident: Incident
    timeline: List[Dict[str, str]]
    root_cause: str
    lessons_learned: List[str]
    action_items: List[Dict[str, str]]
    generated_at: datetime

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


# ==================== Validation Models ====================


class ValidationResult(BaseModel):
    """Result of a capability validation."""

    capability: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    passed: bool = False
    message: str = ""
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)


class ValidationSuite(BaseModel):
    """Complete validation suite results."""

    repository: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    results: List[ValidationResult] = Field(default_factory=list)
    passed: int = 0
    failed: int = 0
    warnings: int = 0

    def dict(self, **kwargs):
        """Override dict to handle datetime serialization."""
        d = super().dict(**kwargs)
        return d

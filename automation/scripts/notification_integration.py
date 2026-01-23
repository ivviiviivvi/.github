#!/usr/bin/env python3
"""
Notification Integration Helper

Provides backward-compatible notification wrapper that integrates existing
Week 9 systems with the unified notification manager.

This module replaces the old utils.send_notification() function with calls
to the unified NotificationManager while maintaining the same API.

Usage in existing scripts:
    # Old code (still works):
    from utils import send_notification
    send_notification("slack", "My message")

    # New code (preferred):
    from notification_integration import notify_sla_breach, notify_incident
    notify_sla_breach(issue_number="123", priority="P0", ...)
"""

from typing import Dict, List, Optional

from notification_manager import Notification, NotificationManager, Priority

# Initialize global notification manager
_notification_manager = None


def get_notification_manager() -> NotificationManager:
    """Get or create global notification manager instance."""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager


# =============================================================================
# Backward Compatibility
# =============================================================================


def send_notification(channel: str, message: str, **kwargs):
    """
    Legacy notification function for backward compatibility.

    This function is deprecated but maintained for compatibility with
    existing code. New code should use the specific notify_* functions.

    Args:
        channel: Channel name (slack, email, pagerduty)
        message: Message text
        **kwargs: Additional parameters (title, priority, source, etc.)
    """
    manager = get_notification_manager()

    # Extract parameters
    title = kwargs.get("title", "Notification")
    priority_str = kwargs.get("priority", "MEDIUM")
    source = kwargs.get("source", "automation")
    metadata = kwargs.get("metadata", {})

    # Map priority string to enum
    priority_map = {
        "CRITICAL": Priority.CRITICAL,
        "HIGH": Priority.HIGH,
        "MEDIUM": Priority.MEDIUM,
        "LOW": Priority.LOW,
        "INFO": Priority.INFO,
    }
    priority = priority_map.get(priority_str.upper(), Priority.MEDIUM)

    # Create notification
    notification = Notification(
        title=title,
        message=message,
        priority=priority,
        source=source,
        channels=[channel] if channel else [],
        metadata=metadata,
    )

    # Send
    manager.send(notification)


# =============================================================================
# SLA Monitor Integrations
# =============================================================================


def notify_sla_breach(
    item_type: str,
    item_number: str,
    repository: str,
    breach_type: str,
    threshold: str,
    actual: str,
    priority: str,
    metadata: Optional[Dict] = None,
):
    """
    Notify about SLA breach.

    Args:
        item_type: Type of item (issue, pr, workflow)
        item_number: Item number/ID
        repository: Repository name (owner/repo)
        breach_type: Type of breach (response_time, resolution_time, etc.)
        threshold: Threshold value
        actual: Actual value
        priority: Priority level (P0, P1, P2, P3)
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    # Map priority to notification priority
    priority_map = {
        "P0": Priority.CRITICAL,
        "P1": Priority.HIGH,
        "P2": Priority.MEDIUM,
        "P3": Priority.LOW,
    }
    notif_priority = priority_map.get(priority, Priority.MEDIUM)

    # Build message
    message = """**Item:** {item_type} #{item_number}
**Repository:** {repository}
**Breach Type:** {breach_type}
**Threshold:** {threshold}
**Actual:** {actual}
**Priority:** {priority}

Action required to maintain SLA compliance."""

    # Create notification
    notification = Notification(
        title=f"SLA Breach Detected - {priority}",
        message=message,
        priority=notif_priority,
        source="sla-monitor",
        metadata={
            "item_type": item_type,
            "item_number": item_number,
            "repository": repository,
            "breach_type": breach_type,
            "threshold": threshold,
            "actual": actual,
            "priority": priority,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


def notify_sla_compliance(
    repository: str,
    compliance_rate: float,
    period_days: int,
    metadata: Optional[Dict] = None,
):
    """
    Notify about SLA compliance status.

    Args:
        repository: Repository name
        compliance_rate: Compliance rate (0.0 to 1.0)
        period_days: Reporting period in days
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    # Determine priority based on compliance rate
    if compliance_rate < 0.90:
        priority = Priority.HIGH
    elif compliance_rate < 0.95:
        priority = Priority.MEDIUM
    else:
        priority = Priority.LOW

    # Build message
    message = """**Repository:** {repository}
**Compliance Rate:** {compliance_rate:.1%}
**Period:** {period_days} days

{"⚠️ Compliance below target (95%)" if compliance_rate < 0.95 else "✅ SLA compliance maintained"}"""  # noqa: E501

    # Create notification
    notification = Notification(
        title=f"SLA Compliance Report - {compliance_rate:.1%}",
        message=message,
        priority=priority,
        source="sla-monitor",
        metadata={
            "repository": repository,
            "compliance_rate": compliance_rate,
            "period_days": period_days,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Incident Response Integrations
# =============================================================================


def notify_incident_created(
    incident_id: str,
    severity: str,
    repository: str,
    description: str,
    status: str = "OPEN",
    metadata: Optional[Dict] = None,
):
    """
    Notify about new incident.

    Args:
        incident_id: Incident ID (e.g., INC-001)
        severity: Severity level (SEV-1, SEV-2, SEV-3, SEV-4)
        repository: Repository name
        description: Incident description
        status: Incident status
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    # Map severity to priority
    priority_map = {
        "SEV-1": Priority.CRITICAL,
        "SEV-2": Priority.HIGH,
        "SEV-3": Priority.MEDIUM,
        "SEV-4": Priority.LOW,
    }
    priority = priority_map.get(severity, Priority.MEDIUM)

    # Build message
    message = """**Incident ID:** {incident_id}
**Severity:** {severity}
**Repository:** {repository}

{description}

**Status:** {status}
**Created:** {metadata.get('created_at', 'now') if metadata else 'now'}"""

    # Create notification
    notification = Notification(
        title=f"New Incident - {severity}",
        message=message,
        priority=priority,
        source="incident-response",
        metadata={
            "incident_id": incident_id,
            "severity": severity,
            "repository": repository,
            "status": status,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


def notify_incident_resolved(
    incident_id: str,
    severity: str,
    duration_minutes: int,
    metadata: Optional[Dict] = None,
):
    """
    Notify about resolved incident.

    Args:
        incident_id: Incident ID
        severity: Severity level
        duration_minutes: Incident duration
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    # Build message
    hours = duration_minutes // 60
    mins = duration_minutes % 60
    f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    message = """**Incident ID:** {incident_id}
**Severity:** {severity}
**Duration:** {duration_str}

Incident has been resolved."""

    # Create notification
    notification = Notification(
        title=f"Incident Resolved - {incident_id}",
        message=message,
        priority=Priority.LOW,
        source="incident-response",
        metadata={
            "incident_id": incident_id,
            "severity": severity,
            "duration_minutes": duration_minutes,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Validation Framework Integrations
# =============================================================================


def notify_validation_failure(
    capability: str,
    repository: str,
    errors: List[str],
    warnings: List[str] = None,
    metadata: Optional[Dict] = None,
):
    """
    Notify about validation failure.

    Args:
        capability: Capability that failed validation
        repository: Repository name
        errors: List of error messages
        warnings: List of warning messages
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    # Build error message
    _error_text = "\n".join(f"- {e}" for e in errors)  # noqa: F841
    _warning_text = (  # noqa: F841
        "\n\n**Warnings:**\n" + "\n".join(f"- {w}" for w in warnings)
        if warnings
        else ""
    )

    message = """**Capability:** {capability}
**Repository:** {repository}

**Errors:**
{error_text}{warning_text}

Please investigate and remediate."""

    # Create notification
    notification = Notification(
        title=f"Validation Failed - {capability}",
        message=message,
        priority=Priority.MEDIUM,
        source="validation-framework",
        metadata={
            "capability": capability,
            "repository": repository,
            "error_count": len(errors),
            "warning_count": len(warnings) if warnings else 0,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


def notify_validation_success(
    repository: str,
    passed_count: int,
    total_count: int,
    metadata: Optional[Dict] = None,
):
    """
    Notify about successful validation run.

    Args:
        repository: Repository name
        passed_count: Number of passed validations
        total_count: Total number of validations
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**Repository:** {repository}
**Passed:** {passed_count}/{total_count} capabilities

All validations completed successfully."""

    # Create notification
    notification = Notification(
        title=f"Validation Complete - {passed_count}/{total_count} passed",
        message=message,
        priority=Priority.LOW,
        source="validation-framework",
        metadata={
            "repository": repository,
            "passed_count": passed_count,
            "total_count": total_count,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Self-Healing Integrations
# =============================================================================


def notify_self_healing_success(
    workflow_name: str,
    run_id: int,
    failure_type: str,
    action_taken: str,
    metadata: Optional[Dict] = None,
):
    """
    Notify about successful self-healing.

    Args:
        workflow_name: Workflow name
        run_id: Run ID
        failure_type: Type of failure
        action_taken: Action taken to heal
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**Workflow:** {workflow_name}
**Run ID:** {run_id}
**Failure Type:** {failure_type}
**Action Taken:** {action_taken}

Workflow failure automatically resolved."""

    # Create notification
    notification = Notification(
        title=f"Self-Healing Success - {workflow_name}",
        message=message,
        priority=Priority.LOW,
        source="self-healing",
        metadata={
            "workflow_name": workflow_name,
            "run_id": run_id,
            "failure_type": failure_type,
            "action_taken": action_taken,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


def notify_self_healing_failure(
    workflow_name: str,
    run_id: int,
    failure_type: str,
    attempts: int,
    metadata: Optional[Dict] = None,
):
    """
    Notify about self-healing failure.

    Args:
        workflow_name: Workflow name
        run_id: Run ID
        failure_type: Type of failure
        attempts: Number of attempts made
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**Workflow:** {workflow_name}
**Run ID:** {run_id}
**Failure Type:** {failure_type}
**Attempts:** {attempts}

Manual intervention may be required."""

    # Create notification
    notification = Notification(
        title=f"Self-Healing Failed - {workflow_name}",
        message=message,
        priority=Priority.HIGH,
        source="self-healing",
        metadata={
            "workflow_name": workflow_name,
            "run_id": run_id,
            "failure_type": failure_type,
            "attempts": attempts,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Maintenance Integrations
# =============================================================================


def notify_maintenance_scheduled(
    task_name: str,
    start_time: str,
    end_time: str,
    duration_minutes: int,
    impact: str,
    metadata: Optional[Dict] = None,
):
    """
    Notify about scheduled maintenance.

    Args:
        task_name: Task name
        start_time: Start time (ISO format)
        end_time: End time (ISO format)
        duration_minutes: Duration in minutes
        impact: Impact description
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**Task:** {task_name}
**Window:** {start_time} - {end_time}
**Duration:** {duration_minutes} minutes
**Impact:** {impact}

Maintenance will be performed automatically."""

    # Create notification
    notification = Notification(
        title=f"Maintenance Scheduled - {task_name}",
        message=message,
        priority=Priority.MEDIUM,
        source="maintenance-scheduler",
        metadata={
            "task_name": task_name,
            "start_time": start_time,
            "end_time": end_time,
            "duration_minutes": duration_minutes,
            "impact": impact,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


def notify_maintenance_complete(
    task_name: str,
    duration_minutes: int,
    success: bool,
    metadata: Optional[Dict] = None,
):
    """
    Notify about completed maintenance.

    Args:
        task_name: Task name
        duration_minutes: Actual duration
        success: Whether maintenance succeeded
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    "✅ Completed successfully" if success else "❌ Failed"
    priority = Priority.LOW if success else Priority.HIGH

    message = """**Task:** {task_name}
**Duration:** {duration_minutes} minutes
**Status:** {status}"""

    # Create notification
    notification = Notification(
        title=f"Maintenance Complete - {task_name}",
        message=message,
        priority=priority,
        source="maintenance-scheduler",
        metadata={
            "task_name": task_name,
            "duration_minutes": duration_minutes,
            "success": success,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Analytics Integrations
# =============================================================================


def notify_model_accuracy_low(
    model_name: str,
    accuracy: float,
    threshold: float,
    metadata: Optional[Dict] = None,
):
    """
    Notify about low model accuracy.

    Args:
        model_name: Model name
        accuracy: Current accuracy
        threshold: Threshold accuracy
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**Model:** {model_name}
**Accuracy:** {accuracy:.1%}
**Threshold:** {threshold:.1%}

Model accuracy has dropped below acceptable threshold. Retraining may be required."""  # noqa: E501

    # Create notification
    notification = Notification(
        title=f"Model Accuracy Alert - {model_name}",
        message=message,
        priority=Priority.MEDIUM,
        source="analytics",
        metadata={
            "model_name": model_name,
            "accuracy": accuracy,
            "threshold": threshold,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)


# =============================================================================
# Auto-Merge Integrations
# =============================================================================


def notify_auto_merge_failure(
    pr_number: int,
    repository: str,
    reason: str,
    metadata: Optional[Dict] = None,
):
    """
    Notify about auto-merge failure.

    Args:
        pr_number: PR number
        repository: Repository name
        reason: Failure reason
        metadata: Additional metadata
    """
    manager = get_notification_manager()

    message = """**PR:** #{pr_number}
**Repository:** {repository}
**Reason:** {reason}

Auto-merge failed. Manual review may be required."""

    # Create notification
    notification = Notification(
        title=f"Auto-Merge Failed - PR #{pr_number}",
        message=message,
        priority=Priority.MEDIUM,
        source="auto-merge",
        metadata={
            "pr_number": pr_number,
            "repository": repository,
            "reason": reason,
            **(metadata or {}),
        },
    )

    # Send
    manager.send(notification)

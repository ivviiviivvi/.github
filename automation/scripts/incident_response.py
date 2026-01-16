#!/usr/bin/env python3
"""
Incident Response Automation

Provides automated incident response with severity classification, runbook
execution, escalation workflows, and post-incident analysis.

Features:
- Automatic incident detection and creation
- Severity classification (SEV-1 through SEV-4)
- Automated runbook execution
- Escalation workflows based on severity
- Real-time status tracking
- Post-incident reporting
- Integration with SLA monitoring

Usage:
    # Create incident from workflow failure
    python incident_response.py --owner ORG --repo REPO --create --run-id 12345

    # Execute runbook for incident
    python incident_response.py --incident-id INC-001 --execute-runbook

    # Update incident status
    python incident_response.py --incident-id INC-001 --update-status resolved

    # Generate post-incident report
    python incident_response.py --incident-id INC-001 --report
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from models import (
    Incident,
    IncidentConfig,
    IncidentSeverity,
    IncidentStatus,
    PostIncidentReport,
    RunbookStep,
)
from notification_integration import notify_incident_created
from utils import GitHubAPIClient, load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class IncidentResponseEngine:
    """Automate incident response and management."""

    def __init__(self, config: IncidentConfig, github_client: GitHubAPIClient):
        """
        Initialize incident response engine.

        Args:
            config: Incident response configuration
            github_client: GitHub API client
        """
        self.config = config
        self.github = github_client
        self.incidents_dir = Path(".github/incidents")
        self.runbooks_dir = Path(".github/runbooks")
        self.incidents_dir.mkdir(parents=True, exist_ok=True)
        self.runbooks_dir.mkdir(parents=True, exist_ok=True)

    def create_incident(
        self,
        owner: str,
        repo: str,
        title: str,
        description: str,
        source: str = "manual",
    ) -> Incident:
        """
        Create a new incident.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Incident title
            description: Incident description
            source: Source of incident (workflow, sla_breach, manual)

        Returns:
            Created incident
        """
        logger.info(f"Creating incident: {title}")

        # Generate incident ID
        incident_id = self._generate_incident_id()

        # Classify severity
        severity = self._classify_severity(title, description, source)

        # Create incident
        incident = Incident(
            incident_id=incident_id,
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.OPEN,
            source=source,
            repository=f"{owner}/{repo}",
            created_at=datetime.now(timezone.utc),
        )

        # Save incident
        self._save_incident(incident)

        # Send notifications
        self._send_incident_notification(incident, "created")

        # Create GitHub issue
        if self.config.create_github_issues:
            issue = self._create_github_issue(owner, repo, incident)
            incident.github_issue_number = issue.get("number")
            self._save_incident(incident)

        # Execute automatic runbook if configured
        if self.config.auto_execute_runbooks:
            self._execute_runbook(incident)

        logger.info(f"Incident {incident_id} created with severity {severity.value}")
        return incident

    def _classify_severity(
        self, title: str, description: str, source: str
    ) -> IncidentSeverity:
        """
        Classify incident severity based on content and source.

        SEV-1: Critical - Production down, data loss, security breach
        SEV-2: High - Major feature broken, significant user impact
        SEV-3: Medium - Minor feature broken, workaround available
        SEV-4: Low - Cosmetic issues, no user impact
        """
        title_lower = title.lower()
        desc_lower = description.lower()
        combined = f"{title_lower} {desc_lower}"

        # SEV-1 indicators
        sev1_keywords = [
            "production down",
            "outage",
            "data loss",
            "security breach",
            "critical failure",
            "all users affected",
        ]
        if any(keyword in combined for keyword in sev1_keywords):
            return IncidentSeverity.SEV1

        # SEV-2 indicators
        sev2_keywords = [
            "major failure",
            "high priority",
            "significant impact",
            "multiple users",
            "main feature",
        ]
        if any(keyword in combined for keyword in sev2_keywords):
            return IncidentSeverity.SEV2

        # SEV-3 indicators
        sev3_keywords = [
            "minor issue",
            "workaround available",
            "limited impact",
            "single feature",
        ]
        if any(keyword in combined for keyword in sev3_keywords):
            return IncidentSeverity.SEV3

        # Source-based classification
        if source == "sla_breach":
            return IncidentSeverity.SEV2
        elif source == "workflow":
            return IncidentSeverity.SEV3

        # Default
        return IncidentSeverity.SEV4

    def _execute_runbook(self, incident: Incident) -> List[RunbookStep]:
        """
        Execute automated runbook for incident.

        Args:
            incident: Incident to handle

        Returns:
            List of executed runbook steps
        """
        logger.info(f"Executing runbook for {incident.incident_id}")

        # Get runbook for severity
        runbook = self._get_runbook(incident.severity)

        executed_steps = []

        for step in runbook:
            logger.info(f"Executing step: {step.name}")

            try:
                if step.action == "notify":
                    self._execute_notify_action(incident, step)
                elif step.action == "create_issue":
                    self._execute_create_issue_action(incident, step)
                elif step.action == "escalate":
                    self._execute_escalate_action(incident, step)
                elif step.action == "run_workflow":
                    self._execute_run_workflow_action(incident, step)
                elif step.action == "update_status":
                    self._execute_update_status_action(incident, step)

                step.executed = True
                step.executed_at = datetime.now(timezone.utc)
                executed_steps.append(step)

            except Exception as e:
                logger.error(f"Failed to execute step {step.name}: {e}")
                step.executed = False
                step.error = str(e)

        # Update incident with executed steps
        incident.runbook_steps = executed_steps
        self._save_incident(incident)

        return executed_steps

    def _get_runbook(self, severity: IncidentSeverity) -> List[RunbookStep]:
        """Get runbook steps for severity level."""
        if severity == IncidentSeverity.SEV1:
            return [
                RunbookStep(
                    name="Page on-call team",
                    action="notify",
                    params={"channel": "pagerduty", "priority": "critical"},
                ),
                RunbookStep(
                    name="Create war room",
                    action="create_issue",
                    params={"labels": ["incident", "sev-1", "war-room"]},
                ),
                RunbookStep(
                    name="Notify management",
                    action="notify",
                    params={"channel": "email", "recipients": ["management"]},
                ),
            ]
        elif severity == IncidentSeverity.SEV2:
            return [
                RunbookStep(
                    name="Notify on-call team",
                    action="notify",
                    params={"channel": "slack", "priority": "high"},
                ),
                RunbookStep(
                    name="Create tracking issue",
                    action="create_issue",
                    params={"labels": ["incident", "sev-2"]},
                ),
            ]
        elif severity == IncidentSeverity.SEV3:
            return [
                RunbookStep(
                    name="Notify team",
                    action="notify",
                    params={"channel": "slack", "priority": "normal"},
                ),
            ]
        else:  # SEV-4
            return [
                RunbookStep(
                    name="Log incident",
                    action="update_status",
                    params={"status": "triaging"},
                ),
            ]

    def _execute_notify_action(self, incident: Incident, step: RunbookStep):
        """Execute notification action."""
        # Use unified notification system
        notify_incident_created(
            incident_id=incident.incident_id,
            severity=incident.severity.value,
            repository=incident.repository,
            description=incident.description,
            status=incident.status.value,
            metadata={
                "title": incident.title,
                "created_at": incident.created_at.isoformat(),
                "workflow_run_id": incident.workflow_run_id,
            },
        )

    def _execute_create_issue_action(self, incident: Incident, step: RunbookStep):
        """Execute create issue action."""
        if incident.github_issue_number:
            logger.info(f"Issue already exists: #{incident.github_issue_number}")
            return

        owner, repo = incident.repository.split("/")
        labels = step.params.get("labels", ["incident"])

        issue_body = f"""
## Incident Details

- **Incident ID**: {incident.incident_id}
- **Severity**: {incident.severity.value}
- **Source**: {incident.source}
- **Created**: {incident.created_at.isoformat()}

## Description

{incident.description}

## Status

Current status: {incident.status.value}

---
*This issue was automatically created by the incident response system.*
"""

        issue = self.github.post(
            f"/repos/{owner}/{repo}/issues",
            json={
                "title": f"[{incident.severity.value}] {incident.title}",
                "body": issue_body,
                "labels": labels,
            },
        )

        incident.github_issue_number = issue.get("number")
        logger.info(f"Created issue #{incident.github_issue_number}")

    def _execute_escalate_action(self, incident: Incident, step: RunbookStep):
        """Execute escalation action."""
        logger.info(f"Escalating incident {incident.incident_id}")

        # Increase severity if not already SEV-1
        if incident.severity != IncidentSeverity.SEV1:
            old_severity = incident.severity
            incident.severity = IncidentSeverity(incident.severity.value[:-1] + "1")
            logger.info(
                f"Escalated from {old_severity.value} to {incident.severity.value}"
            )

        # Send escalation notification
        self._send_incident_notification(incident, "escalated")

    def _execute_run_workflow_action(self, incident: Incident, step: RunbookStep):
        """Execute workflow run action."""
        workflow_name = step.params.get("workflow")
        owner, repo = incident.repository.split("/")

        logger.info(f"Triggering workflow: {workflow_name}")

        self.github.post(
            f"/repos/{owner}/{repo}/actions/workflows/{workflow_name}/dispatches",
            json={"ref": "main", "inputs": {"incident_id": incident.incident_id}},
        )

    def _execute_update_status_action(self, incident: Incident, step: RunbookStep):
        """Execute status update action."""
        new_status = step.params.get("status")
        if new_status:
            incident.status = IncidentStatus(new_status.upper())
            logger.info(f"Updated status to {incident.status.value}")

    def update_incident_status(
        self, incident_id: str, status: IncidentStatus, resolution: Optional[str] = None
    ) -> Incident:
        """
        Update incident status.

        Args:
            incident_id: Incident ID
            status: New status
            resolution: Resolution details (for resolved status)

        Returns:
            Updated incident
        """
        logger.info(f"Updating incident {incident_id} to {status.value}")

        incident = self._load_incident(incident_id)
        old_status = incident.status
        incident.status = status

        if status == IncidentStatus.RESOLVED:
            incident.resolved_at = datetime.now(timezone.utc)
            incident.resolution = resolution or "Resolved"

            # Calculate time to resolution
            incident.time_to_resolution_minutes = (
                incident.resolved_at - incident.created_at
            ).total_seconds() / 60

        self._save_incident(incident)

        # Send notification if status changed
        if old_status != status:
            self._send_incident_notification(incident, f"status_changed_{status.value}")

        return incident

    def generate_post_incident_report(self, incident_id: str) -> PostIncidentReport:
        """
        Generate post-incident report.

        Args:
            incident_id: Incident ID

        Returns:
            Post-incident report
        """
        logger.info(f"Generating post-incident report for {incident_id}")

        incident = self._load_incident(incident_id)

        # Calculate metrics
        timeline = self._build_timeline(incident)
        root_cause = self._analyze_root_cause(incident)
        lessons_learned = self._extract_lessons_learned(incident)
        action_items = self._identify_action_items(incident)

        report = PostIncidentReport(
            incident_id=incident_id,
            incident=incident,
            timeline=timeline,
            root_cause=root_cause,
            lessons_learned=lessons_learned,
            action_items=action_items,
            generated_at=datetime.now(timezone.utc),
        )

        # Save report
        self._save_report(report)

        return report

    def _build_timeline(self, incident: Incident) -> List[Dict]:
        """Build incident timeline."""
        timeline = [
            {
                "time": incident.created_at.isoformat(),
                "event": "Incident created",
                "details": f"Severity: {incident.severity.value}",
            }
        ]

        if incident.runbook_steps:
            for step in incident.runbook_steps:
                if step.executed and step.executed_at:
                    timeline.append(
                        {
                            "time": step.executed_at.isoformat(),
                            "event": f"Runbook step: {step.name}",
                            "details": f"Action: {step.action}",
                        }
                    )

        if incident.resolved_at:
            timeline.append(
                {
                    "time": incident.resolved_at.isoformat(),
                    "event": "Incident resolved",
                    "details": incident.resolution,
                }
            )

        return timeline

    def _analyze_root_cause(self, incident: Incident) -> str:
        """Analyze incident root cause."""
        # Simplified root cause analysis
        if "workflow" in incident.source:
            return "Workflow failure due to test errors or configuration issues"
        elif "sla_breach" in incident.source:
            return "SLA breach due to delayed response or resolution"
        else:
            return "Root cause requires further investigation"

    def _extract_lessons_learned(self, incident: Incident) -> List[str]:
        """Extract lessons learned from incident."""
        lessons = []

        if incident.time_to_resolution_minutes:
            if incident.time_to_resolution_minutes < 60:
                lessons.append("Quick resolution time demonstrates effective runbook")
            elif incident.time_to_resolution_minutes > 240:
                lessons.append(
                    "Long resolution time indicates need for process improvement"
                )

        if incident.severity in [IncidentSeverity.SEV1, IncidentSeverity.SEV2]:
            lessons.append(
                "High severity incidents require improved monitoring and alerting"
            )

        return lessons

    def _identify_action_items(self, incident: Incident) -> List[Dict]:
        """Identify action items from incident."""
        actions = []

        # Always add documentation action
        actions.append(
            {
                "action": "Update runbook documentation",
                "owner": "team",
                "priority": "medium",
                "due_date": "1 week",
            }
        )

        # Add severity-specific actions
        if incident.severity in [IncidentSeverity.SEV1, IncidentSeverity.SEV2]:
            actions.append(
                {
                    "action": "Improve monitoring and alerting",
                    "owner": "ops-team",
                    "priority": "high",
                    "due_date": "2 weeks",
                }
            )

        return actions

    def _generate_incident_id(self) -> str:
        """Generate unique incident ID."""
        timestamp = datetime.now().strftime("%Y%m%d")
        existing = list(self.incidents_dir.glob(f"INC-{timestamp}-*.json"))
        next_num = len(existing) + 1
        return f"INC-{timestamp}-{next_num:03d}"

    def _save_incident(self, incident: Incident):
        """Save incident to disk."""
        incident_file = self.incidents_dir / f"{incident.incident_id}.json"
        with open(incident_file, "w") as f:
            json.dump(incident.dict(), f, indent=2, default=str)
        logger.debug(f"Saved incident to {incident_file}")

    def _load_incident(self, incident_id: str) -> Incident:
        """Load incident from disk."""
        incident_file = self.incidents_dir / f"{incident_id}.json"
        with open(incident_file) as f:
            data = json.load(f)
        return Incident(**data)

    def _save_report(self, report: PostIncidentReport):
        """Save post-incident report."""
        report_file = self.incidents_dir / f"{report.incident_id}_report.json"
        with open(report_file, "w") as f:
            json.dump(report.dict(), f, indent=2, default=str)
        logger.info(f"Saved report to {report_file}")

    def _create_github_issue(self, owner: str, repo: str, incident: Incident) -> Dict:
        """Create GitHub issue for incident."""
        issue = self.github.post(
            f"/repos/{owner}/{repo}/issues",
            json={
                "title": f"[{incident.severity.value}] {incident.title}",
                "body": f"Incident ID: {incident.incident_id}\n\n{incident.description}",
                "labels": ["incident", incident.severity.value.lower()],
            },
        )
        return issue

    def _send_incident_notification(self, incident: Incident, event: str):
        """Send incident notification via unified notification system."""
        # Notifications now handled by notify_incident_created/resolved
        # This method maintained for backward compatibility but is now a no-op
        pass

    def _get_notification_channels(self, severity: IncidentSeverity) -> List[str]:
        """Get notification channels for severity."""
        if severity == IncidentSeverity.SEV1:
            return ["slack", "pagerduty", "email"]
        elif severity == IncidentSeverity.SEV2:
            return ["slack", "email"]
        elif severity == IncidentSeverity.SEV3:
            return ["slack"]
        else:
            return []

    def _format_notification(self, incident: Incident, event: str) -> str:
        """Format notification message."""
        emoji = {
            "created": "🚨",
            "escalated": "⚠️",
            "status_changed_RESOLVED": "✅",
            "status_changed_INVESTIGATING": "🔍",
        }.get(event, "📢")

        return f"""
{emoji} **Incident {event.replace('_', ' ').title()}**

ID: {incident.incident_id}
Title: {incident.title}
Severity: {incident.severity.value}
Status: {incident.status.value}
Repository: {incident.repository}
"""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Incident Response Automation")
    parser.add_argument("--owner", help="Repository owner")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument("--create", action="store_true", help="Create incident")
    parser.add_argument("--title", help="Incident title")
    parser.add_argument("--description", help="Incident description")
    parser.add_argument(
        "--run-id", type=int, help="Workflow run ID (for workflow incidents)"
    )
    parser.add_argument("--incident-id", help="Incident ID")
    parser.add_argument(
        "--execute-runbook", action="store_true", help="Execute runbook"
    )
    parser.add_argument("--update-status", help="Update status")
    parser.add_argument("--resolution", help="Resolution details")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    config = load_config("incident.yml", IncidentConfig)
    github = GitHubAPIClient()

    # Initialize engine
    engine = IncidentResponseEngine(config, github)

    if args.create:
        if not all([args.owner, args.repo, args.title]):
            print("ERROR: --owner, --repo, and --title required for --create")
            return

        description = (
            args.description or f"Incident created from workflow run #{args.run_id}"
            if args.run_id
            else "Manual incident"
        )
        source = "workflow" if args.run_id else "manual"

        incident = engine.create_incident(
            args.owner, args.repo, args.title, description, source
        )
        print(f"\n✅ Created incident {incident.incident_id}")
        print(f"   Severity: {incident.severity.value}")
        print(f"   Status: {incident.status.value}")

    elif args.execute_runbook:
        if not args.incident_id:
            print("ERROR: --incident-id required for --execute-runbook")
            return

        incident = engine._load_incident(args.incident_id)
        steps = engine._execute_runbook(incident)
        print(f"\n✅ Executed {len(steps)} runbook steps")

    elif args.update_status:
        if not args.incident_id:
            print("ERROR: --incident-id required for --update-status")
            return

        status = IncidentStatus(args.update_status.upper())
        incident = engine.update_incident_status(
            args.incident_id, status, args.resolution
        )
        print(f"\n✅ Updated {incident.incident_id} to {status.value}")

    elif args.report:
        if not args.incident_id:
            print("ERROR: --incident-id required for --report")
            return

        report = engine.generate_post_incident_report(args.incident_id)
        print(f"\n✅ Generated post-incident report for {args.incident_id}")
        print(f"   Timeline events: {len(report.timeline)}")
        print(f"   Action items: {len(report.action_items)}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

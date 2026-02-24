# Unified Notification System

> **Centralized notification management for all Week 9 automation capabilities**

## Overview

The **Unified Notification System** provides a centralized, enterprise-grade
notification infrastructure that consolidates all Week 9 automation alerts into
a single, consistent, and reliable delivery platform.

### Benefits

- **Centralized Management**: Single configuration for all notification needs
- **Multi-Channel Support**: Slack, Email, PagerDuty, custom webhooks
- **Smart Routing**: Priority-based and source-based channel routing
- **Rate Limiting**: Prevent notification storms
- **Deduplication**: Avoid sending duplicate notifications
- **Delivery Tracking**: Full audit trail of all notifications
- **Template System**: Consistent message formatting
- **Health Monitoring**: Monitor notification system health

### Key Features

| Feature               | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| **Multi-Channel**     | Slack, Email, PagerDuty, webhooks                          |
| **Priority Routing**  | CRITICAL → PagerDuty+Slack+Email, HIGH → Slack+Email, etc. |
| **Rate Limiting**     | 10/min Slack, 5/min Email, configurable                    |
| **Deduplication**     | 5-minute window, prevents duplicate alerts                 |
| **Templates**         | Pre-built templates for common scenarios                   |
| **Retry Logic**       | 3 attempts with exponential backoff                        |
| **Delivery Tracking** | JSON logs with full audit trail                            |

### Statistics

- **Channels Supported**: 4 (Slack, Email, PagerDuty, Webhook)
- **Priority Levels**: 5 (CRITICAL, HIGH, MEDIUM, LOW, INFO)
- **Message Templates**: 5 pre-built templates
- **Rate Limits**: Configurable per channel
- **Deduplication Window**: 5 minutes (configurable)
- **Retry Attempts**: 3 with exponential backoff

______________________________________________________________________

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Week 9 Systems (Sources)                     │
├─────────────────────────────────────────────────────────────────┤
│ SLA Monitor │ Incidents │ Validation │ Self-Healing │ Analytics │
└──────┬──────────┬───────────┬────────────┬──────────────┬───────┘
       │          │           │            │              │
       └──────────┴───────────┴────────────┴──────────────┘
                              │
                     ┌────────▼────────┐
                     │   Notification  │
                     │     Manager     │
                     └────────┬────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
   ┌───▼───┐           ┌──────▼──────┐       ┌──────▼──────┐
   │ Slack │           │   Email     │       │  PagerDuty  │
   └───────┘           └─────────────┘       └─────────────┘
       │                      │                      │
   ┌───▼───────────┐     ┌───▼────────┐      ┌──────▼──────┐
   │ #incidents    │     │ oncall@    │      │ Production  │
   │ #automation   │     │ team@      │      │ Service     │
   │ #monitoring   │     │ mgmt@      │      └─────────────┘
   └───────────────┘     └────────────┘
```

### Data Flow

1. **Source System** creates notification (SLA breach, incident, etc.)
1. **Notification Manager** receives notification with priority and source
1. **Routing Logic** determines channels based on priority and source
1. **Rate Limiting** checks if channel is within limits
1. **Deduplication** checks if notification was recently sent
1. **Delivery** sends to each channel with retry logic
1. **Tracking** logs delivery status and metrics

### Components

#### NotificationManager

Main orchestration class:

```python
from notification_manager import NotificationManager, Notification, Priority

# Initialize
manager = NotificationManager()

# Send notification
notification = Notification(
    title="SLA Breach Detected",
    message="P0 issue response time exceeded",
    priority=Priority.CRITICAL,
    source="sla-monitor",
    channels=["slack", "pagerduty", "email"]
)

records = manager.send(notification)
```

#### Notification Model

```python
Notification(
    title: str,              # Short title
    message: str,            # Detailed message
    priority: Priority,      # CRITICAL, HIGH, MEDIUM, LOW, INFO
    source: str,             # Source system (sla-monitor, incident-response, etc.)
    channels: List[str],     # Channels to send to (optional, uses routing if empty)
    metadata: Dict,          # Additional metadata
    timestamp: datetime,     # Timestamp (auto-generated)
    notification_id: str     # Unique ID (auto-generated)
)
```

#### Priority Levels

| Priority     | Use Case                             | Default Channels                                       |
| ------------ | ------------------------------------ | ------------------------------------------------------ |
| **CRITICAL** | SEV-1 incidents, P0 SLA breaches     | Slack (#incidents) + PagerDuty + Email (oncall + mgmt) |
| **HIGH**     | SEV-2 incidents, P1 SLA breaches     | Slack (#incidents) + Email (team)                      |
| **MEDIUM**   | SEV-3 incidents, validation failures | Slack (#automation-alerts) + Email (team)              |
| **LOW**      | Successful operations, informational | Slack (#monitoring)                                    |
| **INFO**     | General information                  | None (typically not sent)                              |

______________________________________________________________________

## Configuration

### Quick Start

1. **Copy default configuration**:

   ```bash
   cp .github/notifications.yml.example .github/notifications.yml
   ```

1. **Set environment variables**:

   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   export SLACK_INCIDENTS_WEBHOOK="https://hooks.slack.com/services/INCIDENTS/WEBHOOK"
   export SLACK_AUTOMATION_WEBHOOK="https://hooks.slack.com/services/AUTOMATION/WEBHOOK"
   export PAGERDUTY_INTEGRATION_KEY="your-pagerduty-key"  # pragma: allowlist secret
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_USERNAME="automation@example.com"
   export SMTP_PASSWORD="your-password"  # pragma: allowlist secret
   ```

1. **Test configuration**:

   ```bash
   python automation/scripts/notification_manager.py \
     --title "Test Notification" \
     --message "Testing unified notification system" \
     --priority INFO \
     --source manual
   ```

### Environment Variables

Required:

- `SLACK_WEBHOOK_URL` - Default Slack webhook URL
- `SLACK_INCIDENTS_WEBHOOK` - Slack webhook for #incidents channel
- `SLACK_AUTOMATION_WEBHOOK` - Slack webhook for #automation-alerts
- `SLACK_MONITORING_WEBHOOK` - Slack webhook for #monitoring
- `PAGERDUTY_INTEGRATION_KEY` - PagerDuty integration key
- `SMTP_SERVER` - SMTP server address
- `SMTP_USERNAME` - SMTP username
- `SMTP_PASSWORD` - SMTP password

Optional:

- `DATADOG_WEBHOOK_URL` - Datadog webhook URL
- `DATADOG_API_KEY` - Datadog API key
- `JIRA_WEBHOOK_URL` - Jira webhook URL
- `JIRA_USERNAME` - Jira username
- `JIRA_API_TOKEN` - Jira API token

### Configuration File

`.github/notifications.yml`:

```yaml
# Priority-based routing
priority_routing:
  CRITICAL:
    - "slack:#incidents"
    - "pagerduty"
    - "email:oncall"
    - "email:management"

# Source-specific routing (overrides priority routing)
source_routing:
  sla-monitor:
    CRITICAL:
      - "slack:#oncall"
      - "pagerduty"
      - "email:oncall"

# Rate limiting
rate_limiting:
  enabled: true
  max_per_minute:
    slack: 10
    email: 5
    pagerduty: 5

# Deduplication
deduplication:
  enabled: true
  window_seconds: 300  # 5 minutes
```

See [Configuration Reference](#configuration-reference) for full details.

______________________________________________________________________

## Usage

### Basic Usage

```python
from notification_manager import NotificationManager, Notification, Priority

# Initialize manager
manager = NotificationManager()

# Send notification
notification = Notification(
    title="SLA Breach",
    message="Issue #123 response time exceeded",
    priority=Priority.HIGH,
    source="sla-monitor"
)

records = manager.send(notification)

# Check results
for channel, record in records.items():
    if record.status == NotificationStatus.SENT:
        print(f"✅ Sent to {channel}")
    else:
        print(f"❌ Failed to send to {channel}: {record.error}")
```

### Integration with Week 9 Systems

#### SLA Monitor

```python
from notification_manager import NotificationManager, Notification, Priority

def notify_sla_breach(issue_number: str, priority: str, threshold: int, actual: int):
    manager = NotificationManager()

    notification = Notification(
        title=f"SLA Breach - {priority}",
        message=f"Issue #{issue_number} response time exceeded\n"
                f"Threshold: {threshold}min, Actual: {actual}min",
        priority=Priority.CRITICAL if priority == "P0" else Priority.HIGH,
        source="sla-monitor",
        metadata={
            "issue_number": issue_number,
            "priority": priority,
            "threshold": threshold,
            "actual": actual
        }
    )

    manager.send(notification)
```

#### Incident Response

```python
from notification_manager import NotificationManager, Notification, Priority

def notify_incident_created(incident_id: str, severity: str, description: str):
    manager = NotificationManager()

    priority_map = {
        "SEV-1": Priority.CRITICAL,
        "SEV-2": Priority.HIGH,
        "SEV-3": Priority.MEDIUM,
        "SEV-4": Priority.LOW
    }

    notification = Notification(
        title=f"Incident Created - {severity}",
        message=f"**Incident ID:** {incident_id}\n{description}",
        priority=priority_map.get(severity, Priority.MEDIUM),
        source="incident-response",
        metadata={
            "incident_id": incident_id,
            "severity": severity
        }
    )

    manager.send(notification)
```

#### Validation Framework

```python
from notification_manager import NotificationManager, Notification, Priority

def notify_validation_failure(capability: str, errors: List[str]):
    manager = NotificationManager()

    notification = Notification(
        title=f"Validation Failed - {capability}",
        message=f"Validation errors:\n" + "\n".join(f"- {e}" for e in errors),
        priority=Priority.MEDIUM,
        source="validation-framework",
        metadata={
            "capability": capability,
            "error_count": len(errors)
        }
    )

    manager.send(notification)
```

### CLI Usage

Test notifications from command line:

```bash
# Send test notification
python automation/scripts/notification_manager.py \
  --title "Test Alert" \
  --message "This is a test notification" \
  --priority HIGH \
  --source manual \
  --channels slack email

# Send critical notification
python automation/scripts/notification_manager.py \
  --title "Production Incident" \
  --message "Database connection pool exhausted" \
  --priority CRITICAL \
  --source incident-response

# Send info notification (no channels by default)
python automation/scripts/notification_manager.py \
  --title "Deployment Complete" \
  --message "Version 1.2.3 deployed successfully" \
  --priority INFO \
  --source deployment
```

______________________________________________________________________

## Message Templates

### Using Templates

Templates provide consistent formatting across all notifications:

```python
# Use template for SLA breach
notification = Notification(
    title="SLA Breach Detected - P0",
    message=template_sla_breach.format(
        item_type="issue",
        item_number="123",
        repository="org/repo",
        breach_type="response_time",
        threshold="15min",
        actual="45min",
        priority="P0"
    ),
    priority=Priority.CRITICAL,
    source="sla-monitor"
)
```

### Available Templates

#### 1. SLA Breach

```
**Item:** {{item_type}} #{{item_number}}
**Repository:** {{repository}}
**Breach Type:** {{breach_type}}
**Threshold:** {{threshold}}
**Actual:** {{actual}}
**Priority:** {{priority}}

Action required to maintain SLA compliance.
```

#### 2. Incident Created

```
**Incident ID:** {{incident_id}}
**Severity:** {{severity}}
**Repository:** {{repository}}

{{description}}

**Status:** {{status}}
**Created:** {{created_at}}
```

#### 3. Validation Failure

```
**Capability:** {{capability}}
**Repository:** {{repository}}

{{error_message}}

Please investigate and remediate.
```

#### 4. Self-Healing Failure

```
**Workflow:** {{workflow}}
**Run ID:** {{run_id}}
**Failure Type:** {{failure_type}}
**Attempts:** {{attempts}}

Manual intervention may be required.
```

#### 5. Maintenance Scheduled

```
**Task:** {{task_name}}
**Window:** {{start_time}} - {{end_time}}
**Duration:** {{duration}} minutes
**Impact:** {{impact}}

Maintenance will be performed automatically.
```

______________________________________________________________________

## Channels

### Slack

#### Configuration

```yaml
channels:
  slack:
    webhook_url: "${SLACK_WEBHOOK_URL}"
    channels:
      "#incidents":
        webhook_url: "${SLACK_INCIDENTS_WEBHOOK}"
      "#automation-alerts":
        webhook_url: "${SLACK_AUTOMATION_WEBHOOK}"
```

#### Features

- Rich message formatting with Slack blocks
- Priority emoji indicators (🚨 CRITICAL, ⚠️ HIGH, ℹ️ MEDIUM, ✅ LOW)
- Metadata sections with structured data
- Timestamp footer
- Mentions for critical notifications (optional)

#### Channel Mapping

| Channel              | Purpose                                | Priority Levels |
| -------------------- | -------------------------------------- | --------------- |
| `#incidents`         | Critical incidents, P0/P1 SLA breaches | CRITICAL, HIGH  |
| `#automation-alerts` | System failures, validation failures   | MEDIUM, HIGH    |
| `#monitoring`        | Metrics, successful operations         | LOW, MEDIUM     |
| `#oncall`            | On-call team notifications             | CRITICAL, HIGH  |

### Email

#### Configuration

```yaml
channels:
  email:
    smtp:
      server: "smtp.gmail.com"
      port: 587
      use_tls: true
    recipients:
      oncall:
        - "oncall@example.com"
      team:
        - "team@example.com"
      management:
        - "mgmt@example.com"
```

#### Features

- HTML or plain text formatting
- Recipient groups (oncall, team, management, all)
- Custom subject prefixes
- Branded headers/footers

### PagerDuty

#### Configuration

```yaml
channels:
  pagerduty:
    integration_key: "${PAGERDUTY_INTEGRATION_KEY}"
    services:
      production:
        integration_key: "${PAGERDUTY_PRODUCTION_KEY}"
```

#### Features

- Automatic incident creation
- Severity mapping (CRITICAL → critical, HIGH → error, etc.)
- Custom details with metadata
- Integration with PagerDuty services

### Custom Webhooks

#### Configuration

```yaml
channels:
  webhooks:
    datadog:
      url: "${DATADOG_WEBHOOK_URL}"
      headers:
        DD-API-KEY: "${DATADOG_API_KEY}"
```

#### Features

- HTTP POST with JSON payload
- Custom headers (auth, API keys)
- Full notification object in payload
- Configurable timeouts

______________________________________________________________________

## Rate Limiting

### How It Works

Rate limiting prevents notification storms by limiting the number of
notifications sent per channel per time window.

**Default Limits:**

- **Slack**: 10 notifications/minute
- **Email**: 5 notifications/minute
- **PagerDuty**: 5 notifications/minute
- **Webhooks**: 20 notifications/minute

### Configuration

```yaml
rate_limiting:
  enabled: true
  max_per_minute:
    slack: 10
    email: 5
    pagerduty: 5
  burst_size:
    slack: 20  # Allow bursts up to 20
```

### Behavior

When rate limit is exceeded:

1. Notification status set to `RATE_LIMITED`
1. Delivery record logged
1. No retry attempts
1. Manager returns immediately

**Note**: Critical notifications bypass rate limiting (configurable).

______________________________________________________________________

## Deduplication

### How It Works

Deduplication prevents sending duplicate notifications within a time window.

**Deduplication Keys:**

- `source` (e.g., "sla-monitor")
- `title` (e.g., "SLA Breach - P0")

If a notification with the same source+title was sent within the window, it's
skipped.

### Configuration

```yaml
deduplication:
  enabled: true
  window_seconds: 300  # 5 minutes
  keys:
    - source
    - title
  exceptions:
    - priority: CRITICAL  # Always send CRITICAL
```

### Exceptions

Some notifications always bypass deduplication:

- `priority: CRITICAL` (configurable)
- `source: incident-response` (configurable)

______________________________________________________________________

## Delivery Tracking

### Delivery Records

Every notification delivery is tracked:

```python
DeliveryRecord(
    notification_id="NOTIF-20260116_120000-001",
    channel="slack",
    status=NotificationStatus.SENT,
    attempts=1,
    last_attempt=datetime.now(),
    delivered_at=datetime.now(),
    error=None
)
```

### Statuses

- `PENDING` - Not yet sent
- `SENT` - Successfully delivered
- `FAILED` - Delivery failed after all retries
- `RETRYING` - Retry in progress
- `RATE_LIMITED` - Skipped due to rate limit

### Storage

Delivery records are stored in `.github/notifications/delivery_log/`:

```
.github/notifications/delivery_log/
├── NOTIF-20260116_120000-001.json
├── NOTIF-20260116_120030-002.json
└── NOTIF-20260116_120100-003.json
```

### Retention

- **Default**: 30 days
- **Configurable** in `.github/notifications.yml`
- **Auto-cleanup**: Runs weekly

______________________________________________________________________

## Monitoring

### Health Checks

The notification system monitors its own health:

```yaml
health_monitoring:
  enabled: true
  check_interval_minutes: 15
  metrics:
    - delivery_success_rate
    - delivery_latency
    - rate_limit_hits
    - failed_deliveries
  alert_threshold:
    success_rate: 0.95  # Alert if <95%
```

### Metrics

Tracked metrics:

| Metric                    | Description                          | Alert Threshold |
| ------------------------- | ------------------------------------ | --------------- |
| **delivery_success_rate** | % of successful deliveries           | \<95%           |
| **delivery_latency**      | Time to deliver notification         | >30s            |
| **rate_limit_hits**       | Number of rate limit hits            | >10/hour        |
| **deduplication_hits**    | Number of deduplicated notifications | -               |
| **failed_deliveries**     | Number of failed deliveries          | >5/hour         |

### Prometheus Export

Metrics available at `/metrics/notifications`:

```
# HELP notification_deliveries_total Total notification deliveries
# TYPE notification_deliveries_total counter
notification_deliveries_total{channel="slack",status="sent"} 1234

# HELP notification_delivery_duration_seconds Time to deliver notification
# TYPE notification_delivery_duration_seconds histogram
notification_delivery_duration_seconds_bucket{channel="slack",le="1"} 1000
```

______________________________________________________________________

## Troubleshooting

### Common Issues

#### 1. Notifications Not Sending

**Symptoms:**

- No notifications received
- Delivery records show `FAILED` status

**Solutions:**

- Check environment variables are set correctly
- Verify webhook URLs are valid
- Test with CLI to isolate issue
- Check delivery logs for error messages

```bash
# Test Slack webhook
curl -X POST "${SLACK_WEBHOOK_URL}" \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test message"}'

# Check delivery logs
ls -la .github/notifications/delivery_log/
cat .github/notifications/delivery_log/NOTIF-*.json
```

#### 2. Rate Limiting

**Symptoms:**

- Notifications delayed or skipped
- Delivery records show `RATE_LIMITED` status

**Solutions:**

- Increase rate limits in configuration
- Reduce notification frequency
- Use aggregation to batch notifications
- Exempt critical notifications

```yaml
rate_limiting:
  max_per_minute:
    slack: 20  # Increase from 10
```

#### 3. Duplicate Notifications

**Symptoms:**

- Same notification sent multiple times
- Deduplication not working

**Solutions:**

- Verify deduplication is enabled
- Check deduplication window is appropriate
- Review deduplication keys
- Check for cache issues

```yaml
deduplication:
  enabled: true
  window_seconds: 600  # Increase to 10 minutes
```

#### 4. PagerDuty Not Creating Incidents

**Symptoms:**

- No PagerDuty incidents created
- Delivery shows `SENT` but no incident

**Solutions:**

- Verify integration key is correct
- Check PagerDuty service is active
- Review severity mapping
- Test with PagerDuty API directly

```bash
# Test PagerDuty integration
curl -X POST https://events.pagerduty.com/v2/enqueue \
  -H 'Content-Type: application/json' \
  -d '{
    "routing_key": "YOUR_KEY",
    "event_action": "trigger",
    "payload": {
      "summary": "Test incident",
      "severity": "critical",
      "source": "test"
    }
  }'
```

### Debug Mode

Enable debug logging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with debug flag
python automation/scripts/notification_manager.py \
  --title "Test" \
  --message "Debug test" \
  --priority INFO \
  --source manual \
  --debug
```

### Support

- **Documentation**: This guide
- **Logs**: `.github/notifications/delivery_log/`
- **Configuration**: `.github/notifications.yml`
- **Issues**: Open issue in repository
- **Team**: Contact automation team

______________________________________________________________________

## Configuration Reference

### Complete Configuration

See `.github/notifications.yml` for full configuration with all options
documented.

### Key Sections

- **channels**: Channel-specific configuration (Slack, Email, PagerDuty,
  webhooks)
- **priority_routing**: Default channels for each priority level
- **source_routing**: Override routing based on notification source
- **templates**: Message templates for consistent formatting
- **rate_limiting**: Rate limit configuration per channel
- **deduplication**: Deduplication settings and exceptions
- **delivery**: Retry logic, timeouts, tracking
- **formatting**: Channel-specific formatting options
- **health_monitoring**: Health check and alerting
- **integration**: Week 9 system integration settings

______________________________________________________________________

## Appendix

### File Structure

```
.github/
├── notifications.yml               # Main configuration
└── notifications/
    ├── delivery_log/               # Delivery records
    │   ├── NOTIF-*.json
    │   └── ...
    └── handlers/                   # Custom handlers (optional)
        └── custom_handler.py

automation/scripts/
└── notification_manager.py         # Notification manager

docs/
└── UNIFIED_NOTIFICATION_SYSTEM.md  # This document
```

### Dependencies

Python packages:

- `pydantic` - Data validation and models
- `pyyaml` - YAML configuration parsing
- `requests` - HTTP requests for webhooks

### API Reference

#### NotificationManager

```python
class NotificationManager:
    def __init__(config_path: str)
    def send(notification: Notification) -> Dict[str, DeliveryRecord]
```

#### Notification

```python
@dataclass
class Notification:
    title: str
    message: str
    priority: Priority
    source: str
    channels: List[str] = []
    metadata: Dict = {}
    timestamp: datetime = field(default_factory=datetime.now)
    notification_id: Optional[str] = None
```

#### Priority

```python
class Priority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"
```

### Changelog

- **2026-01-16**: Initial release
  - Multi-channel support (Slack, Email, PagerDuty, webhooks)
  - Priority-based routing
  - Rate limiting and deduplication
  - Delivery tracking
  - Message templates
  - Health monitoring

______________________________________________________________________

**Next Steps:**

1. Configure channels (Slack, Email, PagerDuty)
1. Set environment variables
1. Test with CLI
1. Integrate with Week 9 systems
1. Monitor delivery metrics

For questions or issues, contact the automation team or open an issue in the
repository.

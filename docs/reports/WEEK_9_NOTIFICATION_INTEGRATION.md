# Week 9 Notification Integration Guide

> **Complete guide for integrating Week 9 systems with the unified notification
> manager**

## Overview

This guide covers how to migrate existing Week 9 automation systems to use the
unified notification manager instead of fragmented notification code.

### Benefits of Integration

- **Centralized Configuration**: Single place for all notification settings
- **Consistent Formatting**: All notifications follow same templates
- **Rate Limiting**: Automatic prevention of notification storms
- **Deduplication**: Avoid sending duplicate alerts
- **Delivery Tracking**: Full audit trail of all notifications
- **Multi-Channel**: Easy to add/remove channels without code changes

______________________________________________________________________

## Quick Start

### Before Integration

Old notification code (fragmented across systems):

```python
# Old way - direct Slack call
import requests
webhook_url = os.getenv("SLACK_WEBHOOK_URL")
requests.post(webhook_url, json={"text": "SLA breach detected"})
```

### After Integration

New unified approach:

```python
# New way - unified notification
from notification_integration import notify_sla_breach

notify_sla_breach(
    item_type="issue",
    item_number="123",
    repository="org/repo",
    breach_type="response_time",
    threshold="15min",
    actual="45min",
    priority="P0"
)
```

**Benefits:**

- ✅ Automatic channel routing based on priority
- ✅ Consistent message formatting
- ✅ Rate limiting and deduplication
- ✅ Delivery tracking
- ✅ No manual Slack API calls

______________________________________________________________________

## Integration by System

### 1. SLA Monitor

**Integration Module:** `notification_integration.py`

**Functions Available:**

```python
from notification_integration import notify_sla_breach, notify_sla_compliance

# Notify about SLA breach
notify_sla_breach(
    item_type="issue",
    item_number="123",
    repository="org/repo",
    breach_type="response_time",
    threshold="15min",
    actual="45min",
    priority="P0",  # Maps to Priority.CRITICAL
    metadata={"additional": "data"}
)

# Notify about SLA compliance
notify_sla_compliance(
    repository="org/repo",
    compliance_rate=0.93,  # 93%
    period_days=30,
    metadata={"breaches": 5}
)
```

**Priority Mapping:**

- `P0` → `Priority.CRITICAL` → Slack + PagerDuty + Email (oncall + mgmt)
- `P1` → `Priority.HIGH` → Slack + Email (team)
- `P2` → `Priority.MEDIUM` → Slack + Email (team)
- `P3` → `Priority.LOW` → Slack only

**Migration Steps:**

1. Import notification functions:

   ```python
   from notification_integration import notify_sla_breach
   ```

1. Replace existing notification code:

   ```python
   # OLD:
   send_notification("slack", f"SLA breach: {item_number}")

   # NEW:
   notify_sla_breach(
       item_type=item_type,
       item_number=item_number,
       repository=f"{owner}/{repo}",
       breach_type=breach_type,
       threshold=str(threshold_minutes) + "min",
       actual=str(actual_minutes) + "min",
       priority=priority
   )
   ```

### 2. Incident Response

**Functions Available:**

```python
from notification_integration import (
    notify_incident_created,
    notify_incident_resolved
)

# Notify about new incident
notify_incident_created(
    incident_id="INC-001",
    severity="SEV-1",
    repository="org/repo",
    description="Database connection pool exhausted",
    status="OPEN",
    metadata={"affected_services": ["api", "web"]}
)

# Notify about resolved incident
notify_incident_resolved(
    incident_id="INC-001",
    severity="SEV-1",
    duration_minutes=127,
    metadata={"resolution": "Increased pool size"}
)
```

**Severity Mapping:**

- `SEV-1` → `Priority.CRITICAL` → All channels
- `SEV-2` → `Priority.HIGH` → Slack + Email
- `SEV-3` → `Priority.MEDIUM` → Slack + Email
- `SEV-4` → `Priority.LOW` → Slack only

**Migration Steps:**

1. Find incident creation code:

   ```python
   # OLD:
   send_notification("slack", f"Incident {incident_id} created")
   send_notification("pagerduty", incident_details)
   ```

1. Replace with unified call:

   ```python
   # NEW:
   notify_incident_created(
       incident_id=incident.id,
       severity=incident.severity.value,
       repository=incident.repository,
       description=incident.description,
       status=incident.status.value
   )
   ```

### 3. Validation Framework

**Functions Available:**

```python
from notification_integration import (
    notify_validation_failure,
    notify_validation_success
)

# Notify about validation failure
notify_validation_failure(
    capability="auto-merge",
    repository="org/repo",
    errors=["Merge rate below threshold", "No recent merges"],
    warnings=["Model accuracy decreasing"],
    metadata={"expected_rate": 0.30, "actual_rate": 0.15}
)

# Notify about successful validation
notify_validation_success(
    repository="org/repo",
    passed_count=6,
    total_count=7,
    metadata={"failed": ["analytics"]}
)
```

**Migration Steps:**

1. In `_send_validation_notification()`:

   ```python
   # OLD:
   send_notification("slack", validation_message)

   # NEW:
   if suite.failed > 0:
       failed_capabilities = [r.capability for r in suite.results if not r.passed]
       for result in suite.results:
           if not result.passed:
               notify_validation_failure(
                   capability=result.capability,
                   repository=suite.repository,
                   errors=result.errors,
                   warnings=result.warnings,
                   metadata=result.metrics
               )
   else:
       notify_validation_success(
           repository=suite.repository,
           passed_count=suite.passed,
           total_count=len(suite.results)
       )
   ```

### 4. Self-Healing

**Functions Available:**

```python
from notification_integration import (
    notify_self_healing_success,
    notify_self_healing_failure
)

# Notify about successful healing
notify_self_healing_success(
    workflow_name="CI Build",
    run_id=12345,
    failure_type="dependency_conflict",
    action_taken="Updated package versions",
    metadata={"retry_count": 2}
)

# Notify about healing failure
notify_self_healing_failure(
    workflow_name="CI Build",
    run_id=12346,
    failure_type="test_failure",
    attempts=3,
    metadata={"last_error": "Timeout"}
)
```

**Migration Steps:**

1. In `_send_notification()`:

   ```python
   # OLD:
   if self.config.send_notifications:
       send_notification("slack", f"Self-healing {status}")

   # NEW:
   if classification.auto_fixable and recovery_success:
       notify_self_healing_success(
           workflow_name=workflow_name,
           run_id=run.id,
           failure_type=classification.failure_type,
           action_taken=action_taken
       )
   else:
       notify_self_healing_failure(
           workflow_name=workflow_name,
           run_id=run.id,
           failure_type=classification.failure_type,
           attempts=classification.recovery_attempts
       )
   ```

### 5. Maintenance Scheduler

**Functions Available:**

```python
from notification_integration import (
    notify_maintenance_scheduled,
    notify_maintenance_complete
)

# Notify about scheduled maintenance
notify_maintenance_scheduled(
    task_name="Database index rebuild",
    start_time="2026-01-16T02:00:00Z",
    end_time="2026-01-16T04:00:00Z",
    duration_minutes=120,
    impact="Read-only mode during rebuild"
)

# Notify about completed maintenance
notify_maintenance_complete(
    task_name="Database index rebuild",
    duration_minutes=87,
    success=True,
    metadata={"indexes_rebuilt": 15}
)
```

### 6. Analytics / ML Models

**Functions Available:**

```python
from notification_integration import notify_model_accuracy_low

# Notify about low model accuracy
notify_model_accuracy_low(
    model_name="priority_classifier",
    accuracy=0.78,
    threshold=0.85,
    metadata={"samples": 1000, "last_trained": "2026-01-10"}
)
```

### 7. Auto-Merge

**Functions Available:**

```python
from notification_integration import notify_auto_merge_failure

# Notify about auto-merge failure
notify_auto_merge_failure(
    pr_number=456,
    repository="org/repo",
    reason="CI checks failed",
    metadata={"failed_checks": ["lint", "test"]}
)
```

______________________________________________________________________

## Backward Compatibility

For systems that cannot be immediately migrated, the integration helper provides
backward compatibility:

```python
# Still works - routes through unified manager
from utils import send_notification

send_notification(
    "slack",
    "My message",
    title="Alert",
    priority="HIGH",
    source="custom-system",
    metadata={"key": "value"}
)
```

**Note:** This is deprecated. New code should use the specific `notify_*`
functions.

______________________________________________________________________

## Testing Integration

### Unit Testing

```python
from unittest.mock import patch
from notification_integration import notify_sla_breach

def test_sla_breach_notification():
    with patch('notification_integration.get_notification_manager') as mock_mgr:
        notify_sla_breach(
            item_type="issue",
            item_number="123",
            repository="test/repo",
            breach_type="response_time",
            threshold="15min",
            actual="45min",
            priority="P0"
        )

        # Verify notification was sent
        mock_mgr.return_value.send.assert_called_once()

        # Verify notification properties
        notification = mock_mgr.return_value.send.call_args[0][0]
        assert notification.priority == Priority.CRITICAL
        assert notification.source == "sla-monitor"
        assert "123" in notification.message
```

### Integration Testing

```bash
# Test SLA breach notification
python -c "
from notification_integration import notify_sla_breach
notify_sla_breach(
    item_type='issue',
    item_number='TEST-123',
    repository='test/repo',
    breach_type='response_time',
    threshold='15min',
    actual='45min',
    priority='P0'
)
"

# Check delivery logs
ls -la .github/notifications/delivery_log/
cat .github/notifications/delivery_log/NOTIF-*.json | tail -1
```

______________________________________________________________________

## Migration Checklist

### Phase 1: Preparation (Week 1)

- [ ] Review existing notification code in all systems
- [ ] Identify all notification entry points
- [ ] Document current notification patterns
- [ ] Set up test environment with notification manager
- [ ] Test notification delivery to all channels

### Phase 2: Integration (Week 2)

- [ ] **SLA Monitor**

  - [ ] Update to use `notify_sla_breach()`
  - [ ] Update to use `notify_sla_compliance()`
  - [ ] Test with real SLA data
  - [ ] Verify rate limiting works

- [ ] **Incident Response**

  - [ ] Update to use `notify_incident_created()`
  - [ ] Update to use `notify_incident_resolved()`
  - [ ] Test with test incidents
  - [ ] Verify PagerDuty integration

- [ ] **Validation Framework**

  - [ ] Update to use `notify_validation_failure()`
  - [ ] Update to use `notify_validation_success()`
  - [ ] Run validation suite
  - [ ] Verify deduplication

- [ ] **Self-Healing**

  - [ ] Update to use `notify_self_healing_success()`
  - [ ] Update to use `notify_self_healing_failure()`
  - [ ] Test with failed workflow
  - [ ] Verify escalation works

- [ ] **Maintenance Scheduler**

  - [ ] Update to use `notify_maintenance_scheduled()`
  - [ ] Update to use `notify_maintenance_complete()`
  - [ ] Test with scheduled task
  - [ ] Verify timing notifications

- [ ] **Analytics**

  - [ ] Update to use `notify_model_accuracy_low()`
  - [ ] Test with low-accuracy model
  - [ ] Verify threshold alerts

- [ ] **Auto-Merge**

  - [ ] Update to use `notify_auto_merge_failure()`
  - [ ] Test with failed merge
  - [ ] Verify notification routing

### Phase 3: Validation (Week 3)

- [ ] Run all systems end-to-end
- [ ] Monitor notification delivery rates
- [ ] Check for notification storms (should be prevented)
- [ ] Verify deduplication working
- [ ] Review delivery logs for errors
- [ ] Check Prometheus metrics
- [ ] Validate Slack/Email/PagerDuty delivery

### Phase 4: Optimization (Week 4)

- [ ] Fine-tune rate limits if needed
- [ ] Adjust deduplication windows
- [ ] Update message templates based on feedback
- [ ] Add custom channels if needed
- [ ] Document any issues encountered
- [ ] Train team on new system

______________________________________________________________________

## Troubleshooting

### Common Issues

**Problem:** Notifications not being sent

**Solutions:**

- Check environment variables are set
- Verify `.github/notifications.yml` exists and is valid
- Check notification manager logs
- Test with CLI:
  `python notification_manager.py --title "Test" --message "Test" --priority INFO`

**Problem:** Duplicate notifications

**Solutions:**

- Verify deduplication is enabled in config
- Check deduplication window is appropriate (default 5 minutes)
- Review notification source and title for uniqueness

**Problem:** Rate limiting too aggressive

**Solutions:**

- Increase rate limits in `.github/notifications.yml`:

  ```yaml
  rate_limiting:
    max_per_minute:
      slack: 20  # Increase from 10
  ```

**Problem:** Wrong channels receiving notifications

**Solutions:**

- Check priority routing in config
- Verify source-specific routing overrides
- Review priority mapping in integration functions

______________________________________________________________________

## Best Practices

### 1. Use Specific Functions

✅ **Good:**

```python
notify_sla_breach(item_type="issue", item_number="123", ...)
```

❌ **Avoid:**

```python
send_notification("slack", "SLA breach on issue 123")
```

### 2. Include Metadata

```python
notify_incident_created(
    incident_id="INC-001",
    severity="SEV-1",
    # ...
    metadata={
        "affected_services": ["api", "web"],
        "impact": "high",
        "estimated_users": 10000
    }
)
```

### 3. Handle Errors Gracefully

```python
try:
    notify_sla_breach(...)
except Exception as e:
    logger.error(f"Failed to send notification: {e}")
    # Continue processing - don't let notification failure break workflow
```

### 4. Test Locally First

```python
# Set up test config
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/TEST/WEBHOOK"

# Send test notification
python -c "from notification_integration import notify_sla_breach; ..."

# Check delivery log
cat .github/notifications/delivery_log/NOTIF-*.json | tail -1
```

______________________________________________________________________

## Support

- **Documentation**:
  - [Unified Notification System](../guides/UNIFIED_NOTIFICATION_SYSTEM.md)
  - [Week 9 Advanced Automation](WEEK_9_ADVANCED_AUTOMATION.md)
- **Code**:
  - `automation/scripts/notification_manager.py`
  - `automation/scripts/notification_integration.py`
- **Configuration**: `.github/notifications.yml`
- **Issues**: Open issue in repository

______________________________________________________________________

## Next Steps

1. Review this integration guide
1. Set up test environment
1. Migrate one system at a time
1. Validate each migration
1. Monitor metrics and adjust as needed

For questions or issues, contact the automation team or open an issue.

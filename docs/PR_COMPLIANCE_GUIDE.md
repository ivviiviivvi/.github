# PR Compliance Guide 🔍

A comprehensive guide to understanding and addressing pull request compliance checks for the ivi374forivi organization.

## Table of Contents

- [Overview](#overview)
- [Security Compliance](#security-compliance)
- [Code Quality Compliance](#code-quality-compliance)
- [Ticket Compliance](#ticket-compliance)
- [Codebase Context Compliance](#codebase-context-compliance)
- [Custom Compliance Rules](#custom-compliance-rules)
- [Compliance Status Legend](#compliance-status-legend)
- [Best Practices](#best-practices)

## Overview

All pull requests in the ivi374forivi organization are subject to automated compliance checks. These checks ensure code quality, security, maintainability, and adherence to organizational standards. This guide explains common compliance issues and how to address them.

## Security Compliance

### Unhandled Batch Processing Failures

**Issue**: Using `asyncio.gather(*tasks)` without error handling

**Risk Level**: ⚪ Requires Human Verification → 🔴 High Priority

**Description**: When processing multiple async tasks with `asyncio.gather()`, if any single task raises an exception, the entire batch fails and no results are returned. This can cause data loss or service disruption in production environments.

**Example of Non-Compliant Code**:
```python
tasks = [self.process_event(event, enrichments) for event in events]
return await asyncio.gather(*tasks)
```

**Remediation**:

**Option 1: Use `return_exceptions=True`**
```python
tasks = [self.process_event(event, enrichments) for event in events]
results = await asyncio.gather(*tasks, return_exceptions=True)

# Handle exceptions in results
processed = []
for i, result in enumerate(results):
    if isinstance(result, Exception):
        logger.error(f"Failed to process event {i}: {result}")
        # Handle failure appropriately (skip, retry, etc.)
    else:
        processed.append(result)
return processed
```

**Option 2: Individual Try-Catch Wrappers**
```python
async def safe_process_event(event, enrichments):
    try:
        return await self.process_event(event, enrichments)
    except Exception as e:
        logger.error(f"Failed to process event {event.id}: {e}")
        return None  # or a default/error value

tasks = [safe_process_event(event, enrichments) for event in events]
results = await asyncio.gather(*tasks)
return [r for r in results if r is not None]
```

**Option 3: Use `asyncio.TaskGroup` with exception handling (Python 3.11+)**
```python
try:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(self.process_event(event, enrichments)) 
                 for event in events]
    # All tasks completed successfully
    results = [task.result() for task in tasks]
except* Exception as eg:
    # Handle ExceptionGroup - TaskGroup raises all exceptions together
    logger.error(f"Multiple tasks failed: {eg}")
    # Process partial results from successful tasks only
    results = []
    for task in tasks:
        if task.done() and not task.cancelled():
            # Check for exception before calling result()
            if task.exception() is None:
                results.append(task.result())
            else:
                logger.warning(f"Task failed with: {task.exception()}")
```

### Input Validation and Sanitization

**Issue**: Missing validation for environment variables or user inputs

**Risk Level**: ⚪ Requires Human Verification → 🟡 Medium Priority

**Description**: Environment variables and external inputs should always be validated and sanitized before use to prevent security vulnerabilities.

**Example of Non-Compliant Code**:
```python
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # ...
)
```

**Remediation**:
```python
import re
from urllib.parse import urlparse

def validate_origin(origin: str) -> bool:
    """Validate that an origin is a valid URL"""
    try:
        result = urlparse(origin.strip())
        # Check scheme is http or https
        if result.scheme not in ('http', 'https'):
            return False
        # Check hostname exists
        if not result.netloc:
            return False
        # Reject wildcard origins unless explicitly supported
        if '*' in result.netloc:
            return False
        # Validate port if present
        if result.port is not None:
            if not (1 <= result.port <= 65535):
                return False
        # Check for invalid characters (no spaces or control/non-printable characters)
        if ' ' in origin or not origin.isprintable():
            return False
        return True
    except Exception:
        return False

# Validate and sanitize CORS origins
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
origins = [
    origin.strip() 
    for origin in raw_origins.split(",") 
    if validate_origin(origin)
]

if not origins:
    logger.warning("No valid CORS origins configured, using default")
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # ...
)
```

## Code Quality Compliance

### Meaningful Naming and Self-Documenting Code

**Issue**: Generic or single-letter variable names

**Risk Level**: ⚪ Requires Human Verification → 🟢 Low Priority

**Objective**: Ensure all identifiers clearly express their purpose and intent, making code self-documenting.

**Example of Non-Compliant Code**:
```python
events = [e for e in events if e.source == source]
```

**Remediation**:
```python
events = [event for event in events if event.source == source]
```

**Guidelines**:
- Use descriptive names that clearly indicate purpose
- Avoid single-letter variables except in very limited scopes (e.g., `i` in simple loops)
- For list comprehensions, use the singular form of the collection name
- Exception: Mathematical code where single letters are conventional (e.g., `x`, `y` for coordinates)

### Robust Error Handling and Edge Case Management

**Issue**: Missing boundary validation

**Risk Level**: ⚪ Requires Human Verification → 🟡 Medium Priority

**Objective**: Ensure comprehensive error handling that provides meaningful context and graceful degradation.

**Example of Non-Compliant Code**:
```python
def get_recent_events(
    self,
    limit: int = 10,
    source: Optional[EventSource] = None
) -> List[NormalizedEvent]:
    """Get recent normalized events"""
    events = self.normalized_events

    if source:
        events = [e for e in events if e.source == source]

    return list(reversed(events[-limit:]))
```

**Issues**:
- No validation for negative or zero `limit`
- No handling of empty `events` list
- Generic variable name `e`

**Remediation**:
```python
def get_recent_events(
    self,
    limit: int = 10,
    source: Optional[EventSource] = None
) -> List[NormalizedEvent]:
    """Get recent normalized events in reverse chronological order
    
    Args:
        limit: Maximum number of events to return (must be positive)
        source: Optional filter by event source
        
    Returns:
        List of recent normalized events in reverse chronological order
        
    Raises:
        ValueError: If limit is less than or equal to 0
    """
    # Validate inputs
    if limit <= 0:
        raise ValueError(f"limit must be positive, got {limit}")
    
    events = self.normalized_events
    
    # Handle empty events list
    if not events:
        return []

    # Filter by source if specified
    if source:
        events = [event for event in events if event.source == source]
        
    # Handle case where filtering resulted in no events
    if not events:
        return []

    # Events are appended chronologically, just slice the last N
    return list(reversed(events[-limit:]))
```

**Key Principles**:
1. **Validate all inputs** - Check for invalid values at function boundaries
2. **Handle empty collections** - Check before operations that assume non-empty
3. **Provide meaningful error messages** - Include context about what went wrong
4. **Document edge case behavior** - Use docstrings to clarify expectations
5. **Use type hints** - Make expected types explicit

## Ticket Compliance

**Issue**: No ticket/issue referenced in PR

**Risk Level**: ⚪ Requires Human Verification

**Requirement**: All pull requests should reference an associated issue or ticket for traceability.

**How to Comply**:

1. **Create an issue first**: Before starting work, create an issue describing the problem or feature
2. **Reference in PR**: Link the issue in your PR description using GitHub keywords:
   - `Fixes #123`
   - `Closes #123`
   - `Resolves #123`
   - `Relates to #123`

3. **PR Description Template**: Use the organization's PR template which includes a section for issue references

**Example PR Description**:
```markdown
## Description
Fixes #123

This PR adds error handling to the batch processing logic to prevent data loss.

## Changes
- Added `return_exceptions=True` to asyncio.gather
- Implemented exception logging and filtering
- Added unit tests for error scenarios
```

## Codebase Context Compliance

**Purpose**: Enable AI-powered code review tools to understand your codebase better

**Status**: This is an optional enhancement that improves automated code review quality

**How to Enable**: Follow the [RAG Context Enrichment Guide](https://qodo-merge-docs.qodo.ai/core-abilities/rag_context_enrichment/) to configure codebase context for your repository.

**Benefits**:
- More accurate duplicate code detection
- Better understanding of project-specific patterns
- Improved suggestions based on existing code

## Custom Compliance Rules

The organization enforces several custom compliance rules. Here are the key ones:

### ✅ Comprehensive Audit Trails

**Objective**: Create detailed and reliable records of critical system actions for security analysis and compliance.

**Requirements**:
- Log all authentication attempts (success and failure)
- Log all data access and modifications
- Include timestamps, user identifiers, and action context
- Use structured logging for easy parsing

**Example**:
```python
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def audit_log(action: str, user_id: str, resource: str, **kwargs):
    """Create a structured audit log entry"""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user_id": user_id,
        "resource": resource,
        **kwargs
    }
    logger.info(f"AUDIT: {json.dumps(entry)}")

# Usage
audit_log("data_access", user_id="user123", resource="customer_records", 
          record_count=5, query="SELECT * FROM customers LIMIT 5")
```

### ✅ Secure Error Handling

**Objective**: Prevent leakage of sensitive system information through error messages while providing sufficient detail for internal debugging.

**Requirements**:
- Never expose stack traces to end users
- Don't include sensitive data in error messages (passwords, tokens, internal paths)
- Log detailed errors internally
- Return generic messages to users

**Example**:
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def process_payment(payment_data: dict):
    try:
        # Process payment logic
        result = await payment_processor.charge(payment_data)
        return result
    except PaymentProcessorException as e:
        # Log detailed error internally
        logger.error(
            f"Payment processing failed: {e}",
            extra={
                "user_id": payment_data.get("user_id"),
                "amount": payment_data.get("amount"),
                "error_code": e.code
            }
        )
        # Return generic error to user
        raise HTTPException(
            status_code=400,
            detail="Payment processing failed. Please check your payment information."
        )
    except Exception as e:
        # Log unexpected errors with full context
        logger.exception("Unexpected error in payment processing")
        # Return very generic error to user
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )
```

### ✅ Secure Logging Practices

**Objective**: Ensure logs are useful for debugging and auditing without exposing sensitive information like PII, PHI, or cardholder data.

**Requirements**:
- Never log passwords, tokens, API keys, or credentials
- Redact or mask sensitive data (credit cards, SSNs, etc.)
- Don't log full user records containing PII
- Use log levels appropriately (DEBUG, INFO, WARNING, ERROR)

**Example**:
```python
import logging
import re

logger = logging.getLogger(__name__)

def redact_sensitive_data(data: str) -> str:
    """Redact sensitive information from logs"""
    # Redact credit card numbers (16-digit and 15-digit AmEx format)
    data = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 'XXXX-XXXX-XXXX-XXXX', data)  # 16-digit
    data = re.sub(r'\b\d{4}[\s-]?\d{6}[\s-]?\d{5}\b', 'XXXX-XXXXXX-XXXXX', data)  # 15-digit AmEx
    # Redact email addresses: mask local part but preserve domain for debugging
    data = re.sub(r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)\b', r'[EMAIL]@\2', data)
    # Redact SSN patterns
    data = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', data)
    return data

def safe_log_user_action(user_id: str, action: str, details: dict):
    """Log user action with sensitive data redacted"""
    # Create a copy to avoid modifying original
    safe_details = {
        k: redact_sensitive_data(str(v)) if isinstance(v, str) else v
        for k, v in details.items()
        if not re.search(r'(password|pass|token|api[_-]?key|secret|access[_-]?token)', k, re.IGNORECASE)
    }
    logger.info(f"User {user_id} performed {action}: {safe_details}")
```

## Compliance Status Legend

Understanding compliance check results:

| Symbol | Status | Meaning |
|--------|--------|---------|
| 🟢 | Fully Compliant | All checks passed, no action needed |
| 🟡 | Partially Compliant | Some issues found, improvements recommended |
| 🔴 | Not Compliant | Critical issues found, must be addressed |
| ⚪ | Requires Human Verification | Automated check needs manual review |
| 🏷️ | Compliance Label | Compliance category marker |

## Best Practices

### Before Submitting a PR

1. **Run Local Tests**: Ensure all tests pass locally
2. **Run Linters**: Fix any linting errors
3. **Self-Review**: Read through your changes as if you're reviewing someone else's code
4. **Check Compliance**: Review common compliance issues and ensure your code addresses them
5. **Update Documentation**: Update relevant docs for your changes
6. **Create/Reference Issue**: Ensure there's an issue tracking this work

### Responding to Compliance Checks

1. **Don't Ignore Warnings**: Even if marked as "Requires Human Verification", review carefully
2. **Understand the Issue**: Read the description and understand why it's flagged
3. **Apply Remediation**: Use the examples in this guide to fix issues
4. **Ask for Help**: If you're unsure, ask in PR comments or team chat
5. **Document Decisions**: If you decide a compliance check is a false positive, explain why in comments

### Writing Compliance-Friendly Code

1. **Defensive Programming**: Validate inputs, handle errors, check boundaries
2. **Clear Naming**: Use descriptive variable and function names
3. **Error Context**: Provide helpful error messages for debugging
4. **Security First**: Assume all external input is potentially malicious
5. **Document Assumptions**: Use docstrings and comments to explain non-obvious logic
6. **Test Edge Cases**: Write tests for boundary conditions and error scenarios

### Common Patterns to Avoid

❌ **Bare except clauses**:
```python
try:
    risky_operation()
except:  # Too broad!
    pass
```

✅ **Specific exception handling**:
```python
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except IOError as e:
    logger.error(f"IO error: {e}")
    return default_value
```

---

❌ **Unvalidated environment variables**:
```python
database_url = os.getenv("DATABASE_URL")
connect(database_url)  # What if it's not set?
```

✅ **Validated configuration**:
```python
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is required")
if not database_url.startswith(("postgresql://", "postgres://")):
    raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
connect(database_url)
```

---

❌ **No input validation**:
```python
def get_items(count: int):
    return items[-count:]  # What if count is negative? Or zero?
```

✅ **Validated inputs**:
```python
def get_items(count: int):
    if count <= 0:
        raise ValueError(f"count must be positive, got {count}")
    if count > 1000:
        raise ValueError(f"count too large (max 1000), got {count}")
    return items[-count:]
```

---

❌ **Logging sensitive data**:
```python
logger.info(f"User login: {username} with password {password}")
```

✅ **Safe logging**:
```python
logger.info(f"User login attempt: {username}")
```

## Resources

- [Organization Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Python Error Handling Best Practices](https://docs.python.org/3/tutorial/errors.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Qodo Merge Compliance Documentation](https://qodo-merge-docs.qodo.ai/tools/compliance/)

## Questions or Feedback

If you have questions about compliance checks or suggestions for improving this guide:

1. Open an issue in this repository
2. Tag with `documentation` and `compliance` labels
3. Reach out in the organization's communication channels

---

**Last Updated**: December 2025  
**Maintained by**: ivi374forivi Organization

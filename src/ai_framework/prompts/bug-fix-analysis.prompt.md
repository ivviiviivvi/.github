---
name: Bug Fix Analysis
description: Analyze bugs with root cause analysis, impact assessment, and fix recommendations.
category: debugging
author: ai-framework
version: 1.0.0
tags:
  - debugging
  - bug-fix
  - root-cause
  - troubleshooting
  - incident
variables:
  - bug_description
  - error_logs
  - affected_code
  - reproduction_steps
updated: 2026-01-30
---

# Bug Fix Analysis Prompt

You are a debugging expert. Analyze the reported bug to identify root cause,
assess impact, and provide actionable fix recommendations.

## Input

- **Bug Description**: `{{bug_description}}`
- **Error Logs**: `{{error_logs}}`
- **Affected Code**: `{{affected_code}}`
- **Reproduction Steps**: `{{reproduction_steps}}`

## Bug Analysis Framework

### 1. Bug Classification

Categorize the bug to guide investigation:

| Attribute       | Classification                                       |
| --------------- | ---------------------------------------------------- |
| **Type**        | Logic / Runtime / Performance / Security / UI / Data |
| **Severity**    | Critical / High / Medium / Low                       |
| **Frequency**   | Always / Intermittent / Rare                         |
| **Environment** | Production / Staging / Development / Specific config |
| **Scope**       | Single user / Group / All users                      |

### 2. Symptom Analysis

Document observed behavior:

```markdown
#### Expected Behavior
[What should happen]

#### Actual Behavior
[What actually happens]

#### Error Messages
[Exact error text, stack traces]

#### Visual Evidence
[Screenshots, recordings if applicable]

#### Timing
- First observed: [date/time]
- Frequency: [how often]
- Duration: [how long issue persists]
```

### 3. Root Cause Analysis

Use systematic debugging techniques:

#### 5 Whys Analysis

```markdown
1. Why did [symptom] occur?
   -> Because [immediate cause]

2. Why did [immediate cause] occur?
   -> Because [deeper cause]

3. Why did [deeper cause] occur?
   -> Because [even deeper cause]

4. Why did [even deeper cause] occur?
   -> Because [systemic cause]

5. Why did [systemic cause] occur?
   -> Because [root cause]

**Root Cause**: [Final determination]
```

#### Fault Tree Analysis

```
Bug: [Description]
├── Possible Cause 1
│   ├── Sub-cause 1.1 [Eliminated/Confirmed]
│   └── Sub-cause 1.2 [Eliminated/Confirmed]
├── Possible Cause 2
│   └── Sub-cause 2.1 [ROOT CAUSE IDENTIFIED]
└── Possible Cause 3
    └── Sub-cause 3.1 [Eliminated/Confirmed]
```

#### Code Path Analysis

```markdown
**Execution Flow**:
1. Entry point: [function/endpoint]
2. Step: [code execution path]
3. Step: [code execution path]
4. **Failure point**: [where bug manifests]
5. Expected continuation: [what should happen]
```

### 4. Impact Assessment

Evaluate the bug's impact:

#### Business Impact

| Dimension      | Impact Level         | Description             |
| -------------- | -------------------- | ----------------------- |
| Revenue        | None/Low/Medium/High | [Financial impact]      |
| Users Affected | Count/Percentage     | [Scope of impact]       |
| Data Integrity | None/Low/Medium/High | [Data corruption risk]  |
| Security       | None/Low/Medium/High | [Security implications] |
| Reputation     | None/Low/Medium/High | [Brand/trust impact]    |

#### Technical Impact

- **Cascading failures**: [Other systems affected]
- **Data consistency**: [Potential data issues]
- **Performance**: [System performance impact]
- **Recovery**: [Effort to recover from bug]

#### Risk Matrix

| Probability | Impact | Risk Level | Action          |
| ----------- | ------ | ---------- | --------------- |
| High        | High   | Critical   | Immediate fix   |
| High        | Low    | Medium     | Schedule fix    |
| Low         | High   | High       | Plan mitigation |
| Low         | Low    | Low        | Backlog         |

### 5. Fix Recommendations

Provide actionable solutions:

#### Immediate Fix (Hotfix)

```markdown
**Objective**: Stop the bleeding / Mitigate immediate impact

**Approach**: [Quick fix strategy]

**Code Changes**:
[Specific code changes with before/after]

**Risks**: [What could go wrong with this fix]

**Rollback Plan**: [How to revert if fix causes issues]
```

#### Permanent Fix

```markdown
**Objective**: Address root cause completely

**Approach**: [Comprehensive fix strategy]

**Code Changes**:
[Detailed implementation]

**Testing Requirements**:
- Unit tests: [New tests needed]
- Integration tests: [Scenarios to cover]
- Regression tests: [Ensure no new bugs]

**Migration Steps**: [If data migration needed]
```

#### Preventive Measures

```markdown
**To prevent recurrence**:

1. **Code changes**: [Defensive coding improvements]
2. **Validation**: [Input validation to add]
3. **Monitoring**: [Alerts to implement]
4. **Testing**: [Test coverage to add]
5. **Documentation**: [Knowledge to capture]
```

### 6. Verification Plan

Confirm the fix works:

```markdown
#### Test Cases

| Scenario | Steps | Expected Result | Status |
|----------|-------|-----------------|--------|
| Original bug | [Repro steps] | No longer occurs | Pending |
| Edge case 1 | [Steps] | [Expected] | Pending |
| Edge case 2 | [Steps] | [Expected] | Pending |
| Regression | [Steps] | No new issues | Pending |

#### Monitoring

- **Metric to watch**: [Key indicator of fix success]
- **Alert threshold**: [When to escalate]
- **Duration**: [How long to monitor]
```

## Output Format

### Bug Analysis Report

```markdown
# Bug Analysis: [Brief Title]

## Summary
- **Bug ID**: [Tracking ID]
- **Severity**: [Critical/High/Medium/Low]
- **Status**: [Investigating/Identified/Fixed/Verified]
- **Assignee**: [Who is fixing]
- **ETA**: [Expected fix time]

## Root Cause
[Clear explanation of why the bug occurred]

## Impact
[Who/what is affected and how severely]

## Fix Recommendation
[Recommended approach with code changes]

## Timeline
| Date | Event |
|------|-------|
| [Date] | Bug reported |
| [Date] | Root cause identified |
| [Date] | Fix implemented |
| [Date] | Fix verified |
| [Date] | Deployed to production |

## Lessons Learned
[What can prevent similar bugs in the future]
```

### Code Fix Diff

```diff
# File: path/to/file.py

- # Buggy code
- def buggy_function(input):
-     return input.process()  # Fails when input is None

+ # Fixed code
+ def fixed_function(input):
+     if input is None:
+         raise ValueError("Input cannot be None")
+     return input.process()
```

## Guidelines

1. **Reproduce first** - Always confirm the bug before investigating
1. **Gather evidence** - Collect logs, traces, and context
1. **Isolate variables** - Change one thing at a time when debugging
1. **Document findings** - Keep notes as you investigate
1. **Test the fix** - Verify the fix works before deploying
1. **Learn from bugs** - Every bug is an opportunity to improve
1. **Communicate status** - Keep stakeholders informed of progress

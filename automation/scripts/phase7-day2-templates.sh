#!/bin/bash
# Phase 7 Execution Script - Day 2: Template Validation
# Usage: bash phase7-day2-templates.sh

set -e

echo "🚀 Phase 7 Execution: Day 2 - Template Validation"
echo "================================================="
echo ""

# Template directory
TEMPLATE_DIR=".github/ISSUE_TEMPLATE"

if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "❌ Template directory not found: $TEMPLATE_DIR"
    exit 1
fi

echo "📋 Discovered Templates:"
echo ""
ls -1 "$TEMPLATE_DIR" | while read -r template; do
    echo "  - $template"
done
echo ""

TEMPLATE_COUNT=$(ls -1 "$TEMPLATE_DIR" | wc -l)
echo "Total templates: $TEMPLATE_COUNT"
echo ""

# Create validation report directory
mkdir -p docs/guides

echo "📝 Creating Issue Templates Usage Guide..."
echo ""

cat > docs/guides/issue-templates.md << 'EOF'
# Issue Templates Guide

> **Quick Reference:** How to use GitHub issue templates in this organization

## Overview

This repository provides **17 specialized issue templates** to streamline bug reports, feature requests, and other contributions. Using the right template ensures your issue contains the necessary information for quick triage and resolution.

## Available Templates

### 🐛 Bug Reports

#### `bug_report.yml` ⭐ **Recommended**
- **Purpose:** Report bugs with structured fields
- **Use when:** Something isn't working as expected
- **Fields:** Environment, steps to reproduce, expected vs actual behavior
- **Auto-labels:** `bug`

#### `bug_report.md` (Legacy)
- **Purpose:** Markdown-based bug report
- **Use when:** You prefer freeform markdown
- **Status:** Deprecated - use `bug_report.yml` instead

### ✨ Enhancements

#### `feature_request.yml` ⭐ **Recommended**
- **Purpose:** Request new features with business case
- **Use when:** You want new functionality
- **Fields:** Problem statement, proposed solution, alternatives
- **Auto-labels:** `enhancement`

#### `feature_request.md` (Legacy)
- **Purpose:** Markdown-based feature request
- **Status:** Deprecated - use `feature_request.yml` instead

### 🔧 Specialized Issues

#### `accessibility_issue.yml`
- **Purpose:** Report accessibility concerns
- **Use when:** WCAG compliance issues, screen reader problems
- **Fields:** WCAG criteria, user impact, severity
- **Auto-labels:** `accessibility`, `a11y`

#### `best-practices-review.yml`
- **Purpose:** Request code or process review
- **Use when:** Seeking feedback on implementation approach
- **Fields:** Area to review, specific concerns, context
- **Auto-labels:** `review`, `best-practices`

#### `community-health-check.yml`
- **Purpose:** Provide community feedback
- **Use when:** Suggesting improvements to community processes
- **Fields:** Health metrics, concerns, suggestions
- **Auto-labels:** `community`

#### `infrastructure.yml`
- **Purpose:** Report infrastructure/deployment issues
- **Use when:** CI/CD, deployment, or infrastructure problems
- **Fields:** Environment, affected services, logs
- **Auto-labels:** `infrastructure`, `devops`

#### `performance_issue.yml`
- **Purpose:** Report performance problems
- **Use when:** Slowness, memory leaks, inefficiency
- **Fields:** Baseline metrics, current metrics, profiling data
- **Auto-labels:** `performance`, `optimization`

#### `tech_debt.yml`
- **Purpose:** Track technical debt
- **Use when:** Code needs refactoring or modernization
- **Fields:** Current state, proposed improvements, impact
- **Auto-labels:** `tech-debt`, `refactoring`

#### `walkthrough-request.yml`
- **Purpose:** Request interactive demo or tutorial
- **Use when:** You want a guided walkthrough created
- **Fields:** Topic, target audience, format preferences
- **Auto-labels:** `walkthrough`, `documentation`

### 📚 Documentation

#### `documentation.yml`
- **Purpose:** Request documentation improvements
- **Use when:** Docs are missing, unclear, or outdated
- **Fields:** Affected docs, what's missing, suggested improvements
- **Auto-labels:** `documentation`

#### `documentation.md` (Legacy)
- **Purpose:** Markdown-based documentation request
- **Status:** Deprecated - use `documentation.yml` instead

### 🎯 General

#### `task.yml`
- **Purpose:** Track general tasks
- **Use when:** Work item that doesn't fit other categories
- **Fields:** Description, acceptance criteria, dependencies
- **Auto-labels:** `task`

#### `question.md`
- **Purpose:** Ask questions
- **Use when:** You need help or clarification
- **Note:** Consider using GitHub Discussions instead
- **Auto-labels:** `question`

#### `custom.md`
- **Purpose:** Custom issue not fitting other templates
- **Use when:** None of the above templates apply
- **Note:** This is a fallback - try to use a specific template

## Template Selection Guide

```mermaid
graph TD
    A[New Issue] --> B{What type?}
    B -->|Something broken| C[bug_report.yml]
    B -->|Want new feature| D[feature_request.yml]
    B -->|Performance problem| E[performance_issue.yml]
    B -->|Accessibility concern| F[accessibility_issue.yml]
    B -->|Infrastructure issue| G[infrastructure.yml]
    B -->|Docs need update| H[documentation.yml]
    B -->|Tech debt| I[tech_debt.yml]
    B -->|Request walkthrough| J[walkthrough-request.yml]
    B -->|Need review| K[best-practices-review.yml]
    B -->|Community feedback| L[community-health-check.yml]
    B -->|Task tracking| M[task.yml]
    B -->|General question| N[question.md or Discussions]
    B -->|None fit| O[custom.md]
```

## Best Practices

### DO ✅

- **Search first** - Check if your issue already exists
- **Use the right template** - Choose the most specific template
- **Fill all required fields** - Helps with quick triage
- **Provide context** - Include relevant details
- **Add labels** - Help categorize your issue (auto-applied by templates)
- **Link related issues** - Use `#issue-number` to reference

### DON'T ❌

- **Skip required fields** - Makes triage difficult
- **Create duplicates** - Search before creating
- **Mix multiple issues** - Create separate issues instead
- **Use vague titles** - Be specific and descriptive
- **Post sensitive data** - Remove secrets, PII, etc.

## For Template Maintainers

### Template Structure

All YAML templates follow this structure:

```yaml
name: Template Name
description: Brief description
title: "[CATEGORY] "
labels: ["label1", "label2"]
body:
  - type: markdown | input | textarea | dropdown | checkboxes
    attributes:
      label: Field Label
      description: Help text
      placeholder: Example value (optional)
    validations:
      required: true | false
```

### Validation Rules

- **Required fields:** User must fill before submitting
- **Dropdown fields:** Limit choices to predefined options
- **Checkbox fields:** Allow multiple selections
- **Input fields:** Single-line text
- **Textarea fields:** Multi-line text with optional placeholder

### Auto-applied Labels

Labels specified in template frontmatter are automatically applied when the issue is created. This ensures consistent categorization.

### Updating Templates

When updating templates:

1. **Test changes** - Create test issues to verify functionality
2. **Update this guide** - Keep documentation in sync
3. **Announce changes** - Notify users of significant updates
4. **Version templates** - Consider adding version comments

## Related Resources

- **GitHub Discussions:** For questions and general discussion
- **Contributing Guide:** See `CONTRIBUTING.md`
- **Issue Triage Process:** See `docs/guides/issue-triage.md`
- **Label Guide:** See `docs/LABELS.md`

## Support

**Need help choosing a template?**
- Post in [GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions)
- Ask in the #help channel (if applicable)
- Use the `question.md` template

**Found a problem with a template?**
- Use `bug_report.yml` to report template issues
- Tag with `template-issue` label

---

**Last Updated:** 2026-01-15  
**Maintained by:** Documentation Team
EOF

echo "✅ Created docs/guides/issue-templates.md"
echo ""

echo "📝 Creating Template Validation Report Template..."
echo ""

cat > docs/guides/issue-template-validation-report.md << 'EOF'
# Issue Template Validation Report

**Date:** 2026-01-15  
**Validator:** [To be completed]  
**Repository:** ivviiviivvi/.github  
**Templates Tested:** 17

---

## Executive Summary

**Status:** ⏳ Validation In Progress

This report documents the validation of all GitHub issue templates to ensure they:
- Load correctly in the GitHub UI
- Apply labels automatically
- Validate required fields
- Render all form elements properly

---

## Validation Methodology

Each template was tested using the following procedure:

1. Navigate to GitHub Issues → New Issue
2. Select template from list
3. Verify template loads without errors
4. Check all fields render correctly
5. Test validation rules (required fields, format checks)
6. Create test issue (if applicable)
7. Verify labels auto-apply
8. Close test issue after verification

---

## Template Validation Results

### ✅ YAML-based Templates (Modern)

| Template | Status | Labels | Validation | Notes |
|----------|--------|--------|------------|-------|
| `accessibility_issue.yml` | ⏳ Pending | - | - | - |
| `best-practices-review.yml` | ⏳ Pending | - | - | - |
| `bug_report.yml` | ⏳ Pending | - | - | - |
| `community-health-check.yml` | ⏳ Pending | - | - | - |
| `documentation.yml` | ⏳ Pending | - | - | - |
| `feature_request.yml` | ⏳ Pending | - | - | - |
| `infrastructure.yml` | ⏳ Pending | - | - | - |
| `performance_issue.yml` | ⏳ Pending | - | - | - |
| `task.yml` | ⏳ Pending | - | - | - |
| `tech_debt.yml` | ⏳ Pending | - | - | - |
| `walkthrough-request.yml` | ⏳ Pending | - | - | - |

### 📄 Markdown-based Templates (Legacy)

| Template | Status | Notes |
|----------|--------|-------|
| `bug_report.md` | ⏳ Pending | Legacy - recommend migration to YAML |
| `custom.md` | ⏳ Pending | Fallback template |
| `documentation.md` | ⏳ Pending | Legacy - recommend migration to YAML |
| `feature_request.md` | ⏳ Pending | Legacy - recommend migration to YAML |
| `question.md` | ⏳ Pending | Consider redirecting to Discussions |

### ⚙️ Configuration

| File | Status | Notes |
|------|--------|-------|
| `config.yml` | ⏳ Pending | Contact links and blank issue settings |

---

## Detailed Findings

### Critical Issues (Blocking)

None identified yet.

### Medium Priority Issues

To be completed during validation.

### Low Priority Issues / Enhancements

To be completed during validation.

---

## Configuration Review

### config.yml Analysis

```yaml
# To be completed - paste config.yml contents here
```

**Findings:**
- To be completed

---

## Recommendations

### Immediate Actions

To be completed after validation.

### Short-term Improvements

1. **Consolidate duplicate templates**
   - Deprecate markdown versions of templates that have YAML equivalents
   - Add deprecation notices to legacy templates

2. **Standardize naming**
   - Consider consistent naming pattern (e.g., `{type}_{purpose}.yml`)

3. **Add version comments**
   - Include version/date in template comments for tracking

### Long-term Enhancements

1. **Create template analytics**
   - Track which templates are used most
   - Identify unused templates for removal

2. **Template testing automation**
   - Implement automated validation in CI/CD
   - Catch template errors before deployment

3. **User feedback mechanism**
   - Add feedback link in templates
   - Gather user suggestions for improvements

---

## Test Evidence

### Sample Test Issues Created

To be completed - list test issue numbers here.

### Screenshots

To be completed - attach screenshots of problematic templates (if any).

---

## Sign-off

**Validation Completed By:** _________________  
**Date:** _________________  

**Review Approved By:** _________________  
**Date:** _________________  

**Status:** 
- [ ] Validation Complete
- [ ] All critical issues resolved
- [ ] Documentation updated
- [ ] Phase 7.2 marked complete

---

## Appendix

### A. Template Testing Checklist

Use this checklist for each template:

- [ ] Template appears in "New Issue" dropdown
- [ ] Template loads without errors
- [ ] Title field renders correctly
- [ ] All body fields render correctly
- [ ] Required field validation works
- [ ] Optional fields are truly optional
- [ ] Dropdowns show correct options
- [ ] Checkboxes allow proper selection
- [ ] Labels auto-apply on submission
- [ ] Created issue has correct format
- [ ] No JavaScript errors in console

### B. Template File List

```bash
# Generated via: ls -1 .github/ISSUE_TEMPLATE/
accessibility_issue.yml
best-practices-review.yml
bug_report.md
bug_report.yml
community-health-check.yml
config.yml
custom.md
documentation.md
documentation.yml
feature_request.md
feature_request.yml
infrastructure.yml
performance_issue.yml
question.md
task.yml
tech_debt.yml
walkthrough-request.yml
```

---

**Next Review Date:** 2026-07-15 (6 months)
EOF

echo "✅ Created docs/guides/issue-template-validation-report.md"
echo ""

echo "📋 Template Validation Instructions:"
echo ""
echo "Manual steps required:"
echo "  1. Open https://github.com/ivviiviivvi/.github/issues/new/choose"
echo "  2. Test each template by:"
echo "     - Selecting it from the list"
echo "     - Verifying all fields render"
echo "     - Testing required field validation"
echo "     - Creating a test issue (mark as [TEST])"
echo "     - Verifying labels auto-apply"
echo "     - Closing test issue"
echo "  3. Document results in:"
echo "     - docs/guides/issue-template-validation-report.md"
echo "  4. Update validation status for each template"
echo ""
echo "Estimated time: 2-3 hours (10-15 min per template)"
echo ""

echo "✅ Template validation framework created!"
echo ""

echo "📊 Summary:"
echo "- ✅ Created issue templates usage guide"
echo "- ✅ Created validation report template"
echo "- ⏳ Manual validation required (see instructions above)"
echo ""
echo "After validation:"
echo "  1. Complete validation report"
echo "  2. Update CLEANUP_ROADMAP.md Phase 7.2"
echo "  3. Mark Phase 7 complete"
echo "  4. Commit all changes"
echo ""

echo "🎉 Day 2 Framework Complete!"
echo ""
echo "Ready for manual template validation."

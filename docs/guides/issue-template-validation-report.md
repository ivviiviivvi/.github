# Issue Template Validation Report

**Date:** 2026-01-15\
**Validator:** \[To be completed\]\
**Repository:**
{{ORG_NAME}}/.github\
**Templates Tested:** 17

______________________________________________________________________

## Executive Summary

**Status:** ⏳ Validation In Progress

This report documents the validation of all GitHub issue templates to ensure
they:

- Load correctly in the GitHub UI
- Apply labels automatically
- Validate required fields
- Render all form elements properly

______________________________________________________________________

## Validation Methodology

Each template was tested using the following procedure:

1. Navigate to GitHub Issues → New Issue
1. Select template from list
1. Verify template loads without errors
1. Check all fields render correctly
1. Test validation rules (required fields, format checks)
1. Create test issue (if applicable)
1. Verify labels auto-apply
1. Close test issue after verification

______________________________________________________________________

## Template Validation Results

### ✅ YAML-based Templates (Modern)

| Template                     | Status     | Labels | Validation | Notes |
| ---------------------------- | ---------- | ------ | ---------- | ----- |
| `accessibility_issue.yml`    | ⏳ Pending | -      | -          | -     |
| `best-practices-review.yml`  | ⏳ Pending | -      | -          | -     |
| `bug_report.yml`             | ⏳ Pending | -      | -          | -     |
| `community-health-check.yml` | ⏳ Pending | -      | -          | -     |
| `documentation.yml`          | ⏳ Pending | -      | -          | -     |
| `feature_request.yml`        | ⏳ Pending | -      | -          | -     |
| `infrastructure.yml`         | ⏳ Pending | -      | -          | -     |
| `performance_issue.yml`      | ⏳ Pending | -      | -          | -     |
| `task.yml`                   | ⏳ Pending | -      | -          | -     |
| `tech_debt.yml`              | ⏳ Pending | -      | -          | -     |
| `walkthrough-request.yml`    | ⏳ Pending | -      | -          | -     |

### 📄 Markdown-based Templates (Legacy)

| Template             | Status     | Notes                                |
| -------------------- | ---------- | ------------------------------------ |
| `bug_report.md`      | ⏳ Pending | Legacy - recommend migration to YAML |
| `custom.md`          | ⏳ Pending | Fallback template                    |
| `documentation.md`   | ⏳ Pending | Legacy - recommend migration to YAML |
| `feature_request.md` | ⏳ Pending | Legacy - recommend migration to YAML |
| `question.md`        | ⏳ Pending | Consider redirecting to Discussions  |

### ⚙️ Configuration

| File         | Status     | Notes                                  |
| ------------ | ---------- | -------------------------------------- |
| `config.yml` | ⏳ Pending | Contact links and blank issue settings |

______________________________________________________________________

## Detailed Findings

### Critical Issues (Blocking)

None identified yet.

### Medium Priority Issues

To be completed during validation.

### Low Priority Issues / Enhancements

To be completed during validation.

______________________________________________________________________

## Configuration Review

### config.yml Analysis

```yaml
# To be completed - paste config.yml contents here
```

**Findings:**

- To be completed

______________________________________________________________________

## Recommendations

### Immediate Actions

To be completed after validation.

### Short-term Improvements

1. **Consolidate duplicate templates**

   - Deprecate markdown versions of templates that have YAML equivalents
   - Add deprecation notices to legacy templates

1. **Standardize naming**

   - Consider consistent naming pattern (e.g., `{type}_{purpose}.yml`)

1. **Add version comments**

   - Include version/date in template comments for tracking

### Long-term Enhancements

1. **Create template analytics**

   - Track which templates are used most
   - Identify unused templates for removal

1. **Template testing automation**

   - Implement automated validation in CI/CD
   - Catch template errors before deployment

1. **User feedback mechanism**

   - Add feedback link in templates
   - Gather user suggestions for improvements

______________________________________________________________________

## Test Evidence

### Sample Test Issues Created

To be completed - list test issue numbers here.

### Screenshots

To be completed - attach screenshots of problematic templates (if any).

______________________________________________________________________

## Sign-off

**Validation Completed By:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Date:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Review Approved By:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Date:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Status:**

- [ ] Validation Complete
- [ ] All critical issues resolved
- [ ] Documentation updated
- [ ] Phase 7.2 marked complete

______________________________________________________________________

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

______________________________________________________________________

**Next Review Date:** 2026-07-15 (6 months)

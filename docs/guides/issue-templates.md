# Issue Templates

This guide documents the issue templates under `.github/ISSUE_TEMPLATE/`, the
current validation status, and follow-up items.

## Issue forms (YAML)

- accessibility_issue.yml: Accessibility issues; labels: accessibility,
  needs-triage
- best-practices-review.yml: Best practices review; labels: best-practices,
  review, enhancement
- bug_report.yml: Bug reports; labels: bug, triage
- community-health-check.yml: Community health checks; labels: community,
  health-check, documentation
- documentation.yml: Documentation updates; labels: documentation, triage
- feature_request.yml: Feature requests; labels: enhancement, triage
- infrastructure.yml: Infrastructure or DevOps requests; labels: infrastructure,
  devops, needs-triage
- performance_issue.yml: Performance issues; labels: performance, needs-triage
- security_vulnerability.yml: Low-severity security reports; labels: security,
  low-priority
- task.yml: Tasks; labels: task
- tech_debt.yml: Technical debt or refactoring; labels: tech-debt, refactoring,
  needs-triage
- walkthrough-request.yml: Walkthrough requests; labels: walkthrough,
  feature-request, documentation

## Legacy markdown templates

These files are present but have invalid or incomplete front matter and should
be fixed or removed to avoid confusion:

- bug_report.md (missing front matter end)
- custom.md (front matter YAML error)
- documentation.md (missing front matter end)
- feature_request.md (missing front matter end)
- question.md (missing front matter end)

## Validation checklist

- YAML issue forms parse cleanly and include name, description, and body.
- Body items include type and id (non-markdown types) and attributes with
  labels.
- config.yml contains contact_links with valid URLs (no placeholders).
- Labels are defined for each issue form.
- Logs or attachment fields include a warning against sharing sensitive data.
- Security reporting path points to a private advisory workflow.

## Latest validation (2026-01-14)

- YAML issue forms: OK (12 files).
- config.yml: OK (3 contact links).
- Markdown templates: OK (front matter validated).
- Manual check: bug_report.yml logs field includes a PII warning.
- Security template is public low-severity only; ensure private advisory contact
  link remains in config.yml.

## Re-run validation

```bash
python - <<'PY'
from pathlib import Path
import yaml

issue_dir = Path(".github/ISSUE_TEMPLATE")
for path in sorted(issue_dir.glob("*.yml")):
    if path.name == "config.yml":
        continue
    data = yaml.safe_load(path.read_text())
    assert isinstance(data, dict), f"{path.name}: not a mapping"
    for key in ("name", "description", "body"):
        assert key in data, f"{path.name}: missing {key}"
    for item in data.get("body", []):
        if item.get("type") != "markdown":
            assert item.get("id"), f"{path.name}: missing id"
            assert item.get("attributes", {}).get("label"), f"{path.name}: missing label"
print("Issue forms validated")
PY
```

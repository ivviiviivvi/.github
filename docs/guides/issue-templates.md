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
- task.yml: Tasks; labels: task
- tech_debt.yml: Technical debt or refactoring; labels: tech-debt, refactoring,
  needs-triage
- walkthrough-request.yml: Walkthrough requests; labels: walkthrough,
  feature-request, documentation

## Legacy markdown templates

These files are legacy markdown templates that duplicate the issue forms. The
front matter is valid; consider removing them if you want to use only forms:

- bug_report.md
- custom.md
- documentation.md
- feature_request.md
- question.md

## Validation checklist

- YAML issue forms parse cleanly and include name, description, and body.
- Body items include type and id (non-markdown types) and attributes with
  labels.
- config.yml contains contact_links with valid URLs (no placeholders).
- Labels are defined for each issue form.
- Template labels exist in `.github/labels.yml`.
- Template labels exist in the repository label set.
- Logs or attachment fields include a warning against sharing sensitive data.
- Security reporting path points to a private advisory workflow.
- Template links point to valid repository documents.

## Latest validation (2026-01-14)

- YAML issue forms: OK (11 files).
- config.yml: OK (3 contact links).
- Markdown templates: OK (front matter validated).
- Manual check: bug_report.yml logs field includes a PII warning.
- Links updated to canonical docs and correct org URLs.
- Labels synced in `.github/labels.yml` for all templates.
- Repo labels synced to match `.github/labels.yml`.
- Created and closed template validation issues #230-240; labels matched
  expected template label sets.
- Security template removed; config.yml directs reporters to private advisories.

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
labels = set()
labels_data = yaml.safe_load(Path(".github/labels.yml").read_text())
items = labels_data.get("labels") if isinstance(labels_data, dict) else labels_data
if isinstance(items, list):
    for entry in items:
        if isinstance(entry, dict) and "name" in entry:
            labels.add(entry["name"])
missing = []
for path in sorted(issue_dir.glob("*.yml")):
    if path.name == "config.yml":
        continue
    data = yaml.safe_load(path.read_text())
    lbls = data.get("labels")
    if isinstance(lbls, list):
        missing.extend([lbl for lbl in lbls if lbl not in labels])
if missing:
    raise SystemExit(f"Missing labels: {sorted(set(missing))}")
print("Issue forms and labels validated")
PY
```

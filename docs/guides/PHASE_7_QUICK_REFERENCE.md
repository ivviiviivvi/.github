# Phase 7 Quick Reference

> **⚡ Fast execution guide for completing Phase 7 of CLEANUP_ROADMAP**

---

## One-Command Execution

```bash
# Complete Phase 7 in sequence
bash automation/scripts/phase7-day1-triage.sh && \
bash automation/scripts/phase7-day2-templates.sh
```

Then follow Day 2 manual validation steps.

---

## Individual Steps

### Day 1: Issue Triage (30 min)

```bash
bash automation/scripts/phase7-day1-triage.sh
```

**What happens:**

- Closes issues #152, #151, #150 (completed in other phases)
- Defers issues #153, #149 (strategic planning Q1-Q2 2026)
- Triages issues #242, #241 (assigns teams/priority)

### Day 2: Template Validation (2-3 hours)

```bash
bash automation/scripts/phase7-day2-templates.sh
```

**What happens:**

- Creates `docs/guides/issue-templates.md` (usage guide)
- Creates `docs/guides/issue-template-validation-report.md` (template)
- Shows manual testing instructions

**Manual steps:**

1. Visit <https://github.com/ivviiviivvi/.github/issues/new/choose>
2. Test each of 17 templates
3. Update validation report with results

---

## Mark Complete

After Day 2 validation:

```bash
# Edit CLEANUP_ROADMAP.md
# - Check all Phase 7 checkboxes
# - Add "✅ 100% COMPLETE" to Phase 7 header
# - Update Executive Summary to 100%

# Commit changes
git add .
git commit -m "feat: complete Phase 7 - Issue Triage & Template Validation

- Closed 3 completed issues (#152, #151, #150)
- Deferred 2 strategic issues (#153, #149)
- Triaged 2 new issues (#242, #241)
- Validated all 17 templates
- CLEANUP_ROADMAP 100% complete

Closes #152, #151, #150"

git push origin main
```

---

## Troubleshooting

### "gh: command not found"

```bash
# Install GitHub CLI
# macOS: brew install gh
# Linux: see https://github.com/cli/cli#installation

# Then authenticate
gh auth login
```

### "Permission denied"

```bash
# Make scripts executable
chmod +x automation/scripts/phase7-day*.sh
```

### "Issue not found"

Issues may have been closed already. Check:

```bash
gh issue view 152 --json state,title
```

If closed, skip that issue in the script.

---

## Files Created

- `docs/guides/PHASE_7_COMPLETION_PLAN.md` - Detailed strategy
- `docs/guides/PHASE_7_EXECUTION_SUMMARY.md` - Comprehensive guide
- `docs/guides/issue-templates.md` - Template usage guide
- `docs/guides/issue-template-validation-report.md` - Test results
- `automation/scripts/phase7-day1-triage.sh` - Day 1 automation
- `automation/scripts/phase7-day2-templates.sh` - Day 2 setup

---

## Success Checklist

- [ ] Day 1 script executed successfully
- [ ] All 7 issues have status updates
- [ ] Day 2 templates documentation created
- [ ] All 17 templates tested manually
- [ ] Validation report completed
- [ ] CLEANUP_ROADMAP.md Phase 7 marked complete
- [ ] Changes committed and pushed

---

## Time Estimates

| Task | Time |
|------|------|
| Day 1 triage script | 5 min |
| Day 2 template script | 5 min |
| Manual template testing | 2-3 hours |
| Documentation | 30 min |
| Final commit | 10 min |
| **Total** | **3-4 hours** |

---

## Next Steps After Completion

1. Create GitHub Discussion announcing 100% completion
2. Schedule retrospective meeting
3. Archive CLEANUP_ROADMAP.md
4. Create epics for deferred issues (#242, #241, #153, #149)

---

**Need Help?**

- Review: `docs/guides/PHASE_7_COMPLETION_PLAN.md`
- Detailed: `docs/guides/PHASE_7_EXECUTION_SUMMARY.md`
- Discuss: GitHub Discussions

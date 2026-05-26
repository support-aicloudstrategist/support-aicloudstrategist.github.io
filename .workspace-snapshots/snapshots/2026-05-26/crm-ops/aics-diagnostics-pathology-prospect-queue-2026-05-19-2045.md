# AICS Diagnostics / Pathology Prospect Queue Refresh — 2026-05-19 20:45 IST

**Scope:** AICloudStrategist only  
**Concrete action completed:** Converted the diagnostics/pathology blocker into a verified starter prospect queue with template mapping and approval-readiness status.  
**Guardrail:** No customer contact, no public post, no website deploy, no spend, no credential or sensitive-system changes.

## Output created

- CSV queue: `reports/crm-ops/aics-diagnostics-pathology-prospect-queue-2026-05-19-2045.csv`
- Queue IDs: `AICS-DIAG-20260519-001` to `AICS-DIAG-20260519-004`

## Queue summary

| Status | Count | IDs |
|---|---:|---|
| Verified email-ready for Raj approval pack only | 2 | AICS-DIAG-20260519-001, AICS-DIAG-20260519-003 |
| Needs one final page-level verification before approval email | 1 | AICS-DIAG-20260519-002 |
| Not email-ready; phone-only/no verified email found | 1 | AICS-DIAG-20260519-004 |

## Prospect notes

### AICS-DIAG-20260519-001 — The Diagnostic Clinical Laboratory
- **Website:** https://thediagnosticonline.co.in/
- **Public email:** diagnostic.official@gmail.com
- **Fit signals:** online booking, home blood collection, report delivery within 24 hours, phone/website workflow.
- **Template:** Template 1 — report delivery and enquiry leakage check.
- **Fit score:** 86/100.
- **Next safe action:** Render Template 1 to Raj only for approval before any customer email.

### AICS-DIAG-20260519-002 — Dr. Subir Dutta's Scientific Clinical Laboratory
- **Website:** https://scrl.org.in/
- **Public email found in official-domain search result:** scientificlab86@gmail.com
- **Fit signals:** independent lab, public contact presence, book/test workflow signals.
- **Template:** Template 2 — owner visibility and backup readiness check.
- **Fit score:** 78/100.
- **Next safe action:** Do one final direct page-level verification before adding to Raj approval email.

### AICS-DIAG-20260519-003 — Ashok Laboratory Clinical Testing Centre Private Limited
- **Website:** https://www.ashoklab.com/
- **Public email:** ashoklab86@gmail.com
- **Fit signals:** official contact page, home collection form, public mobile and address.
- **Template:** Template 1 — report delivery and enquiry leakage check.
- **Fit score:** 84/100.
- **Next safe action:** Render Template 1 to Raj only for approval before any customer email.

### AICS-DIAG-20260519-004 — Dr Lal PathLabs Kolkata — Tangra/EM Bypass
- **Website:** https://drlalpathlabskolkata.com/
- **Public email:** not found in verified source.
- **Fit signals:** diagnostic centre, booking phone, tests/packages, report-flow language.
- **Template:** Template 2 if verified email appears.
- **Fit score:** 74/100.
- **Next safe action:** Do not contact. Continue email discovery or exclude from email campaign.

## Approval-pack readiness

This queue is **not a send approval yet**. Per `aics-simple-approval-sop.md`, the next approval-ready asset should first tell Raj:

1. **Identified recipients:** 2 email-ready now, 1 pending final verification, 1 excluded until email verified.
2. **Templates proposed:** Template 1 for The Diagnostic + Ashok Lab; Template 2 for SCRL after final verification.
3. **Exact rendered emails:** send only to Raj personal approval route, not customers.

## Recommended next action

Create the Raj-only rendered diagnostics/pathology approval pack for the two verified email-ready recipients, while separately verifying SCRL's contact page before inclusion. No customer email should be sent until Raj replies APPROVE.

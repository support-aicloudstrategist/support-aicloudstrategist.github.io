# Incident: DIAG-LAB-A internal approval card sent to customers

Time noticed: 2026-05-20 20:23 IST
Reported by: Raj
Severity: High — internal approval workflow exposed in customer-facing email visual.

## What happened
DIAG-LAB-A emails were sent to:
- V-Care Path Lab <vcarelab2015@gmail.com>
- G1 Pathology Lab <gkhvpune@gmail.com>

The HTML used `cid:aicsScorecard`, and the inline attachment was mistakenly set to:
`reports/template-category-approvals/2026-05-20-diagnostics-template-a/template-category-diag-lab-a-card-v2.png`

That image was a founder approval card, not a customer-facing scorecard.

## Exposed text in image
Confirmed via image review:
- “Template + customer-category approval”
- “APPROVAL 1 OF MASTER MAP”
- “Once approved…”
- “Approval keyword: APPROVE TEMPLATE DIAG-LAB-A”
- “Changes/Rejection: CHANGES / REJECT”

## Root cause
- Founder approval asset and customer visual asset lived in the same directory and similar naming flow.
- Send command manually attached the founder approval card as the customer `aicsScorecard` inline asset.
- Guard checked HTML text but not inline image text or attachment filename semantics.
- No final rendered customer-email QA was performed after personalization and inline attachment binding.

## Immediate containment
- Stop all outreach/customer sends.
- Do not send corrections externally until Raj approves.
- Quarantine the bad asset from any customer-send path.

## Required permanent fix
- Add preflight that blocks customer/prospect/marketing sends if attachment filenames or paths contain internal terms: approval, founder, review-card, template-category, approve, reject, changes.
- Add OCR/vision/manual QA requirement for every customer-facing image before send.
- Separate directories: `customer-assets/` vs `approval-assets/`; customer sends may only attach from `customer-assets/`.
- Generate a final preview manifest showing: recipient, subject, HTML file, all attachments, inline CIDs, and visual QA status.

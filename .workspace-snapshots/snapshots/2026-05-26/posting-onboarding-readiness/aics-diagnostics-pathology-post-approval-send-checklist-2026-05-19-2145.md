# AICS diagnostics/pathology post-approval send checklist — 2026-05-19 21:45 IST

## Safe action completed in this run
Prepared an execution-ready internal send manifest and checklist for the diagnostics/pathology campaign so the team can move immediately if Raj approves, without reselecting recipients or risking the wrong sender. No customer/prospect was contacted.

## Approval gate
- Current approval status: **Pending Raj approval**.
- Approval artifact already sent: rendered production approval email from `contact@aicloudstrategist.com` to Raj personal email at 2026-05-19 21:31 IST.
- Approval scope: exactly the 3 verified email-ready recipients in the manifest below, using their mapped Template 1/2 copy.
- Do not send if Raj replies `CHANGES` or `REJECT`, or if any recipient/template/sender changes.

## Ready internal manifest
- Manifest CSV: `reports/posting-onboarding-readiness/aics-diagnostics-pathology-post-approval-send-manifest-2026-05-19-2145.csv`
- Source CRM queue: `reports/crm-ops/aics-diagnostics-pathology-prospect-queue-2026-05-19-2100.csv`
- Queue IDs ready after approval: AICS-DIAG-20260519-001, AICS-DIAG-20260519-002, AICS-DIAG-20260519-003
- Excluded lead remains excluded: `AICS-DIAG-20260519-004` — no verified public email.

## Send execution checklist after APPROVE only
1. Re-open Raj's approval reply and confirm it says exactly `APPROVE` for diagnostics/pathology email outreach.
2. Confirm sender is `contact@aicloudstrategist.com` only. Never use `support@aicloudstrategist.com` for prospect/customer outreach.
3. Send individually, not as a batch/CC/BCC blast, using `aics_mail_send_guard.py`.
4. Send only to these queue IDs:
   - `AICS-DIAG-20260519-001` — The Diagnostic Clinical Laboratory — diagnostic.official@gmail.com — Template 1
   - `AICS-DIAG-20260519-002` — Dr. Subir Dutta's Scientific Clinical Laboratory — scientificlab86@gmail.com — Template 2
   - `AICS-DIAG-20260519-003` — Ashok Laboratory Clinical Testing Centre Private Limited — ashoklab86@gmail.com — Template 1
5. Do not contact `AICS-DIAG-20260519-004` unless a verified public email is later found and Raj approves the updated scope.
6. Save one guarded-send evidence JSON per outbound send under `reports/outbound-mail/`.
7. Refresh `reports/approval-dashboard/aics-approval-dashboard-current.*` with sent evidence and next reply-monitoring action.
8. Monitor replies only; do not make claims, book calls, or send follow-ups beyond the approved copy without a new approval if the content changes materially.

## Operator note
This is an internal readiness asset, not a customer-facing approval request. It reduces the next-step risk once approval arrives.

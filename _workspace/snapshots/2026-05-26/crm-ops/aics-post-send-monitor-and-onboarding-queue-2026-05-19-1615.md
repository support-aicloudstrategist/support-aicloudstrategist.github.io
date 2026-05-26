# AICS Post-Send Monitor + Onboarding Queue — 2026-05-19 16:15 IST

**Scope:** AICloudStrategist only  
**Freshest input reviewed:** `reports/approval-packs/premium-email-templates-20260519/customer-send-report-20260519-1606.json` and `reports/approval-packs/approval-decisions.jsonl`  
**Safe action completed:** converted the 16:07 approved-and-sent premium email execution into a CRM monitoring/onboarding readiness queue. No customer contact, public posting, calls, spending, website deployment, or sensitive/external system change was performed.

## Current state after Raj approval 5213

| Queue ID | Prospect | Channel | Latest approved action | Status | Guardrail |
|---|---|---|---|---|---|
| `AICS-HC-FOLLOWUP-20260519-NKPC-1607` | NKPC Kidney Clinic | Email | Template 1 — Business Flow Check | Sent 2026-05-19 16:07 IST to `nationalkidney99@gmail.com` | Monitor replies only; no second follow-up, WhatsApp, call, attachment, or alternate channel without fresh exact approval. |
| `AICS-HC-FOLLOWUP-20260519-PARK-1607` | Park Clinic Kolkata | Email | Template 1 — Business Flow Check | Sent 2026-05-19 16:07 IST to `info@parkclinickolkata.com` | Monitor replies only; no call to listed numbers or second follow-up without fresh exact approval. |
| `AICS-PROP-20260519-AASTHA-DENTAL-1100` | Aastha Dental Care | WhatsApp/call candidate | One-decision approval card already prepared | Still pending / not contacted | Do not send while WhatsApp route is scan-required; do not switch to phone unless Raj explicitly approves the phone opener. |
| `AICS-HC-WEB-20260519-1045` | Healthcare landing + FAQ | Website | Drafted and approved for discovery/website/PDF use only where applicable | Implementation/publish still pending | Prepare QA/deploy checklist only; no public deploy without Raj approval. |

## Reply triage rules for the two sent emails

Use these rules if a reply appears in `support@aicloudstrategist.com` / `contact@aicloudstrategist.com`:

| Reply intent | Internal classification | Safe response posture | Approval needed before sending? |
|---|---|---|---|
| Interested / asks for details | `positive_reply_needs_discovery_booking` | Draft a short scheduling reply with 2–3 time windows and scorecard agenda. | Yes, unless Raj has given a standing reply approval for that exact template. |
| Asks price / proposal | `commercial_interest_needs_offer_scope` | Prepare a one-page mini-scope: 20-min free check → paid 30-day roadmap option. | Yes. |
| Not relevant / stop / unsubscribe | `opt_out` | Do not contact again; record suppression. | No outbound response unless legally/operationally necessary. |
| Auto-reply / mailbox issue | `delivery_hygiene` | Record evidence; do not try another channel. | Yes for any alternate channel. |
| Complaint / sensitive healthcare concern | `risk_review` | Escalate internally to Raj; no direct debate. | Yes. |

## Discovery-call readiness pack if either prospect replies positively

### 20-minute Healthcare Business Flow Check agenda

1. **2 minutes — Context**  
   Confirm role, location, and whether the issue is patient enquiries, appointment follow-up, report/payment communication, or website trust.

2. **5 minutes — Enquiry flow**  
   Map where new enquiries come from: website, Google listing, phone, WhatsApp, referral, walk-in, email.

3. **5 minutes — Follow-up workflow**  
   Check how missed calls, unanswered WhatsApp messages, pending reports/payments, reminders, and no-shows are tracked.

4. **4 minutes — Trust and hygiene basics**  
   Review website/contact clarity, backup/access hygiene, owner/admin visibility, and obvious operational risks.

5. **4 minutes — Next step**  
   Offer a simple scorecard summary and a 30-day improvement roadmap if there is fit.

### Conservative positioning script

> This is a practical business workflow review, not a medical, legal, cybersecurity, or compliance certification. The goal is to identify where enquiries, appointments, follow-ups, and basic digital trust signals can be improved quickly and safely.

### Required intake fields before a call is booked

- Business name and city
- Replying person’s name and role
- Preferred contact method for the discovery call
- Primary workflow pain: missed enquiries / appointment follow-up / website trust / reports-payments / backups-access / other
- Consent to receive the scorecard summary by email
- Any explicit opt-out or contact restriction

## Next approval-ready item to prepare

If Raj wants momentum without waiting for replies, the next safe item is a **website publish approval card** for the healthcare landing/FAQ or trust-page diff. It should show only:

1. the page/channel to publish,
2. the final production copy or screenshot/checklist,
3. the exact approval choices: `APPROVE / CHANGES / REJECT`.

## Evidence links

- Send evidence: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/premium-email-templates-20260519/customer-send-report-20260519-1606.json`
- Decision log: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/approval-decisions.jsonl`
- Current CRM board before this refresh: `/home/OpenClaw/.openclaw/workspace/reports/crm-ops/aics-crm-ops-follow-up-board-2026-05-19-1600.md`

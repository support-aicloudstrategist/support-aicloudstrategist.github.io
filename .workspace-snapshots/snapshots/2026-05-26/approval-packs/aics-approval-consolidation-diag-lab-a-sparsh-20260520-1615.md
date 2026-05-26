# AICS Approval Consolidation — DIAG-LAB-A + Sparsh WhatsApp Demo

Created: 2026-05-20 16:15 IST  
Scope: safe internal approval-ready consolidation only. No customer/prospect contact, public post, WhatsApp send, call, spend, repo publish, credential work, or destructive action performed.

## SOP verification completed

- Operating system reviewed: `/home/OpenClaw/.openclaw/workspace/aics-autopilot-operating-system.md`.
- Outreach master SOP reviewed: `/home/OpenClaw/.openclaw/workspace/aics-outreach-master-sop.md`.
- Simple approval SOP reviewed: `/home/OpenClaw/.openclaw/workspace/aics-simple-approval-sop.md`.
- Live contact source checked: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 16:15 IST.
- Current public contacts confirmed:
  - Website: `https://aicloudstrategist.com/`
  - Free review: `https://aicloudstrategist.com/free-business-review`
  - Primary outreach/customer email: `contact@aicloudstrategist.com`
  - Support email/reference only: `support@aicloudstrategist.com`
  - WhatsApp Business: `+91 87963 02608`
  - WhatsApp URL: `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
  - Voice line: `+91 80654 80898`
  - Default signature: Anushka Bhattacharya, Director, AICloudStrategist
- Banned old WhatsApp number check for this new artifact: not used.

---

## Founder review card 1 — Diagnostics lab email template/category

Approval required for diagnostics/pathology email outreach.

Identified targets ready for this template: 2 verified email-ready diagnostics/pathology labs from today’s queue:

1. V-Care Path Lab, Pune
2. G1 Pathology Lab, Pune

Channel: Email from `contact@aicloudstrategist.com`  
Template: DIAG-LAB-A — diagnostics enquiry/report request leakage workflow check

If approved, Jarvis may use this same production email format only for verified independent diagnostics/pathology labs with public business emails. Sends remain individual, not bulk, and any material template/category change needs fresh approval.

Approval reply options:

APPROVE TEMPLATE DIAG-LAB-A  
CHANGES  
REJECT

Production email preview:

Subject: Are lab enquiries or report requests slipping between WhatsApp, calls and staff follow-ups?

Hello Team Example Diagnostics & Pathology Lab,

I’m Anushka from AICloudStrategist. We help small healthcare and service businesses make their existing website, WhatsApp, calls and internal workflows work together more reliably — without forcing a heavy software migration.

For diagnostic centres, the common leakage points are usually simple but expensive: missed enquiries, report-delivery questions, callbacks and staff handovers.

What I can check from the outside:

- Home collection or appointment enquiries followed up faster.
- Report-download/report-delivery questions tracked clearly.
- One visible status board for pending enquiries, callbacks and handovers.

If useful, I can do a short 20-minute Digital Readiness Review for Example Diagnostics & Pathology Lab and share 3–5 practical fixes you can implement even if you do not hire us.

Request the free review: https://aicloudstrategist.com/free-business-review  
WhatsApp: +91 87963 02608

Would a quick call this week be worth scheduling?

Regards,  
Anushka Bhattacharya  
Director, AICloudStrategist  
Website: https://aicloudstrategist.com/  
Free review: https://aicloudstrategist.com/free-business-review  
Email: contact@aicloudstrategist.com  
Support: support@aicloudstrategist.com  
WhatsApp: +91 87963 02608  
Voice line: +91 80654 80898

If this is not relevant, reply “not interested” and I will not follow up.

---

## Founder review card 2 — Sparsh WhatsApp customer reply demo

Approval required for Sparsh WhatsApp customer reply.

Target: Sparsh Hair Skin Dermatology Clinic, Prayagraj  
Context: existing inbound WhatsApp reply: “Ok”  
Channel: WhatsApp customer reply  
Action after approval: send only the already prepared demo image plus the exact caption below.

Approval reply options:

APPROVE  
CHANGES  
REJECT

Exact WhatsApp caption:

```text
Namaste Sparsh Hair Skin Dermatology Clinic 👋

Thanks for confirming.

I’m sharing a small *sample WhatsApp enquiry board demo* for a dermatology / skin / hair clinic.

The demo shows how patient enquiries from WhatsApp, missed calls, website forms, or Instagram can be organised into one simple board:

✅ New enquiries
✅ Appointment requests
✅ Staff callback follow-ups
✅ Owner daily summary
✅ No patient medical data required for the first demo

This is not a heavy CRM replacement. It is a practical follow-up board to reduce missed enquiries and make staff handover cleaner.

If useful, we can show a 10–15 minute walkthrough for Sparsh Clinic and adapt the sample flow to your actual enquiry process.

— Anushka Bhattacharya
Director, AICloudStrategist
Website: https://aicloudstrategist.com
WhatsApp: +91 87963 02608
Voice line: +91 80654 80898
Email: contact@aicloudstrategist.com
```

---

## Internal execution controls

### DIAG-LAB-A

- Status: pending Raj approval.
- Approval asset source: `reports/template-category-approvals/2026-05-20-diagnostics-template-a/raj-approval-email-diag-lab-a.html`.
- Template master map: `reports/template-category-approvals/template-category-master-map.json`.
- Queue IDs eligible after approval: `AICS-HLQ-20260520-0830` slots 2 and 4 only unless more verified diagnostics/pathology email prospects are added.
- Guardrail: Raj personal rendered approval email is required before treating a response as executable approval.
- After approval: send only via `aics_mail_send_guard.py` from `contact@aicloudstrategist.com`, one recipient at a time; update approval dashboard and send report.

### Sparsh WhatsApp

- Status: pending exact Raj approval.
- Demo image/caption evidence: `reports/sparsh-whatsapp-board-demo-20260519/approval-card-v2-with-video-backup.md`.
- Guardrail: send only the approved PNG + exact caption to the existing Sparsh WhatsApp conversation. Do not send optional video unless separately approved.

## Next safe action

Route one clean approval item at a time when approval routing is active, starting with DIAG-LAB-A if the goal is to unlock verified diagnostics email sends, or Sparsh if the goal is to respond to the warm inbound WhatsApp conversation.

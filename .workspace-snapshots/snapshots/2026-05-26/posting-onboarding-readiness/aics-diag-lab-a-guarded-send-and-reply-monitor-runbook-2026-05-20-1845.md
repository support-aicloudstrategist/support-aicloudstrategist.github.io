# DIAG-LAB-A guarded-send + reply-monitor runbook — 2026-05-20 18:45 IST

Status: **internal readiness artifact only**. No customer/prospect email, WhatsApp, call, public post, website publish, paid action, credential change, or destructive action was performed.

## SOP gate refreshed

- Operating system and Outreach Master SOP were read for this run.
- Live contact source checked: `https://aicloudstrategist.com/contact-channels.json` at `2026-05-20T13:15:32.886Z`.
- Current WhatsApp Business: **+91 87963 02608**.
- Current voice line: **+91 80654 80898**.
- Customer/prospect sender: **contact@aicloudstrategist.com** only.
- Support reference: **support@aicloudstrategist.com** only; never sender for prospecting.
- Public-facing signature: **Anushka Bhattacharya, Director, AICloudStrategist**.
- Email must remain premium HTML and pass `aics_mail_send_guard.py` before any customer send.

## Approval gate

Do **not** send anything unless Raj explicitly replies:

`APPROVE TEMPLATE DIAG-LAB-A`

If approval wording, channel, recipients, sender, or template changes materially, stop and request fresh approval.

## Immediate post-approval execution sequence

1. Re-check each prospect source page before sending if approval arrives after 19:15 IST or if any source looks stale.
2. Confirm the public business email still appears on the source page.
3. Personalize **BUSINESS_NAME only** in the approved DIAG-LAB-A premium HTML.
4. Send one recipient at a time through `aics_mail_send_guard.py` from `contact@aicloudstrategist.com`.
5. Use no CC, no BCC, no bulk mode, no patient/report data request, and no claims about medical/compliance outcomes.
6. Save guarded-send evidence under `reports/outbound-mail/`.
7. Update approval dashboard + CRM/reply-monitor board immediately after each send.
8. Monitor replies for 48 hours; classify only. Any follow-up must be freshly drafted and Raj-approved before sending.

## Ready queue

| # | Queue ID | Business | Public source | Public email | Current state | Post-approval action |
|---:|---|---|---|---|---|---|
| 1 | `DIAG-LAB-A-POSTAPPROVAL-20260520-1815-001` | V-Care Path Lab | https://www.vcarepathlab.com/ | `vcarelab2015@gmail.com` | Waiting for `APPROVE TEMPLATE DIAG-LAB-A` | Reverify source → guarded individual send → 48h monitor |
| 2 | `DIAG-LAB-A-POSTAPPROVAL-20260520-1815-002` | G1 Pathology Lab | https://g1pathlab.in/contact-us/ | `gkhvpune@gmail.com` | Waiting for `APPROVE TEMPLATE DIAG-LAB-A` | Reverify source → guarded individual send → 48h monitor |

## Reply handling matrix

| Reply type | Safe internal action | External action |
|---|---|---|
| Interested / asks for call | Draft short scheduling reply with current WhatsApp/voice line and Anushka signature | Requires Raj approval before send |
| Asks for details/pricing | Draft premium HTML/plain fallback response package | Requires Raj approval before send |
| Not interested / unsubscribe | Mark do-not-follow-up; no response unless Raj asks | No send |
| Bounce / invalid email | Mark invalid; do not search alternate contact in the same run without fresh verification | No send |
| Ambiguous / vendor / unrelated | Classify and prepare internal note | No send without Raj approval |

## Linked artifacts

- Source queue: `/home/OpenClaw/.openclaw/workspace/reports/posting-onboarding-readiness/aics-diag-lab-a-reverified-post-approval-queue-2026-05-20-1815.csv`
- Reply-monitor CSV: `/home/OpenClaw/.openclaw/workspace/reports/posting-onboarding-readiness/aics-diag-lab-a-reply-monitor-board-2026-05-20-1845.csv`
- Machine-readable runbook: `/home/OpenClaw/.openclaw/workspace/reports/posting-onboarding-readiness/aics-diag-lab-a-guarded-send-and-reply-monitor-runbook-2026-05-20-1845.json`
- Production HTML template: `/home/OpenClaw/.openclaw/workspace/reports/template-category-approvals/2026-05-20-diagnostics-template-a/diag-lab-a-production-template.html`
- Founder card: `/home/OpenClaw/.openclaw/workspace/reports/template-category-approvals/2026-05-20-diagnostics-template-a/founder-review-card-diag-lab-a-20260520-1630.md`

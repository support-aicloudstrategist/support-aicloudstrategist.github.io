# AICS Sparsh WhatsApp Demo — Post-Approval Send Checklist

Date: 2026-05-19 22:15 IST
Status: Approval-ready; **do not send to customer until Raj approves exact image + caption**.

## Target
- Business: Sparsh Hair Skin Dermatology Clinic, Prayagraj
- Channel: WhatsApp reply
- Trigger: inbound reply `Ok`
- Target count: 1 WhatsApp conversation

## Asset to send after approval
- Demo image: `reports/sparsh-whatsapp-board-demo-20260519/sparsh-whatsapp-board-demo.png`
- Final caption: `reports/sparsh-whatsapp-board-demo-20260519/sparsh-whatsapp-reply-caption.txt`
- Founder approval card: `reports/sparsh-whatsapp-board-demo-20260519/approval-card.md`

## Mandatory SOP verification
- [x] Live contact source checked: `https://aicloudstrategist.com/contact-channels.json` at 2026-05-19 22:15 IST.
- [x] WhatsApp Business number in caption: `+91 87963 02608`.
- [x] Voice line in caption: `+91 80654 80898`.
- [x] Primary public email in caption: `contact@aicloudstrategist.com`.
- [x] Signature uses Anushka Bhattacharya, Director, AICloudStrategist.
- [x] Message is not plain-text-only customer experience: image + formatted WhatsApp caption required.
- [x] Healthcare/privacy boundary included: no patient medical data required for first demo.
- [x] No customer send, public post, call, spend, or sensitive system change performed in this run.

## Execution gate
Only after Raj replies `APPROVE` to the exact card/image/caption:
1. Send the PNG demo image first or with caption, depending on WhatsApp tooling support.
2. Send exactly the approved caption without changing contact details or offer terms.
3. Log send evidence in `reports/outbound-whatsapp/` or the current WhatsApp agent evidence path.
4. Refresh approval dashboard and AICS-Ops outcome.

## If Raj requests changes
Revise image/caption, re-run SOP checks, and request approval again before any customer send.

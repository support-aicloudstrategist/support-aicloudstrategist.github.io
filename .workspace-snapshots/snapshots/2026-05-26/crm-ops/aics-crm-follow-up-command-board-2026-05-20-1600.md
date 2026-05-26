# AICS CRM/follow-up command board — 2026-05-20 16:00 IST

Status: CRM/reply evidence refresh and blocker-resolution board. No customer/prospect contact, WhatsApp send, call, public post, website publish, ad spend, credential change, contract action, credential work, or destructive action performed.

## SOP/contact verification

Source of truth checked live this run: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 16:00 IST.

Current production contacts confirmed:
- Website: `https://aicloudstrategist.com/`
- Free review: `https://aicloudstrategist.com/free-business-review`
- Primary outreach/customer email: `contact@aicloudstrategist.com`
- Support reference only: `support@aicloudstrategist.com`
- WhatsApp Business: `+91 87963 02608`
- WhatsApp URL: `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
- Voice line: `+91 80654 80898`
- Default public-facing identity: Anushka Bhattacharya, Director, AICloudStrategist.

## Mailbox/reply evidence checked

- Ran `aics_mail_operator.py --dry-run` only; no mailbox state change was intentionally performed.
- `support@aicloudstrategist.com`: 0 unread.
- `contact@aicloudstrategist.com`: 1 unread internal approval reply from Raj (`gupta082013@gmail.com`) received 2026-05-20 15:34 IST / 10:04 UTC.
- Subject: `Re: APPROVAL REQUIRED: AI Cloud follow-up email draft for 2026-05-20`.
- Raj response body: `Approved`.

## Decision taken this run

The approval was **not executed** because the underlying approval email is an older MotorInc follow-up draft that does not meet the current AICS Outreach Master SOP for customer/prospect sends:

1. It lacks the current WhatsApp `+91 87963 02608` and voice line `+91 80654 80898`.
2. It does not use the default public-facing Anushka Bhattacharya, Director signature.
3. It is not the current premium HTML template standard with full contact/CTA/footer resources.
4. The target recipient needs fresh public/source verification before any follow-up send.
5. The approval predates/sits outside the strict current exact-send SOP gate for this recipient and asset.

Result: **blocked unsafe execution instead of sending a non-compliant prospect follow-up.** This converts a latent risk into a clear approval/verification task.

## Queue advanced now

| Priority | Segment/item | Current state | Earliest safe next action | Approval gate |
|---:|---|---|---|---|
| 1 | MotorInc follow-up approval reply from Raj | Raj replied `Approved` to an older approval draft; send blocked by current SOP non-compliance and target re-verification need | Rebuild as a current SOP-compliant premium HTML follow-up only after target email/source is verified; then send rendered production item to Raj personal approval first | Fresh exact approval required for rebuilt item before any external send |
| 2 | Dental DENTAL-A — Smilex Dental Implant & Aligner Centers | Sent 2026-05-20 15:43 IST from `contact@` | Monitor replies only until 2026-05-22 15:43 IST; then draft premium HTML follow-up for Raj approval if no reply | Fresh Raj approval required before any follow-up send unless covered by later approved reusable follow-up template/category |
| 3 | Dental DENTAL-A — Dr Kadu's Orthodontic & Dental Clinic | Sent 2026-05-20 15:43 IST from `contact@` | Monitor replies only until 2026-05-22 15:43 IST; then draft premium HTML follow-up for Raj approval if no reply | Fresh Raj approval required before any follow-up send unless covered by later approved reusable follow-up template/category |
| 4 | DIAG-LAB-A template/category approval | Production template and card ready; status `pending_raj_approval` in master map | Present clean founder review card when approval routing is active. No sends until approved | `APPROVE TEMPLATE DIAG-LAB-A` or explicit approval required |
| 5 | Diagnostics alternate 2 fresh sends — Subir + Ashok | Sent 2026-05-20 14:35 IST from `contact@` | Monitor replies only until 2026-05-22 14:35 IST; then draft premium HTML follow-up for Raj approval if no reply | Fresh Raj approval required before follow-up send |
| 6 | The Diagnostic Clinical Laboratory correction | Duplicate avoided; correction pack remains prepared/pending | Keep correction pending. If Raj approves exact correction, send only via guarded `contact@` | `APPROVE CORRECTION` / CHANGES / REJECT needed |
| 7 | Sparsh WhatsApp customer reply demo | Customer has inbound “Ok”; approval card and creative exist; no external send performed | If Raj approves, send exact approved PNG + caption to existing Sparsh WhatsApp conversation | Exact WhatsApp demo approval required |
| 8 | Website clinic/dental resource page | Approval-ready page + hub card; no publish/edit | Send/await founder review before repo edit, staging, or publish | `APPROVE CLINIC DENTAL LEAKAGE PAGE` required |
| 9 | Free Review trust/conversion polish | Approval-ready implementation package; no publish/edit | Send/await founder review before applying diff or publishing | `APPROVE FREE REVIEW TRUST POLISH` required |

## MotorInc follow-up rebuild requirements

Before any MotorInc follow-up can be sent:

- Verify the target and email from a credible public source or authoritative prior CRM record.
- Rebuild the message as premium HTML from `contact@aicloudstrategist.com`.
- Use Anushka Bhattacharya, Director, AICloudStrategist signature.
- Include current WhatsApp `+91 87963 02608`, voice line `+91 80654 80898`, website, free review link, and support reference.
- Avoid unsupported claims and keep CTA to a free practical review.
- Send the full rendered production item to Raj personal approval route first; do not rely on the older `Approved` reply for execution.

## Blocker recorded

- MotorInc follow-up: blocked pending fresh target verification + SOP-compliant rebuild + fresh exact approval.
- Dental/diagnostics sends: reply monitoring only; no follow-up until 48-hour windows and fresh approvals.
- Public website/WhatsApp/social actions: still gated by exact Raj approval.

## Next safe action

If no approval arrives, continue with one safe internal workstream: create a SOP-compliant MotorInc follow-up rebuild pack after verifying the recipient from a credible source, or consolidate DIAG-LAB-A into a clean founder review card without sending externally.

# AICS CRM/follow-up command board — 2026-05-20 15:45 IST

Status: Internal CRM/follow-up queue refresh after the DENTAL-A approved sends. No customer/prospect contact, WhatsApp send, call, public post, website publish, ad spend, credential change, contract action, or destructive action performed in this run.

## SOP/contact verification

Source of truth checked live this run: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 15:45 IST.

Current production contacts confirmed:
- Website: `https://aicloudstrategist.com/`
- Free review: `https://aicloudstrategist.com/free-business-review`
- Primary outreach/customer email: `contact@aicloudstrategist.com`
- Support reference only: `support@aicloudstrategist.com`
- WhatsApp Business: `+91 87963 02608`
- WhatsApp URL: `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
- Voice line: `+91 80654 80898`
- Default public-facing identity: Anushka Bhattacharya, Director, AICloudStrategist.

## Freshest AICS outputs reviewed

- `reports/template-category-approvals/2026-05-20-dental-template-a/send-report.md` — DENTAL-A approved by Raj and sent to 2 dental prospects at 15:43 IST.
- `reports/template-category-approvals/template-category-master-map.json` — DENTAL-A approved; DIAG-LAB-A still pending Raj approval.
- `reports/outbound-mail/guarded-send-20260520-154356.json` and `reports/outbound-mail/guarded-send-20260520-154358.json` — individual guarded dental sends from `contact@aicloudstrategist.com`.
- `reports/crm-ops/aics-crm-follow-up-command-board-2026-05-20-1530.md` — prior CRM baseline before dental approval.

## Queue advanced now

| Priority | Segment/item | Current state | Earliest safe next action | Approval gate |
|---:|---|---|---|---|
| 1 | Dental DENTAL-A — Smilex Dental Implant & Aligner Centers | Sent 2026-05-20 15:43 IST from `contact@`; evidence `reports/outbound-mail/guarded-send-20260520-154356.json` | Monitor replies only until 2026-05-22 15:43 IST. If no reply after 48h, draft premium HTML follow-up and send rendered item to Raj personal approval first. | Fresh Raj approval required before any follow-up send unless covered by a later approved reusable follow-up template/category. |
| 2 | Dental DENTAL-A — Dr Kadu's Orthodontic & Dental Clinic | Sent 2026-05-20 15:43 IST from `contact@`; evidence `reports/outbound-mail/guarded-send-20260520-154358.json` | Monitor replies only until 2026-05-22 15:43 IST. If no reply after 48h, draft premium HTML follow-up and send rendered item to Raj personal approval first. | Fresh Raj approval required before any follow-up send unless covered by a later approved reusable follow-up template/category. |
| 3 | DIAG-LAB-A template/category approval | Production template and card ready; status `pending_raj_approval` in master map | Consolidate and present clean founder review card if approval window is active. No sends until approved. | `APPROVE TEMPLATE DIAG-LAB-A` or explicit approval required. |
| 4 | Diagnostics alternate 2 fresh sends — Subir + Ashok | Sent 2026-05-20 14:35 IST from `contact@`; evidence in diagnostics send report | Monitor replies only until 2026-05-22 14:35 IST. If no reply after 48h, draft premium HTML follow-up and route to Raj approval first. | Fresh Raj approval required before follow-up send. |
| 5 | The Diagnostic Clinical Laboratory correction | Duplicate avoided; correction pack remains prepared/pending | Keep correction pending. If Raj approves exact correction, send only via guarded `contact@`. | `APPROVE CORRECTION` / CHANGES / REJECT needed. |
| 6 | Sparsh WhatsApp customer reply demo | Customer has inbound “Ok”; approval card and creative exist; no external send performed | If Raj approves, send exact approved PNG + caption to existing Sparsh WhatsApp conversation. Optional video remains separate approval. | Exact WhatsApp demo approval required. |
| 7 | Website clinic/dental resource page | Approval-ready internal page + hub card; QA-only staging checklist completed | Send/await founder review before any repo edit, staging, or publish. If approved, implement and QA. | `APPROVE CLINIC DENTAL LEAKAGE PAGE` required. |
| 8 | Free Review trust/conversion polish | Approval-ready implementation package; QA-only checklist completed | Send/await founder review before applying diff or publishing. | `APPROVE FREE REVIEW TRUST POLISH` required. |
| 9 | Aesthetic clinic WhatsApp visual + caption | 2 phone/WhatsApp-only prospects; creative/captions ready; no prospect contact | Send exact PNG + captions to Raj personal approval route before any WhatsApp send. | APPROVE / CHANGES / REJECT required. |

## Decision rules refreshed

1. DENTAL-A now has template/category approval for future verified matching prospects, but the two recipients sent today remain on reply-monitoring only until 2026-05-22 15:43 IST.
2. Do not send dental follow-ups, WhatsApp messages, calls, public posts, website edits, or correction emails without exact approval for that next action.
3. DIAG-LAB-A is the freshest safe unfinished template/category approval item; it can be consolidated into a clean founder review card but must not be used for sends until Raj approves.
4. All future customer/prospect emails must stay premium HTML, from `contact@aicloudstrategist.com`, with current WhatsApp `+91 87963 02608`, voice line `+91 80654 80898`, and Anushka Bhattacharya Director identity.

## Recommended next safe action

At the next continuation slot, either:
1. consolidate the DIAG-LAB-A template/category approval into a short founder review card, or
2. refresh inbox/reply evidence for `contact@` and `support@` before the 16:00 CRM slot.

Do not send any prospect/customer follow-up before approval and/or the 48-hour follow-up windows.
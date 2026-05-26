# AICS CRM / Follow-up Board — 2026-05-19 22:30 IST

Status: internal board advanced; no customer/prospect/public action taken.

## SOP gate checked for customer-facing queues
- Live contact source checked: `https://aicloudstrategist.com/contact-channels.json` at 22:30 IST.
- Current WhatsApp: `+91 87963 02608`.
- Current voice line: `+91 80654 80898`.
- Primary customer/prospect sender: `contact@aicloudstrategist.com`.
- Default public signature: Anushka Bhattacharya, Director, AICloudStrategist.
- Guardrail: any prospect/customer send remains blocked until Raj approves the exact rendered item/action.

## Active lanes

### 1) Pending founder approval — highest priority
| Lane | Target/count | Artifact | Approval needed | Safe next action |
|---|---:|---|---|---|
| WhatsApp customer reply demo | 1 conversation: Sparsh Hair Skin Dermatology Clinic, Prayagraj | `reports/sparsh-whatsapp-board-demo-20260519/sparsh-whatsapp-board-demo.png` + `sparsh-whatsapp-reply-caption.txt` | Raj approval of exact image + caption | If APPROVE, send only approved image + caption; if CHANGES/REJECT, do not contact customer. |
| Diagnostics/pathology premium email outreach | 3 verified email-ready labs | `reports/approval-packs/aics-diagnostics-pathology-raj-email-approval-pack-2026-05-19-2100.html` + manifest | Raj approval of rendered email already sent to personal email at 21:31 IST | If APPROVE, execute manifest only via `aics_mail_send_guard.py` from `contact@aicloudstrategist.com`. |
| Website About page polish | 1 public website page | local diff in `repos/support-aicloudstrategist.github.io/about.html` | Raj approval to publish website diff | If APPROVE, publish and QA; otherwise revise/hold. |

### 2) Blocked / do-not-send lanes
| Lane | Blocker | Current safe stance | Next unblock action |
|---|---|---|---|
| The Diagnostic Clinical Laboratory correction | Earlier customer email used old WhatsApp number and Rajiv personal name | No correction sent without Raj approval | Prepare exact correction email only if Raj asks/approves. |
| Dr Lal PathLabs Kolkata local listing | Phone-only; no verified public email | Excluded from email campaign | Continue email discovery later or keep excluded. |
| Healthcare WhatsApp outreach | WhatsApp route/approval experience not production-ready | No customer WhatsApp send | Use approved formatted WhatsApp style only after Raj approval. |
| LinkedIn company post | Company page/admin session unavailable | No LinkedIn posting | Fix brand access/session. |
| X post | Compose redirects to login | No X posting | Connect/login account if Raj asks. |

### 3) Ready reusable assets
| Asset | Use |
|---|---|
| `reports/proposal-assets/aics-diagnostics-pathology-mini-offer-2026-05-19-2030.md` | Proposal/landing-page block for diagnostics/pathology prospects after approval. |
| `reports/posting-onboarding-readiness/aics-diagnostics-reply-onboarding-kit-2026-05-19-2200.md` | First-reply/onboarding readiness if a diagnostics prospect responds positively. |
| `reports/posting-onboarding-readiness/aics-sparsh-whatsapp-demo-post-approval-checklist-2026-05-19-2215.md` | Exact execution checklist for Sparsh after Raj approval. |

## CRM files updated in this run
- `aicloudstrategist-crm/templates/leads.csv`
- `aicloudstrategist-crm/templates/approvals.csv`
- `aicloudstrategist-crm/templates/interactions.csv`
- `aicloudstrategist-crm/reports/daily/daily_report.csv`

## Next action
Request/monitor Raj decision on the two live approval gates: Sparsh WhatsApp demo and diagnostics/pathology rendered email pack. Do not send externally until the relevant exact item is approved.

# AICS Customer Onboarding Fast-Track System

Date: 2026-05-18  
Prepared for: AICloudStrategist / AICS-Ops  
Scope: inbound/approved-lead conversion system from first enquiry to paid kickoff and internal handover. No external outreach performed.

## 1. Existing context used

AICS already has these useful building blocks:

- CSV-first CRM with `leads.csv`, `interactions.csv`, `approvals.csv`, and `inbox_log.csv`.
- Suggested CRM lead statuses: `New`, `Researching`, `Qualified`, `Approval pending`, `Contacted`, `Follow-up`, `Won`, `Lost`, `Avoid`.
- Website/local lead capture setup with UTM fields, landing page, referrer, `source_page`, and Local SMB lane fields.
- Current public contact paths: voice `+91 80654 80898`, WhatsApp Business `+91 87963 02608`, email/contact forms.
- Voice/IVR pilot captures call leads to CSV/JSONL and can send founder WhatsApp alerts.
- WhatsApp templates exist, but customer sends require consent/approval; production scale should move to official WhatsApp Business API/WABA.
- Final offer strategy is outcome-led: **Buy Back Time Automation Audit** as front-door offer, then **One Workflow Pilot Sprint**, then **Managed AI Ops / Workflow Ops Retainer**.

## 2. Fast-track objective

Reduce the time from inbound lead to qualified first call and paid kickoff while preserving AICS approval rules, data hygiene, and founder oversight.

Target service-level agreements:

| Step | Target time | Owner |
|---|---:|---|
| Lead captured and deduped | Immediate / within 15 min | Automation + Ops |
| Priority A internal alert | Immediate | Automation |
| First human review | Within 2 business hours | Raj / assigned owner |
| First response for qualified inbound lead | Same business day | Owner, after approval if outbound |
| Discovery call booked | Within 1-2 days | Owner |
| Proposal/SOW sent after call | Within 24 hours for standard offers | Owner + Jarvis draft |
| Payment link/invoice issued after approval | Same day | Raj / Finance |
| Kickoff scheduled after payment | Within 1 business day | Delivery owner |

## 3. Lead intake fields

### 3.1 Minimum required fields

Use these for website forms, chatbot, IVR/call capture, WhatsApp intake, manual imports, and CRM rows.

| Field | Required | Notes |
|---|---|---|
| `lead_id` | Yes | Format: `AICS-YYYYMMDD-###` or existing `L-####` until migrated. |
| `created_date` | Yes | ISO date. |
| `created_time_ist` | Yes | IST time. |
| `source` | Yes | Website, chatbot, IVR, WhatsApp, email, referral, manual, event, paid-ad, partner. |
| `source_page` | If web | Page/form/chat path. |
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` | If web/ad | Preserve attribution. |
| `landing_page` | If web | First URL. |
| `referrer` | If web | Browser referrer. |
| `company_name` | Yes | If individual, use personal/business name. |
| `contact_name` | Yes | Decision maker or primary contact. |
| `title` | Helpful | Founder, owner, CEO, operations, sales, IT, clinic admin, etc. |
| `email` | Preferred | Required for proposal/SOW. |
| `phone` | Preferred | Required for call/WhatsApp follow-up. |
| `whatsapp_consent` | Yes/No/Unknown | Must be explicit before WhatsApp follow-up where possible. |
| `website` | Helpful | Current website/Google profile/app. |
| `city_country` | Yes | Helps local/regional routing. |
| `industry` | Yes | SaaS, agency, clinic, manufacturing, retail, real estate, education, etc. |
| `company_size` | Helpful | Solo, 2-10, 11-50, 51-200, 200+. |
| `annual_revenue_band` | Optional | Use broad ranges only if volunteered. |
| `problem_statement` | Yes | Customer's own words. |
| `desired_outcome` | Yes | More leads, fewer missed calls, time saving, dashboard, security, cloud cost, etc. |
| `current_tools` | Helpful | WhatsApp, Excel, CRM, website, cloud, helpdesk, POS, ERP. |
| `urgency` | Yes | Immediate, 7 days, 30 days, exploring. |
| `budget_band` | Helpful | Unknown, under ₹25k, ₹25k-₹75k, ₹75k-₹1.5L, ₹1.5L-₹6L, ₹6L+. |
| `decision_maker` | Yes/No/Unknown | Needed before proposal. |
| `service_interest` | Yes | Audit, workflow sprint, revenue recovery, website/lead capture, cloud/security, retainer. |
| `ai_cloud_fit` | Yes | High/Medium/Low. |
| `priority` | Yes | Priority A/B/C/Avoid. |
| `status` | Yes | CRM stage below. |
| `owner` | Yes | Raj / Ops / Delivery lead. |
| `next_action` | Yes | Specific action. |
| `next_action_date` | Yes | Date. |
| `last_contact_date` | If any | Keep historical interactions in interactions.csv. |
| `notes` | Optional | Concise factual notes. |

### 3.2 Discovery enrichment fields

Add after first human review or discovery call:

- Current manual workflow causing pain.
- Approximate volume: leads/month, calls/day, enquiries/day, tickets/week, invoices/month, cloud spend/month.
- Current leakage: missed calls, no follow-up, no CRM, delayed quotes, repeated admin, no dashboard, high cloud bill, security risk.
- Existing documentation/SOP status.
- Access complexity: website admin, Google Business, Meta/WhatsApp, CRM, cloud accounts, domain/email, API availability.
- Compliance sensitivity: health, financial data, children/student data, legal data, personal data, DPDP/privacy concerns.
- Success metric agreed: hours saved, lead response time, missed enquiry reduction, quote turnaround, dashboard accuracy, cloud cost reduction, uptime/security metric.
- Desired go-live date.
- Payment/invoicing contact and GST details.

## 4. Qualification criteria

### 4.1 Priority scoring

Assign priority during intake, then revise after discovery.

#### Priority A — fast-track now

A lead is Priority A if at least four are true:

- Founder/owner/decision maker is directly involved.
- Pain is urgent and measurable: missed revenue, manual bottleneck, slow follow-up, cloud/security risk, customer leakage.
- Clear fit to AICS offer ladder: Buy Back Time Audit, One Workflow Pilot Sprint, Revenue Recovery, Cloud/Security assurance, or Managed Ops.
- Has existing business activity and real volume.
- Budget is plausible for at least a paid audit or starter sprint.
- Can provide access/data within 3-5 days.
- Wants action within 30 days.
- Not asking for generic free advice or unsupported tool-only setup.

Action: same-day internal alert, call booking, qualification note, proposal path if fit confirmed.

#### Priority B — nurture / clarify

Use when:

- Problem is real but not urgent.
- Budget/timeline is unclear.
- Not the decision maker, but can refer internally.
- Fit is likely but details are incomplete.
- Wants information before committing.

Action: send approved educational response, ask 2-3 clarifying questions, schedule review if they engage.

#### Priority C — low fit / waitlist

Use when:

- Very small one-off task with no strategic follow-on.
- No budget and no decision authority.
- Vague curiosity about AI without a business process pain.
- Timeline beyond 90 days.

Action: polite close/nurture, no heavy proposal effort.

#### Avoid / disqualify

Use when:

- Requests illegal, spammy, deceptive, policy-violating, credential-harvesting, or unsafe automation.
- Wants bulk cold WhatsApp/calls/SMS without consent or approvals.
- Requires exposing private numbers/data or bypassing platform rules.
- No legitimate business identity.
- Abusive, non-serious, or clearly fraudulent.

Action: no proposal; log reason; escalate to Raj if sensitive.

### 4.2 Offer fit matrix

| Buyer pain | Best first offer | Follow-on |
|---|---|---|
| Founder is overloaded, too many manual tasks | Buy Back Time Automation Audit | One Workflow Pilot Sprint |
| Missed calls/WhatsApp/enquiries/leads | AI Revenue Recovery / Lead Follow-up Audit | CRM + WhatsApp + dashboard sprint |
| No website or weak lead capture | Website & Lead Capture Sprint | Local automation sprint |
| Existing website but no conversion/follow-up | Website/Lead Capture + Revenue Recovery review | Funnel/CRM/WhatsApp automation |
| Excel/process chaos | Workflow Audit | SOP + automation sprint |
| Cloud bill, reliability, migration, security | Cloud/Security Assurance Review | Remediation sprint / retainer |
| Customer onboarding/churn issues | Customer Success / Retention System Audit | Onboarding automation sprint |
| Wants long-term support after pilot | Managed AI Ops / Workflow Ops Retainer | Monthly improvement backlog |

## 5. CRM stages

Recommended upgraded stages for `leads.csv` / CRM dashboard:

1. **New** — captured, not yet reviewed.
2. **Deduped / Enriched** — basic details cleaned, duplicate checked, source attribution preserved.
3. **Needs Clarification** — missing problem, contact, budget, timeline, or decision maker.
4. **Qualified - Call Needed** — fit appears good; book discovery call.
5. **Call Booked** — time confirmed; prep brief created.
6. **Discovery Completed** — first call notes logged; next step known.
7. **Solution Fit Confirmed** — offer and success metric selected.
8. **Proposal Drafting** — proposal/SOW being drafted.
9. **Proposal Approval Pending** — Raj/founder approval required before sending.
10. **Proposal Sent** — sent through approved channel; follow-up scheduled.
11. **Negotiation / Questions** — scope, price, timeline, legal, access, or payment questions.
12. **Verbal Yes / Payment Pending** — buyer accepted; invoice/payment link pending or issued.
13. **Won - Paid** — payment received / PO accepted; kickoff to be scheduled.
14. **Kickoff Scheduled** — internal and client kickoff calendar invite sent.
15. **Onboarding In Progress** — documents/access collected, project workspace active.
16. **Handover to Delivery Complete** — delivery owner has scope, checklist, risks, access plan.
17. **Delivery Active** — outside sales onboarding pipeline; delivery tracking starts.
18. **Nurture** — not ready now; follow-up later.
19. **Lost** — chose not to proceed; reason logged.
20. **Avoid** — disqualified/risk.

### Stage exit rules

- Do not move to **Qualified - Call Needed** without problem statement, contact path, industry, and tentative offer fit.
- Do not move to **Proposal Drafting** without call notes or written discovery answers.
- Do not move to **Proposal Sent** until proposal is approved if external sending is required.
- Do not move to **Won - Paid** without payment/PO evidence.
- Do not move to **Handover to Delivery Complete** without signed/approved SOW, payment status, kickoff date, and access checklist.

## 6. First-call script

Purpose: qualify, create clarity, avoid unpaid consulting, select the right AICS next step.

### 6.1 Pre-call preparation

Before the call, prepare a 1-page lead brief:

- Who they are, source, website/social presence.
- Stated problem and desired outcome.
- Likely offer fit.
- 3 best discovery questions.
- Any risk flags: budget unclear, compliance-sensitive, access-heavy, unrealistic timeline.

### 6.2 Opening

> Thanks for speaking with AICloudStrategist. I want to keep this practical. In this call, I’ll understand your business, the current bottleneck, what result you want, and whether the right next step is an audit, a focused workflow sprint, or something we should not take on yet. If there is a fit, we’ll send a clear scope and price after the call.

### 6.3 Context questions

1. Tell me about your business in 60 seconds — what do you sell, to whom, and where?
2. What made you reach out now?
3. What is currently breaking, leaking revenue, wasting time, or creating risk?
4. How are you handling this today — people, WhatsApp, Excel, CRM, website, cloud tools, manual calls?
5. Roughly how often does this happen — per day/week/month?

### 6.4 Pain and impact

6. What happens if this is not fixed for the next 3 months?
7. What is the business impact — missed leads, delayed quotes, founder time, customer complaints, cost, risk?
8. Who is affected internally?
9. What have you already tried?

### 6.5 Desired outcome

10. If this worked well 30-60 days from now, what would be different?
11. What metric would prove success?
12. Is speed, reliability, cost, customer experience, or control the top priority?

### 6.6 Buying process

13. Who decides on this project?
14. Is there a target timeline?
15. Have you set aside budget, or should we recommend options?
16. Do you need GST invoice, PO, vendor onboarding, NDA, or security review?

### 6.7 Fit positioning

Use one of these, depending on fit:

**Audit fit**

> The right first step is not to build immediately. We should map the workflow, quantify leakage, score automation opportunities, and give you a 30-day pilot plan. That is our Buy Back Time Automation Audit.

**Pilot sprint fit**

> This sounds specific enough for a focused sprint: one workflow, one measurable outcome, with human approval gates and documentation. We would not try to automate the whole business at once.

**Revenue recovery fit**

> Your biggest gap is lead leakage: enquiries, calls, WhatsApp, and follow-up ownership. The first system should capture, assign, remind, and report — before spending more on marketing.

**Cloud/security fit**

> This is more of a risk/control issue. We should start with a structured review of architecture, access, backup, cost, observability, and security hygiene before touching production systems.

### 6.8 Close

> Based on this, I’ll prepare a short scope with: problem summary, recommended first step, deliverables, timeline, price, what we need from you, and exclusions. If it looks right, we can move to payment/invoice and kickoff. Is there anything that would block you from deciding this week?

### 6.9 Post-call notes

Immediately log:

- Pain statement.
- Desired outcome.
- Success metric.
- Offer fit.
- Budget/timeline.
- Decision maker.
- Risks/blockers.
- Next action and date.

## 7. Proposal / SOW flow

### 7.1 Proposal types

Create three standard proposal/SOW templates:

1. **Buy Back Time Automation Audit** — 5 business days, diagnostic deliverables, fixed fee.
2. **One Workflow Pilot Sprint** — 2-4 weeks, one workflow, measurable outcome, documentation and handover.
3. **Managed AI Ops / Workflow Ops Retainer** — monthly support, monitoring, improvement backlog, dashboards, governance.

Optional add-ons:

- Website & Lead Capture Sprint.
- Revenue Recovery / CRM / WhatsApp follow-up sprint.
- Cloud/Security assurance review.
- DPDP/privacy basics.
- Dashboard/KPI/cash reporting module.

### 7.2 Proposal sections

Every proposal should include:

1. Client context and problem summary.
2. Business outcome target.
3. Recommended first step.
4. Scope included.
5. Scope excluded.
6. Deliverables.
7. Timeline and milestones.
8. Client responsibilities and access needed.
9. Assumptions.
10. Price, taxes, payment schedule.
11. Change request rule.
12. Confidentiality/data handling note.
13. Approval/signature/payment instructions.
14. Validity period, usually 7-14 days.

### 7.3 SOW guardrails

- Keep first engagement narrow: audit or one workflow only.
- Include human approval gates for customer-facing automation.
- Do not promise 10x growth, guaranteed revenue, or fully autonomous decisions.
- Do not include live outbound WhatsApp/calling/email at scale unless consent, platform compliance, and approvals are explicit.
- For cloud/security work, state whether access is read-only or change-approved.
- For AI automations, include quality control and fallback process.
- For production WhatsApp, note Web pilot is not scale-compliant; use official WABA/Cloud API for production template messaging.

### 7.4 Internal approval before sending

If proposal is external-facing:

- Draft in workspace.
- Create/update CRM stage: `Proposal Approval Pending`.
- Record approval item in `approvals.csv` if sending through a channel requiring approval.
- Raj approves scope, price, promises, and channel.
- Only then send and move to `Proposal Sent`.

## 8. Payment, kickoff, and handover checklist

### 8.1 Payment checklist

Before marking `Won - Paid`:

- Final SOW/proposal approved by client.
- Client legal name captured.
- GSTIN/billing address captured if applicable.
- Payment terms confirmed: 100% advance for audit/starter sprint; milestone split for larger sprint/retainer.
- Payment method/link/invoice issued.
- Payment received, PO received, or written approval from Raj to start before payment.
- Receipt/proof linked in CRM.
- Finance/tax notes saved.

Recommended payment rules:

- Audit: 100% advance.
- Small sprint: 50-100% advance, balance before final handover.
- Larger sprint: 50% kickoff, 30% build milestone, 20% before go-live/handover.
- Retainer: monthly advance.

### 8.2 Kickoff checklist

Schedule kickoff only after payment/PO approval.

Kickoff agenda:

1. Confirm scope and success metric.
2. Confirm owners and communication channel.
3. Confirm timeline and meeting cadence.
4. Review access/data collection checklist.
5. Confirm security/privacy boundaries.
6. Confirm decision/approval gates.
7. Confirm first milestone and date.
8. Confirm what is out of scope.

### 8.3 Access and data checklist

Collect only what is needed.

- Website/domain/CMS access.
- Google Business/Profile/Search Console/Analytics if relevant.
- WhatsApp Business / Meta / ad account access if relevant.
- CRM/spreadsheet/tool exports.
- Cloud account read-only access if cloud/security work.
- Existing SOPs, scripts, forms, templates.
- Sample leads/tickets/calls/messages, sanitized where possible.
- Brand assets and business information.
- Stakeholder list and approval owner.

Security rule: prefer least-privilege access, temporary access, named accounts, and no password sharing where avoidable.

### 8.4 Delivery handover checklist

Before marking `Handover to Delivery Complete`, create an internal handover note:

- Lead/client ID and company.
- Signed/approved proposal or SOW link.
- Payment status/proof.
- Scope summary.
- Deliverables and due dates.
- Success metric.
- Primary client contact and escalation contact.
- Communication channel.
- Access status and pending access.
- Risks/assumptions/exclusions.
- First 3 delivery actions.
- Approval gates.
- Any compliance/privacy notes.

## 9. Automation opportunities

### 9.1 Immediate automations

1. **Lead dedupe and ID generation**  
   Match by email, phone, company, website; assign unique ID.

2. **Source attribution capture**  
   Preserve UTM/referrer/source page from website and chatbot.

3. **Priority A alert**  
   If fit/urgency keywords or high-value criteria match, send internal WhatsApp alert to founder/owner.

4. **CRM stage reminder**  
   If `next_action_date` is today or overdue, alert owner.

5. **First-call prep brief**  
   Auto-generate company summary, likely offer fit, and discovery questions.

6. **Post-call summary draft**  
   Turn call notes/transcript into CRM update, action list, and proposal outline.

7. **Proposal skeleton generation**  
   Generate draft from selected offer type and discovery answers; require human approval before sending.

8. **Payment/kickoff checklist tracker**  
   Block kickoff stage until payment, SOW, owner, access checklist, and kickoff date are complete.

### 9.2 Near-term automations

- Chatbot-to-CRM ingestion.
- IVR/call lead CSV sync into main CRM.
- WhatsApp inbound parser for lead details.
- Calendar booking link insertion after approval.
- Daily sales pipeline summary: new, qualified, proposal pending, payment pending, blockers.
- Lost reason analytics.
- Proposal validity/follow-up reminders.
- Founder dashboard: Priority A leads, overdue next actions, proposal value, expected kickoff dates.

### 9.3 Later / production-grade automations

- Replace CSV CRM with database-backed CRM/dashboard once volume justifies it.
- Official WhatsApp Business API/WABA for compliant template messaging.
- Stable production calling endpoint and natural speech agent.
- E-signature integration.
- Payment gateway + invoice automation.
- Customer portal for onboarding documents/access status.
- Delivery project workspace auto-creation.

## 10. Blockers and approvals

### 10.1 Approvals required before external action

- Any customer/prospect outreach that is not a direct reply to an inbound consented enquiry.
- Public posts, ads, campaigns, cold emails, cold calls, SMS, WhatsApp outreach.
- Proposal/SOW scope, pricing, promises, and terms before sending.
- Any spend/subscription above the existing approval threshold.
- Any use of paid ads, Meta policy acceptance, billing, or lead forms.
- Any production customer WhatsApp automation beyond approved pilot use.
- Any customer data transfer to new third-party systems.

### 10.2 Current operational blockers

- CRM is CSV-first; good for pilot, but will need database/dashboard as volume grows.
- Form processing uses static-site style tooling; production data handling, spam protection, consent, and privacy should be reviewed.
- WhatsApp Web pilot is linked and useful for testing/internal alerts, but official WABA is recommended for scale/compliance.
- Voice/IVR pilot exists; stable production endpoint and natural speech stack still need hardening.
- Public outreach remains approval-gated.
- Social/ads/platform lead-generation gates are separate from onboarding and should not block inbound fast-track.

### 10.3 Decisions needed from Raj / AICS-Ops

1. Confirm final standard offer names and starter prices for:
   - Buy Back Time Automation Audit.
   - One Workflow Pilot Sprint.
   - Managed AI Ops / Workflow Ops Retainer.
2. Confirm whether audits are always paid or whether a limited free classification call remains available.
3. Approve standard proposal/SOW template language.
4. Approve payment rules and preferred payment gateway/invoice process.
5. Choose CRM evolution path: continue CSV, Google Sheets dashboard, Twenty CRM, or custom lightweight app.
6. Approve consent/privacy wording for forms, chatbot, WhatsApp, and call capture.
7. Decide delivery owner assignment model once first paid clients arrive.

## 11. Recommended operating cadence

Daily sales/onboarding review, 15 minutes:

- New leads since last review.
- Priority A leads and owner.
- Calls booked today/tomorrow.
- Proposals pending approval.
- Payment pending.
- Kickoff/handover blockers.
- Overdue next actions.

Weekly pipeline review, 30 minutes:

- Lead sources and conversion.
- Lost reasons.
- Proposal cycle time.
- Average first-response time.
- Delivery capacity.
- Which offer is converting best.

## 12. Minimal implementation plan

### Day 1

- Add the upgraded intake fields to the CRM template or a new enriched lead sheet.
- Add CRM stages and stage exit rules.
- Create first-call note template.

### Day 2

- Create 3 proposal/SOW skeletons.
- Create payment/kickoff/handover checklist templates.
- Add daily pipeline summary format.

### Day 3

- Connect existing IVR/chatbot/web lead capture into the same CRM format where feasible.
- Add Priority A alert rule and overdue next-action rule.
- Test with 3 sample leads: Local SMB, founder-led B2B services firm, cloud/security advisory lead.

## 13. Fast-track summary

The practical fast-track is:

1. Capture every lead with source attribution and consent state.
2. Dedupe, enrich, and score Priority A/B/C/Avoid.
3. Book a focused first call only for qualified leads.
4. Use the first call to choose audit, pilot sprint, retainer, or disqualify.
5. Send a narrow approved proposal/SOW within 24 hours.
6. Collect payment/PO before kickoff except with explicit Raj approval.
7. Handover to delivery with scope, success metric, access checklist, risks, and first actions.

This keeps AICS fast without becoming sloppy: clear qualification, narrow first offers, explicit approval gates, and measurable delivery handover.

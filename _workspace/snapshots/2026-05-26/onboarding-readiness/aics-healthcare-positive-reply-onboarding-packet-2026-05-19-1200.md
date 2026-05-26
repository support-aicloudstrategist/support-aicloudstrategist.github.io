# AICS Healthcare Positive-Reply Onboarding Packet — 2026-05-19 12:00 IST

**Workstream advanced:** posting/onboarding readiness → first-response and discovery readiness  
**Operator:** Jarvis / AICS CEO command-center  
**Primary approval ID:** `AICS-HC-ONBOARD-20260519-1200`  
**Guardrail:** No prospect/customer was contacted. No public post, website deploy, paid action, contract, credential change, patient-data collection, or destructive action was performed.

## CEO decision

The healthcare offer now has enough GTM, prospect, proposal, landing-page, FAQ, and staging material. The next highest-leverage safe step is to remove delivery friction for the first positive reply: prepare an approval-gated response, intake checklist, discovery-call worksheet, and handoff board so AICS can respond professionally within minutes after Raj approves contact.

## When to use this packet

Use only after one of these approved events occurs:

1. Raj manually sends an approved healthcare opener and the prospect replies positively.
2. Raj approves a call and the prospect agrees to receive details or book a review.
3. A public website/social lead submits a genuine healthcare readiness enquiry.

Do **not** use this packet for cold outreach by itself. It is a post-reply/onboarding readiness artifact.

---

## 1) Positive-reply triage board

| Reply type | Meaning | Safe internal action | Raj approval needed before external action |
|---|---|---|---|
| “Interested / send details” | Warm but not scheduled | Prepare exact reply using Template A below; log prospect as warm | Approval to send the exact reply if not already covered |
| “Call me” / shares number | Call intent | Prepare 15–20 minute discovery agenda; propose time slots | Approval to call exact number/time/script |
| “What is the price?” | Commercial interest | Share indicative range only if approved; ask scope questions | Approval to send price-bearing message |
| “We already have software” | Objection | Use non-replacement explanation; focus on workflow gaps | Approval to send objection-handling reply |
| “Not interested / STOP” | Opt-out | Mark do-not-contact; no follow-up | None; comply immediately |
| Mentions patient data/files | Sensitive data risk | Do not accept patient data; ask for process-only/anonymised info | Approval before any data-handling workflow |

## 2) First response templates needing Raj approval

### Template A — positive reply / send details

**Approval ID:** `AICS-HC-REPLY-DETAILS-20260519-1200`  
**Channel:** WhatsApp/email/DM, only to a prospect that already replied positively.  

```text
Thanks, {{Name}}. Sharing a short overview.

AICloudStrategist’s Healthcare Digital Readiness Audit helps clinics, diagnostic centres, labs, nursing homes, and small hospitals review practical digital workflow gaps — enquiries, appointments, billing/report delivery, follow-ups, backups, access controls, and management visibility.

The first review does not require patient data. We only discuss systems, workflows, sample process screenshots if needed, and current bottlenecks.

Output: a readiness scorecard, risk/leakage register, 30-day improvement roadmap, and implementation estimate.

Would you prefer a 20-minute review on {{Option 1}} or {{Option 2}}?
```

### Template B — price question reply

**Approval ID:** `AICS-HC-REPLY-PRICE-20260519-1200`  
**Channel:** WhatsApp/email/DM, only after prospect asks about pricing.  

```text
The Healthcare Digital Readiness Audit is usually scoped as a fixed advisory review in the ₹15,000–₹35,000 + applicable taxes range, depending on the number of locations, systems, and workflows reviewed.

Before quoting anything final, we should understand your appointment/enquiry flow, billing/report process, backup setup, and what outcome you want from the review. A 20-minute discovery call is enough to confirm fit and scope.

Would {{Option 1}} or {{Option 2}} work?
```

### Template C — “we already have software” objection

**Approval ID:** `AICS-HC-REPLY-SOFTWARE-20260519-1200`  
**Channel:** WhatsApp/email/DM, only after prospect raises this objection.  

```text
That is completely fine — this is not a replacement pitch for your HIS/EMR/LIS or billing software.

The audit checks the gaps around the software: enquiry capture, missed follow-ups, report delivery flow, backups, access hygiene, owner/admin visibility, and manual workarounds. Many clinics already have software but still lose time because systems and teams are not connected cleanly.

If useful, we can do a 20-minute review and identify only the top 2–3 practical improvements.
```

### Template D — sensitive-data boundary

**Approval ID:** `AICS-HC-REPLY-DATA-BOUNDARY-20260519-1200`  
**Channel:** WhatsApp/email/DM/call script, whenever patient data is mentioned.  

```text
Please do not share patient records, reports, IDs, prescriptions, or any personal health information for the initial review.

For the first stage, we only need process descriptions, system names, anonymised workflow screenshots if required, and examples of bottlenecks without personal data. If a later project ever requires data access, that would need a separate written scope, access control, and approval.
```

---

## 3) Discovery-call worksheet — internal use

**Call goal:** confirm fit, business pain, data boundary, scope, next action.  
**Duration:** 20 minutes.  
**Tone:** advisory, practical, no pressure, no medical/legal/compliance certification claims.

### Opening

- Confirm participant name, role, business name, city, and decision-making role.
- Confirm this is a workflow/digital readiness conversation, not medical advice or regulatory certification.
- State data boundary: no patient data is needed for this call.

### Qualification questions

1. What type of healthcare business is this: clinic, diagnostic centre, lab, nursing home, small hospital, multi-location practice?
2. Approximate scale: doctors, daily appointments/tests, staff/admin users, locations.
3. Current systems: website, Google Business Profile, WhatsApp, calls, forms, HIS/EMR/LIS/billing/reporting, spreadsheets.
4. Top operational pain: missed enquiries, appointment follow-up, report delivery, billing/payment follow-up, backup risk, staff coordination, owner visibility.
5. Where does a new patient/enquiry enter today? Phone, WhatsApp, website form, walk-in, referral, aggregator?
6. What happens when a call is missed or a WhatsApp message is unanswered?
7. Are reports delivered digitally, physically, through portal/WhatsApp/email, or manually?
8. Who can access records/reports/systems, and how are passwords/accounts managed?
9. Is there a backup/restore process? When was restore last tested?
10. What would make the audit valuable: scorecard only, roadmap, implementation estimate, or vendor/tool selection help?

### Close

- Summarise top 2–3 suspected gaps.
- Confirm no patient data will be requested for the proposal stage.
- Explain deliverables: scorecard, risk/leakage register, 30-day roadmap, implementation estimate.
- If fit is strong, request approval to send scoped proposal/next-step email.

---

## 4) CRM fields to create/update after a positive reply

| Field | Example/status |
|---|---|
| lead_id | `AICS-HC-YYYYMMDD-###` |
| business_name | Prospect-provided official name |
| city/state | From prospect/public source |
| contact_person | Name + role if provided |
| source | exact channel and original approval ID |
| consent_status | interested / requested details / requested call / STOP |
| current_systems | website, WhatsApp, HIS, LIS, billing, spreadsheets |
| main_pain | one-line pain summary |
| data_boundary_confirmed | yes/no |
| next_action | details reply / discovery call / proposal / no follow-up |
| next_action_approval_id | approval ID for exact message/call |
| owner | Raj/Jarvis/manual operator |
| last_touch | timestamp + channel |
| blocker | approval needed / scheduling / data boundary / no response |

## 5) Handoff checklist before any paid proposal

- [ ] Prospect has explicitly shown interest or requested details/call.
- [ ] Business identity and contact source are verified.
- [ ] Data boundary is stated: no patient data in initial review.
- [ ] Discovery notes completed using worksheet above.
- [ ] Scope level chosen: single location / multi-location / systems-heavy.
- [ ] Commercial range kept indicative until final scope approval.
- [ ] Raj approves exact proposal/send action before sharing commercial commitment.
- [ ] CRM record updated with approval ID and next action.

## 6) Current blockers

1. **External response actions gated:** even positive-reply templates above need Raj approval before sending unless included in a future exact approval.
2. **Live lead intake not connected:** healthcare landing page is not publicly deployed; staging is pending `AICS-HC-WEB-STAGE-20260519-1145`.
3. **WhatsApp automation blocked:** sender remains scan-required/logged out; use manual approved channel only if Raj approves.
4. **Prospect outreach not approved:** 4-prospect mini-proposal pack remains pending exact target/channel/script approval.

## Next safe action

Package this onboarding packet into the daily approval pack and, if still no external approval arrives, continue with CRM board implementation: create a structured CSV/Markdown warm-lead pipeline template using the fields above so the first positive reply can be logged immediately.

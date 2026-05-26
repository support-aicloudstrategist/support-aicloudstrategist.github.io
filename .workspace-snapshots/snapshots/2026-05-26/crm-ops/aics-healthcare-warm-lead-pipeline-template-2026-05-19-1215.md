# AICS Healthcare Warm-Lead Pipeline Template — 2026-05-19 12:15 IST

**Queue ID:** `AICS-HC-WARM-PIPELINE-20260519-1215`  
**Workstream advanced:** posting/onboarding readiness → CRM implementation readiness  
**Source packet:** `/home/OpenClaw/.openclaw/workspace/reports/onboarding-readiness/aics-healthcare-positive-reply-onboarding-packet-2026-05-19-1200.md`  
**CSV template:** `/home/OpenClaw/.openclaw/workspace/reports/crm-ops/aics-healthcare-warm-lead-pipeline-template-2026-05-19-1215.csv`

## Guardrail

No prospect/customer was contacted. No public post, website deploy, paid action, contract, credential change, patient-data collection, or external system edit was performed. This is an internal queue template so the first positive healthcare reply can be logged cleanly after Raj-approved outreach or inbound interest.

## What this fixes

The 12:00 onboarding packet had response templates and a discovery worksheet, but no ready CRM queue structure. This template turns the onboarding fields into a practical warm-lead board with approval IDs, consent status, data-boundary tracking, and next-action gating.

## Pipeline statuses

| consent_status | Meaning | Safe internal next action | External action gate |
|---|---|---|---|
| `requested_details` | Prospect asked for overview/details | Prepare Template A response | Raj approval to send exact reply |
| `requested_call` | Prospect requested or accepted a call | Prepare discovery worksheet and two time options | Raj approval for exact call time/number/script |
| `asked_price` | Prospect asked commercial range | Prepare indicative price reply | Raj approval before price-bearing reply |
| `software_objection` | Prospect says they already have HIS/EMR/LIS/billing software | Prepare non-replacement explanation | Raj approval before reply |
| `patient_data_mentioned` | Prospect mentions records/reports/patient info | Prepare data-boundary response; do not accept files | Only boundary/safety reply, then Raj approval for next step |
| `STOP_or_not_interested` | Prospect opts out or declines | Mark DNC; preserve evidence | None; no follow-up |

## Required fields before any external response

- `lead_id`
- `business_name`
- `city_state`
- `contact_person` and role if known
- `source_channel`
- `source_artifact` or public source URL
- `original_approval_id`
- `consent_status`
- `main_pain`
- `data_boundary_confirmed`
- `next_action`
- `next_action_approval_id`
- `last_touch_ist`
- `blocker`

## Approval linkage

Use these current onboarding IDs for prepared responses:

- `AICS-HC-REPLY-DETAILS-20260519-1200`
- `AICS-HC-REPLY-PRICE-20260519-1200`
- `AICS-HC-REPLY-SOFTWARE-20260519-1200`
- `AICS-HC-REPLY-DATA-BOUNDARY-20260519-1200`

## Next safe action

If no Raj approval arrives, prepare a staging-only healthcare landing-page QA checklist for `AICS-HC-WEB-STAGE-20260519-1145`, including mobile checks, noindex verification, CTA path, healthcare disclaimer visibility, and screenshot capture list.

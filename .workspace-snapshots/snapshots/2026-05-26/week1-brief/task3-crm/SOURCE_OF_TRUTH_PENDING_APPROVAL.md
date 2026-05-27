# Task 3 — 300-row Prospect CRM Source of Truth Pending Approval

Status: EMPTY SCHEMA ONLY — no prospect rows populated.

## Decision
Use **Google Sheet** as the canonical CRM once founder approves the source-of-truth path.

Reason:
- 300-row research list needs easy review/filtering by Raj/Anushka.
- CSV export/import remains simple.
- Sheet can later feed WhatsApp/email approval workflows without Notion lock-in.

## Proposed Google Sheet
Suggested sheet title:
`AICS Week 1 Task 3 — 300 Prospect CRM — Founder Approved Source of Truth`

Suggested tabs:
1. `Prospects` — 300-row working CRM.
2. `Schema` — field definitions.
3. `Exclusions` — rejected/unusable leads and reason.
4. `Approval_Log` — founder approval status for list/source path.

## Local schema artifact
`/home/OpenClaw/.openclaw/workspace/reports/week1-brief/task3-crm/aics-task3-prospect-crm-empty-schema.csv`

## Rule
Do not populate prospect rows until founder approves the canonical source-of-truth path.

## Required row rule once approved
Every populated prospect row must include a credible public `source_url`. No invented prospects, phone numbers, testimonials, or business claims.

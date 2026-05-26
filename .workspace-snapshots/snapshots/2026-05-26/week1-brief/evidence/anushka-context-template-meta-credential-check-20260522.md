# Rule 11 Evidence — Anushka Context, v2 Template Diff, Meta WhatsApp Credential Check

Timestamp: 2026-05-22 IST  
Scope: Evidence-only consolidation. No commits, no merge, no outreach, no publishing, no CRM rows, no `contact-channels.json` modification.

## Step 1 — Anushka context dump

### Literal grep stdout

Command executed:

```bash
grep -rn "Anushka\|Bhattacharya" /home/OpenClaw/.openclaw/workspace/ 2>/dev/null
```

The literal stdout was captured and posted as attachment because it is 655 lines / ~330 KB and would be truncated in Telegram:

- `/home/OpenClaw/.openclaw/workspace/artifacts/anushka-grep-stdout-20260522.txt`

### Top 5 files by hit count

1. `/home/OpenClaw/.openclaw/workspace/aics-lead-engine-v1/whatsapp-agent/whatsapp-agent.out` — 34 hits
2. `/home/OpenClaw/.openclaw/workspace/aics-lead-engine-v1/whatsapp-agent/events.log` — 34 hits
3. `/home/OpenClaw/.openclaw/workspace/memory/.dreams/short-term-recall.json` — 32 hits
4. `/home/OpenClaw/.openclaw/workspace/memory/2026-05-16.md` — 32 hits
5. `/home/OpenClaw/.openclaw/workspace/memory/2026-05-18.md` — 30 hits

Full surrounding context for these top 5 files was generated and posted as attachment:

- `/home/OpenClaw/.openclaw/workspace/artifacts/anushka-top5-contexts-20260522.md`

For log/JSON files, full matching records/objects were included. For Markdown files, full matching sections were included.

### Anushka photo asset status

Found current public website photo asset path:

- `/home/OpenClaw/.openclaw/workspace/repos/support-aicloudstrategist.github.io/assets/rajiv-headshot-placeholder.png`

Evidence:

```text
assets/rajiv-headshot-placeholder.png: PNG image data, 800 x 800, 8-bit colormap, non-interlaced
commit a7513b9400456b400f1bc54e49d99aee4987470f
    Add Anushka headshot and client communication copy
M	assets/rajiv-headshot-placeholder.png
```

Current About page references the asset with Anushka alt text:

```html
<img
  class="founder-photo"
  src="/assets/rajiv-headshot-placeholder.png"
  alt="Anushka Bhattacharya, Director at AICloudStrategist"
/>
```

Source URL: no explicit source URL was found for the current `a7513b9` Anushka headshot asset. It appears to be an uploaded/replaced asset committed as `Add Anushka headshot and client communication copy`.

Important distinction: a separate LinkedIn image URL was recorded during the reverted Raj/Rajiv headshot investigation, but that asset was reverted and is not confirmed as Anushka's photo source.

### Approval pack / founder-approved Director identity evidence

Founder/Raj explicit identity correction is recorded in memory:

- `/home/OpenClaw/.openclaw/workspace/memory/2026-05-19.md:303`

```text
Raj corrected two major mistakes in a sent diagnostic lab email: Jarvis used old WhatsApp number `+91 78383 47711` instead of current AICS WhatsApp `+91 87963 02608`, and used Rajiv's personal name instead of the finalized public-facing Director identity `Anushka Bhattacharya, Director, AICloudStrategist`.
```

Approval packs / approval artifacts using Anushka as Director include:

- Pack/date: `diagnostics-correction-20260519-2330`, 2026-05-19 23:30 IST  
  Evidence: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/diagnostics-correction-20260519-2330/approval-card.md:18`  
  `Signature: Anushka Bhattacharya, Director, AICloudStrategist`

- Pack/date: `aics-daily-approval-pack-2026-05-20-1202`, 2026-05-20 12:02 IST  
  Evidence: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/aics-daily-approval-pack-2026-05-20-1202.md:16`  
  `Default public signature: Anushka Bhattacharya, Director, AICloudStrategist.`  
  Pack IDs in this file: `AICS-APP-20260520-001` through `AICS-APP-20260520-010`.

- Pack/date: `aics-daily-approval-pack-2026-05-20-1802`, 2026-05-20 18:02 IST  
  Evidence: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/aics-daily-approval-pack-2026-05-20-1802.md:14`  
  `Default public signature: **Anushka Bhattacharya, Director, AICloudStrategist**.`  
  Pack IDs in this file: `AICS-APP-20260520-011` through `AICS-APP-20260520-022`.

- Pack/date: `healthcare-whatsapp-call-asset-20260520-1945`, 2026-05-20 19:45 IST  
  Evidence: `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/healthcare-whatsapp-call-asset-20260520-1945/approval-card.md:56`  
  `Default public signature: Anushka Bhattacharya, Director, AICloudStrategist.`

## Step 2 — v2 template situation

### Commit `ad14eb9` — Lost-Lead Audit v2

Result: commit `ad14eb9` unexpectedly includes the DPDP template file as well as Lost-Lead. The only diff hunk in `ad14eb9` naming Anushka is in the DPDP template, not in the Lost-Lead template.

Literal diff hunk where Anushka is named:

```diff
+Owner: AICloudStrategist / Jarvis orchestration
+Approval requirement: Any customer-facing version requires an approval pack before sending.
+
+---
+
+## 1. Scope Summary
+
+**Client / Business name:** [VERIFIED BUSINESS NAME]
+**Business category:** [CATEGORY]
+**Website / app reviewed:** [URL]
+**Prepared for:** [CONTACT NAME or UNKNOWN]
+**Prepared by:** AICloudStrategist
+**Date:** [YYYY-MM-DD]
+
+**Sprint objective:** Help the business create a practical first-layer DPDP/privacy readiness foundation for its website, lead forms, WhatsApp enquiry handling, consent language, internal process documentation, and vendor/contact-data hygiene.
+
+**Important disclaimer:** This sprint is an operational/privacy-readiness implementation support package. It is not legal advice. The client should consult qualified legal counsel for legal interpretation or final compliance sign-off.
+
+## Brand and People Note
+
+Anushka Bhattacharya is Director at AICloudStrategist and her photo/name may appear in AICloudStrategist public-facing material. Keep Anushka's Director identity and name intact wherever already used. Do not replace Anushka's photo/name with an unverified Rajiv/Raj headshot unless founder identity is confirmed with HIGH confidence and Rajiv approves the exact asset.
+
+---
+
+## 2. Included Deliverables
+
+| Deliverable | Included? | Output format | Owner | Notes |
+|---|---:|---|---|---|
+| Website privacy/trust review | YES | Findings table | AICS | Based on public website and client inputs |
+| Privacy policy gap checklist | YES | Markdown/Doc | AICS | Not legal advice |
+| Consent language recommendations | YES | Copy block | AICS | For forms/WhatsApp where applicable |
+| Lead form data-flow map | YES | Table/diagram | AICS + client | Requires client process input |
+| WhatsApp enquiry handling SOP | YES | SOP | AICS | Covers consent-aware follow-up |
+| Vendor/tool register template | YES | Spreadsheet/table | AICS | Client must verify tools/vendors |
+| Data retention starter policy | YES | Draft SOP | AICS | Client must approve retention periods |
+| Incident/breach readiness checklist | YES | Checklist | AICS | Operational readiness only |
+| Staff handling checklist | YES | Checklist | AICS | Simple SMB-friendly version |
+| Final implementation summary | YES | Report | AICS | With evidence and open items |
+
+---
```

Mark: **KEEP** — The content is now accurate per founder confirmation that Anushka Bhattacharya is the real Director and public-facing person. It is appropriate as an internal/customer-facing template governance note because it prevents accidental replacement with an unverified Raj/Rajiv asset. Customer-specific exports should still go through founder approval as the template itself states.

### Commit `d78b463` — DPDP Sprint v2

Literal diff hunk where Anushka is named:

```diff
 Canonical artifact: `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/templates/dpdp-sprint-scoped-delivery-template.md`
 Status: TEMPLATE — not legal advice and not customer-specific until scoped with verified client data.
 Owner: AICloudStrategist / Jarvis orchestration
 Approval requirement: Any customer-facing version requires an approval pack before sending.
 
 ---
 
 ## 1. Scope Summary
 
 **Client / Business name:** [VERIFIED BUSINESS NAME]
 **Business category:** [CATEGORY]
 **Website / app reviewed:** [URL]
 **Prepared for:** [CONTACT NAME or UNKNOWN]
 **Prepared by:** AICloudStrategist
 **Date:** [YYYY-MM-DD]
 
 **Sprint objective:** Help the business create a practical first-layer DPDP/privacy readiness foundation for its website, lead forms, WhatsApp enquiry handling, consent language, internal process documentation, and vendor/contact-data hygiene.
 
+**Sprint price:** ₹14,999 one-time, no retainer commitment. Founder Customer Program discount available — see https://aicloudstrategist.com/pricing.html
+
 **Important disclaimer:** This sprint is an operational/privacy-readiness implementation support package. It is not legal advice. The client should consult qualified legal counsel for legal interpretation or final compliance sign-off.
 
 ## Brand and People Note
 
 Anushka Bhattacharya is Director at AICloudStrategist and her photo/name may appear in AICloudStrategist public-facing material. Keep Anushka's Director identity and name intact wherever already used. Do not replace Anushka's photo/name with an unverified Rajiv/Raj headshot unless founder identity is confirmed with HIGH confidence and Rajiv approves the exact asset.
 
 ---
 
 ## 2. Included Deliverables
 
 | Deliverable | Included? | Output format | Owner | Notes |
 |---|---:|---|---|---|
 | Website privacy/trust review | YES | Findings table | AICS | Based on public website and client inputs |
 | Privacy policy gap checklist | YES | Markdown/Doc | AICS | Not legal advice |
 | Consent language recommendations | YES | Copy block | AICS | For forms/WhatsApp where applicable |
 | Lead form data-flow map | YES | Table/diagram | AICS + client | Requires client process input |
 | WhatsApp enquiry handling SOP | YES | SOP | AICS | Covers consent-aware follow-up |
 | Vendor/tool register template | YES | Spreadsheet/table | AICS | Client must verify tools/vendors |
 | Data retention starter policy | YES | Draft SOP | AICS | Client must approve retention periods |
 | Incident/breach readiness checklist | YES | Checklist | AICS | Operational readiness only |
```

Mark: **KEEP** — The Anushka reference itself is appropriate and accurate per founder confirmation. Note: the visible diff hunk also includes a price line; pricing/content still requires normal customer-facing approval before use, but Anushka's appearance does not need fabrication remediation.

## Step 3 — Meta WhatsApp Cloud API credential check

### Current credential state

- Meta for Developers app linked to AICS WhatsApp Business: **not found / not verified locally**.
- WhatsApp Business phone number ID for `+91 87963 02608`: **not found locally**.
- Permanent system-user access token: **not found locally**.
- Existing live WhatsApp automation appears to be WhatsApp Web session based, not Meta WhatsApp Cloud API based:
  - Process: `node aics-whatsapp-agent.js`
  - Session path: `/home/OpenClaw/.openclaw/workspace/aics-lead-engine-v1/whatsapp-agent/session/session-aics-business-8796302608`
  - PID `83960` had no matching env keys for `META`, `WHATSAPP`, `WABA`, `PHONE_NUMBER_ID`, `ACCESS_TOKEN`, or `GRAPH`.

### GET `/v18.0/{phone-number-id}` test

Status: **not executable** because both required inputs are missing locally:

- `{phone-number-id}`: missing
- permanent system-user access token: missing

HTTP status: `NOT_EXECUTED_MISSING_PHONE_NUMBER_ID_AND_TOKEN`  
Response body: `NOT_EXECUTED_MISSING_PHONE_NUMBER_ID_AND_TOKEN`

Required status:

**REQUIRES_FOUNDER_AUTH: Meta WhatsApp Cloud API setup.**

## Boundary verification

- No commits were made.
- No merge was executed.
- No outreach was sent.
- No publishing was performed.
- No CRM rows were created.
- `contact-channels.json` was not modified.


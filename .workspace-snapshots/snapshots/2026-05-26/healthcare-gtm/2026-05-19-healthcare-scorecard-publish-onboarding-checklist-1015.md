# Healthcare Digital Readiness Scorecard — Publish + Onboarding Readiness Checklist

**Prepared at:** 2026-05-19 10:15 IST  
**Prepared for:** AICloudStrategist / Raj approval workflow  
**Parent approval:** `AICS-OFFER-20260519-HEALTHCARE-SCORECARD`  
**Current approval status:** Approved by Raj for website + PDF + discovery use. Prospect outreach still requires prospect-level approval.  
**Guardrail:** No website deployment, public posting, prospect contact, calls, paid action, payment-link action, or external-system change was performed by this run.

---

## 1) Freshest source assets confirmed

| Asset | Path | Status | Use |
|---|---|---|---|
| Master scorecard offer | `/home/OpenClaw/.openclaw/workspace/aics-enterprise-docs-polished/autopilot/2026-05-19-healthcare-digital-readiness-scorecard.md` | Approved for website/PDF/discovery | Source of truth for positioning, scope, scorecard framework, pricing range |
| Website landing block | `/home/OpenClaw/.openclaw/workspace/reports/healthcare-gtm/2026-05-19-healthcare-scorecard-website-landing-block.md` | HTML-ready | Website section or standalone landing page |
| Discovery runbook + worksheet | `/home/OpenClaw/.openclaw/workspace/reports/healthcare-gtm/2026-05-19-healthcare-discovery-call-runbook-and-scorecard.md` | Operator-ready | Use only after an approved prospect agrees to review / approved discovery use |
| Prospect exact approval pack | `/home/OpenClaw/.openclaw/workspace/reports/approval-packs/aics-healthcare-4-prospect-exact-approval-pack-2026-05-19-0945.md` | Approval-ready, no outreach | One-by-one prospect approvals |
| Reverified prospect queue | `/home/OpenClaw/.openclaw/workspace/prospecting/2026-05-19/aics-healthcare-prospect-reverification-0930.csv` | Reverified shortlist | Internal CRM/prospect queue only |

---

## 2) Website publish-prep checklist — safe to execute internally

These steps prepare the asset for publication without changing the live site.

- [ ] Create a staging branch or local website working copy only; do not push/deploy without Raj’s deployment approval.
- [ ] Add the HTML-ready section from the landing block to a draft page or component.
- [ ] Use one of these safe placements:
  - Services page insertion after the core cloud/automation advisory section, or
  - Standalone draft page: `/healthcare-digital-readiness-scorecard/`.
- [ ] Set primary CTA to existing approved contact route only: `Book a 20-minute readiness review`.
- [ ] Keep secondary CTA disabled or hidden until PDF file exists at a confirmed path.
- [ ] Keep this disclaimer visible near the pricing/CTA:
  > This is not a medical, legal, or regulatory certification. It is a practical technology and workflow readiness review for business improvement, operational resilience, and better digital execution.
- [ ] Do not add unsupported claims: no patient outcome claims, no compliance certification claims, no guaranteed revenue numbers, no named client proof unless separately approved.
- [ ] Capture local screenshot + diff for Raj review before any public deploy.

### Draft website-change approval line, if needed

```text
APPROVE AICS-WEB-20260519-HEALTHCARE-SCORECARD-PUBLISH: publish approved Healthcare Digital Readiness Scorecard landing block on AICloudStrategist website after final preview screenshot/diff review
```

---

## 3) PDF lead-magnet readiness checklist

- [ ] Convert scorecard into a two-page PDF with AICloudStrategist header, URL, and CTA.
- [ ] Page 1: problem, best-fit audience, what is reviewed, audit deliverables, price range.
- [ ] Page 2: 10-area scorecard table, interpretation bands, discovery CTA, disclaimer.
- [ ] Keep PDF filename stable for website link, recommended:
  - `healthcare-digital-readiness-scorecard.pdf`
- [ ] Store/export draft locally before upload; no public file upload without deployment approval.
- [ ] Check PDF for: no private details, no medical/legal certification claims, no invented proof, readable mobile layout.

---

## 4) First-client onboarding checklist after approved discovery interest

Use only after Raj-approved outreach or inbound opt-in.

### Before call

- [ ] Confirm approval ID or inbound opt-in evidence.
- [ ] Confirm business name, contact person, role, source URL, and approved channel.
- [ ] Prepare the 10-area scorecard worksheet.
- [ ] Reconfirm this positioning: practical technology/workflow readiness, not medical/legal/regulatory certification.

### During 20-minute review

- [ ] Minute 0–2: permission, scope, and owner/admin context.
- [ ] Minute 2–7: enquiries, appointments, missed calls/forms/WhatsApp, daily visibility.
- [ ] Minute 7–12: billing/report/prescription/follow-up handoff.
- [ ] Minute 12–16: backups, restore test, access hygiene, continuity.
- [ ] Minute 16–20: top 3 gaps, next-step fit, scorecard/audit offer.

### After call

- [ ] Save scorecard notes internally.
- [ ] Draft follow-up email using the runbook template.
- [ ] Get Raj approval before sending any proposal, payment link, contract, public claim, or implementation promise.
- [ ] If prospect declines or opts out, mark DNC/hold and stop follow-up.

---

## 5) Current next approval to ask Raj — one item only

Per the one-approval-at-a-time rule, the cleanest next approval remains:

```text
APPROVE AICS-HC-OUTREACH-20260519-001-NKPC-KIDNEY-CLINIC: email only, exact copy approved
```

**Why this first:** NKPC Kidney Clinic has the cleanest official contact-page evidence, a public email route, and strong fit for the approved healthcare scorecard. Email is lower-risk than WhatsApp/call and avoids the current WhatsApp QR blocker.

---

## 6) Blockers intentionally preserved

- No prospect contacted.
- No live website/public deployment performed.
- No social publishing performed.
- No WhatsApp automation bypassed; sender remains scan-required/logged out.
- No payment link, spend, contract, or external system change performed.

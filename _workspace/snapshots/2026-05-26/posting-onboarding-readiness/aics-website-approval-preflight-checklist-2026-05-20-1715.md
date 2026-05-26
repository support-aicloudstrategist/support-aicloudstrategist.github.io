# AICS website approval preflight checklist — 2026-05-20 17:15 IST

Status: internal QA/readiness artifact only. No website repo edit, public publish, customer/prospect contact, WhatsApp send, call, paid action, credential change, contract action, or destructive action performed.

## Source and SOP verification
- AICS Operating System read this run.
- AICS Outreach Master SOP read this run.
- Live contact source checked this run: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 17:15 IST.
- Current WhatsApp Business: `+91 87963 02608` / `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
- Current voice line: `+91 80654 80898` / `tel:+918065480898`.
- Primary public/customer email: `contact@aicloudstrategist.com`.
- Support email: `support@aicloudstrategist.com` only as support reference.
- Public identity guard: no Rajiv personal identity in public copy; Anushka Bhattacharya, Director, AICloudStrategist remains default signature where a signature is needed.

## Freshest AICS outputs found
1. `reports/outbound-whatsapp/sparsh-final-combined-founder-approval-20260520-171424.json` — final Sparsh WhatsApp approval sample with demo video sent to Raj personal WhatsApp for approval only.
2. `reports/posting-onboarding-readiness/aics-approval-pack-consolidation-2026-05-20-1700.md` — approval sequencing board; next safe item was QA-only preflight for website trust/resource packs.
3. `reports/approval-dashboard/aics-approval-dashboard-current.json` — current consolidated approval dashboard; external/customer/public actions remain approval-gated.

## Next safe unfinished item selected
Prepare a single pre-approval QA checklist for the two website/public-presence assets that are ready but still gated:

- Free Review trust/conversion polish
  - Founder card: `reports/approval-packs/free-review-trust-polish-20260520-1345/founder-review-card.md`
  - Implementation package: `reports/website-drafts/free-review-trust-polish-implementation-20260520-1330/`
- Clinic & Dental Lead Leakage Review resource page
  - Approval pack: `reports/brand-presence-polish/2026-05-20/clinic-dental-leakage-proof-page-approval-pack-1400.md`
  - HTML source: `reports/brand-presence-polish/2026-05-20/clinic-dental-leakage-page.html`

## Pre-approval QA checklist

### A. Content and claim safety
- [ ] No invented client results, metrics, testimonials, case-study claims, or implied medical-service claims.
- [ ] “Illustrative workflow example, not a client case study” label remains visible on the clinic/dental resource page.
- [ ] Free review language promises a practical recommendation, not guaranteed revenue, bookings, rankings, or medical outcomes.
- [ ] Safety boundary remains present: do not share passwords, patient records, customer databases, payment details, OTPs, or admin access.
- [ ] Public copy is AICS-only and does not mention Zophire/Zephyr.

### B. Contact and identity checks
- [ ] WhatsApp displayed as `+91 87963 02608` everywhere.
- [ ] WhatsApp links use `https://wa.me/918796302608?...` everywhere.
- [ ] Voice line displayed as `+91 80654 80898` everywhere.
- [ ] Voice links use `tel:+918065480898` where clickable.
- [ ] Primary email displayed as `contact@aicloudstrategist.com`.
- [ ] `support@aicloudstrategist.com` appears only as support reference if used at all.
- [ ] Old WhatsApp number `+91 78383 47711` is absent.
- [ ] Rajiv/Raj personal identity is absent from public copy.

### C. Free Review page implementation checks after approval only
- [ ] Apply only the prepared diff from `free-review-trust-polish-post-approval.diff` unless Raj requests edits.
- [ ] New “What happens next” section appears after “What we check” and before “Book now”.
- [ ] FAQ entries render correctly and expand/collapse on desktop and mobile.
- [ ] FAQPage JSON-LD parses and includes the new FAQ entries.
- [ ] CTA links open the live free-review, WhatsApp, email, and voice routes correctly.
- [ ] Page remains mobile-readable at 360px, 390px, 768px, and desktop widths.

### D. Clinic/Dental resource page implementation checks after approval only
- [ ] Create only the approved URL: `/clinic-dental-lead-leakage-review`.
- [ ] Add exactly one resources hub card pointing to the new URL.
- [ ] Metadata matches the approval pack title, description, and canonical URL.
- [ ] H1, CTA, safety/privacy block, and illustrative-example label render above/before deep scrolling on mobile where practical.
- [ ] Internal links resolve: `/free-business-review`, resources hub card, WhatsApp, email, voice.
- [ ] No page is indexed/staged/published before Raj approval for the exact action.

### E. Post-approval publish gate
- [ ] Raj approval phrase captured exactly for each asset before repo edit/publish:
  - `APPROVE FREE REVIEW TRUST POLISH`
  - `APPROVE CLINIC DENTAL LEAKAGE PAGE`
- [ ] Run local grep after implementation for old number/name/contact regressions.
- [ ] Run link/contact QA and capture evidence paths.
- [ ] Update `reports/approval-dashboard/aics-approval-dashboard-current.*` after any approved implementation.
- [ ] Report published URL/evidence to AICS-Ops only after deployment completes.

## Recommended next approval sequence
1. Keep Sparsh final demo waiting for Raj’s exact approval/rejection; do not send anything to Sparsh yet.
2. Ask Raj for the unresolved diagnostics correction approval before any further diagnostics correction/send.
3. If website polish becomes priority, send the clean founder card for `APPROVE FREE REVIEW TRUST POLISH` first, because it improves the primary conversion path before more outreach.
4. Then request `APPROVE CLINIC DENTAL LEAKAGE PAGE` to strengthen the clinic/dental proof destination.

## Blockers
- Customer/public/external action remains blocked until Raj approves the exact item/action.
- Diagnostics correction remains unresolved pending Raj approval.
- Website repo edit/publish remains blocked pending exact website approval phrase.

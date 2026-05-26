# AICS website QA-only staging checklist — clinic/dental resource + free-review trust block

Prepared: 2026-05-20 15:15 IST  
Status: Internal QA/readiness artifact only. No website repo edit, staging deploy, publish, customer contact, public post, call, spend, credential change, contract action, or destructive action performed.

## Source artifacts reviewed

1. Clinic/dental resource page approval pack: `reports/brand-presence-polish/2026-05-20/clinic-dental-leakage-proof-page-approval-pack-1400.md`
2. Clinic/dental resource page HTML source: `reports/brand-presence-polish/2026-05-20/clinic-dental-leakage-page.html`
3. Free Review trust polish validation: `reports/approval-packs/free-review-trust-polish-20260520-1345/readiness-and-validation.md`
4. Free Review post-approval package: `reports/website-drafts/free-review-trust-polish-implementation-20260520-1330/`

## SOP/contact verification for this run

Live source checked: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 15:15 IST.

Current production contacts confirmed:
- Website: `https://aicloudstrategist.com/`
- Free review: `https://aicloudstrategist.com/free-business-review`
- Primary outreach/customer email: `contact@aicloudstrategist.com`
- Support reference only: `support@aicloudstrategist.com`
- WhatsApp Business: `+91 87963 02608`
- WhatsApp URL: `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
- Voice line: `+91 80654 80898`
- Default public identity/signature rule: Anushka Bhattacharya, Director, AICloudStrategist. The reviewed public page bodies do not use Rajiv personal identity.

## Static preflight performed

| Artifact | Old WhatsApp absent | Current WhatsApp present | Voice line present | `contact@` present | Rajiv public identity absent | Result |
|---|---:|---:|---:|---:|---:|---|
| `clinic-dental-leakage-page.html` | Yes | Yes | Yes | Yes | Yes | Pass |
| `clinic-dental-leakage-proof-page-approval-pack-1400.md` | Yes | Yes | Yes | Yes | Approval-card text only mentions Raj approval mechanics, not production page body | Pass with note |
| `free-business-review.post-approval.html` | Yes | Yes | Yes | Yes | Yes | Pass |
| `free-review-trust-polish-post-approval.diff` | Yes | Yes | Yes | Yes | Yes | Pass |

Search terms checked: old WhatsApp `+91 78383 47711` / `7838347711`, current WhatsApp `+91 87963 02608` / `918796302608`, voice line `+91 80654 80898` / `918065480898`, `contact@aicloudstrategist.com`, and Rajiv personal-name indicators.

## QA-only staging sequence after Raj approval

### Gate 1 — Founder decision required

Do not touch public website files until Raj explicitly approves one or both exact actions:

- `APPROVE CLINIC DENTAL LEAKAGE PAGE`
- `APPROVE FREE REVIEW TRUST POLISH`

If Raj approves only one item, stage only that item. If Raj requests changes, revise the internal source first and rerun this checklist.

### Gate 2 — Local-only implementation checks

For the clinic/dental resource page:
1. Create local route/file for `/clinic-dental-lead-leakage-review` from `clinic-dental-leakage-page.html`.
2. Add one Resources hub card only if the same approval includes the hub card.
3. Confirm canonical: `https://aicloudstrategist.com/clinic-dental-lead-leakage-review`.
4. Confirm page has `index, follow` only when public publish is approved; if staging/noindex preview is requested instead, switch to `noindex, nofollow` for preview.

For the free-review trust block:
1. Apply `free-review-trust-polish-post-approval.diff` to `repos/support-aicloudstrategist.github.io/free-business-review.html` only after approval.
2. Confirm visible FAQ text matches FAQPage JSON-LD.
3. Confirm there is one canonical URL and no duplicate CTA block conflict.

### Gate 3 — Contact and safety QA

Run these checks before any publish:
- No old WhatsApp number: `+91 78383 47711` or `7838347711`.
- WhatsApp link uses `https://wa.me/918796302608`.
- Voice `tel:` link uses `+918065480898`.
- Primary email is `contact@aicloudstrategist.com`.
- `support@aicloudstrategist.com` appears only as support reference, not outreach sender.
- No Rajiv personal public signature or personal identity in page body.
- Free-review safety boundary remains visible: no patient records, passwords, OTPs, payment details, customer databases, or admin access needed.
- No invented claims, client results, testimonials, logos, or unsupported numbers.

### Gate 4 — Layout/link QA evidence

Capture evidence before publish approval is considered complete:
- Desktop screenshot of hero + CTA.
- Mobile screenshot of hero + CTA.
- Screenshot of safety/privacy section.
- Screenshot of resource hub card if added.
- Link-check result for `/free-business-review`, WhatsApp URL, `mailto:contact@aicloudstrategist.com`, and voice `tel:` link.
- HTML/metadata check result for title, meta description, canonical, robots, and JSON-LD.

### Gate 5 — Publish boundary

A local/staging pass is not public-publish approval. If the initial approval only allows staging/noindex preview, return screenshots and QA evidence to Raj for a separate public publish approval before enabling public navigation or deploying as indexable.

## Recommended next action

Send Raj a clean founder review card for the clinic/dental resource page first, because it is already approval-ready and can become a useful healthcare/dental trust asset. Keep the free-review trust polish as the second approval card unless Raj prioritizes conversion-page improvements first.

## Current blocker

Website repo edit, staging deploy, public publish, customer/prospect outreach, WhatsApp send, call, paid action, credential change, contract action, and destructive action all remain blocked until exact Raj approval for the specific action.

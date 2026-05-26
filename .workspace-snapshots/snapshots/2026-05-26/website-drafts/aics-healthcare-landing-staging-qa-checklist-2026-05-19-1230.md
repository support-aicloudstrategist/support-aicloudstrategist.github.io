# AICS Healthcare Landing Page Staging QA Checklist — 2026-05-19 12:30 IST

**Workstream advanced:** website staging readiness → QA and screenshot capture plan  
**Primary approval ID:** `AICS-HC-WEB-STAGE-QA-20260519-1230`  
**Related approval:** `AICS-HC-WEB-STAGE-20260519-1145`  
**Source draft:** `/home/OpenClaw/.openclaw/workspace/reports/website-drafts/aics-healthcare-digital-readiness-audit-2026-05-19-1045.html`  
**FAQ/objection source:** already embedded in the 10:45 HTML draft and referenced by `AICS-HC-WEB-FAQ-20260519-1115`.

## Guardrail

No website deployment, public publishing, customer contact, paid action, contract, credential change, patient-data handling, or external-system edit was performed. This checklist is an internal staging QA artifact only.

## Decision advanced

The staging implementation brief existed, but Raj/developer still needed an exact QA pass list before creating a preview. This artifact closes that gap: once Raj approves staging, the implementer can stage the page, run these checks, capture evidence, and return for final publish approval.

## Must-pass staging checks

| Area | Check | Required result | Evidence to capture |
|---|---|---|---|
| Robots/privacy | `<meta name="robots">` | `noindex, nofollow` remains present on preview | Source snippet or browser devtools screenshot |
| Route | Preview URL | Use staging/preview route only: `/healthcare-digital-readiness-audit?preview=aics-20260519` or equivalent non-public preview URL | Address bar screenshot |
| CTA links | Hero and lower CTA | Both links point to `/free-business-review`; no payment, calendar auto-booking, bulk WhatsApp, or outbound automation is connected | Click/hover screenshot or link inspection |
| Approval identifiers | Top bar/footer/staging note | Shows `AICS-HC-WEB-20260519-1045`, `AICS-HC-WEB-FAQ-20260519-1115`, and `AICS-OFFER-20260519-HEALTHCARE-SCORECARD` in preview context | Desktop screenshot |
| Healthcare disclaimer | Visible disclaimer | Clearly says this is not medical, legal, DPDP, NABH, ABDM, or cybersecurity certification | Screenshot of disclaimer section |
| Patient-data boundary | Sensitive-data note | States no patient data is required for initial review | Screenshot of note/FAQ |
| Pricing | Fee language | Says `₹15,000–₹35,000 + applicable taxes`, scope-dependent; no fixed quote or payment link | Screenshot of pricing card |
| Claims | Proof/guarantees | No testimonials, logos, success metrics, compliance guarantees, medical outcome claims, or unsupported certification wording | Manual pass note |
| Offer scope | Audience fit | Clinics, diagnostic centres, pathology labs, nursing homes, and small hospitals only | Hero/best-fit screenshot |
| CTA language | Ask | Uses 20-minute readiness review language, not hard sales or urgent pressure | Hero/lower CTA screenshot |
| Layout desktop | 1366×768 or similar | Hero readable, cards aligned, table visible, no clipped text | Full-page or top/mid/bottom screenshots |
| Layout mobile | 390×844 or similar | Single-column layout, buttons usable, table readable/scroll-safe, no horizontal overflow | Full-page or top/mid/bottom screenshots |
| Performance basics | Page load | Static page loads without third-party tracking/payment widgets added during staging | Browser network or manual note |
| Final gate | Publish prevention | Preview not linked from live navigation, sitemap, public social, email, WhatsApp, or CRM automation | Implementer confirmation note |

## Screenshot capture list

Save evidence under:

`/home/OpenClaw/.openclaw/workspace/reports/website-drafts/staging-evidence/2026-05-19-healthcare-readiness/`

Required filenames:

1. `desktop-hero-approval-bar.png`
2. `desktop-scope-disclaimer.png`
3. `desktop-deliverables-pricing.png`
4. `desktop-faq-patient-data-boundary.png`
5. `desktop-footer-guardrail.png`
6. `mobile-hero-cta.png`
7. `mobile-scope-disclaimer.png`
8. `mobile-faq-patient-data-boundary.png`
9. `robots-noindex-evidence.png`
10. `cta-link-evidence.png`

## Ready-to-send Raj approval request

```text
APPROVE AICS-HC-WEB-STAGE-20260519-1145: create a noindex staging/preview version of /healthcare-digital-readiness-audit using the approved healthcare scorecard draft, run QA checklist AICS-HC-WEB-STAGE-QA-20260519-1230, capture desktop/mobile screenshots, and return to me for final public-publish approval. Do not publish publicly or promote the URL.
```

## If staging is not approved yet

Continue only internal readiness work: prepare the PDF lead-magnet packaging and discovery-call worksheet, or refine prospect-specific proposal packs. Do not create public links, outreach, payment links, or live site changes without Raj approval of the exact action.

## Next safe action

Prepare a PDF/Google-Doc packaging checklist for the Healthcare Digital Readiness Scorecard so the already-approved website/PDF/discovery offer can be converted into a client-ready lead magnet after Raj confirms the distribution channel.

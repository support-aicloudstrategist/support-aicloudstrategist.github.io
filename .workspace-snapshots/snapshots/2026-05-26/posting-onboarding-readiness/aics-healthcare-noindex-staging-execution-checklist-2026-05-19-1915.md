# AICS Healthcare Noindex Staging Execution Checklist — 2026-05-19 19:15 IST

**Scope:** AICloudStrategist only  
**Queue ID:** `AICS-HC-WEB-STAGE-EXEC-CHECKLIST-20260519-1915`  
**Depends on approval:** `AICS-HC-WEB-STAGE-20260519-1145`  
**Current priority dependency:** keep `/about` publish approval first unless Raj explicitly reprioritises healthcare staging.  
**Guardrail:** This checklist is internal preparation only. No public deployment, navigation/sitemap change, customer contact, public post, payment action, credential change, or destructive action was performed.

## Concrete safe action completed

Prepared the post-approval execution checklist for creating the healthcare landing page as a **noindex staging/preview page** from the clean 19:00 HTML source. This removes execution ambiguity once Raj approves the healthcare staging card.

## Source assets ready

| Asset | Path | Use |
|---|---|---|
| Clean noindex HTML source | `reports/website-drafts/aics-healthcare-digital-readiness-audit-clean-noindex-preview-2026-05-19-1900.html` | Copy into preview page after approval |
| Clean preview manifest | `reports/posting-onboarding-readiness/aics-healthcare-clean-noindex-preview-manifest-2026-05-19-1900.md` | Validation/evidence reference |
| Founder staging card | `reports/approval-packs/aics-healthcare-staging-founder-review-card-2026-05-19-1815.md` | Send after `/about` decision or explicit reprioritisation |
| Website repo | `repos/support-aicloudstrategist.github.io/` | Target repo after approval |
| Current repo blocker | `repos/support-aicloudstrategist.github.io/about.html` modified | Do not mix healthcare staging with pending `/about` approval without explicit Raj direction |

## Exact post-approval implementation path

Use only after Raj replies `APPROVE` to the healthcare noindex staging card.

1. Confirm no unresolved `/about` publish execution is in progress, or Raj explicitly reprioritised healthcare staging.
2. Copy the clean source into a preview-only route:
   - Target candidate: `repos/support-aicloudstrategist.github.io/healthcare-digital-readiness-audit.html`
3. Preserve preview isolation:
   - Keep `<meta name="robots" content="noindex, nofollow">`.
   - Do **not** add the page to `sitemap.xml`.
   - Do **not** add it to top navigation, footer navigation, resources page, social copy, ads, or customer messages.
   - Do **not** add payment links or auto-booking flows.
4. Preserve safe CTA:
   - CTA remains `/free-business-review` only.
5. Preserve healthcare guardrails:
   - Workflow/readiness/backups/access/visibility only.
   - No medical, legal, DPDP, NABH, ABDM, cybersecurity certification, clinical outcome, or guaranteed revenue claim.
   - No patient data needed for initial review.
6. Run local validation before any preview evidence is shared:
   - `grep -qi 'noindex, nofollow' repos/support-aicloudstrategist.github.io/healthcare-digital-readiness-audit.html`
   - `! grep -qi 'approval\|draft\|queue id\|internal' repos/support-aicloudstrategist.github.io/healthcare-digital-readiness-audit.html`
   - `grep -q 'href="/free-business-review"' repos/support-aicloudstrategist.github.io/healthcare-digital-readiness-audit.html`
   - `! grep -q 'healthcare-digital-readiness-audit' repos/support-aicloudstrategist.github.io/sitemap.xml`
7. Capture evidence after staging/preview creation:
   - route/status evidence
   - desktop screenshot
   - mobile screenshot
   - validation result summary
8. Return to Raj for **separate public-publish approval** before any navigation, sitemap, outreach, social post, ad, or public announcement.

## Approval-ready founder card to send later

```text
Approval required for AICloudStrategist healthcare landing-page staging

Identified target: 1 noindex staging/preview page
Channel: AICloudStrategist website preview only, not public navigation
Template/item: Healthcare Digital Readiness Audit landing page + FAQ/objection block

Approve creating a noindex staging preview of /healthcare-digital-readiness-audit using the prepared healthcare landing-page draft and FAQ block, capturing desktop/mobile screenshots, and returning evidence for final public-publish approval.

No public publishing, social posting, customer outreach, payment link, or live navigation change will be done from this approval.

Reply with one option only:
APPROVE
CHANGES
REJECT
```

## Next safe unfinished item

If Raj has not decided the active `/about` approval, keep the queue clean and do not send duplicate founder cards. Continue internal-only preparation: refresh the prospect/follow-up queue, monitor inbound replies, or prepare the next production email approval asset for Raj review without sending to customers.

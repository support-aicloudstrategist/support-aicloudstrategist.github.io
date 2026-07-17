# Navigation and Information Architecture Mapping

## Primary navigation

- Brand mark → `/`
- What We Do → accessible mega menu
- Proof → `/case-studies/`
- Resources → `/resources/`
- About → `/about/`
- Discuss a challenge → `/contact.html`

`Industries` is intentionally excluded from primary navigation. It remains available outside the primary journey until a separate content/SEO retirement decision is approved.

## Mega-menu mapping

### Enterprise AI Services

| New offer | Current canonical page | Interim mapping rationale |
|---|---|---|
| Production AI Assurance | `/services/ai-mlops/` | Closest current page for governed AI/ML delivery, MLOps controls and production readiness. |
| Enterprise AI Systems & Agents | `/services/ai-automation/` | Existing canonical page for agents, workflow automation and governed AI systems. |
| AI FinOps & Cloud Economics | `/services/cloud-finops/` | Existing canonical page for cloud economics, cost controls and FinOps. |
| AI Security, Compliance & Sovereign Platforms | `/services/cloud-security/` | Closest current page for security, compliance and platform controls. |
| Managed AI Platforms & Operations | `/services/devops-observability/` | Closest current page for platform operations, reliability and observability. |

These are interim links, not claims that the legacy page covers every element of the future offer. Each future dedicated pillar page should replace only its corresponding interim mapping.

### Business Growth Systems

| Offer | Canonical page |
|---|---|
| Digital Presence & Search Growth | `/services/website-digital-presence/` |
| Lead Operations & Revenue Automation | `/lead-capture-follow-up/` |
| Digital Trust & Compliance | `/trust-compliance/` |
| Growth & Control Operating System | `/growth-control-os/` |

### Specialist Studio

| Offer | Canonical page |
|---|---|
| AI Creative Studio | `/ai-creative-studio/` |

## Homepage migration

- The former `/home-core-growth/` experience now supplies the root `/` homepage.
- The former Choose Your Path page has been removed from the root journey.
- `/home-core-growth/` is now a migration alias that redirects to `/` and is absent from the sitemap, preventing a duplicate indexed homepage.
- Root canonical and Open Graph URLs point to `https://aicloudstrategist.com/`.

## Shared navigation implementation

The navigation component is maintained in:

- `/css/site-navigation.css`
- `/js/site-navigation.js`

A compact HTML navigation fallback remains visible when JavaScript is unavailable. The enhanced component supports desktop hover, click/touch, keyboard activation, Escape-to-close, outside-click close, mobile scrolling, reduced motion and a non-`backdrop-filter` fallback.

## Pre-deployment recommendations

1. Review the ten interim page mappings with service owners before writing dedicated pillar pages.
2. Keep `/industries.html` out of primary navigation for this release; make deletion/redirect decisions only after checking search traffic and backlinks.
3. Run staging checks for forms, analytics, redirects, CSP/cache headers and mobile behavior on the actual hosting platform.
4. Verify the root and `/home-core-growth/` redirect in the target hosting environment because local static servers do not apply `_redirects` rules.
5. Do not publish dedicated pillar pages until each has unique buyer-oriented copy, evidence boundaries and a single canonical URL.

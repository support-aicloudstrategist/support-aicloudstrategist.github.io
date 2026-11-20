# Publish log — 2026-11-20

## Published / verified
- AICS website / GitHub Pages — Morning: https://support-aicloudstrategist.github.io/publications/2026-11-20/manual-work-automation-readiness-map-live.html/
- GitHub repository / deployment evidence — Morning: https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/2026-11-20

## Discoverability cleanup — 2026-11-20
- Removed a duplicate WhatsApp comparison card from the Resources hub whose title and downloads pointed back to `/resources/` rather than the canonical comparison asset.
- Verification: targeted comparison-link pytest passed; GitHub Pages Resources hub, comparison page and answer-card JSON returned HTTP 200 after propagation, with one canonical comparison card. The custom-domain comparison route remains HTTP 404 and is recorded as a deployment/domain-alignment blocker.

## Infographic
- https://support-aicloudstrategist.github.io/publications/2026-11-20/manual-work-automation-readiness-map.png

## Discoverability repair — 2026-11-20
- Added the small-business AI automation owner checklist, synthetic worksheet and claim-safe answer card to the canonical Resources hub and `llms.txt` so the newest buyer asset is reachable from the evidence library and answer-engine index.
- Local and public verification: hub HTML parsed with one H1 and all three artifact links; CSV parsed with 5 data rows; JSON parsed; no unsupported outcome or customer-proof claim added. After push, GitHub Pages returned HTTP 200 with the new hub/`llms.txt` marker using a commit-scoped cache-busting query; checklist HTML, CSV and JSON routes also returned HTTP 200 with expected content.

## Verification boundary
Educational workflow review only — not a client case study, productivity guarantee, security assessment, legal or compliance advice, vendor recommendation or production-change instruction.

## Discoverability follow-up — 2026-11-20
- Added a Resources-hub card linking the publication page and downloadable worksheet so the artifact is reachable from the canonical evidence library, not only the dated publication index.
- The card labels the artifact as educational and explicitly avoids client-proof or productivity claims.

## Broken-route repair — 2026-11-20
- Restored the previously linked WhatsApp lead follow-up vs CRM comparison, synthetic comparison CSV, owner-map SVG and claim-safe answer card after public route checks found 404s; added verified homepage and Resources-hub links.
- Public GitHub Pages verification after propagation: homepage, Resources hub, comparison page, JSON and CSV all returned HTTP 200 with expected markers.

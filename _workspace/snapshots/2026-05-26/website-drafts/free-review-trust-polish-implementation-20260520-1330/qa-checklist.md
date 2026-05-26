# Free Review Trust Polish — Post-Approval Implementation + QA Checklist

Prepared: 2026-05-20 13:30 IST  
Scope: AICloudStrategist `/free-business-review` only  
Status: Internal post-approval implementation package. No website repo file changed and nothing published.

## SOP gate
- Live contact source checked: `https://aicloudstrategist.com/contact-channels.json` returned 200 at 2026-05-20 13:30 IST.
- WhatsApp Business: `+91 87963 02608` / `https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.`
- Voice line: `+91 80654 80898`.
- Primary email: `contact@aicloudstrategist.com`.
- Support remains support-only.
- No customer/prospect send, public post, call, spend, credential change, or publish action performed.

## Artifact produced this run
- Proposed full post-approval HTML: `free-business-review.post-approval.html`
- Unified diff for implementation: `free-review-trust-polish-post-approval.diff`
- Manifest: `manifest.json`

## What the patch does
1. Adds the approved `What happens next` trust block between `What we check` and `Book now`.
2. Adds two FAQ entries about safe evidence sharing and who the review is suited for.
3. Updates FAQPage JSON-LD so structured data matches the visible FAQ.
4. Preserves current contact channels and avoids old WhatsApp/personal-name usage.

## Post-approval execution steps
1. Confirm Raj approval phrase: `APPROVE FREE REVIEW TRUST POLISH`.
2. Apply the diff to `repos/support-aicloudstrategist.github.io/free-business-review.html`.
3. Run local static validation:
   - `python3 -m http.server 8000` from the repo, then inspect `/free-business-review.html`.
   - Check desktop and mobile viewport.
   - Verify WhatsApp URL, tel link, and mailto link.
   - Verify page still has one canonical URL and valid FAQPage JSON-LD.
4. Capture screenshot evidence.
5. Publish only through the normal approved deployment path.

## Blocker
Public website implementation/publish is blocked until Raj approves the exact website change.

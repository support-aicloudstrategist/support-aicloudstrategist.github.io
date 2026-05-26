# AICS Form CSP Preflight Hardening — 2026-05-23 08:32 IST

Scope: low-noise website/offer quality hardening only. No outreach, public posting, paid action, or remote deploy was performed.

## Concrete improvement made

Hardened the local AICS website preflight so it now catches a production-critical class of lead-capture failure:

- If a public HTML form posts to an external backend such as `https://formsubmit.co`, the checker now verifies that the same origin is allowed by the site `_headers` Content-Security-Policy `form-action` directive.
- This matters because a browser can block the form submission before FormSubmit/Formspree ever receives it, creating silent lead loss even when links, pages, and the backend endpoint look valid.

## Files changed locally

1. `aics-github-sync/operations/website_preflight.py`
   - Added form-action parsing.
   - Added `_headers` CSP parsing.
   - Added `CSP_FORM_ACTION_BLOCK` blocking issue for forms whose action origin is not allowed by CSP.

2. `aics-github-sync/AICloudStrategist.github.io/_headers`
   - Added `https://formsubmit.co` to `form-action`.
   - Added `https://formsubmit.co` to `connect-src` for consistency with form backend usage.

## Finding caught by the new gate

Before the `_headers` fix, the improved preflight found 3 blocking issues:

```text
CSP_FORM_ACTION_BLOCK free-business-review.html -> https://formsubmit.co missing from _headers form-action
CSP_FORM_ACTION_BLOCK index.html -> https://formsubmit.co missing from _headers form-action
CSP_FORM_ACTION_BLOCK local.html -> https://formsubmit.co missing from _headers form-action
```

These pages are core lead-capture entry points, so this was a high-impact quality gap.

## Verification after local fix

Command run:

```bash
cd /home/OpenClaw/.openclaw/workspace/aics-github-sync
python3 operations/website_preflight.py
```

Result:

```text
Site root: /home/OpenClaw/.openclaw/workspace/aics-github-sync/AICloudStrategist.github.io
HTML pages checked: 32
Blocking issues: 0
Warnings: 0
```

## Why it matters for GTM quality

AICS has a known lead-form delivery blocker from the Week 1 brief. This hardening separates two failure classes:

1. Browser/CSP block before the form backend receives the lead.
2. Backend/email delivery issue after the form backend accepts the submission.

With this gate in place, future form-pipeline work can avoid chasing backend/email issues when the real problem is a site security header mismatch.

## Safe next action

Before any public deployment or PR merge, run this preflight against the exact repo/branch being deployed and require:

- `Blocking issues: 0`
- `Warnings: 0` or documented intentional exceptions
- Separate live end-to-end form test with verified inbox message-ID, because CSP pass does not prove email delivery.

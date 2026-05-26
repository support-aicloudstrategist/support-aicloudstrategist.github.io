# PR #6 Merge-and-Test-on-Production — Rule 11 Report (2026-05-23)

GATE STATUS: BLOCKED — Step C failed. Production `/api/lead` returned HTTP 405 instead of HTTP 200, so acceptance failed before email/browser checks. Rollback was executed and pushed. GitHub Pages origin now returns 404 for `/assets/anushka-headshot.png`, but the custom domain still returned 200 after the rollback verification window, indicating Cloudflare/custom-domain edge cache or routing lag remains.

## Step A — DNS prerequisites for MailChannels: PASS, with correction logged

Cloudflare account tag used: `8031172309fe12971ae56861ca12a9cc`
- Note: `GET /accounts` returned HTTP 200 success=true but zero accounts for the scoped token, so I used the same account tag exposed by `GET /zones?name=aicloudstrategist.com` → `zone.account.id`.
- Zone ID: `d62f95edee8549a10c17796946e6935a`

TXT records before changes:
  - aicloudstrategist.com TXT "v=spf1 include:_spf.google.com include:spf.protection.outlook.com include:_spf.resend.com include:amazonses.com ~all" (id 30294907d836ef151c0a2c1a43690758)
  - aicloudstrategist.com TXT MS=ms23692809 (id 74a8842ae10536b186a65640724b4a12)
  - aicloudstrategist.com TXT "google-site-verification=Abhe6m4XXYuUPZZSDzHHKaatfFth7T7tJ9a2VXSaQwY" (id fa7e26c597c81f69be8b510da4beda20)
  - _dmarc.aicloudstrategist.com TXT v=DMARC1; p=none; rua=mailto:support@aicloudstrategist.com; ruf=mailto:support@aicloudstrategist.com; fo=1; aspf=r; adkim=r (id 3a9550eaac01252d319c7d3233ba4ac6)
  - google._domainkey.aicloudstrategist.com TXT v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvb7OAsRoIL0U94CC3B42md79Sr5Wk9uhe0vgUou+3hyxAiU+8m6E+aVrUptrs7jTQL2eCyiG+OSQukvqhpcoBAYA9RrBaTvqnx1udArmM9NIOJHgqxr4dfpWgzlZKGtDueyHf6qJaORYhu7PL/CMDlAz7WIOLkMg8wU+x7TSMWMet//kO07r+G0Qg3V4D9oFofqpaASU+054lU6msPDtnqfvAbaG8D3zWi5ci82GOjBI9DHbQ8alYsVvM0GETIFGdYl5SiRmZVPFcsC369yVAoXCgvG28rDwMQ8lLHbSCjYSlxIG6UdDJe+J6SPKob4aqtiW3kLdT9GSy4Kr+QiUUQIDAQAB (id 2f75538b706b5a6e86006008120da241)
  - resend._domainkey.aicloudstrategist.com TXT "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfEjBEzNRuK/CXfDzjysyFSTFQ/H50nuipHqkPKe4YMVk3r4jNMydr5o8CBmrmMjCuBzz4gEdQiEAajqtuX1B0rmv3ez240fZHbJPhndjuuuKpqhDvBgS455K79SGotdJ3ggcE+FbhJPL6CkhxEY7Z708DLi6JuBuudEOnQOz4DwIDAQAB" (id 8e08dbf1c06024588009b32aa210fe77)
  - send.aicloudstrategist.com TXT "v=spf1 include:amazonses.com ~all" (id 98c40ab8c40c4e807d174246c1bcc6e5)

Initial DNS writes:
  - create_spf: HTTP 200, record_id=485f2cc923254b379db0ab0f178dba8a, value=v=spf1 include:relay.mailchannels.net ~all, success=True
  - create_mailchannels_lockdown: HTTP 200, record_id=5d7db0fb33c1a4c89a8c9bb7a072c53e, value=v=mc1 cfid=8031172309fe12971ae56861ca12a9cc, success=True

Correction applied to comply with “append, do not replace/create duplicate SPF”:
  - update existing SPF: HTTP 200, record_id=30294907d836ef151c0a2c1a43690758, value=v=spf1 include:_spf.google.com include:spf.protection.outlook.com include:_spf.resend.com include:amazonses.com include:relay.mailchannels.net ~all, success=True
  - delete duplicate SPF created during first pass: HTTP 200, record_id=485f2cc923254b379db0ab0f178dba8a, success=True

TXT records after correction:
  - aicloudstrategist.com TXT v=spf1 include:_spf.google.com include:spf.protection.outlook.com include:_spf.resend.com include:amazonses.com include:relay.mailchannels.net ~all (id 30294907d836ef151c0a2c1a43690758)
  - aicloudstrategist.com TXT MS=ms23692809 (id 74a8842ae10536b186a65640724b4a12)
  - aicloudstrategist.com TXT "google-site-verification=Abhe6m4XXYuUPZZSDzHHKaatfFth7T7tJ9a2VXSaQwY" (id fa7e26c597c81f69be8b510da4beda20)
  - _dmarc.aicloudstrategist.com TXT v=DMARC1; p=none; rua=mailto:support@aicloudstrategist.com; ruf=mailto:support@aicloudstrategist.com; fo=1; aspf=r; adkim=r (id 3a9550eaac01252d319c7d3233ba4ac6)
  - google._domainkey.aicloudstrategist.com TXT v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvb7OAsRoIL0U94CC3B42md79Sr5Wk9uhe0vgUou+3hyxAiU+8m6E+aVrUptrs7jTQL2eCyiG+OSQukvqhpcoBAYA9RrBaTvqnx1udArmM9NIOJHgqxr4dfpWgzlZKGtDueyHf6qJaORYhu7PL/CMDlAz7WIOLkMg8wU+x7TSMWMet//kO07r+G0Qg3V4D9oFofqpaASU+054lU6msPDtnqfvAbaG8D3zWi5ci82GOjBI9DHbQ8alYsVvM0GETIFGdYl5SiRmZVPFcsC369yVAoXCgvG28rDwMQ8lLHbSCjYSlxIG6UdDJe+J6SPKob4aqtiW3kLdT9GSy4Kr+QiUUQIDAQAB (id 2f75538b706b5a6e86006008120da241)
  - _mailchannels.aicloudstrategist.com TXT v=mc1 cfid=8031172309fe12971ae56861ca12a9cc (id 5d7db0fb33c1a4c89a8c9bb7a072c53e)
  - resend._domainkey.aicloudstrategist.com TXT "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfEjBEzNRuK/CXfDzjysyFSTFQ/H50nuipHqkPKe4YMVk3r4jNMydr5o8CBmrmMjCuBzz4gEdQiEAajqtuX1B0rmv3ez240fZHbJPhndjuuuKpqhDvBgS455K79SGotdJ3ggcE+FbhJPL6CkhxEY7Z708DLi6JuBuudEOnQOz4DwIDAQAB" (id 8e08dbf1c06024588009b32aa210fe77)
  - send.aicloudstrategist.com TXT "v=spf1 include:amazonses.com ~all" (id 98c40ab8c40c4e807d174246c1bcc6e5)

Cloudflare API responses:
- `/accounts`: HTTP 200, success=True
- zone lookup: HTTP 200, success=True, zone_id=d62f95edee8549a10c17796946e6935a
- TXT list before: HTTP 200, success=True
- TXT list after correction: evidence file below

Evidence files:
- `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/evidence/pr6-dns-mailchannels-20260523.json`
- `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/evidence/pr6-dns-spf-correction-20260523.json`

## Step B — Merge PR #6: PASS

- PR #6 URL: https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/pull/6
- Merge commit SHA: `64226720d40fe5bc12f76eb978dfd76be0eb8495`
- Main HEAD after merge: `64226720d40fe5bc12f76eb978dfd76be0eb8495`
- Deploy verification timestamp: `2026-05-23T04:40:46Z`
- `/assets/anushka-headshot.png` HTTP code after merge: `200`

## Step C — Production E2E form test: FAIL

Submitted at: `2026-05-23T04:40:55Z`

Curl result:
- URL: `https://aicloudstrategist.com/api/lead`
- HTTP status: `405`
- Response body: ``

Response headers:
```text
HTTP/2 405 
date: Sat, 23 May 2026 04:40:55 GMT
content-length: 0
access-control-allow-origin: *
content-security-policy: default-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self' https://formspree.io https://formsubmit.co; script-src 'self' 'unsafe-inline' https://analytics.aicloudstrategist.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.aicloudstrategist.com https://formspree.io https://formsubmit.co https://analytics.aicloudstrategist.com https://cloudflareinsights.com https://*.cloudflareinsights.com; upgrade-insecure-requests
permissions-policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
referrer-policy: strict-origin-when-cross-origin
x-content-type-options: nosniff
x-frame-options: DENY
report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=iFLwPbhr%2Ff4ISN4RukJzQHVnTR3bSfTnPz%2F2TWxLqFQGsiSkILzTR2eOYpbZf6mbqzVGryqFzxPS4Zzk8uwjXpZ%2BWrM0tqFFueswzkcvWdGNPfxSV0TBW8e%2BoH6qJvyxDig60O7jlL051G%2FSpFf7GS2ajWk%3D"}]}
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
server: cloudflare
cf-cache-status: DYNAMIC
strict-transport-security: max-age=31536000
cf-ray: a00162a51b35c63b-SIN
alt-svc: h3=":443"; ma=86400
```

Acceptance evidence:
- `/api/lead` returned HTTP 200 with lead_id/message_id: no
- Email landed in contact@ within 60 seconds: not checked because API failed before send
- Browser form confirmation rendered: not checked because API failed and Step D rollback was required

Diagnostic read: custom domain accepted the PR #6 static asset but `/api/lead` did not route to the Pages Function. This strongly suggests the live custom-domain path is still being served by GitHub Pages/static hosting rather than Cloudflare Pages Functions, or the custom-domain Pages Functions route is not active.

## Step D — Rollback: EXECUTED

- Rollback commit SHA: `fb40968a7c8c6f0abb629253a1cabae47f7152ba`
- New main HEAD: `fb40968a7c8c6f0abb629253a1cabae47f7152ba`
- GitHub Actions rollback deploy: success (`pages-build-deployment`, run 26323708431)
- Local/origin main contains `assets/anushka-headshot.png`: no
- Local/origin main contains `functions/api/lead.ts`: no

Rollback verification:
- `https://support-aicloudstrategist.github.io/assets/anushka-headshot.png` returned 404.
- `https://aicloudstrategist.com/assets/anushka-headshot.png` still returned 200 through the 3-minute verification window.

Custom-domain rollback headers after verification:
```text
HTTP/2 200 
date: Sat, 23 May 2026 04:47:02 GMT
content-type: image/png
content-length: 421836
access-control-allow-origin: *
cache-control: public, max-age=14400, must-revalidate
etag: "cc161097fb2d492bfc209c7bcb5d11d2"
content-security-policy: default-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; script-src 'self' 'unsafe-inline' https://analytics.aicloudstrategist.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.aicloudstrategist.com https://analytics.aicloudstrategist.com https://cloudflareinsights.com https://*.cloudflareinsights.com; upgrade-insecure-requests
permissions-policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
referrer-policy: strict-origin-when-cross-origin
x-content-type-options: nosniff
x-frame-options: DENY
report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=YbETVaONcwuAq9xUa6ogN0cWXvhY2CC0Vq6ifPWtmS7oU6hExwG5VZaCebIUzMcpI8gs9UYYkxKjeu28HdN2998raF6Q%2By6D6qOA9k3dptJ46eTjWeIfdlvwSrphQwAldoF1FTCyjvE%3D"}]}
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
```

GitHub Pages origin headers:
```text
HTTP/2 404 
server: GitHub.com
content-type: text/html; charset=utf-8
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "64d39a40-24a3"
content-security-policy: default-src 'none'; style-src 'unsafe-inline'; img-src data:; connect-src 'self'
x-proxy-cache: MISS
```

## Step E — CRM population: NOT EXECUTED

Step E only begins if Step C passes. Step C failed, rollback executed, and instructions said STOP after rollback. No CRM rows were populated in this run.

## Boundary compliance

- No outreach: confirmed
- No LinkedIn/SEO publishing: confirmed; approval packs remain PENDING
- No contact-channels.json modification: confirmed
- No new scope expansion: confirmed
- No spend: confirmed

## Blocker

Production `/api/lead` is not executing the Cloudflare Pages Function. It returns HTTP 405. Rollback is pushed. GitHub Pages origin verifies rollback with 404 for the Anushka asset, but the custom domain still served the PR #6 asset after the rollback verification window, indicating Cloudflare/custom-domain cache or routing lag. No CRM work performed.

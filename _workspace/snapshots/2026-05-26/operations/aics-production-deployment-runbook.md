# AICloudStrategist Production Deployment Runbook

Last updated: 2026-05-24

## Cloudflare Pages project

- Account ID: `8031172309fe12971ae56861ca12a9cc`
- Project ID: `3df2a6b9-3f08-4186-b193-75e75acfd503`
- Project name: `aicloudstrategist-site`
- Production domains: `aicloudstrategist.com`, `www.aicloudstrategist.com`, `aicloudstrategist-site.pages.dev`
- GitHub binding: `support-aicloudstrategist/support-aicloudstrategist.github.io`
- Production branch: `main`
- Source type: GitHub integration (`github:push`)
- Build command: empty
- Destination directory: `/`
- Root directory: empty

## Form pipeline architecture

1. Website form on `free-business-review.html` sends JSON to `/api/lead`.
2. Cloudflare Pages Function lives at `functions/api/lead.ts`.
3. Function validates required lead fields:
   - `business_name`
   - `website`
   - `whatsapp_number`
   - `vertical`
   - optional `email`, `full_name`, `notes`
4. Function obtains Microsoft Graph app-only token via client credentials.
5. Function sends email through Microsoft Graph:
   - Endpoint: `POST https://graph.microsoft.com/v1.0/users/{M365_SENDER}/sendMail`
   - Sender: `contact@aicloudstrategist.com`
   - Recipient: `contact@aicloudstrategist.com`
6. Email arrives in the contact inbox.
7. Optional KV logging uses `LEAD_LOG` if present. KV failure must not fail the lead submission.

## Current transport: Microsoft Graph

MailChannels is no longer used. MailChannels returned HTTP 401 and is treated as deprecated for this pipeline.

Cloudflare Pages secret names:

- `M365_TENANT_ID`
- `M365_CLIENT_ID`
- `M365_CLIENT_SECRET`
- `M365_SENDER`
- `M365_RECIPIENT`

M365 app facts:

- Tenant ID: `[REDACTED — stored in /home/OpenClaw/.openclaw/secrets/m365-aics-mail-graph.json]`
- Client ID: `[REDACTED — stored in /home/OpenClaw/.openclaw/secrets/m365-aics-mail-graph.json]`
- Sender mailbox: `contact@aicloudstrategist.com`
- Required permission: Microsoft Graph application permission `Mail.Send` with admin consent.
- Also available in current secret metadata: `Mail.ReadWrite`, `User.Read.All`.

### If Graph permission is revoked

Symptoms:

- `/api/lead` returns HTTP 502.
- Response body contains `Email delivery failed` and a Graph details string.
- Direct Graph `sendMail` test returns HTTP 403 / `ErrorAccessDenied`.

Fix:

1. In Azure portal / Microsoft Entra, open the AICS Graph app registration.
2. Confirm API permissions include Microsoft Graph application permission `Mail.Send`.
3. Grant/re-grant admin consent.
4. Re-run direct Graph send test.
5. Re-test preview `/api/lead` before merging any change.

### If app secret is rotated or expired

1. Update `/home/OpenClaw/.openclaw/secrets/m365-aics-mail-graph.json` safely with the new secret.
2. Update Cloudflare Pages secret:
   ```bash
   printf '%s' '<new-secret>' | wrangler pages secret put M365_CLIENT_SECRET --project-name aicloudstrategist-site
   ```
3. Patch both preview and production deployment configs if needed via Cloudflare Pages API so preview receives the same secret.
4. Trigger a preview deployment and test `/api/lead`.
5. Merge only after preview email delivery is verified.

## DNS records relevant to email

Current observed records:

```text
aicloudstrategist.com TXT:
"v=spf1 include:_spf.google.com include:spf.protection.outlook.com include:_spf.resend.com include:amazonses.com include:relay.mailchannels.net ~all"
"MS=ms23692809"
"google-site-verification=Abhe6m4XXYuUPZZSDzHHKaatfFth7T7tJ9a2VXSaQwY"

_mailchannels.aicloudstrategist.com TXT:
"v=mc1 cfid=8031172309fe12971ae56861ca12a9cc"

_dmarc.aicloudstrategist.com TXT:
"v=DMARC1; p=none; rua=mailto:support@aicloudstrategist.com; ruf=mailto:support@aicloudstrategist.com; fo=1; aspf=r; adkim=r"
```

Notes:

- SPF still includes MailChannels but the production form pipeline uses Microsoft Graph.
- Microsoft 365 SPF include is `include:spf.protection.outlook.com`.
- Do not change DNS without explicit founder approval.

## Common failures and fixes

### Function not deployed

Symptoms:

- `POST /api/lead` returns HTTP 405.
- Cloudflare deployment has `uses_functions=false`.
- Deployment manifest does not include `functions/api/lead.ts`.

Checks:

```bash
wrangler pages deployment list --project-name aicloudstrategist-site
curl -i -X POST https://aicloudstrategist.com/api/lead \
  -H 'Content-Type: application/json' \
  -d '{"business_name":"Test","website":"https://test.example.com","whatsapp_number":"+91 87963 02608","vertical":"dental"}'
```

Fix:

- Confirm `functions/api/lead.ts` exists in the deployed commit.
- Confirm Cloudflare Pages project `root_dir` is empty and `destination_dir` is `/`.
- Push a branch and verify preview deployment has `uses_functions=true` before merging.

### Email not arriving

Checks:

1. Confirm `/api/lead` returned HTTP 200.
2. Check contact inbox via Microsoft Graph for subject `Free Lost-Lead Audit request — <business_name>`.
3. If `/api/lead` returned HTTP 502, inspect response details and Pages tail:
   ```bash
   wrangler pages deployment tail --project-name aicloudstrategist-site --environment production --format=json
   ```
4. Directly test Graph send:
   ```bash
   TOKEN=$(curl -s -X POST "https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=<client_id>&client_secret=<secret>&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default" | jq -r .access_token)

   curl -i -X POST "https://graph.microsoft.com/v1.0/users/contact@aicloudstrategist.com/sendMail" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message":{"subject":"AICS Graph Send Test","body":{"contentType":"Text","content":"Test."},"toRecipients":[{"emailAddress":{"address":"contact@aicloudstrategist.com"}}]},"saveToSentItems":"true"}'
   ```

### Build errors

Checks:

```bash
wrangler pages deployment list --project-name aicloudstrategist-site
# open build URL shown in deployment list
```

Fix:

- Inspect Cloudflare Pages build logs.
- Keep build command empty unless the repo structure changes.
- Do not merge failing previews.

## OAuth login recovery for Cloudflare/Wrangler

When Wrangler token expires:

1. Start visible/noVNC browser if founder login is needed.
2. Run:
   ```bash
   wrangler login --browser=false
   ```
3. Copy the printed Cloudflare OAuth URL for founder approval/login.
4. If the local callback cannot be reached from founder phone, open the OAuth URL in the shared Ubuntu browser so the callback to `localhost:8976` completes on the same machine.
5. If needed, use the browser/noVNC LAN URL, not localhost, for founder interaction.
6. Verify:
   ```bash
   wrangler whoami
   wrangler pages project list
   wrangler pages deployment list --project-name aicloudstrategist-site
   ```

Expected account:

```text
Rajivjobnaukri@gmail.com's Account
8031172309fe12971ae56861ca12a9cc
```

## Production curl test examples

```bash
curl -i -X POST "https://aicloudstrategist.com/api/lead" \
  -H "Content-Type: application/json" \
  -d '{"business_name":"AICS Production E2E","website":"https://test.example.com","whatsapp_number":"+91 87963 02608","vertical":"dental","email":"contact@aicloudstrategist.com"}'
```

Expected:

- HTTP 200
- JSON body with `{"ok":true,"lead_id":"..."}`
- Email in `contact@aicloudstrategist.com` inbox.

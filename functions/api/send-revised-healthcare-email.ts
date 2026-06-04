type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type TokenCache = { token: string; expiresAt: number };
let tokenCache: TokenCache | null = null;

const clean = (value: unknown) => String(value ?? "").trim();

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);

  if (!tenantId || !clientId || !clientSecret) {
    throw new Error("Microsoft Graph credentials are not configured.");
  }

  const now = Date.now();
  if (tokenCache && tokenCache.expiresAt - 60_000 > now) {
    return tokenCache.token;
  }

  const body = new URLSearchParams({
    grant_type: "client_credentials",
    client_id: clientId,
    client_secret: clientSecret,
    scope: "https://graph.microsoft.com/.default",
  });

  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  const payload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !payload.access_token) {
    throw new Error(payload.error_description || payload.error || `Graph token failed with ${response.status}.`);
  }

  tokenCache = {
    token: payload.access_token,
    expiresAt: now + Math.max(60, payload.expires_in || 3600) * 1000,
  };

  return tokenCache.token;
}

function buildHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Patient Enquiry Leakage Snapshot</title>
</head>
<body style="margin:0;background:#f3f7fb;font-family:Arial,Helvetica,sans-serif;color:#102033;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;">A simple 1-page clinic audit showing missed enquiry points, competitor signals, quick wins and possible ROI.</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f3f7fb;padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:720px;background:#ffffff;border-radius:22px;overflow:hidden;box-shadow:0 18px 50px rgba(16,32,51,.12);">
          <tr>
            <td style="background:linear-gradient(135deg,#071a33,#0d7282);padding:30px 30px 26px;color:#ffffff;">
              <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#a8f2ff;font-weight:700;">AICloudStrategist</div>
              <h1 style="margin:12px 0 10px;font-size:29px;line-height:1.15;">Quick patient enquiry check for CityCare Dental Clinic</h1>
              <p style="margin:0;font-size:16px;line-height:1.55;color:#e7fbff;">A simple way to see where new patient bookings may be getting missed — before buying any system or starting a large project.</p>
            </td>
          </tr>

          <tr>
            <td style="padding:28px 30px 8px;">
              <p style="margin:0 0 16px;font-size:16px;line-height:1.65;">Hi Dr. Mehta,</p>
              <p style="margin:0 0 16px;font-size:16px;line-height:1.65;">Many clinics are not losing patients because the doctor is weak. They lose patients because the booking journey is not clear enough, calls/WhatsApp messages are not followed up fast enough, or patients compare nearby clinics and choose the one that feels easier to contact.</p>
              <p style="margin:0 0 16px;font-size:16px;line-height:1.65;">We can prepare a <strong>1-page Patient Enquiry Leakage Snapshot</strong> for CityCare Dental Clinic so you can see the issue clearly in business language — not technical language.</p>
            </td>
          </tr>

          <tr>
            <td style="padding:6px 30px 4px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #d9e8f2;border-radius:18px;background:#f8fcff;">
                <tr>
                  <td style="padding:22px;">
                    <h2 style="margin:0 0 14px;font-size:21px;color:#071a33;">What the 1-page audit will show</h2>
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                      <tr>
                        <td style="padding:10px 0;border-bottom:1px solid #e2edf5;"><strong>1. Patient journey map</strong><br><span style="color:#456;line-height:1.5;">Search → website → reviews → call/WhatsApp → follow-up → appointment. We mark where a patient may drop off.</span></td>
                      </tr>
                      <tr>
                        <td style="padding:10px 0;border-bottom:1px solid #e2edf5;"><strong>2. Missed enquiry leakage points</strong><br><span style="color:#456;line-height:1.5;">Missed calls, slow replies, unclear booking button, weak form confirmation, or no reminder flow.</span></td>
                      </tr>
                      <tr>
                        <td style="padding:10px 0;border-bottom:1px solid #e2edf5;"><strong>3. Nearby competitor snapshot</strong><br><span style="color:#456;line-height:1.5;">How nearby clinics appear on reviews, booking clarity, trust signals, and patient-friendly information.</span></td>
                      </tr>
                      <tr>
                        <td style="padding:10px 0;border-bottom:1px solid #e2edf5;"><strong>4. Simple opportunity estimate</strong><br><span style="color:#456;line-height:1.5;">A conservative view of what even 2–5 recovered bookings per month could mean, based on available information.</span></td>
                      </tr>
                      <tr>
                        <td style="padding:10px 0;"><strong>5. Top 3 quick wins</strong><br><span style="color:#456;line-height:1.5;">The first improvements to try before spending on a bigger system.</span></td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:20px 30px 4px;">
              <h2 style="margin:0 0 14px;font-size:21px;color:#071a33;">Example of what the snapshot may include</h2>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td style="width:33%;padding:8px;vertical-align:top;">
                    <div style="border-radius:16px;background:#fff7e6;border:1px solid #ffe0a6;padding:16px;min-height:128px;">
                      <div style="font-size:13px;color:#9a5b00;font-weight:700;">Leakage point</div>
                      <div style="font-size:16px;font-weight:700;margin:8px 0;color:#241600;">Patient has to search too much to book</div>
                      <div style="font-size:14px;line-height:1.5;color:#5f4320;">Fix: visible call and WhatsApp buttons on mobile.</div>
                    </div>
                  </td>
                  <td style="width:33%;padding:8px;vertical-align:top;">
                    <div style="border-radius:16px;background:#eaf9ff;border:1px solid #c5edf8;padding:16px;min-height:128px;">
                      <div style="font-size:13px;color:#006179;font-weight:700;">Opportunity</div>
                      <div style="font-size:16px;font-weight:700;margin:8px 0;color:#073040;">Recover 2–5 bookings/month</div>
                      <div style="font-size:14px;line-height:1.5;color:#2c5563;">Indicative only, depending on actual enquiries and response process.</div>
                    </div>
                  </td>
                  <td style="width:33%;padding:8px;vertical-align:top;">
                    <div style="border-radius:16px;background:#effbf0;border:1px solid #cdeecf;padding:16px;min-height:128px;">
                      <div style="font-size:13px;color:#14712a;font-weight:700;">Quick win</div>
                      <div style="font-size:16px;font-weight:700;margin:8px 0;color:#113b1a;">Instant follow-up flow</div>
                      <div style="font-size:14px;line-height:1.5;color:#315a39;">Missed call → WhatsApp reply → appointment link → reminder.</div>
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding:18px 30px 4px;">
              <div style="background:#071a33;border-radius:18px;padding:22px;color:#ffffff;">
                <h2 style="margin:0 0 10px;font-size:21px;">Why this helps the clinic owner</h2>
                <p style="margin:0 0 12px;font-size:15px;line-height:1.6;color:#dcecff;">You do not have to guess whether the problem is website, staff follow-up, WhatsApp, reviews, reminders, or booking clarity. The audit puts the main gaps on one page, with the first practical fix.</p>
                <p style="margin:0;font-size:15px;line-height:1.6;color:#dcecff;">If the opportunity is small, you know before spending. If the opportunity is meaningful, we can start with a small measurable workflow first.</p>
              </div>
            </td>
          </tr>

          <tr>
            <td style="padding:24px 30px 30px;">
              <p style="margin:0 0 14px;font-size:16px;line-height:1.65;">Should I send this 1-page snapshot for CityCare Dental Clinic?</p>
              <p style="margin:0 0 20px;font-size:16px;line-height:1.65;">If useful, we can also do a short 15-minute walkthrough and show which fix is easiest to implement first.</p>
              <a href="mailto:contact@aicloudstrategist.com?subject=Send%20the%201-page%20Patient%20Enquiry%20Snapshot" style="display:inline-block;background:#08a4bd;color:#ffffff;text-decoration:none;font-weight:700;border-radius:999px;padding:13px 22px;">Yes, send the 1-page snapshot</a>
              <p style="margin:22px 0 0;font-size:15px;line-height:1.6;color:#526575;">Warmly,<br><strong>Anushka Bhattacharya</strong><br>Director, AICloudStrategist<br><a href="https://aicloudstrategist.com" style="color:#087f95;">aicloudstrategist.com</a></p>
              <p style="margin:18px 0 0;font-size:12px;line-height:1.5;color:#7b8b99;">Note: Any opportunity estimate is indicative only and depends on actual enquiry volume, patient response behaviour, team process, and implementation quality. It is not a guaranteed revenue result.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
}

export const onRequest: PagesFunction<Env> = async ({ request, env }) => {
  if (request.method !== "POST") {
    return new Response(JSON.stringify({ ok: false, error: "method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }

  try {
    const sender = clean(env.M365_SENDER);
    if (!sender) throw new Error("Microsoft Graph sender is not configured.");

    const token = await getGraphToken(env);
    const subject = "Revised: 1-page Patient Enquiry Leakage Snapshot for CityCare Dental Clinic";
    const html = buildHtml();

    const graphResponse = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: {
          subject,
          body: { contentType: "HTML", content: html },
          toRecipients: [
            { emailAddress: { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" } },
            { emailAddress: { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" } }
          ],
          replyTo: [{ emailAddress: { address: sender, name: "AICloudStrategist" } }],
        },
        saveToSentItems: true,
      }),
    });

    const responseText = await graphResponse.text();
    if (!graphResponse.ok) {
      return new Response(JSON.stringify({ ok: false, status: graphResponse.status, error: responseText }), {
        status: 502,
        headers: { "Content-Type": "application/json; charset=utf-8" },
      });
    }

    return new Response(JSON.stringify({ ok: true, sender, subject, status: graphResponse.status }), {
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), {
      status: 500,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }
};

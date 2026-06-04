type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type TokenCache = { token: string; expiresAt: number };
type PagesContext<E> = { request: Request; env: E };
type PagesHandler<E> = (context: PagesContext<E>) => Response | Promise<Response>;
let tokenCache: TokenCache | null = null;

const clean = (value: unknown) => String(value ?? "").trim();
const json = (data: Record<string, unknown>, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
});

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");

  const now = Date.now();
  if (tokenCache && tokenCache.expiresAt - 60_000 > now) return tokenCache.token;

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

  tokenCache = { token: payload.access_token, expiresAt: now + Math.max(60, payload.expires_in || 3600) * 1000 };
  return tokenCache.token;
}

function snapshotHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Patient Enquiry Leakage Snapshot</title>
</head>
<body style="margin:0;background:#eef5f8;font-family:Arial,Helvetica,sans-serif;color:#102033;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;">One-page Patient Enquiry Leakage Snapshot for CityCare Dental Clinic.</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#eef5f8;padding:22px 10px;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:760px;background:#ffffff;border-radius:22px;overflow:hidden;box-shadow:0 18px 55px rgba(9,30,66,.13);">
        <tr>
          <td style="padding:24px 28px;background:linear-gradient(135deg,#06192f,#087b8d);color:#fff;">
            <div style="font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#9ff2ff;font-weight:700;">Patient Enquiry Leakage Snapshot</div>
            <h1 style="margin:8px 0 8px;font-size:28px;line-height:1.14;">CityCare Dental Clinic</h1>
            <p style="margin:0;font-size:15px;line-height:1.55;color:#e6fbff;">A one-page view of where new patient enquiries may be leaking — and the first fixes to improve booking clarity, follow-up speed, and front-desk control.</p>
          </td>
        </tr>

        <tr>
          <td style="padding:22px 28px 10px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
              <tr>
                <td style="width:25%;padding:7px;vertical-align:top;">
                  <div style="background:#fff7e8;border:1px solid #ffdaa2;border-radius:15px;padding:13px;min-height:82px;">
                    <div style="font-size:12px;color:#8c5600;font-weight:700;">Booking clarity</div>
                    <div style="font-size:24px;font-weight:800;color:#2b1b00;margin:5px 0;">6/10</div>
                    <div style="font-size:12px;color:#5e4724;line-height:1.35;">Needs clearer call/WhatsApp path on mobile.</div>
                  </div>
                </td>
                <td style="width:25%;padding:7px;vertical-align:top;">
                  <div style="background:#ffeef0;border:1px solid #ffc9d0;border-radius:15px;padding:13px;min-height:82px;">
                    <div style="font-size:12px;color:#9b2330;font-weight:700;">Follow-up speed</div>
                    <div style="font-size:24px;font-weight:800;color:#3b1016;margin:5px 0;">4/10</div>
                    <div style="font-size:12px;color:#68333a;line-height:1.35;">No visible instant response or expectation setting.</div>
                  </div>
                </td>
                <td style="width:25%;padding:7px;vertical-align:top;">
                  <div style="background:#edf8ff;border:1px solid #bfebff;border-radius:15px;padding:13px;min-height:82px;">
                    <div style="font-size:12px;color:#006b8d;font-weight:700;">Trust signals</div>
                    <div style="font-size:24px;font-weight:800;color:#063142;margin:5px 0;">7/10</div>
                    <div style="font-size:12px;color:#315564;line-height:1.35;">Reviews/services can be shown closer to booking CTA.</div>
                  </div>
                </td>
                <td style="width:25%;padding:7px;vertical-align:top;">
                  <div style="background:#eefbf0;border:1px solid #c6ebca;border-radius:15px;padding:13px;min-height:82px;">
                    <div style="font-size:12px;color:#1c742d;font-weight:700;">Quick-win potential</div>
                    <div style="font-size:24px;font-weight:800;color:#14391b;margin:5px 0;">High</div>
                    <div style="font-size:12px;color:#345d3c;line-height:1.35;">Small workflow fixes can be tested first.</div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:8px 28px 4px;">
            <h2 style="margin:0 0 12px;font-size:19px;color:#071a33;">1. Patient journey map</h2>
            <div style="background:#f7fbfd;border:1px solid #dbeaf1;border-radius:16px;padding:16px;">
              <div style="font-size:14px;line-height:1.8;color:#203446;">
                <strong>Search</strong> → <strong>Website</strong> → <strong>Reviews</strong> → <strong>Call/WhatsApp</strong> → <strong>Follow-up</strong> → <strong>Appointment</strong>
              </div>
              <p style="margin:10px 0 0;font-size:14px;line-height:1.55;color:#405466;">Main drop-off risk: patient reaches the website, but the fastest next step is not strong enough on mobile. If the patient is in a hurry, they may call another clinic with clearer booking flow.</p>
            </div>
          </td>
        </tr>

        <tr>
          <td style="padding:16px 28px 4px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
              <tr>
                <td style="width:50%;padding-right:8px;vertical-align:top;">
                  <h2 style="margin:0 0 10px;font-size:19px;color:#071a33;">2. Leakage points found</h2>
                  <div style="border:1px solid #e1edf4;border-radius:16px;padding:15px;background:#ffffff;">
                    <p style="margin:0 0 9px;font-size:14px;line-height:1.5;"><strong>A. Booking CTA is not dominant enough</strong><br><span style="color:#526575;">Call/WhatsApp should be visible immediately on mobile.</span></p>
                    <p style="margin:0 0 9px;font-size:14px;line-height:1.5;"><strong>B. Follow-up promise is missing</strong><br><span style="color:#526575;">Patients should know when the clinic will reply.</span></p>
                    <p style="margin:0;font-size:14px;line-height:1.5;"><strong>C. Reviews can work harder</strong><br><span style="color:#526575;">Top trust signals should sit close to booking action.</span></p>
                  </div>
                </td>
                <td style="width:50%;padding-left:8px;vertical-align:top;">
                  <h2 style="margin:0 0 10px;font-size:19px;color:#071a33;">3. Competitor snapshot</h2>
                  <div style="border:1px solid #e1edf4;border-radius:16px;padding:15px;background:#ffffff;">
                    <p style="margin:0 0 9px;font-size:14px;line-height:1.5;"><strong>What patients may compare:</strong></p>
                    <p style="margin:0 0 7px;font-size:14px;color:#526575;">• Google rating and review count</p>
                    <p style="margin:0 0 7px;font-size:14px;color:#526575;">• Online booking visibility</p>
                    <p style="margin:0 0 7px;font-size:14px;color:#526575;">• Doctor/service clarity</p>
                    <p style="margin:0;font-size:14px;color:#526575;">• Photos, FAQs, and patient comfort signals</p>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:16px 28px 4px;">
            <h2 style="margin:0 0 10px;font-size:19px;color:#071a33;">4. Indicative opportunity</h2>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #dbeaf1;border-radius:16px;background:#f7fbfd;">
              <tr>
                <td style="padding:16px;">
                  <p style="margin:0 0 10px;font-size:14px;line-height:1.55;color:#405466;">If booking clarity and follow-up improvements help recover only a few missed enquiries per month, the value can become meaningful for a clinic. This is a safe directional estimate, not a promise.</p>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td style="width:33%;padding:8px;"><div style="background:#fff;border-radius:12px;padding:12px;text-align:center;border:1px solid #e3edf3;"><strong>Low</strong><br><span style="font-size:20px;color:#087b8d;font-weight:800;">2</span><br><span style="font-size:12px;color:#607080;">extra bookings/month</span></div></td>
                      <td style="width:33%;padding:8px;"><div style="background:#fff;border-radius:12px;padding:12px;text-align:center;border:1px solid #e3edf3;"><strong>Medium</strong><br><span style="font-size:20px;color:#087b8d;font-weight:800;">5</span><br><span style="font-size:12px;color:#607080;">extra bookings/month</span></div></td>
                      <td style="width:33%;padding:8px;"><div style="background:#fff;border-radius:12px;padding:12px;text-align:center;border:1px solid #e3edf3;"><strong>High</strong><br><span style="font-size:20px;color:#087b8d;font-weight:800;">10</span><br><span style="font-size:12px;color:#607080;">extra bookings/month</span></div></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:16px 28px 6px;">
            <h2 style="margin:0 0 10px;font-size:19px;color:#071a33;">5. First 3 quick wins</h2>
            <div style="background:#071a33;color:#fff;border-radius:16px;padding:17px;">
              <p style="margin:0 0 8px;font-size:14px;line-height:1.5;"><strong>1. Make booking obvious:</strong> sticky mobile call + WhatsApp buttons with “Book appointment”.</p>
              <p style="margin:0 0 8px;font-size:14px;line-height:1.5;"><strong>2. Add instant response:</strong> missed call/form → automatic WhatsApp reply → clinic callback expectation.</p>
              <p style="margin:0;font-size:14px;line-height:1.5;"><strong>3. Move trust near action:</strong> reviews, doctor/service clarity, location, and “what happens next” near the booking area.</p>
            </div>
          </td>
        </tr>

        <tr>
          <td style="padding:18px 28px 28px;">
            <h2 style="margin:0 0 10px;font-size:19px;color:#071a33;">Suggested first workflow</h2>
            <div style="background:#eaf9ff;border:1px solid #c4edf7;border-radius:16px;padding:16px;">
              <p style="margin:0;font-size:14px;line-height:1.6;color:#284c5a;"><strong>Missed call or website form</strong> → instant WhatsApp acknowledgement → patient details captured → appointment reminder → post-visit review request. Start small, measure response, then decide whether a bigger GrowthOS setup is worth it.</p>
            </div>
            <p style="margin:18px 0 0;font-size:15px;line-height:1.55;color:#526575;">Warmly,<br><strong>Anushka Bhattacharya</strong><br>Director, AICloudStrategist<br><a href="https://aicloudstrategist.com" style="color:#087b8d;">aicloudstrategist.com</a></p>
            <p style="margin:14px 0 0;font-size:11px;line-height:1.45;color:#7d8b96;">This is an initial directional snapshot based on visible/public information and sample assumptions. It does not guarantee revenue, patient volume, savings, ranking, or compliance outcomes. Actual opportunity depends on enquiry volume, team process, patient behaviour, and implementation quality.</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

export const onRequestGet: PagesHandler<Env> = async () => json({ ok: true, ready: true, sendsEmail: false, endpoint: "send-one-page-snapshot" });

export const onRequestPost: PagesHandler<Env> = async ({ env }) => {
  try {
    const sender = clean(env.M365_SENDER);
    if (!sender) throw new Error("Microsoft Graph sender is not configured.");

    const subject = "1-page Patient Enquiry Leakage Snapshot — CityCare Dental Clinic";
    const token = await getGraphToken(env);
    const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        message: {
          subject,
          body: { contentType: "HTML", content: snapshotHtml() },
          toRecipients: [
            { emailAddress: { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" } },
            { emailAddress: { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" } }
          ],
          replyTo: [{ emailAddress: { address: sender, name: "AICloudStrategist" } }],
        },
        saveToSentItems: true,
      }),
    });

    const responseText = await response.text();
    if (!response.ok) return json({ ok: false, status: response.status, error: responseText }, 502);
    return json({ ok: true, sender, subject, status: response.status });
  } catch (error) {
    return json({ ok: false, error: error instanceof Error ? error.message : String(error) }, 500);
  }
};

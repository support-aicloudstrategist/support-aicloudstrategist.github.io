type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const clean = (value: unknown) => String(value ?? "").trim();
const recipients = [
  { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" },
  { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" },
];

const subject = "Quick patient enquiry check for CityCare Dental Clinic";

const html = `<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${subject}</title></head>
<body style="margin:0;padding:0;background:#eef4fb;font-family:Arial,Helvetica,sans-serif;color:#0f172a;">
  <div style="display:none;max-height:0;overflow:hidden;color:transparent;opacity:0;">A quick check of your patient enquiry journey shows one possible leakage point.</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#eef4fb;padding:28px 0;">
    <tr><td align="center" style="padding:0 12px;">
      <table role="presentation" width="640" cellspacing="0" cellpadding="0" style="width:640px;max-width:100%;background:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 18px 50px rgba(15,23,42,.14);">
        <tr>
          <td style="background:linear-gradient(135deg,#071426,#0b2b4a);padding:22px 26px;color:#ffffff;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
              <td style="font-size:19px;font-weight:800;letter-spacing:.2px;">AI<span style="color:#22d3ee;">Cloud</span>Strategist</td>
              <td align="right" style="font-size:12px;color:#bfdbfe;">Patient enquiry recovery</td>
            </tr></table>
          </td>
        </tr>
        <tr>
          <td style="padding:34px 30px 18px;background:linear-gradient(180deg,#ffffff,#f8fbff);">
            <div style="display:inline-block;background:#0891b2;color:#ffffff;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:8px 12px;border-radius:999px;">Quick patient journey check</div>
            <h1 style="font-size:30px;line-height:1.14;margin:18px 0 12px;color:#0f172a;">Are patient enquiries getting missed before they become appointments?</h1>
            <p style="font-size:16px;line-height:1.6;margin:0;color:#334155;">Hi Dr. Mehta,</p>
            <p style="font-size:16px;line-height:1.6;margin:14px 0 0;color:#334155;">I checked CityCare Dental Clinic’s online patient enquiry journey and noticed one possible leakage point: patients are mainly guided to call, but there does not seem to be a simple instant WhatsApp or booking follow-up flow.</p>
            <p style="font-size:16px;line-height:1.6;margin:14px 0 0;color:#334155;">Many clinics lose enquiries not because of poor care, but because calls are missed during busy hours, follow-ups depend on staff memory, or patients do not get a quick response after showing interest.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:4px 30px 8px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#ecfeff;border:1px solid #bae6fd;border-radius:18px;">
              <tr><td style="padding:20px;">
                <div style="font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#0891b2;margin-bottom:10px;">Quick value estimate</div>
                <div style="font-size:15.5px;line-height:1.7;color:#334155;">If only <strong>5 patient enquiries</strong> are missed per week and average billing value is around <strong>₹1,500</strong>, possible monthly leakage can be around <strong style="color:#0f766e;">₹30,000</strong>.</div>
                <div style="font-size:12px;color:#64748b;margin-top:10px;line-height:1.5;">This is an indicative estimate. Actual value depends on enquiry volume, patient conversion, staff follow-up, and existing systems.</div>
              </td></tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:12px 30px 8px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f8fafc;border:1px solid #dbeafe;border-radius:18px;">
              <tr><td style="padding:20px 20px 8px;">
                <div style="font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#0891b2;margin-bottom:10px;">Mini audit snapshot</div>
                <div style="font-size:15px;line-height:1.5;color:#334155;margin:0 0 12px;"><span style="display:inline-block;width:8px;height:8px;background:#f59e0b;border-radius:99px;margin-right:9px;"></span><strong>Patient booking path:</strong> needs clearer instant action.</div>
                <div style="font-size:15px;line-height:1.5;color:#334155;margin:0 0 12px;"><span style="display:inline-block;width:8px;height:8px;background:#f59e0b;border-radius:99px;margin-right:9px;"></span><strong>Follow-up risk:</strong> manual calls may miss busy-hour enquiries.</div>
                <div style="font-size:15px;line-height:1.5;color:#334155;margin:0 0 12px;"><span style="display:inline-block;width:8px;height:8px;background:#0891b2;border-radius:99px;margin-right:9px;"></span><strong>Quick win:</strong> missed-call reply + WhatsApp appointment capture + reminder flow.</div>
                <div style="font-size:15px;line-height:1.5;color:#334155;margin:0 0 12px;"><span style="display:inline-block;width:8px;height:8px;background:#10b981;border-radius:99px;margin-right:9px;"></span><strong>Possible benefit:</strong> fewer lost enquiries and less front-desk pressure.</div>
              </td></tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:14px 30px 8px;">
            <h2 style="font-size:22px;line-height:1.25;margin:0 0 10px;color:#0f172a;">What we can send you</h2>
            <p style="font-size:15.5px;line-height:1.62;margin:0;color:#334155;">We can prepare a simple 1-page audit for CityCare Dental Clinic showing where patient enquiries may be leaking and what can be fixed first without changing your full system.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:10px 30px 26px;">
            <table role="presentation" cellspacing="0" cellpadding="0"><tr><td bgcolor="#0891b2" style="border-radius:999px;">
              <a href="mailto:contact@aicloudstrategist.com?subject=Please send the 1-page audit" style="display:inline-block;padding:15px 24px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:800;border-radius:999px;">Yes, send the 1-page audit</a>
            </td></tr></table>
            <p style="font-size:14px;line-height:1.6;margin:18px 0 0;color:#475569;">You can also reply to this email with your website link, and we will suggest the first improvement areas.</p>
          </td>
        </tr>
        <tr>
          <td style="background:#071426;color:#cbd5e1;padding:22px 30px;font-size:13px;line-height:1.6;">
            <strong style="color:#ffffff;">Anushka Bhattacharya</strong><br>
            Director, AICloudStrategist<br>
            <a href="mailto:contact@aicloudstrategist.com" style="color:#67e8f9;text-decoration:none;">contact@aicloudstrategist.com</a> · <a href="https://aicloudstrategist.com" style="color:#67e8f9;text-decoration:none;">aicloudstrategist.com</a><br>
            +91 80654 80898<br>
            If this is not relevant, reply “not interested” and we will not email again.
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");
  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) return graphTokenCache.token;
  const body = new URLSearchParams({ grant_type: "client_credentials", client_id: clientId, client_secret: clientSecret, scope: "https://graph.microsoft.com/.default" });
  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
  const payload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !payload.access_token) throw new Error(payload.error_description || payload.error || `Graph token request failed with ${response.status}.`);
  graphTokenCache = { token: payload.access_token, expiresAt: now + Math.max(60, payload.expires_in || 3600) * 1000 };
  return graphTokenCache.token;
}

async function sendGraphMail(env: Env, message: Record<string, unknown>) {
  const sender = clean(env.M365_SENDER) || "contact@aicloudstrategist.com";
  const token = await getGraphToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ message, saveToSentItems: true }),
  });
  const responseText = await response.text();
  if (!response.ok) throw new Error(responseText || `Graph sendMail failed with ${response.status}.`);
  return { status: response.status, responseText };
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  try {
    const result = await sendGraphMail(context.env, {
      subject,
      body: { contentType: "HTML", content: html },
      toRecipients: recipients.map((emailAddress) => ({ emailAddress })),
      replyTo: [{ emailAddress: { address: "contact@aicloudstrategist.com", name: "AICloudStrategist" } }],
    });
    return new Response(JSON.stringify({ ok: true, sender: clean(context.env.M365_SENDER) || "contact@aicloudstrategist.com", subject, status: result.status }), { status: 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  }
};

export const onRequestGet: PagesFunction = async () => new Response(JSON.stringify({ ok: false, error: "not found" }), { status: 404, headers: { "Content-Type": "application/json" } });

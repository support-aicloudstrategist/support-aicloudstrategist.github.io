type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const clean = (value: unknown) => String(value ?? "").trim();
const approvalRecipients = [
  { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" },
  { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" },
];

const baseStyles = `margin:0;padding:0;background:#eef4fb;font-family:Arial,Helvetica,sans-serif;color:#0f172a;`;

function shell(title: string, eyebrow: string, intro: string, points: string[], ctaText: string, ctaUrl: string, accent = "#0891b2") {
  return `<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head>
<body style="${baseStyles}">
  <div style="display:none;max-height:0;overflow:hidden;color:transparent;opacity:0;">${intro}</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#eef4fb;padding:28px 0;">
    <tr><td align="center" style="padding:0 12px;">
      <table role="presentation" width="640" cellspacing="0" cellpadding="0" style="width:640px;max-width:100%;background:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 18px 50px rgba(15,23,42,.14);">
        <tr>
          <td style="background:linear-gradient(135deg,#071426,#0b2b4a);padding:22px 26px;color:#ffffff;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
              <td style="font-size:19px;font-weight:800;letter-spacing:.2px;">AI<span style="color:#22d3ee;">Cloud</span>Strategist</td>
              <td align="right" style="font-size:12px;color:#bfdbfe;">Growth & Control for serious businesses</td>
            </tr></table>
          </td>
        </tr>
        <tr>
          <td style="padding:34px 30px 18px;background:linear-gradient(180deg,#ffffff,#f8fbff);">
            <div style="display:inline-block;background:${accent};color:#ffffff;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:8px 12px;border-radius:999px;">${eyebrow}</div>
            <h1 style="font-size:30px;line-height:1.14;margin:18px 0 12px;color:#0f172a;">${title}</h1>
            <p style="font-size:17px;line-height:1.58;margin:0;color:#334155;">${intro}</p>
          </td>
        </tr>
        <tr>
          <td style="padding:4px 30px 8px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f8fafc;border:1px solid #dbeafe;border-radius:18px;">
              <tr><td style="padding:20px 20px 8px;">
                <div style="font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:${accent};margin-bottom:10px;">Where value is usually lost</div>
                ${points.map((p) => `<div style="font-size:15px;line-height:1.5;color:#334155;margin:0 0 12px;"><span style="display:inline-block;width:8px;height:8px;background:${accent};border-radius:99px;margin-right:9px;"></span>${p}</div>`).join("")}
              </td></tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:12px 30px 8px;">
            <h2 style="font-size:22px;line-height:1.25;margin:0 0 10px;color:#0f172a;">What we can review</h2>
            <p style="font-size:15.5px;line-height:1.62;margin:0;color:#334155;">We look at the business from an owner’s point of view: how customers find you, what they see, how they enquire, how fast the team follows up, where money or time may be wasted, and what needs to be improved first.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:10px 30px 26px;">
            <table role="presentation" cellspacing="0" cellpadding="0"><tr><td bgcolor="${accent}" style="border-radius:999px;">
              <a href="${ctaUrl}" style="display:inline-block;padding:15px 24px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:800;border-radius:999px;">${ctaText}</a>
            </td></tr></table>
            <p style="font-size:14px;line-height:1.6;margin:18px 0 0;color:#475569;">You can also reply to this email with your website link, and we will suggest the first improvement areas.</p>
          </td>
        </tr>
        <tr>
          <td style="background:#071426;color:#cbd5e1;padding:22px 30px;font-size:13px;line-height:1.6;">
            <strong style="color:#ffffff;">Anushka Bhattacharya</strong><br>
            Director, AICloudStrategist<br>
            <a href="mailto:contact@aicloudstrategist.com" style="color:#67e8f9;text-decoration:none;">contact@aicloudstrategist.com</a> · <a href="https://aicloudstrategist.com" style="color:#67e8f9;text-decoration:none;">aicloudstrategist.com</a><br>
            If this is not relevant, reply “not interested” and we will not email again.
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

const drafts = [
  {
    subject: "Are patient enquiries getting missed before they become appointments?",
    html: shell(
      "Are patient enquiries getting missed before they become appointments?",
      "For healthcare businesses",
      "Many hospitals, clinics, diagnostic labs, dental clinics, eye clinics, skin clinics, and wellness centers lose good enquiries before they become appointments. The patient may call once, send a message, check reviews, and then quietly choose another provider.",
      [
        "Patients cannot quickly understand the service, doctor, timing, location, or next step.",
        "Calls and messages are not followed up before the patient loses interest.",
        "The website looks active, but it does not guide the patient toward booking.",
        "Reviews, trust signals, privacy comfort, and appointment options are not clear enough.",
      ],
      "Review my patient enquiry journey",
      "https://aicloudstrategist.com/healthcare-growthos/"
    ),
  },
  {
    subject: "Is your cloud bill growing without clear business control?",
    html: shell(
      "Is your cloud bill growing without clear business control?",
      "For cloud and tech-led companies",
      "Many growing companies spend every month on cloud, software, AI tools, data systems, and subscriptions. But leadership may not have one clear view of what is useful, what is wasted, and what needs attention now.",
      [
        "Cloud and software bills keep increasing, but savings opportunities are not visible.",
        "Different people manage different tools, so ownership becomes scattered.",
        "Important customer, investor, or partner questions take too long to answer.",
        "Leadership does not have a simple business view of cost, risk, and next actions.",
      ],
      "Review my cloud and business control gaps",
      "https://aicloudstrategist.com/growth-control-os/",
      "#2563eb"
    ),
  },
  {
    subject: "Are you losing enquiries, time, or money because systems are not connected?",
    html: shell(
      "Are you losing enquiries, time, or money because systems are not connected?",
      "For business owners",
      "Many businesses work hard to get leads, serve customers, manage teams, and control costs. But the business still feels scattered because the website, enquiries, follow-up, tools, reports, and owner view are not connected properly.",
      [
        "Enquiries come in, but follow-up is slow or inconsistent.",
        "Website visitors do not clearly know what to do next.",
        "Manual work takes time that could be saved with better systems.",
        "The owner does not have one simple view of leads, costs, and pending action.",
      ],
      "Review my business growth and control gaps",
      "https://aicloudstrategist.com/growth-control-os/",
      "#0f766e"
    ),
  },
];

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
    const results = [];
    for (const draft of drafts) {
      const result = await sendGraphMail(context.env, {
        subject: draft.subject,
        body: { contentType: "HTML", content: draft.html },
        toRecipients: approvalRecipients.map((emailAddress) => ({ emailAddress })),
        replyTo: [{ emailAddress: { address: "contact@aicloudstrategist.com", name: "AICloudStrategist" } }],
      });
      results.push({ subject: draft.subject, status: result.status });
    }
    return new Response(JSON.stringify({ ok: true, sender: clean(context.env.M365_SENDER) || "contact@aicloudstrategist.com", results }), { status: 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  }
};

export const onRequestGet: PagesFunction = async () => new Response(JSON.stringify({ ok: false, error: "not found" }), { status: 404, headers: { "Content-Type": "application/json" } });

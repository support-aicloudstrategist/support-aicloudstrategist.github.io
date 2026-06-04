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

function html() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Patient Enquiry Recovery Snapshot</title>
</head>
<body style="margin:0;background:#edf5f8;font-family:Arial,Helvetica,sans-serif;color:#102033;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;">A conversion-focused snapshot: what is leaking, how AICS fixes it, and how to book the free review.</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#edf5f8;padding:22px 10px;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:780px;background:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 18px 55px rgba(9,30,66,.14);">
        <tr>
          <td style="padding:24px 28px;background:linear-gradient(135deg,#06192f,#087b8d);color:#fff;">
            <div style="font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#9ff2ff;font-weight:700;">AICloudStrategist Healthcare GrowthOS</div>
            <h1 style="margin:9px 0 9px;font-size:29px;line-height:1.14;">Patient Enquiry Recovery Snapshot for CityCare Dental Clinic</h1>
            <p style="margin:0 0 18px;font-size:15px;line-height:1.55;color:#e6fbff;">Where patient enquiries may be leaking — and how AICS can help you fix the capture, follow-up, and appointment conversion flow.</p>
            <a href="https://aicloudstrategist.com/contact/" style="display:inline-block;background:#ffffff;color:#087b8d;text-decoration:none;font-weight:800;border-radius:999px;padding:12px 18px;font-size:14px;">Book Free Snapshot Review</a>
            <a href="https://wa.me/918796302608?text=Hi%20AICS%2C%20I%20reviewed%20the%20Patient%20Enquiry%20Recovery%20Snapshot.%20Please%20show%20me%20how%20to%20fix%20my%20patient%20enquiry%20leakage." style="display:inline-block;margin-left:8px;background:#10b981;color:#ffffff;text-decoration:none;font-weight:800;border-radius:999px;padding:12px 18px;font-size:14px;">WhatsApp AICS</a>
          </td>
        </tr>

        <tr>
          <td style="padding:22px 28px 8px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
              <tr>
                <td style="width:25%;padding:7px;vertical-align:top;"><div style="background:#fff7e8;border:1px solid #ffdaa2;border-radius:15px;padding:13px;min-height:86px;"><div style="font-size:12px;color:#8c5600;font-weight:700;">Booking clarity</div><div style="font-size:24px;font-weight:800;color:#2b1b00;margin:5px 0;">6/10</div><div style="font-size:12px;color:#5e4724;line-height:1.35;">CTA not strong enough on mobile.</div></div></td>
                <td style="width:25%;padding:7px;vertical-align:top;"><div style="background:#ffeef0;border:1px solid #ffc9d0;border-radius:15px;padding:13px;min-height:86px;"><div style="font-size:12px;color:#9b2330;font-weight:700;">Follow-up speed</div><div style="font-size:24px;font-weight:800;color:#3b1016;margin:5px 0;">4/10</div><div style="font-size:12px;color:#68333a;line-height:1.35;">Instant response is not visible.</div></div></td>
                <td style="width:25%;padding:7px;vertical-align:top;"><div style="background:#edf8ff;border:1px solid #bfebff;border-radius:15px;padding:13px;min-height:86px;"><div style="font-size:12px;color:#006b8d;font-weight:700;">Owner visibility</div><div style="font-size:24px;font-weight:800;color:#063142;margin:5px 0;">Low</div><div style="font-size:12px;color:#315564;line-height:1.35;">No clear enquiry-to-appointment view.</div></div></td>
                <td style="width:25%;padding:7px;vertical-align:top;"><div style="background:#eefbf0;border:1px solid #c6ebca;border-radius:15px;padding:13px;min-height:86px;"><div style="font-size:12px;color:#1c742d;font-weight:700;">Fix potential</div><div style="font-size:24px;font-weight:800;color:#14391b;margin:5px 0;">High</div><div style="font-size:12px;color:#345d3c;line-height:1.35;">Start with a small recovery workflow.</div></div></td>
              </tr>
            </table>
          </td>
        </tr>

        <tr><td style="padding:8px 28px 6px;">
          <h2 style="margin:0 0 10px;font-size:20px;color:#071a33;">What may be leaking today</h2>
          <div style="background:#f8fcff;border:1px solid #dbeaf1;border-radius:16px;padding:16px;">
            <p style="margin:0 0 9px;font-size:14px;line-height:1.55;"><strong>1. Patients may not see the fastest booking path.</strong> On mobile, call/WhatsApp/appointment steps should be visible immediately.</p>
            <p style="margin:0 0 9px;font-size:14px;line-height:1.55;"><strong>2. Missed calls and forms may not get instant follow-up.</strong> When a patient contacts multiple clinics, the fastest clear response often wins attention.</p>
            <p style="margin:0;font-size:14px;line-height:1.55;"><strong>3. Owner may not know where enquiries are getting lost.</strong> Without one view of source, status, follow-up, booked appointment, and lost reason, growth decisions become guesswork.</p>
          </div>
        </td></tr>

        <tr><td style="padding:16px 28px 6px;">
          <h2 style="margin:0 0 10px;font-size:20px;color:#071a33;">How AICS helps you fix this</h2>
          <div style="background:#071a33;color:#ffffff;border-radius:18px;padding:18px;">
            <p style="margin:0 0 12px;font-size:15px;line-height:1.6;color:#e6f3ff;">AICS does not only point out the leakage. We help your clinic install a practical <strong>Healthcare GrowthOS</strong> — a connected system for patient enquiry capture, faster follow-up, staff reminders, and owner visibility.</p>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
              <tr>
                <td style="width:50%;padding:7px;vertical-align:top;"><div style="background:#0d2949;border:1px solid #1b527c;border-radius:14px;padding:13px;min-height:92px;"><strong>Capture every enquiry</strong><br><span style="color:#cfe7f5;font-size:13px;line-height:1.5;">Connect website forms, calls, WhatsApp, landing pages, and ads into one enquiry flow.</span></div></td>
                <td style="width:50%;padding:7px;vertical-align:top;"><div style="background:#0d2949;border:1px solid #1b527c;border-radius:14px;padding:13px;min-height:92px;"><strong>Respond faster</strong><br><span style="color:#cfe7f5;font-size:13px;line-height:1.5;">Set missed-call replies, WhatsApp acknowledgement, staff alerts, and follow-up reminders.</span></div></td>
              </tr>
              <tr>
                <td style="width:50%;padding:7px;vertical-align:top;"><div style="background:#0d2949;border:1px solid #1b527c;border-radius:14px;padding:13px;min-height:92px;"><strong>Track appointment conversion</strong><br><span style="color:#cfe7f5;font-size:13px;line-height:1.5;">See enquiry source, patient status, follow-up, booked appointment, and lost reason.</span></div></td>
                <td style="width:50%;padding:7px;vertical-align:top;"><div style="background:#0d2949;border:1px solid #1b527c;border-radius:14px;padding:13px;min-height:92px;"><strong>Improve trust and clarity</strong><br><span style="color:#cfe7f5;font-size:13px;line-height:1.5;">Improve service pages, reviews placement, doctor/service clarity, FAQs, and booking prompts.</span></div></td>
              </tr>
            </table>
          </div>
        </td></tr>

        <tr><td style="padding:16px 28px 6px;">
          <h2 style="margin:0 0 10px;font-size:20px;color:#071a33;">Before AICS vs After GrowthOS</h2>
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
            <tr>
              <td style="width:50%;padding-right:8px;vertical-align:top;">
                <div style="border:1px solid #ffd2d6;background:#fff3f4;border-radius:16px;padding:15px;min-height:180px;">
                  <h3 style="margin:0 0 10px;font-size:16px;color:#7f1d1d;">Before</h3>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#633;">• Calls, WhatsApp, forms, and ad leads are scattered</p>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#633;">• Staff may forget follow-up during busy hours</p>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#633;">• Owner cannot see all pending enquiries</p>
                  <p style="margin:0;font-size:13px;line-height:1.45;color:#633;">• Marketing spend continues without clear conversion view</p>
                </div>
              </td>
              <td style="width:50%;padding-left:8px;vertical-align:top;">
                <div style="border:1px solid #bfe8cb;background:#f0fbf3;border-radius:16px;padding:15px;min-height:180px;">
                  <h3 style="margin:0 0 10px;font-size:16px;color:#166534;">After</h3>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#294d31;">• Every enquiry is captured in one flow</p>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#294d31;">• Missed calls/forms get instant response</p>
                  <p style="margin:0 0 7px;font-size:13px;line-height:1.45;color:#294d31;">• Staff gets reminders and next tasks</p>
                  <p style="margin:0;font-size:13px;line-height:1.45;color:#294d31;">• Owner sees status, appointment conversion, and lost reasons</p>
                </div>
              </td>
            </tr>
          </table>
        </td></tr>

        <tr><td style="padding:16px 28px 6px;">
          <h2 style="margin:0 0 10px;font-size:20px;color:#071a33;">What happens when you contact AICS</h2>
          <div style="background:#eaf9ff;border:1px solid #bfeaf7;border-radius:16px;padding:16px;">
            <p style="margin:0 0 10px;font-size:14px;line-height:1.55;color:#284c5a;"><strong>Step 1: Free Snapshot Review.</strong> We walk through the score, leakage points, and the top 2–3 fixes.</p>
            <p style="margin:0 0 10px;font-size:14px;line-height:1.55;color:#284c5a;"><strong>Step 2: 30-day Recovery Plan.</strong> We show what can be fixed first: booking clarity, missed-call workflow, WhatsApp follow-up, dashboard, or trust pages.</p>
            <p style="margin:0;font-size:14px;line-height:1.55;color:#284c5a;"><strong>Step 3: Optional implementation sprint.</strong> If there is fit, AICS can run a focused Patient Enquiry Recovery Sprint before any long-term engagement.</p>
          </div>
        </td></tr>

        <tr><td style="padding:16px 28px 6px;">
          <h2 style="margin:0 0 10px;font-size:20px;color:#071a33;">Low-risk path</h2>
          <div style="background:#f7fbfd;border:1px solid #dbeaf1;border-radius:16px;padding:16px;text-align:center;">
            <span style="display:inline-block;background:#fff;border:1px solid #d8e8ef;border-radius:999px;padding:9px 12px;font-size:13px;margin:4px;"><strong>Free snapshot</strong></span>
            <span style="color:#83939f;">→</span>
            <span style="display:inline-block;background:#fff;border:1px solid #d8e8ef;border-radius:999px;padding:9px 12px;font-size:13px;margin:4px;"><strong>Free review call</strong></span>
            <span style="color:#83939f;">→</span>
            <span style="display:inline-block;background:#fff;border:1px solid #d8e8ef;border-radius:999px;padding:9px 12px;font-size:13px;margin:4px;"><strong>30-day recovery sprint</strong></span>
            <span style="color:#83939f;">→</span>
            <span style="display:inline-block;background:#fff;border:1px solid #d8e8ef;border-radius:999px;padding:9px 12px;font-size:13px;margin:4px;"><strong>Managed GrowthOS</strong></span>
            <p style="margin:12px 0 0;font-size:13px;color:#526575;line-height:1.5;">Start small. Prove the first fix. Continue only if the value is clear.</p>
          </div>
        </td></tr>

        <tr><td style="padding:18px 28px 28px;">
          <div style="background:linear-gradient(135deg,#087b8d,#10b981);border-radius:18px;padding:20px;text-align:center;color:#ffffff;">
            <h2 style="margin:0 0 8px;font-size:22px;">Want help to fix these gaps?</h2>
            <p style="margin:0 0 16px;font-size:15px;line-height:1.55;color:#f0fffb;">Book a free Snapshot Review. We will explain what to fix first, what can wait, and how AICS can help your clinic reduce missed enquiries and improve enquiry-to-appointment tracking.</p>
            <a href="https://aicloudstrategist.com/contact/" style="display:inline-block;background:#ffffff;color:#087b8d;text-decoration:none;font-weight:800;border-radius:999px;padding:13px 20px;font-size:14px;">Book Free Snapshot Review</a>
            <a href="https://wa.me/918796302608?text=Hi%20AICS%2C%20I%20reviewed%20the%20Patient%20Enquiry%20Recovery%20Snapshot.%20Please%20show%20me%20how%20to%20fix%20my%20patient%20enquiry%20leakage." style="display:inline-block;margin-left:8px;background:#071a33;color:#ffffff;text-decoration:none;font-weight:800;border-radius:999px;padding:13px 20px;font-size:14px;">WhatsApp AICS</a>
            <p style="margin:14px 0 0;font-size:12px;color:#e8fff7;">Or email: contact@aicloudstrategist.com</p>
          </div>
          <p style="margin:18px 0 0;font-size:15px;line-height:1.55;color:#526575;">Warmly,<br><strong>Anushka Bhattacharya</strong><br>Director, AICloudStrategist<br><a href="https://aicloudstrategist.com" style="color:#087b8d;">aicloudstrategist.com</a></p>
          <p style="margin:14px 0 0;font-size:11px;line-height:1.45;color:#7d8b96;">This is an initial directional snapshot based on visible/public information and sample assumptions. It does not guarantee revenue, patient volume, rankings, savings, or compliance outcomes. Actual opportunity depends on enquiry volume, team process, patient behaviour, and implementation quality.</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

export const onRequestGet: PagesHandler<Env> = async () => json({ ok: true, ready: true, sendsEmail: false, endpoint: "send-conversion-snapshot" });

export const onRequestPost: PagesHandler<Env> = async ({ env }) => {
  try {
    const sender = clean(env.M365_SENDER);
    if (!sender) throw new Error("Microsoft Graph sender is not configured.");
    const subject = "Revised conversion snapshot — how AICS fixes patient enquiry leakage";
    const token = await getGraphToken(env);
    const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        message: {
          subject,
          body: { contentType: "HTML", content: html() },
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

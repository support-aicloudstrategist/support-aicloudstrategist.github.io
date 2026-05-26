type WebinarEnv = {
  LEAD_LOG?: KVNamespace;
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
  M365_RECIPIENT?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};
const clean = (value: unknown) => String(value ?? "").trim();

async function getGraphToken(env: WebinarEnv): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");
  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) return graphTokenCache.token;
  const body = new URLSearchParams({ grant_type: "client_credentials", client_id: clientId, client_secret: clientSecret, scope: "https://graph.microsoft.com/.default" });
  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
  const tokenPayload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !tokenPayload.access_token) throw new Error(tokenPayload.error_description || tokenPayload.error || `Graph token request failed with ${response.status}.`);
  graphTokenCache = { token: tokenPayload.access_token, expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000 };
  return graphTokenCache.token;
}

async function sendGraphMail(env: WebinarEnv, graphMessage: Record<string, unknown>) {
  const sender = clean(env.M365_SENDER);
  if (!sender) throw new Error("Microsoft Graph sender is not configured.");
  const token = await getGraphToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify({ message: graphMessage, saveToSentItems: true }),
  });
  const responseText = await response.text();
  if (!response.ok) throw new Error(responseText || `Graph sendMail failed with ${response.status}.`);
  return { status: response.status, responseText };
}

function buildConfirmationBody(reg: Record<string, string>) {
  return `Hi ${reg.full_name},

You're registered for DPDP for Indian Clinics: What You Must Do Before November 2026.

Date: {{webinar_date}}
Time: {{webinar_time}} IST
Google Meet: {{join_link}}

Calendar invite + Meet link below. Please keep this email handy.

Warmly,
Anushka
Director, AICloudStrategist`;
}

export const onRequestPost: PagesFunction<WebinarEnv> = async (context) => {
  let payload: Record<string, unknown>;
  try { payload = await context.request.json(); } catch { return new Response(JSON.stringify({ ok: false, error: "Invalid JSON payload." }), { status: 400, headers: jsonHeaders }); }
  const registration = {
    full_name: clean(payload.full_name), email: clean(payload.email), business_name: clean(payload.business_name), role: clean(payload.role), vertical: clean(payload.vertical), whatsapp_number: clean(payload.whatsapp_number),
  };
  const missing = Object.entries(registration).filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), { status: 422, headers: jsonHeaders });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registration.email)) return new Response(JSON.stringify({ ok: false, error: "Enter a valid email address." }), { status: 422, headers: jsonHeaders });
  if (!/^\+?[0-9][0-9\s-]{8,18}$/.test(registration.whatsapp_number)) return new Response(JSON.stringify({ ok: false, error: "Enter a valid WhatsApp number with country code." }), { status: 422, headers: jsonHeaders });
  const submittedAt = new Date().toISOString();
  const registrationId = `webinar-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
  const record = { registration_id: registrationId, submitted_at: submittedAt, source: "dpdp-clinics-webinar", ...registration };
  const internalRecipient = clean(context.env.M365_RECIPIENT || "contact@aicloudstrategist.com" || context.env.M365_SENDER);
  try {
    const registrantResult = await sendGraphMail(context.env, { subject: "You're registered — DPDP for Indian Clinics webinar", body: { contentType: "Text", content: buildConfirmationBody(registration) }, toRecipients: [{ emailAddress: { address: registration.email, name: registration.full_name } }], replyTo: [{ emailAddress: { address: internalRecipient, name: "AICloudStrategist" } }] });
    const internalResult = await sendGraphMail(context.env, { subject: `New webinar registration — ${registration.business_name}`, body: { contentType: "Text", content: `New DPDP webinar registration\n\nRegistration ID: ${registrationId}\nSubmitted at: ${submittedAt}\nName: ${registration.full_name}\nEmail: ${registration.email}\nBusiness: ${registration.business_name}\nRole: ${registration.role}\nVertical: ${registration.vertical}\nWhatsApp: ${registration.whatsapp_number}\n` }, toRecipients: [{ emailAddress: { address: internalRecipient } }], replyTo: [{ emailAddress: { address: registration.email, name: registration.full_name } }] });
    if (context.env.LEAD_LOG) await context.env.LEAD_LOG.put(registrationId, JSON.stringify({ ...record, registrant_graph_status: registrantResult.status, internal_graph_status: internalResult.status }), { metadata: { submitted_at: submittedAt, business_name: registration.business_name } });
    return new Response(JSON.stringify({ ok: true, registration_id: registrationId, confirmation_sent: true }), { status: 200, headers: jsonHeaders });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Email delivery failed.";
    return new Response(JSON.stringify({ ok: false, error: "Email delivery failed. Please retry or WhatsApp us directly.", details: message.slice(0, 300) }), { status: 502, headers: jsonHeaders });
  }
};

export const onRequestOptions: PagesFunction = async () => new Response(null, { status: 204, headers: { "Access-Control-Allow-Origin": "https://aicloudstrategist.com", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" } });

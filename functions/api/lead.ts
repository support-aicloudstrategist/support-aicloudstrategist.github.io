type LeadEnv = {
  LEAD_LOG?: KVNamespace;
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
  M365_RECIPIENT?: string;
};

type GraphTokenCache = {
  token: string;
  expiresAt: number;
};

let graphTokenCache: GraphTokenCache | null = null;

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const clean = (value: unknown) => String(value ?? "").trim();

const sanitizeAttributionUrl = (value: unknown) => {
  const raw = clean(value);
  if (!raw) return "";
  try {
    const parsed = new URL(raw);
    return `${parsed.origin}${parsed.pathname}`;
  } catch {
    return raw.split(/[?#]/, 1)[0];
  }
};

async function readPayload(request: Request): Promise<Record<string, unknown>> {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return (await request.json()) as Record<string, unknown>;
  }

  const formData = await request.formData();
  const payload: Record<string, unknown> = {};
  formData.forEach((value, key) => {
    if (typeof value === "string") payload[key] = value;
  });
  return payload;
}

async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function enforceRateLimit(env: LeadEnv, request: Request) {
  if (!env.LEAD_LOG) return;
  const clientIp = clean(request.headers.get("CF-Connecting-IP"));
  if (!clientIp) return;
  const minute = new Date().toISOString().slice(0, 16);
  const key = `rate:audit:${minute}:${await sha256(clientIp)}`;
  const count = Number(await env.LEAD_LOG.get(key)) || 0;
  if (count >= 5) throw new Error("RATE_LIMITED");
  await env.LEAD_LOG.put(key, String(count + 1), { expirationTtl: 120 });
}

function hasTrustedBrowserProvenance(request: Request) {
  const origin = clean(request.headers.get("Origin"));
  const fetchSite = clean(request.headers.get("Sec-Fetch-Site"));
  if (!origin) return false;
  try {
    const host = new URL(origin).hostname.toLowerCase();
    const trustedHost = host === "aicloudstrategist.com" || host === "www.aicloudstrategist.com" || host.endsWith(".aicloudstrategist-site.pages.dev");
    return trustedHost && (!fetchSite || fetchSite === "same-origin" || fetchSite === "same-site");
  } catch {
    return false;
  }
}

async function submissionId(prefix: string, _request: Request, submittedAt: string) {
  return `${prefix}-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
}

async function getGraphToken(env: LeadEnv): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);

  if (!tenantId || !clientId || !clientSecret) {
    throw new Error("Microsoft Graph credentials are not configured.");
  }

  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) {
    return graphTokenCache.token;
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

  const tokenPayload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !tokenPayload.access_token) {
    throw new Error(tokenPayload.error_description || tokenPayload.error || `Graph token request failed with ${response.status}.`);
  }

  graphTokenCache = {
    token: tokenPayload.access_token,
    expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000,
  };

  return graphTokenCache.token;
}

async function sendGraphMail(env: LeadEnv, graphMessage: Record<string, unknown>) {
  const sender = clean(env.M365_SENDER);
  if (!sender) {
    throw new Error("Microsoft Graph sender is not configured.");
  }

  const token = await getGraphToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: graphMessage, saveToSentItems: true }),
  });

  const responseText = await response.text();
  if (!response.ok) {
    throw new Error(responseText || `Graph sendMail failed with ${response.status}.`);
  }

  return { status: response.status, responseText };
}

async function sendLeadEmail(env: LeadEnv, lead: Record<string, string>, textBody: string) {
  const recipient = clean(env.M365_RECIPIENT || env.M365_SENDER);

  if (!recipient) {
    throw new Error("Microsoft Graph recipient is not configured.");
  }

  const subject = `[AICS-LEAD][AUDIT-REQUEST] ${lead.business_name}`;
  return sendGraphMail(env, {
    subject,
    body: { contentType: "Text", content: textBody },
    toRecipients: [{ emailAddress: { address: recipient } }],
    replyTo: lead.prospect_email ? [{ emailAddress: { address: lead.prospect_email, name: lead.full_name || lead.business_name } }] : undefined,
  });
}

export const onRequestPost: PagesFunction<LeadEnv> = async (context) => {
  if (!hasTrustedBrowserProvenance(context.request)) {
    return new Response(JSON.stringify({ ok: false, error: "Untrusted submission source." }), { status: 403, headers: jsonHeaders });
  }

  let payload: Record<string, unknown>;
  try {
    payload = await readPayload(context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid submission payload." }), { status: 400, headers: jsonHeaders });
  }

  const businessName = clean(payload.business_name);
  const website = clean(payload.website || payload.website_url);
  const whatsappNumber = clean(payload.whatsapp_number);
  const vertical = clean(payload.vertical);
  const prospectEmail = clean(payload.prospect_email || payload.email);
  const notes = clean(payload.notes || payload.specific_notes);
  const fullName = clean(payload.full_name);
  const packageContext = clean(payload.package_context);
  const serviceContext = clean(payload.service_context);
  const landingPage = sanitizeAttributionUrl(payload.landing_page);
  const referrer = sanitizeAttributionUrl(payload.referrer);
  const utmSource = clean(payload.utm_source);
  const utmMedium = clean(payload.utm_medium);
  const utmCampaign = clean(payload.utm_campaign);
  const websiteTrap = clean(payload.company_website);
  const formLoadedAt = Number(clean(payload.form_loaded_at));

  // Suspicious form submission: silently accept the honeypot without delivering mail.
  if (websiteTrap) {
    return new Response(JSON.stringify({ ok: true, lead_id: "accepted" }), { status: 200, headers: jsonHeaders });
  }

  if (Number.isFinite(formLoadedAt) && formLoadedAt > 0 && Date.now() - formLoadedAt < 1_500) {
    return new Response(JSON.stringify({ ok: true, lead_id: "accepted" }), { status: 200, headers: jsonHeaders });
  }

  try {
    await enforceRateLimit(context.env, context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Too many requests. Please wait and retry." }), { status: 429, headers: jsonHeaders });
  }

  const oversized = [
    ["business_name", businessName, 160], ["website", website, 2048], ["whatsapp_number", whatsappNumber, 32],
    ["vertical", vertical, 80], ["prospect_email", prospectEmail, 320], ["notes", notes, 4000],
    ["full_name", fullName, 160], ["package_context", packageContext, 160], ["service_context", serviceContext, 160],
    ["landing_page", landingPage, 2048], ["referrer", referrer, 2048], ["utm_source", utmSource, 256],
    ["utm_medium", utmMedium, 256], ["utm_campaign", utmCampaign, 256],
  ].find(([, value, max]) => String(value).length > Number(max));
  if (oversized) {
    return new Response(JSON.stringify({ ok: false, error: `${oversized[0]} is too long.` }), { status: 422, headers: jsonHeaders });
  }

  const missing = [
    ["business_name", businessName],
    ["website", website],
    ["whatsapp_number", whatsappNumber],
    ["vertical", vertical],
    ["prospect_email", prospectEmail],
  ]
    .filter(([, value]) => !value)
    .map(([field]) => field);

  if (missing.length) {
    return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^https?:\/\//i.test(website)) {
    return new Response(JSON.stringify({ ok: false, error: "Website must start with http:// or https://." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^\+?[0-9][0-9\s-]{8,18}$/.test(whatsappNumber)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid WhatsApp number with country code." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(prospectEmail)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid email address." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  const submittedAt = new Date().toISOString();
  const leadId = await submissionId("lead", context.request, submittedAt);
  const lead = {
    lead_id: leadId,
    submitted_at: submittedAt,
    full_name: fullName,
    business_name: businessName,
    website,
    whatsapp_number: whatsappNumber,
    vertical,
    prospect_email: prospectEmail,
    email: prospectEmail,
    notes,
    package_context: packageContext,
    service_context: serviceContext,
    landing_page: landingPage,
    referrer,
    utm_source: utmSource,
    utm_medium: utmMedium,
    utm_campaign: utmCampaign,
    source: "free-trust-growth-audit",
    pipeline_stage: "new",
    lead_status: "audit-requested",
    owner: "AICloudStrategist Growth Operations",
  };

  const textBody = `New AICloudStrategist Free Trust & Growth Audit request\n\nPipeline stage: NEW\nLead status: AUDIT REQUESTED\nOwner: AICloudStrategist Growth Operations\nLead ID: ${leadId}\nSubmitted at: ${submittedAt}\nFull name: ${fullName || "not provided"}\nBusiness name: ${businessName}\nWebsite: ${website}\nWhatsApp: ${whatsappNumber}\nVertical: ${vertical}\nEmail: ${prospectEmail}\nPackage context: ${packageContext || "not set"}\nService context: ${serviceContext || "not set"}\nLanding page: ${landingPage || "not captured"}\nReferrer: ${referrer || "direct or unavailable"}\nUTM source: ${utmSource || "not set"}\nUTM medium: ${utmMedium || "not set"}\nUTM campaign: ${utmCampaign || "not set"}\nNotes: ${notes || "not provided"}\n`;

  if (!context.env.LEAD_LOG) {
    return new Response(JSON.stringify({ ok: false, error: "Lead storage is temporarily unavailable. Please use WhatsApp or email." }), {
      status: 503,
      headers: jsonHeaders,
    });
  }

  const initialRecord = { ...lead, notification_status: "manual_review_pending" };
  try {
    await context.env.LEAD_LOG.put(leadId, JSON.stringify(initialRecord), { metadata: { submitted_at: submittedAt, business_name: businessName } });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Lead storage failed.";
    return new Response(JSON.stringify({ ok: false, error: "Lead storage failed. Please retry or use WhatsApp.", details: message.slice(0, 300) }), {
      status: 502,
      headers: jsonHeaders,
    });
  }

  return new Response(JSON.stringify({ ok: true, lead_id: leadId, notification_sent: false, notification_mode: "manual-review" }), { status: 200, headers: jsonHeaders });
};

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });

export const onRequestGet: PagesFunction<LeadEnv> = async (context) => {
  const storageConfigured = Boolean(context.env.LEAD_LOG);
  const ok = storageConfigured;
  return new Response(JSON.stringify({ ok, storage_configured: storageConfigured, notification_mode: "manual-review" }), {
    status: ok ? 200 : 503,
    headers: jsonHeaders,
  });
};

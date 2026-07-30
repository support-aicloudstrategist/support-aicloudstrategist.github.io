type ContactEnv = {
  CONTACT_LOG?: KVNamespace;
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

async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function enforceRateLimit(env: ContactEnv, request: Request) {
  const log = env.CONTACT_LOG || env.LEAD_LOG;
  const clientIp = clean(request.headers.get("CF-Connecting-IP"));
  if (!log || !clientIp) return;
  const minute = new Date().toISOString().slice(0, 16);
  const key = `rate:contact:${minute}:${await sha256(clientIp)}`;
  const count = Number(await log.get(key)) || 0;
  if (count >= 5) throw new Error("RATE_LIMITED");
  await log.put(key, String(count + 1), { expirationTtl: 120 });
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

async function parsePayload(request: Request): Promise<Record<string, unknown>> {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return (await request.json()) as Record<string, unknown>;
  }
  const formData = await request.formData();
  return Object.fromEntries(formData.entries());
}

async function getGraphToken(env: ContactEnv): Promise<string> {
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

  const tokenPayload = (await response.json().catch(() => ({}))) as {
    access_token?: string;
    expires_in?: number;
    error?: string;
    error_description?: string;
  };
  if (!response.ok || !tokenPayload.access_token) {
    throw new Error(tokenPayload.error_description || tokenPayload.error || `Graph token request failed with ${response.status}.`);
  }

  graphTokenCache = {
    token: tokenPayload.access_token,
    expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000,
  };

  return graphTokenCache.token;
}

async function sendGraphMail(env: ContactEnv, graphMessage: Record<string, unknown>) {
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

const looksLikeEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

export const onRequestPost: PagesFunction<ContactEnv> = async (context) => {
  if (!hasTrustedBrowserProvenance(context.request)) {
    return new Response(JSON.stringify({ ok: false, error: "Untrusted submission source." }), { status: 403, headers: jsonHeaders });
  }

  let payload: Record<string, unknown>;
  try {
    payload = await parsePayload(context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid submission payload." }), { status: 400, headers: jsonHeaders });
  }

  const name = clean(payload.name || payload.full_name);
  const contact = clean(payload.contact || payload.email || payload.whatsapp_number);
  const need = clean(payload.need || payload.vertical || "Not specified");
  const message = clean(payload.message || payload.notes || payload.specific_notes);
  const website = clean(payload.website || payload.website_url);
  const company = clean(payload.company);
  const role = clean(payload.role);
  const service = clean(payload.service);
  const stage = clean(payload.stage);
  const landingPage = sanitizeAttributionUrl(payload.landing_page);
  const referrer = sanitizeAttributionUrl(payload.referrer);
  const utmSource = clean(payload.utm_source);
  const utmMedium = clean(payload.utm_medium);
  const utmCampaign = clean(payload.utm_campaign);
  const companyWebsite = clean(payload.company_website);

  // Suspicious form submission: silently accept the honeypot without delivering mail.
  if (companyWebsite) {
    return new Response(JSON.stringify({ ok: true, contact_id: "accepted" }), { status: 200, headers: jsonHeaders });
  }

  try {
    await enforceRateLimit(context.env, context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Too many requests. Please wait and retry." }), { status: 429, headers: jsonHeaders });
  }

  const oversized = [
    ["name", name, 160], ["contact", contact, 320], ["need", need, 4000], ["message", message, 4000],
    ["website", website, 2048], ["company", company, 160], ["role", role, 160], ["service", service, 160],
    ["stage", stage, 160], ["landing_page", landingPage, 2048], ["referrer", referrer, 2048],
    ["utm_source", utmSource, 256], ["utm_medium", utmMedium, 256], ["utm_campaign", utmCampaign, 256],
  ].find(([, value, max]) => String(value).length > Number(max));
  if (oversized) {
    return new Response(JSON.stringify({ ok: false, error: `${oversized[0]} is too long.` }), { status: 422, headers: jsonHeaders });
  }

  const missing = [
    ["name", name],
    ["contact", contact],
  ]
    .filter(([, value]) => !value)
    .map(([field]) => field);

  if (missing.length) {
    return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  const submittedAt = new Date().toISOString();
  const contactId = await submissionId("contact", context.request, submittedAt);
  const recipient = clean(context.env.M365_RECIPIENT || context.env.M365_SENDER);

  const textBody = `New AICloudStrategist contact enquiry\n\nPipeline stage: NEW\nLead status: UNREVIEWED\nOwner: AICloudStrategist Growth Operations\nContact ID: ${contactId}\nSubmitted at: ${submittedAt}\nName: ${name}\nContact: ${contact}\nCompany: ${company || "not provided"}\nRole: ${role || "not provided"}\nService interest: ${service || "not specified"}\nBuyer stage: ${stage || "not specified"}\nNeed: ${need}\nWebsite: ${website || "not provided"}\nMessage: ${message || "not provided"}\nLanding page: ${landingPage || "not captured"}\nReferrer: ${referrer || "direct or unavailable"}\nUTM source: ${utmSource || "not set"}\nUTM medium: ${utmMedium || "not set"}\nUTM campaign: ${utmCampaign || "not set"}\nSource: contact page\n`;

  const log = context.env.CONTACT_LOG || context.env.LEAD_LOG;
  if (!log) {
    return new Response(JSON.stringify({ ok: false, error: "Lead storage is temporarily unavailable. Please use WhatsApp or email." }), {
      status: 503,
      headers: jsonHeaders,
    });
  }

  const leadRecord = {
    contact_id: contactId,
    submitted_at: submittedAt,
    name, contact, company, role, service, stage, need, website, message,
    source: "contact-page",
    landing_page: landingPage,
    referrer,
    utm_source: utmSource,
    utm_medium: utmMedium,
    utm_campaign: utmCampaign,
    pipeline_stage: "new",
    lead_status: "unreviewed",
    owner: "AICloudStrategist Growth Operations",
  };

  try {
    await log.put(contactId, JSON.stringify({ ...leadRecord, notification_status: "manual_review_pending" }), { metadata: { submitted_at: submittedAt, name } });
  } catch (error) {
    const messageText = error instanceof Error ? error.message : "Lead storage failed.";
    return new Response(JSON.stringify({ ok: false, error: "Lead storage failed. Please retry or use WhatsApp.", details: messageText.slice(0, 300) }), {
      status: 502,
      headers: jsonHeaders,
    });
  }

  return new Response(JSON.stringify({ ok: true, contact_id: contactId, notification_sent: false, notification_mode: "manual-review" }), { status: 200, headers: jsonHeaders });
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

export const onRequestGet: PagesFunction<ContactEnv> = async (context) => {
  const storageConfigured = Boolean(context.env.CONTACT_LOG || context.env.LEAD_LOG);
  const ok = storageConfigured;
  return new Response(JSON.stringify({ ok, storage_configured: storageConfigured, notification_mode: "manual-review" }), {
    status: ok ? 200 : 503,
    headers: jsonHeaders,
  });
};

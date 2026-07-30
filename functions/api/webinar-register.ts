type WebinarEnv = {
  LEAD_LOG?: KVNamespace;
};

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const clean = (value: unknown) => String(value ?? "").trim();

async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
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

async function readPayload(request: Request): Promise<Record<string, unknown>> {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return (await request.json()) as Record<string, unknown>;
  const formData = await request.formData();
  return Object.fromEntries(formData.entries());
}

async function enforceRateLimit(env: WebinarEnv, request: Request) {
  if (!env.LEAD_LOG) return;
  const clientIp = clean(request.headers.get("CF-Connecting-IP"));
  if (!clientIp) return;
  const minute = new Date().toISOString().slice(0, 16);
  const key = `rate:webinar:${minute}:${await sha256(clientIp)}`;
  const count = Number(await env.LEAD_LOG.get(key)) || 0;
  if (count >= 5) throw new Error("RATE_LIMITED");
  await env.LEAD_LOG.put(key, String(count + 1), { expirationTtl: 120 });
}

async function registrationId(_request: Request, submittedAt: string) {
  return `webinar-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
}

export const onRequestGet: PagesFunction<WebinarEnv> = async ({ env }) => new Response(JSON.stringify({
  ok: Boolean(env.LEAD_LOG),
  storage_configured: Boolean(env.LEAD_LOG),
  notification_mode: "manual-review",
}), { status: env.LEAD_LOG ? 200 : 503, headers: jsonHeaders });

export const onRequestPost: PagesFunction<WebinarEnv> = async (context) => {
  if (!hasTrustedBrowserProvenance(context.request)) {
    return new Response(JSON.stringify({ ok: false, error: "Untrusted submission source." }), { status: 403, headers: jsonHeaders });
  }

  let payload: Record<string, unknown>;
  try {
    payload = await readPayload(context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid submission payload." }), { status: 400, headers: jsonHeaders });
  }

  const registration = {
    full_name: clean(payload.full_name),
    email: clean(payload.email),
    business_name: clean(payload.business_name),
    role: clean(payload.role),
    vertical: clean(payload.vertical),
    whatsapp_number: clean(payload.whatsapp_number),
  };
  const websiteTrap = clean(payload.company_website);
  const formLoadedAt = Number(clean(payload.form_loaded_at));

  if (websiteTrap || (Number.isFinite(formLoadedAt) && formLoadedAt > 0 && Date.now() - formLoadedAt < 1_500)) {
    return new Response(JSON.stringify({ ok: true, registration_id: "accepted", confirmation_sent: false, notification_mode: "manual-review" }), { status: 200, headers: jsonHeaders });
  }

  try {
    await enforceRateLimit(context.env, context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Too many requests. Please wait and retry." }), { status: 429, headers: jsonHeaders });
  }

  const oversized = Object.entries(registration).find(([field, value]) => value.length > (field === "email" ? 320 : field === "whatsapp_number" ? 32 : 160));
  if (oversized) return new Response(JSON.stringify({ ok: false, error: `${oversized[0]} is too long.` }), { status: 422, headers: jsonHeaders });

  const missing = Object.entries(registration).filter(([, value]) => !value).map(([field]) => field);
  if (missing.length) return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), { status: 422, headers: jsonHeaders });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registration.email)) return new Response(JSON.stringify({ ok: false, error: "Enter a valid email address." }), { status: 422, headers: jsonHeaders });
  if (!/^\+?[0-9][0-9\s-]{8,18}$/.test(registration.whatsapp_number)) return new Response(JSON.stringify({ ok: false, error: "Enter a valid WhatsApp number with country code." }), { status: 422, headers: jsonHeaders });
  if (!context.env.LEAD_LOG) return new Response(JSON.stringify({ ok: false, error: "Registration storage is temporarily unavailable." }), { status: 503, headers: jsonHeaders });

  const submittedAt = new Date().toISOString();
  const id = await registrationId(context.request, submittedAt);
  const record = {
    registration_id: id,
    submitted_at: submittedAt,
    source: "dpdp-clinics-webinar",
    notification_status: "manual_review_pending",
    ...registration,
  };

  try {
    await context.env.LEAD_LOG.put(id, JSON.stringify(record), { metadata: { submitted_at: submittedAt, business_name: registration.business_name } });
  } catch (error) {
    const details = error instanceof Error ? error.message : "Registration storage failed.";
    return new Response(JSON.stringify({ ok: false, error: "Registration storage is temporarily unavailable.", details: details.slice(0, 300) }), { status: 503, headers: jsonHeaders });
  }

  return new Response(JSON.stringify({ ok: true, registration_id: id, confirmation_sent: false, notification_mode: "manual-review" }), { status: 200, headers: jsonHeaders });
};

export const onRequestOptions: PagesFunction = async () => new Response(null, {
  status: 204,
  headers: {
    "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  },
});

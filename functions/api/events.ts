type EventEnv = { LEAD_LOG?: KVNamespace };

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const allowedEvents = new Set([
  "page_view",
  "cta_click",
  "button_click",
  "download_click",
  "scroll_depth",
  "dwell_tick",
  "presence_ping",
  "form_start",
  "form_submit_attempt",
  "form_validation_error",
  "form_submit_success",
  "form_submit_error",
  "email_click",
  "phone_click",
  "whatsapp_click",
  "pricing_view",
  "fit_review_view",
  "chat_open",
  "chat_query",
  "email_capture_open",
  "email_capture_dismiss",
  "email_capture_submit_attempt",
  "email_capture_submit_success",
]);

const allowedProps = new Set([
  "cta",
  "destination",
  "form",
  "offer",
  "section",
  "source",
  "status",
  "provider",
  "channel",
  "campaign",
  "service",
  "device",
  "browser",
  "country",
  "visitor",
  "visitor_kind",
  "trigger",
  "via",
  "api",
  "depth",
  "seconds",
]);

// Hard boundary: never accept sensitive personal fields on the analytics event path.
// Voluntary name/email belong only on /api/contact (consented forms), never here.
const blockedSensitivePropKeys = new Set([
  "email",
  "name",
  "full_name",
  "phone",
  "password",
  "passwd",
  "secret",
  "token",
  "card",
  "credit_card",
  "cvv",
  "ssn",
  "aadhaar",
  "pan",
  "dob",
  "health",
  "lat",
  "lng",
  "latitude",
  "longitude",
  "precise_location",
  "ip",
  "address",
]);

const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

function trusted(request: Request) {
  const origin = clean(request.headers.get("Origin"));
  const fetchSite = clean(request.headers.get("Sec-Fetch-Site"));
  if (!origin) return false;
  try {
    const host = new URL(origin).hostname.toLowerCase();
    return (
      (host === "aicloudstrategist.com" ||
        host === "www.aicloudstrategist.com" ||
        host.endsWith(".aicloudstrategist-site.pages.dev")) &&
      (!fetchSite || fetchSite === "same-origin" || fetchSite === "same-site")
    );
  } catch {
    return false;
  }
}

function browserFromUa(ua: string) {
  const value = ua.toLowerCase();
  if (value.includes("edg/")) return "edge";
  if (value.includes("chrome/") && !value.includes("edg/")) return "chrome";
  if (value.includes("safari/") && !value.includes("chrome/")) return "safari";
  if (value.includes("firefox/")) return "firefox";
  if (value.includes("opr/") || value.includes("opera")) return "opera";
  return "other";
}

export const onRequestGet: PagesFunction<EventEnv> = async ({ env }) =>
  new Response(
    JSON.stringify({
      ok: Boolean(env.LEAD_LOG),
      collector: env.LEAD_LOG ? "ready" : "unavailable",
      privacy: "non-PII allowlist",
    }),
    { status: env.LEAD_LOG ? 200 : 503, headers },
  );

export const onRequestPost: PagesFunction<EventEnv> = async ({ request, env }) => {
  if (!trusted(request)) {
    return new Response(JSON.stringify({ ok: false, error: "Untrusted event source." }), {
      status: 403,
      headers,
    });
  }
  if (!env.LEAD_LOG) {
    return new Response(JSON.stringify({ ok: false, error: "Collector unavailable." }), {
      status: 503,
      headers,
    });
  }

  let input: Record<string, unknown>;
  try {
    input = (await request.json()) as Record<string, unknown>;
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid event payload." }), {
      status: 400,
      headers,
    });
  }

  const name = clean(input.name, 64)
    .toLowerCase()
    .replace(/[^a-z0-9_]+/g, "_");
  if (!allowedEvents.has(name)) {
    return new Response(JSON.stringify({ ok: false, error: "Unsupported event." }), {
      status: 422,
      headers,
    });
  }

  const rawPath = clean(input.path, 512);
  const path = rawPath.startsWith("/") && !rawPath.includes("?") && !rawPath.includes("#") ? rawPath : "/";
  const session = clean(input.session, 64).replace(/[^a-zA-Z0-9_-]/g, "");
  const props: Record<string, string> = {};
  if (input.props && typeof input.props === "object" && !Array.isArray(input.props)) {
    for (const [key, value] of Object.entries(input.props as Record<string, unknown>)) {
      const propKey = clean(key, 64).toLowerCase();
      if (blockedSensitivePropKeys.has(propKey)) continue;
      if (!allowedProps.has(key) && !allowedProps.has(propKey)) continue;
      props[key] = clean(value, 120);
    }
  }

  // Server-side enrichment only — country/region at most; never emails, names, autofill, or precise geo.
  const cf = (request as Request & { cf?: { country?: string } }).cf;
  if (!props.country && cf?.country) props.country = clean(cf.country, 8).toUpperCase();
  if (!props.browser) props.browser = browserFromUa(request.headers.get("User-Agent") || "");

  const receivedAt = new Date().toISOString();
  const id = `event:${receivedAt.slice(0, 10)}:${crypto.randomUUID()}`;
  await env.LEAD_LOG.put(
    id,
    JSON.stringify({
      event_id: id,
      received_at: receivedAt,
      name,
      path,
      session,
      props,
      data_policy: "non_pii_allowlist_v2",
    }),
    {
      expirationTtl: 34560000,
      metadata: { received_at: receivedAt, name, path },
    },
  );

  return new Response(JSON.stringify({ ok: true, event_id: id }), { status: 202, headers });
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

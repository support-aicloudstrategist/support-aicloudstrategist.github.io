/**
 * Form-less visitor identification (AI Cloud Strategist).
 * Open-source / free stack only — see DigiScience identify.js for design notes.
 */

const MATOMO_BASE = "https://app.aicloudstrategist.cloud/matomo-aics";
const PROFILE_WAKE = "https://app.aicloudstrategist.cloud/visitor-profile/site-aicloudstrategist-com";
const COOKIE = "aics_vid";

const clean = (v: unknown, max = 200): string =>
  String(v == null ? "" : v).replace(/[\u0000-\u001f]/g, "").trim().slice(0, max);

function readVid(cookieHeader: string): string {
  const m = cookieHeader.match(/(?:^|;\s*)aics_vid=([a-f0-9]{16})/i);
  return m ? m[1].toLowerCase() : "";
}

function randomHex16(): string {
  const bytes = new Uint8Array(8);
  crypto.getRandomValues(bytes);
  return Array.from(bytes).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function ipv4PtrName(ip: string): string {
  const parts = String(ip || "").split(".");
  if (parts.length !== 4 || parts.some((p) => !/^\d{1,3}$/.test(p))) return "";
  return `${parts[3]}.${parts[2]}.${parts[1]}.${parts[0]}.in-addr.arpa`;
}

async function reverseDns(ip: string): Promise<string> {
  const name = ipv4PtrName(ip);
  if (!name) return "";
  try {
    const res = await fetch(`https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(name)}&type=PTR`, {
      headers: { Accept: "application/dns-json" },
    });
    if (!res.ok) return "";
    const data = (await res.json()) as { Answer?: Array<{ type: number; data?: string }> };
    const ans = Array.isArray(data.Answer) ? data.Answer.find((a) => a.type === 12 && a.data) : null;
    return clean(ans?.data ? String(ans.data).replace(/\.$/, "") : "", 180);
  } catch {
    return "";
  }
}

type CfGeo = {
  country?: string;
  region?: string;
  city?: string;
  postalCode?: string;
  timezone?: string;
  latitude?: string | number;
  longitude?: string | number;
  asOrganization?: string;
  colo?: string;
};

function geoFromRequest(request: Request) {
  const cf = ((request as Request & { cf?: CfGeo }).cf || {}) as CfGeo;
  return {
    ip: clean(request.headers.get("CF-Connecting-IP"), 64),
    country: clean(cf.country || request.headers.get("CF-IPCountry"), 2).toUpperCase(),
    region: clean(cf.region, 80),
    city: clean(cf.city, 80),
    postalCode: clean(cf.postalCode, 20),
    timezone: clean(cf.timezone, 64),
    latitude: cf.latitude != null ? String(cf.latitude).slice(0, 16) : "",
    longitude: cf.longitude != null ? String(cf.longitude).slice(0, 16) : "",
    asnOrg: clean(cf.asOrganization, 160),
    colo: clean(cf.colo, 16),
  };
}

export const onRequest: PagesFunction = async (context) => {
  const { request } = context;
  if (request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type",
        "Cache-Control": "no-store",
      },
    });
  }

  const geo = geoFromRequest(request);
  const vid = readVid(request.headers.get("Cookie") || "") || randomHex16();
  let body: Record<string, unknown> = {};
  if (request.method === "POST") {
    try {
      body = (await request.json()) as Record<string, unknown>;
    } catch {
      body = {};
    }
  }
  const ptr = geo.ip ? await reverseDns(geo.ip) : "";

  const profile = {
    company_slug: "site-aicloudstrategist-com",
    vid,
    fingerprint: clean(body.fingerprint, 64),
    name: clean(body.name, 120),
    email: clean(body.email, 160),
    phone: clean(body.phone, 40),
    company: clean(body.company, 160),
    page: clean(body.page, 200),
    url: clean(body.url, 500),
    referrer: clean(body.referrer || request.headers.get("Referer") || "", 400),
    deviceClass: clean(body.deviceClass, 40),
    behavior: {
      scrollMax: Number(body.scrollMax) || 0,
      dwellMs: Number(body.dwellMs) || 0,
      pages: Number(body.pages) || 1,
      clicks: Number(body.clicks) || 0,
      chatTurns: Number(body.chatTurns) || 0,
    },
    geo: { ...geo, ptrHost: ptr },
    ua: clean(request.headers.get("User-Agent"), 300),
    lang: clean(request.headers.get("Accept-Language"), 80),
    captured_at: new Date().toISOString(),
    contact_source: clean(
      body.contact_source || (body.email || body.phone || body.name ? "progressive_chat" : "browse_enrichment"),
      40
    ),
    pii_from_browse: false,
    pii_available: Boolean(body.name || body.email || body.phone),
  };

  const params = new URLSearchParams();
  params.set("idsite", "1");
  params.set("rec", "1");
  params.set("_id", vid);
  params.set("action_name", clean(body.page || "identify", 180) || "identify");
  params.set("url", clean(body.url || request.headers.get("Referer") || "https://aicloudstrategist.com/", 500));
  params.set("ua", profile.ua);
  params.set("lang", profile.lang);
  params.set(
    "_cvar",
    JSON.stringify({
      1: ["fingerprint", profile.fingerprint],
      2: ["asn_org", geo.asnOrg],
      3: ["city_region", [geo.city, geo.region, geo.country].filter(Boolean).join(", ")],
      4: ["ptr_host", ptr],
      5: ["device_class", profile.deviceClass],
    })
  );
  if (profile.name) params.set("dimension1", profile.name);
  if (profile.email) params.set("dimension2", profile.email);
  if (profile.phone) params.set("dimension3", profile.phone);
  if (profile.company || geo.asnOrg) params.set("dimension4", profile.company || geo.asnOrg);

  const hdrs: Record<string, string> = {
    "User-Agent": request.headers.get("User-Agent") || "Mozilla/5.0",
    "Accept-Language": request.headers.get("Accept-Language") || "en",
  };
  if (geo.ip) hdrs["X-Real-Visitor-IP"] = geo.ip;

  context.waitUntil(
    fetch(`${MATOMO_BASE}/matomo.php?${params.toString()}`, { method: "GET", headers: hdrs }).catch(() => null)
  );
  context.waitUntil(
    fetch(PROFILE_WAKE, {
      method: "POST",
      headers: { "content-type": "application/json", "user-agent": "AICSIdentify/1.0" },
      body: JSON.stringify(profile),
    }).catch(() => null)
  );

  return new Response(
    JSON.stringify({
      ok: true,
      vid,
      geo: {
        city: geo.city,
        region: geo.region,
        country: geo.country,
        timezone: geo.timezone,
        asnOrg: geo.asnOrg,
        ptrHost: ptr,
      },
      fingerprint: profile.fingerprint || null,
      identity: {
        name: profile.name || null,
        email: profile.email || null,
        phone: profile.phone || null,
        company: profile.company || geo.asnOrg || null,
      },
      limits: {
        anonymous_browse_yields: ["visitor_id", "fingerprint", "city", "region", "country", "asn_org", "ptr_host", "behavior"],
        requires_visitor_disclosure: ["personal_name", "email", "phone"],
      },
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "Set-Cookie": `${COOKIE}=${vid}; Path=/; Max-Age=31536000; SameSite=Lax; Secure`,
      },
    }
  );
};

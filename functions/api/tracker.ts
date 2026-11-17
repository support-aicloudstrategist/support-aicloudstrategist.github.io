const MATOMO_BASE = "https://app.aicloudstrategist.cloud/matomo-aics";

function readVidCookie(cookieHeader: string): string {
  const m = cookieHeader.match(/(?:^|;\s*)aics_vid=([a-f0-9]{16})/i);
  return m ? m[1].toLowerCase() : "";
}

function randomHex16(): string {
  const bytes = new Uint8Array(8);
  crypto.getRandomValues(bytes);
  return Array.from(bytes).map((b) => b.toString(16).padStart(2, "0")).join("");
}

export const onRequest: PagesFunction = async (context) => {
  const { request } = context;
  const url = new URL(request.url);
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: { "Cache-Control": "no-store" } });
  }

  if (request.method === "GET" && url.searchParams.get("js") === "1") {
    const cache = caches.default;
    const cacheKey = new Request(url.origin + "/api/tracker?js=1", { method: "GET" });
    const cached = await cache.match(cacheKey);
    if (cached) return cached;
    const upstream = await fetch(`${MATOMO_BASE}/matomo.js`, { headers: { "User-Agent": "AICSFirstPartyMatomo/1.0" } });
    if (!upstream.ok) {
      return new Response("/* tracker unavailable */", { status: 200, headers: { "Content-Type": "application/javascript; charset=utf-8", "Cache-Control": "no-store" } });
    }
    const body = await upstream.text();
    const resp = new Response(body, {
      status: 200,
      headers: { "Content-Type": "application/javascript; charset=utf-8", "Cache-Control": "public, max-age=3600" },
    });
    context.waitUntil(cache.put(cacheKey, resp.clone()));
    return resp;
  }

  const vid = readVidCookie(request.headers.get("Cookie") || "") || randomHex16();
  const params = new URLSearchParams(url.search);
  if (request.method === "POST") {
    const ct = request.headers.get("Content-Type") || "";
    if (ct.includes("application/x-www-form-urlencoded") || ct.includes("text/plain")) {
      const txt = await request.text();
      for (const [k, v] of new URLSearchParams(txt).entries()) params.set(k, v);
    }
  }
  params.set("idsite", "1");
  params.set("rec", "1");
  if (!params.get("_id")) params.set("_id", vid);

  const clientIp = request.headers.get("CF-Connecting-IP") || "";
  const hdrs: Record<string, string> = {
    "User-Agent": request.headers.get("User-Agent") || "Mozilla/5.0",
    "Accept-Language": request.headers.get("Accept-Language") || "en",
  };
  if (clientIp) hdrs["X-Real-Visitor-IP"] = clientIp;

  context.waitUntil(fetch(`${MATOMO_BASE}/matomo.php?${params.toString()}`, { method: "GET", headers: hdrs }).catch(() => null));

  return new Response(null, {
    status: 204,
    headers: {
      "Cache-Control": "no-store",
      "Set-Cookie": `aics_vid=${vid}; Path=/; Max-Age=31536000; SameSite=Lax; Secure`,
    },
  });
};

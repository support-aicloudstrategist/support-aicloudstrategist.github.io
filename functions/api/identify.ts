/**
 * Form-less visitor identification (AI Cloud Strategist).
 * Open-source / free stack — Team Cymru DoH, RDAP, PeeringDB, CF edge, PTR.
 * Honest limit: no person-level name/email/phone from IP alone.
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

const ISP_HOSTING_RE =
  /\b(isp|telecom|mobile|broadband|communications?|cable|dsl|wireless|cellular|comcast|verizon|at&?t|jio|airtel|bsnl|vodafone|idea|reliance jio|hostinger|amazon\.com|google llc|microsoft corporation|digitalocean|hetzner|ovh|cloudflare|akamai|fastly|linode|vultr|contabo|godaddy|aws|azure|gcp|oracle cloud|alibaba|tencent|softlayer|leaseweb|choopa|quadranet|cogent|level3|lumen|centurylink|charter|spectrum|cox communications|t-mobile|sprint|bt public|orange s\.?a|telefonica|deutsche telekom|singtel|telstra|ntt communications|pccw|china telecom|china unicom|china mobile)\b/i;

const PDB_CORP_HINT = /enterprise|business|corporation|limited|ltd|pvt|inc\.|gmbh|llc/i;

type Enrich = {
  ptrHost: string;
  cymru: { asn: string; prefix: string; registry: string; allocated: string };
  rdap: { name: string; handle: string; country: string; org: string; abuseEmail: string };
  peeringdb: {
    name: string;
    aka: string;
    website: string;
    infoType: string;
    infoTraffic: string;
    infoScope: string;
    orgId: string;
  };
  asn: string;
  networkType: string;
  companyCandidate: string | null;
  confidence: number;
  domainGuess: string | null;
  emailPatterns: string[];
  sources: string[];
};

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

async function teamCymru(ip: string) {
  const rawIp = String(ip || "");
  let name = "";
  const v4 = rawIp.split(".");
  if (v4.length === 4 && v4.every((p) => /^\d{1,3}$/.test(p))) {
    name = `${v4.join(".")}.origin.asn.cymru.com`;
  } else if (rawIp.includes(":")) {
    try {
      const parts = rawIp.split("::");
      const head = (parts[0] ? parts[0].split(":") : []).filter(Boolean);
      const tail = (parts[1] ? parts[1].split(":") : []).filter(Boolean);
      const miss = 8 - (head.length + tail.length);
      const full = [...head, ...Array(Math.max(miss, 0)).fill("0"), ...tail].map((h) => h.padStart(4, "0"));
      const nibbles = full.join("").split("").join(".");
      name = `${nibbles}.origin6.asn.cymru.com`;
    } catch {
      return { asn: "", prefix: "", registry: "", allocated: "" };
    }
  } else {
    return { asn: "", prefix: "", registry: "", allocated: "" };
  }
  try {
    const res = await fetch(`https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(name)}&type=TXT`, {
      headers: { Accept: "application/dns-json" },
    });
    if (!res.ok) return { asn: "", prefix: "", registry: "", allocated: "" };
    const data = (await res.json()) as { Answer?: Array<{ data?: string }> };
    const raw =
      Array.isArray(data.Answer) && data.Answer[0]?.data ? String(data.Answer[0].data).replace(/^"|"$/g, "") : "";
    const bits = raw.split("|").map((s) => s.trim());
    return {
      asn: clean(bits[0], 12),
      prefix: clean(bits[1], 40),
      registry: clean(bits[3], 20),
      allocated: clean(bits[4], 20),
    };
  } catch {
    return { asn: "", prefix: "", registry: "", allocated: "" };
  }
}

async function rdapLookup(ip: string) {
  if (!ip) return { name: "", handle: "", country: "", org: "", abuseEmail: "" };
  try {
    const res = await fetch(`https://rdap.org/ip/${encodeURIComponent(ip)}`, {
      headers: { Accept: "application/rdap+json, application/json" },
    });
    if (!res.ok) return { name: "", handle: "", country: "", org: "", abuseEmail: "" };
    const data = (await res.json()) as {
      name?: string;
      handle?: string;
      country?: string;
      entities?: Array<{ roles?: string[]; handle?: string; vcardArray?: unknown[] }>;
    };
    let org = "";
    let abuseEmail = "";
    for (const ent of data.entities || []) {
      const roles = (ent.roles || []).map((r) => String(r).toLowerCase());
      const vcard = ent.vcardArray && Array.isArray(ent.vcardArray[1]) ? (ent.vcardArray[1] as unknown[]) : [];
      for (const row of vcard) {
        if (!Array.isArray(row)) continue;
        if (row[0] === "fn" && roles.includes("registrant") && !org) org = clean(row[3], 160);
        if (row[0] === "email" && roles.includes("abuse") && !abuseEmail) abuseEmail = clean(row[3], 160);
      }
      if (!org && roles.includes("registrant") && ent.handle) org = clean(ent.handle, 160);
    }
    return {
      name: clean(data.name, 160),
      handle: clean(data.handle, 80),
      country: clean(data.country, 2).toUpperCase(),
      org,
      abuseEmail,
    };
  } catch {
    return { name: "", handle: "", country: "", org: "", abuseEmail: "" };
  }
}

async function peeringDb(asn: string) {
  const n = String(asn || "").replace(/^AS/i, "");
  if (!/^\d+$/.test(n)) {
    return { name: "", aka: "", website: "", infoType: "", infoTraffic: "", infoScope: "", orgId: "" };
  }
  try {
    const res = await fetch(`https://www.peeringdb.com/api/net?asn=${encodeURIComponent(n)}`, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return { name: "", aka: "", website: "", infoType: "", infoTraffic: "", infoScope: "", orgId: "" };
    const data = (await res.json()) as { data?: Array<Record<string, unknown>> };
    const net = Array.isArray(data.data) && data.data[0] ? data.data[0] : null;
    if (!net) return { name: "", aka: "", website: "", infoType: "", infoTraffic: "", infoScope: "", orgId: "" };
    return {
      name: clean(net.name, 160),
      aka: clean((net.aka as string) || (net.name_long as string), 160),
      website: clean(net.website, 200),
      infoType: clean(net.info_type, 80),
      infoTraffic: clean(net.info_traffic, 40),
      infoScope: clean(net.info_scope, 40),
      orgId: clean(net.org_id, 20),
    };
  } catch {
    return { name: "", aka: "", website: "", infoType: "", infoTraffic: "", infoScope: "", orgId: "" };
  }
}

function domainFromUrlOrHost(value: string): string {
  const raw = clean(value, 200).toLowerCase().replace(/^https?:\/\//, "").replace(/^www\./, "");
  if (!raw) return "";
  const host = raw.split("/")[0].split(":")[0];
  if (!host || !host.includes(".")) return "";
  const labels = host.split(".").filter(Boolean);
  if (labels.length < 2) return "";
  const multi = new Set(["co.uk", "com.au", "co.in", "com.br", "co.jp"]);
  const last2 = labels.slice(-2).join(".");
  const last3 = labels.slice(-3).join(".");
  if (multi.has(last2) && labels.length >= 3) return last3;
  return last2;
}

function emailPatternTemplates(domain: string): string[] {
  if (!domain || ISP_HOSTING_RE.test(domain)) return [];
  return [`{first}.{last}@${domain}`, `{first}@${domain}`, `{f}{last}@${domain}`, `{first}{last}@${domain}`];
}

function classifyNetwork(input: {
  asnOrg: string;
  pdb: Enrich["peeringdb"];
  rdap: Enrich["rdap"];
  ptrHost: string;
}) {
  const org = clean(input.asnOrg || input.pdb.name || input.rdap.org || "", 160);
  const infoType = clean(input.pdb.infoType, 80);
  const ptr = clean(input.ptrHost, 180);
  if (!org && !infoType) return { asnOrg: org, companyCandidate: "", networkType: "unknown", confidence: 0 };
  if (/cable\/dsl\/isp|nsp|content|route server|route collector/i.test(infoType)) {
    return { asnOrg: org || input.asnOrg, companyCandidate: "", networkType: "isp_or_hosting", confidence: 0.9 };
  }
  if (ISP_HOSTING_RE.test(org) || ISP_HOSTING_RE.test(ptr)) {
    return { asnOrg: org || input.asnOrg, companyCandidate: "", networkType: "isp_or_hosting", confidence: 0.85 };
  }
  if (/enterprise/i.test(infoType) || PDB_CORP_HINT.test(org) || PDB_CORP_HINT.test(input.pdb.aka || "")) {
    return {
      asnOrg: org || input.asnOrg,
      companyCandidate: clean(input.pdb.aka || org, 160),
      networkType: "possible_business",
      confidence: 0.7,
    };
  }
  if (org && !ISP_HOSTING_RE.test(org)) {
    return { asnOrg: org, companyCandidate: org, networkType: "possible_business", confidence: 0.55 };
  }
  return { asnOrg: org || input.asnOrg, companyCandidate: "", networkType: "isp_or_hosting", confidence: 0.5 };
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
  asn?: number | string;
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
    asnOrg: clean(cf.asOrganization || "", 160),
    colo: clean(cf.colo, 16),
    asn: cf.asn != null ? String(cf.asn) : "",
  };
}


async function ripeAsOverview(asn: string) {
  const n = String(asn || "").replace(/^AS/i, "");
  if (!/^\d+$/.test(n)) return { holder: "", type: "" };
  try {
    const res = await fetch(`https://stat.ripe.net/data/as-overview/data.json?resource=AS${encodeURIComponent(n)}`, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return { holder: "", type: "" };
    const data = (await res.json()) as { data?: { holder?: string; type?: string } };
    const d = data.data || {};
    return { holder: clean(d.holder, 160), type: clean(d.type, 40) };
  } catch {
    return { holder: "", type: "" };
  }
}

async function enrichIp(ip: string, cfAsnOrg: string, cfAsn: string): Promise<Enrich> {
  const [ptr, cymru, rdap] = await Promise.all([reverseDns(ip), teamCymru(ip), rdapLookup(ip)]);
  const asn = clean(cymru.asn || cfAsn, 12);
  const [pdb, ripe] = await Promise.all([peeringDb(asn), ripeAsOverview(asn)]);
  if (!pdb.name && ripe.holder) pdb.name = ripe.holder;
  if (!pdb.infoType && ripe.type) pdb.infoType = ripe.type;
  const classified = classifyNetwork({ asnOrg: cfAsnOrg || pdb.name || ripe.holder, pdb, rdap, ptrHost: ptr });
  const domain = domainFromUrlOrHost(pdb.website) || domainFromUrlOrHost(ptr) || "";
  const corporateDomain = classified.networkType === "possible_business" ? domain : "";
  return {
    ptrHost: ptr,
    cymru,
    rdap,
    peeringdb: pdb,
    asn: asn ? `AS${asn}` : "",
    networkType: classified.networkType,
    companyCandidate: classified.companyCandidate || null,
    confidence: classified.confidence,
    domainGuess: corporateDomain || null,
    emailPatterns: corporateDomain ? emailPatternTemplates(corporateDomain) : [],
    sources: ["cloudflare_edge", "team_cymru_doh", "rdap", "peeringdb", "ripe_stat", "ptr_doh"],
  };
}

const emptyEnrich = (): Enrich => ({
  ptrHost: "",
  cymru: { asn: "", prefix: "", registry: "", allocated: "" },
  rdap: { name: "", handle: "", country: "", org: "", abuseEmail: "" },
  peeringdb: { name: "", aka: "", website: "", infoType: "", infoTraffic: "", infoScope: "", orgId: "" },
  asn: "",
  networkType: "unknown",
  companyCandidate: null,
  confidence: 0,
  domainGuess: null,
  emailPatterns: [],
  sources: [],
});

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
  let body: Record<string, unknown> = {};
  if (request.method === "POST") {
    try {
      body = (await request.json()) as Record<string, unknown>;
    } catch {
      body = {};
    }
  }
  const bodyVid = clean(body.visitorId || body.vid, 36).toLowerCase();
  const cookieVid = readVid(request.headers.get("Cookie") || "");
  const vid = cookieVid || (/^[a-f0-9]{16}$/.test(bodyVid) ? bodyVid : "") || randomHex16();
  const enrich = geo.ip ? await enrichIp(geo.ip, geo.asnOrg, geo.asn) : emptyEnrich();

  const profile = {
    company_slug: "site-aicloudstrategist-com",
    vid,
    fingerprint: clean(body.fingerprint, 64),
    name: clean(body.name, 120),
    email: clean(body.email, 160),
    phone: clean(body.phone, 40),
    company: clean(body.company, 160),
    page: clean(body.page || body.path, 200),
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
    geo: {
      ...geo,
      ptrHost: enrich.ptrHost,
      networkType: enrich.networkType,
      companyCandidate: enrich.companyCandidate,
      asn: enrich.asn,
      domainGuess: enrich.domainGuess,
      emailPatterns: enrich.emailPatterns,
      confidence: enrich.confidence,
      rdapName: enrich.rdap.name,
      peeringdbName: enrich.peeringdb.name,
      peeringdbType: enrich.peeringdb.infoType,
      cymruPrefix: enrich.cymru.prefix,
    },
    enrichment: {
      sources: enrich.sources,
      emailPatterns: enrich.emailPatterns,
      domainGuess: enrich.domainGuess,
      confidence: enrich.confidence,
    },
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
      4: ["ptr_host", enrich.ptrHost],
      5: ["device_class", profile.deviceClass],
    })
  );
  if (profile.name) params.set("dimension1", profile.name);
  if (profile.email) params.set("dimension2", profile.email);
  if (profile.phone) params.set("dimension3", profile.phone);
  if (profile.company || enrich.companyCandidate || geo.asnOrg) {
    params.set("dimension4", profile.company || enrich.companyCandidate || geo.asnOrg);
  }

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
        asn: enrich.asn || null,
        ptrHost: enrich.ptrHost || null,
        networkType: enrich.networkType,
        companyCandidate: enrich.companyCandidate,
        domainGuess: enrich.domainGuess,
        confidence: enrich.confidence,
        peeringdbType: enrich.peeringdb.infoType || null,
        rdapName: enrich.rdap.name || null,
      },
      enrichment: {
        emailPatterns: enrich.emailPatterns,
        sources: enrich.sources,
        note: "emailPatterns are templates only; not real addresses",
      },
      fingerprint: profile.fingerprint || null,
      identity: {
        name: profile.name || null,
        email: profile.email || null,
        phone: profile.phone || null,
        company: profile.company || enrich.companyCandidate || null,
      },
      limits: {
        anonymous_browse_yields: [
          "visitor_id",
          "fingerprint",
          "city",
          "region",
          "country",
          "asn",
          "asn_org",
          "ptr_host",
          "rdap_network",
          "peeringdb_type",
          "behavior",
          "possible_business_org",
          "domain_guess",
          "email_pattern_templates",
        ],
        requires_visitor_disclosure: ["personal_name", "personal_email", "phone"],
        person_level_from_ip: false,
        email_patterns_are_templates_only: true,
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

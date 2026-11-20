import {
  classifyTraffic,
  isPrivateRoute,
  normalizePath,
  storageTrafficBucket,
} from "./_lib/analytics-rules";

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
  "traffic_class",
  "trigger",
  "via",
  "api",
  "depth",
  "seconds",
  "dwell_mode",
  "visible_seconds",
  "hidden_seconds",
]);

function normalizeTrafficClass(value: unknown, path: string, ua: string) {
  // Central classifier — never auto-promote unmarked traffic to external.
  return storageTrafficBucket(
    classifyTraffic({ path, ua, clientClass: value }),
  );
}

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
  const path =
    rawPath.startsWith("/") && !rawPath.includes("?") && !rawPath.includes("#")
      ? normalizePath(rawPath)
      : "/";
  // Private / operational routes must never create public analytics records.
  if (isPrivateRoute(path)) {
    return new Response(JSON.stringify({ ok: true, dropped: true, reason: "private_route" }), {
      status: 202,
      headers,
    });
  }
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
  const ua = request.headers.get("User-Agent") || "";
  if (!props.country && cf?.country) props.country = clean(cf.country, 8).toUpperCase();
  if (!props.browser) props.browser = browserFromUa(ua);
  props.traffic_class = normalizeTrafficClass(props.traffic_class, path, ua);

  const receivedAt = new Date().toISOString();
  const day = receivedAt.slice(0, 10);
  const id = `event:${day}:${crypto.randomUUID()}`;
  const record = {
    event_id: id,
    received_at: receivedAt,
    name,
    path,
    session,
    props,
    data_policy: "non_pii_allowlist_v2",
  };

  // Raw event (for forensic detail when KV list quota allows) + day rollup for list-free dashboards.
  await env.LEAD_LOG.put(id, JSON.stringify(record), {
    expirationTtl: 34560000,
    metadata: { received_at: receivedAt, name, path },
  });

  try {
    await bumpDayAggregate(env.LEAD_LOG, day, record);
  } catch {
    // Aggregate is best-effort; never fail the collector on rollup issues.
  }

  return new Response(JSON.stringify({ ok: true, event_id: id }), { status: 202, headers });
};

type PathStats = {
  page_views: number;
  cta_clicks: number;
  scroll_50_plus: number;
  downloads: number;
  /** Sum of per-session max active dwell seconds (not cumulative tick totals). */
  dwell_sum: number;
  dwell_samples: number;
  /** session -> max active dwell seconds observed for this path */
  dwell_by_session?: Record<string, number>;
};

type DayAggSlice = {
  totals: Record<string, number>;
  /** Events that arrived without a valid public page-view anchor in this slice. */
  orphan_totals: Record<string, number>;
  page_views: number;
  sessions: Record<string, true>;
  visitors: Record<string, true>;
  /** visitor_id -> country from first valid public page view (unique-visitor geography). */
  visitor_geo: Record<string, string>;
  countries: Record<string, number>;
  browsers: Record<string, number>;
  devices: Record<string, number>;
  providers: Record<string, number>;
  visitor_kinds: Record<string, number>;
  traffic_buckets: Record<string, number>;
  paths: Record<string, PathStats>;
};

type DayAgg = DayAggSlice & {
  day: string;
  updated_at: string;
  live?: Array<{ at: string; name: string; path: string; session: string; country: string; source: string; traffic_class?: string }>;
  /** Per-audience rollups. Legacy days without by_class are treated as Unknown at read time. */
  by_class?: Partial<Record<"external" | "internal" | "bot" | "unknown", DayAggSlice>>;
};

function emptySlice(): DayAggSlice {
  return {
    totals: {},
    orphan_totals: {},
    page_views: 0,
    sessions: {},
    visitors: {},
    visitor_geo: {},
    countries: {},
    browsers: {},
    devices: {},
    providers: {},
    visitor_kinds: {},
    traffic_buckets: {},
    paths: {},
  };
}

function ensurePath(paths: Record<string, PathStats>, path: string): PathStats {
  if (!paths[path]) {
    paths[path] = {
      page_views: 0,
      cta_clicks: 0,
      scroll_50_plus: 0,
      downloads: 0,
      dwell_sum: 0,
      dwell_samples: 0,
      dwell_by_session: {},
    };
  }
  if (!paths[path].dwell_by_session) paths[path].dwell_by_session = {};
  return paths[path];
}

function trimSetMap(map: Record<string, true>, keep = 600, max = 800) {
  const ids = Object.keys(map);
  if (ids.length > max) {
    for (const id of ids.slice(0, ids.length - keep)) delete map[id];
  }
}

/**
 * Business KPIs require a valid public page-view anchor.
 * Telemetry without an anchored session is counted only under orphan_totals.
 */
function applyEventToSlice(
  slice: DayAggSlice,
  event: { name: string; path: string; session: string; props: Record<string, string> },
) {
  if (!slice.orphan_totals) slice.orphan_totals = {};
  if (!slice.visitor_geo) slice.visitor_geo = {};

  bumpMap(slice.totals, event.name);

  const privatePath = isPrivateRoute(event.path);
  const provider = clean(event.props.provider, 120) || "direct";
  const channel = clean(event.props.channel, 120);
  const campaign = clean(event.props.campaign, 120);
  const device = clean(event.props.device, 40) || "unknown";
  const browser = clean(event.props.browser, 40) || "unknown";
  const country = (clean(event.props.country, 8) || "unknown").toUpperCase();
  const visitorKind = clean(event.props.visitor_kind, 24) || "unknown";
  const visitor = clean(event.props.visitor, 64);
  const depth = Number(event.props.depth || 0);
  const seconds = Number(event.props.seconds || 0);
  const isDelta = clean(event.props.dwell_mode, 24) === "delta";

  // Private routes never enter content-performance path stats (collection also drops them).
  if (privatePath) {
    bumpMap(slice.orphan_totals, event.name);
    return;
  }

  if (event.name === "page_view") {
    slice.page_views += 1;
    if (event.session) {
      slice.sessions[event.session] = true;
      trimSetMap(slice.sessions);
    }
    if (visitor) {
      slice.visitors[visitor] = true;
      trimSetMap(slice.visitors);
      // First valid public page view wins country for this visitor (deterministic).
      if (!slice.visitor_geo[visitor]) slice.visitor_geo[visitor] = country;
      // Keep countries map in sync with unique visitor geography for new data.
      slice.countries = {};
      for (const c of Object.values(slice.visitor_geo)) bumpMap(slice.countries, c || "UNKNOWN");
    } else {
      bumpMap(slice.countries, country);
    }
    bumpMap(slice.providers, provider);
    bumpMap(slice.devices, device);
    bumpMap(slice.browsers, browser);
    bumpMap(slice.visitor_kinds, visitorKind);
    bumpMap(slice.traffic_buckets, classifySource(provider, channel, campaign));
    ensurePath(slice.paths, event.path).page_views += 1;
    return;
  }

  const sessionAnchored = Boolean(event.session && slice.sessions[event.session]);
  if (!sessionAnchored) {
    // Orphan / unanchored: dwell, engagement, presence without a prior page_view in this slice.
    bumpMap(slice.orphan_totals, event.name);
    return;
  }

  if (event.name === "cta_click" || event.name === "button_click") {
    ensurePath(slice.paths, event.path).cta_clicks += 1;
  }
  if (event.name === "download_click") {
    ensurePath(slice.paths, event.path).downloads += 1;
  }
  if (event.name === "scroll_depth" && depth >= 50) {
    ensurePath(slice.paths, event.path).scroll_50_plus += 1;
  }
  if (event.name === "dwell_tick" && Number.isFinite(seconds) && seconds > 0) {
    const row = ensurePath(slice.paths, event.path);
    const sid = event.session || "unknown";
    const prev = row.dwell_by_session![sid] || 0;
    // Delta mode: accumulate active visible seconds. Legacy cumulative: keep max per session.
    const next = isDelta ? prev + seconds : Math.max(prev, seconds);
    // Flag unusually long sessions in diagnostics via totals; still store measured value.
    if (next > 3600) bumpMap(slice.orphan_totals, "dwell_long_session_flag");
    row.dwell_by_session![sid] = next;
    // Recompute path dwell from per-session maxima (idempotent; avoids double-counting ticks).
    const vals = Object.values(row.dwell_by_session!);
    row.dwell_samples = vals.length;
    row.dwell_sum = vals.reduce((a, b) => a + b, 0);
  }
}

function classifySource(provider: string, channel: string, campaign: string) {
  const p = provider.toLowerCase();
  const c = channel.toLowerCase();
  if (campaign || c.includes("cpc") || c.includes("ppc") || c.includes("paid")) return "campaigns";
  if (p === "google" || p === "bing") return "search";
  if (
    p.includes("linkedin") ||
    p.includes("twitter") ||
    p.includes("x.com") ||
    p.includes("facebook") ||
    p.includes("instagram") ||
    p.includes("youtube") ||
    c.includes("social")
  ) {
    return "social";
  }
  if (p === "direct" || !p) return "direct";
  if (p === "referral" || p.includes(".")) return "referrals";
  return p || "other";
}

function bumpMap(map: Record<string, number>, key: string, by = 1) {
  const k = key || "unknown";
  map[k] = (map[k] || 0) + by;
}

async function bumpDayAggregate(
  store: KVNamespace,
  day: string,
  event: {
    received_at: string;
    name: string;
    path: string;
    session: string;
    props: Record<string, string>;
  },
) {
  const key = `agg:v1:day:${day}`;
  const raw = await store.get(key);
  const agg: DayAgg = raw
    ? (JSON.parse(raw) as DayAgg)
    : {
        day,
        updated_at: event.received_at,
        ...emptySlice(),
        live: [],
        by_class: {},
      };

  agg.updated_at = event.received_at;
  if (!agg.by_class) agg.by_class = {};
  const trafficClass = (["external", "internal", "bot", "unknown"].includes(event.props.traffic_class)
    ? event.props.traffic_class
    : "unknown") as "external" | "internal" | "bot" | "unknown";

  // Top-level = All Traffic. by_class keeps filterable slices without rewriting history.
  applyEventToSlice(agg, event);
  if (!agg.by_class[trafficClass]) agg.by_class[trafficClass] = emptySlice();
  applyEventToSlice(agg.by_class[trafficClass]!, event);

  const provider = clean(event.props.provider, 120) || "direct";
  const channel = clean(event.props.channel, 120);
  const campaign = clean(event.props.campaign, 120);
  const country = clean(event.props.country, 8) || "unknown";
  const live = Array.isArray(agg.live) ? agg.live : [];
  live.unshift({
    at: event.received_at,
    name: event.name,
    path: event.path,
    session: event.session,
    country,
    source: classifySource(provider, channel, campaign),
    traffic_class: trafficClass,
  });
  agg.live = live.slice(0, 40);

  await store.put(key, JSON.stringify(agg), { expirationTtl: 34560000 });
}

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });

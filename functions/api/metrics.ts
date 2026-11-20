import {
  geographyFromLegacyCountryCounts,
  geographyFromVisitorGeo,
  isPrivateRoute,
  labelEvents,
  meaningfulEngagementTotal,
  normalizeAudience,
  normalizePath,
  partitionEventTotals,
  validateReportInvariants,
  type AudienceFilter,
} from "./_lib/analytics-rules";

type MetricsEnv = {
  LEAD_LOG?: KVNamespace;
  CONTACT_LOG?: KVNamespace;
  AICS_REPORT_TOKEN?: string;
};

type StoredEvent = {
  name?: string;
  path?: string;
  session?: string;
  received_at?: string;
  props?: Record<string, string>;
};

type StoredLead = {
  contact_id?: string;
  submitted_at?: string;
  name?: string;
  contact?: string;
  company?: string;
  role?: string;
  service?: string;
  stage?: string;
  need?: string;
  message?: string;
  source?: string;
  landing_page?: string;
  referrer?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  lead_status?: string;
};

type KeyMeta = { received_at?: string; name?: string; path?: string };

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "private, max-age=20",
};

const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

/** Normalize pasted/header tokens: trim, strip wrapping quotes, strip accidental Bearer prefix. */
function normalizeToken(value: unknown, max = 512) {
  let token = String(value ?? "")
    .replace(/^\uFEFF/, "")
    .trim()
    .slice(0, max);
  if (
    (token.startsWith('"') && token.endsWith('"')) ||
    (token.startsWith("'") && token.endsWith("'"))
  ) {
    token = token.slice(1, -1).trim();
  }
  token = token.replace(/^Bearer\s+/i, "").trim();
  return token;
}

function extractBearerToken(request: Request) {
  const raw = request.headers.get("Authorization") || request.headers.get("X-AICS-Report-Token") || "";
  const match = raw.match(/^Bearer\s+(.+)$/i);
  if (match) return normalizeToken(match[1], 512);
  // Allow raw token in Authorization for paste mistakes, plus dedicated header.
  return normalizeToken(raw, 512);
}

// Same read-only Company Agents hash used by /api/leads (hash only; plaintext never stored in repo).
const PRODUCT_READER_SHA256 = "95c7ac6b1f2ed3024b6bb22333cb9cb1414c01c4d6c1179ff967d857068bacdf";

type AuthResult =
  | { ok: true; token: string }
  | { ok: false; status: number; error: string; code: string };

async function sha256Hex(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function authorize(request: Request, env: MetricsEnv): Promise<AuthResult> {
  const configured = normalizeToken(env.AICS_REPORT_TOKEN, 512);
  const supplied = extractBearerToken(request);

  if (!supplied) {
    return {
      ok: false,
      status: 401,
      code: "missing_authorization",
      error: "No access key provided. Paste your access key and click Load.",
    };
  }

  // Accept either the Pages secret or the shared Company Agents reader token.
  if (configured && supplied === configured) {
    return { ok: true, token: supplied };
  }
  if ((await sha256Hex(supplied)) === PRODUCT_READER_SHA256) {
    return { ok: true, token: supplied };
  }

  if (!configured) {
    return {
      ok: false,
      status: 503,
      code: "server_token_missing",
      error:
        "Server misconfigured: AICS_REPORT_TOKEN is missing in Cloudflare Pages Production. Add the secret, then redeploy.",
    };
  }

  return {
    ok: false,
    status: 401,
    code: "invalid_token",
    error:
      "Access key does not match. Use the Production AICS_REPORT_TOKEN (not Preview), or the Company Agents reader key.",
  };
}

function dayKey(iso: string) {
  return iso.slice(0, 10) || "unknown";
}

function bump(map: Record<string, number>, key: string, by = 1) {
  const k = key || "unknown";
  map[k] = (map[k] || 0) + by;
}

function topEntries(map: Record<string, number>, limit = 20) {
  return Object.entries(map)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([key, count]) => ({ key, count }));
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

function eachDay(fromMs: number, toMs: number): string[] {
  const days: string[] = [];
  const start = new Date(fromMs);
  start.setUTCHours(0, 0, 0, 0);
  for (let t = start.getTime(); t <= toMs; t += 86400000) {
    days.push(new Date(t).toISOString().slice(0, 10));
  }
  return days;
}

function isKvQuotaError(error: unknown) {
  const message = error instanceof Error ? error.message : String(error ?? "");
  return /list\(\)\s*limit|operation limit|limit exceeded|429|quota/i.test(message);
}

const DASHBOARD_CACHE_TTL_SEC = 180;
const REALTIME_CACHE_TTL_SEC = 45;
const LAST_KNOWN_CACHE_TTL_SEC = 86400;

function metricsCacheKey(
  kind: "dashboard" | "realtime",
  days: number,
  fromIso: string,
  toIso: string,
  audience = "external",
) {
  const fromDay = fromIso.slice(0, 10) || "na";
  const toDay = toIso.slice(0, 10) || "na";
  return `cache:metrics:v3:${kind}:a${audience}:d${days}:${fromDay}:${toDay}`;
}

function meaningfulEngagement(totals: Record<string, number>) {
  return meaningfulEngagementTotal(totals);
}

async function readMetricsCache(store: KVNamespace | undefined, key: string, allowLastKnown = false) {
  if (!store) return null;
  try {
    const raw = await store.get(key);
    if (raw) return JSON.parse(raw) as Record<string, unknown>;
    if (!allowLastKnown) return null;
    const last = await store.get(`${key}:last`);
    if (!last) return null;
    return JSON.parse(last) as Record<string, unknown>;
  } catch {
    return null;
  }
}

async function writeMetricsCache(
  store: KVNamespace | undefined,
  key: string,
  payload: Record<string, unknown>,
  ttlSec: number,
) {
  if (!store) return;
  try {
    // Cache writes use get/put only (no list). Fresh TTL for normal hits; 24h last-known for quota fallback.
    const body = JSON.stringify(payload);
    await store.put(key, body, { expirationTtl: Math.max(60, ttlSec) });
    await store.put(`${key}:last`, body, { expirationTtl: LAST_KNOWN_CACHE_TTL_SEC });
  } catch {
    // Ignore cache write failures; primary response still returns.
  }
}

async function listKeysForPrefix(store: KVNamespace, prefix: string, maxKeys: number) {
  const keys: Array<{ name: string; metadata?: KeyMeta }> = [];
  let cursor: string | undefined;
  do {
    let page: KVNamespaceListResult<KeyMeta>;
    try {
      page = await store.list({ prefix, limit: Math.min(1000, maxKeys - keys.length), cursor });
    } catch (error) {
      if (isKvQuotaError(error)) {
        throw new Error("KV list() limit exceeded for the day.");
      }
      throw error;
    }
    for (const key of page.keys) {
      keys.push({ name: key.name, metadata: key.metadata as KeyMeta | undefined });
      if (keys.length >= maxKeys) return keys;
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return keys;
}

async function getMany(store: KVNamespace, names: string[], batchSize = 40) {
  const out = new Map<string, string | null>();
  for (let i = 0; i < names.length; i += batchSize) {
    const chunk = names.slice(i, i + batchSize);
    const values = await Promise.all(chunk.map((name) => store.get(name)));
    chunk.forEach((name, idx) => out.set(name, values[idx]));
  }
  return out;
}

type DayAggSlice = {
  totals?: Record<string, number>;
  orphan_totals?: Record<string, number>;
  page_views?: number;
  sessions?: Record<string, true>;
  visitors?: Record<string, true>;
  visitor_geo?: Record<string, string>;
  countries?: Record<string, number>;
  browsers?: Record<string, number>;
  devices?: Record<string, number>;
  providers?: Record<string, number>;
  visitor_kinds?: Record<string, number>;
  traffic_buckets?: Record<string, number>;
  paths?: Record<
    string,
    {
      page_views?: number;
      cta_clicks?: number;
      scroll_50_plus?: number;
      downloads?: number;
      dwell_sum?: number;
      dwell_samples?: number;
      dwell_by_session?: Record<string, number>;
    }
  >;
};

type DayAgg = DayAggSlice & {
  day?: string;
  updated_at?: string;
  live?: Array<{
    at?: string;
    name?: string;
    path?: string;
    session?: string;
    country?: string;
    source?: string;
    traffic_class?: string;
  }>;
  by_class?: Partial<Record<"external" | "internal" | "bot" | "unknown", DayAggSlice>>;
};

/** Resolve the rollup slice for an audience filter. Legacy days without by_class = Unknown only. */
function sliceForAudience(agg: DayAgg, audience: AudienceFilter): DayAggSlice | null {
  if (audience === "all") return agg;
  const hasClass = agg.by_class && Object.keys(agg.by_class).length > 0;
  if (!hasClass) {
    // Historical / restored rollups without traffic_class → Unknown (never auto-external).
    return audience === "unknown" ? agg : null;
  }
  return agg.by_class?.[audience as "external" | "internal" | "bot" | "unknown"] || null;
}

async function loadDayAggregates(store: KVNamespace | undefined, days: string[]) {
  if (!store || !days.length) return [] as DayAgg[];
  const bodies = await getMany(
    store,
    days.map((day) => `agg:v1:day:${day}`),
    20,
  );
  const out: DayAgg[] = [];
  for (const day of days) {
    const raw = bodies.get(`agg:v1:day:${day}`);
    if (!raw) continue;
    try {
      out.push(JSON.parse(raw) as DayAgg);
    } catch {
      // skip bad rollup
    }
  }
  return out;
}

async function loadLeads(
  stores: Array<KVNamespace | undefined>,
  cutoff: number,
  rangeEnd: number,
  maxKeys = 500,
) {
  const leads: Array<Record<string, string>> = [];
  const seen = new Set<string>();

  for (const store of stores) {
    if (!store) continue;

    // Prefer list-free index maintained by /api/contact.
    let leadKeyNames: string[] = [];
    try {
      const indexRaw = await store.get("agg:v1:leads:index");
      if (indexRaw) {
        const parsed = JSON.parse(indexRaw) as { keys?: string[] };
        if (Array.isArray(parsed.keys)) leadKeyNames = parsed.keys.slice(0, maxKeys);
      }
    } catch {
      leadKeyNames = [];
    }

    // Never fall back to KV list() here — free-plan daily list quota must stay reserved
    // for optional ?scan=raw rebuilds. Without an index, skip contacts for this store.
    if (!leadKeyNames.length) continue;

    const leadBodies = await getMany(store, leadKeyNames, 40);
    for (const keyName of leadKeyNames) {
      if (seen.has(keyName)) continue;
      const raw = leadBodies.get(keyName);
      if (!raw) continue;
      try {
        const lead = JSON.parse(raw) as StoredLead;
        const submittedAt = clean(lead.submitted_at, 40);
        const ts = Date.parse(submittedAt);
        if (Number.isFinite(ts) && (ts < cutoff || ts > rangeEnd)) continue;
        seen.add(keyName);
        leads.push({
          contact_id: clean(lead.contact_id || keyName, 120),
          submitted_at: submittedAt,
          name: clean(lead.name, 160),
          email: clean(lead.contact, 320),
          company: clean(lead.company, 160),
          role: clean(lead.role, 160),
          stage: clean(lead.stage, 160),
          source: clean(lead.source, 80),
          service: clean(lead.service, 160),
          landing_page: clean(lead.landing_page, 400),
          referrer: clean(lead.referrer, 400),
          utm_source: clean(lead.utm_source, 120),
          utm_medium: clean(lead.utm_medium, 120),
          utm_campaign: clean(lead.utm_campaign, 120),
          need: clean(lead.need, 240),
          message: clean(lead.message, 400),
          lead_status: clean(lead.lead_status, 40),
        });
      } catch {
        // Skip malformed lead rows.
      }
    }
  }

  leads.sort((a, b) => String(b.submitted_at).localeCompare(String(a.submitted_at)));
  return leads;
}

export const onRequestGet: PagesFunction<MetricsEnv> = async ({ request, env }) => {
  const started = Date.now();
  try {
    const auth = await authorize(request, env);
    if (!auth.ok) {
      return new Response(
        JSON.stringify({ ok: false, error: auth.error, code: auth.code }),
        { status: auth.status, headers },
      );
    }

    const eventStore = env.LEAD_LOG;
    const leadStore = env.CONTACT_LOG || env.LEAD_LOG;
    if (!eventStore && !leadStore) {
      return new Response(JSON.stringify({ ok: false, error: "Metrics store unavailable" }), {
        status: 503,
        headers,
      });
    }

    const url = new URL(request.url);
    const mode = clean(url.searchParams.get("mode") || "dashboard", 40);
    const realtimeOnly = mode === "realtime" || url.searchParams.get("realtime") === "1";
    const forceRefresh = url.searchParams.get("refresh") === "1";
    const audience = normalizeAudience(url.searchParams.get("audience") || url.searchParams.get("traffic"));
    const days = Math.min(90, Math.max(1, Number(url.searchParams.get("days") || 28)));
    const fromParam = clean(url.searchParams.get("from"), 32);
    const toParam = clean(url.searchParams.get("to"), 32);
    const now = Date.now();
    let cutoff = now - days * 86400000;
    let rangeEnd = now;
    if (fromParam && Date.parse(fromParam)) cutoff = Date.parse(fromParam);
    if (toParam && Date.parse(toParam)) rangeEnd = Date.parse(toParam) + 86400000 - 1;

    const cacheStore = eventStore || leadStore;
    const cacheKind = realtimeOnly ? "realtime" : "dashboard";
    const cacheKey = metricsCacheKey(
      cacheKind,
      days,
      new Date(cutoff).toISOString(),
      new Date(rangeEnd).toISOString(),
      audience,
    );
    const cacheTtl = realtimeOnly ? REALTIME_CACHE_TTL_SEC : DASHBOARD_CACHE_TTL_SEC;

    const preferAggregates = url.searchParams.get("scan") !== "raw";

    // Cache only for the aggregate path. Raw scans must never be short-circuited by a stale rollup.
    if (!forceRefresh && preferAggregates) {
      const cached = await readMetricsCache(cacheStore, cacheKey);
      if (cached && cached.ok === true) {
        return new Response(
          JSON.stringify({
            ...cached,
            from_cache: true,
            cache_key: cacheKey,
            duration_ms: Date.now() - started,
          }),
          { status: 200, headers },
        );
      }
    }

    const liveWindowMs = 2 * 60 * 1000;
    const enterWindowMs = 5 * 60 * 1000;

    // Primary path: day rollups via KV get() only — avoids the free-plan daily list() quota.
    if (preferAggregates && eventStore) {
      const dayList = realtimeOnly
        ? eachDay(now - liveWindowMs - 86400000, now)
        : eachDay(cutoff, rangeEnd);
      const aggs = await loadDayAggregates(eventStore, dayList);
      const totals: Record<string, number> = {};
      const orphanTotals: Record<string, number> = {};
      const providers: Record<string, number> = {};
      const devices: Record<string, number> = {};
      const browsers: Record<string, number> = {};
      const visitorKinds: Record<string, number> = {};
      const trafficBuckets: Record<string, number> = {};
      const pathViews: Record<string, number> = {};
      const pathCta: Record<string, number> = {};
      const pathScroll: Record<string, number> = {};
      const pathDwellSum: Record<string, number> = {};
      const pathDwellCount: Record<string, number> = {};
      const pathDownloads: Record<string, number> = {};
      const dailyViews: Record<string, number> = {};
      const dailySessions: Record<string, number> = {};
      const sessionSeen = new Set<string>();
      const visitorSeen = new Set<string>();
      const visitorGeoMerged: Record<string, string> = {};
      const legacyCountryCounts: Record<string, number> = {};
      let hasVisitorGeo = false;
      const liveSessions = new Set<string>();
      const livePages: Record<string, number> = {};
      const liveSources: Record<string, number> = {};
      const liveLocations: Record<string, number> = {};
      const enteringSessions = new Set<string>();
      const feed: Array<Record<string, string>> = [];

      for (const agg of aggs) {
        const day = clean(agg.day, 12);
        const slice = sliceForAudience(agg, audience);
        if (!slice) continue;
        for (const [k, v] of Object.entries(slice.totals || {})) bump(totals, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.orphan_totals || {})) bump(orphanTotals, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.providers || {})) bump(providers, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.devices || {})) bump(devices, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.browsers || {})) bump(browsers, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.countries || {})) bump(legacyCountryCounts, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.visitor_kinds || {})) bump(visitorKinds, k, Number(v) || 0);
        for (const [k, v] of Object.entries(slice.traffic_buckets || {})) bump(trafficBuckets, k, Number(v) || 0);
        bump(dailyViews, day, Number(slice.page_views) || 0);
        const daySessions = Object.keys(slice.sessions || {});
        bump(dailySessions, day, daySessions.length);
        for (const s of daySessions) sessionSeen.add(s);
        for (const v of Object.keys(slice.visitors || {})) visitorSeen.add(v);
        for (const [vid, country] of Object.entries(slice.visitor_geo || {})) {
          hasVisitorGeo = true;
          // First valid public page view in range wins (earlier days processed first via eachDay order).
          if (!visitorGeoMerged[vid]) visitorGeoMerged[vid] = country;
        }
        for (const [path, stats] of Object.entries(slice.paths || {})) {
          if (isPrivateRoute(path)) continue;
          bump(pathViews, path, Number(stats.page_views) || 0);
          bump(pathCta, path, Number(stats.cta_clicks) || 0);
          bump(pathScroll, path, Number(stats.scroll_50_plus) || 0);
          bump(pathDownloads, path, Number(stats.downloads) || 0);
          // Prefer per-session maxima when present (new schema); else legacy dwell_sum/samples.
          const bySession = stats.dwell_by_session || {};
          const sessionVals = Object.values(bySession);
          if (sessionVals.length) {
            pathDwellSum[path] = (pathDwellSum[path] || 0) + sessionVals.reduce((a, b) => a + (Number(b) || 0), 0);
            pathDwellCount[path] = (pathDwellCount[path] || 0) + sessionVals.length;
          } else {
            pathDwellSum[path] = (pathDwellSum[path] || 0) + (Number(stats.dwell_sum) || 0);
            pathDwellCount[path] = (pathDwellCount[path] || 0) + (Number(stats.dwell_samples) || 0);
          }
        }
        for (const row of agg.live || []) {
          const rowClass = clean(row.traffic_class, 24) || "unknown";
          if (audience !== "all" && rowClass !== audience) {
            if (!(audience === "unknown" && !agg.by_class)) continue;
          }
          if (audience === "external" && rowClass !== "external") continue;
          if (audience === "internal" && rowClass !== "internal") continue;
          if (audience === "bot" && rowClass !== "bot") continue;
          const at = clean(row.at, 40);
          const ts = Date.parse(at);
          const session = clean(row.session, 64);
          const path = normalizePath(row.path || "/");
          // Live content panels exclude private routes; feed may note them as admin-only.
          const privateLive = isPrivateRoute(path);
          if (Number.isFinite(ts) && now - ts <= liveWindowMs && session && !privateLive) {
            liveSessions.add(session);
            bump(livePages, path);
            bump(liveSources, clean(row.source, 40) || "direct");
            bump(liveLocations, clean(row.country, 8) || "unknown");
          }
          if (
            Number.isFinite(ts) &&
            now - ts <= enterWindowMs &&
            session &&
            row.name === "page_view" &&
            !privateLive
          ) {
            enteringSessions.add(session);
          }
          if (feed.length < 40 && !privateLive) {
            feed.push({
              at,
              name: clean(row.name, 64),
              path,
              detail: clean(row.source || row.country, 80),
            });
          }
        }
      }

      feed.sort((a, b) => String(b.at).localeCompare(String(a.at)));

      if (realtimeOnly) {
        const realtimePayload: Record<string, unknown> = {
          ok: true,
          mode: "realtime",
          source: "day_aggregates",
          generated_at: new Date().toISOString(),
          duration_ms: Date.now() - started,
          realtime: {
            live_visitors: liveSessions.size,
            entering_visitors: enteringSessions.size,
            window_seconds: Math.round(liveWindowMs / 1000),
            enter_window_seconds: Math.round(enterWindowMs / 1000),
            pages_in_view: topEntries(livePages, 15),
            traffic_sources: topEntries(liveSources, 10),
            locations: topEntries(liveLocations, 15),
            feed: feed.slice(0, 25),
            refresh_hint_seconds: 45,
            identity: "Live visitor panels are aggregated only. Contacts below are voluntary form submissions.",
          },
        };
        await writeMetricsCache(cacheStore, cacheKey, realtimePayload, cacheTtl);
        return new Response(JSON.stringify(realtimePayload), { status: 200, headers });
      }

      let pageViews = totals.page_view || Object.values(dailyViews).reduce((a, b) => a + b, 0);
      // Page-view anchor: without valid views, business KPIs must be zero (orphans → diagnostics only).
      const anchored = pageViews > 0;
      let reportVisitors = anchored ? visitorSeen.size : 0;
      let reportSessions = anchored ? sessionSeen.size : 0;
      if (!anchored) {
        for (const day of Object.keys(dailySessions)) dailySessions[day] = 0;
      }

      const geo = hasVisitorGeo
        ? geographyFromVisitorGeo(visitorGeoMerged, anchored ? visitorSeen : [])
        : geographyFromLegacyCountryCounts(legacyCountryCounts, reportVisitors);
      const countries = geo.countries;
      const locationRows = topEntries(countries, 25);
      const locationDenominator = geo.denominator;
      const locationSum = locationRows.reduce((sum, row) => sum + (row.count || 0), 0);

      let content = Object.keys({ ...pathViews, ...pathDwellSum })
        .filter((path) => !isPrivateRoute(path))
        .filter((path) => (pathViews[path] || 0) > 0 || (pathDwellCount[path] || 0) > 0)
        .map((path) => {
          const views = pathViews[path] || 0;
          const cta = pathCta[path] || 0;
          const dwellSamples = pathDwellCount[path] || 0;
          // Dwell without page views is orphaned — do not publish page metrics.
          const publishDwell = views > 0 && dwellSamples > 0;
          const avgDwell = publishDwell ? Math.round((pathDwellSum[path] || 0) / dwellSamples) : null;
          return {
            path,
            page_views: views,
            cta_clicks: views > 0 ? cta : 0,
            cta_rate: views ? Number(((cta / views) * 100).toFixed(1)) : 0,
            scroll_50_plus: views > 0 ? pathScroll[path] || 0 : 0,
            downloads: views > 0 ? pathDownloads[path] || 0 : 0,
            avg_dwell_seconds: avgDwell,
            dwell_available: publishDwell,
            dwell_samples: publishDwell ? dwellSamples : 0,
          };
        })
        .filter((row) => row.page_views > 0)
        .sort(
          (a, b) =>
            (b.avg_dwell_seconds || 0) - (a.avg_dwell_seconds || 0) || b.page_views - a.page_views,
        )
        .slice(0, 40);

      if (!anchored) content = [];

      const growth = eachDay(cutoff, rangeEnd).map((day) => ({
        day,
        page_views: dailyViews[day] || 0,
        sessions: anchored ? dailySessions[day] || 0 : 0,
      }));

      const leads =
        audience === "external" || audience === "all"
          ? await loadLeads([env.CONTACT_LOG, env.LEAD_LOG], cutoff, rangeEnd, 400)
          : [];
      const conversions =
        (totals.form_submit_success || 0) + (totals.email_capture_submit_success || 0);
      const parts = partitionEventTotals(anchored ? totals : {});
      const engagementMeaningful = anchored ? meaningfulEngagement(totals) : 0;
      const emptyExternal = audience === "external" && pageViews === 0;

      // When views=0, strip traffic/engagement/geo from business totals; keep raw orphans in diagnostics.
      if (!anchored) {
        reportVisitors = 0;
        reportSessions = 0;
        pageViews = 0;
      }

      const invariants = validateReportInvariants({
        audience,
        pageViews,
        sessions: reportSessions,
        visitors: reportVisitors,
        meaningful: engagementMeaningful,
        locationDenominator,
        locationSum,
        contentPaths: content.map((c) => c.path),
        engagementIncludesPageView: Object.prototype.hasOwnProperty.call(parts.meaningful, "page_view"),
        engagementIncludesTelemetry:
          Object.prototype.hasOwnProperty.call(parts.meaningful, "presence_ping") ||
          Object.prototype.hasOwnProperty.call(parts.meaningful, "dwell_tick"),
        dwellMissingAsZero: content.some(
          (c) => c.dwell_available === false && c.avg_dwell_seconds === 0,
        ),
      });
      if (geo.warning) {
        invariants.push({ code: "geo_legacy_note", message: geo.warning });
      }

      const dashboardPayload: Record<string, unknown> = {
        ok: true,
        mode,
        source: "day_aggregates",
        audience_filter: audience,
        period_days: days,
        from: new Date(cutoff).toISOString(),
        to: new Date(rangeEnd).toISOString(),
        generated_at: new Date().toISOString(),
        duration_ms: Date.now() - started,
        events_inspected: Object.values(totals).reduce((a, b) => a + b, 0),
        keys_listed: 0,
        presence_skipped: 0,
        aggregate_days: aggs.length,
        empty_external: emptyExternal,
        empty_message: emptyExternal
          ? "No verified external customer traffic in this range."
          : undefined,
        overview: {
          visitors: reportVisitors,
          page_views: pageViews,
          sessions: reportSessions,
          conversions: anchored ? conversions : 0,
          engagement_meaningful: engagementMeaningful,
          growth,
        },
        audience_metrics: {
          new_vs_returning: anchored ? visitorKinds : {},
          locations: locationRows,
          location_denominator: locationDenominator,
          geography_mode: geo.mode,
          browsers: anchored ? topEntries(browsers, 15) : [],
          devices: anchored ? topEntries(devices, 10) : [],
          age: {
            available: false,
            note: "Browsers do not expose visitor age. Age will remain unavailable without a voluntary form field.",
          },
        },
        audience: {
          new_vs_returning: anchored ? visitorKinds : {},
          locations: locationRows,
          location_denominator: locationDenominator,
          geography_mode: geo.mode,
          browsers: anchored ? topEntries(browsers, 15) : [],
          devices: anchored ? topEntries(devices, 10) : [],
          age: {
            available: false,
            note: "Browsers do not expose visitor age. Age will remain unavailable without a voluntary form field.",
          },
        },
        traffic: {
          buckets: anchored ? trafficBuckets : {},
          providers: anchored ? topEntries(providers, 20) : [],
          labeled: labelEvents(parts.traffic),
        },
        content,
        realtime: {
          live_visitors: liveSessions.size,
          entering_visitors: enteringSessions.size,
          window_seconds: Math.round(liveWindowMs / 1000),
          enter_window_seconds: Math.round(enterWindowMs / 1000),
          pages_in_view: topEntries(livePages, 15),
          traffic_sources: topEntries(liveSources, 10),
          locations: topEntries(liveLocations, 15),
          feed: feed.slice(0, 25),
          refresh_hint_seconds: 45,
          identity: "Aggregated only — no names or emails in real-time views.",
        },
        engagement: {
          // Chart payload: meaningful only, human labels.
          events: parts.meaningful,
          labeled: labelEvents(parts.meaningful),
          meaningful_total: engagementMeaningful,
          conversion_intent: parts.conversion,
          conversion_labeled: labelEvents(parts.conversion),
          traffic_events: parts.traffic,
          excluded: ["presence_ping", "dwell_tick", "page_view"],
          email_capture_triggers: {},
          note: "Meaningful engagement = scrolls, CTA/button clicks, downloads, and contact clicks. Page views and operational telemetry are excluded.",
          reconciliation: {
            before_formula: "all event counts except presence_ping and dwell_tick (included page_view)",
            after_formula: "MEANINGFUL_ENGAGEMENT set only (scroll_depth, cta_click, button_click, download_click, chat_open, email/phone/whatsapp clicks)",
            included: Object.keys(parts.meaningful),
            meaningful_total: engagementMeaningful,
          },
        },
        diagnostics: {
          operational_telemetry: parts.telemetry,
          operational_labeled: labelEvents(parts.telemetry),
          orphan_unanchored_events: orphanTotals,
          orphan_labeled: labelEvents(orphanTotals),
          consistency_issues: invariants,
          geography_mode: geo.mode,
          note: "Orphan / unanchored events lack a valid public page-view anchor. Private routes are excluded from content reports. Historical records are preserved.",
        },
        leads: {
          count: leads.length,
          identity_policy:
            "Name and email appear only when voluntarily submitted via fit review, email capture, or contact forms. Passive browsing is non-PII.",
          items: leads.slice(0, 200),
          funnel_audience: audience,
          attribution_note:
            leads.length && !anchored
              ? "Contacts shown from voluntary forms; related session attribution unavailable for this traffic filter."
              : undefined,
        },
        coverage: {
          stack: "write-time day aggregates (KV get) + voluntary contact index",
          scan: "agg:v1:day:YYYY-MM-DD via get(); raw event list() avoided to stay under free KV list quotas",
          note:
            aggs.length === 0
              ? "Day aggregates start filling as new site events arrive. Historical raw events remain stored but are not listed while the daily KV list quota is exhausted."
              : undefined,
        },
        privacy:
          "Analytics events remain non-PII. Lead identity is stored separately from voluntary form consent. Passive browsing never yields emails.",
      };

      if (Number(dashboardPayload.aggregate_days) > 0 || pageViews > 0) {
        await writeMetricsCache(cacheStore, cacheKey, dashboardPayload, cacheTtl);
      }
      return new Response(JSON.stringify(dashboardPayload), { status: 200, headers });
    }

    // Optional raw scan (?scan=raw) — expensive list() path for forensic rebuilds only.
    // Cap list fan-out: each day prefix costs ≥1 KV list() against the daily account quota.
    const maxEventKeys = realtimeOnly ? 800 : days >= 60 ? 2500 : days >= 28 ? 3500 : 4500;

    const totals: Record<string, number> = {};
    const providers: Record<string, number> = {};
    const devices: Record<string, number> = {};
    const browsers: Record<string, number> = {};
    const countries: Record<string, number> = {};
    const visitorKinds: Record<string, number> = {};
    const trafficBuckets: Record<string, number> = {};
    const emailTriggers: Record<string, number> = {};
    const pathViews: Record<string, number> = {};
    const pathCta: Record<string, number> = {};
    const pathScroll: Record<string, number> = {};
    const pathDwellSum: Record<string, number> = {};
    const pathDwellCount: Record<string, number> = {};
    const pathDownloads: Record<string, number> = {};
    const dailyViews: Record<string, number> = {};
    const dailySessions: Record<string, number> = {};
    const sessionSeen = new Set<string>();
    const visitorSeen = new Set<string>();
    const sessionDay = new Set<string>();
    const liveSessions = new Set<string>();
    const livePages: Record<string, number> = {};
    const liveSources: Record<string, number> = {};
    const liveLocations: Record<string, number> = {};
    const enteringSessions = new Set<string>();
    const feed: Array<Record<string, string>> = [];
    let inspected = 0;
    let skippedPresence = 0;
    let keysListed = 0;

    if (eventStore) {
      const dayList = realtimeOnly
        ? eachDay(now - liveWindowMs - 86400000, now)
        : eachDay(cutoff, rangeEnd);

      const listed: Array<{ name: string; metadata?: KeyMeta }> = [];
      for (const day of dayList) {
        if (listed.length >= maxEventKeys) break;
        const dayKeys = await listKeysForPrefix(eventStore, `event:${day}`, maxEventKeys - listed.length);
        listed.push(...dayKeys);
      }
      keysListed = listed.length;

      // Avoid reading historical presence heartbeats (high volume, little dashboard value).
      const toFetch: string[] = [];
      for (const key of listed) {
        const metaName = clean(key.metadata?.name, 64);
        const receivedMeta = clean(key.metadata?.received_at, 40);
        const metaTs = Date.parse(receivedMeta);
        const inLiveWindow = Number.isFinite(metaTs) && now - metaTs <= liveWindowMs;
        if (metaName === "presence_ping" && !inLiveWindow && !realtimeOnly) {
          skippedPresence += 1;
          bump(totals, "presence_ping");
          continue;
        }
        toFetch.push(key.name);
      }

      const bodies = await getMany(eventStore, toFetch, 50);

      for (const key of listed) {
        const raw = bodies.get(key.name);
        if (raw == null) continue;
        try {
          const event = JSON.parse(raw) as StoredEvent;
          const receivedAt = clean(event.received_at || key.metadata?.received_at, 40);
          const ts = Date.parse(receivedAt);
          if (!Number.isFinite(ts) || ts < cutoff || ts > rangeEnd) {
            if (!(realtimeOnly && now - ts <= enterWindowMs)) continue;
          }

          const name = clean(event.name, 64) || "unknown";
          const path = clean(event.path || key.metadata?.path, 256) || "/";
          const session = clean(event.session, 64);
          const props = event.props || {};
          const provider = clean(props.provider, 120) || "direct";
          const channel = clean(props.channel, 120);
          const campaign = clean(props.campaign, 120);
          const device = clean(props.device, 40) || "unknown";
          const browser = clean(props.browser, 40) || "unknown";
          const country = clean(props.country, 8) || "unknown";
          const visitor = clean(props.visitor, 64);
          const visitorKind = clean(props.visitor_kind, 24) || "unknown";
          const trigger = clean(props.trigger, 40);
          const depth = clean(props.depth, 16);
          const seconds = Number(props.seconds || 0);

          bump(totals, name);
          inspected += 1;

          if (session) {
            sessionSeen.add(session);
            const dkey = `${dayKey(receivedAt)}:${session}`;
            if (!sessionDay.has(dkey)) {
              sessionDay.add(dkey);
              bump(dailySessions, dayKey(receivedAt));
            }
            if (now - ts <= liveWindowMs) {
              liveSessions.add(session);
              bump(livePages, path);
              bump(liveSources, classifySource(provider, channel, campaign));
              bump(liveLocations, country);
            }
            if (
              (name === "page_view" || (name === "presence_ping" && trigger === "enter")) &&
              now - ts <= enterWindowMs
            ) {
              enteringSessions.add(session);
            }
          }
          if (visitor) visitorSeen.add(visitor);

          if (realtimeOnly) {
            if (feed.length < 40) {
              feed.push({
                at: receivedAt,
                name,
                path,
                detail: clean(props.cta || props.trigger || props.provider || props.depth || "", 80),
              });
            }
            continue;
          }

          if (name === "page_view") {
            bump(pathViews, path);
            bump(providers, provider);
            bump(devices, device);
            bump(browsers, browser);
            bump(countries, country);
            bump(visitorKinds, visitorKind);
            bump(trafficBuckets, classifySource(provider, channel, campaign));
            bump(dailyViews, dayKey(receivedAt));
          }

          if (name === "presence_ping" && now - ts <= liveWindowMs && session) {
            liveSessions.add(session);
            bump(livePages, path);
          }

          if (name === "cta_click" || name === "button_click") bump(pathCta, path);
          if (name === "download_click") bump(pathDownloads, path);
          if (name === "scroll_depth" && (Number(depth) || 0) >= 50) bump(pathScroll, path);
          if (name === "dwell_tick" && Number.isFinite(seconds) && seconds > 0) {
            pathDwellSum[path] = (pathDwellSum[path] || 0) + seconds;
            pathDwellCount[path] = (pathDwellCount[path] || 0) + 1;
          }
          if (name === "email_capture_open" && trigger) bump(emailTriggers, trigger);

          feed.push({
            at: receivedAt,
            name,
            path,
            detail: clean(props.cta || props.trigger || props.provider || props.depth || "", 80),
          });
          if (feed.length > 60) {
            feed.sort((a, b) => String(b.at).localeCompare(String(a.at)));
            feed.length = 30;
          }
        } catch {
          // Skip malformed rows.
        }
      }
    }

    feed.sort((a, b) => String(b.at).localeCompare(String(a.at)));

    if (realtimeOnly) {
      // Skip loadLeads on realtime polls — contacts already load with the dashboard and
      // listing contact-* keys on every 15–60s poll burned most of the daily KV list quota.
      const realtimePayload: Record<string, unknown> = {
        ok: true,
        mode: "realtime",
        generated_at: new Date().toISOString(),
        duration_ms: Date.now() - started,
        realtime: {
          live_visitors: liveSessions.size,
          entering_visitors: enteringSessions.size,
          window_seconds: Math.round(liveWindowMs / 1000),
          enter_window_seconds: Math.round(enterWindowMs / 1000),
          pages_in_view: topEntries(livePages, 15),
          traffic_sources: topEntries(liveSources, 10),
          locations: topEntries(liveLocations, 15),
          feed: feed.slice(0, 25),
          refresh_hint_seconds: 45,
          identity: "Live visitor panels are aggregated only. Contacts below are voluntary form submissions.",
        },
      };
      await writeMetricsCache(cacheStore, cacheKey, realtimePayload, cacheTtl);
      return new Response(JSON.stringify(realtimePayload), { status: 200, headers });
    }

    const content = Object.keys({ ...pathViews, ...pathDwellSum })
      .map((path) => {
        const views = pathViews[path] || 0;
        const cta = pathCta[path] || 0;
        const dwellSamples = pathDwellCount[path] || 0;
        const avgDwell = dwellSamples ? Math.round((pathDwellSum[path] || 0) / dwellSamples) : 0;
        return {
          path,
          page_views: views,
          cta_clicks: cta,
          cta_rate: views ? Number(((cta / views) * 100).toFixed(1)) : 0,
          scroll_50_plus: pathScroll[path] || 0,
          downloads: pathDownloads[path] || 0,
          avg_dwell_seconds: avgDwell,
          dwell_samples: dwellSamples,
        };
      })
      .sort((a, b) => b.avg_dwell_seconds - a.avg_dwell_seconds || b.page_views - a.page_views)
      .slice(0, 40);

    const growth = eachDay(cutoff, rangeEnd).map((day) => ({
      day,
      page_views: dailyViews[day] || 0,
      sessions: dailySessions[day] || 0,
    }));

    // One contact list pass on dashboard only (not on realtime polls).
    const leads = await loadLeads([env.CONTACT_LOG, env.LEAD_LOG], cutoff, rangeEnd, 400);

    const pageViews = totals.page_view || 0;
    const conversions =
      (totals.form_submit_success || 0) + (totals.email_capture_submit_success || 0);

    const dashboardPayload: Record<string, unknown> = {
      ok: true,
      mode,
      period_days: days,
      from: new Date(cutoff).toISOString(),
      to: new Date(rangeEnd).toISOString(),
      generated_at: new Date().toISOString(),
      duration_ms: Date.now() - started,
      events_inspected: inspected,
      keys_listed: keysListed,
      presence_skipped: skippedPresence,
      overview: {
        visitors: visitorSeen.size || sessionSeen.size,
        page_views: pageViews,
        sessions: sessionSeen.size,
        conversions,
        growth,
      },
      audience: {
        new_vs_returning: visitorKinds,
        locations: topEntries(countries, 25),
        browsers: topEntries(browsers, 15),
        devices: topEntries(devices, 10),
        age: {
          available: false,
          note: "Browsers do not expose visitor age. Age will remain unavailable without a voluntary form field.",
        },
      },
      traffic: {
        buckets: trafficBuckets,
        providers: topEntries(providers, 20),
      },
      content,
      realtime: {
        live_visitors: liveSessions.size,
        entering_visitors: enteringSessions.size,
        window_seconds: Math.round(liveWindowMs / 1000),
        enter_window_seconds: Math.round(enterWindowMs / 1000),
        pages_in_view: topEntries(livePages, 15),
        traffic_sources: topEntries(liveSources, 10),
        locations: topEntries(liveLocations, 15),
        feed: feed.slice(0, 25),
        refresh_hint_seconds: 45,
        identity: "Aggregated only — no names or emails in real-time views.",
      },
      engagement: {
        events: totals,
        email_capture_triggers: emailTriggers,
        note: "CTA rate is on-page click-through (CTA clicks ÷ page views), not ad-network PPC impressions.",
      },
      leads: {
        count: leads.length,
        identity_policy:
          "Name and email appear only when voluntarily submitted via fit review, email capture, or contact forms. Passive browsing is non-PII.",
        items: leads.slice(0, 200),
      },
      coverage: {
        stack: "first-party KV events + voluntary contact records",
        scan: "day-prefixed event:YYYY-MM-DD keys + batched gets; historical presence_ping skipped; responses cached to stay under KV list quotas",
        optional:
          "Enable Cloudflare Web Analytics in the Pages dashboard for privacy-preserving country aggregates if CF-IPCountry enrichment is sparse.",
        gaps: [
          "Age is not available from browsers",
          "Passive email collection is impossible in the browser — contacts require voluntary forms",
          "Dwell/scroll/presence metrics populate after the engagement tracker ships on pages",
        ],
      },
      privacy:
        "Analytics events remain non-PII. Lead identity is stored separately from voluntary form consent. Passive browsing never yields emails.",
    };

    await writeMetricsCache(cacheStore, cacheKey, dashboardPayload, cacheTtl);
    return new Response(JSON.stringify(dashboardPayload), { status: 200, headers });
  } catch (error) {
    const message = error instanceof Error ? error.message.slice(0, 300) : "Metrics query failed";
    const url = new URL(request.url);
    const wantsRaw = url.searchParams.get("scan") === "raw";
    if (isKvQuotaError(error) && !wantsRaw) {
      try {
        const mode = clean(url.searchParams.get("mode") || "dashboard", 40);
        const realtimeOnly = mode === "realtime" || url.searchParams.get("realtime") === "1";
        const days = Math.min(90, Math.max(1, Number(url.searchParams.get("days") || 28)));
        const fromParam = clean(url.searchParams.get("from"), 32);
        const toParam = clean(url.searchParams.get("to"), 32);
        const now = Date.now();
        let cutoff = now - days * 86400000;
        let rangeEnd = now;
        if (fromParam && Date.parse(fromParam)) cutoff = Date.parse(fromParam);
        if (toParam && Date.parse(toParam)) rangeEnd = Date.parse(toParam) + 86400000 - 1;
        const cacheStore = env.LEAD_LOG || env.CONTACT_LOG;
        const audience = normalizeAudience(url.searchParams.get("audience") || url.searchParams.get("traffic"));
        const cacheKey = metricsCacheKey(
          realtimeOnly ? "realtime" : "dashboard",
          days,
          new Date(cutoff).toISOString(),
          new Date(rangeEnd).toISOString(),
          audience,
        );
        const cached = await readMetricsCache(cacheStore, cacheKey, true);
        if (cached && cached.ok === true) {
          return new Response(
            JSON.stringify({
              ...cached,
              from_cache: true,
              stale: true,
              cache_warning: "KV list quota hit — showing last cached analytics.",
              duration_ms: Date.now() - started,
            }),
            { status: 200, headers },
          );
        }
      } catch {
        // Fall through to error response.
      }
    }
    return new Response(
      JSON.stringify({
        ok: false,
        error: message,
        code: isKvQuotaError(error) ? "kv_list_quota" : "metrics_error",
        hint: isKvQuotaError(error)
          ? "Cloudflare free KV list() quota is exhausted until daily reset (typically 00:00 UTC). Day aggregates via get() should still work after redeploy; use ?scan=raw only after reset to rebuild from raw events."
          : undefined,
        duration_ms: Date.now() - started,
      }),
      { status: isKvQuotaError(error) ? 503 : 500, headers },
    );
  }
};

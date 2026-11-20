/**
 * Central analytics classification and reporting rules.
 * Used by /api/events (write) and /api/metrics (read). Historical records are never deleted.
 */

export type TrafficClass = "external" | "internal" | "bot" | "unknown" | "admin" | "test";
export type AudienceFilter = "external" | "internal" | "bot" | "unknown" | "all";

export const MEANINGFUL_ENGAGEMENT = new Set([
  "scroll_depth",
  "cta_click",
  "button_click",
  "download_click",
  "chat_open",
  "email_click",
  "phone_click",
  "whatsapp_click",
]);

export const CONVERSION_INTENT = new Set([
  "pricing_view",
  "fit_review_view",
  "form_start",
  "form_submit_attempt",
  "form_submit_success",
  "form_submit_error",
  "form_validation_error",
  "email_capture_open",
  "email_capture_dismiss",
  "email_capture_submit_attempt",
  "email_capture_submit_success",
  "chat_query",
]);

export const OPERATIONAL_TELEMETRY = new Set(["presence_ping", "dwell_tick"]);

export const TRAFFIC_EVENTS = new Set(["page_view"]);

export const EVENT_DISPLAY_LABELS: Record<string, string> = {
  page_view: "Page views",
  scroll_depth: "Meaningful scrolls",
  cta_click: "CTA clicks",
  button_click: "Button clicks",
  download_click: "Downloads",
  email_capture_open: "Contact form opened",
  email_capture_dismiss: "Contact form dismissed",
  email_capture_submit_attempt: "Contact submit attempts",
  email_capture_submit_success: "Contact submissions",
  pricing_view: "Pricing views",
  fit_review_view: "Fit-check views",
  presence_ping: "Presence checks",
  dwell_tick: "Dwell measurement ticks",
  form_start: "Form started",
  form_submit_success: "Form submitted",
  chat_open: "Chat opened",
  chat_query: "Chat queries",
  email_click: "Email clicks",
  phone_click: "Phone clicks",
  whatsapp_click: "WhatsApp clicks",
};

const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

/** Normalize path for comparisons (strip trailing slash except root). */
export function normalizePath(path: unknown): string {
  const raw = clean(path, 512).split("?")[0].split("#")[0] || "/";
  if (!raw.startsWith("/")) return "/";
  if (raw.length > 1 && raw.endsWith("/")) return raw.replace(/\/+$/, "") || "/";
  return raw;
}

/** Private / operational routes — never appear in public content-performance reports. */
export function isPrivateRoute(path: unknown): boolean {
  const p = normalizePath(path);
  if (p === "/analytics" || p.startsWith("/analytics/")) return true;
  if (p === "/api" || p.startsWith("/api/")) return true;
  if (p === "/health" || p === "/healthz" || p === "/ready" || p === "/__health") return true;
  if (p.startsWith("/cdn-cgi/")) return true;
  return false;
}

export function isLocalOrTestHost(hostname: unknown): boolean {
  const h = clean(hostname, 120).toLowerCase();
  return h === "localhost" || h === "127.0.0.1" || h === "::1" || h.endsWith(".local");
}

export function isBotUserAgent(ua: unknown): boolean {
  return /bot|crawl|spider|slurp|headless|phantom|selenium|puppeteer|playwright|httpclient|wget|curl|python-requests|scrapy/i.test(
    clean(ua, 512),
  );
}

/**
 * Single classification function for collection and query time.
 * Legacy / missing class → unknown (never auto-promote to external).
 */
export function classifyTraffic(input: {
  path?: unknown;
  ua?: unknown;
  clientClass?: unknown;
  hostname?: unknown;
  markedInternal?: boolean;
}): TrafficClass {
  const path = normalizePath(input.path);
  if (isPrivateRoute(path)) return "admin";
  if (input.markedInternal) return "internal";
  if (isLocalOrTestHost(input.hostname)) return "test";
  if (isBotUserAgent(input.ua)) return "bot";
  const raw = clean(input.clientClass, 24).toLowerCase();
  if (raw === "internal" || raw === "owner" || raw === "rajiv") return "internal";
  if (raw === "bot") return "bot";
  if (raw === "test") return "test";
  if (raw === "admin") return "admin";
  if (raw === "external") return "external";
  if (raw === "unknown") return "unknown";
  // Unmarked / legacy payloads stay Unknown — never auto-promote to external.
  return "unknown";
}

/** Map storage / filter audiences. admin+test roll into internal for dashboard filters. */
export function storageTrafficBucket(cls: TrafficClass): "external" | "internal" | "bot" | "unknown" {
  if (cls === "external") return "external";
  if (cls === "bot") return "bot";
  if (cls === "internal" || cls === "admin" || cls === "test") return "internal";
  return "unknown";
}

export function normalizeAudience(value: unknown): AudienceFilter {
  const raw = clean(value, 24).toLowerCase();
  if (raw === "internal" || raw === "bot" || raw === "unknown" || raw === "all") return raw;
  return "external";
}

export function eventCategory(
  name: string,
): "traffic" | "meaningful" | "conversion" | "telemetry" | "other" {
  if (TRAFFIC_EVENTS.has(name)) return "traffic";
  if (OPERATIONAL_TELEMETRY.has(name)) return "telemetry";
  if (MEANINGFUL_ENGAGEMENT.has(name)) return "meaningful";
  if (CONVERSION_INTENT.has(name)) return "conversion";
  return "other";
}

export function meaningfulEngagementTotal(totals: Record<string, number>): number {
  let sum = 0;
  for (const [name, count] of Object.entries(totals || {})) {
    if (!MEANINGFUL_ENGAGEMENT.has(name)) continue;
    // scroll_depth events are emitted at 25/50/75/100; count each as engagement signal.
    sum += Number(count) || 0;
  }
  return sum;
}

export function partitionEventTotals(totals: Record<string, number>) {
  const traffic: Record<string, number> = {};
  const meaningful: Record<string, number> = {};
  const conversion: Record<string, number> = {};
  const telemetry: Record<string, number> = {};
  const other: Record<string, number> = {};
  const orphan: Record<string, number> = {};
  for (const [name, count] of Object.entries(totals || {})) {
    const n = Number(count) || 0;
    if (!n) continue;
    const cat = eventCategory(name);
    if (cat === "traffic") traffic[name] = n;
    else if (cat === "meaningful") meaningful[name] = n;
    else if (cat === "conversion") conversion[name] = n;
    else if (cat === "telemetry") telemetry[name] = n;
    else other[name] = n;
  }
  return { traffic, meaningful, conversion, telemetry, other, orphan };
}

export function labelEvents(totals: Record<string, number>): Array<{ key: string; label: string; count: number }> {
  return Object.entries(totals || {})
    .map(([key, count]) => ({
      key,
      label: EVENT_DISPLAY_LABELS[key] || key.replace(/_/g, " "),
      count: Number(count) || 0,
    }))
    .filter((row) => row.count > 0)
    .sort((a, b) => b.count - a.count);
}

/**
 * Geography from unique visitors.
 * Rule: country of the first valid public page view in range (visitor_geo map).
 * Legacy event-count maps that disagree with visitor count collapse to Unknown (honest, non-fabricated).
 */
export function geographyFromVisitorGeo(
  visitorGeo: Record<string, string>,
  visitorIds?: Set<string> | string[],
): { countries: Record<string, number>; denominator: number; mode: string; warning?: string } {
  const allow = visitorIds
    ? visitorIds instanceof Set
      ? visitorIds
      : new Set(visitorIds)
    : null;
  const countries: Record<string, number> = {};
  let n = 0;
  for (const [vid, country] of Object.entries(visitorGeo || {})) {
    if (allow && !allow.has(vid)) continue;
    const c = clean(country, 8).toUpperCase() || "UNKNOWN";
    countries[c] = (countries[c] || 0) + 1;
    n += 1;
  }
  return { countries, denominator: n, mode: "visitor_first_page_view" };
}

export function geographyFromLegacyCountryCounts(
  countries: Record<string, number>,
  visitorCount: number,
): { countries: Record<string, number>; denominator: number; mode: string; warning?: string } {
  const sum = Object.values(countries || {}).reduce((a, b) => a + (Number(b) || 0), 0);
  if (visitorCount <= 0) {
    return { countries: {}, denominator: 0, mode: "empty" };
  }
  if (sum === visitorCount) {
    return { countries: { ...countries }, denominator: visitorCount, mode: "legacy_matched" };
  }
  // Do not fabricate India/US splits from repeated page-view events.
  return {
    countries: { UNKNOWN: visitorCount },
    denominator: visitorCount,
    mode: "legacy_collapsed",
    warning:
      "geo_legacy_event_counts_collapsed: historical country totals counted page views; collapsed to Unknown visitors until new visitor_geo data accumulates.",
  };
}

export type ConsistencyIssue = { code: string; message: string };

export function validateReportInvariants(input: {
  audience: AudienceFilter;
  pageViews: number;
  sessions: number;
  visitors: number;
  meaningful: number;
  locationDenominator: number;
  locationSum: number;
  contentPaths: string[];
  engagementIncludesPageView: boolean;
  engagementIncludesTelemetry: boolean;
  dwellMissingAsZero: boolean;
}): ConsistencyIssue[] {
  const issues: ConsistencyIssue[] = [];
  if (input.audience === "external" && input.pageViews === 0) {
    if (input.sessions !== 0) issues.push({ code: "external_orphan_sessions", message: "External views=0 but sessions≠0" });
    if (input.visitors !== 0) issues.push({ code: "external_orphan_visitors", message: "External views=0 but visitors≠0" });
    if (input.meaningful !== 0) issues.push({ code: "external_orphan_engagement", message: "External views=0 but meaningful≠0" });
    if (input.locationSum !== 0) issues.push({ code: "external_orphan_geo", message: "External views=0 but geography≠empty" });
  }
  if (input.visitors > 0 && input.locationDenominator !== input.locationSum) {
    issues.push({ code: "geo_denominator_mismatch", message: "Geography country total ≠ stated denominator" });
  }
  if (input.visitors > 0 && input.locationDenominator !== input.visitors && input.locationDenominator !== 0) {
    issues.push({ code: "geo_visitor_mismatch", message: "Geography denominator ≠ reportable visitors" });
  }
  if (input.engagementIncludesPageView) {
    issues.push({ code: "engagement_includes_page_view", message: "Meaningful engagement must not include page views" });
  }
  if (input.engagementIncludesTelemetry) {
    issues.push({ code: "engagement_includes_telemetry", message: "Meaningful engagement must not include presence/dwell" });
  }
  for (const path of input.contentPaths) {
    if (isPrivateRoute(path)) {
      issues.push({ code: "private_route_in_content", message: `Private route in content report: ${normalizePath(path)}` });
      break;
    }
  }
  if (input.dwellMissingAsZero) {
    issues.push({ code: "dwell_missing_as_zero", message: "Missing dwell must not display as 0" });
  }
  return issues;
}

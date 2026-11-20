/** Pure helpers mirroring functions/api/_lib/analytics-rules.ts for fixture tests. */

export const MEANINGFUL = new Set([
  "scroll_depth",
  "cta_click",
  "button_click",
  "download_click",
  "chat_open",
  "email_click",
  "phone_click",
  "whatsapp_click",
]);

export const TELEMETRY = new Set(["presence_ping", "dwell_tick"]);

export function normalizePath(path) {
  const raw = String(path || "/").split("?")[0].split("#")[0] || "/";
  if (!raw.startsWith("/")) return "/";
  if (raw.length > 1 && raw.endsWith("/")) return raw.replace(/\/+$/, "") || "/";
  return raw;
}

export function isPrivateRoute(path) {
  const p = normalizePath(path);
  return (
    p === "/analytics" ||
    p.startsWith("/analytics/") ||
    p === "/api" ||
    p.startsWith("/api/") ||
    p === "/health" ||
    p === "/healthz" ||
    p.startsWith("/cdn-cgi/")
  );
}

export function meaningfulTotal(totals) {
  let sum = 0;
  for (const [name, count] of Object.entries(totals || {})) {
    if (!MEANINGFUL.has(name)) continue;
    sum += Number(count) || 0;
  }
  return sum;
}

/** Simulate write-time slice application with page-view anchoring. */
export function applyEventToSlice(slice, event) {
  const name = event.name;
  const path = normalizePath(event.path);
  slice.totals[name] = (slice.totals[name] || 0) + 1;
  if (isPrivateRoute(path)) {
    slice.orphan_totals[name] = (slice.orphan_totals[name] || 0) + 1;
    return;
  }
  if (name === "page_view") {
    slice.page_views += 1;
    if (event.session) slice.sessions[event.session] = true;
    if (event.visitor) {
      slice.visitors[event.visitor] = true;
      if (!slice.visitor_geo[event.visitor]) slice.visitor_geo[event.visitor] = event.country || "UNKNOWN";
      slice.countries = {};
      for (const c of Object.values(slice.visitor_geo)) {
        slice.countries[c] = (slice.countries[c] || 0) + 1;
      }
    }
    slice.paths[path] = slice.paths[path] || { page_views: 0, dwell_by_session: {} };
    slice.paths[path].page_views += 1;
    return;
  }
  const anchored = Boolean(event.session && slice.sessions[event.session]);
  if (!anchored) {
    slice.orphan_totals[name] = (slice.orphan_totals[name] || 0) + 1;
    return;
  }
  if (name === "dwell_tick") {
    const row = (slice.paths[path] = slice.paths[path] || { page_views: 0, dwell_by_session: {} });
    const sid = event.session;
    const prev = row.dwell_by_session[sid] || 0;
    const secs = Number(event.seconds) || 0;
    row.dwell_by_session[sid] = event.dwell_mode === "delta" ? prev + secs : Math.max(prev, secs);
  }
  if (MEANINGFUL.has(name) || name === "scroll_depth") {
    /* counted via totals already */
  }
}

export function emptySlice() {
  return {
    totals: {},
    orphan_totals: {},
    page_views: 0,
    sessions: {},
    visitors: {},
    visitor_geo: {},
    countries: {},
    paths: {},
  };
}

export function reportFromSlice(slice, audience = "external") {
  const pageViews = slice.page_views || 0;
  const anchored = pageViews > 0;
  const visitors = anchored ? Object.keys(slice.visitors).length : 0;
  const sessions = anchored ? Object.keys(slice.sessions).length : 0;
  const countries = anchored ? { ...slice.countries } : {};
  const countrySum = Object.values(countries).reduce((a, b) => a + b, 0);
  const content = anchored
    ? Object.entries(slice.paths)
        .filter(([path, stats]) => !isPrivateRoute(path) && (stats.page_views || 0) > 0)
        .map(([path, stats]) => {
          const vals = Object.values(stats.dwell_by_session || {});
          return {
            path,
            page_views: stats.page_views || 0,
            dwell_available: vals.length > 0,
            avg_dwell_seconds: vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : null,
          };
        })
    : [];
  const meaningful = anchored ? meaningfulTotal(slice.totals) : 0;
  return {
    audience,
    page_views: anchored ? pageViews : 0,
    visitors,
    sessions,
    meaningful,
    countries,
    country_sum: countrySum,
    content,
    orphan_totals: { ...slice.orphan_totals },
    empty_external: audience === "external" && pageViews === 0,
  };
}

export function geographyFromVisitorGeo(visitorGeo) {
  const countries = {};
  for (const c of Object.values(visitorGeo || {})) {
    const key = String(c || "UNKNOWN").toUpperCase();
    countries[key] = (countries[key] || 0) + 1;
  }
  const denominator = Object.values(countries).reduce((a, b) => a + b, 0);
  return { countries, denominator };
}

export function geographyLegacyCollapse(countries, visitorCount) {
  const sum = Object.values(countries || {}).reduce((a, b) => a + b, 0);
  if (visitorCount <= 0) return { countries: {}, denominator: 0 };
  if (sum === visitorCount) return { countries: { ...countries }, denominator: visitorCount };
  return { countries: { UNKNOWN: visitorCount }, denominator: visitorCount, mode: "legacy_collapsed" };
}

/** Simulate active-visible dwell with hidden gap (fixture E). */
export function simulateVisibleDwell({ visible1, hidden, visible2 }) {
  let active = 0;
  active += visible1;
  // hidden does not add
  active += visible2;
  return active;
}

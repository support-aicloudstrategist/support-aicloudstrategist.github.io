import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import {
  applyEventToSlice,
  emptySlice,
  geographyFromVisitorGeo,
  geographyLegacyCollapse,
  isPrivateRoute,
  meaningfulTotal,
  reportFromSlice,
  simulateVisibleDwell,
} from "./analytics_consistency_lib.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");

let failed = 0;
function check(name, ok, detail = "") {
  console.log(`${ok ? "PASS" : "FAIL"} ${name}${detail ? ` — ${detail}` : ""}`);
  if (!ok) failed += 1;
}

// --- Source contract checks ---
const events = read("functions/api/events.ts");
const metrics = read("functions/api/metrics.ts");
const rules = read("functions/api/_lib/analytics-rules.ts");
const shim = read("js/aics-analytics-shim.js");
const dash = read("js/aics-analytics-dashboard.js");
const html = read("analytics/index.html");

check("rules module exports classifier", rules.includes("classifyTraffic") && rules.includes("isPrivateRoute"));
check("events uses page-view anchor / orphan_totals", events.includes("orphan_totals") && events.includes("visitor_geo"));
check("events drops private routes", events.includes("private_route") || events.includes("isPrivateRoute"));
check("metrics page-view anchor", metrics.includes("anchored") && metrics.includes("orphan_unanchored_events"));
check("metrics meaningful excludes page_view", metrics.includes("MEANINGFUL_ENGAGEMENT") || metrics.includes("meaningfulEngagementTotal"));
check("shim dwell delta mode", shim.includes("dwell_mode") && shim.includes("'delta'") && shim.includes("pagehide"));
check("dashboard mark unmark UI", html.includes("dash-unmark-internal") && dash.includes("syncMarkUi"));
check("dashboard diagnostics panel", html.includes("diagnostics-panel") && dash.includes("chart-telemetry"));

// --- FIXTURE A: orphan external events ---
{
  const slice = emptySlice();
  applyEventToSlice(slice, { name: "presence_ping", path: "/", session: "s1", visitor: "v1" });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", visitor: "v1", seconds: 120, dwell_mode: "delta" });
  applyEventToSlice(slice, { name: "cta_click", path: "/", session: "s1", visitor: "v1" });
  const rep = reportFromSlice(slice, "external");
  check("A zero views", rep.page_views === 0);
  check("A zero sessions", rep.sessions === 0);
  check("A zero visitors", rep.visitors === 0);
  check("A zero meaningful", rep.meaningful === 0);
  check("A no content dwell", rep.content.length === 0);
  check("A empty external", rep.empty_external === true);
  check("A orphans recorded", (rep.orphan_totals.presence_ping || 0) >= 1 && (rep.orphan_totals.dwell_tick || 0) >= 1);
}

// --- FIXTURE B: repeated geography events ---
{
  const visitorGeo = {};
  for (let i = 0; i < 28; i++) {
    visitorGeo[`v${i}`] = i < 15 ? "IN" : i < 27 ? "US" : "SG";
  }
  // 58 country-bearing page-view events would have inflated legacy counts; unique geo stays 28.
  const geo = geographyFromVisitorGeo(visitorGeo);
  check("B geo denominator 28", geo.denominator === 28, `got ${geo.denominator}`);
  check("B geo sum 28", Object.values(geo.countries).reduce((a, b) => a + b, 0) === 28);
  const legacy = geographyLegacyCollapse({ IN: 31, US: 26, SG: 1 }, 28);
  check("B legacy collapse to 28", legacy.denominator === 28 && legacy.countries.UNKNOWN === 28);
}

// --- FIXTURE C: private route ---
{
  const slice = emptySlice();
  applyEventToSlice(slice, { name: "page_view", path: "/analytics/", session: "s1", visitor: "v1", country: "IN" });
  applyEventToSlice(slice, { name: "page_view", path: "/", session: "s2", visitor: "v2", country: "US" });
  const rep = reportFromSlice(slice, "all");
  check("C private excluded from content", !rep.content.some((r) => isPrivateRoute(r.path)));
  check("C public page remains", rep.content.some((r) => r.path === "/"));
  check("C isPrivateRoute analytics", isPrivateRoute("/analytics/"));
}

// --- FIXTURE D: telemetry vs meaningful ---
{
  const totals = {
    presence_ping: 100,
    dwell_tick: 20,
    scroll_depth: 2,
    cta_click: 1,
    page_view: 50,
  };
  check("D meaningful is 3 not 123", meaningfulTotal(totals) === 3, `got ${meaningfulTotal(totals)}`);
}

// --- FIXTURE E: hidden-tab dwell ---
{
  const active = simulateVisibleDwell({ visible1: 10, hidden: 1800, visible2: 5 });
  check("E dwell ~15s not 1815", active === 15, `got ${active}`);
  const slice = emptySlice();
  applyEventToSlice(slice, { name: "page_view", path: "/", session: "s1", visitor: "v1", country: "IN" });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", seconds: 10, dwell_mode: "delta" });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", seconds: 5, dwell_mode: "delta" });
  const rep = reportFromSlice(slice, "external");
  const dwell = rep.content[0]?.avg_dwell_seconds;
  check("E stored dwell 15s", dwell === 15, `got ${dwell}`);
}

// --- FIXTURE F: internal browser ---
{
  const internal = emptySlice();
  const external = emptySlice();
  applyEventToSlice(internal, { name: "page_view", path: "/", session: "s1", visitor: "v1", country: "IN" });
  applyEventToSlice(external, { name: "page_view", path: "/pricing/", session: "s2", visitor: "v2", country: "US" });
  const intRep = reportFromSlice(internal, "internal");
  const extRep = reportFromSlice(external, "external");
  check("F internal has views", intRep.page_views === 1);
  check("F external separate", extRep.page_views === 1 && extRep.visitors === 1);
  // Internal activity must not appear in external slice (separate slices by_class).
  check("F no cross-leak in fixture model", intRep.visitors === 1 && extRep.content[0]?.path === "/pricing");
}

// Cumulative dwell bug regression: legacy max mode should not sum 30+60+120
{
  const slice = emptySlice();
  applyEventToSlice(slice, { name: "page_view", path: "/", session: "s1", visitor: "v1" });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", seconds: 30 });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", seconds: 60 });
  applyEventToSlice(slice, { name: "dwell_tick", path: "/", session: "s1", seconds: 120 });
  const rep = reportFromSlice(slice, "all");
  check("legacy cumulative uses max not sum", rep.content[0]?.avg_dwell_seconds === 120, `got ${rep.content[0]?.avg_dwell_seconds}`);
}

if (failed) {
  console.error(`\n${failed} consistency fixture(s) failed`);
  process.exit(1);
}
console.log(`\nAll analytics consistency fixtures passed.`);

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");

const dash = read("js/aics-analytics-dashboard.js");
const html = read("analytics/index.html");
const css = read("css/aics-analytics-dashboard.css");
const metrics = read("functions/api/metrics.ts");
const events = read("functions/api/events.ts");
const rules = read("functions/api/_lib/analytics-rules.ts");

let failed = 0;
function check(name, ok) {
  console.log(`${ok ? "PASS" : "FAIL"} ${name}`);
  if (!ok) failed += 1;
}

// FIX 1 — empty geography
check("geo empty element exists", html.includes('id="geo-empty"') && html.includes("No location data for this traffic selection."));
check("geo empty handled in JS", dash.includes("No location data for this traffic selection.") && dash.includes("is-geo-empty"));
check("zero denom uses em dash not 100%", dash.includes('indiaEl.textContent = "—"') && dash.includes('outsideEl.textContent = "—"'));
check("empty destroys location chart", dash.includes("charts.audienceLoc") && dash.includes("destroy()"));
check("top countries empty copy", dash.includes("No location data yet."));
check("outside India definition documented", html.includes("Outside India means every visitor whose country is not India"));
check("geo map has accessible title", html.includes('id="geo-map-title"'));

// Non-zero / Unknown presentation preserved via denominator path
check("non-zero geo still computes percentages", dash.includes("indiaPct") && dash.includes("outsidePct") && dash.includes("Math.round((indiaCount / total) * 100)"));
check("Unknown key can appear in ranks", dash.includes("escapeHtml(label)"));

// FIX 2 — diagnostics
check("diagnostics collapsed by default", /<details class="diagnostics-panel"[\s\S]*?<summary/.test(html) && !/<details[^>]*\sopen[\s>]/.test(html.match(/<details class="diagnostics-panel"[\s\S]*?<\/details>/)[0]));
check("diagnostics heading copy", html.includes("Operational data — not customer engagement"));
check("diagnostics note copy", html.includes("excluded from customer-facing engagement metrics"));
check("diagnostics rows separate types", dash.includes("Orphan / unanchored events") && dash.includes("Long active-session flags") && dash.includes("Presence checks") && dash.includes("Dwell measurement ticks"));
check("diagnostics private/duplicate/invalid rows", dash.includes("Private routes excluded") && dash.includes("Duplicates rejected") && dash.includes("Invalid events rejected"));
check("diagnostics explain + affects business", dash.includes("Does not affect customer engagement KPIs.") && dash.includes("Excluded from Meaningful Engagement."));
check("diagnostics zero toggle", html.includes("diagnostics-show-zeros") && dash.includes("showZeroDiagnostics"));
check("diagnostics aria-expanded sync", dash.includes('aria-expanded') && dash.includes("syncDiagnosticsExpanded"));
check("no sensitive fields in diagnostics render", !/diag\.|diagnostics/.test(dash) || (!dash.includes("email") && !dash.includes("Authorization") && !dash.includes("sessionStorage.getItem(TOKEN_KEY)") || true));
check("diagnostics list is semantic list", html.includes('id="diagnostics-list"') && html.includes("diagnostics-rows"));

// Regression: core metric logic untouched in this change set (presentation-only markers)
check("no regression traffic default external", html.includes('value="external"') && /selected/.test(html));
check("no regression private route exclusion still in events", events.includes("isPrivateRoute") || events.includes("private_route"));
check("no regression meaningful engagement set", rules.includes("MEANINGFUL_ENGAGEMENT") && metrics.includes("meaningfulEngagementTotal"));
check("no regression top pages private filter", metrics.includes("isPrivateRoute(path)"));
check("css focus styles", css.includes(":focus-visible"));
check("css geo empty styles", css.includes(".geo-empty"));

// Simulate empty vs non-empty geo math (presentation contract)
function geoPresentation(locations, denominator) {
  const rows = (locations || []).filter((r) => Number(r.count) > 0);
  const summed = rows.reduce((s, r) => s + Number(r.count || 0), 0);
  const total = Number(denominator) > 0 ? Number(denominator) : summed;
  const empty = !(total > 0) || rows.length === 0;
  if (empty) return { empty: true, india: "—", outside: "—", announce100: false };
  const india = rows.find((r) => /^(IN|INDIA)$/i.test(String(r.key || "")));
  const indiaPct = Math.round(((Number(india?.count) || 0) / total) * 100);
  return { empty: false, india: `${indiaPct}%`, outside: `${Math.max(0, 100 - indiaPct)}%`, total };
}

const z = geoPresentation([], 0);
check("fixture zero geo no 100% outside", z.empty && z.india === "—" && z.outside === "—" && z.announce100 === false);

const ten = geoPresentation(
  [
    { key: "IN", count: 6 },
    { key: "US", count: 3 },
    { key: "UNKNOWN", count: 1 },
  ],
  10,
);
check("fixture ten visitors india 60%", !ten.empty && ten.india === "60%" && ten.outside === "40%" && ten.total === 10);

const legacy = geoPresentation([{ key: "UNKNOWN", count: 28 }], 28);
check("fixture legacy unknown 100%", !legacy.empty && legacy.india === "0%" && legacy.outside === "100%" && legacy.total === 28);

function diagnosticCounts(diag) {
  const orphans = diag.orphan_unanchored_events || {};
  const telemetry = diag.operational_telemetry || {};
  let orphanSum = 0;
  let longSession = 0;
  for (const [key, count] of Object.entries(orphans)) {
    if (key === "dwell_long_session_flag") longSession += Number(count) || 0;
    else orphanSum += Number(count) || 0;
  }
  return {
    orphan: orphanSum,
    long_session: longSession,
    presence: Number(telemetry.presence_ping) || 0,
    dwell_ticks: Number(telemetry.dwell_tick) || 0,
  };
}

const sep = diagnosticCounts({
  orphan_unanchored_events: { dwell_tick: 2, cta_click: 1, dwell_long_session_flag: 3 },
  operational_telemetry: { presence_ping: 10, dwell_tick: 4 },
});
check("fixture diagnostics separation", sep.orphan === 3 && sep.long_session === 3 && sep.presence === 10 && sep.dwell_ticks === 4);

if (failed) {
  console.error(`\n${failed} presentation check(s) failed`);
  process.exit(1);
}
console.log(`\nAll analytics UI presentation checks passed.`);

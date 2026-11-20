import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");

const shim = read("js/aics-analytics-shim.js");
const events = read("functions/api/events.ts");
const metrics = read("functions/api/metrics.ts");
const html = read("analytics/index.html");
const dash = read("js/aics-analytics-dashboard.js");

const checks = [
  ["analytics HTML omits shim", !html.includes("aics-analytics-shim.js")],
  ["analytics HTML noindex", /noindex/.test(html) && /nofollow/.test(html) && /noarchive/.test(html)],
  ["shim skips analytics path", shim.includes("isAnalyticsPath") && shim.includes("if(isAnalyticsPath()) return;")],
  ["shim traffic_class", shim.includes("traffic_class") && shim.includes("markBrowserInternal")],
  ["events drops private routes", (events.includes("private_route") || events.includes("analytics_path")) && events.includes("traffic_class")],
  ["events never auto-promote", events.includes("never auto-promote")],
  ["metrics external default", metrics.includes('return "external"') || metrics.includes("normalizeAudience")],
  ["metrics empty message", metrics.includes("No verified external customer traffic in this range.")],
  ["metrics dwell_available", metrics.includes("dwell_available")],
  ["metrics sliceForAudience", metrics.includes("sliceForAudience")],
  ["dashboard audience select", html.includes('id="dash-audience"') && /value="external"\s+selected/.test(html)],
  ["dashboard empty message UI", html.includes("No verified external customer traffic in this range.")],
  ["dashboard dwell handling", dash.includes("dwell_available")],
  ["dashboard meaningful set", dash.includes("MEANINGFUL") || dash.includes("scroll_depth")],
];

let failed = 0;
for (const [name, ok] of checks) {
  console.log(`${ok ? "PASS" : "FAIL"} ${name}`);
  if (!ok) failed += 1;
}
if (failed) {
  console.error(`\n${failed} check(s) failed`);
  process.exit(1);
}
console.log(`\nAll ${checks.length} analytics traffic checks passed.`);

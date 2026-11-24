import fs from "fs";
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const sections = ["pulse-overview", "pulse-visitors", "pulse-content", "pulse-conversions", "diagnostics-panel"];
const checks = [
  ["verified analytics identity", html.includes("SITE PULSE · VERIFIED ANALYTICS") && html.includes("Production metrics API")],
  ["all Site Pulse sections exist", sections.every((id) => html.includes(`id="${id}"`))],
  ["all Site Pulse navigation controls exist", sections.every((id) => html.includes(`data-pulse-target="${id}"`))],
  ["navigation scrolls to section", js.includes("[data-pulse-target]") && js.includes("scrollIntoView")],
  ["diagnostics opens before navigation", js.includes('target?.tagName === "DETAILS"') && js.includes("target.open = true")],
  ["real date filters remain", html.includes('id="dash-days"') && html.includes('id="dash-from"') && html.includes('id="dash-to"')],
  ["real audience filter remains", html.includes('id="dash-audience"')],
];
let failures = 0;
for (const [name, ok] of checks) { console.log(`${ok ? "PASS" : "FAIL"} ${name}`); if (!ok) failures += 1; }
if (failures) process.exit(1);
console.log("\nAll Site Pulse shell checks passed.");

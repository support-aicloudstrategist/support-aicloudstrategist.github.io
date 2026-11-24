import fs from "fs";
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const checks = [
  ["start and close controls", html.includes('id="daily-start"') && html.includes('id="daily-close"')],
  ["live elapsed timer", html.includes('id="daily-elapsed"') && js.includes("setInterval(syncDailyTimer, 1000)")],
  ["active day persists", js.includes('internalRequest("tasks"') && js.includes('id: "active-day"')],
  ["closed day persists to history", js.includes('internalRequest("history"') && js.includes('status: "closed"')],
  ["day advances only from closed history", js.includes("dailyState.history?.length")],
  ["unfinished tasks carry over", js.includes("filter((task) => !task.done)") && js.includes("carried: true")],
  ["four-day review rhythm", js.includes("dayNumber % 4 === 0")],
  ["owner-only controls", js.includes('sessionIdentity?.role !== "owner"')],
];
let failures = 0;
for (const [name, ok] of checks) { console.log(`${ok ? "PASS" : "FAIL"} ${name}`); if (!ok) failures += 1; }
if (failures) process.exit(1);
console.log("\nAll Daily Operations contract checks passed.");

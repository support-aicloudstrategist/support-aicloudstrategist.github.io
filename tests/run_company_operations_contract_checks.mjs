import fs from "fs";
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const modules = ["crm", "delivery", "finance", "evidence", "knowledge"];
const checks = [
  ["all operations tabs exist", modules.every((name) => html.includes(`data-ops-tab="${name}"`))],
  ["all operations forms exist", modules.every((name) => html.includes(`data-ops-form="${name}"`))],
  ["records load from persistent API", js.includes("loadCompanyOperations") && js.includes("Promise.all(modules.map")],
  ["record add is wired", js.includes('method: "POST"') && js.includes("form.reset()")],
  ["record removal is wired", js.includes('method: "DELETE"') && js.includes("data-ops-delete")],
  ["viewer controls are disabled", js.includes('sessionIdentity?.role !== "owner"')],
  ["tabs switch panels", js.includes("data-ops-panel") && js.includes("panel.hidden")],
];
let failures = 0;
for (const [name, ok] of checks) { console.log(`${ok ? "PASS" : "FAIL"} ${name}`); if (!ok) failures += 1; }
if (failures) process.exit(1);
console.log("\nAll Company Operations contract checks passed.");

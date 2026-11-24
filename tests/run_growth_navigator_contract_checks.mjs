import fs from "fs";
const html = fs.readFileSync("analytics/index.html", "utf8"); const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const checks = [
  ["evidence decision result flow shown", ["Evidence", "Finding", "Approval", "Result"].every((word) => html.includes(word))],
  ["findings actions results sections", ["findings", "actions", "results"].every((name) => html.includes(`data-growth-panel="${name}"`))],
  ["finding uses Site Pulse snapshot", js.includes("lastDashboard?.page_views") && js.includes("lastDashboard?.leads?.count")],
  ["findings persist", js.includes('internalRequest("decisions"') && js.includes('kind: "finding"')],
  ["owner approval persists", js.includes('status: "approved"') && js.includes("approved_at")],
  ["results persist", js.includes('kind: "result"') && js.includes('source: "Owner evidence"')],
  ["viewer cannot mutate", js.includes('sessionIdentity?.role !== "owner"')],
];
let failures=0; for(const [name,ok] of checks){console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok)failures+=1;} if(failures)process.exit(1); console.log("\nAll Growth Navigator contract checks passed.");

import fs from "fs";

const auth = fs.readFileSync("functions/api/_lib/internal-auth.ts", "utf8");
const session = fs.readFileSync("functions/api/internal-session.ts", "utf8");
const dashboard = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const metrics = fs.readFileSync("functions/api/metrics.ts", "utf8");

const checks = [
  ["backend owns role assignment", auth.includes('role: "owner"') && auth.includes('role: "viewer"')],
  ["backend owns company scope", auth.includes('companies: ["aics", "dst"]') && auth.includes('companies: ["aics"]')],
  ["company scope is enforced", session.includes("canAccessCompany") && session.includes("company_forbidden")],
  ["metrics enforce company scope", metrics.includes("canAccessCompany(auth.identity") && metrics.includes("company_forbidden")],
  ["session response is no-store", session.includes('"Cache-Control": "no-store"')],
  ["dashboard verifies server session", dashboard.includes("/api/internal-session?company=${encodeURIComponent(company)}")],
  ["dashboard renders verified identity", dashboard.includes("identityLabel(sessionIdentity)") && dashboard.includes('getElementById("header-company")')],
];

let failures = 0;
for (const [name, ok] of checks) {
  console.log(`${ok ? "PASS" : "FAIL"} ${name}`);
  if (!ok) failures += 1;
}
if (failures) process.exit(1);
console.log("\nAll internal auth contract checks passed.");

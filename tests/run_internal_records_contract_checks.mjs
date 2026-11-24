import fs from "fs";

const source = fs.readFileSync("functions/api/internal-records.ts", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");
const checks = [
  ["transactional D1 binding required", source.includes("AICS_IDENTITY_DB?: D1Database") && source.includes("storage_unavailable")],
  ["company access enforced", source.includes("canAccessCompany") && source.includes("company_forbidden")],
  ["owner-only writes", source.includes('ctx.auth.role !== "owner"') && source.includes("write_forbidden")],
  ["all operating modules covered", ["tasks", "crm", "history", "finance", "delivery", "evidence", "knowledge", "decisions"].every((name) => source.includes(`"${name}"`))],
  ["records are company and module scoped", source.includes("WHERE company = ? AND module = ?")],
  ["concurrent edits use optimistic versions", source.includes("expected_version") && source.includes("edit_conflict") && js.includes("activeVersion")],
  ["payload size is bounded", source.includes("20000") && source.includes("record_too_large")],
  ["read write delete handlers exist", source.includes("onRequestGet") && source.includes("onRequestPost") && source.includes("onRequestDelete")],
  ["responses cannot be cached", source.includes('"Cache-Control": "no-store"')],
];

let failures = 0;
for (const [name, ok] of checks) {
  console.log(`${ok ? "PASS" : "FAIL"} ${name}`);
  if (!ok) failures += 1;
}
if (failures) process.exit(1);
console.log("\nAll internal records contract checks passed.");

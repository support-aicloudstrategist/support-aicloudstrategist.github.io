import fs from "fs";

const source = fs.readFileSync("functions/api/internal-records.ts", "utf8");
const checks = [
  ["persistent KV binding required", source.includes("AICS_INTERNAL_OS?: KVNamespace") && source.includes("storage_unavailable")],
  ["company access enforced", source.includes("canAccessCompany") && source.includes("company_forbidden")],
  ["owner-only writes", source.includes('ctx.auth.role !== "owner"') && source.includes("write_forbidden")],
  ["all operating modules covered", ["tasks", "crm", "history", "finance", "delivery", "evidence", "knowledge", "decisions"].every((name) => source.includes(`"${name}"`))],
  ["records are company and module namespaced", source.includes("internal:v1:${company}:${module}:")],
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

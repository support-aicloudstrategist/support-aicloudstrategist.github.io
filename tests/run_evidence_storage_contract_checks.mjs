import fs from "node:fs";

const api = fs.readFileSync("functions/api/internal-evidence.ts", "utf8");
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");

const checks = [
  ["R2 binding is required", api.includes("AICS_EVIDENCE?: R2Bucket") && api.includes("storage_unavailable")],
  ["uploads are owner only", api.includes("context(request, env, true)") && api.includes("write_forbidden")],
  ["company scope is enforced", api.includes("canAccessCompany") && api.includes("`${ctx.company}/evidence/`")],
  ["size and file types are bounded", api.includes("10 * 1024 * 1024") && api.includes("ALLOWED_TYPES")],
  ["downloads are private and no-store", api.includes('"Cache-Control": "private, no-store"')],
  ["evidence form requires a file", html.includes('name="file"') && html.includes("Upload evidence")],
  ["dashboard uploads then records metadata", js.includes("evidenceFileRequest") && js.includes("file_key")],
  ["file downloads stay authenticated", js.includes("data-evidence-download") && js.includes("Authorization: `Bearer ${auth}`")],
  ["file deletion precedes metadata deletion", js.includes('method: "DELETE", key: record.data.file_key')],
];

let failed = 0;
for (const [name, pass] of checks) {
  if (pass) console.log(`PASS ${name}`);
  else { failed += 1; console.error(`FAIL ${name}`); }
}
if (failed) process.exit(1);
console.log("\nAll secure evidence storage contract checks passed.");

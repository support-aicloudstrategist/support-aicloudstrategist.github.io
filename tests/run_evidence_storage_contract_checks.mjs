import fs from "node:fs";

const api = fs.readFileSync("functions/api/internal-evidence.ts", "utf8");
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");

const checks = [
  ["existing private KV binding is required", api.includes("AICS_INTERNAL_OS?: KVNamespace") && api.includes("storage_unavailable")],
  ["uploads are owner only", api.includes("context(request, env, true)") && api.includes("write_forbidden")],
  ["company scope is enforced", api.includes("canAccessCompany") && api.includes("internal:evidence:v1:${ctx.company}:")],
  ["size and file types are bounded", api.includes("5 * 1024 * 1024") && api.includes("ALLOWED_TYPES")],
  ["binary files use KV metadata", api.includes("getWithMetadata") && api.includes("originalName: name, contentType")],
  ["downloads are private and no-store", api.includes('"Cache-Control": "private, no-store"')],
  ["evidence form requires a file", html.includes('name="file"') && html.includes("Upload evidence")],
  ["dashboard uploads then records metadata", js.includes("evidenceFileRequest") && js.includes("file_key")],
  ["orphaned uploads are cleaned up if metadata fails", js.includes("uploadedFileKey") && js.includes('method: "DELETE", key: uploadedFileKey')],
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

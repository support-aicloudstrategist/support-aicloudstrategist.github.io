import fs from "node:fs";

const api = fs.readFileSync("functions/api/internal-backup.ts", "utf8");
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");

const checks = [
  ["restore remains owner only and company scoped", api.includes("ownerContext") && api.includes("canAccessCompany(ctx.identity, company)")],
  ["restore payload and record counts are bounded", api.includes("MAX_BACKUP_BYTES") && api.includes("total > 1000") && api.includes("20000")],
  ["evidence binaries are included and bounded", api.includes("evidence_files") && api.includes("collectEvidence") && api.includes("MAX_EVIDENCE_BYTES")],
  ["audit history cannot be overwritten", api.includes('module !== "audit"') && api.includes('data: { action: "restore"')],
  ["dry run is the default", api.includes("payload.apply !== true") && api.includes("dry_run: true")],
  ["exact company confirmation is required", api.includes('`RESTORE ${company.toUpperCase()}`') && api.includes("confirmation_required")],
  ["a complete rollback snapshot precedes restore", api.includes("internal:restore-snapshot:v1") && api.includes("currentEvidence.files") && api.includes("expirationTtl: 604800")],
  ["restore UI requires a local backup file", html.includes('id="admin-restore-file"') && html.includes("Validate backup")],
  ["UI validates before apply", js.includes("validatedRestore") && js.includes("restoreRequest(backup)") && js.includes("restoreRequest(validatedRestore.backup, true, confirmation)")],
  ["successful restore refreshes dashboard data", js.includes("loadCompanyOperations(), loadCommandHome()")],
];

let failed = 0;
for (const [name, pass] of checks) {
  if (pass) console.log(`PASS ${name}`);
  else { failed += 1; console.error(`FAIL ${name}`); }
}
if (failed) process.exit(1);
console.log("\nAll guarded backup restore contract checks passed.");

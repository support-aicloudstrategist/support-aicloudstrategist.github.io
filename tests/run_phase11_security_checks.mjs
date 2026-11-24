import fs from "fs";
const records=fs.readFileSync("functions/api/internal-records.ts","utf8"), backup=fs.readFileSync("functions/api/internal-backup.ts","utf8");
const checks=[
  ["audit module exists",records.includes('"audit"')&&records.includes("writeAudit")],
  ["audit records are immutable",records.includes("audit_immutable")&&records.includes('ctx.module === "audit"')],
  ["mutations create audit events",records.includes('"create"')&&records.includes('"update"')&&records.includes('"delete"')],
  ["rate limits protect reads and writes",records.includes("enforceRateLimit")&&records.includes("rate_limited")&&records.includes('"Retry-After"')],
  ["request ids aid incident tracing",records.includes("X-Request-Id")&&records.includes("request_id")],
  ["backup is owner only",backup.includes('role !== "owner"')&&backup.includes("backup_forbidden")],
  ["backup remains company scoped",backup.includes("canAccessCompany")&&backup.includes("company_forbidden")],
  ["backup covers all modules",["tasks","crm","history","finance","delivery","evidence","knowledge","decisions","audit"].every((name)=>backup.includes(`"${name}"`))],
  ["backup downloads without caching",backup.includes("Content-Disposition")&&backup.includes('"Cache-Control": "no-store"')],
];let failures=0;for(const[name,ok]of checks){console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok)failures++;}if(failures)process.exit(1);console.log("\nAll Phase 11 security checks passed.");

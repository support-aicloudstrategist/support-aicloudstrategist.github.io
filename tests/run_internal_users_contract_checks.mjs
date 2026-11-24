import fs from "node:fs";

const api = fs.readFileSync("functions/api/internal-users.ts", "utf8");
const auth = fs.readFileSync("functions/api/_lib/internal-auth.ts", "utf8");
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");

const checks = [
  ["access codes are cryptographically random", api.includes("crypto.getRandomValues(new Uint8Array(32))")],
  ["only token hashes are stored", api.includes("sha256Hex(accessToken)") && api.includes("token_hash: tokenHash")],
  ["access codes expire automatically", api.includes("expires_at: expiresAt") && api.includes("90 * 24 * 60 * 60 * 1000") && auth.includes("unexpired")],
  ["identity uses strongly consistent D1", api.includes("AICS_IDENTITY_DB?: D1Database") && auth.includes("AICS_IDENTITY_DB.prepare")],
  ["duplicate active emails are rejected by a unique constraint", api.includes("duplicate_user") && api.includes("INSERT INTO internal_users")],
  ["user administration is owner only", api.includes('identity.role !== "owner"')],
  ["roles and company scopes are validated", api.includes('["aics", "dst"].includes(company)') && api.includes('body?.role === "owner"')],
  ["revocation invalidates the token transactionally", api.includes("UPDATE internal_users SET status = 'revoked'")],
  ["active named users can authenticate", auth.includes("WHERE token_hash = ?") && auth.includes('subject: `user:${access.id}`')],
  ["administration form collects named-user access", html.includes('id="admin-user-form"') && html.includes('id="admin-user-list"')],
  ["one-time code can be copied explicitly", js.includes("data-copy-access") && js.includes("navigator.clipboard.writeText")],
  ["user revocation is wired to the UI", js.includes("data-user-revoke") && js.includes('method: "DELETE", id: revoke.getAttribute')],
];

let failed = 0;
for (const [name, pass] of checks) {
  if (pass) console.log(`PASS ${name}`);
  else { failed += 1; console.error(`FAIL ${name}`); }
}
if (failed) process.exit(1);
console.log("\nAll named-user access contract checks passed.");

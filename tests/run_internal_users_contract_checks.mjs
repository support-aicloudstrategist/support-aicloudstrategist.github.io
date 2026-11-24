import fs from "node:fs";

const api = fs.readFileSync("functions/api/internal-users.ts", "utf8");
const auth = fs.readFileSync("functions/api/_lib/internal-auth.ts", "utf8");
const html = fs.readFileSync("analytics/index.html", "utf8");
const js = fs.readFileSync("js/aics-analytics-dashboard.js", "utf8");

const checks = [
  ["access codes are cryptographically random", api.includes("crypto.getRandomValues(new Uint8Array(32))")],
  ["only token hashes are stored", api.includes("sha256Hex(accessToken)") && api.includes("token_hash: tokenHash")],
  ["access codes expire automatically", api.includes("expires_at: expiresAt") && api.includes("expirationTtl: 90 * 24 * 60 * 60") && auth.includes("unexpired")],
  ["duplicate active emails are rejected", api.includes("duplicate_user") && api.includes("user.email === email")],
  ["user administration is owner only", api.includes('identity.role !== "owner"')],
  ["roles and company scopes are validated", api.includes('["aics", "dst"].includes(company)') && api.includes('body?.role === "owner"')],
  ["revocation removes user and access index", api.includes('internal:user:v1:${id}') && api.includes('internal:access:v1:${user.token_hash}')],
  ["active named users can authenticate", auth.includes('internal:access:v1:${hash}') && auth.includes('subject: `user:${access.id}`')],
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

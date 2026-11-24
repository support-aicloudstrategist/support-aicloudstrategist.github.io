import { authorizeInternal, canAccessCompany, type InternalAuthEnv } from "./_lib/internal-auth";

type BackupEnv = InternalAuthEnv & { AICS_INTERNAL_OS?: KVNamespace };
const MODULES = ["tasks", "crm", "history", "finance", "delivery", "evidence", "knowledge", "decisions", "audit"];
const RESTORABLE_MODULES = MODULES.filter((module) => module !== "audit");
const MAX_BACKUP_BYTES = 2 * 1024 * 1024;
const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers });

async function ownerContext(request: Request, env: BackupEnv) {
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) return { response: json({ ok: false, code: auth.code, error: auth.error }, auth.status) };
  if (auth.identity.role !== "owner") return { response: json({ ok: false, code: "backup_forbidden", error: "Owner access is required." }, 403) };
  if (!env.AICS_INTERNAL_OS) return { response: json({ ok: false, code: "storage_unavailable", error: "Internal storage is not configured." }, 503) };
  return { identity: auth.identity, store: env.AICS_INTERNAL_OS };
}

export const onRequestGet: PagesFunction<BackupEnv> = async ({ request, env }) => {
  const requestId = crypto.randomUUID();
  const auth = await authorizeInternal(request, env);
  const baseHeaders = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Request-Id": requestId };
  if (!auth.ok) return new Response(JSON.stringify({ ok: false, code: auth.code, error: auth.error, request_id: requestId }), { status: auth.status, headers: baseHeaders });
  if (auth.identity.role !== "owner") return new Response(JSON.stringify({ ok: false, code: "backup_forbidden", error: "Owner access is required.", request_id: requestId }), { status: 403, headers: baseHeaders });
  const company = String(new URL(request.url).searchParams.get("company") || "aics").trim().toLowerCase();
  if (!canAccessCompany(auth.identity, company)) return new Response(JSON.stringify({ ok: false, code: "company_forbidden", error: "Company access is not allowed.", request_id: requestId }), { status: 403, headers: baseHeaders });
  if (!env.AICS_INTERNAL_OS) return new Response(JSON.stringify({ ok: false, code: "storage_unavailable", error: "Internal storage is not configured.", request_id: requestId }), { status: 503, headers: baseHeaders });
  const records: Record<string, unknown[]> = {};
  for (const module of MODULES) {
    const listed = await env.AICS_INTERNAL_OS.list({ prefix: `internal:v1:${company}:${module}:`, limit: 1000 });
    records[module] = (await Promise.all(listed.keys.map((key) => env.AICS_INTERNAL_OS!.get(key.name, "json")))).filter(Boolean);
  }
  const generatedAt = new Date().toISOString();
  return new Response(JSON.stringify({ ok: true, schema_version: 1, company, generated_at: generatedAt, records, request_id: requestId }, null, 2), {
    status: 200,
    headers: { ...baseHeaders, "Content-Disposition": `attachment; filename="aics-internal-backup-${generatedAt.slice(0, 10)}.json"` },
  });
};

export const onRequestPost: PagesFunction<BackupEnv> = async ({ request, env }) => {
  const ctx = await ownerContext(request, env);
  if ("response" in ctx) return ctx.response;
  if (Number(request.headers.get("Content-Length") || 0) > MAX_BACKUP_BYTES) return json({ ok: false, code: "backup_too_large", error: "Backup exceeds the 2 MB restore limit." }, 413);
  const raw = await request.text();
  if (new TextEncoder().encode(raw).byteLength > MAX_BACKUP_BYTES) return json({ ok: false, code: "backup_too_large", error: "Backup exceeds the 2 MB restore limit." }, 413);
  let payload: any;
  try { payload = JSON.parse(raw); } catch { return json({ ok: false, code: "invalid_backup", error: "Backup must be valid JSON." }, 400); }
  const backup = payload?.backup;
  const company = String(backup?.company || "").trim().toLowerCase();
  if (backup?.schema_version !== 1 || !company || !backup?.records || typeof backup.records !== "object") return json({ ok: false, code: "invalid_backup", error: "Backup schema is invalid." }, 400);
  if (!canAccessCompany(ctx.identity, company)) return json({ ok: false, code: "company_forbidden", error: "Company access is not allowed." }, 403);
  let total = 0;
  const normalized: Record<string, any[]> = {};
  for (const module of RESTORABLE_MODULES) {
    const records = backup.records[module] ?? [];
    if (!Array.isArray(records)) return json({ ok: false, code: "invalid_backup", error: `${module} records must be an array.` }, 400);
    normalized[module] = records;
    for (const record of records) {
      total += 1;
      if (total > 1000 || !record || typeof record !== "object" || !/^[a-zA-Z0-9_-]{1,100}$/.test(String(record.id || "")) || record.company !== company || record.module !== module || !record.data || typeof record.data !== "object" || Array.isArray(record.data) || JSON.stringify(record.data).length > 20000) {
        return json({ ok: false, code: "invalid_backup", error: "Backup contains an invalid or excessive record set." }, 400);
      }
    }
  }
  const counts = Object.fromEntries(RESTORABLE_MODULES.map((module) => [module, normalized[module].length]));
  if (payload.apply !== true) return json({ ok: true, dry_run: true, company, counts, total, required_confirmation: `RESTORE ${company.toUpperCase()}` });
  if (payload.confirm !== `RESTORE ${company.toUpperCase()}`) return json({ ok: false, code: "confirmation_required", error: "Exact restore confirmation is required." }, 409);

  const current: Record<string, unknown[]> = {};
  for (const module of RESTORABLE_MODULES) {
    const listed = await ctx.store.list({ prefix: `internal:v1:${company}:${module}:`, limit: 1000 });
    current[module] = (await Promise.all(listed.keys.map((key) => ctx.store.get(key.name, "json")))).filter(Boolean);
  }
  const snapshotId = `${Date.now()}-${crypto.randomUUID()}`;
  await ctx.store.put(`internal:restore-snapshot:v1:${company}:${snapshotId}`, JSON.stringify({ schema_version: 1, company, generated_at: new Date().toISOString(), records: current }), { expirationTtl: 604800 });
  for (const module of RESTORABLE_MODULES) {
    const listed = await ctx.store.list({ prefix: `internal:v1:${company}:${module}:`, limit: 1000 });
    await Promise.all(listed.keys.map((key) => ctx.store.delete(key.name)));
    await Promise.all(normalized[module].map((record) => ctx.store.put(`internal:v1:${company}:${module}:${record.id}`, JSON.stringify({ ...record, company, module, updated_at: new Date().toISOString(), updated_by: ctx.identity.subject }))));
  }
  const auditId = `${Date.now()}-${crypto.randomUUID()}`;
  const now = new Date().toISOString();
  await ctx.store.put(`internal:v1:${company}:audit:${auditId}`, JSON.stringify({ id: auditId, company, module: "audit", data: { action: "restore", actor: ctx.identity.subject, restored_records: total, snapshot_id: snapshotId }, created_at: now, updated_at: now, updated_by: ctx.identity.subject }));
  return json({ ok: true, restored: true, company, counts, total, snapshot_created: true });
};

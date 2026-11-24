import { authorizeInternal, canAccessCompany, type InternalAuthEnv } from "./_lib/internal-auth";

type InternalRecordsEnv = InternalAuthEnv & { AICS_INTERNAL_OS?: KVNamespace; AICS_IDENTITY_DB?: D1Database };
const MODULES = new Set(["tasks", "crm", "history", "finance", "delivery", "evidence", "knowledge", "decisions", "audit"]);
const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
const json = (body: unknown, status = 200, extra: Record<string, string> = {}) => new Response(JSON.stringify(body), { status, headers: { ...headers, ...extra } });
const clean = (value: unknown, max = 120) => String(value ?? "").trim().slice(0, max);
const validId = (value: unknown) => /^[a-zA-Z0-9_-]{1,100}$/.test(String(value || ""));
const rowToRecord = (row: any) => ({ ...row, data: JSON.parse(row.data || "{}") });

async function enforceRateLimit(store: KVNamespace, subject: string, write: boolean, requestId: string) {
  const minute = Math.floor(Date.now() / 60000);
  const key = `internal:rate:v1:${subject}:${minute}:${write ? "write" : "read"}`;
  const current = Number(await store.get(key) || 0);
  const limit = write ? 40 : 180;
  if (current >= limit) return json({ ok: false, code: "rate_limited", error: "Too many internal requests. Try again shortly.", request_id: requestId }, 429, { "Retry-After": "60", "X-Request-Id": requestId });
  await store.put(key, String(current + 1), { expirationTtl: 120 });
  return null;
}

async function context(request: Request, env: InternalRecordsEnv) {
  const requestId = crypto.randomUUID();
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) return { response: json({ ok: false, code: auth.code, error: auth.error, request_id: requestId }, auth.status, { "X-Request-Id": requestId }) };
  const url = new URL(request.url);
  const company = clean(url.searchParams.get("company") || "aics", 40).toLowerCase();
  const module = clean(url.searchParams.get("module"), 40).toLowerCase();
  if (!canAccessCompany(auth.identity, company)) return { response: json({ ok: false, code: "company_forbidden", error: "Company access is not allowed.", request_id: requestId }, 403) };
  if (!MODULES.has(module)) return { response: json({ ok: false, code: "invalid_module", error: "A supported module is required.", request_id: requestId }, 400) };
  if (!env.AICS_IDENTITY_DB || !env.AICS_INTERNAL_OS) return { response: json({ ok: false, code: "storage_unavailable", error: "Transactional internal storage is not configured.", request_id: requestId }, 503) };
  return { auth: auth.identity, company, module, db: env.AICS_IDENTITY_DB, rateStore: env.AICS_INTERNAL_OS, url, requestId };
}

export const onRequestGet: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  const limited = await enforceRateLimit(ctx.rateStore, ctx.auth.subject, false, ctx.requestId);
  if (limited) return limited;
  const id = clean(ctx.url.searchParams.get("id"), 100);
  if (id) {
    if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is invalid." }, 400);
    const row = await ctx.db.prepare("SELECT * FROM internal_records WHERE company = ? AND module = ? AND id = ?").bind(ctx.company, ctx.module, id).first();
    return row ? json({ ok: true, record: rowToRecord(row), request_id: ctx.requestId }) : json({ ok: false, code: "not_found", error: "Record was not found.", request_id: ctx.requestId }, 404);
  }
  const limit = Math.min(200, Math.max(1, Number(ctx.url.searchParams.get("limit") || 100)));
  const result = await ctx.db.prepare("SELECT * FROM internal_records WHERE company = ? AND module = ? ORDER BY updated_at DESC LIMIT ?").bind(ctx.company, ctx.module, limit).all();
  return json({ ok: true, company: ctx.company, module: ctx.module, records: (result.results || []).map(rowToRecord), cursor: null, request_id: ctx.requestId });
};

export const onRequestPost: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  if (ctx.auth.role !== "owner") return json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403);
  if (ctx.module === "audit") return json({ ok: false, code: "audit_immutable", error: "Audit records cannot be created directly." }, 403);
  const limited = await enforceRateLimit(ctx.rateStore, ctx.auth.subject, true, ctx.requestId);
  if (limited) return limited;
  let payload: any;
  try { payload = await request.json(); } catch { return json({ ok: false, code: "invalid_json", error: "Valid JSON is required." }, 400); }
  const id = clean(payload?.id || crypto.randomUUID(), 100);
  if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is invalid." }, 400);
  const data = payload?.data;
  if (!data || typeof data !== "object" || Array.isArray(data)) return json({ ok: false, code: "invalid_data", error: "Record data must be an object." }, 400);
  const encoded = JSON.stringify(data);
  if (encoded.length > 20000) return json({ ok: false, code: "record_too_large", error: "Record exceeds the 20 KB limit." }, 413);
  const existing: any = await ctx.db.prepare("SELECT created_at, version FROM internal_records WHERE company = ? AND module = ? AND id = ?").bind(ctx.company, ctx.module, id).first();
  if (existing && Number(payload?.expected_version) !== Number(existing.version)) return json({ ok: false, code: "edit_conflict", error: "This record changed in another session. Reload before saving." }, 409);
  const now = new Date().toISOString();
  const version = existing ? Number(existing.version) + 1 : 1;
  const auditId = `${Date.now()}-${crypto.randomUUID()}`;
  const recordStatement = existing
    ? ctx.db.prepare("UPDATE internal_records SET data = ?, updated_at = ?, updated_by = ?, version = version + 1 WHERE company = ? AND module = ? AND id = ? AND version = ?").bind(encoded, now, ctx.auth.subject, ctx.company, ctx.module, id, existing.version)
    : ctx.db.prepare("INSERT INTO internal_records (company, module, id, data, created_at, updated_at, updated_by, version) VALUES (?, ?, ?, ?, ?, ?, ?, 1) ON CONFLICT(company, module, id) DO NOTHING").bind(ctx.company, ctx.module, id, encoded, now, now, ctx.auth.subject);
  const auditStatement = ctx.db.prepare("INSERT INTO internal_records (company, module, id, data, created_at, updated_at, updated_by, version) SELECT ?, 'audit', ?, ?, ?, ?, ?, 1 WHERE EXISTS (SELECT 1 FROM internal_records WHERE company = ? AND module = ? AND id = ? AND version = ? AND updated_at = ? AND updated_by = ?)").bind(ctx.company, auditId, JSON.stringify({ action: existing ? "update" : "create", target_module: ctx.module, target_id: id, actor: ctx.auth.subject, request_id: ctx.requestId }), now, now, ctx.auth.subject, ctx.company, ctx.module, id, version, now, ctx.auth.subject);
  const results = await ctx.db.batch([recordStatement, auditStatement]);
  if (Number(results[0]?.meta?.changes || 0) !== 1) return json({ ok: false, code: "edit_conflict", error: "This record changed in another session. Reload before saving." }, 409);
  return json({ ok: true, record: { id, company: ctx.company, module: ctx.module, data, created_at: existing?.created_at || now, updated_at: now, updated_by: ctx.auth.subject, version }, request_id: ctx.requestId }, existing ? 200 : 201);
};

export const onRequestDelete: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  if (ctx.auth.role !== "owner") return json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403);
  if (ctx.module === "audit") return json({ ok: false, code: "audit_immutable", error: "Audit records cannot be deleted." }, 403);
  const limited = await enforceRateLimit(ctx.rateStore, ctx.auth.subject, true, ctx.requestId);
  if (limited) return limited;
  const id = clean(ctx.url.searchParams.get("id"), 100);
  if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is required." }, 400);
  const now = new Date().toISOString();
  const auditId = `${Date.now()}-${crypto.randomUUID()}`;
  await ctx.db.batch([
    ctx.db.prepare("DELETE FROM internal_records WHERE company = ? AND module = ? AND id = ?").bind(ctx.company, ctx.module, id),
    ctx.db.prepare("INSERT INTO internal_records (company, module, id, data, created_at, updated_at, updated_by, version) VALUES (?, 'audit', ?, ?, ?, ?, ?, 1)").bind(ctx.company, auditId, JSON.stringify({ action: "delete", target_module: ctx.module, target_id: id, actor: ctx.auth.subject, request_id: ctx.requestId }), now, now, ctx.auth.subject),
  ]);
  return json({ ok: true, deleted: id, request_id: ctx.requestId });
};

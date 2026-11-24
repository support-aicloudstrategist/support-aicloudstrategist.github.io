import { authorizeInternal, canAccessCompany, type InternalAuthEnv } from "./_lib/internal-auth";

type InternalRecordsEnv = InternalAuthEnv & { AICS_INTERNAL_OS?: KVNamespace };

const MODULES = new Set(["tasks", "crm", "history", "finance", "delivery", "evidence", "knowledge", "decisions", "audit"]);
const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };

const json = (body: unknown, status = 200, extraHeaders: Record<string, string> = {}) => new Response(JSON.stringify(body), { status, headers: { ...headers, ...extraHeaders } });
const clean = (value: unknown, max = 120) => String(value ?? "").trim().slice(0, max);
const validId = (value: unknown) => /^[a-zA-Z0-9_-]{1,100}$/.test(String(value || ""));
const prefixFor = (company: string, module: string) => `internal:v1:${company}:${module}:`;

async function enforceRateLimit(store: KVNamespace, subject: string, write: boolean, requestId: string) {
  const minute = Math.floor(Date.now() / 60000);
  const key = `internal:rate:v1:${subject}:${minute}:${write ? "write" : "read"}`;
  const current = Number(await store.get(key) || 0);
  const limit = write ? 40 : 180;
  if (current >= limit) return json({ ok: false, code: "rate_limited", error: "Too many internal requests. Try again shortly.", request_id: requestId }, 429, { "Retry-After": "60", "X-Request-Id": requestId });
  await store.put(key, String(current + 1), { expirationTtl: 120 });
  return null;
}

async function writeAudit(store: KVNamespace, company: string, actor: string, action: string, module: string, recordId: string, requestId: string) {
  const now = new Date().toISOString();
  const id = `${Date.now()}-${crypto.randomUUID()}`;
  await store.put(`${prefixFor(company, "audit")}${id}`, JSON.stringify({ id, company, module: "audit", data: { action, target_module: module, target_id: recordId, actor, request_id: requestId }, created_at: now, updated_at: now, updated_by: actor }));
}

async function context(request: Request, env: InternalRecordsEnv) {
  const requestId = crypto.randomUUID();
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) return { response: json({ ok: false, code: auth.code, error: auth.error, request_id: requestId }, auth.status, { "X-Request-Id": requestId }) };
  const url = new URL(request.url);
  const company = clean(url.searchParams.get("company") || "aics", 40).toLowerCase();
  const module = clean(url.searchParams.get("module"), 40).toLowerCase();
  if (!canAccessCompany(auth.identity, company)) return { response: json({ ok: false, code: "company_forbidden", error: "Company access is not allowed.", request_id: requestId }, 403, { "X-Request-Id": requestId }) };
  if (!MODULES.has(module)) return { response: json({ ok: false, code: "invalid_module", error: "A supported module is required.", request_id: requestId }, 400, { "X-Request-Id": requestId }) };
  if (!env.AICS_INTERNAL_OS) return { response: json({ ok: false, code: "storage_unavailable", error: "Internal storage is not configured.", request_id: requestId }, 503, { "X-Request-Id": requestId }) };
  return { auth: auth.identity, company, module, store: env.AICS_INTERNAL_OS, url, requestId };
}

export const onRequestGet: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  const limited = await enforceRateLimit(ctx.store, ctx.auth.subject, false, ctx.requestId);
  if (limited) return limited;
  const id = clean(ctx.url.searchParams.get("id"), 100);
  if (id) {
    if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is invalid." }, 400);
    const record = await ctx.store.get(`${prefixFor(ctx.company, ctx.module)}${id}`, "json");
    return record ? json({ ok: true, record, request_id: ctx.requestId }, 200, { "X-Request-Id": ctx.requestId }) : json({ ok: false, code: "not_found", error: "Record was not found.", request_id: ctx.requestId }, 404, { "X-Request-Id": ctx.requestId });
  }
  const limit = Math.min(200, Math.max(1, Number(ctx.url.searchParams.get("limit") || 100)));
  const listed = await ctx.store.list({ prefix: prefixFor(ctx.company, ctx.module), limit });
  const records = (await Promise.all(listed.keys.map((key) => ctx.store.get(key.name, "json")))).filter(Boolean);
  records.sort((a: any, b: any) => String(b.updated_at || b.created_at).localeCompare(String(a.updated_at || a.created_at)));
  return json({ ok: true, company: ctx.company, module: ctx.module, records, cursor: listed.list_complete ? null : listed.cursor || null, request_id: ctx.requestId }, 200, { "X-Request-Id": ctx.requestId });
};

export const onRequestPost: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  if (ctx.auth.role !== "owner") return json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403);
  if (ctx.module === "audit") return json({ ok: false, code: "audit_immutable", error: "Audit records cannot be created directly." }, 403);
  const limited = await enforceRateLimit(ctx.store, ctx.auth.subject, true, ctx.requestId);
  if (limited) return limited;
  let payload: any;
  try { payload = await request.json(); } catch { return json({ ok: false, code: "invalid_json", error: "Valid JSON is required." }, 400); }
  const id = clean(payload?.id || crypto.randomUUID(), 100);
  if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is invalid." }, 400);
  const data = payload?.data;
  if (!data || typeof data !== "object" || Array.isArray(data)) return json({ ok: false, code: "invalid_data", error: "Record data must be an object." }, 400);
  const encoded = JSON.stringify(data);
  if (encoded.length > 20000) return json({ ok: false, code: "record_too_large", error: "Record exceeds the 20 KB limit." }, 413);
  const key = `${prefixFor(ctx.company, ctx.module)}${id}`;
  const existing: any = await ctx.store.get(key, "json");
  const now = new Date().toISOString();
  const record = { id, company: ctx.company, module: ctx.module, data, created_at: existing?.created_at || now, updated_at: now, updated_by: ctx.auth.subject };
  await ctx.store.put(key, JSON.stringify(record));
  await writeAudit(ctx.store, ctx.company, ctx.auth.subject, existing ? "update" : "create", ctx.module, id, ctx.requestId);
  return json({ ok: true, record, request_id: ctx.requestId }, existing ? 200 : 201, { "X-Request-Id": ctx.requestId });
};

export const onRequestDelete: PagesFunction<InternalRecordsEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  if (ctx.auth.role !== "owner") return json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403);
  if (ctx.module === "audit") return json({ ok: false, code: "audit_immutable", error: "Audit records cannot be deleted." }, 403);
  const limited = await enforceRateLimit(ctx.store, ctx.auth.subject, true, ctx.requestId);
  if (limited) return limited;
  const id = clean(ctx.url.searchParams.get("id"), 100);
  if (!validId(id)) return json({ ok: false, code: "invalid_id", error: "Record id is required." }, 400);
  await ctx.store.delete(`${prefixFor(ctx.company, ctx.module)}${id}`);
  await writeAudit(ctx.store, ctx.company, ctx.auth.subject, "delete", ctx.module, id, ctx.requestId);
  return json({ ok: true, deleted: id, request_id: ctx.requestId }, 200, { "X-Request-Id": ctx.requestId });
};

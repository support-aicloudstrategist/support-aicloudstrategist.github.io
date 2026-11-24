import { authorizeInternal, canAccessCompany, type InternalAuthEnv } from "./_lib/internal-auth";

type EvidenceEnv = InternalAuthEnv & { AICS_INTERNAL_OS?: KVNamespace };

const MAX_FILE_BYTES = 5 * 1024 * 1024;
const ALLOWED_TYPES = new Set([
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/webp",
  "text/csv",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]);
const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers });
const clean = (value: unknown, max = 180) => String(value ?? "").trim().slice(0, max);
const safeName = (value: unknown) => clean(value || "evidence", 180).replace(/[^a-zA-Z0-9._ -]+/g, "-").replace(/\s+/g, "-");

async function context(request: Request, env: EvidenceEnv, ownerOnly = false) {
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) return { response: json({ ok: false, code: auth.code, error: auth.error }, auth.status) };
  if (ownerOnly && auth.identity.role !== "owner") return { response: json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403) };
  const company = clean(new URL(request.url).searchParams.get("company") || "aics", 40).toLowerCase();
  if (!canAccessCompany(auth.identity, company)) return { response: json({ ok: false, code: "company_forbidden", error: "Company access is not allowed." }, 403) };
  if (!env.AICS_INTERNAL_OS) return { response: json({ ok: false, code: "storage_unavailable", error: "Secure evidence storage is not configured." }, 503) };
  return { auth: auth.identity, company, store: env.AICS_INTERNAL_OS };
}

export const onRequestPost: PagesFunction<EvidenceEnv> = async ({ request, env }) => {
  const ctx = await context(request, env, true);
  if ("response" in ctx) return ctx.response;
  const url = new URL(request.url);
  const name = safeName(url.searchParams.get("name"));
  const contentType = clean(request.headers.get("Content-Type") || "application/octet-stream", 120).toLowerCase();
  const declaredSize = Number(request.headers.get("Content-Length") || 0);
  if (!ALLOWED_TYPES.has(contentType)) return json({ ok: false, code: "unsupported_file", error: "Use PDF, PNG, JPEG, WebP, CSV, DOCX or XLSX evidence files." }, 415);
  if (declaredSize > MAX_FILE_BYTES) return json({ ok: false, code: "file_too_large", error: "Evidence files must be 5 MB or smaller." }, 413);
  const body = await request.arrayBuffer();
  if (!body.byteLength || body.byteLength > MAX_FILE_BYTES) return json({ ok: false, code: "invalid_file_size", error: "Evidence files must be between 1 byte and 5 MB." }, 413);
  const id = crypto.randomUUID();
  const key = `internal:evidence:v1:${ctx.company}:${id}`;
  await ctx.store.put(key, body, { metadata: { company: ctx.company, uploadedBy: ctx.auth.subject, originalName: name, contentType } });
  return json({ ok: true, file: { id, key, name, content_type: contentType, size: body.byteLength } }, 201);
};

export const onRequestGet: PagesFunction<EvidenceEnv> = async ({ request, env }) => {
  const ctx = await context(request, env);
  if ("response" in ctx) return ctx.response;
  const key = clean(new URL(request.url).searchParams.get("key"), 500);
  if (!key.startsWith(`internal:evidence:v1:${ctx.company}:`)) return json({ ok: false, code: "invalid_key", error: "Evidence key is invalid." }, 400);
  const object = await ctx.store.getWithMetadata<{ originalName?: string; contentType?: string }>(key, "arrayBuffer");
  if (!object.value) return json({ ok: false, code: "not_found", error: "Evidence file was not found." }, 404);
  const name = safeName(object.metadata?.originalName || "evidence");
  const responseHeaders = new Headers({ "Cache-Control": "private, no-store", "Content-Disposition": `attachment; filename="${name}"` });
  if (object.metadata?.contentType) responseHeaders.set("Content-Type", object.metadata.contentType);
  return new Response(object.value, { status: 200, headers: responseHeaders });
};

export const onRequestDelete: PagesFunction<EvidenceEnv> = async ({ request, env }) => {
  const ctx = await context(request, env, true);
  if ("response" in ctx) return ctx.response;
  const key = clean(new URL(request.url).searchParams.get("key"), 500);
  if (!key.startsWith(`internal:evidence:v1:${ctx.company}:`)) return json({ ok: false, code: "invalid_key", error: "Evidence key is invalid." }, 400);
  await ctx.store.delete(key);
  return json({ ok: true, deleted: key });
};

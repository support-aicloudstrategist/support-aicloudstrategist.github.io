import { authorizeInternal, sha256Hex, type InternalAuthEnv, type InternalRole } from "./_lib/internal-auth";

type UsersEnv = InternalAuthEnv & { AICS_INTERNAL_OS?: KVNamespace };
type StoredUser = { id: string; name: string; email: string; role: InternalRole; companies: string[]; status: "active"; token_hash: string; created_at: string; created_by: string };

const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers });
const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);
const publicUser = ({ token_hash: _tokenHash, ...user }: StoredUser) => user;
const randomToken = () => {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
};

async function ownerContext(request: Request, env: UsersEnv) {
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) return { response: json({ ok: false, code: auth.code, error: auth.error }, auth.status) };
  if (auth.identity.role !== "owner") return { response: json({ ok: false, code: "write_forbidden", error: "Owner access is required." }, 403) };
  if (!env.AICS_INTERNAL_OS) return { response: json({ ok: false, code: "storage_unavailable", error: "Internal user storage is not configured." }, 503) };
  return { identity: auth.identity, store: env.AICS_INTERNAL_OS };
}

export const onRequestGet: PagesFunction<UsersEnv> = async ({ request, env }) => {
  const ctx = await ownerContext(request, env);
  if ("response" in ctx) return ctx.response;
  const listed = await ctx.store.list({ prefix: "internal:user:v1:", limit: 200 });
  const users = (await Promise.all(listed.keys.map((key) => ctx.store.get(key.name, "json") as Promise<StoredUser | null>))).filter(Boolean).map((user) => publicUser(user as StoredUser));
  return json({ ok: true, users });
};

export const onRequestPost: PagesFunction<UsersEnv> = async ({ request, env }) => {
  const ctx = await ownerContext(request, env);
  if ("response" in ctx) return ctx.response;
  let body: any;
  try { body = await request.json(); } catch { return json({ ok: false, code: "invalid_json", error: "Valid JSON is required." }, 400); }
  const name = clean(body?.name, 100);
  const email = clean(body?.email, 160).toLowerCase();
  const role: InternalRole = body?.role === "owner" ? "owner" : "viewer";
  const companies = Array.from(new Set((Array.isArray(body?.companies) ? body.companies : ["aics"]).map((company: unknown) => clean(company, 40).toLowerCase()).filter((company: string) => ["aics", "dst"].includes(company))));
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !companies.length) return json({ ok: false, code: "invalid_user", error: "Name, valid email and at least one company are required." }, 400);
  const accessToken = randomToken();
  const tokenHash = await sha256Hex(accessToken);
  const now = new Date().toISOString();
  const user: StoredUser = { id: crypto.randomUUID(), name, email, role, companies, status: "active", token_hash: tokenHash, created_at: now, created_by: ctx.identity.subject };
  await ctx.store.put(`internal:user:v1:${user.id}`, JSON.stringify(user));
  await ctx.store.put(`internal:access:v1:${tokenHash}`, JSON.stringify({ id: user.id, role, companies, status: "active" }));
  return json({ ok: true, user: publicUser(user), access_token: accessToken, notice: "Show this access code once and share it through an approved secure channel." }, 201);
};

export const onRequestDelete: PagesFunction<UsersEnv> = async ({ request, env }) => {
  const ctx = await ownerContext(request, env);
  if ("response" in ctx) return ctx.response;
  const id = clean(new URL(request.url).searchParams.get("id"), 100);
  if (!id) return json({ ok: false, code: "missing_id", error: "User id is required." }, 400);
  const user = await ctx.store.get(`internal:user:v1:${id}`, "json") as StoredUser | null;
  if (!user) return json({ ok: false, code: "not_found", error: "User was not found." }, 404);
  await Promise.all([ctx.store.delete(`internal:user:v1:${id}`), ctx.store.delete(`internal:access:v1:${user.token_hash}`)]);
  return json({ ok: true, revoked: id });
};

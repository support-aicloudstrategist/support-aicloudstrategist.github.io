export type InternalRole = "owner" | "viewer";

export type InternalIdentity = {
  subject: string;
  role: InternalRole;
  companies: string[];
};

export type InternalAuthEnv = {
  AICS_REPORT_TOKEN?: string;
  AICS_INTERNAL_OS?: KVNamespace;
};

export type InternalAuthResult =
  | { ok: true; identity: InternalIdentity }
  | { ok: false; status: number; code: string; error: string };

const PRODUCT_READER_SHA256 = "95c7ac6b1f2ed3024b6bb22333cb9cb1414c01c4d6c1179ff967d857068bacdf";

const normalizeToken = (value: unknown) => {
  let token = String(value ?? "").replace(/^\uFEFF/, "").trim().slice(0, 512);
  if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) {
    token = token.slice(1, -1).trim();
  }
  return token.replace(/^Bearer\s+/i, "").trim();
};

const tokenFromRequest = (request: Request) =>
  normalizeToken(request.headers.get("Authorization") || request.headers.get("X-AICS-Report-Token") || "");

const sha256Hex = async (value: string) => {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
};

export async function authorizeInternal(request: Request, env: InternalAuthEnv): Promise<InternalAuthResult> {
  const supplied = tokenFromRequest(request);
  const ownerToken = normalizeToken(env.AICS_REPORT_TOKEN);
  if (!supplied) {
    return { ok: false, status: 401, code: "missing_authorization", error: "Sign in is required." };
  }
  if (ownerToken && supplied === ownerToken) {
    return { ok: true, identity: { subject: "aics-owner", role: "owner", companies: ["aics", "dst"] } };
  }
  if ((await sha256Hex(supplied)) === PRODUCT_READER_SHA256) {
    return { ok: true, identity: { subject: "company-agents-reader", role: "viewer", companies: ["aics"] } };
  }
  if (env.AICS_INTERNAL_OS) {
    const hash = await sha256Hex(supplied);
    const access = await env.AICS_INTERNAL_OS.get(`internal:access:v1:${hash}`, "json") as { id?: string; role?: InternalRole; companies?: string[]; status?: string } | null;
    if (access?.id && access.status === "active" && (access.role === "owner" || access.role === "viewer") && Array.isArray(access.companies)) {
      return { ok: true, identity: { subject: `user:${access.id}`, role: access.role, companies: access.companies.map((company) => String(company).toLowerCase()) } };
    }
  }
  if (!ownerToken) {
    return { ok: false, status: 503, code: "server_token_missing", error: "Internal authentication is not configured." };
  }
  return { ok: false, status: 401, code: "invalid_token", error: "Access key does not match." };
}

export { sha256Hex };

export function canAccessCompany(identity: InternalIdentity, company: string) {
  return identity.companies.includes(String(company || "").trim().toLowerCase());
}

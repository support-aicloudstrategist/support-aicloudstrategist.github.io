import { authorizeInternal, canAccessCompany, type InternalAuthEnv } from "./_lib/internal-auth";

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

export const onRequestGet: PagesFunction<InternalAuthEnv> = async ({ request, env }) => {
  const auth = await authorizeInternal(request, env);
  if (!auth.ok) {
    return new Response(JSON.stringify({ ok: false, code: auth.code, error: auth.error }), {
      status: auth.status,
      headers,
    });
  }
  const requestedCompany = String(new URL(request.url).searchParams.get("company") || "aics").trim().toLowerCase();
  if (!canAccessCompany(auth.identity, requestedCompany)) {
    return new Response(JSON.stringify({ ok: false, code: "company_forbidden", error: "Company access is not allowed." }), {
      status: 403,
      headers,
    });
  }
  return new Response(JSON.stringify({
    ok: true,
    identity: {
      subject: auth.identity.subject,
      role: auth.identity.role,
      companies: auth.identity.companies,
      active_company: requestedCompany,
    },
  }), { status: 200, headers });
};

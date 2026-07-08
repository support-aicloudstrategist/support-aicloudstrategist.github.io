type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const APPROVAL_KEY = "raj-approved-2026-07-08-mixed-top-5-send";

const EXPECTED = [
  { customer: "Facets.cloud", to: "prashant@facets.cloud", subject: "Facets.cloud: a 30-day cloud control snapshot for platform growth" },
  { customer: "Sleepy Owl Coffee", to: "arman@sleepyowl.co", subject: "Sleepy Owl: where D2C revenue may leak after the first click" },
  { customer: "Aditi Dental Care", to: "aditidentalcare@gmail.com", subject: "Aditi Dental Care: missed appointment leakage between Google, calls and follow-up" },
  { customer: "Chauhan’s Dental Care", to: "chauhansdentalcare@gmail.com", subject: "Chauhan’s Dental Care: turning multiple enquiry channels into booked appointments" },
  { customer: "Vakilsearch", to: "hamilton@vakilsearch.com", subject: "Vakilsearch: reducing client drop-off between enquiry and document completion" },
];

const jsonHeaders = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" };

function clean(value: unknown): string { return typeof value === "string" ? value.trim() : ""; }
function sleep(ms: number) { return new Promise((resolve) => setTimeout(resolve, ms)); }
function norm(value: string) { return value.trim().toLowerCase(); }

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");
  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt > now + 60_000) return graphTokenCache.token;
  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    scope: "https://graph.microsoft.com/.default",
    grant_type: "client_credentials",
  });
  const response = await fetch(`https://login.microsoftonline.com/${encodeURIComponent(tenantId)}/oauth2/v2.0/token`, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body,
  });
  const payload = await response.json<Record<string, any>>().catch(() => ({}));
  if (!response.ok || !payload.access_token) throw new Error(payload.error_description || payload.error || `Graph token failed ${response.status}`);
  graphTokenCache = { token: payload.access_token, expiresAt: now + Number(payload.expires_in || 3300) * 1000 };
  return graphTokenCache.token;
}

async function graph(env: Env, path: string, init: RequestInit = {}) {
  const sender = clean(env.M365_SENDER);
  if (!sender) throw new Error("M365 sender is not configured.");
  const token = await getGraphToken(env);
  const url = `https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}${path}`;
  const response = await fetch(url, { ...init, headers: { authorization: `Bearer ${token}`, accept: "application/json", ...(init.headers || {}) } });
  const text = await response.text();
  let body: any = null;
  if (text) { try { body = JSON.parse(text); } catch { body = text; } }
  if (!response.ok) throw new Error(typeof body === "string" ? body : (body?.error?.message || `Graph ${response.status} for ${path}`));
  return { status: response.status, body };
}

async function listFolder(env: Env, folder: "drafts" | "sentitems") {
  const select = "$select=id,subject,toRecipients,sentDateTime,createdDateTime";
  const order = folder === "sentitems" ? "&$orderby=sentDateTime desc" : "&$orderby=createdDateTime desc";
  const res = await graph(env, `/mailFolders/${folder}/messages?$top=80&${select}${order}`);
  return (res.body?.value || []) as any[];
}

function msgToAddresses(msg: any): string[] {
  return (msg.toRecipients || []).map((r: any) => norm(r?.emailAddress?.address || "")).filter(Boolean);
}

function matches(msg: any, expected: typeof EXPECTED[number]) {
  return msg.subject === expected.subject && msgToAddresses(msg).includes(norm(expected.to));
}

async function verify(env: Env) {
  const [drafts, sent] = await Promise.all([listFolder(env, "drafts"), listFolder(env, "sentitems")]);
  return EXPECTED.map((expected) => ({
    customer: expected.customer,
    to: expected.to,
    subject: expected.subject,
    draftRemaining: drafts.some((m) => matches(m, expected)),
    sentFound: sent.some((m) => matches(m, expected)),
    sentAt: sent.find((m) => matches(m, expected))?.sentDateTime || null,
  }));
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  try {
    const payload = await context.request.json<any>().catch(() => ({}));
    if (payload.key !== APPROVAL_KEY) return new Response(JSON.stringify({ ok: false, error: "unauthorized" }), { status: 401, headers: jsonHeaders });
    const action = payload.action || "send";
    if (action === "verify") {
      return new Response(JSON.stringify({ ok: true, verification: await verify(context.env) }, null, 2), { headers: jsonHeaders });
    }

    const drafts = await listFolder(context.env, "drafts");
    const sentBefore = await listFolder(context.env, "sentitems");
    const results: any[] = [];

    for (const expected of EXPECTED) {
      if (sentBefore.some((m) => matches(m, expected))) {
        results.push({ ...expected, status: "already-sent-before-this-run" });
        continue;
      }
      const draft = drafts.find((m) => matches(m, expected));
      if (!draft?.id) {
        results.push({ ...expected, status: "draft-not-found" });
        continue;
      }
      await graph(context.env, `/messages/${encodeURIComponent(draft.id)}/send`, { method: "POST" });
      results.push({ ...expected, status: "send-called", draftId: draft.id });
    }

    let verification = await verify(context.env);
    for (let i = 0; i < 4 && verification.some((v) => !v.sentFound); i++) {
      await sleep(1500);
      verification = await verify(context.env);
    }

    return new Response(JSON.stringify({ ok: true, results, verification }, null, 2), { headers: jsonHeaders });
  } catch (error: any) {
    return new Response(JSON.stringify({ ok: false, error: error?.message || String(error) }, null, 2), { status: 500, headers: jsonHeaders });
  }
};

export const onRequestGet: PagesFunction<Env> = async () => new Response(JSON.stringify({ ok: false, error: "POST required" }), { status: 405, headers: jsonHeaders });

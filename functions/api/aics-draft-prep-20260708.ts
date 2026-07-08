type DraftEnv = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type TokenCache = { token: string; expiresAt: number };
let tokenCache: TokenCache | null = null;

const DRAFT_KEY = "aics-draft-prep-20260708-raj-approved-c0a7b7e9";

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

const clean = (value: unknown) => String(value ?? "").trim();

async function getToken(env: DraftEnv): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("M365 Graph credentials are missing.");

  const now = Date.now();
  if (tokenCache && tokenCache.expiresAt - 60_000 > now) return tokenCache.token;

  const body = new URLSearchParams({
    grant_type: "client_credentials",
    client_id: clientId,
    client_secret: clientSecret,
    scope: "https://graph.microsoft.com/.default",
  });

  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  const payload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !payload.access_token) throw new Error(payload.error_description || payload.error || `Token request failed: ${response.status}`);

  tokenCache = { token: payload.access_token, expiresAt: now + Math.max(60, payload.expires_in || 3600) * 1000 };
  return tokenCache.token;
}

async function graph(env: DraftEnv, path: string, init: RequestInit = {}) {
  const sender = clean(env.M365_SENDER);
  if (!sender) throw new Error("M365_SENDER is missing.");
  const token = await getToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });
  const text = await response.text();
  let data: unknown = text;
  try { data = text ? JSON.parse(text) : null; } catch {}
  if (!response.ok) throw new Error(`Graph ${init.method || "GET"} ${path} failed ${response.status}: ${text.slice(0, 500)}`);
  return { status: response.status, data };
}

async function listDrafts(env: DraftEnv) {
  const out: Array<{ id: string; subject?: string; toRecipients?: unknown; createdDateTime?: string }> = [];
  let path = "/mailFolders/drafts/messages?$top=50&$select=id,subject,toRecipients,createdDateTime";
  for (let i = 0; i < 10 && path; i++) {
    const res = await graph(env, path);
    const data = res.data as { value?: Array<{ id: string; subject?: string; toRecipients?: unknown; createdDateTime?: string }>; "@odata.nextLink"?: string };
    out.push(...(data.value || []));
    const next = data["@odata.nextLink"];
    path = next ? next.replace(/^https:\/\/graph\.microsoft\.com\/v1\.0\/users\/[^/]+/, "") : "";
  }
  return out;
}

function htmlShell(title: string, body: string) {
  return `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#172033;max-width:680px">
<p>Hi ${title},</p>
${body}
<p style="margin-top:22px">Warmly,<br><strong>Anushka Bhattacharya</strong><br>Director, AICloudStrategist<br><a href="https://aicloudstrategist.com">aicloudstrategist.com</a><br>WhatsApp: +91 87963 02608</p>
</div>`;
}

const drafts = [
  {
    to: "prashant@facets.cloud",
    name: "Prashant",
    subject: "Quick cloud cost/control snapshot for Facets.cloud",
    body: htmlShell("Prashant", `<p>I reviewed Facets.cloud from outside and saw a strong fit for a short, business-facing cloud cost and control diagnostic.</p>
<p>We help cloud/SaaS teams get a practical snapshot of where cloud spend, ownership, reliability responsibility, and executive visibility may be getting scattered as the platform grows.</p>
<p>This is not a long consulting engagement. It is a compact diagnostic with:</p>
<ul><li>cost/control leakage points,</li><li>ownership gaps,</li><li>quick-win recommendations, and</li><li>a 30-day action plan.</li></ul>
<p>If useful, I can share a one-page outline and you can decide if it is worth a short discussion.</p>`),
  },
  {
    to: "arman@sleepyowl.co",
    name: "Arman",
    subject: "Revenue leakage diagnostic idea for Sleepy Owl",
    body: htmlShell("Arman", `<p>I reviewed Sleepy Owl from outside and saw a possible fit for a short D2C revenue leakage diagnostic.</p>
<p>For D2C brands, small gaps between ads, website, subscriptions, WhatsApp/support, carts, repeat purchase follow-up, and owner visibility can quietly reduce revenue.</p>
<p>We map these gaps in simple business language and produce:</p>
<ul><li>where enquiries/orders may be leaking,</li><li>where customer follow-up can be tightened,</li><li>what can be fixed quickly, and</li><li>a 30-day action plan.</li></ul>
<p>Can I share a one-page outline for you to review?</p>`),
  },
  {
    to: "aditidentalcare@gmail.com",
    name: "Dr. Tripti",
    subject: "Clinic enquiry leakage check for Aditi Dental Care",
    body: htmlShell("Dr. Tripti", `<p>I reviewed Aditi Dental Care from outside. Many clinics lose potential appointments between Google search, website, phone/WhatsApp, and follow-up — especially for higher-value dental treatments.</p>
<p>We do a short Clinic Leakage Diagnostic that shows:</p>
<ul><li>where patient enquiries may be getting missed,</li><li>whether follow-up is visible to the owner/doctor,</li><li>simple trust and booking improvements, and</li><li>a practical 30-day fix plan.</li></ul>
<p>This is a small diagnostic, not a long project. If useful, I can share a one-page outline.</p>`),
  },
  {
    to: "chauhansdentalcare@gmail.com",
    name: "Dr. Vivek / Dr. Rashmi",
    subject: "Missed patient enquiry diagnostic for Chauhan's Dental Care",
    body: htmlShell("Dr. Vivek / Dr. Rashmi", `<p>I reviewed Chauhan's Dental Care from outside. Your clinic has multiple public contact routes, which is good — but it can also create missed enquiry and follow-up leakage if everything is not tracked clearly.</p>
<p>We run a short Clinic Leakage Diagnostic for owner-led clinics. It checks:</p>
<ul><li>Google/website/phone/WhatsApp enquiry flow,</li><li>missed-call and follow-up gaps,</li><li>booking friction for high-value treatments, and</li><li>a 30-day improvement plan.</li></ul>
<p>Can I share a one-page outline for your review?</p>`),
  },
  {
    to: "hamilton@vakilsearch.com",
    name: "Hamilton",
    subject: "Client enquiry leakage diagnostic for Vakilsearch",
    body: htmlShell("Hamilton", `<p>I reviewed Vakilsearch from outside and saw a possible fit for a short client enquiry and onboarding leakage diagnostic.</p>
<p>In legal/compliance services, revenue can leak between website forms, calls, WhatsApp/support, document collection, follow-up ownership, and client onboarding visibility.</p>
<p>Our diagnostic gives a practical snapshot of:</p>
<ul><li>where enquiries may be dropping,</li><li>where onboarding friction may delay conversion,</li><li>what should be tracked daily by the business owner/team, and</li><li>a 30-day action plan.</li></ul>
<p>If useful, I can share a one-page outline for review.</p>`),
  },
];

function requireKey(request: Request) {
  return request.headers.get("x-draft-key") === DRAFT_KEY;
}

export const onRequestGet: PagesFunction<DraftEnv> = async (context) => {
  if (!requireKey(context.request)) return new Response(JSON.stringify({ ok: false }), { status: 404, headers });
  try {
    const existing = await listDrafts(context.env);
    return new Response(JSON.stringify({ ok: true, count: existing.length, drafts: existing.map((d) => ({ id: d.id, subject: d.subject, toRecipients: d.toRecipients })) }), { headers });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers });
  }
};

export const onRequestPost: PagesFunction<DraftEnv> = async (context) => {
  if (!requireKey(context.request)) return new Response(JSON.stringify({ ok: false }), { status: 404, headers });
  try {
    const before = await listDrafts(context.env);
    const deleted: string[] = [];
    for (const draft of before) {
      await graph(context.env, `/messages/${draft.id}`, { method: "DELETE" });
      deleted.push(draft.id);
    }

    const created = [] as Array<{ id?: string; subject: string; to: string; status: number }>;
    for (const draft of drafts) {
      const res = await graph(context.env, "/messages", {
        method: "POST",
        body: JSON.stringify({
          subject: draft.subject,
          importance: "normal",
          body: { contentType: "HTML", content: draft.body },
          toRecipients: [{ emailAddress: { address: draft.to, name: draft.name } }],
        }),
      });
      const data = res.data as { id?: string };
      created.push({ id: data.id, subject: draft.subject, to: draft.to, status: res.status });
    }

    const after = await listDrafts(context.env);
    return new Response(JSON.stringify({ ok: true, deleted_count: deleted.length, created_count: created.length, created, after_count: after.length }), { headers });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers });
  }
};

type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type Prospect = { id: string; name: string; to: string; subject: string; body: string; route: string };

const TOKEN = "aics-20260710-cron-9f2b7b8c-owner-clinic-low-volume";

const prospects: Prospect[] = [
  {
    id: "AICS-MIX-001",
    name: "Recreate Dental & Implant Center",
    to: "recreatedental2010@gmail.com",
    route: "direct public clinic Gmail from official website/contact page",
    subject: "Small Recreate Dental enquiry leakage note?",
    body: `Hi Recreate Dental team,

I noticed your clinic has a long-running Indirapuram presence, high-value implant/full-mouth treatments, and multiple patient entry points: Google, website, phone and appointment requests.

For owner-led dental clinics, the expensive leak is usually not marketing. It is simpler: a serious implant/full-mouth patient asks once, the team responds, but nobody can later see whether that enquiry was followed up, booked, priced, or quietly lost.

AICloudStrategist helps clinics map this in plain language: where enquiries come from, what happens next, and a simple owner dashboard for missed follow-ups. No medical claims, no fake case studies, no disruption to your clinic.

If useful, I can send a one-page Recreate-specific leakage note. If you later want a paid diagnostic, it is usually ₹25k-₹75k depending on scope.

Regards,
AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com/healthcare-growthos/`
  },
  {
    id: "AICS-MIX-002",
    name: "32 Smiles Multispeciality Dental Clinics",
    to: "32smilesbangalore@gmail.com",
    route: "public clinic Gmail from official contact page; founder Dr. Naveen Indla named on homepage title",
    subject: "32 Smiles: quick appointment leakage check?",
    body: `Hi Dr. Naveen / 32 Smiles team,

I saw 32 Smiles highlights implants, cosmetic cases, aligners, multiple branches and appointment links. With that many patient routes, a small hidden leak can become costly: a patient asks on WhatsApp/call/site, but the owner cannot quickly see which enquiries were called back, booked, quoted, or dropped.

AICloudStrategist helps clinics create a simple enquiry-leakage map and owner view across Google, website, WhatsApp/calls and follow-up. It is business follow-up visibility only — no medical outcome claims and no disruption to treatment workflows.

If useful, I can send a short 32 Smiles-specific note showing where appointment-ready patients may slip. Paid diagnostic, only if you want to go deeper, is ₹25k-₹75k based on scope.

Regards,
AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com/healthcare-growthos/`
  },
  {
    id: "AICS-MIX-005",
    name: "Dental Inn",
    to: "info@dentalinnclinic.com",
    route: "public clinic email on official contact page; contact form showed Cloudflare/Turnstile widget, so direct public email used",
    subject: "Dental Inn: Baner follow-up visibility note",
    body: `Hi Dental Inn team,

I noticed your site explains a clear 4-step appointment journey and uses WhatsApp/call booking for patients in Baner. For clinics like this, a common leak is simple: a patient asks about pain, aligners or RCT, but later nobody can easily see which enquiry got called back, quoted, booked, or went quiet.

AICloudStrategist helps owner-led clinics build a small enquiry-leakage diagnostic: Google/website/WhatsApp/call follow-up mapped in plain language, then a simple owner dashboard. No medical claims, no disruption — just visibility into where appointment-ready patients may be slipping.

If useful, I can send a one-page Dental Inn-specific leakage note. Paid diagnostic, if you want it after seeing the note, is ₹25k-₹75k depending on scope.

Regards,
AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com/healthcare-growthos/`
  }
];

const clean = (v: unknown) => String(v ?? "").trim();
let cached: { token: string; expiresAt: number } | null = null;

async function token(env: Env): Promise<string> {
  const tenant = clean(env.M365_TENANT_ID), client = clean(env.M365_CLIENT_ID), secret = clean(env.M365_CLIENT_SECRET);
  if (!tenant || !client || !secret) throw new Error("Graph credentials missing");
  const now = Date.now();
  if (cached && cached.expiresAt > now + 60000) return cached.token;
  const res = await fetch(`https://login.microsoftonline.com/${tenant}/oauth2/v2.0/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "client_credentials", client_id: client, client_secret: secret, scope: "https://graph.microsoft.com/.default" })
  });
  const data = await res.json() as { access_token?: string; expires_in?: number; error_description?: string; error?: string };
  if (!res.ok || !data.access_token) throw new Error(data.error_description || data.error || `token ${res.status}`);
  cached = { token: data.access_token, expiresAt: now + (data.expires_in || 3600) * 1000 };
  return cached.token;
}

async function graph(env: Env, path: string, init?: RequestInit) {
  const sender = clean(env.M365_SENDER);
  if (!sender) throw new Error("M365 sender missing");
  const t = await token(env);
  return fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}${path}`, { ...init, headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json", ...(init?.headers || {}) } });
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  if (request.headers.get("x-aics-token") !== TOKEN) return new Response(JSON.stringify({ ok: false, error: "not found" }), { status: 404 });
  const dry = new URL(request.url).searchParams.get("dry") === "1";
  const sentAt = new Date().toISOString();
  const results = [];
  for (const p of prospects) {
    if (dry) { results.push({ ...p, body: undefined, dry: true }); continue; }
    const body = {
      message: {
        subject: p.subject,
        body: { contentType: "Text", content: p.body },
        toRecipients: [{ emailAddress: { address: p.to, name: p.name } }],
        replyTo: [{ emailAddress: { address: "contact@aicloudstrategist.com", name: "AICloudStrategist" } }],
        internetMessageHeaders: [{ name: "X-AICS-Lead-ID", value: p.id }]
      },
      saveToSentItems: true
    };
    const res = await graph(env, "/sendMail", { method: "POST", body: JSON.stringify(body) });
    const text = await res.text();
    results.push({ id: p.id, name: p.name, to: p.to, subject: p.subject, route: p.route, sentAt, sendStatus: res.status, graphAccepted: res.status === 202, response: text.slice(0, 300) });
  }
  return new Response(JSON.stringify({ ok: results.every((r: any) => r.dry || r.graphAccepted), sentAt, results }, null, 2), { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
};

export const onRequestGet: PagesFunction = async () => new Response(JSON.stringify({ ok: true, endpoint: "temporary AICS cron outreach 2026-07-10", prospects: prospects.map(({ body, ...p }) => p) }, null, 2), { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });

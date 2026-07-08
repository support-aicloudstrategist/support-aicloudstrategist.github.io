type DraftEnv = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type TokenCache = { token: string; expiresAt: number };
let tokenCache: TokenCache | null = null;

const DRAFT_KEY = "aics-infographic-drafts-20260708-raj-approved-7d31ef";

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

  const body = new URLSearchParams({ grant_type: "client_credentials", client_id: clientId, client_secret: clientSecret, scope: "https://graph.microsoft.com/.default" });
  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
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
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", ...(init.headers || {}) },
  });
  const text = await response.text();
  let data: unknown = text;
  try { data = text ? JSON.parse(text) : null; } catch {}
  if (!response.ok) throw new Error(`Graph ${init.method || "GET"} ${path} failed ${response.status}: ${text.slice(0, 700)}`);
  return { status: response.status, data };
}

async function listFolderMessages(env: DraftEnv, folder: "drafts" | "sentitems", top = 100) {
  const out: Array<{ id: string; subject?: string; toRecipients?: Array<{ emailAddress?: { address?: string; name?: string } }>; createdDateTime?: string; sentDateTime?: string }> = [];
  let path = `/mailFolders/${folder}/messages?$top=${top}&$select=id,subject,toRecipients,createdDateTime,sentDateTime`;
  for (let i = 0; i < 12 && path; i++) {
    const res = await graph(env, path);
    const data = res.data as { value?: typeof out; "@odata.nextLink"?: string };
    out.push(...(data.value || []));
    const next = data["@odata.nextLink"];
    path = next ? next.replace(/^https:\/\/graph\.microsoft\.com\/v1\.0\/users\/[^/]+/, "") : "";
  }
  return out;
}

const selected = [
  "prashant@facets.cloud",
  "arman@sleepyowl.co",
  "aditidentalcare@gmail.com",
  "chauhansdentalcare@gmail.com",
  "hamilton@vakilsearch.com",
];

function emailBase(preheader: string, inner: string) {
  return `<!doctype html><html><body style="margin:0;padding:0;background:#f6f9fc;font-family:Arial,Helvetica,sans-serif;color:#172033;">
<div style="display:none;max-height:0;overflow:hidden;color:transparent;opacity:0;">${preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f9fc;padding:24px 0;"><tr><td align="center">
<table role="presentation" width="680" cellpadding="0" cellspacing="0" style="width:680px;max-width:94%;background:#ffffff;border:1px solid #e5edf5;border-radius:18px;overflow:hidden;box-shadow:0 24px 60px rgba(50,50,93,.18),0 12px 28px rgba(0,0,0,.08);">
${inner}
<tr><td style="padding:24px 32px 30px;background:#061b31;color:#d9e7ff;">
<div style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#9ec1ff;margin-bottom:8px;">AICloudStrategist</div>
<div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:6px;">Growth, trust and control systems for owner-led teams.</div>
<div style="font-size:14px;line-height:1.5;color:#c3d4ef;">Warmly,<br><strong style="color:#fff;">Anushka Bhattacharya</strong>, Director<br><a href="https://aicloudstrategist.com" style="color:#9ec1ff;text-decoration:none;">aicloudstrategist.com</a> · WhatsApp +91 87963 02608</div>
</td></tr>
</table>
</td></tr></table></body></html>`;
}

function hero(kicker: string, title: string, subtitle: string, accent = "#533afd") {
  return `<tr><td style="padding:34px 32px 22px;background:linear-gradient(135deg,#ffffff 0%,#f7f3ff 56%,#e8f2ff 100%);">
<div style="display:inline-block;background:${accent};color:#fff;border-radius:999px;padding:6px 11px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;">${kicker}</div>
<h1 style="margin:18px 0 10px;font-size:32px;line-height:1.08;font-weight:700;color:#061b31;letter-spacing:-.7px;">${title}</h1>
<p style="margin:0;font-size:17px;line-height:1.5;color:#4f6077;">${subtitle}</p>
</td></tr>`;
}
function stat(label: string, value: string, color = "#533afd") { return `<td style="padding:12px;width:33.33%;vertical-align:top;"><div style="border:1px solid #e5edf5;border-radius:14px;padding:14px;background:#fff;"><div style="font-size:25px;font-weight:800;color:${color};line-height:1;">${value}</div><div style="font-size:12px;line-height:1.25;color:#64748d;margin-top:7px;">${label}</div></div></td>`; }
function issue(title: string, text: string) { return `<tr><td style="padding:10px 0;border-bottom:1px solid #edf2f7;"><strong style="color:#061b31;">${title}</strong><br><span style="color:#5d6c82;font-size:14px;line-height:1.45;">${text}</span></td></tr>`; }
function step(n: string, title: string, text: string) { return `<td style="padding:10px;vertical-align:top;width:33.33%;"><div style="height:100%;border:1px solid #d6d9fc;border-radius:14px;padding:14px;background:#fbfbff;"><div style="width:28px;height:28px;border-radius:50%;background:#533afd;color:#fff;text-align:center;line-height:28px;font-weight:800;margin-bottom:10px;">${n}</div><strong style="color:#061b31;">${title}</strong><div style="font-size:13px;line-height:1.45;color:#64748d;margin-top:5px;">${text}</div></div></td>`; }
function cta(text: string) { return `<tr><td style="padding:18px 32px 30px;"><div style="border-left:4px solid #533afd;background:#f7f5ff;border-radius:12px;padding:16px 18px;color:#273951;font-size:15px;line-height:1.5;">${text}</div></td></tr>`; }

const drafts = [
  {
    id: "facets-cloud",
    account: "Facets.cloud",
    to: "prashant@facets.cloud",
    name: "Prashant Dhanke",
    subject: "Facets.cloud: a 30-day cloud control snapshot for platform growth",
    body: emailBase("A compact cloud cost/control diagnostic shaped for a platform engineering company.",
      hero("Cloud Control Snapshot", "Facets.cloud may already solve platform complexity for customers — the hidden risk is internal cost/control drift while scaling.", "A short diagnostic can turn cloud spend, ownership and reliability responsibility into a clear founder/leadership control view.") +
      `<tr><td style="padding:22px 32px 8px;"><p style="font-size:16px;line-height:1.55;color:#344055;margin:0;">Hi Prashant, I reviewed Facets.cloud from outside. Because your business sits around software delivery and cloud/platform orchestration, the most relevant problem is not generic “cloud consulting” — it is <strong>control clarity as environments, customers and delivery responsibility grow</strong>.</p></td></tr>
<tr><td style="padding:12px 20px;"><table width="100%" role="presentation"><tr>${stat("Cost ownership visible by product/customer", "₹/$", "#533afd")}${stat("Delivery reliability tied to business owner", "SLO", "#ea2261")}${stat("30-day control actions", "30", "#108c3d")}</tr></table></td></tr>
<tr><td style="padding:10px 32px;"><table width="100%" role="presentation" style="border-collapse:collapse;">${issue("Likely leakage", "Cloud cost, reliability and environment ownership can become scattered across engineering, DevOps and customer success as the platform scales.")}${issue("Business impact", "Leadership sees infrastructure spend and reliability as totals, but not always as customer/product-level decisions.")}${issue("AICS diagnostic", "We build a compact cost/control map, owner dashboard requirements, and a 30-day action plan without disrupting your engineering team.")}</table></td></tr>
<tr><td style="padding:12px 22px;"><table width="100%" role="presentation"><tr>${step("1","Map","Cloud spend/control signals by environment and owner.")}${step("2","Find","Gaps where cost, reliability or escalation responsibility is unclear.")}${step("3","Fix","30-day control board and decision cadence for leadership.")}</tr></table></td></tr>` + cta("If useful, I can share the one-page diagnostic outline. If it does not map to a current pain, you can ignore it.")),
  },
  {
    id: "sleepy-owl",
    account: "Sleepy Owl Coffee",
    to: "arman@sleepyowl.co",
    name: "Arman Sood",
    subject: "Sleepy Owl: where D2C revenue may leak after the first click",
    body: emailBase("A D2C revenue leakage map for coffee subscriptions, carts, support and repeat purchase.",
      hero("D2C Revenue Leakage Map", "Sleepy Owl’s real growth leak may not be traffic — it may be what happens after a customer shows buying intent.", "We map the post-click path across product pages, carts, subscriptions, support and repeat purchase follow-up.", "#ea2261") +
      `<tr><td style="padding:22px 32px 8px;"><p style="font-size:16px;line-height:1.55;color:#344055;margin:0;">Hi Arman, I reviewed Sleepy Owl from outside. For a D2C coffee brand, a generic marketing email is not useful. The sharper issue is <strong>lost revenue between discovery, trial, repeat purchase and subscription habit</strong>.</p></td></tr>
<tr><td style="padding:12px 20px;"><table width="100%" role="presentation"><tr>${stat("Cart / checkout friction", "Cart", "#ea2261")}${stat("Subscription & repeat purchase nudges", "Repeat", "#533afd")}${stat("Support-to-sale follow-up", "Care", "#108c3d")}</tr></table></td></tr>
<tr><td style="padding:10px 32px;"><table width="100%" role="presentation" style="border-collapse:collapse;">${issue("Likely leakage", "Customers may browse blends, packs or subscriptions but drop when questions, delivery concerns or habit reminders are not handled at the right moment.")}${issue("Business impact", "Paid traffic and brand love can still underperform if support, subscription prompts and reorder flows are not visible as one revenue system.")}${issue("AICS diagnostic", "We create a revenue-leakage board that shows where buyers stall, what follow-up is missing, and what to fix first in 30 days.")}</table></td></tr>
<tr><td style="padding:12px 22px;"><table width="100%" role="presentation"><tr>${step("1","Trace","Ad/site/product/cart/support path from first interest to repeat order.")}${step("2","Score","Identify the highest-value drop-offs and response gaps.")}${step("3","Recover","30-day fixes for follow-up, reorder and subscription conversion.")}</tr></table></td></tr>` + cta("Can I share a one-page revenue leakage outline for Sleepy Owl? It will be practical, not a long proposal.")),
  },
  {
    id: "aditi-dental",
    account: "Aditi Dental Care",
    to: "aditidentalcare@gmail.com",
    name: "Dr. Tripti",
    subject: "Aditi Dental Care: missed appointment leakage between Google, calls and follow-up",
    body: emailBase("A clinic enquiry leakage diagnostic for Sarjapur dental enquiries and high-value treatment follow-up.",
      hero("Clinic Leakage Diagnostic", "Aditi Dental Care has strong doctor credibility — the revenue risk is missed visibility after a patient enquiry starts.", "We check where dental enquiries may get lost between Google, website, calls, WhatsApp and treatment follow-up.", "#15be53") +
      `<tr><td style="padding:22px 32px 8px;"><p style="font-size:16px;line-height:1.55;color:#344055;margin:0;">Hi Dr. Tripti, I reviewed Aditi Dental Care from outside and saw your strong positioning as an experienced multi-speciality dental clinic. The practical growth issue for clinics like yours is often <strong>not more ads first</strong> — it is making sure every high-intent patient enquiry becomes visible and followed up.</p></td></tr>
<tr><td style="padding:12px 20px;"><table width="100%" role="presentation"><tr>${stat("Google / website enquiry capture", "Lead", "#15be53")}${stat("Call + WhatsApp follow-up visibility", "Follow", "#533afd")}${stat("High-value treatment conversion", "Care", "#ea2261")}</tr></table></td></tr>
<tr><td style="padding:10px 32px;"><table width="100%" role="presentation" style="border-collapse:collapse;">${issue("Likely leakage", "Patients may call, WhatsApp or submit interest, but the doctor/owner may not get a daily view of missed calls, pending replies and treatment follow-ups.")}${issue("Business impact", "Implants, aligners, RCT, cosmetic and multi-visit cases can be lost if follow-up is delayed or not owned clearly.")}${issue("AICS diagnostic", "We review enquiry routes from outside, map follow-up gaps, and give a 30-day clinic owner dashboard/fix plan.")}</table></td></tr>
<tr><td style="padding:12px 22px;"><table width="100%" role="presentation"><tr>${step("1","Check","Google, website, phone and WhatsApp enquiry path.")}${step("2","Expose","Missed-call, slow-reply and pending-treatment gaps.")}${step("3","Improve","Simple daily owner view and 30-day follow-up fixes.")}</tr></table></td></tr>` + cta("If useful, I can share a one-page Clinic Leakage Diagnostic outline for Aditi Dental Care.")),
  },
  {
    id: "chauhans-dental",
    account: "Chauhan's Dental Care",
    to: "chauhansdentalcare@gmail.com",
    name: "Dr. Vivek / Dr. Rashmi",
    subject: "Chauhan’s Dental Care: turning multiple enquiry channels into booked appointments",
    body: emailBase("A multi-channel patient enquiry leakage diagnostic for Chauhan’s Dental Care.",
      hero("Multi-Channel Clinic Map", "Multiple phone/WhatsApp routes are useful — but they can also hide missed patient enquiries unless tracked clearly.", "A short diagnostic can show where booking intent is leaking and what the clinic owner should see daily.", "#533afd") +
      `<tr><td style="padding:22px 32px 8px;"><p style="font-size:16px;line-height:1.55;color:#344055;margin:0;">Hi Dr. Vivek / Dr. Rashmi, I reviewed Chauhan’s Dental Care from outside. You already have strong doctor-led credibility and multiple contact numbers. The sharp business problem is <strong>channel leakage</strong>: when Google, website, phone and WhatsApp enquiries are split, some high-intent patients may not get the right follow-up.</p></td></tr>
<tr><td style="padding:12px 20px;"><table width="100%" role="presentation"><tr>${stat("Multiple public numbers", "3+", "#533afd")}${stat("Booking intent needing owner view", "Daily", "#ea2261")}${stat("30-day appointment recovery plan", "30", "#108c3d")}</tr></table></td></tr>
<tr><td style="padding:10px 32px;"><table width="100%" role="presentation" style="border-collapse:collapse;">${issue("Likely leakage", "Patients may choose different phone/WhatsApp routes. Without one clear view, missed calls and delayed replies can stay invisible.")}${issue("Business impact", "High-value dental cases need timely follow-up, reassurance and booking discipline; otherwise patients compare and book elsewhere.")}${issue("AICS diagnostic", "We map every public enquiry route, find response gaps, and create a simple owner-level appointment recovery board.")}</table></td></tr>
<tr><td style="padding:12px 22px;"><table width="100%" role="presentation"><tr>${step("1","Route","Map every public phone, WhatsApp, website and Google path.")}${step("2","Measure","Find where calls/replies/follow-ups go missing.")}${step("3","Recover","Owner dashboard and 30-day appointment recovery actions.")}</tr></table></td></tr>` + cta("Can I share a one-page diagnostic outline specific to Chauhan’s Dental Care?")),
  },
  {
    id: "vakilsearch",
    account: "Vakilsearch",
    to: "hamilton@vakilsearch.com",
    name: "Hamilton Manoraj",
    subject: "Vakilsearch: reducing client drop-off between enquiry and document completion",
    body: emailBase("A client enquiry and onboarding leakage diagnostic for legal/compliance services.",
      hero("Client Onboarding Leakage", "For legal/compliance services, the leak is often not demand — it is the handoff from enquiry to documents, payment and case progress.", "We map where client intent slows down across forms, calls, support, document collection and follow-up ownership.", "#0d5bd7") +
      `<tr><td style="padding:22px 32px 8px;"><p style="font-size:16px;line-height:1.55;color:#344055;margin:0;">Hi Hamilton, I reviewed Vakilsearch from outside. The practical issue I would not pitch as generic automation. For a legal/compliance service, the core problem is likely <strong>client drop-off between first enquiry and completed onboarding</strong>.</p></td></tr>
<tr><td style="padding:12px 20px;"><table width="100%" role="presentation"><tr>${stat("Form/call/support handoffs", "Flow", "#0d5bd7")}${stat("Document collection friction", "Docs", "#ea2261")}${stat("Owner view of stuck cases", "View", "#108c3d")}</tr></table></td></tr>
<tr><td style="padding:10px 32px;"><table width="100%" role="presentation" style="border-collapse:collapse;">${issue("Likely leakage", "Prospects can start with intent but slow down during qualification, document collection, payment, clarification or support handoff.")}${issue("Business impact", "Even a small improvement in stuck-client recovery can lift conversion without increasing acquisition spend.")}${issue("AICS diagnostic", "We build a leakage map of enquiry-to-onboarding, identify owner-visible stuck points, and suggest 30-day recovery actions.")}</table></td></tr>
<tr><td style="padding:12px 22px;"><table width="100%" role="presentation"><tr>${step("1","Map","Enquiry, qualification, docs, payment and support handoffs.")}${step("2","Locate","Where high-intent clients get stuck or delayed.")}${step("3","Recover","30-day stuck-client visibility and follow-up plan.")}</tr></table></td></tr>` + cta("If useful, I can share the one-page Client Onboarding Leakage outline for review.")),
  },
];

function recipientsOf(msg: { toRecipients?: Array<{ emailAddress?: { address?: string } }> }) {
  return (msg.toRecipients || []).map((r) => clean(r.emailAddress?.address).toLowerCase()).filter(Boolean);
}

function matchesSelected(msg: { subject?: string; toRecipients?: Array<{ emailAddress?: { address?: string } }> }) {
  const to = recipientsOf(msg);
  return selected.some((s) => to.includes(s));
}

async function run(context: EventContext<DraftEnv, string, unknown>) {
  const existingDrafts = await listFolderMessages(context.env, "drafts", 50);
  const deleted: Array<{ id: string; subject?: string }> = [];
  for (const d of existingDrafts) {
    await graph(context.env, `/messages/${d.id}`, { method: "DELETE" });
    deleted.push({ id: d.id, subject: d.subject });
  }

  const sent = await listFolderMessages(context.env, "sentitems", 100);
  const sentMatches = sent.filter(matchesSelected).map((m) => ({ subject: m.subject, sentDateTime: m.sentDateTime, to: recipientsOf(m) }));
  const sentAddresses = new Set(sentMatches.flatMap((m) => m.to));
  const eligible = drafts.filter((d) => !sentAddresses.has(d.to.toLowerCase()));
  const skipped = drafts.filter((d) => sentAddresses.has(d.to.toLowerCase())).map((d) => ({ account: d.account, to: d.to, reason: "already found in Sent Items" }));

  const created: Array<{ id?: string; account: string; to: string; subject: string; status: number }> = [];
  for (const d of eligible) {
    const res = await graph(context.env, "/messages", { method: "POST", body: JSON.stringify({ subject: d.subject, importance: "normal", body: { contentType: "HTML", content: d.body }, toRecipients: [{ emailAddress: { address: d.to, name: d.name } }] }) });
    const data = res.data as { id?: string };
    created.push({ id: data.id, account: d.account, to: d.to, subject: d.subject, status: res.status });
  }
  const afterDrafts = await listFolderMessages(context.env, "drafts", 50);
  return { deleted_count: deleted.length, deleted, sent_checked_count: sent.length, sent_matches: sentMatches, skipped, created_count: created.length, created, after_drafts_count: afterDrafts.length, after_drafts: afterDrafts.map((d) => ({ id: d.id, subject: d.subject, to: recipientsOf(d) })) };
}

function requireKey(request: Request) { return request.headers.get("x-draft-key") === DRAFT_KEY; }

export const onRequestGet: PagesFunction<DraftEnv> = async (context) => {
  if (!requireKey(context.request)) return new Response(JSON.stringify({ ok: false }), { status: 404, headers });
  try {
    const draftsNow = await listFolderMessages(context.env, "drafts", 50);
    return new Response(JSON.stringify({ ok: true, drafts_count: draftsNow.length, drafts: draftsNow.map((d) => ({ subject: d.subject, to: recipientsOf(d) })) }), { headers });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers });
  }
};

export const onRequestPost: PagesFunction<DraftEnv> = async (context) => {
  if (!requireKey(context.request)) return new Response(JSON.stringify({ ok: false }), { status: 404, headers });
  try { return new Response(JSON.stringify({ ok: true, ...(await run(context)) }), { headers }); }
  catch (error) { return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers }); }
};

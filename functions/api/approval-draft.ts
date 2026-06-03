type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

const clean = (value: unknown) => String(value ?? "").trim();
const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");
  const body = new URLSearchParams({ grant_type: "client_credentials", client_id: clientId, client_secret: clientSecret, scope: "https://graph.microsoft.com/.default" });
  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
  const payload = (await response.json().catch(() => ({}))) as { access_token?: string; error_description?: string; error?: string };
  if (!response.ok || !payload.access_token) throw new Error(payload.error_description || payload.error || `Graph token failed ${response.status}`);
  return payload.access_token;
}

async function sendGraphMail(env: Env, subject: string, html: string) {
  const sender = clean(env.M365_SENDER || "contact@aicloudstrategist.com");
  const token = await getGraphToken(env);
  const message = {
    subject,
    body: { contentType: "HTML", content: html },
    toRecipients: [
      { emailAddress: { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" } },
      { emailAddress: { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" } },
    ],
    replyTo: [{ emailAddress: { address: sender, name: "AICloudStrategist" } }],
  };
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ message, saveToSentItems: true }),
  });
  const text = await response.text();
  if (!response.ok) throw new Error(text || `Graph sendMail failed ${response.status}`);
  return { status: response.status, sender };
}

function shell(title: string, label: string, accent: string, hero: string, intro: string, cards: string, cta: string, safe: string) {
  return `<!doctype html><html><body style="margin:0;padding:0;background:#eef4fb;font-family:Arial,sans-serif;"><div style="display:none;max-height:0;overflow:hidden;color:transparent;">Approval draft for Raj and Anushka. Not sent to customers.</div><table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#eef4fb;padding:24px 0;"><tr><td align="center"><table role="presentation" width="640" cellspacing="0" cellpadding="0" style="width:640px;max-width:96%;background:#fff;border-radius:26px;overflow:hidden;box-shadow:0 18px 50px rgba(15,23,42,.14);"><tr><td style="background:#071426;padding:18px 24px;color:#fff;"><table width="100%"><tr><td style="font-weight:800;font-size:18px;">AI<span style="color:#22d3ee;">Cloud</span>Strategist</td><td align="right" style="font-size:12px;color:#bfdbfe;">Approval draft · not sent to customers</td></tr></table></td></tr><tr><td><img src="${hero}" width="640" alt="${label}" style="display:block;width:100%;max-width:640px;height:auto;border:0;"></td></tr><tr><td style="padding:30px;background:linear-gradient(180deg,#ffffff,#f8fbff);"><div style="display:inline-block;background:${accent};color:#fff;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:8px 12px;border-radius:999px;">${label}</div><h1 style="font-size:31px;line-height:1.12;margin:16px 0 10px;color:#0f172a;">${title}</h1><p style="font-size:17px;line-height:1.55;margin:0;color:#334155;">${intro}</p><table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top:22px;"><tr><td style="padding:10px;background:#f0f9ff;border-radius:14px;color:#075985;font-size:13px;"><b>1</b><br>Show leakage/value</td><td width="10"></td><td style="padding:10px;background:#ecfdf5;border-radius:14px;color:#065f46;font-size:13px;"><b>2</b><br>Offer short review</td><td width="10"></td><td style="padding:10px;background:#f5f3ff;border-radius:14px;color:#5b21b6;font-size:13px;"><b>3</b><br>Ask permission</td></tr></table></td></tr><tr><td style="padding:8px 30px 6px;"><h2 style="font-size:22px;margin:0 0 12px;color:#0f172a;">Customized customer versions</h2>${cards}</td></tr><tr><td style="padding:14px 30px 26px;"><div style="border-left:5px solid ${accent};background:#f8fafc;border-radius:16px;padding:16px 18px;color:#334155;font-size:15px;line-height:1.55;"><b>Safe proof/value line:</b> ${safe}</div></td></tr><tr><td align="center" style="padding:0 30px 30px;"><a href="https://aicloudstrategist.com/free-business-review/" style="background:${accent};color:#fff;text-decoration:none;font-weight:800;padding:15px 24px;border-radius:999px;display:inline-block;">${cta}</a><p style="font-size:12px;color:#64748b;line-height:1.5;margin:16px 0 0;">Approval note: after Raj/Anushka approval, customer versions will be sent individually with organisation name, segment, city, and one visible observation. No bulk generic send.</p></td></tr><tr><td style="background:#071426;color:#cbd5e1;padding:20px 30px;font-size:13px;line-height:1.55;">Anushka Bhattacharya · Director, AICloudStrategist<br>contact@aicloudstrategist.com · +91 87963 02608 · <a href="https://aicloudstrategist.com" style="color:#67e8f9;">aicloudstrategist.com</a></td></tr></table></td></tr></table></body></html>`;
}

const card = (label: string, subject: string, body: string, personalize: string, accent = "#0891b2") => `<div style="padding:14px 16px;border:1px solid #dbeafe;border-radius:16px;background:#fff;margin:0 0 12px;"><div style="font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:${accent};font-weight:800;">${label}</div><h3 style="font-size:20px;line-height:1.25;margin:8px 0;color:#0f172a;">${subject}</h3><p style="font-size:15px;line-height:1.55;margin:0 0 10px;color:#334155;">${body}</p><div style="font-size:13px;color:#475569;background:#f8fafc;border-radius:12px;padding:10px;">Personalize with: <b>${personalize}</b></div></div>`;

function healthcareHtml() {
  return shell("A visual Healthcare GrowthOS email system — customized by facility type", "Healthcare GrowthOS", "#0891b2", "https://aicloudstrategist.com/assets/openai/aics-owner-growth-dashboard-india.webp", "Professional hospital/clinic outreach should look like a mini business case: picture, problem, leakage, short review offer, and clear permission-based CTA.",
    card("Hospital / multi-speciality", "Reduce missed patient enquiries before they become lost revenue", "For a hospital, the first loss often happens after the patient checks services, calls once, sends a WhatsApp message, or compares reviews. We can review the public enquiry journey and show where appointments may be leaking.", "service line + appointment CTA + WhatsApp/call path")+
    card("Diagnostic lab", "Make test enquiries easier to capture, follow up, and convert", "For diagnostic labs, patients often need fast clarity on tests, home sample collection, reports, price confidence, and WhatsApp response. We can review the current path and suggest practical fixes.", "home collection, reports, test booking, location")+
    card("Dental / eye / skin / aesthetic clinic", "Turn high-intent treatment enquiries into booked consultations", "For specialty clinics, trust signals, before/after safety, doctor credibility, reviews, and fast follow-up strongly affect conversion. We can review the digital path and show 3–5 improvements.", "treatment category + reviews + consultation CTA")+
    card("IVF / fertility / wellness", "Build a calmer, trust-first journey for sensitive patient enquiries", "For sensitive healthcare decisions, patients need privacy, trust, clarity, and timely follow-up. We can review the public journey and identify gaps without touching internal patient data.", "privacy, doctor/facility trust, counselling CTA"),
    "Approve Healthcare Review Email", "Use conservative language: potential leakage, visible public journey, practical improvement points — no revenue guarantee and no patient-data access.");
}

function cloudHtml() {
  return shell("A visual Cloud Trust & FinOps email system — customized by company type", "Cloud Trust & FinOps", "#7c3aed", "https://aicloudstrategist.com/assets/openai/aics-cloud-security-trust-india.webp", "Cloud-heavy outreach should show value before price: cost leakage, governance, trust-readiness, and a short review before any paid proposal.",
    card("SaaS / AI startup", "Find cloud waste and trust gaps before enterprise buyers ask", "As product usage grows, cloud spend, access controls, AI governance, and buyer due-diligence questions become harder to manage. We can review public trust signals and suggest a practical operating layer.", "pricing page, status/trust page, cloud signals", "#7c3aed")+
    card("Fintech / regulated tech", "Strengthen cloud governance and buyer trust-readiness", "Fintech buyers and partners care about governance, access hygiene, audit readiness, operational continuity, and cost control. We can identify visible gaps and propose a safe first review path.", "risk/compliance page, security posture, cloud controls", "#7c3aed")+
    card("Healthtech", "Improve cloud trust signals without slowing product growth", "Healthtech teams face both growth and trust pressure: uptime, patient/data sensitivity, integrations, and buyer confidence. We can review public trust signals and cloud-cost leakage opportunities.", "health data sensitivity, integrations, trust pages", "#7c3aed")+
    card("Cloud-heavy services company", "Convert cloud operations into a visible control dashboard", "If cloud costs, manual operations, and ownership are spread across tools, leadership loses visibility. We can show a simple dashboard-led control model and where savings may exist.", "cloud stack, team workflow, spend visibility", "#7c3aed"),
    "Approve Cloud Review Email", "Use safe language: public trust signals, possible cost leakage, governance gaps, and measurable next steps only after baseline review.");
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const body = await context.request.json().catch(() => ({})) as { token?: string };
  if (body.token !== "aics-approval-draft-2026-06-03") return new Response(JSON.stringify({ ok: false, error: "not found" }), { status: 404, headers });
  const h = await sendGraphMail(context.env, "[APPROVAL DRAFT] Visual Healthcare GrowthOS outreach templates", healthcareHtml());
  const c = await sendGraphMail(context.env, "[APPROVAL DRAFT] Visual Cloud Trust & FinOps outreach templates", cloudHtml());
  return new Response(JSON.stringify({ ok: true, healthcare: h, cloud: c }), { status: 200, headers });
};

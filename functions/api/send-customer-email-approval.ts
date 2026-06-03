type Env = {
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const clean = (value: unknown) => String(value ?? "").trim();
const recipients = [
  { address: "rajivjobnaukri@gmail.com", name: "Rajiv Gupta" },
  { address: "bhattacharyaanushka01@gmail.com", name: "Anushka Bhattacharya" },
];

const drafts = [
  {
    approvalSubject: "Approval needed: production-ready customer email — Healthcare",
    customerSubject: "Are patient enquiries getting missed before they become appointments?",
    body: `Hi,

Many healthcare businesses lose good enquiries without noticing it.

A patient may visit your website, check reviews, call once, send a WhatsApp message, or look for appointment details. If the next step is not clear, or if follow-up is slow, that patient may quietly choose another clinic, lab, or hospital.

AICloudStrategist helps healthcare businesses improve this journey.

We review what a patient sees before booking:

- Is the website clear and trustworthy?
- Is it easy to call, WhatsApp, or book?
- Are important services explained properly?
- Are reviews, doctor details, timings, and location easy to find?
- Are enquiries followed up before they go cold?

After the review, we share practical improvement points that can help your team get better value from the enquiries you are already receiving.

This is not a long technical audit. It is a business review focused on missed enquiries, patient trust, and appointment conversion.

If you would like, we can do a quick review of your website and patient enquiry journey.

You can reply to this email, or visit:

https://aicloudstrategist.com/healthcare-growthos/

Regards,
Anushka Bhattacharya
Director, AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com`,
  },
  {
    approvalSubject: "Approval needed: production-ready customer email — US cloud and tech",
    customerSubject: "Is your cloud bill growing without clear business control?",
    body: `Hi,

Many growing companies pay for cloud tools, servers, software, and AI systems every month, but the owner or leadership team may not have a clear view of what is useful, what is wasted, and what needs attention.

The problem usually looks like this:

- Cloud bills keep increasing.
- Different teams manage different tools.
- No one has one clear business view.
- Some services may be unused or over-sized.
- Buyer or investor questions take too long to answer.
- Important risks are noticed late.

AICloudStrategist helps businesses bring this under control.

We review your public business setup and cloud/control signals, then help identify practical areas where the company may be losing money, time, or clarity.

The goal is simple:

- reduce avoidable waste
- improve owner-level visibility
- make cloud and AI systems easier to manage
- prepare better answers for customers, buyers, partners, or investors
- create a clearer growth and control system for the business

This is not a technical report for engineers only. It is a business review for leadership teams that want better control over cost, systems, and growth.

If you would like, we can do a short first review and share the main improvement areas.

You can reply to this email, or visit:

https://aicloudstrategist.com/growth-control-os/

Regards,
Anushka Bhattacharya
Director, AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com`,
  },
  {
    approvalSubject: "Approval needed: production-ready customer email — Global business owners",
    customerSubject: "Are you losing enquiries, time, or money because systems are not connected?",
    body: `Hi,

Many businesses are working hard to get leads, serve customers, manage teams, and control costs. But the business still feels scattered.

Common problems are:

- enquiries come in but are not followed up properly
- website visitors do not take the next step
- team work is handled manually
- business tools are not connected
- reporting is not clear
- owners do not have one simple view of what is happening
- costs increase without clear control

AICloudStrategist helps businesses build a better Growth & Control system.

We look at your website, enquiry flow, follow-up process, business tools, and owner visibility. Then we show practical improvements that can help reduce leakage and improve control.

The aim is not to add more complexity.

The aim is to help your business:

- look more professional
- capture more enquiries
- follow up faster
- reduce wasted effort
- improve customer trust
- give leadership a clearer view

If you would like, we can do a short review and share the main areas where your business may be losing value.

You can reply to this email, or visit:

https://aicloudstrategist.com/growth-control-os/

Regards,
Anushka Bhattacharya
Director, AICloudStrategist
contact@aicloudstrategist.com
https://aicloudstrategist.com`,
  },
];

async function getGraphToken(env: Env): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Microsoft Graph credentials are not configured.");
  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) return graphTokenCache.token;
  const body = new URLSearchParams({ grant_type: "client_credentials", client_id: clientId, client_secret: clientSecret, scope: "https://graph.microsoft.com/.default" });
  const response = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
  const payload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !payload.access_token) throw new Error(payload.error_description || payload.error || `Graph token request failed with ${response.status}.`);
  graphTokenCache = { token: payload.access_token, expiresAt: now + Math.max(60, payload.expires_in || 3600) * 1000 };
  return graphTokenCache.token;
}

async function sendGraphMail(env: Env, message: Record<string, unknown>) {
  const sender = clean(env.M365_SENDER) || "contact@aicloudstrategist.com";
  const token = await getGraphToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ message, saveToSentItems: true }),
  });
  const responseText = await response.text();
  if (!response.ok) throw new Error(responseText || `Graph sendMail failed with ${response.status}.`);
  return { status: response.status, responseText };
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  try {
    const results = [];
    for (const draft of drafts) {
      const content = `Raj / Anushka,

Please approve this exact customer email. The customer-facing email starts after the line below. Only the recipient email address will change before customer send.

--- CUSTOMER EMAIL START ---
Subject: ${draft.customerSubject}

${draft.body}
--- CUSTOMER EMAIL END ---`;
      const result = await sendGraphMail(context.env, {
        subject: draft.approvalSubject,
        body: { contentType: "Text", content },
        toRecipients: recipients.map((emailAddress) => ({ emailAddress })),
        replyTo: [{ emailAddress: { address: "contact@aicloudstrategist.com", name: "AICloudStrategist" } }],
      });
      results.push({ subject: draft.approvalSubject, status: result.status });
    }
    return new Response(JSON.stringify({ ok: true, sender: clean(context.env.M365_SENDER) || "contact@aicloudstrategist.com", results }), { status: 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error instanceof Error ? error.message : String(error) }), { status: 500, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  }
};

export const onRequestGet: PagesFunction = async () => new Response(JSON.stringify({ ok: false, error: "not found" }), { status: 404, headers: { "Content-Type": "application/json" } });

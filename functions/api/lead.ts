type LeadEnv = {
  LEAD_LOG?: KVNamespace;
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
  M365_RECIPIENT?: string;
};

type GraphTokenCache = {
  token: string;
  expiresAt: number;
};

let graphTokenCache: GraphTokenCache | null = null;

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const clean = (value: unknown) => String(value ?? "").trim();

async function getGraphToken(env: LeadEnv): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);

  if (!tenantId || !clientId || !clientSecret) {
    throw new Error("Microsoft Graph credentials are not configured.");
  }

  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) {
    return graphTokenCache.token;
  }

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

  const tokenPayload = (await response.json().catch(() => ({}))) as { access_token?: string; expires_in?: number; error?: string; error_description?: string };
  if (!response.ok || !tokenPayload.access_token) {
    throw new Error(tokenPayload.error_description || tokenPayload.error || `Graph token request failed with ${response.status}.`);
  }

  graphTokenCache = {
    token: tokenPayload.access_token,
    expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000,
  };

  return graphTokenCache.token;
}

async function sendGraphMail(env: LeadEnv, graphMessage: Record<string, unknown>) {
  const sender = clean(env.M365_SENDER);
  if (!sender) {
    throw new Error("Microsoft Graph sender is not configured.");
  }

  const token = await getGraphToken(env);
  const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: graphMessage, saveToSentItems: true }),
  });

  const responseText = await response.text();
  if (!response.ok) {
    throw new Error(responseText || `Graph sendMail failed with ${response.status}.`);
  }

  return { status: response.status, responseText };
}

async function sendLeadEmail(env: LeadEnv, lead: Record<string, string>, textBody: string) {
  const recipient = clean(env.M365_RECIPIENT || env.M365_SENDER);

  if (!recipient) {
    throw new Error("Microsoft Graph recipient is not configured.");
  }

  const subject = `Free Trust & Growth Audit request — ${lead.business_name}`;
  return sendGraphMail(env, {
    subject,
    body: { contentType: "Text", content: textBody },
    toRecipients: [{ emailAddress: { address: recipient } }],
    replyTo: lead.prospect_email ? [{ emailAddress: { address: lead.prospect_email, name: lead.full_name || lead.business_name } }] : undefined,
  });
}

function buildProspectConfirmationBody(lead: Record<string, string>) {
  return `Hi ${lead.full_name || "there"},

Thank you for requesting your Free Trust & Growth Audit for ${lead.business_name}. I have your details and the audit is now in motion.

You can expect the report within 48 working hours. We will check website clarity, enquiry capture, WhatsApp/call follow-up, trust signals, and basic privacy/consent readiness.

If something urgent needs to be added before we review it, WhatsApp us at +91 87963 02608 with your business name.

Warmly,
Anushka Bhattacharya
Director, AICloudStrategist`;
}

async function sendProspectConfirmationEmail(env: LeadEnv, lead: Record<string, string>) {
  if (!lead.prospect_email) {
    return { status: 0, responseText: "skipped: prospect email not provided" };
  }

  return sendGraphMail(env, {
    subject: "Your Free Trust & Growth Audit is in motion — AICloudStrategist",
    body: { contentType: "Text", content: buildProspectConfirmationBody(lead) },
    toRecipients: [{ emailAddress: { address: lead.prospect_email, name: lead.full_name || lead.business_name } }],
    replyTo: [{ emailAddress: { address: clean(env.M365_RECIPIENT || env.M365_SENDER), name: "AICloudStrategist" } }],
  });
}

export const onRequestPost: PagesFunction<LeadEnv> = async (context) => {
  let payload: Record<string, unknown>;
  try {
    payload = await context.request.json();
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid JSON payload." }), { status: 400, headers: jsonHeaders });
  }

  const businessName = clean(payload.business_name);
  const website = clean(payload.website || payload.website_url);
  const whatsappNumber = clean(payload.whatsapp_number);
  const vertical = clean(payload.vertical);
  const prospectEmail = clean(payload.prospect_email || payload.email);
  const notes = clean(payload.notes || payload.specific_notes);
  const fullName = clean(payload.full_name);

  const missing = [
    ["business_name", businessName],
    ["website", website],
    ["whatsapp_number", whatsappNumber],
    ["vertical", vertical],
    ["prospect_email", prospectEmail],
  ]
    .filter(([, value]) => !value)
    .map(([field]) => field);

  if (missing.length) {
    return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^https?:\/\//i.test(website)) {
    return new Response(JSON.stringify({ ok: false, error: "Website must start with http:// or https://." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^\+?[0-9][0-9\s-]{8,18}$/.test(whatsappNumber)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid WhatsApp number with country code." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(prospectEmail)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid email address." }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  const submittedAt = new Date().toISOString();
  const leadId = `lead-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
  const lead = {
    lead_id: leadId,
    submitted_at: submittedAt,
    full_name: fullName,
    business_name: businessName,
    website,
    whatsapp_number: whatsappNumber,
    vertical,
    prospect_email: prospectEmail,
    email: prospectEmail,
    notes,
    source: "free-trust-growth-audit",
  };

  const textBody = `New AICloudStrategist Free Trust & Growth Audit request\n\nLead ID: ${leadId}\nSubmitted at: ${submittedAt}\nFull name: ${fullName || "not provided"}\nBusiness name: ${businessName}\nWebsite: ${website}\nWhatsApp: ${whatsappNumber}\nVertical: ${vertical}\nEmail: ${prospectEmail}\nNotes: ${notes || "not provided"}\n`;

  let internalGraphResult: { status: number; responseText: string };
  let prospectGraphResult: { status: number; responseText: string };
  try {
    internalGraphResult = await sendLeadEmail(context.env, lead, textBody);
    prospectGraphResult = await sendProspectConfirmationEmail(context.env, lead);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Email delivery failed.";
    return new Response(JSON.stringify({ ok: false, error: "Email delivery failed. Please retry or WhatsApp us directly.", details: message.slice(0, 300) }), {
      status: 502,
      headers: jsonHeaders,
    });
  }

  const logRecord = {
    ...lead,
    graph_status: internalGraphResult.status,
    graph_response: internalGraphResult.responseText.slice(0, 500),
    prospect_confirmation_status: prospectGraphResult.status,
    prospect_confirmation_response: prospectGraphResult.responseText.slice(0, 500),
  };
  try {
    if (context.env.LEAD_LOG) {
      await context.env.LEAD_LOG.put(leadId, JSON.stringify(logRecord), { metadata: { submitted_at: submittedAt, business_name: businessName } });
    }
  } catch {
    // Email delivery is the primary pipeline. KV logging failure should not create a false failure for the prospect.
  }

  return new Response(JSON.stringify({ ok: true, lead_id: leadId, confirmation_sent: prospectGraphResult.status > 0 }), { status: 200, headers: jsonHeaders });
};

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });

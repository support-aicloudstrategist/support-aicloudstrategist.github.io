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

type Line = "A" | "B" | "contact";

let graphTokenCache: GraphTokenCache | null = null;

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const clean = (value: unknown) => String(value ?? "").trim();

function classifyLine(rawLine: string): Line {
  const l = rawLine.toLowerCase();
  if (l.startsWith("a")) return "A";
  if (l.startsWith("b")) return "B";
  return "contact";
}

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

// ── Line-aware copy ───────────────────────────────────────────────────────────
function internalSubject(line: Line, businessName: string) {
  if (line === "A") return `New Cost Teardown lead — ${businessName}`;
  if (line === "B") return `New Web/SEO Teardown lead — ${businessName}`;
  return `New contact enquiry — ${businessName}`;
}

function prospectSubject(line: Line) {
  if (line === "A") return "Your free AI & Cloud Cost Teardown is in motion — AICloudStrategist";
  if (line === "B") return "Your free Website + SEO Teardown is in motion — AICloudStrategist";
  return "We received your message — AICloudStrategist";
}

function buildProspectConfirmationBody(line: Line, lead: Record<string, string>) {
  const name = lead.full_name || "there";
  const signoff = `Warmly,\nAnushka Bhattacharya\nDirector, AICloudStrategist`;

  if (line === "A") {
    return `Hi ${name},

Thanks for requesting your free AI & Cloud Cost Teardown for ${lead.business_name}.

We'll review your setup (${lead.vertical || "your cloud/AI stack"}) and send back a clear teardown: where you're overspending on cloud, GPU and LLM/API, the highest-impact savings, and a ranked list of fixes — with estimated monthly and annual savings.

You can expect it within 2 working days. To add context before we review, just reply to this email, or WhatsApp +91 87963 02608 with your business name.

${signoff}`;
  }

  if (line === "B") {
    return `Hi ${name},

Thanks for requesting your free Website + SEO Teardown for ${lead.business_name}.

We'll review ${lead.website} and send back: a conversion review of your current site, your technical / on-page / content SEO gaps, keywords you can realistically win, and a ranked, prioritized fix list.

You can expect it within 2 working days. To add context, reply to this email, or WhatsApp +91 87963 02608 with your business name.

${signoff}`;
  }

  return `Hi ${name},

Thanks for reaching out to AICloudStrategist — we have your message about ${lead.business_name} and will reply within 1 working day.

If it's urgent, WhatsApp us at +91 87963 02608 or call +91 80654 80898.

${signoff}`;
}

async function sendLeadEmail(env: LeadEnv, line: Line, lead: Record<string, string>, textBody: string) {
  const recipient = clean(env.M365_RECIPIENT || env.M365_SENDER);
  if (!recipient) {
    throw new Error("Microsoft Graph recipient is not configured.");
  }

  return sendGraphMail(env, {
    subject: internalSubject(line, lead.business_name),
    body: { contentType: "Text", content: textBody },
    toRecipients: [{ emailAddress: { address: recipient } }],
    replyTo: lead.prospect_email ? [{ emailAddress: { address: lead.prospect_email, name: lead.full_name || lead.business_name } }] : undefined,
  });
}

async function sendProspectConfirmationEmail(env: LeadEnv, line: Line, lead: Record<string, string>) {
  if (!lead.prospect_email) {
    return { status: 0, responseText: "skipped: prospect email not provided" };
  }

  return sendGraphMail(env, {
    subject: prospectSubject(line),
    body: { contentType: "Text", content: buildProspectConfirmationBody(line, lead) },
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
  const rawLine = clean(payload.line);
  const line = classifyLine(rawLine);

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
    line: rawLine || line,
    line_class: line,
    landing_page: clean(payload.landing_page),
    referrer: clean(payload.referrer),
    utm_source: clean(payload.utm_source),
    utm_medium: clean(payload.utm_medium),
    utm_campaign: clean(payload.utm_campaign),
    utm_content: clean(payload.utm_content),
    utm_term: clean(payload.utm_term),
    source: rawLine || "website",
  };

  const lineLabel = line === "A" ? "Line A — AI & Cloud Cost" : line === "B" ? "Line B — Web & SEO" : "General contact";
  const textBody = `New AICloudStrategist lead\n\nLine: ${lineLabel} (${rawLine || "n/a"})\nLead ID: ${leadId}\nSubmitted at: ${submittedAt}\nFull name: ${fullName || "not provided"}\nBusiness name: ${businessName}\nWebsite: ${website}\nWhatsApp: ${whatsappNumber}\nVertical: ${vertical}\nEmail: ${prospectEmail}\nNotes: ${notes || "not provided"}\n\nLanding page: ${lead.landing_page || "n/a"}\nReferrer: ${lead.referrer || "n/a"}\nUTM: ${lead.utm_source || "-"}/${lead.utm_medium || "-"}/${lead.utm_campaign || "-"}\n`;

  let internalGraphResult: { status: number; responseText: string };
  let prospectGraphResult: { status: number; responseText: string };
  try {
    internalGraphResult = await sendLeadEmail(context.env, line, lead, textBody);
    prospectGraphResult = await sendProspectConfirmationEmail(context.env, line, lead);
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
      await context.env.LEAD_LOG.put(leadId, JSON.stringify(logRecord), { metadata: { submitted_at: submittedAt, business_name: businessName, line } });
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

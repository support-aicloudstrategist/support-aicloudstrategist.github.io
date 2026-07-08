type ContactEnv = {
  CONTACT_LOG?: KVNamespace;
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

async function parsePayload(request: Request): Promise<Record<string, unknown>> {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return (await request.json()) as Record<string, unknown>;
  }
  const formData = await request.formData();
  return Object.fromEntries(formData.entries());
}

async function getGraphToken(env: ContactEnv): Promise<string> {
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

  const tokenPayload = (await response.json().catch(() => ({}))) as {
    access_token?: string;
    expires_in?: number;
    error?: string;
    error_description?: string;
  };
  if (!response.ok || !tokenPayload.access_token) {
    throw new Error(tokenPayload.error_description || tokenPayload.error || `Graph token request failed with ${response.status}.`);
  }

  graphTokenCache = {
    token: tokenPayload.access_token,
    expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000,
  };

  return graphTokenCache.token;
}

async function sendGraphMail(env: ContactEnv, graphMessage: Record<string, unknown>) {
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

const looksLikeEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

export const onRequestPost: PagesFunction<ContactEnv> = async (context) => {
  let payload: Record<string, unknown>;
  try {
    payload = await parsePayload(context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid submission payload." }), { status: 400, headers: jsonHeaders });
  }

  const name = clean(payload.name || payload.full_name);
  const contact = clean(payload.contact || payload.email || payload.whatsapp_number);
  const need = clean(payload.need || payload.vertical || "Not specified");
  const message = clean(payload.message || payload.notes || payload.specific_notes);
  const website = clean(payload.website || payload.website_url);

  const missing = [
    ["name", name],
    ["contact", contact],
  ]
    .filter(([, value]) => !value)
    .map(([field]) => field);

  if (missing.length) {
    return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), {
      status: 422,
      headers: jsonHeaders,
    });
  }

  const submittedAt = new Date().toISOString();
  const contactId = `contact-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
  const recipient = clean(context.env.M365_RECIPIENT || context.env.M365_SENDER);
  if (!recipient) {
    return new Response(JSON.stringify({ ok: false, error: "Contact delivery is not configured. Please WhatsApp us directly." }), {
      status: 502,
      headers: jsonHeaders,
    });
  }

  const textBody = `New AICloudStrategist contact enquiry\n\nContact ID: ${contactId}\nSubmitted at: ${submittedAt}\nName: ${name}\nContact: ${contact}\nNeed: ${need}\nWebsite: ${website || "not provided"}\nMessage: ${message || "not provided"}\nSource: contact page\n`;

  let graphResult: { status: number; responseText: string };
  try {
    graphResult = await sendGraphMail(context.env, {
      subject: `Website contact enquiry — ${name}`,
      body: { contentType: "Text", content: textBody },
      toRecipients: [{ emailAddress: { address: recipient } }],
      replyTo: looksLikeEmail(contact) ? [{ emailAddress: { address: contact, name } }] : undefined,
    });
  } catch (error) {
    const messageText = error instanceof Error ? error.message : "Email delivery failed.";
    return new Response(JSON.stringify({ ok: false, error: "We could not submit the enquiry. Please retry or WhatsApp us directly.", details: messageText.slice(0, 300) }), {
      status: 502,
      headers: jsonHeaders,
    });
  }

  const logRecord = {
    contact_id: contactId,
    submitted_at: submittedAt,
    name,
    contact,
    need,
    website,
    message,
    source: "contact-page",
    graph_status: graphResult.status,
    graph_response: graphResult.responseText.slice(0, 500),
  };

  try {
    const log = context.env.CONTACT_LOG || context.env.LEAD_LOG;
    if (log) {
      await log.put(contactId, JSON.stringify(logRecord), { metadata: { submitted_at: submittedAt, name } });
    }
  } catch {
    // Delivery is the primary pipeline. Logging failure should not create a false failure for the prospect.
  }

  return new Response(JSON.stringify({ ok: true, contact_id: contactId }), { status: 200, headers: jsonHeaders });
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

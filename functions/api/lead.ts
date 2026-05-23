export const onRequestPost: PagesFunction<{
  LEAD_LOG?: KVNamespace;
}> = async (context) => {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
  };

  let payload: Record<string, unknown>;
  try {
    payload = await context.request.json();
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid JSON payload." }), { status: 400, headers });
  }

  const clean = (value: unknown) => String(value ?? "").trim();
  const businessName = clean(payload.business_name);
  const website = clean(payload.website || payload.website_url);
  const whatsappNumber = clean(payload.whatsapp_number);
  const vertical = clean(payload.vertical);
  const email = clean(payload.email);
  const notes = clean(payload.notes || payload.specific_notes);
  const fullName = clean(payload.full_name);

  const missing = [
    ["business_name", businessName],
    ["website", website],
    ["whatsapp_number", whatsappNumber],
    ["vertical", vertical],
  ]
    .filter(([, value]) => !value)
    .map(([field]) => field);

  if (missing.length) {
    return new Response(JSON.stringify({ ok: false, error: `Missing required field(s): ${missing.join(", ")}` }), {
      status: 422,
      headers,
    });
  }

  if (!/^https?:\/\//i.test(website)) {
    return new Response(JSON.stringify({ ok: false, error: "Website must start with http:// or https://." }), {
      status: 422,
      headers,
    });
  }

  if (!/^\+?[0-9][0-9\s-]{8,18}$/.test(whatsappNumber)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid WhatsApp number with country code." }), {
      status: 422,
      headers,
    });
  }

  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(JSON.stringify({ ok: false, error: "Enter a valid email address or leave it blank." }), {
      status: 422,
      headers,
    });
  }

  const submittedAt = new Date().toISOString();
  const leadId = `lead-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID()}`;
  const lead = { lead_id: leadId, submitted_at: submittedAt, full_name: fullName, business_name: businessName, website, whatsapp_number: whatsappNumber, vertical, email, notes, source: "free-business-review" };

  const textBody = `New AICloudStrategist Lost-Lead Audit request\n\nLead ID: ${leadId}\nSubmitted at: ${submittedAt}\nFull name: ${fullName || "not provided"}\nBusiness name: ${businessName}\nWebsite: ${website}\nWhatsApp: ${whatsappNumber}\nVertical: ${vertical}\nEmail: ${email || "not provided"}\nNotes: ${notes || "not provided"}\n`;

  const mailPayload = {
    personalizations: [{ to: [{ email: "contact@aicloudstrategist.com", name: "AICloudStrategist" }] }],
    from: { email: "contact@aicloudstrategist.com", name: "AICloudStrategist Website" },
    reply_to: { email: email || "contact@aicloudstrategist.com", name: fullName || businessName },
    subject: `Free Lost-Lead Audit request — ${businessName}`,
    content: [{ type: "text/plain", value: textBody }],
  };

  let mailStatus = 0;
  let mailResponseText = "";
  let messageId = "";
  try {
    const mailResponse = await fetch("https://api.mailchannels.net/tx/v1/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(mailPayload),
    });
    mailStatus = mailResponse.status;
    mailResponseText = await mailResponse.text();
    messageId = mailResponse.headers.get("x-message-id") || mailResponse.headers.get("message-id") || "";
    if (!mailResponse.ok) {
      return new Response(
        JSON.stringify({ ok: false, error: "Email delivery failed. Please retry or WhatsApp us directly.", mail_status: mailStatus }),
        { status: 502, headers },
      );
    }
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: "Email delivery failed. Please retry or WhatsApp us directly." }), {
      status: 502,
      headers,
    });
  }

  const logRecord = { ...lead, mail_status: mailStatus, mail_response: mailResponseText.slice(0, 500), message_id: messageId };
  try {
    if (context.env.LEAD_LOG) {
      await context.env.LEAD_LOG.put(leadId, JSON.stringify(logRecord), { metadata: { submitted_at: submittedAt, business_name: businessName } });
    }
  } catch {
    // Email delivery is the primary pipeline. KV logging failure should not create a false failure for the prospect.
  }

  return new Response(JSON.stringify({ ok: true, lead_id: leadId, message_id: messageId }), { status: 200, headers });
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

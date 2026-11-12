type ChatEnv = {
  AI?: {
    run: (model: string, inputs: Record<string, unknown>) => Promise<unknown>;
  };
  CONTACT_LOG?: KVNamespace;
  LEAD_LOG?: KVNamespace;
  M365_TENANT_ID?: string;
  M365_CLIENT_ID?: string;
  M365_CLIENT_SECRET?: string;
  M365_SENDER?: string;
  M365_RECIPIENT?: string;
};

type GraphTokenCache = { token: string; expiresAt: number };
let graphTokenCache: GraphTokenCache | null = null;

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
  "Access-Control-Allow-Origin": "https://aicloudstrategist.com",
};

const clean = (value: unknown) => String(value ?? "").trim();

const KNOWLEDGE = [
  {
    id: "offer",
    keys: ["service", "diagnostic", "what do you do", "offer", "help", "finops", "governance"],
    title: "What AICloudStrategist offers",
    answer:
      "AICloudStrategist provides one fixed-fee Cloud & AI Cost Governance Diagnostic. It connects AWS, Azure, GCP, Kubernetes and GPU/model spend to owners, then ranks safe next actions as act, investigate or hold. It is consultancy work—not a dashboard subscription and not a savings-share engagement.",
  },
  {
    id: "pricing",
    keys: ["price", "pricing", "cost", "fee", "how much", "inr", "usd", "founding"],
    title: "Pricing",
    answer:
      "Fit review is free. Typical single-estate diagnostic: USD 2,500–3,000 (India visitors see INR 1,00,000–1,50,000). Complex multi-cloud/GPU estates: USD 5,500–12,000. Fee is fixed in writing after scope. No contingent savings share. First five paid diagnostics may get a time-boxed 20% founding credit.",
  },
  {
    id: "fit",
    keys: ["fit review", "book", "start", "contact", "call", "meeting"],
    title: "How to start",
    answer:
      "Start with a free fit review at /request-fit-review/. No billing files or credentials are required to begin. We reply within about 30 minutes in business hours with fit, clarify, or next-step guidance.",
  },
  {
    id: "process",
    keys: ["process", "how it works", "timeline", "steps", "deliverable", "dossier"],
    title: "Process",
    answer:
      "Four steps: free fit review → evidence intake (agreed exports/access) → ownership map → 30-day action plan. Typical single-estate readout is 10–15 business days after complete evidence intake. We do not execute production changes.",
  },
  {
    id: "platforms",
    keys: ["aws", "azure", "gcp", "kubernetes", "k8s", "gpu", "ai", "model"],
    title: "Platforms covered",
    answer:
      "The diagnostic covers material spend in scope across AWS, Azure, GCP, Kubernetes, and AI/GPU or model estates when evidence exists.",
  },
  {
    id: "risk",
    keys: ["risk", "guarantee", "savings", "roi", "hold", "safe"],
    title: "Risk and guarantees",
    answer:
      "We do not guarantee savings percentages or ROI. Recommendations include act, investigate or hold so thin evidence does not become a forced cut. You keep change ownership.",
  },
  {
    id: "audience",
    keys: ["finance", "engineering", "operations", "who", "audience"],
    title: "Who it is for",
    answer:
      "Built for finance (defendable ownership), engineering (safe action with blast radius), and operations (a usable 30-day owner view). See /why/ for audience and outcome pages.",
  },
  {
    id: "company",
    keys: ["about", "company", "legal", "cin", "who are you"],
    title: "Company",
    answer:
      "Public brand: AICloudStrategist. Legal entity: AICLOUDSTRATEGIST PRIVATE LIMITED. CIN U62020DC2026PTC470945. Contact: contact@aicloudstrategist.com · +91 80654 80898.",
  },
];

const SYSTEM_PROMPT = `You are the AICloudStrategist site assistant.
Answer only about AICloudStrategist's Cloud & AI Cost Governance Diagnostic, pricing, process, platforms, fit review, and boundaries.
Be concise (2–5 short sentences). Prefer facts from the knowledge snippets.
If asked for something outside that scope, say you can help with the diagnostic and point to the free fit review.
Never invent savings guarantees, credentials requests, or production changes by AICloudStrategist.
Never ask for billing files or cloud credentials in chat.
End with a gentle next step when relevant (fit review or pricing page).`;

async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function hasTrustedBrowserProvenance(request: Request) {
  const origin = clean(request.headers.get("Origin"));
  const fetchSite = clean(request.headers.get("Sec-Fetch-Site"));
  if (!origin) return false;
  try {
    const host = new URL(origin).hostname.toLowerCase();
    const trusted =
      host === "aicloudstrategist.com" ||
      host === "www.aicloudstrategist.com" ||
      host.endsWith(".aicloudstrategist-site.pages.dev") ||
      host === "127.0.0.1" ||
      host === "localhost";
    return trusted && (!fetchSite || fetchSite === "same-origin" || fetchSite === "same-site");
  } catch {
    return false;
  }
}

async function enforceRateLimit(env: ChatEnv, request: Request) {
  const log = env.CONTACT_LOG || env.LEAD_LOG;
  const clientIp = clean(request.headers.get("CF-Connecting-IP")) || "local";
  if (!log) return;
  const minute = new Date().toISOString().slice(0, 16);
  const key = `rate:chat:${minute}:${await sha256(clientIp)}`;
  const count = Number(await log.get(key)) || 0;
  if (count >= 20) throw new Error("RATE_LIMITED");
  await log.put(key, String(count + 1), { expirationTtl: 120 });
}

function scoreKnowledge(message: string) {
  const hay = message.toLowerCase();
  return KNOWLEDGE
    .map((item) => {
      const score = item.keys.reduce((sum, key) => sum + (hay.includes(key) ? 2 : 0), 0) +
        (hay.includes(item.title.toLowerCase()) ? 1 : 0);
      return { item, score };
    })
    .sort((a, b) => b.score - a.score);
}

function knowledgeReply(message: string) {
  const ranked = scoreKnowledge(message);
  const top = ranked.filter((row) => row.score > 0).slice(0, 2);
  if (!top.length) {
    return {
      reply:
        "I can help with AICloudStrategist's fixed-fee Cloud & AI Cost Governance Diagnostic—scope, pricing, process, platforms, and the free fit review. Ask about any of those, or book a fit review at /request-fit-review/.",
      refs: [] as string[],
    };
  }
  const reply = `${top.map((row) => row.item.answer).join(" ")} If you want, book a free fit review at /request-fit-review/.`;
  return { reply, refs: top.map((row) => row.item.id) };
}

async function getGraphToken(env: ChatEnv): Promise<string> {
  const tenantId = clean(env.M365_TENANT_ID);
  const clientId = clean(env.M365_CLIENT_ID);
  const clientSecret = clean(env.M365_CLIENT_SECRET);
  if (!tenantId || !clientId || !clientSecret) throw new Error("Graph credentials missing");

  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt - 60_000 > now) return graphTokenCache.token;

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
  };
  if (!response.ok || !tokenPayload.access_token) throw new Error("Graph token failed");
  graphTokenCache = {
    token: tokenPayload.access_token,
    expiresAt: now + Math.max(60, tokenPayload.expires_in || 3600) * 1000,
  };
  return graphTokenCache.token;
}

async function notifyOwner(env: ChatEnv, record: Record<string, unknown>) {
  const recipient = clean(env.M365_RECIPIENT || env.M365_SENDER);
  if (!recipient) return { sent: false, mode: "kv-only" as const };

  const text = `New website chatbot query\n\nChat ID: ${record.chat_id}\nSession: ${record.session_id}\nSubmitted: ${record.submitted_at}\nPage: ${record.page || "unknown"}\nMode: ${record.mode}\n\nVisitor: ${record.message}\n\nAssistant: ${record.reply}\n`;
  try {
    const token = await getGraphToken(env);
    const sender = clean(env.M365_SENDER);
    const response = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(sender)}/sendMail`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: {
          subject: `AICS chatbot query — ${(clean(record.message) || "message").slice(0, 60)}`,
          body: { contentType: "Text", content: text },
          toRecipients: [{ emailAddress: { address: recipient } }],
        },
        saveToSentItems: true,
      }),
    });
    return { sent: response.ok, mode: "microsoft-graph" as const };
  } catch {
    return { sent: false, mode: "notification-failed" as const };
  }
}

async function runWorkersAi(env: ChatEnv, message: string, history: Array<{ role: string; content: string }>) {
  if (!env.AI || typeof env.AI.run !== "function") return null;

  const ranked = scoreKnowledge(message).slice(0, 3);
  const snippets = ranked
    .filter((row) => row.score > 0)
    .map((row) => `- ${row.item.title}: ${row.item.answer}`)
    .join("\n");

  const messages = [
    { role: "system", content: SYSTEM_PROMPT },
    {
      role: "system",
      content: `Knowledge snippets:\n${snippets || "- Use only publicly known AICloudStrategist diagnostic facts."}`,
    },
    ...history.slice(-6).map((item) => ({
      role: item.role === "assistant" ? "assistant" : "user",
      content: clean(item.content).slice(0, 1200),
    })),
    { role: "user", content: message.slice(0, 1200) },
  ];

  // Prefer Llama 3.1 8B; fall back to smaller free-tier models if unavailable.
  const models = [
    "@cf/meta/llama-3.1-8b-instruct",
    "@cf/meta/llama-3.2-3b-instruct",
    "@cf/qwen/qwen1.5-1.8b-chat",
  ];

  for (const model of models) {
    try {
      const result = (await env.AI.run(model, { messages })) as {
        response?: string;
        result?: string;
      };
      const text = clean(result?.response || result?.result);
      if (text) return { text: text.slice(0, 1800), model };
    } catch {
      // Try next free-tier compatible model.
    }
  }
  return null;
}

export const onRequestPost: PagesFunction<ChatEnv> = async (context) => {
  // Allow local preview + production trusted origins.
  const origin = clean(context.request.headers.get("Origin"));
  let localOk = false;
  try {
    const host = origin ? new URL(origin).hostname.toLowerCase() : "";
    localOk = host === "127.0.0.1" || host === "localhost";
  } catch {
    localOk = false;
  }
  if (!localOk && !hasTrustedBrowserProvenance(context.request)) {
    return new Response(JSON.stringify({ ok: false, error: "Untrusted chat source." }), { status: 403, headers: jsonHeaders });
  }

  let payload: Record<string, unknown>;
  try {
    payload = (await context.request.json()) as Record<string, unknown>;
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid chat payload." }), { status: 400, headers: jsonHeaders });
  }

  const message = clean(payload.message);
  const sessionId = clean(payload.session_id).slice(0, 80) || crypto.randomUUID();
  const page = clean(payload.page).slice(0, 300);
  const history = Array.isArray(payload.history) ? (payload.history as Array<{ role: string; content: string }>) : [];

  if (!message || message.length < 2) {
    return new Response(JSON.stringify({ ok: false, error: "Message is required." }), { status: 422, headers: jsonHeaders });
  }
  if (message.length > 1200) {
    return new Response(JSON.stringify({ ok: false, error: "Message is too long." }), { status: 422, headers: jsonHeaders });
  }

  try {
    await enforceRateLimit(context.env, context.request);
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Too many chat requests. Please wait a moment." }), {
      status: 429,
      headers: jsonHeaders,
    });
  }

  const submittedAt = new Date().toISOString();
  const chatId = `chat-${submittedAt.replace(/[:.]/g, "-")}-${crypto.randomUUID().slice(0, 8)}`;

  let mode = "knowledge-base";
  let reply = "";
  let modelUsed = "";
  const aiReply = await runWorkersAi(context.env, message, history);
  if (aiReply?.text) {
    mode = "workers-ai";
    reply = aiReply.text;
    modelUsed = aiReply.model || "";
  } else {
    reply = knowledgeReply(message).reply;
  }

  const log = context.env.CONTACT_LOG || context.env.LEAD_LOG;
  const record = {
    chat_id: chatId,
    session_id: sessionId,
    submitted_at: submittedAt,
    page,
    message,
    reply,
    mode,
    model: modelUsed || null,
    source: "site-chatbot",
    pipeline_stage: "chat-lead",
    lead_status: "unreviewed",
  };

  if (log) {
    try {
      await log.put(chatId, JSON.stringify(record), {
        metadata: { submitted_at: submittedAt, source: "site-chatbot", session_id: sessionId },
      });
      const sessionKey = `chat-session:${sessionId}`;
      const priorRaw = await log.get(sessionKey);
      const prior = priorRaw ? (JSON.parse(priorRaw) as { turns?: unknown[] }) : { turns: [] };
      const turns = Array.isArray(prior.turns) ? prior.turns.slice(-40) : [];
      turns.push({ at: submittedAt, chat_id: chatId, message, reply, mode });
      await log.put(sessionKey, JSON.stringify({ session_id: sessionId, updated_at: submittedAt, turns }), {
        expirationTtl: 60 * 60 * 24 * 30,
      });
    } catch {
      // Reply still returns even if logging fails.
    }
  }

  const notify = await notifyOwner(context.env, record);

  return new Response(
    JSON.stringify({
      ok: true,
      chat_id: chatId,
      session_id: sessionId,
      reply,
      mode,
      model: modelUsed || null,
      notification_sent: notify.sent,
      notification_mode: notify.mode,
    }),
    { status: 200, headers: jsonHeaders }
  );
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

export const onRequestGet: PagesFunction<ChatEnv> = async (context) => {
  const storage = Boolean(context.env.CONTACT_LOG || context.env.LEAD_LOG);
  const ai = Boolean(context.env.AI);
  return new Response(
    JSON.stringify({
      ok: true,
      storage_configured: storage,
      workers_ai_bound: ai,
      free_tier: "Cloudflare Workers AI 10,000 neurons/day when AI binding is enabled; knowledge-base fallback always free",
    }),
    { status: 200, headers: jsonHeaders }
  );
};

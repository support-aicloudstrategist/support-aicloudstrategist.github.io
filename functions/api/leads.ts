type LeadsEnv = {
  CONTACT_LOG?: KVNamespace;
  LEAD_LOG?: KVNamespace;
  AICS_REPORT_TOKEN?: string;
};

// Read-only reader hash for Company Agents (only the SHA-256 hash is stored here; the token stays private).
const PRODUCT_READER_SHA256 = "95c7ac6b1f2ed3024b6bb22333cb9cb1414c01c4d6c1179ff967d857068bacdf";

const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

async function sha256Hex(value: string) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function isAuthorized(request: Request, env: LeadsEnv) {
  const auth = request.headers.get("Authorization") || "";
  const match = auth.match(/^Bearer\s+(.+)$/i);
  const token = match ? match[1].trim() : "";
  if (!token) return false;
  if (env.AICS_REPORT_TOKEN && token === env.AICS_REPORT_TOKEN.trim()) return true;
  return (await sha256Hex(token)) === PRODUCT_READER_SHA256;
}

async function listKeys(kv: KVNamespace | undefined, prefixes: string[]) {
  if (!kv) return [];
  const out: Array<{ kv: KVNamespace; name: string; submittedAt: string }> = [];
  for (const prefix of prefixes) {
    let cursor: string | undefined;
    for (let page = 0; page < 5; page += 1) {
      const listed = await kv.list(cursor ? { prefix, limit: 500, cursor } : { prefix, limit: 500 });
      for (const k of listed.keys || []) {
        const meta = (k.metadata || {}) as Record<string, unknown>;
        out.push({ kv, name: k.name, submittedAt: String(meta.submitted_at || meta.submittedAt || k.name) });
      }
      if (!listed.list_complete && listed.cursor) cursor = listed.cursor;
      else break;
    }
  }
  return out;
}

function toNormalizedRecord(raw: Record<string, unknown>) {
  const id = String(raw.contact_id || raw.lead_id || "");
  return {
    leadId: id,
    status: String(raw.lead_status || raw.pipeline_stage || "new"),
    lead: {
      submittedAt: String(raw.submitted_at || ""),
      sourcePage: String(raw.source || ""),
      formType: raw.contact_id ? "fit_review_contact" : "audit_lead",
      fullName: String(raw.name || raw.full_name || ""),
      businessEmail: String(raw.contact || raw.prospect_email || raw.email || ""),
      phone: String(raw.whatsapp_number || ""),
      company: String(raw.company || raw.business_name || ""),
      websiteOrLinkedIn: String(raw.website || ""),
      role: String(raw.role || ""),
      industry: String(raw.vertical || ""),
      aiInterestArea: String(raw.service || raw.service_context || raw.package_context || ""),
      businessProblem: [raw.need, raw.message, raw.notes].filter(Boolean).join(" — "),
      landingPage: String(raw.landing_page || ""),
      referrer: String(raw.referrer || ""),
      utmSource: String(raw.utm_source || ""),
      utmMedium: String(raw.utm_medium || ""),
      utmCampaign: String(raw.utm_campaign || ""),
      gclid: String(raw.gclid || ""),
      msclkid: String(raw.msclkid || ""),
      liFatId: String(raw.li_fat_id || ""),
    },
  };
}

export const onRequestGet: PagesFunction<LeadsEnv> = async ({ request, env }) => {
  if (!(await isAuthorized(request, env))) {
    return new Response(JSON.stringify({ ok: false, error: "Unauthorized" }), { status: 401, headers: jsonHeaders });
  }
  if (!env.CONTACT_LOG && !env.LEAD_LOG) {
    return new Response(JSON.stringify({ ok: false, error: "Lead storage is not configured" }), { status: 503, headers: jsonHeaders });
  }
  const url = new URL(request.url);
  const limit = Math.min(Math.max(Number(url.searchParams.get("limit") || 50), 1), 200);
  const seen = new Set<string>();
  const candidates: Array<{ kv: KVNamespace; name: string; submittedAt: string }> = [];
  for (const item of [
    ...(await listKeys(env.CONTACT_LOG, ["contact-"])),
    ...(await listKeys(env.LEAD_LOG, ["contact-", "lead-"])),
  ]) {
    if (!seen.has(item.name)) {
      seen.add(item.name);
      candidates.push(item);
    }
  }
  candidates.sort((a, b) => b.submittedAt.localeCompare(a.submittedAt));
  const slice = candidates.slice(0, limit);
  const leads = (
    await Promise.all(
      slice.map(async (entry) => {
        const val = await entry.kv.get(entry.name, "json");
        return val && typeof val === "object" ? toNormalizedRecord(val as Record<string, unknown>) : null;
      }),
    )
  ).filter(Boolean);
  return new Response(JSON.stringify({ ok: true, count: leads.length, totalStored: candidates.length, leads }), { status: 200, headers: jsonHeaders });
};

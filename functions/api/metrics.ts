type MetricsEnv = {
  LEAD_LOG?: KVNamespace;
  CONTACT_LOG?: KVNamespace;
  AICS_REPORT_TOKEN?: string;
};

type StoredEvent = {
  name?: string;
  path?: string;
  session?: string;
  received_at?: string;
  props?: Record<string, string>;
};

type StoredLead = {
  contact_id?: string;
  submitted_at?: string;
  name?: string;
  contact?: string;
  company?: string;
  role?: string;
  service?: string;
  stage?: string;
  need?: string;
  message?: string;
  source?: string;
  landing_page?: string;
  referrer?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  lead_status?: string;
};

type KeyMeta = { received_at?: string; name?: string; path?: string };

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "private, max-age=20",
};

const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

/** Normalize pasted/header tokens: trim, strip wrapping quotes, strip accidental Bearer prefix. */
function normalizeToken(value: unknown, max = 512) {
  let token = String(value ?? "")
    .replace(/^\uFEFF/, "")
    .trim()
    .slice(0, max);
  if (
    (token.startsWith('"') && token.endsWith('"')) ||
    (token.startsWith("'") && token.endsWith("'"))
  ) {
    token = token.slice(1, -1).trim();
  }
  token = token.replace(/^Bearer\s+/i, "").trim();
  return token;
}

function extractBearerToken(request: Request) {
  const raw = request.headers.get("Authorization") || request.headers.get("X-AICS-Report-Token") || "";
  const match = raw.match(/^Bearer\s+(.+)$/i);
  if (match) return normalizeToken(match[1], 512);
  // Allow raw token in Authorization for paste mistakes, plus dedicated header.
  return normalizeToken(raw, 512);
}

type AuthResult =
  | { ok: true; token: string }
  | { ok: false; status: number; error: string; code: string };

function authorize(request: Request, env: MetricsEnv): AuthResult {
  const configured = normalizeToken(env.AICS_REPORT_TOKEN, 512);
  if (!configured) {
    return {
      ok: false,
      status: 503,
      code: "server_token_missing",
      error:
        "AICS_REPORT_TOKEN is not set on this Cloudflare Pages environment. Add it under Pages → Settings → Environment variables (Production), then redeploy.",
    };
  }

  const supplied = extractBearerToken(request);
  if (!supplied) {
    return {
      ok: false,
      status: 401,
      code: "missing_authorization",
      error: "Missing Authorization Bearer token. Paste the report token in the dashboard and click Load.",
    };
  }

  // Exact match after normalization (case-sensitive — secrets usually are).
  if (supplied !== configured) {
    return {
      ok: false,
      status: 401,
      code: "invalid_token",
      error:
        "Invalid report token. Check you copied AICS_REPORT_TOKEN from the Production environment (not Preview), with no extra spaces or quotes.",
    };
  }

  return { ok: true, token: supplied };
}

function dayKey(iso: string) {
  return iso.slice(0, 10) || "unknown";
}

function bump(map: Record<string, number>, key: string, by = 1) {
  const k = key || "unknown";
  map[k] = (map[k] || 0) + by;
}

function topEntries(map: Record<string, number>, limit = 20) {
  return Object.entries(map)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([key, count]) => ({ key, count }));
}

function classifySource(provider: string, channel: string, campaign: string) {
  const p = provider.toLowerCase();
  const c = channel.toLowerCase();
  if (campaign || c.includes("cpc") || c.includes("ppc") || c.includes("paid")) return "campaigns";
  if (p === "google" || p === "bing") return "search";
  if (
    p.includes("linkedin") ||
    p.includes("twitter") ||
    p.includes("x.com") ||
    p.includes("facebook") ||
    p.includes("instagram") ||
    p.includes("youtube") ||
    c.includes("social")
  ) {
    return "social";
  }
  if (p === "direct" || !p) return "direct";
  if (p === "referral" || p.includes(".")) return "referrals";
  return p || "other";
}

function eachDay(fromMs: number, toMs: number): string[] {
  const days: string[] = [];
  const start = new Date(fromMs);
  start.setUTCHours(0, 0, 0, 0);
  for (let t = start.getTime(); t <= toMs; t += 86400000) {
    days.push(new Date(t).toISOString().slice(0, 10));
  }
  return days;
}

async function listKeysForPrefix(store: KVNamespace, prefix: string, maxKeys: number) {
  const keys: Array<{ name: string; metadata?: KeyMeta }> = [];
  let cursor: string | undefined;
  do {
    const page = await store.list({ prefix, limit: Math.min(1000, maxKeys - keys.length), cursor });
    for (const key of page.keys) {
      keys.push({ name: key.name, metadata: key.metadata as KeyMeta | undefined });
      if (keys.length >= maxKeys) return keys;
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return keys;
}

async function getMany(store: KVNamespace, names: string[], batchSize = 40) {
  const out = new Map<string, string | null>();
  for (let i = 0; i < names.length; i += batchSize) {
    const chunk = names.slice(i, i + batchSize);
    const values = await Promise.all(chunk.map((name) => store.get(name)));
    chunk.forEach((name, idx) => out.set(name, values[idx]));
  }
  return out;
}

async function loadLeads(
  stores: Array<KVNamespace | undefined>,
  cutoff: number,
  rangeEnd: number,
  maxKeys = 500,
) {
  const leads: Array<Record<string, string>> = [];
  const seen = new Set<string>();

  for (const store of stores) {
    if (!store) continue;
    const leadKeys = await listKeysForPrefix(store, "contact-", maxKeys);
    const leadBodies = await getMany(
      store,
      leadKeys.map((k) => k.name),
      40,
    );
    for (const key of leadKeys) {
      if (seen.has(key.name)) continue;
      const raw = leadBodies.get(key.name);
      if (!raw) continue;
      try {
        const lead = JSON.parse(raw) as StoredLead;
        const submittedAt = clean(lead.submitted_at, 40);
        const ts = Date.parse(submittedAt);
        if (Number.isFinite(ts) && (ts < cutoff || ts > rangeEnd)) continue;
        seen.add(key.name);
        leads.push({
          contact_id: clean(lead.contact_id || key.name, 120),
          submitted_at: submittedAt,
          name: clean(lead.name, 160),
          email: clean(lead.contact, 320),
          company: clean(lead.company, 160),
          role: clean(lead.role, 160),
          stage: clean(lead.stage, 160),
          source: clean(lead.source, 80),
          service: clean(lead.service, 160),
          landing_page: clean(lead.landing_page, 400),
          referrer: clean(lead.referrer, 400),
          utm_source: clean(lead.utm_source, 120),
          utm_medium: clean(lead.utm_medium, 120),
          utm_campaign: clean(lead.utm_campaign, 120),
          need: clean(lead.need, 240),
          message: clean(lead.message, 400),
          lead_status: clean(lead.lead_status, 40),
        });
      } catch {
        // Skip malformed lead rows.
      }
    }
  }

  leads.sort((a, b) => String(b.submitted_at).localeCompare(String(a.submitted_at)));
  return leads;
}

export const onRequestGet: PagesFunction<MetricsEnv> = async ({ request, env }) => {
  const started = Date.now();
  try {
    const auth = authorize(request, env);
    if (!auth.ok) {
      return new Response(
        JSON.stringify({ ok: false, error: auth.error, code: auth.code }),
        { status: auth.status, headers },
      );
    }

    const eventStore = env.LEAD_LOG;
    const leadStore = env.CONTACT_LOG || env.LEAD_LOG;
    if (!eventStore && !leadStore) {
      return new Response(JSON.stringify({ ok: false, error: "Metrics store unavailable" }), {
        status: 503,
        headers,
      });
    }

    const url = new URL(request.url);
    const mode = clean(url.searchParams.get("mode") || "dashboard", 40);
    const realtimeOnly = mode === "realtime" || url.searchParams.get("realtime") === "1";
    const days = Math.min(90, Math.max(1, Number(url.searchParams.get("days") || 28)));
    const fromParam = clean(url.searchParams.get("from"), 32);
    const toParam = clean(url.searchParams.get("to"), 32);
    const now = Date.now();
    let cutoff = now - days * 86400000;
    let rangeEnd = now;
    if (fromParam && Date.parse(fromParam)) cutoff = Date.parse(fromParam);
    if (toParam && Date.parse(toParam)) rangeEnd = Date.parse(toParam) + 86400000 - 1;

    // Long ranges: prefer coarser work budgets so Workers finish before the edge times out.
    const maxEventKeys = realtimeOnly ? 1500 : days >= 60 ? 4000 : days >= 28 ? 6000 : 8000;
    const liveWindowMs = 2 * 60 * 1000;
    const enterWindowMs = 5 * 60 * 1000;

    const totals: Record<string, number> = {};
    const providers: Record<string, number> = {};
    const devices: Record<string, number> = {};
    const browsers: Record<string, number> = {};
    const countries: Record<string, number> = {};
    const visitorKinds: Record<string, number> = {};
    const trafficBuckets: Record<string, number> = {};
    const emailTriggers: Record<string, number> = {};
    const pathViews: Record<string, number> = {};
    const pathCta: Record<string, number> = {};
    const pathScroll: Record<string, number> = {};
    const pathDwellSum: Record<string, number> = {};
    const pathDwellCount: Record<string, number> = {};
    const pathDownloads: Record<string, number> = {};
    const dailyViews: Record<string, number> = {};
    const dailySessions: Record<string, number> = {};
    const sessionSeen = new Set<string>();
    const visitorSeen = new Set<string>();
    const sessionDay = new Set<string>();
    const liveSessions = new Set<string>();
    const livePages: Record<string, number> = {};
    const liveSources: Record<string, number> = {};
    const liveLocations: Record<string, number> = {};
    const enteringSessions = new Set<string>();
    const feed: Array<Record<string, string>> = [];
    let inspected = 0;
    let skippedPresence = 0;
    let keysListed = 0;

    if (eventStore) {
      const dayList = realtimeOnly
        ? eachDay(now - liveWindowMs - 86400000, now)
        : eachDay(cutoff, rangeEnd);

      const listed: Array<{ name: string; metadata?: KeyMeta }> = [];
      for (const day of dayList) {
        if (listed.length >= maxEventKeys) break;
        const dayKeys = await listKeysForPrefix(eventStore, `event:${day}`, maxEventKeys - listed.length);
        listed.push(...dayKeys);
      }
      keysListed = listed.length;

      // Avoid reading historical presence heartbeats (high volume, little dashboard value).
      const toFetch: string[] = [];
      for (const key of listed) {
        const metaName = clean(key.metadata?.name, 64);
        const receivedMeta = clean(key.metadata?.received_at, 40);
        const metaTs = Date.parse(receivedMeta);
        const inLiveWindow = Number.isFinite(metaTs) && now - metaTs <= liveWindowMs;
        if (metaName === "presence_ping" && !inLiveWindow && !realtimeOnly) {
          skippedPresence += 1;
          bump(totals, "presence_ping");
          continue;
        }
        toFetch.push(key.name);
      }

      const bodies = await getMany(eventStore, toFetch, 50);

      for (const key of listed) {
        const raw = bodies.get(key.name);
        if (raw == null) continue;
        try {
          const event = JSON.parse(raw) as StoredEvent;
          const receivedAt = clean(event.received_at || key.metadata?.received_at, 40);
          const ts = Date.parse(receivedAt);
          if (!Number.isFinite(ts) || ts < cutoff || ts > rangeEnd) {
            if (!(realtimeOnly && now - ts <= enterWindowMs)) continue;
          }

          const name = clean(event.name, 64) || "unknown";
          const path = clean(event.path || key.metadata?.path, 256) || "/";
          const session = clean(event.session, 64);
          const props = event.props || {};
          const provider = clean(props.provider, 120) || "direct";
          const channel = clean(props.channel, 120);
          const campaign = clean(props.campaign, 120);
          const device = clean(props.device, 40) || "unknown";
          const browser = clean(props.browser, 40) || "unknown";
          const country = clean(props.country, 8) || "unknown";
          const visitor = clean(props.visitor, 64);
          const visitorKind = clean(props.visitor_kind, 24) || "unknown";
          const trigger = clean(props.trigger, 40);
          const depth = clean(props.depth, 16);
          const seconds = Number(props.seconds || 0);

          bump(totals, name);
          inspected += 1;

          if (session) {
            sessionSeen.add(session);
            const dkey = `${dayKey(receivedAt)}:${session}`;
            if (!sessionDay.has(dkey)) {
              sessionDay.add(dkey);
              bump(dailySessions, dayKey(receivedAt));
            }
            if (now - ts <= liveWindowMs) {
              liveSessions.add(session);
              bump(livePages, path);
              bump(liveSources, classifySource(provider, channel, campaign));
              bump(liveLocations, country);
            }
            if (
              (name === "page_view" || (name === "presence_ping" && trigger === "enter")) &&
              now - ts <= enterWindowMs
            ) {
              enteringSessions.add(session);
            }
          }
          if (visitor) visitorSeen.add(visitor);

          if (realtimeOnly) {
            if (feed.length < 40) {
              feed.push({
                at: receivedAt,
                name,
                path,
                detail: clean(props.cta || props.trigger || props.provider || props.depth || "", 80),
              });
            }
            continue;
          }

          if (name === "page_view") {
            bump(pathViews, path);
            bump(providers, provider);
            bump(devices, device);
            bump(browsers, browser);
            bump(countries, country);
            bump(visitorKinds, visitorKind);
            bump(trafficBuckets, classifySource(provider, channel, campaign));
            bump(dailyViews, dayKey(receivedAt));
          }

          if (name === "presence_ping" && now - ts <= liveWindowMs && session) {
            liveSessions.add(session);
            bump(livePages, path);
          }

          if (name === "cta_click" || name === "button_click") bump(pathCta, path);
          if (name === "download_click") bump(pathDownloads, path);
          if (name === "scroll_depth" && (Number(depth) || 0) >= 50) bump(pathScroll, path);
          if (name === "dwell_tick" && Number.isFinite(seconds) && seconds > 0) {
            pathDwellSum[path] = (pathDwellSum[path] || 0) + seconds;
            pathDwellCount[path] = (pathDwellCount[path] || 0) + 1;
          }
          if (name === "email_capture_open" && trigger) bump(emailTriggers, trigger);

          feed.push({
            at: receivedAt,
            name,
            path,
            detail: clean(props.cta || props.trigger || props.provider || props.depth || "", 80),
          });
          if (feed.length > 60) {
            feed.sort((a, b) => String(b.at).localeCompare(String(a.at)));
            feed.length = 30;
          }
        } catch {
          // Skip malformed rows.
        }
      }
    }

    feed.sort((a, b) => String(b.at).localeCompare(String(a.at)));

    if (realtimeOnly) {
      // Same contact records email notifications use (/api/contact → contact-* KV).
      const liveLeads = await loadLeads([env.CONTACT_LOG, env.LEAD_LOG], cutoff, rangeEnd, 300);
      return new Response(
        JSON.stringify({
          ok: true,
          mode: "realtime",
          generated_at: new Date().toISOString(),
          duration_ms: Date.now() - started,
          realtime: {
            live_visitors: liveSessions.size,
            entering_visitors: enteringSessions.size,
            window_seconds: Math.round(liveWindowMs / 1000),
            enter_window_seconds: Math.round(enterWindowMs / 1000),
            pages_in_view: topEntries(livePages, 15),
            traffic_sources: topEntries(liveSources, 10),
            locations: topEntries(liveLocations, 15),
            feed: feed.slice(0, 25),
            refresh_hint_seconds: 15,
            identity: "Live visitor panels are aggregated only. Contacts below are voluntary form submissions.",
          },
          leads: {
            count: liveLeads.length,
            identity_policy:
              "Name and email appear only when voluntarily submitted via fit review, email capture, or contact forms.",
            items: liveLeads.slice(0, 200),
          },
        }),
        { status: 200, headers },
      );
    }

    const content = Object.keys({ ...pathViews, ...pathDwellSum })
      .map((path) => {
        const views = pathViews[path] || 0;
        const cta = pathCta[path] || 0;
        const dwellSamples = pathDwellCount[path] || 0;
        const avgDwell = dwellSamples ? Math.round((pathDwellSum[path] || 0) / dwellSamples) : 0;
        return {
          path,
          page_views: views,
          cta_clicks: cta,
          cta_rate: views ? Number(((cta / views) * 100).toFixed(1)) : 0,
          scroll_50_plus: pathScroll[path] || 0,
          downloads: pathDownloads[path] || 0,
          avg_dwell_seconds: avgDwell,
          dwell_samples: dwellSamples,
        };
      })
      .sort((a, b) => b.avg_dwell_seconds - a.avg_dwell_seconds || b.page_views - a.page_views)
      .slice(0, 40);

    const growth = eachDay(cutoff, rangeEnd).map((day) => ({
      day,
      page_views: dailyViews[day] || 0,
      sessions: dailySessions[day] || 0,
    }));

    const leads = await loadLeads([env.CONTACT_LOG, env.LEAD_LOG], cutoff, rangeEnd, 500);

    const pageViews = totals.page_view || 0;
    const conversions =
      (totals.form_submit_success || 0) + (totals.email_capture_submit_success || 0);

    return new Response(
      JSON.stringify({
        ok: true,
        mode,
        period_days: days,
        from: new Date(cutoff).toISOString(),
        to: new Date(rangeEnd).toISOString(),
        generated_at: new Date().toISOString(),
        duration_ms: Date.now() - started,
        events_inspected: inspected,
        keys_listed: keysListed,
        presence_skipped: skippedPresence,
        overview: {
          visitors: visitorSeen.size || sessionSeen.size,
          page_views: pageViews,
          sessions: sessionSeen.size,
          conversions,
          growth,
        },
        audience: {
          new_vs_returning: visitorKinds,
          locations: topEntries(countries, 25),
          browsers: topEntries(browsers, 15),
          devices: topEntries(devices, 10),
          age: {
            available: false,
            note: "Browsers do not expose visitor age. Age will remain unavailable without a voluntary form field.",
          },
        },
        traffic: {
          buckets: trafficBuckets,
          providers: topEntries(providers, 20),
        },
        content,
        realtime: {
          live_visitors: liveSessions.size,
          entering_visitors: enteringSessions.size,
          window_seconds: Math.round(liveWindowMs / 1000),
          enter_window_seconds: Math.round(enterWindowMs / 1000),
          pages_in_view: topEntries(livePages, 15),
          traffic_sources: topEntries(liveSources, 10),
          locations: topEntries(liveLocations, 15),
          feed: feed.slice(0, 25),
          refresh_hint_seconds: 15,
          identity: "Aggregated only — no names or emails in real-time views.",
        },
        engagement: {
          events: totals,
          email_capture_triggers: emailTriggers,
          note: "CTA rate is on-page click-through (CTA clicks ÷ page views), not ad-network PPC impressions.",
        },
        leads: {
          count: leads.length,
          identity_policy:
            "Name and email appear only when voluntarily submitted via fit review, email capture, or contact forms. Passive browsing is non-PII.",
          items: leads.slice(0, 200),
        },
        coverage: {
          stack: "first-party KV events + voluntary contact records",
          scan: "day-prefixed event:YYYY-MM-DD keys + batched gets; historical presence_ping skipped",
          optional:
            "Enable Cloudflare Web Analytics in the Pages dashboard for privacy-preserving country aggregates if CF-IPCountry enrichment is sparse.",
          gaps: [
            "Age is not available from browsers",
            "Passive email collection is impossible in the browser — contacts require voluntary forms",
            "Dwell/scroll/presence metrics populate after the engagement tracker ships on pages",
          ],
        },
        privacy:
          "Analytics events remain non-PII. Lead identity is stored separately from voluntary form consent. Passive browsing never yields emails.",
      }),
      { status: 200, headers },
    );
  } catch (error) {
    const message = error instanceof Error ? error.message.slice(0, 300) : "Metrics query failed";
    return new Response(
      JSON.stringify({
        ok: false,
        error: message,
        duration_ms: Date.now() - started,
      }),
      { status: 500, headers },
    );
  }
};

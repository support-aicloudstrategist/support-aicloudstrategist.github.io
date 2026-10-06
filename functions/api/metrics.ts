type MetricsEnv = { LEAD_LOG?: KVNamespace; AICS_REPORT_TOKEN?: string };

const headers = {"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"};
const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

function authorized(request: Request, env: MetricsEnv) {
  const configured = clean(env.AICS_REPORT_TOKEN, 512);
  const supplied = clean(request.headers.get("Authorization"), 520).replace(/^Bearer\s+/i, "");
  return Boolean(configured && supplied && configured === supplied);
}

export const onRequestGet: PagesFunction<MetricsEnv> = async ({ request, env }) => {
  if (!authorized(request, env)) return new Response(JSON.stringify({ok:false,error:"Unauthorized"}), {status:401,headers});
  if (!env.LEAD_LOG) return new Response(JSON.stringify({ok:false,error:"Metrics store unavailable"}), {status:503,headers});

  const url = new URL(request.url);
  const days = Math.min(90, Math.max(1, Number(url.searchParams.get("days") || 28)));
  const cutoff = Date.now() - days * 86400000;
  const totals: Record<string, number> = {};
  const providers: Record<string, number> = {};
  const paths: Record<string, number> = {};
  let cursor: string | undefined;
  let inspected = 0;

  do {
    const page = await env.LEAD_LOG.list({prefix:"event:",limit:1000,cursor});
    for (const key of page.keys) {
      const received = String(key.metadata && (key.metadata as Record<string, unknown>).received_at || "");
      if (received && Date.parse(received) < cutoff) continue;
      const raw = await env.LEAD_LOG.get(key.name);
      if (!raw) continue;
      try {
        const event = JSON.parse(raw) as {name?:string;path?:string;props?:Record<string,string>;received_at?:string};
        if (event.received_at && Date.parse(event.received_at) < cutoff) continue;
        const name = clean(event.name,64) || "unknown";
        const path = clean(event.path,256) || "/";
        const provider = clean(event.props && event.props.provider,120) || "unknown";
        totals[name] = (totals[name] || 0) + 1;
        paths[path] = (paths[path] || 0) + 1;
        if (name === "page_view") providers[provider] = (providers[provider] || 0) + 1;
        inspected += 1;
      } catch {}
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor && inspected < 10000);

  return new Response(JSON.stringify({ok:true,period_days:days,generated_at:new Date().toISOString(),events_inspected:inspected,events:totals,page_views_by_provider:providers,top_paths:Object.entries(paths).sort((a,b)=>b[1]-a[1]).slice(0,25),privacy:"aggregate non-PII events only"}), {status:200,headers});
};

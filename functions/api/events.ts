type EventEnv = { LEAD_LOG?: KVNamespace };

const headers = {"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store","Access-Control-Allow-Origin":"https://aicloudstrategist.com"};
const allowedEvents = new Set(["page_view","cta_click","form_start","form_submit_attempt","form_validation_error","form_submit_success","form_submit_error","email_click","phone_click","whatsapp_click","pricing_view"]);
const allowedProps = new Set(["cta","destination","form","offer","section","source","status"]);
const clean = (value: unknown, max = 160) => String(value ?? "").trim().slice(0, max);

function trusted(request: Request) {
  const origin = clean(request.headers.get("Origin"));
  const fetchSite = clean(request.headers.get("Sec-Fetch-Site"));
  if (!origin) return false;
  try {
    const host = new URL(origin).hostname.toLowerCase();
    return (host === "aicloudstrategist.com" || host === "www.aicloudstrategist.com" || host.endsWith(".aicloudstrategist-site.pages.dev")) && (!fetchSite || fetchSite === "same-origin" || fetchSite === "same-site");
  } catch { return false; }
}

export const onRequestGet: PagesFunction<EventEnv> = async ({ env }) => new Response(JSON.stringify({
  ok:Boolean(env.LEAD_LOG), collector:env.LEAD_LOG ? "ready" : "unavailable", privacy:"non-PII allowlist"
}), {status:env.LEAD_LOG ? 200 : 503, headers});

export const onRequestPost: PagesFunction<EventEnv> = async ({ request, env }) => {
  if (!trusted(request)) return new Response(JSON.stringify({ok:false,error:"Untrusted event source."}), {status:403,headers});
  if (!env.LEAD_LOG) return new Response(JSON.stringify({ok:false,error:"Collector unavailable."}), {status:503,headers});
  let input: Record<string, unknown>;
  try { input = await request.json() as Record<string, unknown>; }
  catch { return new Response(JSON.stringify({ok:false,error:"Invalid event payload."}), {status:400,headers}); }
  const name = clean(input.name,64).toLowerCase().replace(/[^a-z0-9_]+/g,"_");
  if (!allowedEvents.has(name)) return new Response(JSON.stringify({ok:false,error:"Unsupported event."}), {status:422,headers});
  const rawPath = clean(input.path,512);
  const path = rawPath.startsWith("/") && !rawPath.includes("?") && !rawPath.includes("#") ? rawPath : "/";
  const session = clean(input.session,64).replace(/[^a-zA-Z0-9_-]/g,"");
  const props: Record<string,string> = {};
  if (input.props && typeof input.props === "object" && !Array.isArray(input.props)) {
    for (const [key,value] of Object.entries(input.props as Record<string,unknown>)) if (allowedProps.has(key)) props[key]=clean(value,120);
  }
  const receivedAt = new Date().toISOString();
  const id = `event:${receivedAt.slice(0,10)}:${crypto.randomUUID()}`;
  await env.LEAD_LOG.put(id, JSON.stringify({event_id:id,received_at:receivedAt,name,path,session,props,data_policy:"non_pii_allowlist_v1"}), {expirationTtl:34560000,metadata:{received_at:receivedAt,name,path}});
  return new Response(JSON.stringify({ok:true,event_id:id}), {status:202,headers});
};

export const onRequestOptions: PagesFunction = async () => new Response(null,{status:204,headers:{"Access-Control-Allow-Origin":"https://aicloudstrategist.com","Access-Control-Allow-Methods":"POST, OPTIONS","Access-Control-Allow-Headers":"Content-Type"}});

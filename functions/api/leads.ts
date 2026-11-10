type LeadDeskEnv = {
  CONTACT_LOG?: KVNamespace;
  LEAD_LOG?: KVNamespace;
  AICS_REPORT_TOKEN?: string;
  AICS_LEAD_DESK_ENABLED?: string;
};

const headers = {"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"};
const clean = (value: unknown, max = 512) => String(value ?? "").trim().slice(0,max);
const stages = new Set(["new","contacted","qualified","follow-up","proposal","won","lost"]);
const enabled = (env: LeadDeskEnv) => clean(env.AICS_LEAD_DESK_ENABLED).toLowerCase() === "true";
function authorized(request: Request, env: LeadDeskEnv) {
  const configured = clean(env.AICS_REPORT_TOKEN);
  const supplied = clean(request.headers.get("Authorization"), 520).replace(/^Bearer\s+/i, "");
  return Boolean(configured && supplied && configured === supplied);
}
function store(env: LeadDeskEnv) { return env.CONTACT_LOG || env.LEAD_LOG; }
function denied(env: LeadDeskEnv, request: Request) {
  if (!enabled(env)) return new Response(JSON.stringify({ok:false,error:"Lead Desk is disabled."}),{status:503,headers});
  if (!authorized(request,env)) return new Response(JSON.stringify({ok:false,error:"Unauthorized"}),{status:401,headers});
  if (!store(env)) return new Response(JSON.stringify({ok:false,error:"Lead store unavailable"}),{status:503,headers});
  return null;
}

export const onRequestGet: PagesFunction<LeadDeskEnv> = async ({request,env}) => {
  const failure=denied(env,request); if(failure) return failure;
  const kv=store(env)!; const leads: Record<string,unknown>[]=[]; let cursor: string|undefined;
  do {
    const page=await kv.list({prefix:"contact-",limit:200,cursor});
    for(const key of page.keys){const raw=await kv.get(key.name);if(raw){try{leads.push(JSON.parse(raw));}catch{}}}
    cursor=page.list_complete?undefined:page.cursor;
  } while(cursor && leads.length<1000);
  leads.sort((a,b)=>String(b.submitted_at||"").localeCompare(String(a.submitted_at||"")));
  return new Response(JSON.stringify({ok:true,master:"AICS Lead Desk",count:leads.length,leads}),{status:200,headers});
};

export const onRequestPatch: PagesFunction<LeadDeskEnv> = async ({request,env}) => {
  const failure=denied(env,request); if(failure) return failure;
  let input: Record<string,unknown>; try{input=await request.json() as Record<string,unknown>;}catch{return new Response(JSON.stringify({ok:false,error:"Invalid payload"}),{status:400,headers});}
  const id=clean(input.contact_id,200); const stage=clean(input.pipeline_stage,32).toLowerCase(); const owner=clean(input.owner,160);
  if(!id.startsWith("contact-")||!stages.has(stage)||!owner)return new Response(JSON.stringify({ok:false,error:"Valid contact_id, stage and owner are required"}),{status:422,headers});
  const kv=store(env)!; const raw=await kv.get(id); if(!raw)return new Response(JSON.stringify({ok:false,error:"Lead not found"}),{status:404,headers});
  const lead=JSON.parse(raw) as Record<string,unknown>; const history=Array.isArray(lead.history)?lead.history.slice(-49):[]; const at=new Date().toISOString();
  const updated={...lead,pipeline_stage:stage,owner,updated_at:at,history:[...history,{at,type:"stage-updated",stage,owner}]};
  await kv.put(id,JSON.stringify(updated),{expirationTtl:31536000,metadata:{submitted_at:String(lead.submitted_at||at),name:String(lead.name||"")}});
  return new Response(JSON.stringify({ok:true,lead:updated}),{status:200,headers});
};

export const onRequestOptions: PagesFunction = async () => new Response(null,{status:204,headers:{"Access-Control-Allow-Methods":"GET, PATCH, OPTIONS","Access-Control-Allow-Headers":"Authorization, Content-Type"}});

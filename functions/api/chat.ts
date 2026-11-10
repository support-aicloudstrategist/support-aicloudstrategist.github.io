type ChatEnv = { AICS_CHAT_ENABLED?: string };
const headers={"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"};
const clean=(v:unknown,max=600)=>String(v??"").trim().slice(0,max);
const approvedAnswers=[
 {terms:["service","diagnostic","what do you do"],answer:"AICS offers one public service: the Cloud & AI Cost Governance Diagnostic. It connects agreed cloud and AI spend to workloads, products, owners and evidence-backed next actions.",source:"/cloud-ai-cost-governance-diagnostic/"},
 {terms:["price","pricing","fee","cost"],answer:"Pricing is fixed-fee after scope. The fee depends on the agreed estate, billing period, evidence sources and decision question. AICS does not use a contingent savings fee.",source:"/cloud-ai-cost-governance-diagnostic/"},
 {terms:["turnaround","timeline","how long"],answer:"Typical turnaround is 10–15 business days after complete evidence intake. The exact delivery date is confirmed in scope.",source:"/cloud-ai-cost-governance-diagnostic/"},
 {terms:["fit","ideal customer","who is it for"],answer:"The diagnostic is designed for technology and finance leaders with material cloud, Kubernetes, GPU, model or data-platform spend and an ownership or cost decision that needs defensible evidence.",source:"/#fit"},
 {terms:["data","files","credentials","billing"],answer:"Do not submit billing files, credentials or confidential data through the website or chatbot. Initial contact uses non-sensitive context only; any later evidence route must be agreed separately.",source:"/trust-data-handling/"},
 {terms:["savings","guarantee","results"],answer:"AICS does not guarantee savings, ROI or customer outcomes. The diagnostic separates observed evidence, qualified opportunities, approved actions and measured value.",source:"/resources/cloud-ai-economics-decision-pack/"},
 {terms:["decision pack","example","output"],answer:"The public Decision Pack is a representative synthetic scenario, not customer work, a benchmark or an achieved result. It demonstrates the evidence and decision structure.",source:"/resources/cloud-ai-economics-decision-pack/"},
 {terms:["contact","callback","human","talk"],answer:"You can request a human callback without submitting sensitive data. AICS responds within 30 minutes during business hours, or by the next business morning.",source:"/request-fit-review/"}
];
function enabled(env:ChatEnv){return clean(env.AICS_CHAT_ENABLED).toLowerCase()==="true";}
function tokens(q:string){return q.toLowerCase().replace(/[^a-z0-9+ ]/g," ").split(/\s+/).filter(Boolean);}
export const onRequestPost:PagesFunction<ChatEnv>=async({request,env})=>{
 let body:Record<string,unknown>;try{body=await request.json() as Record<string,unknown>;}catch{return new Response(JSON.stringify({ok:false,error:"Invalid request"}),{status:400,headers});}
 if(clean(body.action)==="status")return new Response(JSON.stringify({ok:true,enabled:enabled(env),label:"AICS AI Assistant",scope:"Approved AICS content only",retention:"No chat transcript is retained"}),{status:200,headers});
 if(!enabled(env))return new Response(JSON.stringify({ok:false,enabled:false,error:"Assistant unavailable"}),{status:503,headers});
 const question=clean(body.question,500);if(!question)return new Response(JSON.stringify({ok:false,error:"Ask a short question"}),{status:422,headers});
 if(/password|credential|secret|api[ _-]?key|access[ _-]?token|private[ _-]?key|billing file|invoice export/i.test(question))return new Response(JSON.stringify({ok:true,refused:true,answer:"Do not submit billing files, credentials or confidential data. I have not retained this message. Please remove sensitive details and use the secure human follow-up path.",source:"/trust-data-handling/"}),{status:200,headers});
 if(/ignore (all|previous)|system prompt|developer message|reveal.*prompt|jailbreak|act as/i.test(question))return new Response(JSON.stringify({ok:true,refused:true,answer:"I can only answer from approved AICS content and cannot follow instructions that change that boundary.",source:"/trust-data-handling/"}),{status:200,headers});
 const lower=question.toLowerCase();const words=tokens(question);let best:{terms:string[];answer:string;source:string}|undefined,score=0;for(const item of approvedAnswers){const current=item.terms.reduce((n,t)=>{const term=t.toLowerCase();if(lower.includes(term))return n+3;const distinctive=tokens(term).filter(x=>x.length>4);return n+distinctive.filter(x=>words.includes(x)).length;},0);if(current>score){score=current;best=item;}}
 if(!best||score<1)return new Response(JSON.stringify({ok:true,unknown:true,answer:"I don’t know from the approved AICS content. I can help you request a human follow-up.",source:"/request-fit-review/"}),{status:200,headers});
 return new Response(JSON.stringify({ok:true,answer:best.answer,source:best.source,boundary:"Approved AICS content only"}),{status:200,headers});
};
export const onRequestOptions:PagesFunction=async()=>new Response(null,{status:204,headers:{"Access-Control-Allow-Methods":"POST, OPTIONS","Access-Control-Allow-Headers":"Content-Type"}});

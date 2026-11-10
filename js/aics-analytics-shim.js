(function(){
  var endpoint='/api/events';
  var allowedProps=new Set(['cta','destination','form','offer','section','source','status','provider','channel','campaign']);
  var aliases={'cta email click':'email_click','cta phone click':'phone_click','cta button click':'cta_click','contact form submit attempt':'form_submit_attempt','contact form submit success':'form_submit_success','contact form submit error':'form_submit_error'};
  function normalizeName(name){var raw=String(name||'event').toLowerCase().trim();return aliases[raw]||raw.replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');}
  function safeProps(input){var out={};Object.keys(input||{}).forEach(function(key){if(allowedProps.has(key))out[key]=String(input[key]==null?'':input[key]).slice(0,120);});return out;}
  function send(payload){if(location.hostname==='127.0.0.1'||location.hostname==='localhost')return;var body=JSON.stringify(payload);if(navigator.sendBeacon){try{if(navigator.sendBeacon(endpoint,new Blob([body],{type:'application/json'})))return;}catch(e){}}fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true,credentials:'same-origin'}).catch(function(){});}
  function record(name,options){var event={name:normalizeName(name),path:location.pathname,props:safeProps((options&&options.props)||{})};window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'aics_'+event.name,aics:event});send(event);}
  window.plausible=window.plausible||record;
  window.aicsAnalytics={track:record,mode:'first-party-anonymous',privacy:'no cookies, fingerprint or persistent visitor ID'};
  function acquisition(){var params=new URLSearchParams(location.search),host='';try{host=new URL(document.referrer).hostname.toLowerCase();}catch(e){}var provider=params.get('utm_source')||'';if(!provider){if(host.indexOf('chatgpt.com')>-1)provider='chatgpt';else if(host.indexOf('perplexity.ai')>-1)provider='perplexity';else if(host.indexOf('google.')>-1)provider='google';else if(host.indexOf('bing.com')>-1)provider='bing';else provider=host?'referral':'direct';}return{source:'browser',provider:provider.slice(0,120),channel:(params.get('utm_medium')||'organic_or_direct').slice(0,120),campaign:(params.get('utm_campaign')||'').slice(0,120)};}
  function start(){record('page_view',{props:acquisition()});if(location.pathname.indexOf('/resources/cloud-ai-economics-decision-pack')===0)record('decision_pack_view',{props:{section:'decision-pack'}});}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();

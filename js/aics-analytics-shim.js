(function(){
  var endpoint='/api/events';
  var allowedProps=new Set(['cta','destination','form','offer','section','source','status']);
  var aliases={'cta whatsapp click':'whatsapp_click','cta phone click':'phone_click','cta email click':'email_click','cta pricing click':'cta_click','cta free review click':'cta_click','cta button click':'cta_click','contact form submit attempt':'form_submit_attempt','contact form submit success':'form_submit_success','contact form submit error':'form_submit_error'};
  function sessionId(){var key='aics_measurement_session_v1';try{var value=sessionStorage.getItem(key);if(!value){value=(crypto.randomUUID?crypto.randomUUID():Math.random().toString(36).slice(2))+'-'+Date.now().toString(36);sessionStorage.setItem(key,value);}return value;}catch(e){return '';}}
  function normalizeName(name){var raw=String(name||'event').toLowerCase().trim();return aliases[raw]||raw.replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');}
  function safeProps(input){var out={};Object.keys(input||{}).forEach(function(key){if(allowedProps.has(key))out[key]=String(input[key]==null?'':input[key]).slice(0,120);});return out;}
  function send(payload){var body=JSON.stringify(payload);if(navigator.sendBeacon){try{if(navigator.sendBeacon(endpoint,new Blob([body],{type:'application/json'})))return;}catch(e){}}fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true,credentials:'same-origin'}).catch(function(){});}
  function record(name,options){var event={name:normalizeName(name),path:location.pathname,session:sessionId(),props:safeProps((options&&options.props)||{})};window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'aics_'+event.name,aics:event});send(event);}
  window.plausible=window.plausible||record;
  window.aicsAnalytics={track:record,mode:'first-party-kv',privacy:'non-PII allowlist'};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){record('page_view',{props:{source:'browser'}});},{once:true});else record('page_view',{props:{source:'browser'}});
})();

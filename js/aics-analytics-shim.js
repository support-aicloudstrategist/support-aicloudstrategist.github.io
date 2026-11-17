(function(){
  var endpoint='/api/events';
  var gaMeasurementId='G-5F6Y7JZFB5';
  var allowedProps=new Set(['cta','destination','form','offer','section','source','status','provider','channel','campaign','service','device','trigger','via','api']);
  var aliases={
    'cta whatsapp click':'whatsapp_click',
    'cta phone click':'phone_click',
    'cta email click':'email_click',
    'cta pricing click':'cta_click',
    'cta free review click':'cta_click',
    'cta button click':'cta_click',
    'contact form submit attempt':'form_submit_attempt',
    'contact form submit success':'form_submit_success',
    'contact form submit error':'form_submit_error',
    'fit review view':'fit_review_view',
    'chat open':'chat_open',
    'chat query':'chat_query'
  };
  function sessionId(){var key='aics_measurement_session_v1';try{var value=sessionStorage.getItem(key);if(!value){value=(crypto.randomUUID?crypto.randomUUID():Math.random().toString(36).slice(2))+'-'+Date.now().toString(36);sessionStorage.setItem(key,value);}return value;}catch(e){return '';}}
  function normalizeName(name){var raw=String(name||'event').toLowerCase().trim();return aliases[raw]||raw.replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');}
  function safeProps(input){var out={};Object.keys(input||{}).forEach(function(key){if(allowedProps.has(key))out[key]=String(input[key]==null?'':input[key]).slice(0,120);});return out;}
  function deviceClass(){var w=window.innerWidth||0;if(w<768)return 'mobile';if(w<1100)return 'tablet';return 'desktop';}
  function send(payload){if(location.hostname==='127.0.0.1'||location.hostname==='localhost')return;var body=JSON.stringify(payload);if(navigator.sendBeacon){try{if(navigator.sendBeacon(endpoint,new Blob([body],{type:'application/json'})))return;}catch(e){}}fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true,credentials:'same-origin'}).catch(function(){});}
  function record(name,options){
    var props=safeProps((options&&options.props)||{});
    if(!props.device)props.device=deviceClass();
    var event={name:normalizeName(name),path:location.pathname,session:sessionId(),props:props};
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:'aics_'+event.name,aics:event});
    if(typeof window.gtag==='function'&&event.name!=='page_view'){try{window.gtag('event',event.name,props);}catch(e){}}
    send(event);
  }
  window.plausible=window.plausible||record;
  window.aicsAnalytics={track:record,mode:'first-party-kv+ga4',privacy:'non-PII allowlist'};
  function loadGoogleAnalytics(){
    if(!/^G-[A-Z0-9]+$/i.test(gaMeasurementId))return;
    window.dataLayer=window.dataLayer||[];
    window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
    if(window.__AICS_GA4_INITIALIZED__)return;
    window.__AICS_GA4_INITIALIZED__=true;
    if(!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')){
      var gs=document.createElement('script');
      gs.async=true;
      gs.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(gaMeasurementId);
      document.head.appendChild(gs);
    }
    window.gtag('js',new Date());
    window.gtag('config',gaMeasurementId,{send_page_view:true,transport_type:'beacon'});
  }
  function acquisition(){var params=new URLSearchParams(location.search),host='';try{host=new URL(document.referrer).hostname.toLowerCase();}catch(e){}var provider=params.get('utm_source')||'';if(!provider){if(host.indexOf('chatgpt.com')>-1)provider='chatgpt';else if(host.indexOf('perplexity.ai')>-1)provider='perplexity';else if(host.indexOf('google.')>-1)provider='google';else if(host.indexOf('bing.com')>-1)provider='bing';else if(host.indexOf('claude.ai')>-1)provider='claude';else if(host.indexOf('gemini.google.com')>-1)provider='gemini';else provider=host?'referral':'direct';}var ft={utm_source:provider.slice(0,120),utm_medium:(params.get('utm_medium')||'organic_or_direct').slice(0,120),utm_campaign:(params.get('utm_campaign')||'').slice(0,120),gclid:(params.get('gclid')||'').slice(0,120),msclkid:(params.get('msclkid')||'').slice(0,120),li_fat_id:(params.get('li_fat_id')||'').slice(0,120),referrer:document.referrer.slice(0,240)};try{if(!sessionStorage.getItem('aics_first_touch_v1'))sessionStorage.setItem('aics_first_touch_v1',JSON.stringify(ft));}catch(e){}return{source:'browser',provider:ft.utm_source,channel:ft.utm_medium,campaign:ft.utm_campaign,device:deviceClass()};}
  function loadCloudflareWebAnalytics(){
    // Optional manual beacon if dashboard auto-inject is off. Token from meta only — never hardcode secrets in HTML if unused.
    if(document.querySelector('script[data-cf-beacon],script[src*="cloudflareinsights.com/beacon"]'))return;
    var meta=document.querySelector('meta[name="cf-web-analytics-token"]');
    var token=meta&&meta.getAttribute('content');
    if(!token||!/^[a-f0-9-]{20,64}$/i.test(token))return;
    var s=document.createElement('script');
    s.defer=true;
    s.src='https://static.cloudflareinsights.com/beacon.min.js';
    s.setAttribute('data-cf-beacon',JSON.stringify({token:token}));
    document.head.appendChild(s);
  }
  function boot(){
    loadGoogleAnalytics();
    loadCloudflareWebAnalytics();
    var acq=acquisition();
    record('page_view',{props:acq});
    var path=location.pathname.replace(/\/+$/,'')||'/';
    if(path==='/request-fit-review') record('fit_review_view',{props:{section:'fit-review',source:acq.provider||'direct'}});
    if(path==='/pricing') record('pricing_view',{props:{section:'pricing',source:acq.provider||'direct'}});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

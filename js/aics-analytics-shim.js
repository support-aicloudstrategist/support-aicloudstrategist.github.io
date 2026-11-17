(function(){
  var endpoint='/api/events';
  var gaMeasurementId='G-5F6Y7JZFB5';
  var allowedProps=new Set(['cta','destination','form','offer','section','source','status','provider','channel','campaign','service','device','trigger','via','api']);
  var aliases={
    'cta whatsapp click':'click_whatsapp',
    'cta phone click':'click_phone',
    'cta email click':'click_mailto',
    'cta pricing click':'cta_click',
    'cta free review click':'cta_click',
    'cta button click':'cta_click',
    'contact form submit attempt':'form_submit_attempt',
    'contact form submit success':'generate_lead',
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
  function acquisition(){var params=new URLSearchParams(location.search),host='';try{host=new URL(document.referrer).hostname.toLowerCase();}catch(e){}var provider=params.get('utm_source')||'';if(!provider){if(host.indexOf('chatgpt.com')>-1)provider='chatgpt';else if(host.indexOf('perplexity.ai')>-1)provider='perplexity';else if(host.indexOf('google.')>-1)provider='google';else if(host.indexOf('bing.com')>-1)provider='bing';else if(host.indexOf('claude.ai')>-1)provider='claude';else if(host.indexOf('gemini.google.com')>-1)provider='gemini';else if(host&&host.indexOf('aicloudstrategist.')===-1)provider='referral';else provider='direct';}var ft={landing_page:location.origin+location.pathname,utm_source:provider.slice(0,120),utm_medium:(params.get('utm_medium')||(provider==='direct'?'direct':'organic_or_referral')).slice(0,120),utm_campaign:(params.get('utm_campaign')||'').slice(0,120),gclid:(params.get('gclid')||'').slice(0,120),msclkid:(params.get('msclkid')||'').slice(0,120),li_fat_id:(params.get('li_fat_id')||'').slice(0,120),referrer:(host&&host.indexOf('aicloudstrategist.')===-1?document.referrer:'').slice(0,240)};try{var saved=sessionStorage.getItem('aics_first_touch_v1');if(saved){ft=JSON.parse(saved);}else{sessionStorage.setItem('aics_first_touch_v1',JSON.stringify(ft));}}catch(e){}window.aicsAttribution=ft;return{source:'browser',provider:ft.utm_source,channel:ft.utm_medium,campaign:ft.utm_campaign,device:deviceClass()};}
  function bindStandardClickEvents(){
    document.addEventListener('click',function(ev){
      var a=ev.target&&ev.target.closest?ev.target.closest('a[href]'):null;
      if(!a)return;
      var href=String(a.getAttribute('href')||'');
      if(href.indexOf('mailto:')===0)record('click_mailto',{props:{destination:href.slice(0,120),section:'contact'}});
      else if(href.indexOf('tel:')===0)record('click_phone',{props:{destination:href.slice(0,120),section:'contact'}});
      else if(href.indexOf('wa.me/')>-1||href.indexOf('whatsapp')>-1)record('click_whatsapp',{props:{destination:href.slice(0,120),section:'contact'}});
      else if(href.indexOf('cal.com/')>-1)record('cta_click',{props:{cta:'calcom_booking',destination:href.slice(0,120),section:'booking'}});
    },{passive:true});
  }
  function bindQuickForms(){
    document.querySelectorAll('form[data-aics-quick-form]').forEach(function(qf){
      qf.addEventListener('submit',function(ev){
        ev.preventDefault();
        var note=qf.querySelector('[data-quick-status]');
        var btn=qf.querySelector('button[type="submit"]');
        var fd=new FormData(qf);
        var ft=window.aicsAttribution||{};
        var payload={
          name:fd.get('name')||'',
          contact:fd.get('contact')||'',
          company:fd.get('company')||'',
          need:fd.get('need')||'Cloud spend or ownership question from guide',
          message:fd.get('message')||'',
          service:'Cloud & AI Cost Governance Diagnostic',
          stage:'Guide quick enquiry',
          privacy_consent:fd.get('privacy_consent')?'yes':'',
          company_website:fd.get('company_website')||'',
          landing_page:ft.landing_page||(location.origin+location.pathname),
          referrer:ft.referrer||document.referrer||'',
          utm_source:ft.utm_source||'',
          utm_medium:ft.utm_medium||'',
          utm_campaign:ft.utm_campaign||'',
          gclid:ft.gclid||'',
          msclkid:ft.msclkid||'',
          li_fat_id:ft.li_fat_id||''
        };
        record('form_submit_attempt',{props:{form:'guide_quick_enquiry',section:'resource'}});
        if(btn){btn.disabled=true;btn.textContent='Sending…';}
        fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(function(r){return r.json().then(function(j){return{ok:r.ok&&j.ok,j:j};});}).then(function(res){
          if(!res.ok)throw new Error((res.j&&res.j.error)||'Failed');
          if(note){note.hidden=false;note.textContent='Recorded ('+(res.j.contact_id||'ok')+'). We reply within 1 business day — or pick a 30-min slot on Cal.com above.';}
          qf.reset();
          record('generate_lead',{props:{form:'guide_quick_enquiry',section:'resource'}});
        }).catch(function(){
          if(note){note.hidden=false;note.textContent='Could not send right now — please use the 30-min Cal.com link above or email contact@aicloudstrategist.com.';}
          record('form_submit_error',{props:{form:'guide_quick_enquiry',section:'resource'}});
        }).finally(function(){if(btn){btn.disabled=false;btn.textContent='Send question';}});
      });
    });
  }
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
    bindStandardClickEvents();
    bindQuickForms();
    record('page_view',{props:acq});
    var path=location.pathname.replace(/\/+$/,'')||'/';
    if(path==='/request-fit-review') record('fit_review_view',{props:{section:'fit-review',source:acq.provider||'direct'}});
    if(path==='/pricing') record('pricing_view',{props:{section:'pricing',source:acq.provider||'direct'}});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

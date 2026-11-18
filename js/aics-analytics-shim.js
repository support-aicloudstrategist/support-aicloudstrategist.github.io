(function(){
  var endpoint='/api/events';
  var gaMeasurementId='G-5F6Y7JZFB5';
  var allowedProps=new Set(['cta','destination','form','offer','section','source','status','provider','channel','campaign','service','device','browser','country','visitor','visitor_kind','trigger','via','api','depth','seconds']);
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
  function sessionId(){
    var key='aics_measurement_session_v1';
    try{
      var value=sessionStorage.getItem(key);
      if(!value){
        value=(crypto.randomUUID?crypto.randomUUID():Math.random().toString(36).slice(2))+'-'+Date.now().toString(36);
        sessionStorage.setItem(key,value);
      }
      return value;
    }catch(e){return '';}
  }
  function visitorId(){
    var key='aics_measurement_visitor_v1';
    try{
      var existing=localStorage.getItem(key);
      if(existing) return {id:existing,kind:'returning'};
      var id=(crypto.randomUUID?crypto.randomUUID():Math.random().toString(36).slice(2))+'-'+Date.now().toString(36);
      localStorage.setItem(key,id);
      return {id:id,kind:'new'};
    }catch(e){return {id:'',kind:'unknown'};}
  }
  function normalizeName(name){
    var raw=String(name||'event').toLowerCase().trim();
    return aliases[raw]||raw.replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');
  }
  function safeProps(input){
    var out={};
    Object.keys(input||{}).forEach(function(key){
      if(allowedProps.has(key)) out[key]=String(input[key]==null?'':input[key]).slice(0,120);
    });
    return out;
  }
  function deviceClass(){
    var w=window.innerWidth||0;
    if(w<768) return 'mobile';
    if(w<1100) return 'tablet';
    return 'desktop';
  }
  function browserClass(){
    var ua=(navigator.userAgent||'').toLowerCase();
    if(ua.indexOf('edg/')>-1) return 'edge';
    if(ua.indexOf('chrome/')>-1) return 'chrome';
    if(ua.indexOf('safari/')>-1) return 'safari';
    if(ua.indexOf('firefox/')>-1) return 'firefox';
    return 'other';
  }
  function send(payload){
    if(location.hostname==='127.0.0.1'||location.hostname==='localhost') return;
    var body=JSON.stringify(payload);
    if(navigator.sendBeacon){
      try{ if(navigator.sendBeacon(endpoint,new Blob([body],{type:'application/json'}))) return; }catch(e){}
    }
    fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true,credentials:'same-origin'}).catch(function(){});
  }
  function record(name,options){
    var props=safeProps((options&&options.props)||{});
    if(!props.device) props.device=deviceClass();
    if(!props.browser) props.browser=browserClass();
    var visitor=visitorId();
    if(visitor.id && !props.visitor) props.visitor=visitor.id;
    if(!props.visitor_kind) props.visitor_kind=visitor.kind;
    var event={name:normalizeName(name),path:location.pathname,session:sessionId(),props:props};
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:'aics_'+event.name,aics:event});
    if(typeof window.gtag==='function'&&event.name!=='page_view'){try{window.gtag('event',event.name,props);}catch(e){}}
    send(event);
  }
  window.plausible=window.plausible||record;
  window.aicsAnalytics={track:record,mode:'first-party-kv+ga4',privacy:'non-PII allowlist — no emails from passive browsing'};
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
  function acquisition(){
    var params=new URLSearchParams(location.search),host='';
    try{host=new URL(document.referrer).hostname.toLowerCase();}catch(e){}
    var provider=params.get('utm_source')||'';
    if(!provider){
      if(host.indexOf('chatgpt.com')>-1) provider='chatgpt';
      else if(host.indexOf('perplexity.ai')>-1) provider='perplexity';
      else if(host.indexOf('google.')>-1) provider='google';
      else if(host.indexOf('bing.com')>-1) provider='bing';
      else if(host.indexOf('linkedin.')>-1) provider='linkedin';
      else if(host.indexOf('twitter.')>-1||host.indexOf('x.com')>-1) provider='twitter';
      else if(host.indexOf('facebook.')>-1) provider='facebook';
      else if(host.indexOf('claude.ai')>-1) provider='claude';
      else if(host.indexOf('gemini.google.com')>-1) provider='gemini';
      else provider=host?'referral':'direct';
    }
    var ft={
      landing_page:location.origin+location.pathname,
      utm_source:provider.slice(0,120),
      utm_medium:(params.get('utm_medium')||'organic_or_direct').slice(0,120),
      utm_campaign:(params.get('utm_campaign')||'').slice(0,120),
      gclid:(params.get('gclid')||'').slice(0,120),
      msclkid:(params.get('msclkid')||'').slice(0,120),
      li_fat_id:(params.get('li_fat_id')||'').slice(0,120),
      referrer:document.referrer.slice(0,240)
    };
    try{ var sv=sessionStorage.getItem('aics_first_touch_v1'); if(sv) ft=JSON.parse(sv); else sessionStorage.setItem('aics_first_touch_v1',JSON.stringify(ft)); }catch(e){}
    window.aicsAttribution=ft;
    return {
      source:'browser',
      provider:ft.utm_source,
      channel:ft.utm_medium,
      campaign:ft.utm_campaign,
      device:deviceClass(),
      browser:browserClass()
    };
  }
  function loadCloudflareWebAnalytics(){
    if(document.querySelector('script[data-cf-beacon],script[src*="cloudflareinsights.com/beacon"]')) return;
    var meta=document.querySelector('meta[name="cf-web-analytics-token"]');
    var token=meta&&meta.getAttribute('content');
    if(!token||!/^[a-f0-9-]{20,64}$/i.test(token)) return;
    var s=document.createElement('script');
    s.defer=true;
    s.src='https://static.cloudflareinsights.com/beacon.min.js';
    s.setAttribute('data-cf-beacon',JSON.stringify({token:token}));
    document.head.appendChild(s);
  }
  function trackEngagement(){
    var marks={25:false,50:false,75:false,100:false};
    var dwellSeconds=0;
    var dwellTimer=null;
    function scrollRatio(){
      var doc=document.documentElement;
      var top=window.scrollY||doc.scrollTop||0;
      var height=Math.max(doc.scrollHeight-window.innerHeight,1);
      return top/height;
    }
    function onScroll(){
      var ratio=scrollRatio();
      [25,50,75,100].forEach(function(mark){
        if(!marks[mark] && ratio*100>=mark){
          marks[mark]=true;
          record('scroll_depth',{props:{depth:String(mark),section:location.pathname}});
        }
      });
    }
    function tickDwell(){
      if(document.visibilityState!=='visible') return;
      dwellSeconds+=30;
      if(dwellSeconds===30||dwellSeconds===60||dwellSeconds===120||dwellSeconds%180===0){
        record('dwell_tick',{props:{seconds:String(dwellSeconds)}});
      }
      // Presence every 30s keeps realtime useful without flooding KV.
      record('presence_ping',{props:{seconds:String(dwellSeconds),trigger:'heartbeat'}});
    }
    window.addEventListener('scroll',onScroll,{passive:true});
    onScroll();
    dwellTimer=window.setInterval(tickDwell,30000);
    if(document.visibilityState==='visible'){
      record('presence_ping',{props:{seconds:'0',trigger:'enter'}});
    }
    document.addEventListener('visibilitychange',function(){
      if(document.visibilityState==='hidden' && dwellSeconds>0){
        record('dwell_tick',{props:{seconds:String(dwellSeconds),trigger:'hide'}});
      }
    });
    window.addEventListener('beforeunload',function(){
      if(dwellTimer) window.clearInterval(dwellTimer);
    });
  }
  function trackClicks(){
    document.addEventListener('click',function(event){
      var target=event.target;
      if(!target||!target.closest) return;
      var cta=target.closest('[data-aics-cta]');
      if(cta){
        record('cta_click',{props:{cta:cta.getAttribute('data-aics-cta')||'cta',destination:(cta.getAttribute('href')||'').slice(0,120)}});
        return;
      }
      var link=target.closest('a[href]');
      if(!link) return;
      var href=link.getAttribute('href')||'';
      if(href.indexOf('mailto:')===0){record('email_click',{props:{destination:href.slice(0,120),section:'contact'}});record('click_mailto',{props:{destination:href.slice(0,120),section:'contact'}});return;}
      if(href.indexOf('tel:')===0){record('phone_click',{props:{destination:href.slice(0,120),section:'contact'}});record('click_phone',{props:{destination:href.slice(0,120),section:'contact'}});return;}
      if(href.indexOf('wa.me/')>-1||href.indexOf('whatsapp')>-1){record('whatsapp_click',{props:{destination:href.slice(0,120),section:'contact'}});record('click_whatsapp',{props:{destination:href.slice(0,120),section:'contact'}});return;}
      if(href.indexOf('cal.com/')>-1){record('cta_click',{props:{cta:'calcom_booking',destination:href.slice(0,120),section:'booking'}});return;}
      var download=link.hasAttribute('download')||/\.(pdf|docx?|xlsx?|csv|zip)(\?|$)/i.test(href);
      if(download){
        record('download_click',{props:{destination:href.slice(0,120),cta:link.textContent?link.textContent.trim().slice(0,80):'download'}});
        return;
      }
      if(link.classList.contains('button')||link.classList.contains('btn')){
        record('button_click',{props:{cta:(link.textContent||'button').trim().slice(0,80),destination:href.slice(0,120)}});
      }
    },true);
  }
  function boot(){
    loadGoogleAnalytics();
    loadCloudflareWebAnalytics();
    var acq=acquisition();
    record('page_view',{props:acq});
    var path=location.pathname.replace(/\/+$/,'')||'/';
    if(path==='/request-fit-review') record('fit_review_view',{props:{section:'fit-review',source:acq.provider||'direct'}});
    if(path==='/pricing') record('pricing_view',{props:{section:'pricing',source:acq.provider||'direct'}});
    trackEngagement();
    trackClicks();
    // Contact / quick-form submit + success modal live in /js/aics-form-success.js
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot,{once:true});
  else boot();
})();

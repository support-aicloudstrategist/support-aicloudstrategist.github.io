(function(){
  function now(){return new Date().toISOString();}
  function currentAttribution(){
    var params=new URLSearchParams(location.search);
    var referrer='';
    try{if(document.referrer){var ref=new URL(document.referrer);referrer=ref.origin+ref.pathname;}}catch(e){}
    return {
      landing_page:location.origin+location.pathname,
      referrer:referrer,
      utm_source:params.get('utm_source')||'',
      utm_medium:params.get('utm_medium')||'',
      utm_campaign:params.get('utm_campaign')||'',
      captured_at:now()
    };
  }
  function firstTouch(){
    var key='aics:first-touch:v1', value=null;
    try{value=JSON.parse(sessionStorage.getItem(key)||'null');}catch(e){}
    if(!value||!value.landing_page){
      value=currentAttribution();
      try{sessionStorage.setItem(key,JSON.stringify(value));}catch(e){}
    }
    return value;
  }
  window.aicsAttribution=firstTouch();
  function safeText(el){return (el.getAttribute('aria-label') || el.innerText || el.textContent || '').trim().slice(0,120);}
  function eventNameFor(a){
    var href=(a.getAttribute('href')||'').toLowerCase();
    if(href.indexOf('wa.me/')>-1 || href.indexOf('whatsapp')>-1) return 'CTA WhatsApp Click';
    if(href.indexOf('tel:')===0) return 'CTA Phone Click';
    if(href.indexOf('mailto:')===0) return 'CTA Email Click';
    if(href.indexOf('/free-business-review')>-1) return 'CTA Free Review Click';
    if(href.indexOf('/pricing')>-1) return 'CTA Pricing Click';
    if(a.hasAttribute('data-aics-cta') || (a.classList && (a.classList.contains('btn') || a.classList.contains('aics-nav-cta')))) return 'CTA Button Click';
    return null;
  }
  function send(name, props){
    props=props||{};
    props.page=location.pathname;
    props.ts=now();
    if(window.aicsAnalytics&&window.aicsAnalytics.track){try{window.aicsAnalytics.track(name,{props:props});}catch(e){}} else if(window.plausible){ try{ window.plausible(name,{props:props}); }catch(e){} }
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:name.replace(/\s+/g,'_').toLowerCase(), aics:name, aics_props:props});
  }
  document.addEventListener('click', function(e){
    var a=e.target.closest && e.target.closest('a[href]');
    if(!a) return;
    var name=eventNameFor(a);
    if(!name) return;
    send(name,{href:a.href, text:safeText(a), cta:a.getAttribute('data-aics-cta')||'', section:(a.closest('section')||{}).className||''});
  }, true);
  document.addEventListener('submit', function(e){
    var f=e.target;
    if(!f || !f.tagName || f.tagName.toLowerCase()!=='form') return;
    send('Form Submit Attempt',{action:f.action||'', id:f.id||'', name:f.getAttribute('name')||''});
  }, true);
  window.aicsTrack=send;
})();

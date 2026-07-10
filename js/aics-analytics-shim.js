(function(){
  function record(name, options){
    var props=(options&&options.props)||{};
    var event={name:String(name||'event'),props:props,page:location.pathname,url:location.href,ts:new Date().toISOString()};
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:'aics_'+event.name.toLowerCase().replace(/[^a-z0-9]+/g,'_'),aics:event});
    try{
      var key='aics_recent_events';
      var arr=JSON.parse(localStorage.getItem(key)||'[]');
      arr.push(event); localStorage.setItem(key, JSON.stringify(arr.slice(-50)));
    }catch(e){}
    if(window.console && location.search.indexOf('debug_aics=1')>-1) console.log('[AICS event]', event);
  }
  window.plausible = window.plausible || record;
  window.aicsAnalytics = {track:record, mode:'local-failsafe', note:'Server analytics endpoint intentionally not called from the browser until a healthy collector is available.'};
})();

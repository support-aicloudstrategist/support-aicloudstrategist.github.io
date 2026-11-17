/**
 * Form-less visitor ID client (AI Cloud Strategist).
 * MIT-style self-contained fingerprint + behavioral beacon → /api/identify
 * Does not load any third-party identification SaaS.
 */
(function () {
  'use strict';
  if (window.__AICS_VISITOR_ID_INIT__) return;
  window.__AICS_VISITOR_ID_INIT__ = true;

  var started = Date.now();
  var scrollMax = 0;
  var clicks = 0;
  var pages = 1;
  try {
    pages = Number(sessionStorage.getItem('aics_pages_seen') || '0') + 1;
    sessionStorage.setItem('aics_pages_seen', String(pages));
  } catch (e) {}

  function deviceClass() {
    var w = window.innerWidth || 0;
    if (w < 768) return 'mobile';
    if (w < 1024) return 'tablet';
    return 'desktop';
  }

  function canvasSignal() {
    try {
      var c = document.createElement('canvas');
      c.width = 240; c.height = 60;
      var ctx = c.getContext('2d');
      if (!ctx) return '';
      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillStyle = '#f60';
      ctx.fillRect(0, 0, 240, 60);
      ctx.fillStyle = '#069';
      ctx.fillText('AICS-fp-' + (navigator.language || ''), 2, 2);
      ctx.strokeStyle = '#ff0';
      ctx.beginPath(); ctx.arc(50, 30, 20, 0, Math.PI * 2); ctx.stroke();
      return c.toDataURL().slice(-96);
    } catch (e) { return ''; }
  }

  function webglSignal() {
    try {
      var c = document.createElement('canvas');
      var gl = c.getContext('webgl') || c.getContext('experimental-webgl');
      if (!gl) return '';
      var dbg = gl.getExtension('WEBGL_debug_renderer_info');
      var vendor = dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : '';
      var renderer = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : '';
      return String(vendor) + '|' + String(renderer);
    } catch (e) { return ''; }
  }

  function sha256Hex(str) {
    if (!window.crypto || !window.crypto.subtle || !window.TextEncoder) {
      var h = 2166136261;
      for (var i = 0; i < str.length; i++) {
        h ^= str.charCodeAt(i);
        h = Math.imul(h, 16777619);
      }
      return ('00000000' + (h >>> 0).toString(16)).slice(-8) + ('00000000' + str.length.toString(16)).slice(-8);
    }
    return window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(str)).then(function (buf) {
      return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('').slice(0, 32);
    });
  }

  function buildFingerprintRaw() {
    var nav = navigator || {};
    var scr = window.screen || {};
    return [
      nav.userAgent || '',
      nav.language || '',
      (nav.languages || []).join(','),
      nav.platform || '',
      nav.hardwareConcurrency || '',
      nav.deviceMemory || '',
      nav.maxTouchPoints || '',
      scr.width + 'x' + scr.height + 'x' + (scr.colorDepth || ''),
      String(new Date().getTimezoneOffset()),
      Intl.DateTimeFormat().resolvedOptions().timeZone || '',
      canvasSignal(),
      webglSignal(),
      deviceClass()
    ].join('||');
  }

  function savedIdentity() {
    try { return JSON.parse(localStorage.getItem('aics_visitor_identity_v1') || '{}'); }
    catch (e) { return {}; }
  }

  function beacon(extra) {
    var id = savedIdentity();
    var payload = Object.assign({
      fingerprint: window.__aicsFingerprint || '',
      page: location.pathname,
      url: location.href,
      referrer: document.referrer || '',
      deviceClass: deviceClass(),
      scrollMax: scrollMax,
      dwellMs: Math.max(0, Date.now() - started),
      pages: pages,
      clicks: clicks,
      chatTurns: Number(sessionStorage.getItem('aics_chat_turns') || '0') || 0,
      name: id.name || '',
      email: id.email || '',
      phone: id.phone || '',
      company: id.company || '',
      contact_source: (extra && extra.contact_source) || (id.email || id.phone || id.name ? 'progressive_chat' : 'browse_enrichment')
    }, extra || {});
    return fetch('/api/identify', {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify(payload),
      keepalive: true,
      credentials: 'same-origin'
    }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (data) {
        if (data && data.ok) {
          window.__aicsIdentify = data;
          try {
            localStorage.setItem('aics_visitor_enrichment_v1', JSON.stringify({
              at: new Date().toISOString(),
              vid: data.vid,
              fingerprint: data.fingerprint,
              geo: data.geo,
              identity: data.identity
            }));
          } catch (e) {}
          if (data.geo && data.geo.asnOrg && window.aicsStitchIdentity) {
            var cur = savedIdentity();
            if (!cur.company) window.aicsStitchIdentity({ company: data.geo.asnOrg });
          }
        }
        return data;
      }).catch(function () { return null; });
  }

  window.aicsIdentifyBeacon = beacon;

  // WhatsApp click-to-chat attribution: encode visitorId + path + UTMs into prefilled text.
  function firstTouch() {
    try {
      return JSON.parse(sessionStorage.getItem('aics_first_touch_v1') || localStorage.getItem('aics_first_touch_v1') || '{}');
    } catch (e) { return {}; }
  }
  function buildAicsWhatsAppHref(intent) {
    var ft = firstTouch();
    var parts = [String(intent || 'Hi AICloudStrategist, I want ownership-first FinOps notes').trim()];
    parts.push('vid:' + String(window.aicsVisitorId || '').slice(0, 16));
    parts.push('p:' + String(location.pathname || '/').slice(0, 80));
    if (ft.utm_source) parts.push('src:' + String(ft.utm_source).slice(0, 40));
    if (ft.utm_campaign) parts.push('cmp:' + String(ft.utm_campaign).slice(0, 40));
    if (ft.gclid) parts.push('gclid:1');
    return 'https://wa.me/918796302608?text=' + encodeURIComponent(parts.join(' | '));
  }
  window.aicsWhatsAppHref = buildAicsWhatsAppHref;
  function decorateAicsWhatsAppLinks() {
    document.querySelectorAll('a[href*="wa.me/918796302608"]').forEach(function (link) {
      if (link.getAttribute('data-aics-wa-decorated') === '1') return;
      var intent = 'Hi AICloudStrategist, I want ownership-first FinOps notes';
      try {
        var u = new URL(link.getAttribute('href') || '', location.origin);
        var existing = u.searchParams.get('text');
        if (existing) intent = existing.split(' | vid:')[0].split(' | p:')[0].trim() || intent;
      } catch (e) {}
      link.setAttribute('href', buildAicsWhatsAppHref(intent));
      link.setAttribute('data-aics-wa-decorated', '1');
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', decorateAicsWhatsAppLinks);
  } else {
    decorateAicsWhatsAppLinks();
  }
  document.addEventListener('click', function (ev) {
    var link = ev.target && ev.target.closest && ev.target.closest('a[href*="wa.me/918796302608"]');
    if (!link) return;
    var intent = 'Hi AICloudStrategist, I want ownership-first FinOps notes';
    try {
      var u = new URL(link.getAttribute('href') || '', location.origin);
      var t = u.searchParams.get('text') || '';
      intent = t.split(' | vid:')[0].split(' | p:')[0].trim() || intent;
    } catch (e) {}
    link.setAttribute('href', buildAicsWhatsAppHref(intent));
    beacon({ contact_source: 'whatsapp_click' });
  }, true);

  window.addEventListener('scroll', function () {
    var doc = document.documentElement;
    var max = Math.max(doc.scrollHeight - window.innerHeight, 1);
    scrollMax = Math.max(scrollMax, Math.round((window.scrollY / max) * 100));
  }, { passive: true });
  window.addEventListener('click', function () { clicks += 1; }, { passive: true });

  Promise.resolve(sha256Hex(buildFingerprintRaw())).then(function (fp) {
    window.__aicsFingerprint = fp;
    try { localStorage.setItem('aics_fp_v1', fp); } catch (e) {}
    beacon({ contact_source: 'browse_enrichment' });
    setTimeout(function () { beacon({ contact_source: 'browse_enrichment' }); }, 25000);
  });

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') beacon({ contact_source: 'browse_enrichment' });
  });
})();

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

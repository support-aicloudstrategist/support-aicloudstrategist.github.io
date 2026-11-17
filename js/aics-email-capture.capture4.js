/*
 * AICloudStrategist FinOps lead-gen layer (AICS only; WhatsApp 918796302608).
 * - Page-specific offer context (comparison / commercial / guide / triage / PDF pages)
 * - Sticky Book + WhatsApp bar on commercial FinOps landers
 * - Scroll-triggered soft capture (non-modal): free triage / comparison PDF + WhatsApp path
 * - Exit-intent modal copy is page-specific (read lazily via window.aicsFinopsContext)
 */
(() => {
  if (window.__AICS_FINOPS_LEADGEN__) return;
  window.__AICS_FINOPS_LEADGEN__ = true;

  const WA = "918796302608";
  const BOOK = "/request-fit-review/";
  const TRIAGE = "/cloud-waste-triage/";
  const PDF = "/get/finops-comparison-onepager/";

  const normPath = (raw) => {
    let p = String(raw || window.location.pathname || "/").replace(/\/index\.html$/, "/").replace(/\.html$/, "");
    p = p.replace(/\/+$/, "");
    return p || "/";
  };
  const waHref = (text) => `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;

  const COMPARE = [
    "/aws-cost-explorer-alternatives", "/azure-cost-management-alternatives", "/finops-diagnostic-vs-cloud-cost-tools",
    "/prosperops-alternatives", "/cloudability-alternatives",
    "/resources/why-fixed-fee-diagnostics-beat-savings-share",
    "/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison",
  ];
  const COMMERCIAL = [
    "/aws-cost-optimization", "/azure-cost-optimization", "/gcp-cost-optimization", "/kubernetes-cost-allocation",
    "/cloud-cost-optimization", "/cloud-cost-audit", "/cloud-cost-governance", "/enterprise-cloud-cost-optimization",
    "/finops-consulting", "/finops-services-india", "/reduce-cloud-spend",
  ];
  const GUIDES = [
    "/resources/how-to-read-a-cloud-bill", "/resources/what-is-cloud-cost-ownership",
    "/resources/kubernetes-eks-aks-gke-cost-allocation-guide", "/resources/gpu-and-llm-inference-cost-governance",
    "/resources/cloud-cogs-for-the-board-and-saas-gross-margin", "/resources/ai-agent-and-cloud-automation-cost-checklist",
    "/resources/sample-diagnostic-deliverable",
  ];

  const context = (rawPath) => {
    const p = normPath(rawPath);
    const slug = p.replace(/^\//, "").replace(/^resources\//, "").replace(/-/g, " ");
    const triageNudge = (title, body) => ({
      eyebrow: "Free · 2 minutes · result before any ask",
      title,
      body,
      primary: { label: "Run the free waste triage", href: TRIAGE },
      secondary: { label: "FinOps comparison PDF", href: PDF },
      waLabel: "Ask on WhatsApp",
      waText: `Hi AICloudStrategist, I read the ${slug} page and want the cloud waste checklist`,
    });
    if (COMPARE.includes(p)) {
      return {
        kind: "compare", path: p,
        stickyLabel: "Comparing FinOps options?",
        stickyExtra: { label: "Free PDF", href: PDF },
        waText: `Hi AICloudStrategist, I read the ${slug} comparison and want the one-pager PDF`,
        nudge: {
          eyebrow: "Comparing options? Free one-pager",
          title: "Take the honest comparison with you",
          body: "Native consoles vs FinOps platforms vs savings-share vs a fixed-fee diagnostic: strengths, limits and when each fits. Preview is free; WhatsApp unlocks the PDF.",
          primary: { label: "Preview the comparison PDF", href: PDF },
          secondary: { label: "Free waste triage", href: TRIAGE },
          waLabel: "Ask on WhatsApp",
          waText: `Hi AICloudStrategist, please send the FinOps comparison one-pager PDF (from ${p})`,
        },
        exit: {
          eyebrow: "Before you go",
          title: "Take the FinOps comparison with you",
          lead: `One page: Cost Explorer vs FinOps platforms vs savings-share vs a fixed-fee diagnostic. WhatsApp is fastest in India, or leave a work email. Opt-in only; the <a href="${PDF}">preview</a> is free.`,
          waLabel: "Get the PDF on WhatsApp",
          waText: `Hi AICloudStrategist, please send the FinOps comparison one-pager PDF (from ${p})`,
          submitLabel: "Send me the comparison PDF",
          extra: { label: "Or run the free waste triage", href: TRIAGE },
          need: "FinOps comparison one-pager (exit/scroll capture)",
        },
      };
    }
    if (COMMERCIAL.includes(p)) {
      return {
        kind: "commercial", path: p,
        stickyLabel: "Cut cloud waste, fixed fee:",
        stickyExtra: { label: "Free triage", href: TRIAGE },
        waText: `Hi AICloudStrategist, I read the ${slug} page and want to discuss my cloud spend`,
        nudge: triageNudge("Where is your cloud waste, really?", "Answer 4 questions and see your priority band first. Want the 1-page checklist for your result? Ask on WhatsApp. No forms, no billing files."),
        exit: {
          eyebrow: "Before you go",
          title: "Get your cloud waste priority first",
          lead: `The free <a href="${TRIAGE}">4-question waste triage</a> shows your priority band before we ask for anything. Prefer a human? WhatsApp us “triage” and we reply with a 1-page checklist. Opt-in only.`,
          waLabel: "WhatsApp “triage”",
          waText: `Hi AICloudStrategist, I want the cloud waste triage checklist (from ${p})`,
          submitLabel: "Send the waste checklist",
          extra: { label: "Run the 2-min triage", href: TRIAGE },
          need: "Cloud waste triage checklist (exit/scroll capture)",
        },
      };
    }
    if (GUIDES.includes(p)) {
      return {
        kind: "guide", path: p,
        stickyLabel: "Apply this to your estate:",
        stickyExtra: { label: "Free triage", href: TRIAGE },
        waText: `Hi AICloudStrategist, I read the ${slug} guide and want a next-step note`,
        nudge: triageNudge("Turn this guide into a result", "Run the free waste triage (2 minutes) and see which of these levers to pull first. Then ask on WhatsApp for the matching 1-page checklist."),
        exit: {
          eyebrow: "Before you go",
          title: "Which lever should you pull first?",
          lead: `Run the free <a href="${TRIAGE}">cloud waste triage</a> (result first), or WhatsApp us your cloud and biggest cost pain and we reply with a 1-page checklist. Opt-in only.`,
          waLabel: "WhatsApp your cost pain",
          waText: `Hi AICloudStrategist, I read the ${slug} guide and want the cloud waste checklist`,
          submitLabel: "Send the checklist",
          extra: { label: "Run the 2-min triage", href: TRIAGE },
          need: "Cloud waste triage checklist (guide exit/scroll capture)",
        },
      };
    }
    if (p === "/cloud-waste-triage") {
      return {
        kind: "triage", path: p, noNudge: true,
        stickyLabel: "Prefer to talk it through?",
        waText: "Hi AICloudStrategist, I am doing the cloud waste triage and have a question",
        exit: {
          eyebrow: "Before you go",
          title: "Want the checklist for your result?",
          lead: "Finish the triage to see your priority band first. Or WhatsApp us your cloud and biggest pain and we reply with a 1-page checklist. Opt-in only.",
          waLabel: "WhatsApp for the checklist",
          waText: "Hi AICloudStrategist, I want the cloud waste triage checklist",
          submitLabel: "Send the waste checklist",
          extra: { label: "Compare FinOps options (PDF)", href: PDF },
          need: "Cloud waste triage checklist (triage page exit capture)",
        },
      };
    }
    if (p === "/get/finops-comparison-onepager" || p === "/get/cost-alert-triage-onepager") {
      return {
        kind: "pdf", path: p, noNudge: true,
        stickyLabel: "Prefer WhatsApp for the PDF?",
        waText: "Hi AICloudStrategist, please send the one-pager PDF",
        exit: {
          eyebrow: "Before you go",
          title: "Get the PDF on WhatsApp instead",
          lead: `Skip the form: WhatsApp us and we send the one-pager. Or run the free <a href="${TRIAGE}">waste triage</a> (result first). Opt-in only.`,
          waLabel: "WhatsApp for the PDF",
          waText: "Hi AICloudStrategist, please send the one-pager PDF",
          submitLabel: "Send the PDF details",
          extra: { label: "Run the 2-min triage", href: TRIAGE },
          need: "FinOps one-pager PDF (exit capture)",
        },
      };
    }
    return null;
  };
  window.aicsFinopsContext = context;

  const track = (name, props) => {
    try {
      if (window.aicsAnalytics && typeof window.aicsAnalytics.track === "function") {
        window.aicsAnalytics.track(name, { props: props || {} });
      } else if (typeof window.plausible === "function") {
        window.plausible(name, { props: props || {} });
      }
    } catch (_) {}
  };

  const ctx = context();
  if (!ctx) return;
  const path = ctx.path;
  const loadedAt = Date.now();

  const injectStyle = () => {
    if (document.getElementById("aics-finops-leadgen-style")) return;
    const st = document.createElement("style");
    st.id = "aics-finops-leadgen-style";
    st.textContent = `
      .aics-sticky-cta{position:fixed;left:max(.85rem,env(safe-area-inset-left));bottom:max(.85rem,env(safe-area-inset-bottom));z-index:78;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;max-width:calc(100vw - 7.5rem);padding:.55rem .75rem;border-radius:.9rem;background:rgba(255,255,255,.97);border:1px solid var(--card-border,rgba(8,140,155,.22));box-shadow:0 14px 36px rgba(18,55,75,.18);font-family:var(--body,inherit)}
      .aics-sticky-cta[hidden]{display:none!important}
      .aics-sticky-label{font-size:.82rem;color:var(--muted,#3d5368);font-weight:650}
      .aics-sticky-btn{font-size:.82rem;font-weight:750;padding:.5rem .85rem;border-radius:.55rem;text-decoration:none;border:1px solid var(--cyan,#087989);line-height:1.2}
      .aics-sticky-primary{background:linear-gradient(135deg,var(--cyan-soft,#0ea3b4),var(--cyan,#087989));color:#fff}
      .aics-sticky-secondary{background:#fff;color:var(--ink,#0a1828)}
      .aics-scroll-nudge{position:fixed;left:max(.85rem,env(safe-area-inset-left));bottom:5.4rem;z-index:77;width:min(22rem,calc(100vw - 1.7rem));padding:1rem 1rem .9rem;border-radius:1rem;border:1px solid var(--card-border,rgba(8,140,155,.22));background:linear-gradient(158deg,#fff 0%,#eef9fb 60%,#fff8ef 100%);box-shadow:0 18px 44px rgba(18,55,75,.2);color:var(--ink,#0a1828);font-family:var(--body,inherit);opacity:0;transform:translateY(.9rem);transition:opacity .25s ease,transform .25s ease}
      .aics-scroll-nudge[hidden]{display:none!important}
      .aics-scroll-nudge.is-open{opacity:1;transform:none}
      .aics-scroll-nudge .eyebrow{margin:0 0 .3rem;font-size:.7rem}
      .aics-scroll-nudge h2{margin:0 1.4rem .4rem 0;font-size:1.02rem;line-height:1.3}
      .aics-scroll-nudge .aics-nudge-body{margin:0 0 .8rem;font-size:.86rem;line-height:1.5;color:var(--muted,#3d5368)}
      .aics-scroll-nudge-close{position:absolute;top:.4rem;right:.6rem;background:none;border:0;font-size:1.3rem;line-height:1;cursor:pointer;color:var(--dim,#5f758a)}
      .aics-scroll-nudge-actions{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
      .aics-scroll-nudge-actions a{font-size:.82rem;font-weight:750;padding:.5rem .85rem;border-radius:.55rem;text-decoration:none;border:1px solid var(--cyan,#087989)}
      .aics-scroll-nudge-primary{background:linear-gradient(135deg,var(--cyan-soft,#0ea3b4),var(--cyan,#087989));color:#fff}
      .aics-scroll-nudge-secondary{background:#fff;color:var(--ink,#0a1828)}
      .aics-scroll-nudge-wa{flex:1 0 100%;border:0!important;padding:.15rem 0!important;color:var(--cyan,#087989)}
      @media (max-width:720px){
        .aics-sticky-cta{right:5.4rem;max-width:none;gap:.4rem;padding:.45rem .55rem}
        .aics-sticky-label{display:none}
        .aics-scroll-nudge{left:.6rem;right:.6rem;width:auto;bottom:4.9rem}
      }
    `;
    document.head.appendChild(st);
  };

  // ---- Sticky Book + WhatsApp bar (commercial / comparison / guide pages) ----
  const initSticky = () => {
    if (ctx.kind === "pdf" || document.querySelector(".aics-sticky-cta")) return;
    const bar = document.createElement("aside");
    bar.className = "aics-sticky-cta";
    bar.hidden = true;
    bar.setAttribute("aria-label", "Book a fit review or WhatsApp");
    const extra = ctx.stickyExtra
      ? `<a class="aics-sticky-btn aics-sticky-secondary" data-sticky-extra href="${ctx.stickyExtra.href}">${ctx.stickyExtra.label}</a>`
      : "";
    bar.innerHTML = `
      <span class="aics-sticky-label">${ctx.stickyLabel}</span>
      <a class="aics-sticky-btn aics-sticky-primary" data-sticky-book href="${BOOK}">Book free fit review</a>
      <a class="aics-sticky-btn aics-sticky-secondary" data-sticky-wa href="${waHref(ctx.waText)}">WhatsApp</a>
      ${extra}
    `;
    document.body.appendChild(bar);
    bar.querySelector("[data-sticky-book]").addEventListener("click", () => track("click_book_call", { section: path, source: "sticky_bar" }));
    bar.querySelector("[data-sticky-wa]").addEventListener("click", () => track("whatsapp_click", { section: path, source: "sticky_bar" }));
    const ex = bar.querySelector("[data-sticky-extra]");
    if (ex) ex.addEventListener("click", () => track("sticky_cta_click", { section: path, target: ctx.stickyExtra.href }));
    const toggle = () => {
      const doc = document.documentElement;
      const max = Math.max(doc.scrollHeight - window.innerHeight, 1);
      const ratio = (window.scrollY || doc.scrollTop || 0) / max;
      const show = ratio >= 0.2 && max > 320;
      bar.hidden = !show;
    };
    window.addEventListener("scroll", toggle, { passive: true });
    toggle();
  };

  // ---- Scroll-triggered soft capture (non-modal) ----
  const initNudge = () => {
    if (ctx.noNudge || !ctx.nudge || document.querySelector(".aics-scroll-nudge")) return;
    const KEY_UNTIL = "aicsScrollNudgeDismissUntil";
    const KEY_SESSION = "aicsScrollNudgeShown";
    const suppressed = () => {
      try {
        if (localStorage.getItem("aicsEmailCaptureDone") === "1") return true;
        const until = Number(localStorage.getItem(KEY_UNTIL) || "0");
        if (until && Date.now() < until) return true;
        if (sessionStorage.getItem(KEY_SESSION) === "1") return true;
      } catch (_) {}
      return false;
    };
    if (suppressed()) return;
    const n = ctx.nudge;
    const el = document.createElement("aside");
    el.className = "aics-scroll-nudge";
    el.hidden = true;
    el.setAttribute("role", "complementary");
    el.setAttribute("aria-label", "Free FinOps tool");
    el.innerHTML = `
      <button type="button" class="aics-scroll-nudge-close" aria-label="Dismiss">×</button>
      <p class="eyebrow">${n.eyebrow}</p>
      <h2>${n.title}</h2>
      <p class="aics-nudge-body">${n.body}</p>
      <div class="aics-scroll-nudge-actions">
        <a class="aics-scroll-nudge-primary" data-target="primary" href="${n.primary.href}">${n.primary.label}</a>
        <a class="aics-scroll-nudge-secondary" data-target="secondary" href="${n.secondary.href}">${n.secondary.label}</a>
        <a class="aics-scroll-nudge-wa" data-target="whatsapp" href="${waHref(n.waText)}">${n.waLabel} →</a>
      </div>
    `;
    document.body.appendChild(el);
    const setUntil = (days) => { try { localStorage.setItem(KEY_UNTIL, String(Date.now() + days * 86400000)); } catch (_) {} };
    const hide = (via) => {
      el.classList.remove("is-open");
      el.hidden = true;
      setUntil(3);
      track("scroll_nudge_dismiss", { section: path, kind: ctx.kind, via });
    };
    el.querySelector(".aics-scroll-nudge-close").addEventListener("click", () => hide("close"));
    el.querySelectorAll("a[data-target]").forEach((a) => {
      a.addEventListener("click", () => {
        const target = a.getAttribute("data-target");
        track("scroll_nudge_click", { section: path, kind: ctx.kind, target });
        if (target === "whatsapp") track("whatsapp_click", { section: path, source: "scroll_nudge" });
        setUntil(7);
      });
    });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && el.classList.contains("is-open")) hide("escape");
    });
    let shown = false;
    const check = () => {
      if (shown || suppressed()) return;
      if (Date.now() - loadedAt < 8000) return;
      if (document.querySelector(".aics-email-capture.is-open") || document.querySelector(".aics-chat.is-open")) return;
      const doc = document.documentElement;
      const ratio = (window.scrollY || doc.scrollTop || 0) / Math.max(doc.scrollHeight - window.innerHeight, 1);
      if (ratio < 0.4) return;
      shown = true;
      try { sessionStorage.setItem(KEY_SESSION, "1"); } catch (_) {}
      el.hidden = false;
      requestAnimationFrame(() => el.classList.add("is-open"));
      track("scroll_nudge_open", { section: path, kind: ctx.kind, trigger: "scroll_40" });
    };
    window.addEventListener("scroll", check, { passive: true });
    window.setTimeout(check, 8200);
  };

  injectStyle();
  initSticky();
  initNudge();
})();

(() => {
  if (window.__AICS_EMAIL_CAPTURE__) return;
  window.__AICS_EMAIL_CAPTURE__ = true;

  const STORAGE_DONE = "aicsEmailCaptureDone";
  const STORAGE_DISMISS_COUNT = "aicsEmailCaptureDismissCount";
  const SCROLL_RATIO = 0.6;
  const TIME_ON_PAGE_MS = 50_000;
  const EXIT_MIN_MS = (typeof window.aicsFinopsContext === "function" && window.aicsFinopsContext()) ? 15_000 : 45_000;
  const REDISPLAY_MS = 0;
  const MAX_SESSION_DISMISSES = 1;
  const DISMISS_DAYS_KEY = "aicsEmailCaptureDismissUntil";
  const DISMISS_DAYS = 7;
  const fctx = typeof window.aicsFinopsContext === "function" ? window.aicsFinopsContext() : null;
  const fexit = fctx && fctx.exit ? fctx.exit : null;
  const looksLikeEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || "").trim());

  const readDone = () => {
    try {
      if (localStorage.getItem(STORAGE_DONE) === "1") return true;
      const until = Number(localStorage.getItem(DISMISS_DAYS_KEY) || "0");
      return Boolean(until && Date.now() < until);
    } catch (_) {
      return false;
    }
  };

  const markDone = () => {
    try {
      localStorage.setItem(STORAGE_DONE, "1");
    } catch (_) {}
  };

  const markDismissDays = () => {
    try {
      localStorage.setItem(DISMISS_DAYS_KEY, String(Date.now() + DISMISS_DAYS * 86400000));
    } catch (_) {}
  };

  const dismissCount = () => {
    try {
      return Number(sessionStorage.getItem(STORAGE_DISMISS_COUNT) || "0") || 0;
    } catch (_) {
      return 0;
    }
  };

  const bumpDismiss = () => {
    try {
      sessionStorage.setItem(STORAGE_DISMISS_COUNT, String(dismissCount() + 1));
    } catch (_) {}
  };

  if (readDone()) return;
  if (dismissCount() >= MAX_SESSION_DISMISSES) return;

  const pageLoadAt = Date.now();
  let open = false;
  let shownOnce = false;
  let redisplayTimer = null;
  let timeGateTimer = null;
  let lastTrigger = "time";

  const root = document.createElement("div");
  root.className = "aics-email-capture";
  root.hidden = true;
  root.innerHTML = `
    <div class="aics-email-capture-backdrop" data-aics-email-dismiss tabindex="-1" aria-hidden="true"></div>
    <div class="aics-email-capture-panel" role="dialog" aria-modal="true" aria-labelledby="aics-email-capture-title">
      <button type="button" class="aics-email-capture-close" data-aics-email-dismiss aria-label="Close">×</button>
      <p class="eyebrow">${fexit ? fexit.eyebrow : "Stay in the loop"}</p>
      <h2 id="aics-email-capture-title">${fexit ? fexit.title : "Get the ownership checklist + waste triage"}</h2>
      <p class="aics-email-capture-lead">${fexit ? fexit.lead : 'Fastest in India: WhatsApp first. Or leave WhatsApp / work email for the ownership checklist — try the free <a href="/cloud-waste-triage/">cloud waste triage</a> (result before any ask) or unlock the <a href="/get/finops-comparison-onepager/">FinOps comparison PDF</a>. Opt-in only.'}</p>
      <form class="aics-email-capture-form" novalidate>
        <label class="sr-only" for="aics-email-capture-name">First name (optional)</label>
        <input id="aics-email-capture-name" name="name" type="text" autocomplete="given-name" maxlength="80" placeholder="First name (optional)">
        <label class="sr-only" for="aics-email-capture-phone">WhatsApp number (preferred)</label>
        <input id="aics-email-capture-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40" placeholder="WhatsApp number (preferred)">
        <label class="sr-only" for="aics-email-capture-input">Work email</label>
        <input id="aics-email-capture-input" name="email" type="email" autocomplete="email" inputmode="email" maxlength="320" placeholder="Work email (or WhatsApp above)">
        <label class="aics-email-capture-consent">
          <input type="checkbox" name="privacy_consent" value="yes" required>
          <span>I agree to the <a href="/privacy">Privacy Policy</a> for this enquiry.</span>
        </label>
        <div class="honeypot" aria-hidden="true">
          <label>Leave this field empty<input name="company_website" type="text" tabindex="-1" autocomplete="off"></label>
        </div>
        <div class="aics-email-capture-actions">
          <a class="button button-primary" href="https://wa.me/918796302608?text=${encodeURIComponent(fexit ? fexit.waText : "Hi AICloudStrategist, I want ownership-first FinOps notes")}" data-aics-wa-primary>${fexit ? fexit.waLabel : "Chat on WhatsApp"}</a>
          <button type="submit" class="button button-secondary aics-email-capture-submit">${fexit ? fexit.submitLabel : "Send details"}</button>
          ${fexit && fexit.extra ? `<a class="button button-secondary" data-aics-exit-extra href="${fexit.extra.href}">${fexit.extra.label}</a>` : ""}
        </div>
        <p class="aics-email-capture-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  `;
  document.body.appendChild(root);

  const form = root.querySelector(".aics-email-capture-form");
  const nameInput = root.querySelector("#aics-email-capture-name");
  const input = root.querySelector("#aics-email-capture-input");
  const status = root.querySelector(".aics-email-capture-status");
  const submitBtn = root.querySelector(".aics-email-capture-submit");
  const waPrimary = root.querySelector("[data-aics-wa-primary]");
  const exitExtra = root.querySelector("[data-aics-exit-extra]");
  if (exitExtra) {
    exitExtra.addEventListener("click", () => {
      track("email_capture_tool_click", { section: sectionLabel(), trigger: lastTrigger, target: fexit.extra.href });
    });
  }
  if (waPrimary) {
    waPrimary.addEventListener("click", () => {
      track("whatsapp_click", { section: sectionLabel(), source: "email_capture_primary", trigger: lastTrigger });
      markDone();
    });
  }

  const clearRedisplay = () => {
    if (redisplayTimer) {
      clearTimeout(redisplayTimer);
      redisplayTimer = null;
    }
  };

  const track = (name, props) => {
    try {
      if (window.aicsAnalytics && typeof window.aicsAnalytics.track === "function") {
        window.aicsAnalytics.track(name, { props: props || {} });
      } else if (typeof window.plausible === "function") {
        window.plausible(name, { props: props || {} });
      }
    } catch (_) {}
  };

  const sectionLabel = () => {
    const path = (location.pathname || "/").replace(/\/+$/, "") || "/";
    return path === "/" ? "homepage" : path.slice(1, 80);
  };

  const show = (trigger) => {
    if (readDone() || open) return;
    if (dismissCount() >= MAX_SESSION_DISMISSES) return;
    // Never stack on top of the scroll nudge for time/scroll triggers; exit-intent may still fire.
    if (trigger !== "exit" && document.querySelector(".aics-scroll-nudge.is-open")) return;
    // The modal takes precedence over the soft nudge (exit-intent after the nudge was shown).
    const openNudge = document.querySelector(".aics-scroll-nudge.is-open");
    if (openNudge) { openNudge.classList.remove("is-open"); openNudge.hidden = true; }
    lastTrigger = trigger || lastTrigger;
    open = true;
    shownOnce = true;
    root.hidden = false;
    root.classList.add("is-open");
    document.body.classList.add("aics-email-capture-open");
    track("email_capture_open", { section: sectionLabel(), trigger: lastTrigger });
    window.setTimeout(() => {
      try {
        input.focus({ preventScroll: true });
      } catch (_) {
        input.focus();
      }
    }, 40);
  };

  const hide = ({ reschedule } = { reschedule: false }) => {
    if (!open) return;
    open = false;
    root.classList.remove("is-open");
    root.hidden = true;
    document.body.classList.remove("aics-email-capture-open");
    status.textContent = "";
    markDismissDays();
    clearRedisplay();
    if (reschedule && REDISPLAY_MS > 0 && !readDone() && dismissCount() < MAX_SESSION_DISMISSES) {
      redisplayTimer = window.setTimeout(() => {
        redisplayTimer = null;
        show("redisplay");
      }, REDISPLAY_MS);
    }
  };

  const scrollDepth = () => {
    const doc = document.documentElement;
    const scrollTop = window.scrollY || doc.scrollTop || 0;
    const height = Math.max(doc.scrollHeight - window.innerHeight, 1);
    return scrollTop / height;
  };

  const onScroll = () => {
    if (open || readDone()) return;
    // On FinOps pages the 40% scroll nudge is the scroll capture; modal stays for exit-intent / time.
    if (fexit && fctx && !fctx.noNudge) return;
    if (scrollDepth() >= SCROLL_RATIO) show("scroll");
  };

  const onExitIntent = (event) => {
    if (open || readDone() || shownOnce) return;
    if (Date.now() - pageLoadAt < EXIT_MIN_MS) return;
    if (event.clientY > 12) return;
    if (event.relatedTarget) return;
    show("exit");
  };

  // Prefer non-modal bar on narrow screens.
  if (window.matchMedia("(max-width: 720px)").matches) {
    root.classList.add("is-inline-prefer");
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  document.addEventListener("mouseout", onExitIntent);
  onScroll();

  // Show after 45–60s OR 60% scroll (whichever first)—never immediately.
  timeGateTimer = window.setTimeout(() => {
    timeGateTimer = null;
    if (!shownOnce) show("time");
  }, TIME_ON_PAGE_MS);

  root.querySelectorAll("[data-aics-email-dismiss]").forEach((el) => {
    el.addEventListener("click", () => {
      bumpDismiss();
      track("email_capture_dismiss", { section: sectionLabel(), trigger: lastTrigger });
      hide({ reschedule: dismissCount() < MAX_SESSION_DISMISSES });
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && open) {
      bumpDismiss();
      track("email_capture_dismiss", { section: sectionLabel(), via: "escape", trigger: lastTrigger });
      hide({ reschedule: dismissCount() < MAX_SESSION_DISMISSES });
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (readDone()) {
      hide({ reschedule: false });
      return;
    }

    const email = String(input.value || "").trim();
    const consent = form.querySelector('input[name="privacy_consent"]');
    const honeypot = form.querySelector('input[name="company_website"]');
    const phoneVal = String((form.elements.phone && form.elements.phone.value) || "").trim();
    const phoneDigits = phoneVal.replace(/\D/g, "");
    const phoneOk = phoneDigits.length >= 10 && phoneDigits.length <= 15;
    const emailOk = looksLikeEmail(email);

    if (!emailOk && !phoneOk) {
      status.textContent = "Enter WhatsApp number or work email (WhatsApp preferred).";
      (form.elements.phone || input).focus();
      return;
    }
    if (email && !emailOk) {
      status.textContent = "Enter a valid work email, or leave email blank and use WhatsApp.";
      input.focus();
      return;
    }
    if (!consent || !consent.checked) {
      status.textContent = "Privacy consent is required.";
      return;
    }

    submitBtn.disabled = true;
    status.textContent = "Sending…";
    track("email_capture_submit_attempt", { section: sectionLabel(), trigger: lastTrigger });

    const localPart = emailOk ? email.split("@")[0] || "Visitor" : phoneVal.slice(0, 24) || "Visitor";
    const givenName = String((nameInput && nameInput.value) || "").trim().slice(0, 80);
    if (window.aicsStitchIdentity) window.aicsStitchIdentity({ name: givenName, email: emailOk ? email : "", phone: phoneVal });
    const payload = {
      name: givenName || localPart.slice(0, 80),
      email: emailOk ? email : "",
      contact: emailOk ? email : phoneVal,
      phone: phoneVal,
      visitor_id: window.aicsVisitorId || '',
      privacy_consent: "yes",
      service: "Cloud & AI Cost Governance Diagnostic",
      stage: "Email capture",
      source: "email-capture",
      need: fexit ? fexit.need : "Email capture opt-in",
      message: `${fexit ? fexit.need : "Email capture opt-in"} (${lastTrigger}) on ${sectionLabel()}`,
      company_website: honeypot ? honeypot.value : "",
      landing_page: window.location.href,
      referrer: document.referrer || "",
    };

    let apiOk = false;
    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "same-origin",
      });
      const data = await response.json().catch(() => ({}));
      apiOk = response.ok && data && data.ok !== false;
      if (!apiOk && data && data.error) {
        status.textContent = String(data.error);
      }
    } catch (_) {
      apiOk = false;
    }

    // Always persist locally after a valid submit so the popup never returns.
    markDone();
    clearRedisplay();
    if (timeGateTimer) {
      clearTimeout(timeGateTimer);
      timeGateTimer = null;
    }
    track("email_capture_submit_success", {
      section: sectionLabel(),
      trigger: lastTrigger,
      status: apiOk ? "ok" : "local_only",
    });
    status.textContent = apiOk
      ? (fexit ? "Thanks — we’ll send it shortly on the contact you shared." : "Thanks — you’re on the list.")
      : "Thanks — saved on this device.";
    window.setTimeout(() => hide({ reschedule: false }), 900);
    submitBtn.disabled = false;
  });
})();

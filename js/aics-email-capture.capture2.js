(() => {
  if (window.__AICS_EMAIL_CAPTURE__) return;
  window.__AICS_EMAIL_CAPTURE__ = true;

  const STORAGE_DONE = "aicsEmailCaptureDone";
  const STORAGE_DISMISS_COUNT = "aicsEmailCaptureDismissCount";
  const SCROLL_RATIO = 0.6;
  const TIME_ON_PAGE_MS = 50_000;
  const EXIT_MIN_MS = 45_000;
  const REDISPLAY_MS = 0;
  const MAX_SESSION_DISMISSES = 1;
  const DISMISS_DAYS_KEY = "aicsEmailCaptureDismissUntil";
  const DISMISS_DAYS = 7;
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
      <p class="eyebrow">Stay in the loop</p>
      <h2 id="aics-email-capture-title">Get the ownership checklist + waste triage</h2>
      <p class="aics-email-capture-lead">Fastest in India: WhatsApp first. Or leave WhatsApp / work email for the ownership checklist — and try the free <a href="/cloud-waste-triage/">cloud waste triage</a> (result before any ask). Opt-in only.</p>
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
          <a class="button button-primary" href="https://wa.me/918796302608?text=Hi%20AICloudStrategist%2C%20I%20want%20ownership-first%20FinOps%20notes" data-aics-wa-primary>Chat on WhatsApp</a>
          <button type="submit" class="button button-secondary aics-email-capture-submit">Send details</button>
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
      need: "Email capture opt-in",
      message: `Email capture opt-in (${lastTrigger}) on ${sectionLabel()}`,
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
    status.textContent = apiOk ? "Thanks — you’re on the list." : "Thanks — saved on this device.";
    window.setTimeout(() => hide({ reschedule: false }), 900);
    submitBtn.disabled = false;
  });
})();

(() => {
  if (window.__AICS_EMAIL_CAPTURE__) return;
  window.__AICS_EMAIL_CAPTURE__ = true;

  const STORAGE_DONE = "aicsEmailCaptureDone";
  const SCROLL_PX = 280;
  const FIRST_DELAY_MS = 30_000;
  const REDISPLAY_MS = 20_000;
  const looksLikeEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || "").trim());

  const readDone = () => {
    try {
      return localStorage.getItem(STORAGE_DONE) === "1";
    } catch (_) {
      return false;
    }
  };

  const markDone = () => {
    try {
      localStorage.setItem(STORAGE_DONE, "1");
    } catch (_) {}
  };

  if (readDone()) return;

  const pageLoadAt = Date.now();
  let scrolledEnough = false;
  let open = false;
  let redisplayTimer = null;
  let firstGateTimer = null;

  const root = document.createElement("div");
  root.className = "aics-email-capture";
  root.hidden = true;
  root.innerHTML = `
    <div class="aics-email-capture-backdrop" data-aics-email-dismiss tabindex="-1" aria-hidden="true"></div>
    <div class="aics-email-capture-panel" role="dialog" aria-modal="true" aria-labelledby="aics-email-capture-title">
      <button type="button" class="aics-email-capture-close" data-aics-email-dismiss aria-label="Close">×</button>
      <p class="eyebrow">Stay in the loop</p>
      <h2 id="aics-email-capture-title">Get ownership-first FinOps notes</h2>
      <p class="aics-email-capture-lead">Leave your work email for short updates on cloud cost ownership and the fixed-fee diagnostic. No billing files needed.</p>
      <form class="aics-email-capture-form" novalidate>
        <label class="sr-only" for="aics-email-capture-input">Work email</label>
        <input id="aics-email-capture-input" name="email" type="email" autocomplete="email" inputmode="email" maxlength="320" required placeholder="nina.v@example.com">
        <label class="aics-email-capture-consent">
          <input type="checkbox" name="privacy_consent" value="yes" required>
          <span>I agree to the <a href="/privacy">Privacy Policy</a> for this enquiry.</span>
        </label>
        <div class="honeypot" aria-hidden="true">
          <label>Leave this field empty<input name="company_website" type="text" tabindex="-1" autocomplete="off"></label>
        </div>
        <button type="submit" class="button button-primary aics-email-capture-submit">Send email</button>
        <p class="aics-email-capture-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  `;
  document.body.appendChild(root);

  const panel = root.querySelector(".aics-email-capture-panel");
  const form = root.querySelector(".aics-email-capture-form");
  const input = root.querySelector("#aics-email-capture-input");
  const status = root.querySelector(".aics-email-capture-status");
  const submitBtn = root.querySelector(".aics-email-capture-submit");

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

  const show = () => {
    if (readDone() || open) return;
    open = true;
    root.hidden = false;
    root.classList.add("is-open");
    document.body.classList.add("aics-email-capture-open");
    track("email_capture_open", { section: "homepage" });
    window.setTimeout(() => {
      try {
        input.focus({ preventScroll: true });
      } catch (_) {
        input.focus();
      }
    }, 40);
  };

  const hide = ({ reschedule } = { reschedule: true }) => {
    if (!open) return;
    open = false;
    root.classList.remove("is-open");
    root.hidden = true;
    document.body.classList.remove("aics-email-capture-open");
    status.textContent = "";
    if (reschedule && !readDone()) {
      clearRedisplay();
      redisplayTimer = window.setTimeout(() => {
        redisplayTimer = null;
        show();
      }, REDISPLAY_MS);
    }
  };

  const tryFirstShow = () => {
    if (readDone() || open) return;
    if (!scrolledEnough) return;
    if (Date.now() - pageLoadAt < FIRST_DELAY_MS) return;
    show();
  };

  const onScroll = () => {
    if (scrolledEnough) return;
    if (window.scrollY >= SCROLL_PX || document.documentElement.scrollTop >= SCROLL_PX) {
      scrolledEnough = true;
      tryFirstShow();
    }
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  firstGateTimer = window.setTimeout(() => {
    firstGateTimer = null;
    tryFirstShow();
  }, FIRST_DELAY_MS);

  root.querySelectorAll("[data-aics-email-dismiss]").forEach((el) => {
    el.addEventListener("click", () => {
      track("email_capture_dismiss", { section: "homepage" });
      hide({ reschedule: true });
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && open) {
      track("email_capture_dismiss", { section: "homepage", via: "escape" });
      hide({ reschedule: true });
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

    if (!looksLikeEmail(email)) {
      status.textContent = "Enter a valid work email.";
      input.focus();
      return;
    }
    if (!consent || !consent.checked) {
      status.textContent = "Privacy consent is required.";
      return;
    }

    submitBtn.disabled = true;
    status.textContent = "Sending…";
    track("email_capture_submit_attempt", { section: "homepage" });

    const localPart = email.split("@")[0] || "Visitor";
    const payload = {
      name: localPart.slice(0, 80),
      email,
      contact: email,
      privacy_consent: "yes",
      service: "Cloud & AI Cost Governance Diagnostic",
      stage: "Homepage email capture",
      need: "Homepage email capture",
      message: "Homepage email capture popup",
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
    if (firstGateTimer) {
      clearTimeout(firstGateTimer);
      firstGateTimer = null;
    }
    track("email_capture_submit_success", { section: "homepage", api: apiOk ? "ok" : "local_only" });
    status.textContent = apiOk ? "Thanks — you’re on the list." : "Thanks — saved on this device.";
    window.setTimeout(() => hide({ reschedule: false }), 900);
    submitBtn.disabled = false;
  });
})();

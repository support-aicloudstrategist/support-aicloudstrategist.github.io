(() => {
  if (window.__AICS_FORM_SUCCESS__) return;
  window.__AICS_FORM_SUCCESS__ = true;

  const DEFAULT_TITLE = "Your message has been received";
  const DEFAULT_BODY =
    "Thank you. We have recorded your enquiry and will reply within one business day (IST). Do not send billing files or credentials by email.";

  function ensureModal() {
    let root = document.getElementById("aics-form-success-modal");
    if (root) return root;
    root = document.createElement("div");
    root.id = "aics-form-success-modal";
    root.className = "aics-form-success";
    root.hidden = true;
    root.innerHTML =
      '<div class="aics-form-success-backdrop" data-aics-form-success-close tabindex="-1" aria-hidden="true"></div>' +
      '<div class="aics-form-success-panel" role="dialog" aria-modal="true" aria-labelledby="aics-form-success-title">' +
      '<button type="button" class="aics-form-success-close" data-aics-form-success-close aria-label="Close">×</button>' +
      '<p class="eyebrow">Confirmation</p>' +
      '<h2 id="aics-form-success-title"></h2>' +
      '<p class="aics-form-success-body"></p>' +
      '<p class="aics-form-success-ref" hidden></p>' +
      '<button type="button" class="button button-primary" data-aics-form-success-close>Continue</button>' +
      "</div>";
    document.body.appendChild(root);
    root.querySelectorAll("[data-aics-form-success-close]").forEach((el) => {
      el.addEventListener("click", () => hideFormSuccess());
    });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && !root.hidden) hideFormSuccess();
    });
    return root;
  }

  function showFormSuccess(options) {
    const opts = options || {};
    const root = ensureModal();
    const title = root.querySelector("#aics-form-success-title");
    const body = root.querySelector(".aics-form-success-body");
    const ref = root.querySelector(".aics-form-success-ref");
    title.textContent = opts.title || DEFAULT_TITLE;
    body.textContent = opts.body || DEFAULT_BODY;
    if (opts.ref) {
      ref.hidden = false;
      ref.textContent = "Reference: " + opts.ref;
    } else {
      ref.hidden = true;
      ref.textContent = "";
    }
    root.hidden = false;
    document.body.classList.add("aics-form-success-open");
    const closeBtn = root.querySelector(".button[data-aics-form-success-close]");
    if (closeBtn) closeBtn.focus();
  }

  function hideFormSuccess() {
    const root = document.getElementById("aics-form-success-modal");
    if (!root) return;
    root.hidden = true;
    document.body.classList.remove("aics-form-success-open");
  }

  window.aicsShowFormReceived = showFormSuccess;
  window.aicsHideFormReceived = hideFormSuccess;

  function attribution() {
    const ft = window.aicsAttribution || {};
    const params = new URLSearchParams(window.location.search);
    return {
      landing_page: ft.landing_page || window.location.origin + window.location.pathname,
      referrer: ft.referrer || document.referrer || "",
      utm_source: ft.utm_source || params.get("utm_source") || "",
      utm_medium: ft.utm_medium || params.get("utm_medium") || "",
      utm_campaign: ft.utm_campaign || params.get("utm_campaign") || "",
      gclid: ft.gclid || params.get("gclid") || "",
      msclkid: ft.msclkid || params.get("msclkid") || "",
      li_fat_id: ft.li_fat_id || params.get("li_fat_id") || "",
    };
  }

  function track(name, props) {
    try {
      if (window.aicsAnalytics && typeof window.aicsAnalytics.track === "function") {
        window.aicsAnalytics.track(name, { props: props || {} });
      }
    } catch (_) {}
  }

  function isContactApiForm(form) {
    if (!(form instanceof HTMLFormElement)) return false;
    if (form.hasAttribute("data-aics-skip-success-bind")) return false;
    if (form.classList.contains("aics-email-capture-form")) return false;
    if (form.classList.contains("aics-chat-form")) return false;
    const action = (form.getAttribute("action") || "").toLowerCase();
    if (form.hasAttribute("data-aics-quick-form")) return true;
    if (form.id === "costFitReviewForm") return true;
    if (form.id === "contactForm") return true;
    return action.indexOf("/api/contact") !== -1;
  }

  function payloadFromForm(form) {
    const fd = new FormData(form);
    const attr = attribution();
    const contact = String(fd.get("contact") || fd.get("email") || "").trim();
    const isFit = form.id === "costFitReviewForm";
    const isQuick = form.hasAttribute("data-aics-quick-form");
    return {
      name: String(fd.get("name") || fd.get("full_name") || "").trim(),
      contact,
      email: contact,
      company: String(fd.get("company") || "").trim(),
      role: String(fd.get("role") || "").trim(),
      need: String(fd.get("need") || fd.get("vertical") || (isQuick ? "Guide question" : "Not specified")).trim(),
      message: String(fd.get("message") || fd.get("notes") || "").trim(),
      website: String(fd.get("website") || "").trim(),
      service: String(fd.get("service") || "Cloud & AI Cost Governance Diagnostic").trim() || "Cloud & AI Cost Governance Diagnostic",
      stage: String(
        fd.get("stage") || (isFit ? "Fit review requested" : isQuick ? "Guide quick enquiry" : "Contact form"),
      ).trim(),
      source: String(fd.get("source") || (isFit ? "fit-review" : isQuick ? "resource-guide" : "contact-form")).trim(),
      privacy_consent: fd.get("privacy_consent") ? "yes" : "",
      company_website: String(fd.get("company_website") || "").trim(),
      landing_page: String(fd.get("landing_page") || attr.landing_page).trim(),
      referrer: String(fd.get("referrer") || attr.referrer).trim(),
      utm_source: String(fd.get("utm_source") || attr.utm_source).trim(),
      utm_medium: String(fd.get("utm_medium") || attr.utm_medium).trim(),
      utm_campaign: String(fd.get("utm_campaign") || attr.utm_campaign).trim(),
      gclid: String(fd.get("gclid") || attr.gclid).trim(),
      msclkid: String(fd.get("msclkid") || attr.msclkid).trim(),
      li_fat_id: String(fd.get("li_fat_id") || attr.li_fat_id).trim(),
    };
  }

  async function submitContactForm(form) {
    const btn = form.querySelector('button[type="submit"]');
    const note = form.querySelector("[data-quick-status], #fitReviewSuccess, #fitReviewError, .form-notice.success, .form-notice.error");
    const success = form.ownerDocument.getElementById("fitReviewSuccess");
    const error = form.ownerDocument.getElementById("fitReviewError");
    const originalLabel = btn ? btn.textContent : "";
    const formKind = form.id === "costFitReviewForm" ? "fit_review" : form.hasAttribute("data-aics-quick-form") ? "guide_quick_enquiry" : "contact_form";

    if (!form.checkValidity()) {
      form.reportValidity();
      track("form_validation_error", { form: formKind, section: "forms" });
      return;
    }

    const payload = payloadFromForm(form);
    if (success) success.hidden = true;
    if (error) error.hidden = true;

    track("form_submit_attempt", { form: formKind, section: "forms" });
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Sending…";
    }

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || !result.ok) throw new Error(result.error || "Submission failed");

      form.reset();
      if (success) {
        success.textContent =
          "Thanks—your request is recorded" + (result.contact_id ? " (ref " + result.contact_id + ")" : "") + ". We’ll reply within one business day.";
        success.hidden = false;
      }
      if (note && note.hasAttribute("data-quick-status")) {
        note.hidden = false;
        note.textContent = "Received. We reply within 1 business day.";
      }
      showFormSuccess({
        title: "Your message has been received",
        body: "Thank you. We have recorded your enquiry and will reply within one business day (IST).",
        ref: result.contact_id || "",
      });
      track("form_submit_success", { form: formKind, section: "forms" });
      track("generate_lead", { form: formKind, section: "forms" });
    } catch (_) {
      if (error) {
        error.textContent = "The request could not be confirmed. Please retry or email contact@aicloudstrategist.com.";
        error.hidden = false;
      }
      if (note && note.hasAttribute("data-quick-status")) {
        note.hidden = false;
        note.textContent = "Could not send — please use Cal.com or email contact@aicloudstrategist.com.";
      }
      track("form_submit_error", { form: formKind, section: "forms" });
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = originalLabel || (form.id === "costFitReviewForm" ? "Request a diagnostic fit check" : "Send question");
      }
    }
  }

  function bindForms() {
    document.querySelectorAll("form").forEach((form) => {
      if (!isContactApiForm(form)) return;
      if (form.getAttribute("data-aics-success-bound") === "1") return;
      form.setAttribute("data-aics-success-bound", "1");
      // Prevent native POST to JSON API (black pretty-print page).
      form.setAttribute("action", form.getAttribute("action") || "/api/contact");
      form.addEventListener(
        "submit",
        (ev) => {
          ev.preventDefault();
          ev.stopPropagation();
          submitContactForm(form);
        },
        true,
      );
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindForms, { once: true });
  } else {
    bindForms();
  }
})();

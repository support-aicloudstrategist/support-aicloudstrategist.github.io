(() => {
  const STORAGE_KEY = "aics_currency_pref";

  function readManualPref() {
    try {
      const v = (localStorage.getItem(STORAGE_KEY) || "").toUpperCase();
      if (v === "INR" || v === "USD") return v;
    } catch (_) {
      /* ignore */
    }
    return null;
  }

  function writeManualPref(currency) {
    try {
      localStorage.setItem(STORAGE_KEY, currency);
    } catch (_) {
      /* ignore */
    }
    document.cookie = `aics_currency=${currency}; Path=/; Max-Age=31536000; SameSite=Lax`;
  }

  function readQueryCurrency() {
    try {
      const params = new URLSearchParams(window.location.search);
      const currency = (params.get("currency") || "").toUpperCase();
      if (currency === "INR" || currency === "USD") return currency;
      const geo = (params.get("geo") || "").toUpperCase().replace(/[^A-Z]/g, "").slice(0, 2);
      if (geo === "IN") return "INR";
      if (geo && geo !== "XX") return "USD";
    } catch (_) {
      /* ignore */
    }
    return null;
  }

  function readCookieGeo() {
    const match = document.cookie.match(/(?:^|;\s*)aics_currency=(INR|USD)/);
    if (!match) return null;
    return { country: match[1] === "INR" ? "IN" : "XX", currency: match[1] };
  }

  function syncAttrsFromConfig() {
    const cfg = window.__AICS_PRICING__;
    if (!cfg) return;
    document.querySelectorAll("[data-price-band]").forEach((node) => {
      const band = node.getAttribute("data-price-band");
      const row = cfg[band];
      if (!row || !row.usd) return;
      node.setAttribute("data-usd", String(row.usd.min));
      if (row.usd.max != null) node.setAttribute("data-usd-max", String(row.usd.max));
      if (row.inr) {
        node.setAttribute("data-inr", String(row.inr.min));
        if (row.inr.max != null) node.setAttribute("data-inr-max", String(row.inr.max));
      }
    });
  }

  function resolveGeo() {
    const manual = readManualPref();
    if (manual) {
      return { country: manual === "INR" ? "IN" : "XX", currency: manual, source: "manual" };
    }

    const queryCurrency = readQueryCurrency();
    if (queryCurrency) {
      return {
        country: queryCurrency === "INR" ? "IN" : "XX",
        currency: queryCurrency,
        source: "query",
      };
    }

    if (window.__AICS_GEO__ && (window.__AICS_GEO__.currency === "INR" || window.__AICS_GEO__.currency === "USD")) {
      return {
        country: window.__AICS_GEO__.country || (window.__AICS_GEO__.currency === "INR" ? "IN" : "XX"),
        currency: window.__AICS_GEO__.currency,
        source: "server",
      };
    }

    const cookieGeo = readCookieGeo();
    if (cookieGeo) return { ...cookieGeo, source: "cookie" };

    return { country: "XX", currency: "USD", source: "default" };
  }

  let geo = resolveGeo();

  function formatInr(amount) {
    return `₹${Math.round(amount).toLocaleString("en-IN")}`;
  }

  function formatUsdAmount(amount) {
    return Math.round(amount).toLocaleString("en-US");
  }

  function renderNode(node) {
    const useInr = geo.currency === "INR";
    const format = node.getAttribute("data-format") || "plain";
    const minUsd = Number(node.getAttribute("data-usd"));
    const maxUsdAttr = node.getAttribute("data-usd-max");
    const maxUsd = maxUsdAttr != null && maxUsdAttr !== "" ? Number(maxUsdAttr) : null;
    const minInrAttr = node.getAttribute("data-inr");
    const maxInrAttr = node.getAttribute("data-inr-max");
    const minInr = minInrAttr != null && minInrAttr !== "" ? Number(minInrAttr) : null;
    const maxInr = maxInrAttr != null && maxInrAttr !== "" ? Number(maxInrAttr) : null;

    let text;
    if (useInr && minInr != null && Number.isFinite(minInr)) {
      if (maxInr != null && Number.isFinite(maxInr)) {
        text = `${formatInr(minInr)}–${formatInr(maxInr)}`;
      } else {
        text = formatInr(minInr);
      }
      if (format === "from") text = `From ${text}`;
      if (node.hasAttribute("data-gst") || (window.__AICS_PRICING__ && useInr)) {
        const note = (window.__AICS_PRICING__ && window.__AICS_PRICING__[node.getAttribute("data-price-band") || ""]?.inrNote) || "";
        if (note && !text.includes("GST")) text = `${text} ${note}`;
      }
    } else if (Number.isFinite(minUsd)) {
      if (maxUsd != null && Number.isFinite(maxUsd)) {
        text = `USD ${formatUsdAmount(minUsd)}–${formatUsdAmount(maxUsd)}`;
      } else {
        text = `USD ${formatUsdAmount(minUsd)}`;
      }
      if (format === "from") text = `From ${text}`;
    } else {
      return;
    }

    const prefix = node.getAttribute("data-prefix") || "";
    const suffix = node.getAttribute("data-suffix") || "";
    node.textContent = `${prefix}${text}${suffix}`;
  }

  function applyGeoVisibility() {
    document.querySelectorAll("[data-geo-show]").forEach((node) => {
      const want = (node.getAttribute("data-geo-show") || "").toUpperCase();
      const show =
        want === "ANY" ||
        want === geo.currency ||
        (want === "IN" && geo.currency === "INR") ||
        (want === "INTL" && geo.currency === "USD");
      node.hidden = !show;
    });
  }

  function syncToggleUi() {
    document.querySelectorAll("[data-currency-toggle]").forEach((root) => {
      root.querySelectorAll("button[data-set-currency]").forEach((btn) => {
        const cur = (btn.getAttribute("data-set-currency") || "").toUpperCase();
        const on = cur === geo.currency;
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        btn.classList.toggle("is-active", on);
      });
    });
  }

  function apply() {
    syncAttrsFromConfig();
    document.querySelectorAll("[data-usd], [data-inr]").forEach(renderNode);
    applyGeoVisibility();
    document.querySelectorAll("[data-geo-currency-note]").forEach((node) => {
      node.hidden = false;
      if (geo.currency === "INR") {
        node.textContent =
          "Shown in INR for visitors in India (plus GST unless the proposal says otherwise). These are India fee bands, not a live FX conversion. Fit review is free. Final proposals confirm the fixed fee in writing.";
      } else {
        node.textContent =
          "Shown in USD (default for crawlers and international visitors). India visitors see separate INR fee bands. Fit review is free. Final proposals confirm the fixed fee in writing. Taxes apply as stated in the proposal.";
      }
    });
    document.documentElement.dataset.aicsCurrency = geo.currency;
    document.documentElement.dataset.aicsGeoSource = geo.source || "";
    syncToggleUi();
  }

  function setCurrency(currency) {
    const next = currency === "INR" ? "INR" : "USD";
    writeManualPref(next);
    geo = { country: next === "INR" ? "IN" : "XX", currency: next, source: "manual" };
    apply();
  }

  window.__AICS_SET_CURRENCY__ = setCurrency;

  document.addEventListener("click", (event) => {
    const btn = event.target.closest && event.target.closest("[data-set-currency]");
    if (!btn) return;
    event.preventDefault();
    setCurrency(btn.getAttribute("data-set-currency"));
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply, { once: true });
  } else {
    apply();
  }
})();

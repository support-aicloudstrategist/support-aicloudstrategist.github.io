(() => {
  const RATE_NOTE = null; // fees are independent bands, not FX conversions

  function readQueryCurrency() {
    try {
      const value = new URLSearchParams(window.location.search).get("currency");
      if (!value) return null;
      const normalized = value.toUpperCase();
      if (normalized === "INR" || normalized === "USD") return normalized;
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

  function writeCookie(currency) {
    document.cookie = `aics_currency=${currency}; Path=/; Max-Age=86400; SameSite=Lax`;
  }

  function resolveGeo() {
    const queryCurrency = readQueryCurrency();
    if (queryCurrency) {
      const geo = {
        country: queryCurrency === "INR" ? "IN" : "XX",
        currency: queryCurrency,
        source: "query",
      };
      writeCookie(geo.currency);
      return geo;
    }

    if (window.__AICS_GEO__ && (window.__AICS_GEO__.currency === "INR" || window.__AICS_GEO__.currency === "USD")) {
      writeCookie(window.__AICS_GEO__.currency);
      return {
        country: window.__AICS_GEO__.country || (window.__AICS_GEO__.currency === "INR" ? "IN" : "XX"),
        currency: window.__AICS_GEO__.currency,
        source: "server",
      };
    }

    const cookieGeo = readCookieGeo();
    if (cookieGeo) return { ...cookieGeo, source: "cookie" };

    // Without edge geo (local preview), default international USD—not INR.
    return { country: "XX", currency: "USD", source: "default" };
  }

  const geo = resolveGeo();

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

  function apply() {
    document.querySelectorAll("[data-usd], [data-inr]").forEach(renderNode);
    applyGeoVisibility();
    document.querySelectorAll("[data-geo-currency-note]").forEach((node) => {
      node.hidden = false;
      if (geo.currency === "INR") {
        node.textContent =
          "Shown in INR for visitors in India (CF-IPCountry=IN). Fit review is free. Final proposals confirm the fixed fee in writing.";
      } else {
        node.textContent =
          "Shown in USD for international visitors. India visitors see INR 1,00,000–1,50,000. Fit review is free. Final proposals confirm the fixed fee in writing.";
      }
      void RATE_NOTE;
    });
    document.documentElement.dataset.aicsCurrency = geo.currency;
    document.documentElement.dataset.aicsGeoSource = geo.source || "";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply, { once: true });
  } else {
    apply();
  }
})();

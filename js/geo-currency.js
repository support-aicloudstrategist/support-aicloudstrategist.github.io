(() => {
  const geo = window.__AICS_GEO__ || readCookieGeo() || { country: "XX", currency: "USD" };

  function readCookieGeo() {
    const match = document.cookie.match(/(?:^|;\s*)aics_currency=(INR|USD)/);
    if (!match) return null;
    return { country: match[1] === "INR" ? "IN" : "XX", currency: match[1] };
  }

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

  function apply() {
    document.querySelectorAll("[data-usd], [data-inr]").forEach(renderNode);
    document.querySelectorAll("[data-geo-currency-note]").forEach((node) => {
      node.hidden = false;
      if (geo.currency === "INR") {
        node.textContent =
          "Shown in INR for visitors in India. Fit review is free. Final proposals confirm the fixed fee in writing.";
      } else {
        node.textContent =
          "Shown in USD. Visitors in India see INR pricing. Fit review is free. Final proposals confirm the fixed fee in writing.";
      }
    });
    document.documentElement.dataset.aicsCurrency = geo.currency;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply, { once: true });
  } else {
    apply();
  }
})();

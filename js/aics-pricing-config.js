/**
 * Single source of truth for public fee bands.
 * Change INR / pilot values here; pages read via data-* attrs populated by aics-pricing-apply.js
 * or via window.__AICS_PRICING__.
 *
 * Crawlers and noscript see USD defaults in HTML. Geo + manual toggle switch display client-side.
 */
window.__AICS_PRICING__ = {
  currencyDefault: "USD",
  taxesNote: "Fees are exclusive of applicable taxes (including GST in India) unless the written proposal says otherwise.",
  fitReview: {
    label: "Fit review",
    usd: { min: 0, max: 0, display: "Free" },
    inr: { min: 0, max: 0, display: "Free" },
  },
  singleEstate: {
    label: "Single-estate diagnostic",
    usd: { min: 2500, max: 3000 },
    // TODO: Confirm final INR public bands with founder before marketing hard-commit.
    inr: { min: 75000, max: 100000 },
    inrNote: "plus GST",
  },
  complexEstate: {
    label: "Complex multi-cloud or GPU diagnostic",
    usd: { min: 5500, max: 12000 },
    // TODO: Confirm final INR public bands with founder before marketing hard-commit.
    inr: { min: 175000, max: 400000 },
    inrNote: "plus GST",
  },
  pilot: {
    // Pilot pricing is intentionally not published until approved in writing.
    enabled: true,
    seats: 3,
    rateLabel: "Rate confirmed in writing",
    rateUsd: null,
    rateInr: null,
    exchange: "First 3 diagnostics at a pilot rate in exchange for permission to publish an anonymised result. No pilot has been completed yet.",
  },
  foundingOfferDeprecated: false,
};

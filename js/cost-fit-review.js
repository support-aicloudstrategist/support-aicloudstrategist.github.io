(() => {
  const form = document.getElementById("costFitReviewForm");
  if (!form) return;

  // Shared aics-form-success.js owns submit + success modal.
  // This file only fills attribution hidden fields and tracks form start.
  const attribution = window.aicsAttribution || {};
  const params = new URLSearchParams(window.location.search);
  let started = false;

  ["landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign", "gclid", "msclkid", "li_fat_id"].forEach((field) => {
    if (form.elements[field]) form.elements[field].value = attribution[field] || params.get(field) || "";
  });

  const track = (name, props) => {
    if (window.aicsAnalytics) window.aicsAnalytics.track(name, { props });
  };

  form.addEventListener(
    "focusin",
    () => {
      if (started) return;
      started = true;
      track("form_start", { form: "cloud_ai_cost_fit_review", section: "fit-review" });
    },
    { once: true },
  );
})();

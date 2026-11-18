(() => {
  const form = document.getElementById('costFitReviewForm');
  if (!form) return;

  const success = document.getElementById('fitReviewSuccess');
  const error = document.getElementById('fitReviewError');
  const submit = document.getElementById('fitReviewSubmit');
  const attribution = window.aicsAttribution || {};
  const params = new URLSearchParams(window.location.search);
  let started = false;

  ['landing_page', 'referrer', 'utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'msclkid', 'li_fat_id'].forEach((field) => {
    if (form.elements[field]) form.elements[field].value = attribution[field] || params.get(field) || '';
  });

  const track = (name, props) => {
    if (window.aicsAnalytics) window.aicsAnalytics.track(name, { props });
  };

  form.addEventListener('focusin', () => {
    if (started) return;
    started = true;
    track('form_start', { form: 'cloud_ai_cost_fit_review', section: 'fit-review' });
  }, { once: true });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    success.hidden = true;
    error.hidden = true;

    if (!form.checkValidity()) {
      track('form_validation_error', { form: 'cloud_ai_cost_fit_review', section: 'fit-review' });
      form.reportValidity();
      return;
    }

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.service = 'Cloud & AI Cost Governance Diagnostic';
    payload.stage = 'Fit review requested';
    const ft = window.aicsAttribution || {};
    payload.source = 'fit-review';
    payload.landing_page = payload.landing_page || ft.landing_page || (window.location.origin + window.location.pathname);
    payload.referrer = payload.referrer || ft.referrer || '';
    payload.utm_source = payload.utm_source || ft.utm_source || '';
    payload.utm_medium = payload.utm_medium || ft.utm_medium || '';
    payload.utm_campaign = payload.utm_campaign || ft.utm_campaign || '';
    payload.gclid = payload.gclid || ft.gclid || params.get('gclid') || '';
    payload.msclkid = payload.msclkid || ft.msclkid || params.get('msclkid') || '';
    payload.li_fat_id = payload.li_fat_id || ft.li_fat_id || params.get('li_fat_id') || '';

    track('form_submit_attempt', {
      form: 'cloud_ai_cost_fit_review',
      service: payload.service,
      section: 'fit-review',
    });

    submit.disabled = true;
    submit.textContent = 'Submitting securely…';

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || !result.ok) throw new Error(result.error || 'Submission failed');

      success.textContent = `Thanks—your request is recorded${result.contact_id ? ` (ref ${result.contact_id})` : ''}. We’ll reply within one business day. Do not send credentials or billing files by email.`;
      success.hidden = false;
      form.reset();
      track('form_submit_success', { form: 'cloud_ai_cost_fit_review', service: payload.service, section: 'fit-review' });
      track('generate_lead', { form: 'cloud_ai_cost_fit_review', service: payload.service, section: 'fit-review' });
    } catch (submissionError) {
      error.textContent = 'The request could not be confirmed. Please retry or email contact@aicloudstrategist.com.';
      error.hidden = false;
      track('form_submit_error', { form: 'cloud_ai_cost_fit_review', section: 'fit-review' });
    } finally {
      submit.disabled = false;
      submit.textContent = 'Request a free fit review';
    }
  });
})();

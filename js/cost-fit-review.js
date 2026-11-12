(() => {
  const form = document.getElementById('costFitReviewForm');
  if (!form) return;

  const success = document.getElementById('fitReviewSuccess');
  const error = document.getElementById('fitReviewError');
  const submit = document.getElementById('fitReviewSubmit');
  const attribution = window.aicsAttribution || {};
  const params = new URLSearchParams(window.location.search);
  let started = false;

  ['landing_page', 'referrer', 'utm_source', 'utm_medium', 'utm_campaign'].forEach((field) => {
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

      success.textContent = `Request received. Reference: ${result.contact_id}. AICS will review the scope and reply using the work email supplied.`;
      success.hidden = false;
      form.reset();
      track('form_submit_success', {
        form: 'cloud_ai_cost_fit_review',
        service: payload.service,
        section: 'fit-review',
      });
    } catch (submissionError) {
      error.textContent = 'The request could not be confirmed. Please retry or email contact@aicloudstrategist.com.';
      error.hidden = false;
      track('form_submit_error', { form: 'cloud_ai_cost_fit_review', section: 'fit-review' });
    } finally {
      submit.disabled = false;
      submit.textContent = 'Book a free fit review';
    }
  });
})();

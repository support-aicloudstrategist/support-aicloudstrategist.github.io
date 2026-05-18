// AICloudStrategist Razorpay payment link integration
(function(){
  const CONFIG_URL = '/payment-config.json';
  const INR = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 });

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[c]));
  }

  function fallbackWhatsApp(item) {
    const text = `Namaste AICloudStrategist, I want to pay for ${item.title} (${INR.format(item.amount)}). Please share the secure Razorpay payment link.`;
    return `https://wa.me/918796302608?text=${encodeURIComponent(text)}`;
  }

  function itemCard(item, enabled) {
    const hasLink = Boolean(item.paymentLink);
    const href = hasLink ? item.paymentLink : fallbackWhatsApp(item);
    const cta = hasLink && enabled ? 'Pay securely with Razorpay' : 'Request Razorpay payment link';
    const status = hasLink && enabled ? 'Secure Razorpay checkout' : 'Payment link pending founder confirmation';
    return `
      <article class="payment-card" data-payment-id="${escapeHtml(item.id)}">
        <span class="pill">${escapeHtml(status)}</span>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.description)}</p>
        <div class="payment-price">${INR.format(item.amount)}</div>
        <a class="btn btn-primary btn-full" href="${escapeHtml(href)}" ${hasLink ? 'target="_blank" rel="noopener"' : ''} data-payment-cta="${escapeHtml(item.id)}">${cta}</a>
      </article>`;
  }

  async function loadPayments() {
    const list = document.querySelector('[data-payment-list]');
    const status = document.querySelector('[data-payment-status]');
    if (!list) return;
    try {
      const response = await fetch(CONFIG_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error('Payment config not found');
      const config = await response.json();
      list.innerHTML = (config.items || []).map(item => itemCard(item, config.enabled)).join('');
      const readyCount = (config.items || []).filter(item => item.paymentLink).length;
      if (status) {
        status.textContent = config.enabled && readyCount
          ? `${readyCount} Razorpay payment link${readyCount === 1 ? '' : 's'} active.`
          : 'Razorpay account exists. Live payment links are pending dashboard/API configuration.';
      }
    } catch (error) {
      list.innerHTML = '<p class="payment-note">Payment options could not load. Please WhatsApp AICloudStrategist for the secure Razorpay link.</p>';
      if (status) status.textContent = 'Payment configuration unavailable.';
      console.error(error);
    }
  }

  loadPayments();
})();

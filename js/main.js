// AICloudStrategist premium site interactions — dependency-free
(function(){
  const navbar = document.getElementById('navbar') || document.querySelector('.nav');
  if (navbar) {
    const setScrolled = () => navbar.classList.toggle('scrolled', window.scrollY > 24);
    setScrolled();
    window.addEventListener('scroll', setScrolled, { passive: true });
  }

  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => navLinks.classList.toggle('active'));
    navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => navLinks.classList.remove('active')));
  }

  const revealItems = document.querySelectorAll('.reveal, .offer-card, .evidence-item, .process-step, .mini-panel, .contact-card, .card');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealItems.forEach((el, index) => {
      if (!el.classList.contains('reveal')) el.classList.add('animate-in');
      if (!el.style.transitionDelay && index < 20) el.style.transitionDelay = `${Math.min(index % 4, 3) * 0.06}s`;
      observer.observe(el);
    });
  } else {
    revealItems.forEach(el => el.classList.add('visible'));
  }

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navHeight = navbar ? navbar.offsetHeight : 0;
      const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 12;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  function trackEvent(name, props = {}) {
    if (window.plausible) window.plausible(name, { props });
  }

  document.querySelectorAll('a[href^="tel:"]').forEach(link => link.addEventListener('click', () => trackEvent('Phone CTA Click', { page: location.pathname })));
  document.querySelectorAll('a[href*="wa.me"]').forEach(link => link.addEventListener('click', () => trackEvent('WhatsApp CTA Click', { page: location.pathname })));
  document.querySelectorAll('a[href^="mailto:"]').forEach(link => link.addEventListener('click', () => trackEvent('Email CTA Click', { page: location.pathname })));

  document.querySelectorAll('form.lead-form').forEach(form => {
    const params = new URLSearchParams(window.location.search);
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(key => {
      const field = form.querySelector(`[name="${key}"]`);
      if (field) field.value = params.get(key) || '';
    });
    const landing = form.querySelector('[name="landing_page"]');
    if (landing) landing.value = window.location.href;
    const ref = form.querySelector('[name="referrer"]');
    if (ref) ref.value = document.referrer || '';
  });

  const launcher = document.getElementById('chatLauncher');
  const panel = document.getElementById('aicsChatPanel');
  const closeChat = document.getElementById('chatClose');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');
  const suggestions = document.getElementById('chatSuggestions');
  const chatSession = 'web-' + Math.random().toString(36).slice(2) + Date.now().toString(36);

  function addChatMessage(role, html) {
    if (!chatMessages) return;
    const msg = document.createElement('div');
    msg.className = `chat-msg ${role}`;
    msg.innerHTML = html;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  function escapeHtml(text) {
    return String(text || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  }
  function openChat() {
    if (!panel || !launcher) return;
    panel.hidden = false;
    launcher.setAttribute('aria-expanded', 'true');
    setTimeout(() => chatInput && chatInput.focus(), 80);
    trackEvent('Chatbot Open', { page: location.pathname });
  }
  function closeChatPanel() {
    if (!panel || !launcher) return;
    panel.hidden = true;
    launcher.setAttribute('aria-expanded', 'false');
  }
  async function askAics(message) {
    addChatMessage('user', `<p>${escapeHtml(message)}</p>`);
    addChatMessage('bot typing', '<p>Checking AICS knowledge base…</p>');
    try {
      const res = await fetch('https://api.aicloudstrategist.com/rag/v1/website/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: chatSession })
      });
      if (!res.ok) throw new Error('RAG response failed');
      const data = await res.json();
      const typing = chatMessages && chatMessages.querySelector('.chat-msg.typing');
      if (typing) typing.remove();
      const answer = escapeHtml(data.answer || 'I can map this to the right AICloudStrategist module after a short business review.').replace(/\n/g, '<br>');
      addChatMessage('bot', `<p>${answer}</p><a class="chat-cta" href="/free-business-review">Book free review</a>`);
      trackEvent('Chatbot Question', { page: location.pathname });
    } catch (error) {
      const typing = chatMessages && chatMessages.querySelector('.chat-msg.typing');
      if (typing) typing.remove();
      addChatMessage('bot', '<p>I could not reach the AICS knowledge base right now. Please WhatsApp us with your industry, city and biggest leakage point — we will map the right module.</p><a class="chat-cta" href="https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20to%20map%20my%20business%20problem%20to%20the%20right%20AI%20module.">WhatsApp AICS</a>');
      console.error(error);
    }
  }
  if (launcher) launcher.addEventListener('click', openChat);
  document.querySelectorAll('[data-open-chat]').forEach(btn => btn.addEventListener('click', openChat));
  if (closeChat) closeChat.addEventListener('click', closeChatPanel);
  if (suggestions) suggestions.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => { openChat(); askAics(btn.textContent); }));
  if (launcher && panel && !sessionStorage.getItem('aicsChatSeen')) {
    window.setTimeout(() => {
      if (!sessionStorage.getItem('aicsChatSeen')) {
        openChat();
        sessionStorage.setItem('aicsChatSeen', '1');
      }
    }, 1400);
  }
  if (chatForm) chatForm.addEventListener('submit', e => {
    e.preventDefault();
    const message = chatInput ? chatInput.value.trim() : '';
    if (!message) return;
    chatInput.value = '';
    askAics(message);
  });

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      const originalText = btn ? btn.textContent : '';
      const status = this.querySelector('[data-form-status]');
      if (btn) { btn.textContent = 'Sending...'; btn.disabled = true; }
      if (status) { status.textContent = ''; status.className = 'form-status'; }
      const formData = new FormData(this);
      fetch(this.action, { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } })
        .then(response => {
          if (!response.ok) throw new Error('Form submission failed');
          trackEvent('Contact Form Submit', { page: window.location.pathname || '/', service: String(formData.get('service') || 'not_selected') });
          if (btn) { btn.textContent = 'Message Sent!'; btn.style.background = '#10B981'; }
          if (status) { status.textContent = 'Thanks. Your request was sent successfully.'; status.classList.add('success'); }
          this.reset();
        })
        .catch(error => {
          if (btn) btn.textContent = 'Try Again';
          if (status) { status.textContent = 'Sorry, the message did not send. Please email contact@aicloudstrategist.com directly.'; status.classList.add('error'); }
          console.error(error);
        })
        .finally(() => setTimeout(() => { if (btn) { btn.textContent = originalText; btn.style.background = ''; btn.disabled = false; } }, 3000));
    });
  }
})();

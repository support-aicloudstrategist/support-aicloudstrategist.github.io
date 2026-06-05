// AICloudStrategist premium site interactions — dependency-free
(function(){

  const siteLoader = document.getElementById('site-loader');
  if (siteLoader) {
    const fill = document.getElementById('site-loader-fill');
    const pct = document.getElementById('site-loader-pct');
    const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const minVisibleMs = 3000;
    const safeFallbackMs = 6500;
    const startedAt = Date.now();
    let isCompleting = false;
    let progress = 0;
    const finishLoader = () => {
      siteLoader.classList.add('is-done');
      window.setTimeout(() => siteLoader.remove(), 650);
    };
    const countTimer = reduceMotion ? null : window.setInterval(() => {
      progress += Math.max(1, (96 - progress) * 0.08) + Math.random() * 1.5;
      progress = Math.min(progress, 96);
      if (fill) fill.style.width = progress + '%';
      if (pct) pct.textContent = Math.floor(progress) + '%';
    }, 90);
    const complete = () => {
      if (isCompleting || !document.body.contains(siteLoader)) return;
      isCompleting = true;
      if (countTimer) window.clearInterval(countTimer);
      if (fill) fill.style.width = '100%';
      if (pct) pct.textContent = '100%';
      const elapsed = Date.now() - startedAt;
      window.setTimeout(finishLoader, Math.max(0, minVisibleMs - elapsed));
    };
    window.addEventListener('load', complete, { once: true });
    window.setTimeout(complete, safeFallbackMs);
  }

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


  const revealItems = document.querySelectorAll('.reveal, .section, .section-head, .subhero, .pricing-hero, .customer-industry-hero, .offer-card, .evidence-item, .process-step, .mini-panel, .contact-card, .card, .service-card, .actual-tile, .deliverable-tile, .before-after-card, .process-card, .industry-card, .deep-industry-card, .industry-flow-card, .pricing-card, .aics-price-card');
  const reveal = el => el.classList.add('visible');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { reveal(entry.target); observer.unobserve(entry.target); }
      });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    revealItems.forEach((el, index) => {
      if (!el.classList.contains('reveal')) el.classList.add('animate-in');
      if (!el.style.transitionDelay && index < 20) el.style.transitionDelay = `${Math.min(index % 4, 3) * 0.06}s`;
      observer.observe(el);
    });
    // Safety net: anything that has reached (or scrolled past) the viewport is
    // revealed even on fast scrolls / anchor jumps; a timed backstop guarantees
    // nothing can ever stay stuck invisible.
    const sweep = () => revealItems.forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.94) reveal(el);
    });
    window.addEventListener('scroll', sweep, { passive: true });
    window.addEventListener('load', () => window.setTimeout(sweep, 60));
    window.setTimeout(sweep, 1500);
  } else {
    revealItems.forEach(reveal);
  }



  const reduceMotionPref = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.body.classList.add('motion-ready');
  document.querySelectorAll('.animate-in').forEach((el, index) => {
    el.style.setProperty('--aics-delay', `${Math.min(index % 6, 5) * 55}ms`);
  });
  if (!reduceMotionPref && window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const tiltTargets = document.querySelectorAll('.growth-system-scene, .service-card, .actual-tile, .deliverable-tile, .industry-card, .deep-industry-card, .industry-flow-card, .pricing-card, .aics-price-card, .process-card, .process-step');
    tiltTargets.forEach(el => {
      el.addEventListener('pointermove', event => {
        const rect = el.getBoundingClientRect();
        const x = ((event.clientX - rect.left) / rect.width - 0.5) * 6;
        const y = ((event.clientY - rect.top) / rect.height - 0.5) * -5;
        el.style.setProperty('--tiltX', `${x.toFixed(2)}deg`);
        el.style.setProperty('--tiltY', `${y.toFixed(2)}deg`);
      }, { passive: true });
      el.addEventListener('pointerleave', () => {
        el.style.setProperty('--tiltX', '0deg');
        el.style.setProperty('--tiltY', '0deg');
      }, { passive: true });
    });
    const hero = document.querySelector('.conversion-hero');
    if (hero) hero.addEventListener('pointermove', event => {
      const rect = hero.getBoundingClientRect();
      document.body.style.setProperty('--aics-mx', `${Math.round(((event.clientX - rect.left) / rect.width) * 100)}%`);
      document.body.style.setProperty('--aics-my', `${Math.round(((event.clientY - rect.top) / rect.height) * 100)}%`);
    }, { passive: true });
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
      const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top, behavior: reduceMotion ? 'auto' : 'smooth' });
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

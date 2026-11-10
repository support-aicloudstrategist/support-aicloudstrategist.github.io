(() => {
  const header = document.querySelector('[data-site-header]');
  const toggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('#primary-navigation');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const updateHeader = () => {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 18);
  };

  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  if (toggle && navigation) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      navigation.classList.toggle('is-open', open);
    });

    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        navigation.classList.remove('is-open');
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        toggle.setAttribute('aria-expanded', 'false');
        navigation.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  const costSystem = document.querySelector('[data-cost-system]');
  if (costSystem) {
    const filters = [...costSystem.querySelectorAll('[data-cost-filter]')];
    const sources = [...costSystem.querySelectorAll('[data-cost-source]')];
    const decisions = [...costSystem.querySelectorAll('[data-cost-decision]')];

    const activateCostPath = (value) => {
      costSystem.dataset.costState = value;
      filters.forEach((filter) => filter.setAttribute('aria-pressed', String(filter.dataset.costFilter === value)));
      sources.forEach((source) => source.classList.toggle('is-active', source.dataset.costSource === value));
      decisions.forEach((decision) => decision.classList.toggle('is-active', decision.dataset.costDecision === value));
    };

    filters.forEach((filter) => {
      filter.addEventListener('click', () => activateCostPath(filter.dataset.costFilter));
    });
    activateCostPath(costSystem.dataset.costState || 'cloud');
  }

  const revealItems = [...document.querySelectorAll('[data-reveal]')];
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  revealItems.forEach((item) => observer.observe(item));
})();

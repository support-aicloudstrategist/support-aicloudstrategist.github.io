(() => {
  'use strict';

  const root = document.documentElement;
  const page = document.querySelector('body.about-dossier');
  if (!page) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const flowScenes = [...document.querySelectorAll(
    '.mandate-architecture, #principles, #capabilities, #contact'
  )];
  const delivery = document.querySelector('[data-delivery-rail]');

  const showEverything = () => {
    flowScenes.forEach((element) => {
      element.classList.add('is-visible');
    });
    if (delivery) delivery.style.setProperty('--delivery-progress', '100%');
  };

  if (reduceMotion.matches || !('IntersectionObserver' in window)) {
    showEverything();
    return;
  }

  const flowObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  flowScenes.forEach((element) => flowObserver.observe(element));

  if (delivery) {
    const deliveryObserver = new IntersectionObserver((entries, observer) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      delivery.style.setProperty('--delivery-progress', '100%');
      observer.disconnect();
    }, { threshold: 0.25 });
    deliveryObserver.observe(delivery);
  }

  const onPreferenceChange = (event) => {
    if (!event.matches) return;
    showEverything();
    root.style.scrollBehavior = 'auto';
  };

  if (typeof reduceMotion.addEventListener === 'function') {
    reduceMotion.addEventListener('change', onPreferenceChange);
  } else if (typeof reduceMotion.addListener === 'function') {
    reduceMotion.addListener(onPreferenceChange);
  }
})();

(() => {
  const header = document.querySelector('[data-site-header]');
  const toggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('#primary-navigation');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isNarrow = window.matchMedia('(max-width: 820px)').matches;
  const INTRO_KEY = 'aicsIntroPlayed';

  let introFinished = false;
  const finishIntro = (scene, headerBrand) => {
    if (introFinished) return;
    introFinished = true;
    try { sessionStorage.setItem(INTRO_KEY, '1'); } catch (_) { /* ignore */ }
    if (headerBrand) headerBrand.classList.add('is-intro-ready');
    document.body.classList.remove('has-intro', 'is-intro-docking');
    if (!scene) return;
    scene.classList.add('is-done');
    window.setTimeout(() => {
      if (scene.parentNode) scene.parentNode.removeChild(scene);
    }, 420);
  };

  const runIntroScene = () => {
    const scene = document.querySelector('[data-aics-intro]');
    const introBrand = document.querySelector('[data-intro-brand]');
    const headerBrand = document.querySelector('[data-header-brand]');
    if (!scene || !introBrand || !headerBrand) return;

    let alreadyPlayed = false;
    try { alreadyPlayed = sessionStorage.getItem(INTRO_KEY) === '1'; } catch (_) { alreadyPlayed = false; }

    // Skip cinematic intro on phones — it delays first paint and interaction.
    if (alreadyPlayed || reducedMotion || isNarrow) {
      scene.hidden = true;
      headerBrand.classList.add('is-intro-ready');
      return;
    }

    document.body.classList.add('has-intro');
    scene.hidden = false;
    headerBrand.classList.remove('is-intro-ready');

    window.requestAnimationFrame(() => {
      scene.classList.add('is-active');
      introBrand.classList.add('is-alive');
    });

    const holdMs = 2400;
    const dockMs = 1100;

    window.setTimeout(() => {
      // Freeze the unit (mark + wordmark) at its held pose before measuring.
      introBrand.classList.remove('is-alive');
      introBrand.style.animation = 'none';
      introBrand.style.transition = 'none';
      introBrand.style.opacity = '1';
      introBrand.style.transform = 'translate3d(0, 0, 0) scale(1)';
      introBrand.style.transformOrigin = 'center center';

      // Reveal header layout so the destination slot can be measured accurately.
      document.body.classList.add('is-intro-docking');
      void introBrand.offsetWidth;

      window.requestAnimationFrame(() => {
        const from = introBrand.getBoundingClientRect();
        const to = headerBrand.getBoundingClientRect();
        if (!from.width || !to.width) {
          finishIntro(scene, headerBrand);
          return;
        }

        const fromCx = from.left + from.width / 2;
        const fromCy = from.top + from.height / 2;
        const toCx = to.left + to.width / 2;
        const toCy = to.top + to.height / 2;
        // Scale the whole logo unit to the header brand width so mark + wordmark stay together.
        const scale = to.width / from.width;
        const dx = toCx - fromCx;
        const dy = toCy - fromCy;

        scene.classList.add('is-docking');
        void introBrand.offsetWidth;

        introBrand.style.transition = `transform ${dockMs}ms cubic-bezier(0.33, 0.1, 0.15, 1)`;
        introBrand.style.transform = `translate3d(${dx}px, ${dy}px, 0) scale(${scale})`;

        const end = (event) => {
          if (event && event.propertyName && event.propertyName !== 'transform') return;
          introBrand.removeEventListener('transitionend', end);
          finishIntro(scene, headerBrand);
        };
        introBrand.addEventListener('transitionend', end);
        window.setTimeout(() => finishIntro(scene, headerBrand), dockMs + 180);
      });
    }, holdMs);
  };

  runIntroScene();

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
      if (!open) {
        navigation.querySelectorAll('.nav-item.is-open').forEach((item) => {
          item.classList.remove('is-open');
          const trigger = item.querySelector('[data-nav-menu]');
          if (trigger) trigger.setAttribute('aria-expanded', 'false');
        });
      }
    });

    const prefersHoverNav = () =>
      window.matchMedia('(hover: hover) and (pointer: fine)').matches &&
      window.matchMedia('(min-width: 821px)').matches;

    const closeNavMenus = () => {
      navigation.querySelectorAll('.nav-item.is-open').forEach((item) => {
        item.classList.remove('is-open');
        const trigger = item.querySelector('[data-nav-menu]');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      });
    };

    navigation.querySelectorAll('.nav-item').forEach((item) => {
      const trigger = item.querySelector('[data-nav-menu]');
      if (!trigger) return;
      item.addEventListener('mouseenter', () => {
        if (!prefersHoverNav()) return;
        trigger.setAttribute('aria-expanded', 'true');
      });
      item.addEventListener('mouseleave', () => {
        if (!prefersHoverNav()) return;
        trigger.setAttribute('aria-expanded', 'false');
      });
    });

    navigation.addEventListener('click', (event) => {
      const menuTrigger = event.target.closest('[data-nav-menu]');
      if (menuTrigger) {
        // Desktop hover devices open via CSS; only tap-toggle on touch / mobile drawer.
        if (prefersHoverNav()) return;
        event.preventDefault();
        const item = menuTrigger.closest('.nav-item');
        const open = !item.classList.contains('is-open');
        navigation.querySelectorAll('.nav-item.is-open').forEach((other) => {
          if (other !== item) {
            other.classList.remove('is-open');
            const otherTrigger = other.querySelector('[data-nav-menu]');
            if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
          }
        });
        item.classList.toggle('is-open', open);
        menuTrigger.setAttribute('aria-expanded', String(open));
        return;
      }

      if (event.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        navigation.classList.remove('is-open');
        closeNavMenus();
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        toggle.setAttribute('aria-expanded', 'false');
        navigation.classList.remove('is-open');
        closeNavMenus();
        toggle.focus();
      }
    });

    document.addEventListener('click', (event) => {
      if (event.target.closest('.nav-item') || event.target.closest('.nav-toggle')) return;
      closeNavMenus();
    });
  }

  const bindVizLoop = (root, opts) => {
    const filterAttr = opts.filterAttr;
    const nodeAttr = opts.nodeAttr;
    const stateAttr = opts.stateAttr;
    const filters = [...root.querySelectorAll(`[${filterAttr}]`)];
    const nodes = [...root.querySelectorAll(`[${nodeAttr}]`)];
    if (!filters.length && !nodes.length) return;
    const states = filters.length
      ? filters.map((filter) => filter.getAttribute(filterAttr)).filter(Boolean)
      : [...new Set(nodes.map((node) => node.getAttribute(nodeAttr)).filter(Boolean))];
    if (!states.length) return;
    let activeIndex = Math.max(0, states.indexOf(root.getAttribute(stateAttr) || states[0]));
    let timerId = null;

    const activate = (value) => {
      const nextIndex = states.indexOf(value);
      if (nextIndex >= 0) activeIndex = nextIndex;
      root.setAttribute(stateAttr, value);
      filters.forEach((filter) => {
        filter.setAttribute('aria-pressed', String(filter.getAttribute(filterAttr) === value));
      });
      nodes.forEach((node) => {
        node.classList.toggle('is-active', node.getAttribute(nodeAttr) === value);
      });
    };

    const startLoop = () => {
      if (reducedMotion || isNarrow || states.length < 2) return;
      window.clearInterval(timerId);
      timerId = window.setInterval(() => {
        activeIndex = (activeIndex + 1) % states.length;
        activate(states[activeIndex]);
      }, opts.intervalMs || 2600);
    };

    if (!isNarrow) {
      filters.forEach((filter) => {
        filter.addEventListener('click', () => {
          activate(filter.getAttribute(filterAttr));
          startLoop();
        });
      });
    }

    activate(states[activeIndex] || states[0]);
    startLoop();
  };

  // Desktop-only: home ownership model is replaced on phones by .hero-mobile-strip.
  const costSystem = document.querySelector('[data-cost-system]');
  if (costSystem && !isNarrow) {
    bindVizLoop(costSystem, {
      filterAttr: 'data-cost-filter',
      nodeAttr: 'data-cost-source',
      stateAttr: 'data-cost-state',
      intervalMs: 2600
    });
    // Also toggle decision nodes for the home ownership model.
    const decisions = [...costSystem.querySelectorAll('[data-cost-decision]')];
    const syncDecisions = () => {
      const value = costSystem.getAttribute('data-cost-state');
      decisions.forEach((decision) => {
        decision.classList.toggle('is-active', decision.dataset.costDecision === value);
      });
    };
    syncDecisions();
    const observer = new MutationObserver(syncDecisions);
    observer.observe(costSystem, { attributes: true, attributeFilter: ['data-cost-state'] });
  }

  if (!isNarrow) {
    document.querySelectorAll('[data-page-viz]').forEach((viz) => {
      bindVizLoop(viz, {
        filterAttr: 'data-viz-filter',
        nodeAttr: 'data-viz-node',
        stateAttr: 'data-viz-state',
        intervalMs: 2400
      });
    });
  } else {
    document.querySelectorAll('[data-page-viz]').forEach((viz) => {
      viz.querySelectorAll('[aria-pressed]').forEach((btn) => {
        btn.setAttribute('tabindex', '-1');
        btn.setAttribute('aria-disabled', 'true');
      });
    });
  }

  const revealItems = [...document.querySelectorAll('[data-reveal]')];
  if (reducedMotion || isNarrow || !('IntersectionObserver' in window)) {
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

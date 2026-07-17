(() => {
  "use strict";

  const enterpriseServices = [
    {
      label: "Production AI Assurance",
      href: "/services/ai-mlops/",
      description: "Validate AI quality, controls and production readiness."
    },
    {
      label: "Enterprise AI Systems & Agents",
      href: "/services/ai-automation/",
      description: "Build governed agents and measurable AI workflows."
    },
    {
      label: "AI FinOps & Cloud Economics",
      href: "/services/cloud-finops/",
      description: "Connect AI and cloud spend to business outcomes."
    },
    {
      label: "AI Security, Compliance & Sovereign Platforms",
      href: "/services/cloud-security/",
      description: "Strengthen data, platform and jurisdictional controls."
    },
    {
      label: "Managed AI Platforms & Operations",
      href: "/services/devops-observability/",
      description: "Operate production platforms with reliability and visibility."
    }
  ];

  const growthServices = [
    {
      label: "Digital Presence & Search Growth",
      href: "/services/website-digital-presence/",
      description: "Create a credible, discoverable digital foundation."
    },
    {
      label: "Lead Operations & Revenue Automation",
      href: "/lead-capture-follow-up/",
      description: "Capture, route and follow up every serious enquiry."
    },
    {
      label: "Digital Trust & Compliance",
      href: "/trust-compliance/",
      description: "Improve privacy, consent and customer-facing trust."
    },
    {
      label: "Growth & Control Operating System",
      href: "/growth-control-os/",
      description: "Unify growth, automation, trust and owner reporting."
    }
  ];

  const studioServices = [
    {
      label: "AI Creative Studio",
      href: "/ai-creative-studio/",
      description: "Governed creative production, localisation and campaign assets."
    }
  ];

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

  const serviceLinks = (services) => services.map((service) => `
    <a class="aics-mega-link" href="${escapeHtml(service.href)}">
      <span class="aics-mega-link-title">${escapeHtml(service.label)}</span>
      <span class="aics-mega-link-copy">${escapeHtml(service.description)}</span>
      <span class="aics-mega-link-arrow" aria-hidden="true">↗</span>
    </a>`).join("");

  const navigationMarkup = (index) => {
    const panelId = `aics-mega-panel-${index}`;
    const mobileId = `aics-primary-links-${index}`;
    return `
      <nav class="aics-site-nav" aria-label="Primary navigation">
        <div class="aics-site-nav-inner">
          <a class="aics-site-brand" href="/" aria-label="AICloudStrategist home">
            <span class="aics-site-brand-mark" aria-hidden="true">AI</span>
            <span>AICloudStrategist</span>
          </a>
          <button class="aics-mobile-trigger" type="button" aria-expanded="false" aria-controls="${mobileId}" aria-label="Open navigation">
            <span></span><span></span><span></span>
          </button>
          <div class="aics-primary-links" id="${mobileId}">
            <div class="aics-mega-trigger-wrap">
              <button class="aics-mega-trigger" type="button" aria-expanded="false" aria-controls="${panelId}">
                What We Do
                <svg aria-hidden="true" viewBox="0 0 12 8"><path d="m1 1 5 5 5-5"/></svg>
              </button>
              <div class="aics-mega-panel" id="${panelId}" hidden>
                <div class="aics-mega-grid">
                  <section class="aics-mega-group aics-mega-group-enterprise" aria-labelledby="aics-enterprise-heading-${index}">
                    <p class="aics-mega-kicker">Primary capability</p>
                    <h2 id="aics-enterprise-heading-${index}">Enterprise AI Services</h2>
                    <p class="aics-mega-intro">For enterprises moving AI from pilots into controlled production.</p>
                    <div class="aics-mega-enterprise-links">${serviceLinks(enterpriseServices)}</div>
                  </section>
                  <section class="aics-mega-group" aria-labelledby="aics-growth-heading-${index}">
                    <p class="aics-mega-kicker">Growth systems</p>
                    <h2 id="aics-growth-heading-${index}">Business Growth Systems</h2>
                    <p class="aics-mega-intro">For organisations building a trusted, measurable digital growth engine.</p>
                    <div>${serviceLinks(growthServices)}</div>
                  </section>
                  <section class="aics-mega-group aics-mega-studio" aria-labelledby="aics-studio-heading-${index}">
                    <p class="aics-mega-kicker">Specialist business unit</p>
                    <h2 id="aics-studio-heading-${index}">Specialist Studio</h2>
                    <div>${serviceLinks(studioServices)}</div>
                    <p class="aics-studio-note">AI Creative Studio by AICloudStrategist</p>
                  </section>
                </div>
                <div class="aics-mega-footer">
                  <a href="/services/">View the complete service portfolio <span aria-hidden="true">→</span></a>
                  <a class="aics-mega-footer-cta" href="/contact.html">Discuss your challenge <span aria-hidden="true">→</span></a>
                </div>
              </div>
            </div>
            <a class="aics-primary-link" href="/case-studies/">Proof</a>
            <a class="aics-primary-link" href="/resources/">Resources</a>
            <a class="aics-primary-link" href="/about/">About</a>
            <a class="aics-primary-cta" href="/contact.html">Discuss a challenge</a>
          </div>
        </div>
      </nav>`;
  };

  const desktopQuery = window.matchMedia("(min-width: 901px)");

  document.querySelectorAll("[data-aics-site-nav]").forEach((mount, index) => {
    mount.classList.add("aics-site-nav-shell");
    mount.innerHTML = navigationMarkup(index);

    const nav = mount.querySelector(".aics-site-nav");
    const triggerWrap = mount.querySelector(".aics-mega-trigger-wrap");
    const trigger = mount.querySelector(".aics-mega-trigger");
    const panel = mount.querySelector(".aics-mega-panel");
    const mobileTrigger = mount.querySelector(".aics-mobile-trigger");
    const primaryLinks = mount.querySelector(".aics-primary-links");
    let closeTimer = 0;

    const openMega = () => {
      window.clearTimeout(closeTimer);
      panel.hidden = false;
      trigger.setAttribute("aria-expanded", "true");
      triggerWrap.classList.add("is-open");
      if (!desktopQuery.matches) {
        window.requestAnimationFrame(() => primaryLinks.scrollTo({ top: 0, behavior: "auto" }));
      }
    };

    const closeMega = ({ returnFocus = false } = {}) => {
      window.clearTimeout(closeTimer);
      panel.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
      triggerWrap.classList.remove("is-open");
      if (returnFocus) trigger.focus();
    };

    const closeMobile = () => {
      primaryLinks.classList.remove("is-mobile-open");
      mobileTrigger.setAttribute("aria-expanded", "false");
      mobileTrigger.setAttribute("aria-label", "Open navigation");
      document.documentElement.classList.remove("aics-nav-open");
      if (!desktopQuery.matches) closeMega();
    };

    trigger.addEventListener("click", () => {
      if (desktopQuery.matches) {
        openMega();
      } else if (trigger.getAttribute("aria-expanded") === "true") {
        closeMega();
      } else {
        openMega();
      }
    });

    triggerWrap.addEventListener("pointerenter", () => {
      if (desktopQuery.matches) openMega();
    });
    triggerWrap.addEventListener("pointerleave", () => {
      if (desktopQuery.matches) closeTimer = window.setTimeout(() => closeMega(), 160);
    });
    triggerWrap.addEventListener("focusin", (event) => {
      if (panel.contains(event.target)) openMega();
    });
    triggerWrap.addEventListener("focusout", (event) => {
      if (desktopQuery.matches && !triggerWrap.contains(event.relatedTarget)) closeMega();
    });

    mobileTrigger.addEventListener("click", () => {
      const willOpen = !primaryLinks.classList.contains("is-mobile-open");
      primaryLinks.classList.toggle("is-mobile-open", willOpen);
      mobileTrigger.setAttribute("aria-expanded", String(willOpen));
      mobileTrigger.setAttribute("aria-label", willOpen ? "Close navigation" : "Open navigation");
      document.documentElement.classList.toggle("aics-nav-open", willOpen);
    });

    nav.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMega({ returnFocus: trigger.getAttribute("aria-expanded") === "true" });
        closeMobile();
      }
    });

    document.addEventListener("click", (event) => {
      if (!nav.contains(event.target)) {
        closeMega();
        closeMobile();
      }
    });

    primaryLinks.addEventListener("click", (event) => {
      if (event.target.closest("a") && !desktopQuery.matches) closeMobile();
    });

    desktopQuery.addEventListener("change", () => {
      closeMega();
      closeMobile();
    });
  });
})();

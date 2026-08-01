(() => {
  "use strict";

  const ROOT_ATTRIBUTE = "data-aics-global-nav";
  const FOOTER_ATTRIBUTE = "data-aics-global-footer";
  const MOBILE_BREAKPOINT = "(max-width: 1020px)";

  const PRIMARY_LINKS = Object.freeze([
    { label: "Home", href: "/" },
    { label: "Proof", href: "/case-studies/" },
    { label: "Resources", href: "/resources/" },
    { label: "About", href: "/about/" },
  ]);

  const MEGA_GROUPS = Object.freeze([
    {
      heading: "Enterprise AI",
      kind: "enterprise",
      items: Object.freeze([
        { label: "Production AI Assurance", href: "/services/ai-mlops/" },
        { label: "Enterprise AI Systems & Agents", href: "/services/ai-automation/" },
        { label: "AI FinOps & Cloud Economics", href: "/services/cloud-finops/" },
        { label: "AI Security, Compliance & Sovereign Platforms", href: "/services/cloud-security/" },
        { label: "Managed AI Platforms & Operations", href: "/services/devops-observability/" },
      ]),
    },
    {
      heading: "Business Growth Systems",
      kind: "growth",
      items: Object.freeze([
        {
          label: "AI Digital Presence",
          href: "/services/website-digital-presence/",
          icon: "presence",
          description: "Digital experiences and customer journeys built to attract, qualify and convert demand.",
        },
        {
          label: "AI Lead Intelligence",
          href: "/lead-capture-follow-up/",
          icon: "intelligence",
          description: "Capture, qualification, routing and follow-up across the commercial pipeline.",
        },
        {
          label: "AI Trust Layer",
          href: "/trust-compliance/",
          icon: "trust",
          description: "Privacy, governance and trust controls for connected customer journeys.",
        },
        {
          label: "AI Growth Operations",
          href: "/growth-control-os/",
          icon: "operations",
          description: "Connected workflows and operational intelligence across growth systems.",
        },
      ]),
    },
    {
      heading: "AI Creative Studio",
      kind: "creative",
      href: "/ai-creative-studio/",
      capabilities: Object.freeze([
        "Advertisements",
        "Commercials",
        "Product visuals",
        "Campaign assets",
        "Promotional videos",
        "Social media creatives",
      ]),
    },
  ]);

  const ICONS = Object.freeze({
    presence: '<svg viewBox="0 0 24 24" focusable="false"><rect x="3.5" y="4.5" width="17" height="15" rx="2.5"></rect><path d="M3.5 8.5h17M8 4.5v4M16.5 13.5l1 1 2-2M7 13h5M7 16h7"></path></svg>',
    intelligence: '<svg viewBox="0 0 24 24" focusable="false"><path d="M4 5h16l-6.5 7.2V18l-3 1.5v-7.3z"></path><circle cx="17.5" cy="6.5" r="2.5"></circle><path d="M17.5 3v1M17.5 9v1M14 6.5h1M20 6.5h1"></path></svg>',
    trust: '<svg viewBox="0 0 24 24" focusable="false"><path d="M12 3l7 3.5v5.2c0 4.3-2.9 7.5-7 9.3-4.1-1.8-7-5-7-9.3V6.5z"></path><path d="M8.8 12.1l2 2 4.6-4.6"></path></svg>',
    operations: '<svg viewBox="0 0 24 24" focusable="false"><path d="M5.1 8.2A8 8 0 0 1 19 7l1.3 2.4M18.9 15.8A8 8 0 0 1 5 17l-1.3-2.4"></path><path d="M20.3 5.2v4.2h-4.2M3.7 18.8v-4.2h4.2"></path><circle cx="12" cy="12" r="2.5"></circle></svg>',
    mail: '<svg viewBox="0 0 24 24" focusable="false"><path d="M4 6.5h16v11H4z"></path><path d="m5 8 7 5 7-5"></path></svg>',
    phone: '<svg viewBox="0 0 24 24" focusable="false"><path d="M7.2 4.5 9.8 8 8.2 9.8c1.2 2.5 3.3 4.5 5.8 5.7l1.7-1.6 3.8 2.5-.8 3c-.2.7-.8 1.1-1.5 1.1C9.7 20 4 14.3 3.5 6.8c0-.7.4-1.3 1.1-1.5z"></path></svg>',
  });

  const CTA = Object.freeze({ label: "Discuss your AI initiative", href: "/contact.html?service=enterprise-ai" });

  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character]);

  const normalisePath = (value) => {
    let path = String(value || "/");
    try {
      path = new URL(path, window.location.origin).pathname;
    } catch {
      path = path.split(/[?#]/)[0];
    }
    path = path.replace(/index\.html$/i, "");
    if (path === "/") return path;
    return path.endsWith("/") ? path : `${path}/`;
  };

  const isCurrent = (href) => normalisePath(window.location.pathname) === normalisePath(href);

  const linkMarkup = ({ label, href }, className = "aics-nav-link") => (
    `<a class="${className}" href="${escapeHtml(href)}"${isCurrent(href) ? ' aria-current="page"' : ""}>${escapeHtml(label)}</a>`
  );

  const enterpriseMarkup = (group) => group.items.map((item, index) => `
    <a class="aics-mega-link aics-mega-link--enterprise" href="${escapeHtml(item.href)}"${isCurrent(item.href) ? ' aria-current="page"' : ""}>
      <span class="aics-mega-index" aria-hidden="true">0${index + 1}</span>
      <span class="aics-mega-link-label">${escapeHtml(item.label)}</span>
      <span class="aics-mega-arrow" aria-hidden="true">↗</span>
    </a>
  `).join("");

  const growthMarkup = (group) => group.items.map((item) => `
    <a class="aics-mega-link aics-mega-link--detailed" href="${escapeHtml(item.href)}"${isCurrent(item.href) ? ' aria-current="page"' : ""}>
      <span class="aics-mega-link-icon" aria-hidden="true">${ICONS[item.icon]}</span>
      <span class="aics-mega-link-copy">
        <span class="aics-mega-link-label">${escapeHtml(item.label)}</span>
        <span class="aics-mega-link-description">${escapeHtml(item.description)}</span>
      </span>
    </a>
  `).join("");

  const creativeMarkup = (group) => `
    <div class="aics-creative-card">
      <div class="aics-creative-visual" aria-hidden="true">
        <span class="aics-creative-frame aics-creative-frame--one"></span>
        <span class="aics-creative-frame aics-creative-frame--two"></span>
        <span class="aics-creative-play">▶</span>
      </div>
      <div class="aics-creative-capabilities" aria-label="AI Creative Studio capabilities">
        ${group.capabilities.map((capability) => `<span class="aics-creative-capability"><span aria-hidden="true"></span>${escapeHtml(capability)}</span>`).join("")}
      </div>
      <a class="aics-creative-cta" href="${escapeHtml(group.href)}"${isCurrent(group.href) ? ' aria-current="page"' : ""}>
        Explore AI Creative Studio <span aria-hidden="true">→</span>
      </a>
    </div>
  `;

  const megaMarkup = () => MEGA_GROUPS.map((group) => {
    const id = `aics-mega-${group.heading.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
    const body = group.kind === "enterprise"
      ? enterpriseMarkup(group)
      : group.kind === "growth"
        ? growthMarkup(group)
        : creativeMarkup(group);
    const count = group.items ? group.items.length : group.capabilities.length;
    return `
      <section class="aics-mega-group aics-mega-group--${group.kind}" aria-labelledby="${id}">
        <div class="aics-mega-heading-row">
          <h2 class="aics-mega-heading" id="${id}">${escapeHtml(group.heading)}</h2>
          <span class="aics-mega-count" aria-label="${count} capabilities">${String(count).padStart(2, "0")}</span>
        </div>
        <div class="aics-mega-items">${body}</div>
      </section>
    `;
  }).join("");

  const createNavigation = () => {
    const root = document.createElement("div");
    root.className = "aics-global-nav";
    root.setAttribute(ROOT_ATTRIBUTE, "");
    root.innerHTML = `
      <aside class="aics-utility-bar" data-aics-utility-bar aria-label="Contact and delivery information">
        <div class="aics-utility-inner">
          <span class="aics-utility-trust"><span class="aics-utility-status" aria-hidden="true"></span><span class="aics-utility-trust-copy">Enterprise AI systems, controls and managed operations</span><span class="aics-utility-mobile-copy">Enterprise AI · Global delivery</span></span>
          <span class="aics-utility-contacts">
            <a href="mailto:contact@aicloudstrategist.com" aria-label="Email AICloudStrategist at contact@aicloudstrategist.com">${ICONS.mail}<span class="aics-utility-email">contact@aicloudstrategist.com</span><span class="aics-utility-email-short">Email</span></a>
            <span class="aics-utility-divider" aria-hidden="true"></span>
            <a href="tel:+918065480898" aria-label="Call AICloudStrategist on +91 80654 80898">${ICONS.phone}<span>+91 80654 80898</span></a>
          </span>
        </div>
      </aside>
      <nav class="aics-nav-shell" aria-label="Primary navigation">
        <div class="aics-nav-bar">
          <a class="aics-nav-brand" href="/" aria-label="AICloudStrategist home">
            <span class="aics-nav-mark" aria-hidden="true">AI</span>
            <span class="aics-nav-name">AICloudStrategist</span>
          </a>
          <button class="aics-nav-mobile-toggle" type="button" aria-expanded="false" aria-controls="aics-primary-links" aria-label="Open navigation">
            <span></span><span></span><span></span>
          </button>
          <div class="aics-primary-links" id="aics-primary-links">
            ${linkMarkup(PRIMARY_LINKS[0])}
            <div class="aics-mega-trigger-wrap">
              <button class="aics-mega-trigger" type="button" aria-expanded="false" aria-controls="aics-mega-panel">
                <span>What We Do</span><span class="aics-nav-chevron" aria-hidden="true"></span>
              </button>
              <div class="aics-mega-panel" id="aics-mega-panel" hidden>
                <div class="aics-mega-grid">${megaMarkup()}</div>
                <div class="aics-mega-assurance"><span>One connected delivery model</span><span aria-hidden="true">Assess</span><i></i><span aria-hidden="true">Build</span><i></i><span aria-hidden="true">Control</span><i></i><span aria-hidden="true">Operate</span></div>
              </div>
            </div>
            ${PRIMARY_LINKS.slice(1).map((link) => linkMarkup(link)).join("")}
            ${linkMarkup(CTA, "aics-nav-cta")}
          </div>
        </div>
      </nav>
    `;
    return root;
  };

  const footerLinkGroup = (heading, links, extraClass = "") => `
    <section class="aics-footer-group ${extraClass}">
      <h2>${escapeHtml(heading)}</h2>
      ${links.map((link) => `<a href="${escapeHtml(link.href)}">${escapeHtml(link.label)}</a>`).join("")}
    </section>
  `;

  const createFooter = () => {
    const footer = document.createElement("footer");
    footer.className = "aics-global-footer";
    footer.setAttribute(FOOTER_ATTRIBUTE, "");
    footer.innerHTML = `
      <div class="aics-footer-inner">
        <div class="aics-footer-grid">
          <section class="aics-footer-brand-block">
            <a class="aics-footer-brand" href="/" aria-label="AICloudStrategist home"><span class="aics-footer-mark" aria-hidden="true">AI</span><span>AICloudStrategist</span></a>
            <p>Enterprise AI systems, controls, economics and managed operations for business-critical initiatives.</p>
            <a class="aics-footer-primary-link" href="${CTA.href}">${CTA.label}<span aria-hidden="true">→</span></a>
          </section>
          ${footerLinkGroup("Enterprise AI", [
            { label: "Production AI Assurance", href: "/services/ai-mlops/" },
            { label: "AI Systems & Agents", href: "/services/ai-automation/" },
            { label: "AI FinOps & Economics", href: "/services/cloud-finops/" },
            { label: "AI Security & Sovereignty", href: "/services/cloud-security/" },
            { label: "Managed AI Operations", href: "/services/devops-observability/" },
          ])}
          ${footerLinkGroup("Company", [
            { label: "Why AICloudStrategist", href: "/#why-aics" },
            { label: "Evidence", href: "/case-studies/" },
            { label: "How we engage", href: "/#engagement" },
            { label: "About", href: "/about/" },
            { label: "Contact", href: CTA.href },
          ])}
          ${footerLinkGroup("Specialist Practices", [
            { label: "Business Growth Systems", href: "/contact.html?service=business-growth-systems" },
            { label: "AI Creative Studio", href: "/ai-creative-studio/" },
            { label: "Enterprise AI resources", href: "/resources/" },
            { label: "Proof policy", href: "/case-studies/" },
          ], "aics-footer-practices")}
          <section class="aics-footer-contact">
            <h2>Contact</h2>
            <a href="mailto:contact@aicloudstrategist.com">contact@aicloudstrategist.com</a>
            <a href="tel:+918065480898">+91 80654 80898</a>
            <p>Serving enterprises, mid-market companies and scale-ups worldwide.</p>
          </section>
        </div>
        <div class="aics-footer-bottom">
          <span>© AICloudStrategist</span>
          <span class="aics-footer-legal"><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></span>
          <span>Enterprise-grade, not enterprise-exclusive.</span>
        </div>
      </div>
    `;
    return footer;
  };

  const initialiseInteractions = (root) => {
    const mobileQuery = window.matchMedia(MOBILE_BREAKPOINT);
    const mobileToggle = root.querySelector(".aics-nav-mobile-toggle");
    const primaryLinks = root.querySelector(".aics-primary-links");
    const triggerWrap = root.querySelector(".aics-mega-trigger-wrap");
    const trigger = root.querySelector(".aics-mega-trigger");
    const panel = root.querySelector(".aics-mega-panel");
    const supportsPopover = typeof primaryLinks.showPopover === "function";
    let closeTimer = 0;

    const setMegaOpen = (open, returnFocus = false) => {
      window.clearTimeout(closeTimer);
      panel.hidden = !open;
      panel.setAttribute("aria-hidden", String(!open));
      triggerWrap.classList.toggle("is-open", open);
      trigger.setAttribute("aria-expanded", String(open));
      if (open && mobileQuery.matches) {
        window.requestAnimationFrame(() => {
          primaryLinks.scrollTop = 0;
          panel.scrollTop = 0;
        });
      }
      if (!open && returnFocus) trigger.focus();
    };

    const setMobileOpen = (open) => {
      primaryLinks.classList.toggle("is-open", open);
      mobileToggle.setAttribute("aria-expanded", String(open));
      mobileToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");

      if (open && mobileQuery.matches && supportsPopover) {
        const navBottom = root.querySelector(".aics-nav-shell").getBoundingClientRect().bottom;
        primaryLinks.style.setProperty("--aics-mobile-nav-top", `${Math.max(0, Math.round(navBottom))}px`);
        primaryLinks.setAttribute("popover", "manual");
        try {
          if (!primaryLinks.matches(":popover-open")) primaryLinks.showPopover();
        } catch {
          primaryLinks.removeAttribute("popover");
        }
      }

      if (!open) {
        setMegaOpen(false, false);
        if (supportsPopover) {
          try {
            if (primaryLinks.matches(":popover-open")) primaryLinks.hidePopover();
          } catch {
            primaryLinks.removeAttribute("popover");
          }
        }
        primaryLinks.removeAttribute("popover");
        primaryLinks.style.removeProperty("--aics-mobile-nav-top");
      }
    };

    const scheduleClose = () => {
      window.clearTimeout(closeTimer);
      closeTimer = window.setTimeout(() => setMegaOpen(false, false), 220);
    };

    const cancelClose = () => window.clearTimeout(closeTimer);

    mobileToggle.addEventListener("click", () => {
      setMobileOpen(mobileToggle.getAttribute("aria-expanded") !== "true");
    });

    trigger.addEventListener("click", () => {
      if (mobileQuery.matches) setMegaOpen(trigger.getAttribute("aria-expanded") !== "true", false);
      else setMegaOpen(true, false);
    });

    trigger.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
      event.preventDefault();
      setMegaOpen(true, false);
      const links = panel.querySelectorAll("a");
      const target = event.key === "ArrowDown" ? links[0] : links[links.length - 1];
      if (target) window.requestAnimationFrame(() => target.focus());
    });

    panel.addEventListener("keydown", (event) => {
      if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) return;
      const links = Array.from(panel.querySelectorAll("a"));
      const currentIndex = links.indexOf(document.activeElement);
      if (currentIndex < 0 || !links.length) return;
      event.preventDefault();
      let nextIndex = currentIndex;
      if (event.key === "ArrowDown") nextIndex = (currentIndex + 1) % links.length;
      if (event.key === "ArrowUp") nextIndex = (currentIndex - 1 + links.length) % links.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = links.length - 1;
      links[nextIndex].focus();
    });

    triggerWrap.addEventListener("pointerenter", () => {
      cancelClose();
      if (!mobileQuery.matches) setMegaOpen(true, false);
    });
    triggerWrap.addEventListener("pointerleave", () => {
      if (!mobileQuery.matches) scheduleClose();
    });
    triggerWrap.addEventListener("focusout", (event) => {
      if (!mobileQuery.matches && !triggerWrap.contains(event.relatedTarget)) scheduleClose();
    });

    root.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      if (trigger.getAttribute("aria-expanded") === "true") {
        event.preventDefault();
        setMegaOpen(false, true);
      } else if (mobileToggle.getAttribute("aria-expanded") === "true") {
        event.preventDefault();
        setMobileOpen(false);
        mobileToggle.focus();
      }
    });

    root.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (link && mobileQuery.matches) setMobileOpen(false);
    });

    document.addEventListener("pointerdown", (event) => {
      if (!triggerWrap.contains(event.target)) setMegaOpen(false, false);
      if (
        mobileQuery.matches
        && mobileToggle.getAttribute("aria-expanded") === "true"
        && !primaryLinks.contains(event.target)
        && !mobileToggle.contains(event.target)
      ) {
        setMobileOpen(false);
      }
    });

    const handleViewportChange = () => {
      setMegaOpen(false, false);
      setMobileOpen(false);
    };
    if (typeof mobileQuery.addEventListener === "function") mobileQuery.addEventListener("change", handleViewportChange);
    else if (typeof mobileQuery.addListener === "function") mobileQuery.addListener(handleViewportChange);
  };

  const mount = () => {
    const navMount = document.querySelector("[data-aics-navigation-mount]");
    if (navMount && !document.querySelector(`[${ROOT_ATTRIBUTE}]`)) {
      const root = createNavigation();
      navMount.replaceWith(root);
      initialiseInteractions(root);
    }

    const footerMount = document.querySelector("[data-aics-footer-mount]");
    if (footerMount && !document.querySelector(`[${FOOTER_ATTRIBUTE}]`)) footerMount.replaceWith(createFooter());
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount, { once: true });
  else mount();
})();

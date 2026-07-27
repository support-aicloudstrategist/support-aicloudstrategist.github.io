(() => {
  "use strict";

  const ROOT_ATTRIBUTE = "data-aics-global-nav";
  const MOBILE_BREAKPOINT = "(max-width: 1020px)";

  const PRIMARY_LINKS = Object.freeze([
    { label: "Home", href: "/" },
    { label: "Proof", href: "/case-studies/" },
    { label: "Resources", href: "/resources/" },
    { label: "About", href: "/about/" },
  ]);

  const MEGA_GROUPS = Object.freeze([
    {
      heading: "Enterprise AI Services",
      items: Object.freeze([
        { label: "Production AI Assurance", href: "/services/ai-mlops/" },
        { label: "Enterprise AI Systems & Agents", href: "/services/ai-automation/" },
        { label: "AI FinOps & Cloud Economics", href: "/services/cloud-finops/" },
        { label: "AI Security, Compliance & Sovereign Platforms", href: "/services/cloud-security/" },
        { label: "Managed AI Platforms & Operations", href: "/services/devops-observability/" },
      ]),
    },
    {
      heading: "Specialist Practices",
      items: Object.freeze([
        { label: "Business Growth Systems", href: "/contact.html?service=business-growth-systems" },
        { label: "AI Creative Studio", href: "/ai-creative-studio/" },
      ]),
    },
  ]);

  const CTA = Object.freeze({ label: "Discuss your AI initiative", href: "/contact.html?service=enterprise-ai" });

  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character]);

  const normalisePath = (value) => {
    const path = String(value || "/").replace(/index\.html$/i, "");
    if (path === "/") return path;
    return path.endsWith("/") ? path : `${path}/`;
  };

  const linkMarkup = ({ label, href }, className = "aics-nav-link") => {
    const current = normalisePath(window.location.pathname) === normalisePath(href);
    return `<a class="${className}" href="${escapeHtml(href)}"${current ? ' aria-current="page"' : ""}>${escapeHtml(label)}</a>`;
  };

  const megaMarkup = () => MEGA_GROUPS.map((group) => `
    <section class="aics-mega-group" aria-labelledby="aics-mega-${escapeHtml(group.heading.toLowerCase().replace(/[^a-z0-9]+/g, "-"))}">
      <h2 class="aics-mega-heading" id="aics-mega-${escapeHtml(group.heading.toLowerCase().replace(/[^a-z0-9]+/g, "-"))}">${escapeHtml(group.heading)}</h2>
      <div class="aics-mega-items">
        ${group.items.map((item) => linkMarkup(item, "aics-mega-link")).join("")}
      </div>
    </section>
  `).join("");

  const createNavigation = () => {
    const root = document.createElement("div");
    root.className = "aics-global-nav";
    root.setAttribute(ROOT_ATTRIBUTE, "");
    root.innerHTML = `
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

  const initialiseInteractions = (root) => {
    const mobileQuery = window.matchMedia(MOBILE_BREAKPOINT);
    const mobileToggle = root.querySelector(".aics-nav-mobile-toggle");
    const primaryLinks = root.querySelector(".aics-primary-links");
    const triggerWrap = root.querySelector(".aics-mega-trigger-wrap");
    const trigger = root.querySelector(".aics-mega-trigger");
    const panel = root.querySelector(".aics-mega-panel");
    const supportsPopover = typeof primaryLinks.showPopover === "function";
    let closeTimer = 0;

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

    const setMegaOpen = (open, returnFocus = false) => {
      window.clearTimeout(closeTimer);
      panel.hidden = !open;
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

    const scheduleClose = () => {
      window.clearTimeout(closeTimer);
      closeTimer = window.setTimeout(() => setMegaOpen(false, false), 140);
    };

    mobileToggle.addEventListener("click", () => {
      setMobileOpen(mobileToggle.getAttribute("aria-expanded") !== "true");
    });

    trigger.addEventListener("click", () => {
      if (mobileQuery.matches) {
        setMegaOpen(trigger.getAttribute("aria-expanded") !== "true", false);
      } else {
        setMegaOpen(true, false);
      }
    });

    trigger.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
      event.preventDefault();
      setMegaOpen(true, false);
      const links = panel.querySelectorAll(".aics-mega-link");
      const target = event.key === "ArrowDown" ? links[0] : links[links.length - 1];
      if (target) window.requestAnimationFrame(() => target.focus());
    });

    panel.addEventListener("keydown", (event) => {
      if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) return;
      const links = Array.from(panel.querySelectorAll(".aics-mega-link"));
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
    if (document.querySelector(`[${ROOT_ATTRIBUTE}]`)) return;
    const mountPoint = document.querySelector("[data-aics-navigation-mount]");
    if (!mountPoint) return;
    const root = createNavigation();
    mountPoint.replaceWith(root);
    initialiseInteractions(root);
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount, { once: true });
  else mount();
})();

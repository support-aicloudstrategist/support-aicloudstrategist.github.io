(() => {
  "use strict";

  const ROOT_ATTRIBUTE = "data-aics-global-nav";
  const FOOTER_ATTRIBUTE = "data-aics-global-footer";
  const MOBILE_BREAKPOINT = "(max-width: 1020px)";
  const SERVICE = "/cloud-ai-cost-governance-diagnostic/";
  const FIT_REVIEW = "/request-fit-review/";
  const CTA_LABEL = "Request a Cloud & AI Cost Fit Review";
  const SERVICE_NAME = "Cloud & AI Cost Governance Diagnostic";

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

  const currentAttribute = (href) => (
    normalisePath(window.location.pathname) === normalisePath(href) ? ' aria-current="page"' : ""
  );

  const createNavigation = () => {
    const root = document.createElement("div");
    root.className = "aics-global-nav";
    root.setAttribute(ROOT_ATTRIBUTE, "");
    root.innerHTML = `
      <aside class="aics-utility-bar" data-aics-utility-bar aria-label="Service and contact information">
        <div class="aics-utility-inner">
          <span class="aics-utility-trust"><span class="aics-utility-status" aria-hidden="true"></span><span class="aics-utility-trust-copy">${SERVICE_NAME} · India and international delivery</span><span class="aics-utility-mobile-copy">Cost governance · Global delivery</span></span>
          <span class="aics-utility-contacts"><a href="mailto:contact@aicloudstrategist.com"><span class="aics-utility-email">contact@aicloudstrategist.com</span><span class="aics-utility-email-short">Email</span></a></span>
        </div>
      </aside>
      <nav class="aics-nav-shell" aria-label="Primary navigation">
        <div class="aics-nav-bar">
          <a class="aics-nav-brand" href="/"><span class="aics-nav-mark" aria-hidden="true">AI</span><span class="aics-nav-name">AICloudStrategist</span></a>
          <button class="aics-nav-mobile-toggle" type="button" aria-expanded="false" aria-controls="aics-primary-links" aria-label="Open navigation"><span></span><span></span><span></span></button>
          <div class="aics-primary-links" id="aics-primary-links">
            <a class="aics-nav-link" href="${SERVICE}"${currentAttribute(SERVICE)}>Diagnostic</a>
            <a class="aics-nav-link" href="/#process">Method</a>
            <a class="aics-nav-link" href="/resources/cloud-ai-economics-decision-pack/"${currentAttribute("/resources/cloud-ai-economics-decision-pack/")}>Decision Pack</a>
            <a class="aics-nav-link" href="/resources/"${currentAttribute("/resources/")}>Resources</a>
            <a class="aics-nav-link" href="/about/"${currentAttribute("/about/")}>About</a>
            <a class="aics-nav-cta" href="${FIT_REVIEW}"${currentAttribute(FIT_REVIEW)}>${CTA_LABEL}</a>
          </div>
        </div>
      </nav>`;
    return root;
  };

  const createFooter = () => {
    const footer = document.createElement("footer");
    footer.className = "aics-global-footer";
    footer.setAttribute(FOOTER_ATTRIBUTE, "");
    footer.innerHTML = `
      <div class="aics-footer-inner">
        <div class="aics-footer-grid">
          <section class="aics-footer-brand-block"><a class="aics-footer-brand" href="/"><span class="aics-footer-mark" aria-hidden="true">AI</span><span>AICloudStrategist</span></a><p>Cloud and AI cost governance for accountable technology decisions.</p><small>AICLOUDSTRATEGIST PRIVATE LIMITED · CIN U62020DC2026PTC470945</small></section>
          <section class="aics-footer-group"><h2>Diagnostic</h2><a href="${SERVICE}">Service scope</a><a href="/resources/cloud-ai-economics-decision-pack/">Representative Decision Pack</a><a href="${FIT_REVIEW}">${CTA_LABEL}</a></section>
          <section class="aics-footer-group"><h2>Company</h2><a href="/about/">About</a><a href="/trust-data-handling/">Trust & data handling</a><a href="/company-details/">Registered company details</a></section>
          <section class="aics-footer-contact"><h2>Contact</h2><a href="mailto:contact@aicloudstrategist.com">contact@aicloudstrategist.com</a><p><a href="/privacy">Privacy</a> · <a href="/terms">Terms</a></p></section>
        </div>
        <div class="aics-footer-bottom"><span>© AICloudStrategist</span><span>${SERVICE_NAME}</span></div>
      </div>`;
    return footer;
  };

  const initialiseNavigation = (root) => {
    const mobileQuery = window.matchMedia(MOBILE_BREAKPOINT);
    const toggle = root.querySelector(".aics-nav-mobile-toggle");
    const links = root.querySelector(".aics-primary-links");
    const setOpen = (open) => {
      links.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    };
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    links.addEventListener("click", (event) => {
      if (event.target.closest("a") && mobileQuery.matches) setOpen(false);
    });
    root.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
    const reset = () => setOpen(false);
    if (typeof mobileQuery.addEventListener === "function") mobileQuery.addEventListener("change", reset);
    else if (typeof mobileQuery.addListener === "function") mobileQuery.addListener(reset);
  };

  const mount = () => {
    const navMount = document.querySelector("[data-aics-navigation-mount]");
    if (navMount && !document.querySelector(`[${ROOT_ATTRIBUTE}]`)) {
      const root = createNavigation();
      navMount.replaceWith(root);
      initialiseNavigation(root);
    }
    const footerMount = document.querySelector("[data-aics-footer-mount]");
    if (footerMount && !document.querySelector(`[${FOOTER_ATTRIBUTE}]`)) footerMount.replaceWith(createFooter());
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount, { once: true });
  else mount();
})();

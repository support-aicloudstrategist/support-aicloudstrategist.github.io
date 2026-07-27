(() => {
  const normaliseBrandNames = () => {
    if (!document.body.classList.contains("paa-page")) return;
    document.querySelectorAll(".aics-nav-brand, .aics-footer-brand").forEach((link) => {
      link.setAttribute("aria-label", "AI AICloudStrategist home");
    });
  };

  normaliseBrandNames();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", normaliseBrandNames, { once: true });
  }
})();

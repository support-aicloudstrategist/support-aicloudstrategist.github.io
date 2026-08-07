(() => {
  const browser = document.querySelector(".air-artifact-browser");
  if (!browser) return;

  const tabs = Array.from(browser.querySelectorAll('[role="tab"]'));
  const panels = Array.from(browser.querySelectorAll('[role="tabpanel"]'));
  const mobile = window.matchMedia("(max-width: 767px)");

  const selectedIndex = () => Math.max(0, tabs.findIndex((tab) => tab.getAttribute("aria-selected") === "true"));

  const showAllPanels = () => {
    panels.forEach((panel) => panel.removeAttribute("hidden"));
  };

  const activate = (index, moveFocus = false) => {
    const safeIndex = (index + tabs.length) % tabs.length;
    tabs.forEach((tab, tabIndex) => {
      const active = tabIndex === safeIndex;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(tab.getAttribute("aria-controls"));
      if (panel) panel.toggleAttribute("hidden", !active);
    });
    if (moveFocus) tabs[safeIndex].focus();
  };

  const syncViewport = () => {
    if (mobile.matches) {
      showAllPanels();
      tabs.forEach((tab) => { tab.tabIndex = -1; });
      return;
    }
    activate(selectedIndex());
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(index));
    tab.addEventListener("keydown", (event) => {
      let next = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") next = index + 1;
      else if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = index - 1;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(next, true);
    });
  });

  if (typeof mobile.addEventListener === "function") mobile.addEventListener("change", syncViewport);
  else mobile.addListener(syncViewport);

  syncViewport();
})();

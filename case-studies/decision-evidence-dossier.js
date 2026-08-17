// Route-local accessibility repair: preserve smooth scrolling while moving focus past navigation.
(() => {
  const skipLink = document.querySelector('.dossier-skip-link[href="#main-content"]');
  const main = document.getElementById('main-content');
  if (!skipLink || !main) return;

  skipLink.addEventListener('click', () => {
    window.requestAnimationFrame(() => {
      main.focus({ preventScroll: true });
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', '#main-content');
      }
    });
  });
})();

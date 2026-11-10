from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "css" / "cost-governance.css").read_text(encoding="utf-8")
JS = (ROOT / "js" / "cost-governance.js").read_text(encoding="utf-8")


class MotionAndResponsiveContractTests(unittest.TestCase):
    def test_cost_map_has_keyboard_operable_filters(self):
        self.assertEqual(HOME.count("data-cost-filter="), 3)
        self.assertEqual(HOME.count("data-cost-source="), 3)
        self.assertIn('aria-label="Explore the representative cost path"', HOME)
        for value in ("cloud", "kubernetes", "ai-gpu"):
            self.assertIn(f'data-cost-filter="{value}"', HOME)
            self.assertIn(f'data-cost-source="{value}"', HOME)

    def test_interaction_exposes_state_accessibly(self):
        self.assertIn('aria-pressed="true"', HOME)
        self.assertGreaterEqual(HOME.count('aria-pressed="false"'), 2)
        self.assertIn("data-cost-state", HOME)
        self.assertIn("setAttribute('aria-pressed'", JS)
        self.assertIn("dataset.costState", JS)

    def test_motion_is_meaningful_and_not_scroll_jacking(self):
        for mechanism in ("@keyframes data-pulse", "@keyframes orbit-spin", "@keyframes system-scan", "IntersectionObserver"):
            self.assertIn(mechanism, CSS + JS)
        for forbidden in ("preventDefault()", "window.scrollTo({", "setInterval("):
            self.assertNotIn(forbidden, JS)

    def test_reduced_motion_and_no_js_fallbacks_exist(self):
        self.assertIn("prefers-reduced-motion: reduce", CSS)
        self.assertIn("prefers-reduced-motion: reduce", JS)
        self.assertIn("<noscript>", HOME.lower())
        reduced = re.search(r"@media \(prefers-reduced-motion: reduce\)(.*)$", CSS, re.S)
        self.assertIsNotNone(reduced)
        if reduced is not None:
            self.assertIn("animation-duration: .01ms", reduced.group(1))
            self.assertIn("[data-reveal]", reduced.group(1))

    def test_mobile_and_tablet_layout_contracts_exist(self):
        self.assertIn("@media (max-width: 1050px)", CSS)
        self.assertGreaterEqual(CSS.count("@media (max-width: 820px)"), 1)
        self.assertGreaterEqual(CSS.count("@media (max-width: 560px)"), 1)
        self.assertIn("overflow-x: hidden", CSS)

    def test_visual_is_disclosed_as_illustrative(self):
        lower = HOME.lower()
        self.assertIn("representative cost-ownership model", lower)
        self.assertIn("illustrative system", lower)
        self.assertIn("no customer data or achieved outcome", lower)


if __name__ == "__main__":
    unittest.main()

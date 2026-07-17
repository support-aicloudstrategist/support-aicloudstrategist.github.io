import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "growth-control-os" / "index.html"


class GrowthControlOsRegressionTests(unittest.TestCase):
    def test_removed_legacy_navigation_cannot_abort_reveal_initialization(self):
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn('data-aics-site-nav', html)
        self.assertNotIn('id="mobileToggle"', html)
        self.assertNotIn('id="navLinks"', html)
        self.assertIn(
            "if (mt && nl)",
            html,
            "The legacy mobile-navigation hook must be guarded after the shared navigation replaces its DOM IDs.",
        )


if __name__ == "__main__":
    unittest.main()

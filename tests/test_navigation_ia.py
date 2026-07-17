import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAV_JS = ROOT / "js" / "site-navigation.js"
NAV_CSS = ROOT / "css" / "site-navigation.css"
MAPPED_PAGES = {
    "Production AI Assurance": ROOT / "services" / "ai-mlops" / "index.html",
    "Enterprise AI Systems & Agents": ROOT / "services" / "ai-automation" / "index.html",
    "AI FinOps & Cloud Economics": ROOT / "services" / "cloud-finops" / "index.html",
    "AI Security, Compliance & Sovereign Platforms": ROOT / "services" / "cloud-security" / "index.html",
    "Managed AI Platforms & Operations": ROOT / "services" / "devops-observability" / "index.html",
    "Digital Presence & Search Growth": ROOT / "services" / "website-digital-presence" / "index.html",
    "Lead Operations & Revenue Automation": ROOT / "lead-capture-follow-up" / "index.html",
    "Digital Trust & Compliance": ROOT / "trust-compliance" / "index.html",
    "Growth & Control Operating System": ROOT / "growth-control-os" / "index.html",
    "AI Creative Studio": ROOT / "ai-creative-studio" / "index.html",
}
EXPECTED_LINKS = {
    "Production AI Assurance": "/services/ai-mlops/",
    "Enterprise AI Systems & Agents": "/services/ai-automation/",
    "AI FinOps & Cloud Economics": "/services/cloud-finops/",
    "AI Security, Compliance & Sovereign Platforms": "/services/cloud-security/",
    "Managed AI Platforms & Operations": "/services/devops-observability/",
    "Digital Presence & Search Growth": "/services/website-digital-presence/",
    "Lead Operations & Revenue Automation": "/lead-capture-follow-up/",
    "Digital Trust & Compliance": "/trust-compliance/",
    "Growth & Control Operating System": "/growth-control-os/",
    "AI Creative Studio": "/ai-creative-studio/",
}


class NavigationInformationArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.nav_js = NAV_JS.read_text(encoding="utf-8") if NAV_JS.exists() else ""
        cls.nav_css = NAV_CSS.read_text(encoding="utf-8") if NAV_CSS.exists() else ""

    def test_core_growth_content_is_the_root_homepage_not_a_choice_gate(self):
        self.assertIn("Growth you can measure. Control you can see.", self.home)
        self.assertNotIn("Choose Your Path", self.home)
        self.assertIn('<link rel="canonical" href="https://aicloudstrategist.com/"', self.home)
        redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
        self.assertRegex(redirects, r"(?m)^/home-core-growth/\*\s+/\s+301!")

    def test_old_home_variant_is_removed_from_sitemap(self):
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        locations = [node.text for node in sitemap.iter() if node.tag.endswith("loc")]
        self.assertNotIn("https://aicloudstrategist.com/home-core-growth/", locations)

    def test_primary_navigation_uses_what_we_do_and_omits_industries(self):
        self.assertIn("What We Do", self.nav_js)
        self.assertNotRegex(self.nav_js, r'href=["\']/industries(?:\.html)?/?["\']')
        self.assertIn("Business Growth Systems", self.nav_js)
        self.assertIn("Specialist Studio", self.nav_js)

    def test_mega_menu_maps_all_approved_offers_to_existing_pages(self):
        for label, href in EXPECTED_LINKS.items():
            with self.subTest(label=label):
                self.assertIn(label, self.nav_js)
                self.assertIn(href, self.nav_js)
                self.assertTrue(MAPPED_PAGES[label].is_file())

    def test_navigation_assets_are_shared_by_home_and_mapped_pages(self):
        pages = [ROOT / "index.html", ROOT / "services" / "index.html", *MAPPED_PAGES.values()]
        for page in pages:
            with self.subTest(page=str(page.relative_to(ROOT))):
                html = page.read_text(encoding="utf-8")
                self.assertIn('/css/site-navigation.css', html)
                self.assertIn('/js/site-navigation.js', html)
                self.assertIn('data-aics-site-nav', html)

    def test_mega_menu_supports_keyboard_touch_and_accessible_state(self):
        required_js = (
            "aria-expanded",
            "aria-controls",
            "Escape",
            "focusin",
            "pointerenter",
            "click",
        )
        for token in required_js:
            with self.subTest(token=token):
                self.assertIn(token, self.nav_js)
        self.assertIn("aria-label=\"Primary navigation\"", self.nav_js)

    def test_translucent_menu_has_responsive_and_accessibility_fallbacks(self):
        for token in (
            "backdrop-filter",
            "@supports not",
            "@media (max-width: 900px)",
            "prefers-reduced-motion",
            ":focus-visible",
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.nav_css)


if __name__ == "__main__":
    unittest.main()

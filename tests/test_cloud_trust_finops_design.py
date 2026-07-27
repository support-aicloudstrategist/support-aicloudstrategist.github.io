import re
import unittest
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "cloud-trust-finops" / "index.html"


class CloudTrustFinOpsDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_uses_the_shared_site_shell_assets(self):
        self.assertIn('href="/css/styles.css?v=clean-navbar-20260604"', self.html)
        self.assertIn('src="/js/main.js?v=clean-navbar-20260604"', self.html)
        self.assertIn('href="/css/site-navigation.css?v=premium-shell-20260727"', self.html)
        self.assertIn('src="/js/site-navigation.js?v=premium-shell-20260727"', self.html)
        self.assertIn('data-aics-navigation-mount', self.html)
        self.assertNotIn('class="topbar"', self.html)
        self.assertRegex(self.html, r'<body class="[^"]*reform-site[^"]*cloud-finops-page[^"]*">')

    def test_page_content_is_scoped_away_from_shared_navigation(self):
        self.assertIn('<main class="finops-content">', self.html)
        style = re.search(r"<style>(.*?)</style>", self.html, re.S).group(1)
        self.assertNotRegex(style, r"(?:^|})\s*\.nav\s*\{")
        self.assertNotRegex(style, r"(?:^|})\s*\.brand\s*\{")
        self.assertNotRegex(style, r"(?:^|})\s*\.btn\s*\{")

    def test_uses_consistent_premium_footer(self):
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)
        self.assertNotIn('data-aics-footer-mount', self.html)
        self.assertRegex(self.html, r'(?s)<footer\b[^>]*data-aics-global-footer[^>]*>.*?</footer>\s*</body>')
        self.assertIn('href="tel:+918065480898"', self.html)

    def test_page_sections_override_shared_shell_vertical_padding(self):
        style = re.search(r"<style>(.*?)</style>", self.html, re.S).group(1)
        self.assertIn(".finops-content .section{margin-top:24px;padding:0!important}", style)
        self.assertRegex(style, r"\.finops-content \.diagnostic\{[^}]*padding:32px!important")
        self.assertIn(".finops-content .diagnostic{padding:22px!important;border-radius:22px}", style)

    def test_existing_offer_copy_and_destinations_are_preserved(self):
        required = [
            "Cloud clarity, cost control, and trust for serious growth.",
            "FinOps cost discipline",
            "Trust & control basics",
            "Founder dashboard",
            "Who this is for",
            "Safe promise",
            "Cloud Trust & FinOps diagnostic outline",
            "What the customer receives",
            '/free-business-review/?service=cloud-trust-finops',
            '/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison/',
            '/resources/uae-saas-cloud-finops-trust-diagnostic-package/',
        ]
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.html)


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "tests/fixtures/premium-shell-baseline.json").read_text())["pages"]


def extract(pattern, source):
    match = re.search(pattern, source, re.I | re.S)
    return match.group(1) if match else None


class PremiumShellPreservationTests(unittest.TestCase):
    def test_public_page_denominator_and_content_are_preserved(self):
        current = {}
        for path in sorted(ROOT.rglob("*.html")):
            if ".git" in path.parts:
                continue
            source = path.read_text(errors="replace")
            if "data-aics-navigation-mount" not in source:
                continue
            rel = path.relative_to(ROOT).as_posix()
            main = re.search(r"<main\b[^>]*>.*?</main\s*>", source, re.I | re.S)
            forms = re.findall(r"<form\b[^>]*>.*?</form\s*>", source, re.I | re.S)
            current[rel] = {
                "main_sha256": hashlib.sha256(main.group(0).encode()).hexdigest() if main else None,
                "title": extract(r"<title\b[^>]*>(.*?)</title\s*>", source),
                "canonical": extract(
                    r"<link\b(?=[^>]*\brel=[\"'][^\"']*canonical[^\"']*[\"'])(?=[^>]*\bhref=[\"']([^\"']+)[\"'])[^>]*>",
                    source,
                ),
                "forms": len(forms),
                "forms_sha256": hashlib.sha256("".join(forms).encode()).hexdigest(),
            }
        self.assertEqual(set(current), set(BASELINE))
        self.assertEqual(current, BASELINE)

    def test_every_public_page_uses_one_canonical_shell_contract(self):
        for rel in BASELINE:
            source = (ROOT / rel).read_text(errors="replace")
            with self.subTest(page=rel):
                self.assertEqual(source.count('data-aics-navigation-mount'), 1)
                self.assertEqual(source.count('data-aics-global-footer'), 1)
                self.assertEqual(source.count('data-aics-footer-mount'), 0)
                self.assertEqual(source.count('/css/site-navigation.css?v=premium-shell-20260727'), 1)
                expected_navigation_script = (
                    '/js/site-navigation.js?v=20260801-ai-systems'
                    if rel == 'services/ai-automation/index.html'
                    else '/js/site-navigation.js?v=premium-shell-20260727'
                )
                self.assertEqual(source.count(expected_navigation_script), 1)
                self.assertEqual(source.count('/js/site-navigation.js?v='), 1)
                self.assertRegex(source, r'(?s)<footer\b[^>]*data-aics-global-footer[^>]*>.*?</footer>\s*</body>')
                self.assertIn('href="mailto:contact@aicloudstrategist.com"', source)
                self.assertIn('href="tel:+918065480898"', source)
                self.assertIn('href="/privacy.html"', source)
                self.assertIn('href="/terms.html"', source)
                self.assertIsNone(re.search(r'tel:[^"\']*\*', source))
                self.assertIsNone(re.search(r'class=["\'][^"\']*\btopbar\b', source, re.I))

    def test_shell_source_contains_approved_information_architecture(self):
        js = (ROOT / "js/site-navigation.js").read_text()
        for label in (
            "Production AI Assurance",
            "Enterprise AI Systems & Agents",
            "AI FinOps & Cloud Economics",
            "AI Security, Compliance & Sovereign Platforms",
            "Managed AI Platforms & Operations",
            "AI Digital Presence",
            "AI Lead Intelligence",
            "AI Trust Layer",
            "AI Growth Operations",
            "Advertisements",
            "Commercials",
            "Product visuals",
            "Campaign assets",
            "Promotional videos",
            "Social media creatives",
        ):
            self.assertIn(label, js)
        self.assertIn('heading: "Enterprise AI"', js)
        self.assertIn('heading: "Business Growth Systems"', js)
        self.assertIn('heading: "AI Creative Studio"', js)
        self.assertIn('contact@aicloudstrategist.com', js)
        self.assertIn('+91 80654 80898', js)
        self.assertEqual(js.count('tel:+918065480898'), 2)
        self.assertNotRegex(js, r'tel:[^"\']*\*')
        self.assertIn('data-aics-utility-bar', js)
        self.assertIn('data-aics-global-footer', js)

    def test_page_specific_outcome_disclosures_are_preserved(self):
        expected = {
            "growth-control-os/index.html": "We do not guarantee revenue outcomes or fabricate proof.",
            "healthcare-growthos/index.html": "does not guarantee patient bookings or medical outcomes.",
            "website-digital-presence/index.html": "does not guarantee traffic or sales.",
        }
        for rel, text in expected.items():
            source = (ROOT / rel).read_text(errors="replace")
            with self.subTest(page=rel):
                self.assertEqual(source.count('data-aics-page-disclosure'), 1)
                self.assertIn(text, source)

    def test_approved_homepage_capability_sections_survive_shell_migration(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "css/homepage-enterprise.css").read_text(encoding="utf-8")

        self.assertIn('<section class="section ea-services" id="services">', home)
        self.assertEqual(home.count("data-enterprise-service"), 5)
        self.assertEqual(home.count('class="ea-card-top"'), 5)
        for marker in (
            "ea-visual-assure",
            "ea-visual-build",
            "ea-visual-finance",
            "ea-visual-secure",
            "ea-visual-operate",
        ):
            self.assertIn(marker, home)
        self.assertIn("Enterprise AI capabilities", home)

        self.assertIn('id="business-growth-systems"', home)
        self.assertEqual(home.count('class="ea-growth-card"'), 4)
        self.assertIn('id="ai-creative-studio"', home)
        self.assertIn("ea-creative-studio-showcase", home)
        self.assertIn("ea-creative-stage", home)

        self.assertNotIn('id="specialist-practices"', home)
        self.assertNotIn("ea-practice-grid", home)
        self.assertNotIn("Five disciplines for production AI.", home)
        self.assertNotIn("Focused capabilities for distinct commercial needs.", home)

        for marker in (
            ".ea-service-visual",
            ".ea-growth-grid",
            ".ea-creative-studio-showcase",
            ".ea-creative-stage",
        ):
            self.assertIn(marker, css)
        self.assertIn("enterprise-visual-20260727", home)

    def test_shell_styles_include_refinement_primitives(self):
        css = (ROOT / "css/site-navigation.css").read_text()
        for token in (
            ".aics-utility-bar",
            ".aics-mega-panel",
            ".aics-mega-group--creative",
            ".aics-creative-capability",
            ".aics-global-footer",
            "@keyframes aicsMegaReveal",
            "cubic-bezier(.22, 1, .36, 1)",
            "prefers-reduced-motion: reduce",
        ):
            self.assertIn(token, css)
        self.assertRegex(css, r"\.aics-nav-cta\s*\{[^}]*min-height:\s*42px")
        self.assertRegex(css, r"\.aics-nav-cta\s*\{[^}]*padding:\s*0 16px")


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_BASE = "29aeccfc9dd765dcb3dbd6cf8e73dcc22e0e057c"
ABOUT_ROUTES = (ROOT / "about" / "index.html", ROOT / "about.html")
CSS = ROOT / "css" / "about-dossier.css"
JS = ROOT / "js" / "about-dossier.js"
EXPECTED_SECTIONS = (
    "company-mandate",
    "principles",
    "capabilities",
    "delivery",
    "risk-authority",
    "evidence",
    "ownership",
    "why-aics",
    "contact",
)
FORBIDDEN_PERSONAL_TERMS = (
    "anushka",
    "rajiv",
    "founder",
    "headshot",
    "personal bio",
    '"@type":"person"',
)


def extract_footer(source: str) -> str:
    match = re.search(
        r"<footer\b[^>]*data-aics-global-footer[^>]*>.*?</footer>",
        source,
        re.I | re.S,
    )
    if not match:
        raise AssertionError("Missing shared global footer")
    return match.group(0)


def selectors(styles: str):
    def walk(rules):
        for rule in rules:
            if rule.type == "qualified-rule":
                yield tinycss2.serialize(rule.prelude).strip()
            elif (
                rule.type == "at-rule"
                and rule.lower_at_keyword in {"media", "supports", "layer"}
                and rule.content is not None
            ):
                nested = tinycss2.parse_rule_list(
                    rule.content, skip_whitespace=True, skip_comments=True
                )
                yield from walk(nested)

    rules = tinycss2.parse_stylesheet(styles, skip_whitespace=True, skip_comments=True)
    yield from walk(rules)


class AboutCapabilityDossierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = [path.read_text(encoding="utf-8") for path in ABOUT_ROUTES]
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")

    def test_both_about_aliases_are_identical(self):
        self.assertEqual(self.sources[0], self.sources[1])

    def test_approved_company_first_structure_is_complete_and_ordered(self):
        for source in self.sources:
            positions = []
            for section_id in EXPECTED_SECTIONS:
                marker = f'id="{section_id}"'
                self.assertEqual(source.count(marker), 1)
                positions.append(source.index(marker))
            self.assertEqual(positions, sorted(positions))
            self.assertEqual(source.count("data-aics-navigation-mount"), 1)
            self.assertEqual(source.count("data-aics-global-footer"), 1)

    def test_personal_credibility_and_founder_material_are_absent(self):
        for path, source in zip(ABOUT_ROUTES, self.sources):
            lower = source.lower()
            for term in FORBIDDEN_PERSONAL_TERMS:
                with self.subTest(path=path, term=term):
                    self.assertNotIn(term, lower)
            self.assertNotRegex(source, r"<img\b")

    def test_positioning_and_primary_cta_are_exact(self):
        required = (
            "AICloudStrategist brings engineering, security, evaluation and operating disciplines together for production AI initiatives",
            "Discuss your AI initiative",
            "/contact.html?service=enterprise-ai",
            "Enterprise AI Systems &amp; Agents",
            "Production AI Assurance",
            "AI FinOps &amp; Cloud Economics",
            "AI Security &amp; Sovereignty",
            "Managed AI Operations",
        )
        for source in self.sources:
            for phrase in required:
                self.assertIn(phrase, source)

    def test_structured_data_parses_and_identifies_the_company_page(self):
        for path in ABOUT_ROUTES:
            source = path.read_text()
            blocks = re.findall(
                r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                source,
                re.I | re.S,
            )
            self.assertEqual(len(blocks), 2, path)
            parsed = [json.loads(block) for block in blocks]
            self.assertEqual({item["@type"] for item in parsed}, {"Organization", "WebPage"})
            self.assertTrue(all(item["@context"] == "https://schema.org" for item in parsed))

    def test_finite_flow_selectors_reference_existing_sections(self):
        self.assertIn('id="contact"', self.sources[0])
        self.assertIn("#contact", self.css)
        self.assertIn("#contact", self.js)
        self.assertNotIn("#next-decision", self.css)
        self.assertNotIn("#next-decision", self.js)

    def test_proof_classes_and_boundaries_are_explicit(self):
        required = (
            "Published methodology",
            "Representative evidence · synthetic",
            "AICS self-case",
            "Not client work or a production screenshot",
            "No customer outcome is implied here",
            "makes no claim of certifications, partnerships, awards, testimonials or customer results",
        )
        for source in self.sources:
            for phrase in required:
                self.assertIn(phrase, source)
            for fabricated_pattern in (
                r'client-logo',
                r'<blockquote[^>]*testimonial',
                r'customer success rate',
                r'certified partner',
            ):
                self.assertIsNone(re.search(fabricated_pattern, source, re.I))

    def test_shared_footer_is_byte_identical_to_production_parent(self):
        parent = subprocess.check_output(
            ["git", "show", f"{PRODUCTION_BASE}:about/index.html"],
            cwd=ROOT,
            text=True,
        )
        expected = hashlib.sha256(extract_footer(parent).encode()).hexdigest()
        for source in self.sources:
            self.assertEqual(
                hashlib.sha256(extract_footer(source).encode()).hexdigest(), expected
            )

    def test_page_assets_are_dedicated_and_css_is_route_scoped(self):
        for source in self.sources:
            self.assertEqual(source.count('/css/about-dossier.css?v=20260810'), 1)
            self.assertEqual(source.count('/js/about-dossier.js?v=20260810'), 1)
            self.assertEqual(source.count('/css/site-navigation.css?v=premium-shell-20260727'), 1)
            self.assertEqual(source.count('/js/site-navigation.js?v=premium-shell-20260727'), 1)

        allowed = (
            "body.about-dossier",
            "html.has-js body.about-dossier",
        )
        for selector_list in selectors(self.css):
            for selector in selector_list.split(","):
                selector = selector.strip()
                with self.subTest(selector=selector):
                    self.assertTrue(
                        selector.startswith(allowed),
                        f"About CSS leaks outside the route scope: {selector}",
                    )

    def test_content_is_visible_without_javascript(self):
        default_rule = re.search(
            r"body\.about-dossier \.dossier-reveal\s*\{([^}]*)\}", self.css, re.S
        )
        self.assertIsNotNone(default_rule)
        default_body = default_rule.group(1) if default_rule else ""
        self.assertIn("opacity: 1", default_body)
        self.assertIn("transform: none", default_body)
        self.assertNotIn(".dossier-reveal.is-pending", self.css)
        self.assertNotIn("classList.add('is-pending')", self.js)
        self.assertIn("const flowScenes", self.js)
        self.assertIn("if (!page) return", self.js)

    def test_motion_is_purposeful_and_reduced_motion_is_static(self):
        for animation in (
            "dossierPathFlow",
            "dossierPacket",
            "dossierRailScan",
            "dossierSpineFlow",
            "dossierCtaPacket",
        ):
            self.assertIn(f"@keyframes {animation}", self.css)
        self.assertNotIn("infinite", self.css)
        reduced = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(.*)\}\s*$",
            self.css,
            re.S,
        )
        self.assertIsNotNone(reduced)
        reduced_body = reduced.group(1) if reduced else ""
        self.assertIn("animation: none !important", reduced_body)
        self.assertIn("transform: none", reduced_body)
        self.assertIn(".path-packet", reduced_body)

    def test_mobile_has_dedicated_architecture_and_no_horizontal_dependency(self):
        self.assertIn("@media (max-width: 640px)", self.css)
        mobile = self.css[self.css.index("@media (max-width: 640px)") :]
        for marker in (
            ".architecture-lines { display: none; }",
            ".delivery-rail { grid-template-columns: 1fr; }",
            ".authority-model ol { grid-template-columns: 1fr; gap: 8px; }",
            ".evidence-row { grid-template-columns: 1fr;",
        ):
            self.assertIn(marker, self.css if marker.startswith(".evidence") else mobile)
        self.assertIn("overflow-x: hidden", self.css)


if __name__ == "__main__":
    unittest.main()

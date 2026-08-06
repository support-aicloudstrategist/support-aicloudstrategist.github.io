import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "cloud-security" / "index.html"
STYLES = ROOT / "css" / "ai-security-sovereignty.css"


class AiSecurityFlagshipDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")

    def test_page_uses_dedicated_scoped_design_asset(self):
        self.assertIn('<body class="ai-security-page">', self.source)
        self.assertIn(
            '<link rel="stylesheet" href="/css/ai-security-sovereignty.css?v=20260806-1">',
            self.source,
        )
        self.assertNotRegex(self.source, r"<style\b")
        self.assertTrue(STYLES.exists(), "Dedicated AI Security stylesheet is missing")

    def test_semantic_page_shell_preserves_shared_assets(self):
        self.assertIn('class="ais-skip-link" href="#main-content"', self.source)
        self.assertEqual(len(re.findall(r"<main\b", self.source, flags=re.I)), 1)
        self.assertIn('<main id="main-content">', self.source)
        self.assertIn('data-aics-navigation-mount', self.source)
        self.assertEqual(self.source.count('data-aics-global-footer'), 1)
        self.assertIn('href="/css/site-navigation.css?v=premium-shell-20260727"', self.source)
        self.assertIn('src="/js/site-navigation.js?v=premium-shell-20260727"', self.source)

    def test_hero_contains_meaningful_ai_control_boundary(self):
        hero = re.search(
            r'<header\b[^>]*class="[^"]*ais-hero[^"]*"[^>]*>(.*?)</header>',
            self.source,
            flags=re.I | re.S,
        )
        self.assertIsNotNone(hero, "Missing flagship AI Security hero")
        assert hero is not None
        block = hero.group(1)
        self.assertIn('class="ais-hero-grid"', block)
        self.assertIn('<figure class="ais-boundary ais-boundary--hero"', block)
        self.assertIn('<figcaption', block)
        for boundary_object in [
            "Human authority",
            "Model or agent",
            "Enterprise data",
            "Tools and actions",
            "Platform, provider and jurisdiction",
            "Evidence-supported decision",
        ]:
            self.assertIn(boundary_object, block)
        for outcome in ["Proceed", "Controlled pilot", "Remediate", "Hold"]:
            self.assertIn(outcome, block)
        self.assertNotRegex(block, r"\b\d+%\b|security score|compliance score")

    def test_three_component_families_create_the_approved_narrative(self):
        expected_sections = [
            "security-boundary",
            "service-scope",
            "how-it-works",
            "deliverables",
            "fit",
            "why-aics",
            "enterprise-diligence",
            "connected-capabilities",
            "final-cta",
        ]
        actual_sections = re.findall(
            r'<section\b[^>]*class="[^"]*ais-section[^"]*"[^>]*id="([^"]+)"',
            self.source,
        )
        self.assertEqual(actual_sections, expected_sections)
        for component in [
            "ais-boundary",
            "ais-signal-ledger",
            "ais-control-model",
            "ais-journey",
            "ais-evidence-system",
            "ais-decision-panel",
        ]:
            self.assertIn(component, self.source)

    def test_method_is_a_connected_six_stage_journey(self):
        method = self.source[
            self.source.index('id="how-it-works"'):self.source.index('id="deliverables"')
        ]
        self.assertIn('class="ais-journey"', method)
        steps = re.findall(r'data-security-step="(\d+)"', method)
        self.assertEqual(steps, ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(method.count('class="ais-journey-step"'), 6)

    def test_deliverables_are_an_explicit_representative_evidence_system(self):
        deliverables = self.source[
            self.source.index('id="deliverables"'):self.source.index('id="fit"')
        ]
        self.assertIn('class="ais-evidence-system"', deliverables)
        self.assertIn('class="ais-evidence-brief"', deliverables)
        self.assertIn("Representative structure — not previous client work", deliverables)
        for field in [
            "Decision required",
            "Boundary reviewed",
            "Evidence state",
            "Assumptions and unknowns",
            "Accountable owner",
            "Release condition",
        ]:
            self.assertIn(field, deliverables)
        self.assertEqual(deliverables.count("data-representative-output="), 8)

    def test_fit_trust_diligence_and_conversion_are_decision_panels(self):
        fit = self.source[self.source.index('id="fit"'):self.source.index('id="why-aics"')]
        self.assertIn('class="ais-decision-panel ais-fit-panel"', fit)
        self.assertEqual(fit.count('class="ais-fit-side'), 2)

        why = self.source[
            self.source.index('id="why-aics"'):self.source.index('id="enterprise-diligence"')
        ]
        self.assertIn('class="ais-principles-ledger"', why)
        self.assertEqual(len(re.findall(r'<article class="ais-principle(?:\s|\")', why)), 5)

        diligence = self.source[
            self.source.index('id="enterprise-diligence"'):
            self.source.index('id="connected-capabilities"')
        ]
        self.assertIn("ais-responsibility-map", diligence)
        self.assertEqual(diligence.count('class="ais-responsibility"'), 3)

        final_cta = self.source[self.source.index('id="final-cta"'):self.source.index("</main>")]
        self.assertIn('class="ais-engagement-brief"', final_cta)
        for label in ["Bring", "First conversation", "Boundary"]:
            self.assertIn(label, final_cta)
        self.assertLess(
            final_cta.index("ais-engagement-brief"),
            final_cta.index("ais-actions"),
            "Engagement boundaries must be read before the final action",
        )
        self.assertIn("/contact.html?service=ai-security-sovereignty", final_cta)

    def test_page_css_is_scoped_responsive_static_and_accessible(self):
        css = STYLES.read_text(encoding="utf-8")
        self.assertGreater(len(css), 12000)
        for selector in [
            "body.ai-security-page",
            ".ai-security-page .ais-hero-grid",
            ".ai-security-page .ais-boundary-map",
            ".ai-security-page .ais-signal-ledger",
            ".ai-security-page .ais-control-model",
            ".ai-security-page .ais-journey",
            ".ai-security-page .ais-evidence-system",
            ".ai-security-page .ais-decision-panel",
            ".ai-security-page .ais-engagement-panel",
        ]:
            self.assertIn(selector, css)
        for contract in [
            "@media (max-width: 1100px)",
            "@media (max-width: 900px)",
            "@media (max-width: 680px)",
            "@media (max-width: 430px)",
            "@media (prefers-reduced-motion: reduce)",
            "@media (prefers-contrast: more)",
            "@media print",
            ":focus-visible",
        ]:
            self.assertIn(contract, css)
        self.assertNotIn("@keyframes", css)
        self.assertNotRegex(css, r"\banimation(?:-name)?\s*:")
        self.assertNotRegex(css, r"url\(\s*['\"]?https?://")

        def selectors(rules):
            for rule in rules:
                if rule.type == "qualified-rule":
                    yield tinycss2.serialize(rule.prelude).strip()
                elif rule.type == "at-rule" and rule.content is not None:
                    nested = tinycss2.parse_rule_list(
                        rule.content,
                        skip_comments=True,
                        skip_whitespace=True,
                    )
                    yield from selectors(nested)

        rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
        for selector_group in selectors(rules):
            for selector in selector_group.split(","):
                selector = selector.strip()
                self.assertIn(
                    ".ai-security-page",
                    selector,
                    f"Unscoped selector could affect another page: {selector}",
                )

    def test_tablet_control_model_uses_a_non_overlapping_composition(self):
        css = STYLES.read_text(encoding="utf-8")
        tablet = css[
            css.index("@media (max-width: 900px)"):
            css.index("@media (max-width: 680px)")
        ]
        self.assertIn(".ai-security-page .ais-control-centre", tablet)
        self.assertIn("position: relative", tablet)
        self.assertIn("grid-column: 1 / -1", tablet)
        self.assertIn("transform: none", tablet)
        self.assertIn(".ai-security-page .ais-control-domain", tablet)
    def test_mobile_control_model_keeps_its_continuous_connector(self):
        css = STYLES.read_text(encoding="utf-8")
        mobile = css[
            css.index("@media (max-width: 680px)"):
            css.index("@media (max-width: 430px)")
        ]
        connector = mobile[
            mobile.index(".ai-security-page .ais-control-model::before"):
            mobile.index(".ai-security-page .ais-control-model::after")
        ]
        self.assertIn('content: ""', connector)
    def test_desktop_why_heading_stays_inside_its_column(self):
        css = STYLES.read_text(encoding="utf-8")
        self.assertIn("@media (min-width: 1101px)", css)
        self.assertIn(".ai-security-page #why-aics .ais-section-grid", css)
        self.assertIn("minmax(0, 0.85fr) minmax(0, 1.15fr)", css)
        self.assertIn("font-size: clamp(2.8rem, 3.7vw, 3.3rem)", css)
        self.assertIn("@media (min-width: 901px) and (max-width: 1100px)", css)


if __name__ == "__main__":
    unittest.main()

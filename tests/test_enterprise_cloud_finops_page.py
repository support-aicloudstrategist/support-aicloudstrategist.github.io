import html
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "cloud-finops" / "index.html"
PHASE_TWO_CSS = ROOT / "css" / "enterprise-finops.css"


def text_content(source):
    without_scripts = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    without_tags = re.sub(r"<[^>]+>", " ", without_scripts)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def section(source, section_id):
    match = re.search(
        rf'<section\b[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>(.*?)</section>',
        source,
        flags=re.I | re.S,
    )
    if match is None:
        raise AssertionError(f"Missing section #{section_id}")
    return match.group(1)


class EnterpriseCloudFinOpsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.text = text_content(cls.source)
        cls.contact = (ROOT / "contact.html").read_text(encoding="utf-8")

    def test_phase_two_visual_system_is_page_scoped_and_external(self):
        self.assertIn(
            'href="/css/enterprise-finops.css?v=20260803-1"',
            self.source,
        )
        self.assertNotRegex(self.source, r"<style\b")
        css = PHASE_TWO_CSS.read_text(encoding="utf-8")
        self.assertGreater(len(css), 12000)
        for selector in [
            "body.enterprise-finops-page",
            ".enterprise-finops-page .finops-hero-grid",
            ".enterprise-finops-page .finops-control-brief",
            ".enterprise-finops-page .finops-control-stages",
            ".enterprise-finops-page .finops-output-grid",
            ".enterprise-finops-page #engagement",
            ".enterprise-finops-page #final-decision",
        ]:
            self.assertIn(selector, css)

    def test_phase_two_adds_semantic_executive_control_visual_without_fake_metrics(self):
        hero = re.search(
            r'<header\b[^>]*class="[^"]*finops-hero[^"]*"[^>]*>(.*?)</header>',
            self.source,
            flags=re.I | re.S,
        )
        assert hero is not None
        self.assertIn('class="finops-hero-grid"', hero.group(1))
        self.assertIn('<figure class="finops-control-brief"', hero.group(1))
        self.assertIn('<figcaption', hero.group(1))
        self.assertEqual(hero.group(1).count('class="finops-brief-stage"'), 4)
        self.assertNotRegex(hero.group(1), r"\b\d+%\b|\$\d|£\d|€\d")

    def test_visual_system_respects_accessibility_and_motion_preferences(self):
        css = PHASE_TWO_CSS.read_text(encoding="utf-8")
        self.assertIn(":focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("@media (prefers-contrast: more)", css)
        self.assertIn("@media print", css)
        self.assertIn('class="finops-skip-link" href="#main-content"', self.source)

    def test_visual_hierarchy_preserves_phase_one_section_architecture(self):
        expected = [
            "decision-triggers", "economic-control", "economic-scope", "decisions",
            "deliverables", "why-aics", "buyer-committee", "fit", "engagement",
            "procurement", "connected-capabilities", "final-decision",
        ]
        actual = re.findall(r'<section\b[^>]*class="[^"]*finops-section[^"]*"[^>]*id="([^"]+)"', self.source)
        self.assertEqual(actual, expected)

    def test_one_outcome_led_h1_and_context_preserving_hero_actions(self):
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", self.source, flags=re.I | re.S)
        self.assertEqual(len(h1s), 1)
        self.assertEqual(
            text_content(h1s[0]),
            "Turn cloud and AI spend into accountable business decisions.",
        )

        hero = re.search(
            r'<header\b[^>]*class="[^"]*finops-hero[^"]*"[^>]*>(.*?)</header>',
            self.source,
            flags=re.I | re.S,
        )
        assert hero is not None, "Missing Enterprise FinOps hero"
        actions = re.findall(
            r'<a\b[^>]*class="[^"]*finops-button[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            hero.group(1),
            flags=re.I | re.S,
        )
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0][0], "/contact.html?service=ai-finops-cloud-economics")
        self.assertEqual(text_content(actions[0][1]), "Request a Cloud & AI Economics Review")
        self.assertEqual(actions[1][0], "#economic-control")
        self.assertEqual(text_content(actions[1][1]), "See the economic control method")

    def test_customer_questions_are_answered_in_decision_order(self):
        required = [
            ("decision-triggers", "When cloud spend becomes an executive decision"),
            ("economic-control", "From cost data to governed decisions"),
            ("economic-scope", "One economic system across cloud and AI"),
            ("decisions", "Decisions this service is designed to support"),
            ("deliverables", "Decision evidence your teams can use"),
            ("why-aics", "Why AICloudStrategist for this decision"),
            ("buyer-committee", "Built for a cross-functional decision"),
            ("fit", "Where Enterprise FinOps Advisory creates the most value"),
            ("engagement", "Start with a decision baseline, not a free audit"),
            ("procurement", "Designed for enterprise diligence"),
            ("connected-capabilities", "Connected Enterprise AI capabilities"),
            ("final-decision", "Make the next cloud or AI investment decision with evidence"),
        ]
        positions = []
        for section_id, heading in required:
            block = section(self.source, section_id)
            self.assertIn(heading, text_content(block))
            positions.append(self.source.index(f'id="{section_id}"'))
        self.assertEqual(positions, sorted(positions))

    def test_economic_control_method_has_four_ordered_stages(self):
        block = section(self.source, "economic-control")
        stages = re.findall(
            r'data-control-stage="(\d+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>',
            block,
            flags=re.I | re.S,
        )
        self.assertEqual([number for number, _ in stages], ["1", "2", "3", "4"])
        self.assertEqual(
            [text_content(label) for _, label in stages],
            ["Economic visibility", "Accountable ownership", "Risk-constrained decisions", "Verified value"],
        )

    def test_scope_covers_established_finops_and_ai_economics(self):
        block = text_content(section(self.source, "economic-scope")).lower()
        required = [
            "aws, azure and google cloud",
            "allocation and shared costs",
            "forecasting and commitments",
            "kubernetes",
            "gpu utilisation",
            "token and inference economics",
            "quality, latency, reliability and risk",
            "cost per successful business outcome",
        ]
        for phrase in required:
            self.assertIn(phrase, block)

    def test_decision_model_is_not_a_savings_checklist(self):
        block = text_content(section(self.source, "decisions")).lower()
        for decision in ["scale", "optimise", "renegotiate", "rearchitect", "pause", "retire"]:
            self.assertIn(decision, block)
        self.assertIn("reliability", block)
        self.assertIn("security", block)
        self.assertIn("business value", block)

    def test_outputs_are_truthfully_labelled_and_do_not_invent_proof(self):
        block = section(self.source, "deliverables")
        outputs = [
            html.unescape(value)
            for value in re.findall(r'data-representative-output="([^"]+)"', block)
        ]
        self.assertEqual(
            outputs,
            [
                "Economic Baseline",
                "Allocation & Ownership Map",
                "Cloud Economics Ledger",
                "Commitment Decision Record",
                "Cloud & AI Unit Economics Tree",
                "90-Day Decision Portfolio",
                "Value Verification Record",
                "Executive Decision Brief",
            ],
        )
        copy = text_content(block).lower()
        self.assertIn("representative outputs", copy)
        self.assertIn("not previous client work", copy)
        self.assertIn("depends on scope and available evidence", copy)
        self.assertNotRegex(block, r"\b\d+%\b")

    def test_buyer_committee_and_procurement_roles_are_explicit(self):
        buyer = text_content(section(self.source, "buyer-committee")).lower()
        for role in ["cto or cio", "head of cloud", "finops lead", "cfo", "cloud architect"]:
            self.assertIn(role, buyer)

        procurement = text_content(section(self.source, "procurement")).lower()
        for phrase in [
            "least-privilege",
            "data retention",
            "production changes",
            "confidentiality",
            "decision ownership",
            "no guaranteed savings",
            "accounting policy",
            "product-value definitions",
            "vendor authority",
            "final commitment approval",
        ]:
            self.assertIn(phrase, procurement)

    def test_method_authority_and_fit_boundaries_are_explicit(self):
        why = text_content(section(self.source, "why-aics")).lower()
        for phrase in [
            "vendor-neutral",
            "economic evidence",
            "cloud and ai",
            "decision boundaries",
            "verified profiles",
        ]:
            self.assertIn(phrase, why)

        fit = text_content(section(self.source, "fit")).lower()
        for phrase in [
            "material to budget, margin or investment",
            "cross-functional ownership",
            "one-off bill cleanup",
            "reseller discount",
            "accounting, tax or legal opinion",
            "24/7 operations",
        ]:
            self.assertIn(phrase, fit)

    def test_aics_facilitates_evidence_while_client_retains_final_authority(self):
        connected = text_content(section(self.source, "connected-capabilities")).lower()
        self.assertIn("owns and facilitates the economic evidence layer", connected)
        self.assertIn("client retains final decision authority", connected)
        self.assertNotIn("finops owns the economic decision system", connected)

    def test_signature_terms_are_defined_before_they_are_used_as_outputs(self):
        method = text_content(section(self.source, "economic-control")).lower()
        self.assertIn("economic leakage map identifies", method)
        self.assertIn("spend-to-value topology connects", method)
        self.assertLess(method.index("economic leakage map identifies"), method.index("cloud economics ledger"))

    def test_contact_route_accepts_the_service_query_value(self):
        self.assertRegex(
            self.contact,
            r'<option value="ai-finops-cloud-economics">[^<]+</option>',
        )

    def test_connected_capabilities_preserve_portfolio_boundaries(self):
        block = section(self.source, "connected-capabilities")
        expected = {
            "/services/ai-automation/": "Enterprise AI Systems & Agents",
            "/services/ai-mlops/": "Production AI Assurance",
            "/services/devops-observability/": "Managed AI Operations",
            "/services/cloud-security/": "AI Security & Sovereignty",
        }
        links = {
            href: text_content(label)
            for href, label in re.findall(
                r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                block,
                flags=re.I | re.S,
            )
        }
        for href, label in expected.items():
            self.assertEqual(links.get(href), label)
        copy = text_content(block).lower()
        self.assertIn("owns and facilitates the economic evidence layer", copy)
        self.assertIn("client retains final decision authority", copy)
        self.assertIn("stand-alone engagement", copy)

    def test_legacy_low_trust_language_is_removed(self):
        lowered = self.text.lower()
        forbidden = [
            "primary seo target",
            "money page",
            "startups, saas teams",
            "get free growth review",
            "fastest revenue impact",
            "quick savings opportunities",
            "cloud & trust",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, lowered)

        unsupported = [
            "trusted by thousands",
            "award-winning",
            "world-leading",
            "industry-leading",
        ]
        for phrase in unsupported:
            self.assertNotIn(phrase, lowered)
        self.assertNotRegex(lowered, r"(?<!no )guaranteed savings")

    def test_route_shell_and_semantic_page_boundaries_are_preserved(self):
        self.assertIn("Enterprise FinOps Advisory", self.text)
        self.assertIn('<body class="enterprise-finops-page">', self.source)
        self.assertEqual(len(re.findall(r"<main\b", self.source, flags=re.I)), 1)
        self.assertIn('<main id="main-content">', self.source)
        self.assertIn('data-aics-navigation-mount', self.source)
        self.assertEqual(self.source.count('data-aics-global-footer'), 1)
        self.assertIn('href="/css/site-navigation.css?v=premium-shell-20260727"', self.source)
        self.assertIn('src="/js/site-navigation.js?v=premium-shell-20260727"', self.source)
        self.assertIn('<link rel="canonical" href="https://aicloudstrategist.com/services/cloud-finops/">', self.source)
        self.assertRegex(
            self.source,
            r'<nav class="[^"]*finops-shell[^"]*finops-breadcrumb[^"]*" aria-label="Breadcrumb">',
        )
        self.assertIn('<li aria-current="page">Cloud &amp; AI Economics</li>', self.source)


if __name__ == "__main__":
    unittest.main()

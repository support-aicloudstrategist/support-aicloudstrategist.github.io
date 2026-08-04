import html
import json
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "ai-mlops" / "index.html"
STYLES = ROOT / "css" / "production-ai-assurance.css"
SCRIPT = ROOT / "js" / "production-ai-assurance.js"


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


def qualified_selectors(styles):
    """Return style-rule selectors, recursing into conditional at-rules only."""
    def visit(rules):
        for rule in rules:
            if rule.type == "qualified-rule":
                yield tinycss2.serialize(rule.prelude).strip()
            elif (
                rule.type == "at-rule"
                and rule.lower_at_keyword in {"media", "supports", "layer"}
                and rule.content is not None
            ):
                nested = tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True)
                yield from visit(nested)

    rules = tinycss2.parse_stylesheet(styles, skip_comments=True, skip_whitespace=True)
    yield from visit(rules)


class ProductionAiAssurancePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.text = text_content(cls.source)
        cls.styles = STYLES.read_text(encoding="utf-8") if STYLES.exists() else ""
        cls.script = SCRIPT.read_text(encoding="utf-8") if SCRIPT.exists() else ""

    def test_metadata_positions_the_flagship_service_truthfully(self):
        self.assertIn("<title>Production AI Assurance Services | AICloudStrategist</title>", self.source)
        self.assertRegex(
            self.source,
            r'<meta name="description" content="[^"]*ready for production[^"]*release evidence[^"]*">',
        )
        self.assertIn(
            '<link rel="canonical" href="https://aicloudstrategist.com/services/ai-mlops/">',
            self.source,
        )
        self.assertIn('<meta property="og:title" content="Production AI Assurance Services | AICloudStrategist">', self.source)

        schema_match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            self.source,
            flags=re.S,
        )
        assert schema_match is not None, "Missing JSON-LD schema"
        schema = json.loads(schema_match.group(1))
        graph = schema["@graph"]
        service = next(item for item in graph if item.get("@type") == "Service")
        self.assertEqual(service["name"], "Production AI Assurance")
        self.assertEqual(service["url"], "https://aicloudstrategist.com/services/ai-mlops/")
        self.assertIn("production readiness", service["serviceType"].lower())

    def test_page_has_one_problem_led_h1_and_two_hero_actions(self):
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", self.source, flags=re.I | re.S)
        self.assertEqual(len(h1s), 1)
        self.assertEqual(text_content(h1s[0]), "Know whether your AI system is ready for production.")

        hero_match = re.search(r'<header\b[^>]*class="[^"]*paa-hero[^"]*"[^>]*>(.*?)</header>', self.source, flags=re.I | re.S)
        assert hero_match is not None, "Missing Production AI Assurance hero"
        hero = hero_match.group(1)
        actions = re.findall(r'<a\b[^>]*class="[^"]*paa-button[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', hero, flags=re.I | re.S)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0][0], "/contact.html?service=production-ai-assurance")
        primary_label = re.sub(r'<span\b[^>]*aria-hidden="true"[^>]*>.*?</span>', '', actions[0][1], flags=re.I | re.S)
        secondary_label = re.sub(r'<span\b[^>]*aria-hidden="true"[^>]*>.*?</span>', '', actions[1][1], flags=re.I | re.S)
        self.assertEqual(text_content(primary_label), "Assess your AI system")
        self.assertEqual(actions[1][0], "#how-it-works")
        self.assertEqual(text_content(secondary_label), "See how assurance works")

    def test_required_customer_questions_are_answered_in_order(self):
        required = [
            ("why-production-ai-fails", "Why production AI fails"),
            ("how-it-works", "How Production AI Assurance works"),
            ("what-youll-receive", "What you'll receive"),
            ("who-this-is-for", "Who this is for"),
            ("why-aicloudstrategist", "Why AICloudStrategist"),
            ("connected-capabilities", "Connected Enterprise AI capabilities"),
        ]
        positions = []
        for section_id, heading in required:
            block = section(self.source, section_id)
            self.assertIn(heading, text_content(block))
            positions.append(self.source.index(f'id="{section_id}"'))
        self.assertEqual(positions, sorted(positions))

    def test_failure_section_explains_six_operational_gaps_without_fear_mongering(self):
        block = text_content(section(self.source, "why-production-ai-fails"))
        expected = [
            "worked in testing",
            "edge cases",
            "release evidence",
            "human oversight",
            "monitoring",
            "ownership",
        ]
        for phrase in expected:
            self.assertIn(phrase, block.lower())
        self.assertIn("do not mean the system must be abandoned", block.lower())

    def test_workflow_contains_seven_ordered_release_stages(self):
        block = section(self.source, "how-it-works")
        stages = re.findall(r'data-workflow-step="(\d+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', block, flags=re.I | re.S)
        self.assertEqual([number for number, _ in stages], [str(i) for i in range(1, 8)])
        self.assertEqual(
            [text_content(label) for _, label in stages],
            ["Understand", "Review", "Assess", "Evaluate", "Generate evidence", "Release decision", "Production, if approved"],
        )
        self.assertIn("controlled pilot", text_content(block).lower())
        self.assertIn("remediation", text_content(block).lower())
        self.assertIn("hold", text_content(block).lower())
        self.assertIn("only when release conditions are met", text_content(block).lower())

    def test_outputs_are_explicitly_representative_not_prior_client_work(self):
        block = section(self.source, "what-youll-receive")
        outputs = re.findall(r'data-representative-output="([^"]+)"', block)
        self.assertEqual(
            outputs,
            [
                "AI Readiness Report",
                "Risk Register",
                "Evaluation Summary",
                "Governance Checklist",
                "Failure Mode Review",
                "Release Recommendation",
                "Human Oversight Map",
                "Executive Summary",
            ],
        )
        copy = text_content(block).lower()
        self.assertIn("representative outputs", copy)
        self.assertIn("not examples of previous client work", copy)
        self.assertIn("depends on scope", copy)
        self.assertNotIn("--bar:", block)
        self.assertNotRegex(block, r'\b\d+%\b')

    def test_audiences_cover_requested_systems_and_sensitive_contexts(self):
        block = text_content(section(self.source, "who-this-is-for")).lower()
        for phrase in [
            "organisations building ai products",
            "internal enterprise ai systems",
            "ai agents",
            "llm applications",
            "enterprise automation",
            "healthcare ai",
            "financial ai",
        ]:
            self.assertIn(phrase, block)

    def test_differentiation_is_specific_and_non_exaggerated(self):
        block = text_content(section(self.source, "why-aicloudstrategist")).lower()
        for phrase in [
            "evidence-based",
            "human oversight",
            "enterprise engineering",
            "vendor-neutral",
            "integrated enterprise ai",
            "governance before deployment",
            "operational readiness",
        ]:
            self.assertIn(phrase, block)

        lowered = self.text.lower()
        forbidden = [
            "world-leading",
            "industry-leading",
            "guaranteed outcomes",
            "trusted by thousands",
            "award-winning",
            "primary seo target",
            "money page",
            "get free growth review",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, lowered)
        self.assertIn("we assess where review", block)
        self.assertIn("we identify the approval", block)
        self.assertNotIn("we make review", block)
        self.assertNotIn("are established before production", block)

    def test_connected_capabilities_use_real_routes_and_allow_a_standalone_start(self):
        block = section(self.source, "connected-capabilities")
        expected = {
            "/services/ai-automation/": "Enterprise AI Systems & Agents",
            "/services/cloud-finops/": "AI FinOps & Cloud Economics",
            "/services/cloud-security/": "AI Security, Compliance & Sovereign Platforms",
            "/services/devops-observability/": "Managed AI Platforms & Operations",
        }
        links = {
            href: text_content(label)
            for href, label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.I | re.S)
        }
        for href, label in expected.items():
            self.assertEqual(links.get(href), label)
        copy = text_content(block).lower()
        self.assertIn("start with one capability", copy)
        self.assertIn("stand alone", copy)
        self.assertIn("when required", copy)

    def test_assets_and_accessibility_contracts(self):
        self.assertIn('<body class="paa-page aics-brand-system">', self.source)
        self.assertIn('<link rel="stylesheet" href="/css/production-ai-assurance.css?v=20260727-2">', self.source)
        self.assertIn('<link rel="stylesheet" href="/css/enterprise-brand-system.css?v=20260804-v1">', self.source)
        self.assertIn('<script src="/js/production-ai-assurance.js?v=20260727-1" defer></script>', self.source)
        self.assertTrue(STYLES.exists(), "Dedicated page stylesheet is missing")
        self.assertTrue(self.script, "Route-level accessibility script is missing")
        self.assertIn('AI AICloudStrategist home', self.script)
        self.assertIn('<link rel="icon" href="data:,">', self.source)
        self.assertIn('<nav class="paa-shell paa-breadcrumb" aria-label="Breadcrumb">', self.source)
        self.assertIn('<a href="/#what-we-do">Enterprise AI</a>', self.source)
        self.assertIn('<li aria-current="page">Production AI Assurance</li>', self.source)
        self.assertNotRegex(self.source, r'<img\b[^>]*src="https?://')
        self.assertNotRegex(self.source, r'<script\b(?![^>]*application/ld\+json)[^>]*src="https?://')
        self.assertIn('aria-label="Production readiness decision flow"', self.source)
        self.assertEqual(self.source.count('aria-labelledby='), 7)
        for title_id in (
            "failure-title",
            "method-title",
            "outputs-title",
            "audience-title",
            "why-aics-title",
            "connected-title",
            "final-title",
        ):
            self.assertIn(f'id="{title_id}"', self.source)
        for svg in re.findall(r"<svg\b[^>]*>", self.source, flags=re.I):
            self.assertIn('aria-hidden="true"', svg)
            self.assertIn('focusable="false"', svg)

    def test_page_css_is_scoped_responsive_and_motion_safe(self):
        self.assertTrue(self.styles, "Dedicated page stylesheet is empty")
        self.assertIn("@media (max-width: 760px)", self.styles)
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.styles)
        self.assertIn("animation-duration: .001ms", self.styles)
        self.assertIn("@keyframes paaDataFlow", self.styles)
        self.assertIn("@keyframes paaReveal", self.styles)
        self.assertIn(".paa-page .paa-evidence-map", self.styles)
        self.assertIn("grid-template-columns: minmax(270px, .57fr) minmax(0, 1.43fr);", self.styles)
        self.assertNotRegex(self.styles, r"\.paa-page \.paa-diagnostic-result\s*\{[^}]*display:\s*none")
        compact_pipeline_css = self.styles.split("@media (max-width: 1023px)", 1)[1].split("@media (max-width: 900px)", 1)[0]
        self.assertRegex(
            compact_pipeline_css,
            r"\.paa-page \.paa-workflow-step,\s*\.paa-page \.paa-workflow-step:last-child\s*\{[^}]*border:\s*0;[^}]*background:\s*transparent;",
        )
        self.assertRegex(
            compact_pipeline_css,
            r"\.paa-page \.paa-workflow-track\s*\{[^}]*display:\s*none;",
        )
        compact_css = self.styles.split("@media (max-width: 420px)", 1)[1].split("@media (max-width: 380px)", 1)[0]
        self.assertIn(".paa-page .paa-why-statement h2", compact_css)
        self.assertIn("font-size: clamp(1.68rem, calc(10vw - .32rem), 2.31rem)", compact_css)

        for selector_group in qualified_selectors(self.styles):
            for selector in selector_group.split(","):
                selector = selector.strip()
                self.assertTrue(
                    selector == ":root" or selector.startswith(".paa-page") or selector.startswith("body.paa-page"),
                    f"Unscoped page selector: {selector}",
                )


if __name__ == "__main__":
    unittest.main()

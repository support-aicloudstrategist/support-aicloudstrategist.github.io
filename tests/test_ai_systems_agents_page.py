import html
import json
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "ai-automation" / "index.html"
STYLES = ROOT / "css" / "ai-systems-agents.css"
SCRIPT = ROOT / "js" / "ai-systems-agents.js"
TRACKER = ROOT / "js" / "aics-conversion-tracking.js"
CONTACT = ROOT / "contact.html"


def text_content(source):
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()


def extract_section(source, section_id):
    marker = re.search(rf'<section\b[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>', source, re.I)
    if marker is None:
        raise AssertionError(f"Missing section #{section_id}")
    next_section = re.search(r"<section\b", source[marker.end():], re.I)
    end = marker.end() + next_section.start() if next_section else source.find("</main>", marker.end())
    return source[marker.start():end]


def json_ld_graph(source):
    blocks = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>\s*(.*?)\s*</script>',
        source,
        re.I | re.S,
    )
    graph = []
    for block in blocks:
        data = json.loads(block)
        graph.extend(data.get("@graph", [data]))
    return graph


def css_selectors(styles):
    def visit(rules):
        for rule in rules:
            if rule.type == "qualified-rule":
                yield tinycss2.serialize(rule.prelude).strip()
            elif rule.type == "at-rule" and rule.content is not None and rule.lower_at_keyword in {
                "media", "supports", "layer", "container"
            }:
                nested = tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True)
                yield from visit(nested)

    rules = tinycss2.parse_stylesheet(styles, skip_comments=True, skip_whitespace=True)
    yield from visit(rules)


class AiSystemsAgentsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.text = text_content(cls.source)
        cls.styles = STYLES.read_text(encoding="utf-8") if STYLES.exists() else ""
        cls.script = SCRIPT.read_text(encoding="utf-8") if SCRIPT.exists() else ""
        cls.tracker = TRACKER.read_text(encoding="utf-8")
        cls.contact = CONTACT.read_text(encoding="utf-8")

    def test_metadata_preserves_route_and_search_intent(self):
        self.assertIn(
            "<title>Enterprise AI Automation &amp; AI Agents | AICloudStrategist</title>",
            self.source,
        )
        self.assertIn(
            '<link rel="canonical" href="https://aicloudstrategist.com/services/ai-automation/">',
            self.source,
        )
        self.assertRegex(
            self.source,
            r'<meta name="description" content="[^"]*AI automation[^"]*AI agents[^"]*human accountability[^"]*">',
        )
        self.assertIn('name="robots" content="index, follow, max-image-preview:large"', self.source)
        self.assertEqual(self.source.count('<meta name="description"'), 1)

    def test_one_executive_h1_and_consistent_hero_actions(self):
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", self.source, re.I | re.S)
        self.assertEqual(len(h1s), 1)
        self.assertEqual(text_content(h1s[0]), "Turn business-critical workflows into controlled AI systems.")

        hero = re.search(r'<header\b[^>]*class="[^"]*asa-hero[^"]*"[^>]*>(.*?)</header>', self.source, re.I | re.S)
        if hero is None:
            self.fail("Missing Enterprise AI Systems & Agents hero")
        actions = re.findall(r'<a\b[^>]*class="[^"]*asa-button[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', hero.group(1), re.I | re.S)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0][0], "/contact.html?service=ai-systems-agents")
        self.assertEqual(text_content(actions[0][1]).replace("↗", "").strip(), "Discuss your AI system")
        self.assertEqual(actions[1][0], "#how-it-works")
        self.assertEqual(text_content(actions[1][1]).replace("↓", "").strip(), "See how the system works")

    def test_ten_chapters_form_one_ordered_customer_journey(self):
        expected = [
            "problem",
            "diagnosis",
            "solution",
            "how-it-works",
            "governance",
            "delivery",
            "evidence",
            "engagement",
            "final-cta",
        ]
        positions = []
        for section_id in expected:
            marker = f'id="{section_id}"'
            self.assertEqual(self.source.count(marker), 1, f"Expected one #{section_id}")
            positions.append(self.source.index(marker))
        self.assertEqual(positions, sorted(positions))
        main = re.search(r"<main\b[^>]*>(.*?)</main>", self.source, re.I | re.S)
        if main is None:
            self.fail("Missing main landmark")
        self.assertEqual(len(re.findall(r"<main\b[^>]*>.*?</main>", self.source, re.I | re.S)), 1)
        self.assertEqual(len(re.findall(r"<section\b", main.group(1))), 9)

    def test_problem_and_diagnosis_prioritize_control_over_tool_sales(self):
        problem = text_content(extract_section(self.source, "problem")).lower()
        for phrase in [
            "disconnected systems",
            "manual interpretation",
            "exceptions",
            "ownership",
            "response delay",
        ]:
            self.assertIn(phrase, problem)

        diagnosis = text_content(extract_section(self.source, "diagnosis")).lower()
        for phrase in ["value", "feasibility", "control", "automate", "assist", "redesign first", "keep human-led"]:
            self.assertIn(phrase, diagnosis)
        self.assertIn("not every workflow should be automated", diagnosis)
        self.assertIn("sensitive", diagnosis)

    def test_solution_and_operating_circuit_explain_the_complete_system(self):
        solution = text_content(extract_section(self.source, "solution")).lower()
        for phrase in [
            "connect",
            "decide",
            "act and observe",
            "identity",
            "data boundaries",
            "permissions",
            "escalation",
            "audit trail",
        ]:
            self.assertIn(phrase, solution)

        circuit = extract_section(self.source, "how-it-works")
        steps = re.findall(r'data-circuit-step="(\d+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', circuit, re.I | re.S)
        self.assertEqual([number for number, _ in steps], [str(i) for i in range(1, 7)])
        self.assertIn("human", text_content(circuit).lower())
        self.assertIn("fallback", text_content(circuit).lower())

    def test_governance_is_specific_without_unsupported_compliance_claims(self):
        block = text_content(extract_section(self.source, "governance")).lower()
        for phrase in [
            "identity and permissions",
            "data boundaries",
            "human approval",
            "testing and failure handling",
            "logging and monitoring",
            "change and release control",
        ]:
            self.assertIn(phrase, block)
        for forbidden in ["certified compliant", "guaranteed compliance", "zero risk", "fully autonomous"]:
            self.assertNotIn(forbidden, self.text.lower())

    def test_delivery_is_evidence_gated_and_scope_honest(self):
        block = extract_section(self.source, "delivery")
        stages = re.findall(r'data-delivery-step="(\d+)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', block, re.I | re.S)
        self.assertEqual([text_content(label) for _, label in stages], ["Diagnose", "Architect", "Deliver", "Operate"])
        copy = text_content(block).lower()
        self.assertIn("acceptance", copy)
        self.assertIn("scope", copy)
        self.assertIn("client", copy)
        self.assertNotIn("days 0–7", copy)
        self.assertNotIn("weeks 3–4", copy)

    def test_evidence_is_tangible_and_truthfully_labelled(self):
        block = extract_section(self.source, "evidence")
        outputs = re.findall(r'data-representative-output="([^"]+)"', block)
        self.assertEqual(
            outputs,
            [
                "Workflow and system map",
                "Decision and escalation matrix",
                "Integration and data-boundary design",
                "Test scenarios and acceptance evidence",
                "Operational dashboard definition",
                "Runbook, ownership and change controls",
                "Pilot or release recommendation",
            ],
        )
        copy = text_content(block).lower()
        self.assertIn("representative delivery artifacts", copy)
        self.assertIn("not presented as prior client work", copy)
        self.assertIn("depend on scope", copy)
        self.assertNotRegex(block, r"\b\d+%\b")

    def test_engagement_qualifies_by_stakes_and_answers_real_objections(self):
        block = extract_section(self.source, "engagement")
        copy = text_content(block).lower()
        self.assertIn("focused workflow pilot", copy)
        self.assertIn("business-critical system initiative", copy)
        self.assertIn("multiple systems or teams", copy)
        self.assertNotIn("small business plan", copy)
        self.assertNotIn("enterprise plan", copy)
        self.assertEqual(len(re.findall(r"<details\b", block, re.I)), 4)
        connected_routes = {
            "/services/ai-mlops/": ROOT / "services" / "ai-mlops" / "index.html",
            "/services/cloud-security/": ROOT / "services" / "cloud-security" / "index.html",
            "/services/cloud-finops/": ROOT / "services" / "cloud-finops" / "index.html",
            "/services/devops-observability/": ROOT / "services" / "devops-observability" / "index.html",
        }
        for href, target in connected_routes.items():
            self.assertIn(f'href="{href}"', block)
            self.assertTrue(target.exists(), f"Connected capability has no local page: {href}")

    def test_visible_faq_and_schema_are_exactly_aligned(self):
        engagement = extract_section(self.source, "engagement")
        visible = []
        for detail in re.findall(r"<details\b[^>]*>(.*?)</details>", engagement, re.I | re.S):
            question = re.search(r"<summary\b[^>]*>(.*?)</summary>", detail, re.I | re.S)
            answer = re.search(r"<div\b[^>]*class=" + '"[^"]*asa-faq-answer[^"]*"' + r"[^>]*>(.*?)</div>", detail, re.I | re.S)
            if question is None or answer is None:
                self.fail("Each FAQ disclosure needs a summary and .asa-faq-answer")
            visible.append((text_content(question.group(1)), text_content(answer.group(1))))

        graph = json_ld_graph(self.source)
        faq = next(item for item in graph if item.get("@type") == "FAQPage")
        schema = [(item["name"], item["acceptedAnswer"]["text"]) for item in faq["mainEntity"]]
        self.assertEqual(schema, visible)

    def test_conversion_path_is_direct_consistent_and_trackable(self):
        cta_href = "/contact.html?service=ai-systems-agents"
        self.assertGreaterEqual(self.source.count(f'href="{cta_href}"'), 4)
        self.assertNotIn("/free-business-review/", self.source)
        self.assertNotIn("Map your AI automation opportunities", self.source)
        self.assertEqual(self.source.count('/js/aics-conversion-tracking.js'), 1)
        self.assertIn("a.hasAttribute('data-aics-cta')", self.tracker)
        self.assertIn("cta:a.getAttribute('data-aics-cta')||''", self.tracker)
        self.assertIn('value="ai-systems-agents"', self.contact)
        self.assertIn("Enterprise AI Systems &amp; Agents", self.contact)
        self.assertIn("requestedService", self.contact)

    def test_original_visuals_have_accessible_semantic_equivalents(self):
        figures = re.findall(r'<figure\b[^>]*data-asa-diagram="([^"]+)"[^>]*>(.*?)</figure>', self.source, re.I | re.S)
        self.assertEqual(
            [name for name, _ in figures],
            ["workflow-control-map", "diagnostic-lens", "operating-bands", "operating-circuit", "control-plane"],
        )
        for name, figure in figures:
            self.assertIn("<svg", figure, name)
            for svg in re.findall(r"<svg\b[^>]*>", figure, re.I):
                self.assertIn('aria-hidden="true"', svg)
                self.assertIn('focusable="false"', svg)
            self.assertRegex(figure, r"<(figcaption|ol|ul)\b", name)
        self.assertNotRegex(self.source, r'<img\b[^>]*src="https?://')

    def test_page_assets_are_dedicated_scoped_and_resilient(self):
        self.assertIn('<body class="asa-page">', self.source)
        self.assertEqual(self.source.count('/css/ai-systems-agents.css'), 1)
        self.assertLessEqual(self.source.count('/js/ai-systems-agents.js'), 1)
        self.assertTrue(STYLES.exists(), "Missing route stylesheet")
        self.assertTrue(self.styles, "Route stylesheet is empty")
        self.assertIn("@media (max-width: 760px)", self.styles)
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.styles)
        self.assertNotIn("overflow-x: hidden", self.styles)
        self.assertNotIn("overflow-x:hidden", self.styles)
        for group in css_selectors(self.styles):
            for selector in group.split(","):
                selector = selector.strip()
                self.assertTrue(
                    selector == ":root" or selector.startswith(".asa-page") or selector.startswith("body.asa-page"),
                    f"Unscoped page selector: {selector}",
                )

    def test_landmarks_breadcrumb_headings_and_static_shell_are_preserved(self):
        self.assertEqual(self.source.count("data-aics-navigation-mount"), 1)
        self.assertEqual(self.source.count("data-aics-global-footer"), 1)
        self.assertIn('<nav class="asa-shell asa-breadcrumb" aria-label="Breadcrumb">', self.source)
        self.assertIn('aria-current="page">Enterprise AI Systems &amp; Agents</li>', self.source)
        for title_id in [
            "problem-title",
            "diagnosis-title",
            "solution-title",
            "circuit-title",
            "governance-title",
            "delivery-title",
            "evidence-title",
            "engagement-title",
            "final-title",
        ]:
            self.assertIn(f'id="{title_id}"', self.source)
            self.assertIn(f'aria-labelledby="{title_id}"', self.source)

    def test_legacy_catalogue_and_template_patterns_are_removed(self):
        for phrase in [
            "The AICloudStrategist Automation Leakage Map",
            "Buyer scenarios: what to automate first",
            "Industry examples",
            "Integrations we commonly design around",
            "Pricing drivers",
            "Related AI automation paths",
            "grid2",
            'class="grid"',
            'class="card"',
            '<table',
        ]:
            self.assertNotIn(phrase, self.source)


if __name__ == "__main__":
    unittest.main()

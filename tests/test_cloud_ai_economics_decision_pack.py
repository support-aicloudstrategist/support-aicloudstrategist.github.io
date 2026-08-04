import html
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "resources" / "cloud-ai-economics-decision-pack" / "index.html"
PACK_CSS = ROOT / "css" / "cloud-ai-economics-decision-pack.css"
PACK_PDF = ROOT / "downloads" / "cloud-ai-economics-decision-pack.pdf"
PACK_BUILDER = ROOT / "scripts" / "build_cloud_ai_economics_decision_pack.py"
SERVICE = ROOT / "services" / "cloud-finops" / "index.html"
CONTACT = ROOT / "contact.html"


def text_content(source):
    without_scripts = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    without_tags = re.sub(r"<[^>]+>", " ", without_scripts)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


class CloudAiEconomicsDecisionPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = PACK.read_text(encoding="utf-8") if PACK.exists() else ""
        cls.pack_text = text_content(cls.pack)
        cls.service = SERVICE.read_text(encoding="utf-8")
        cls.contact = CONTACT.read_text(encoding="utf-8")

    def test_pack_is_ungated_browser_inspectable_and_truthfully_labelled(self):
        self.assertTrue(PACK.exists(), "Decision Pack page must exist")
        self.assertIn("Cloud & AI Economics Decision Pack", self.pack_text)
        self.assertIn("Representative evidence · synthetic scenario", self.pack_text)
        for boundary in [
            "not client work",
            "not a case study",
            "not a benchmark",
            "not a savings promise",
            "No billing files, credentials or work email are required",
        ]:
            self.assertIn(boundary, self.pack_text)
        self.assertNotRegex(self.pack, r'<form\b|type=["\']email["\']')
        self.assertNotRegex(self.pack_text.lower(), r"trusted by|customer logo|testimonial|award-winning")

    def test_pack_contains_the_ten_required_decision_outputs(self):
        outputs = re.findall(r'data-decision-output="([^"]+)"', self.pack)
        self.assertEqual(
            outputs,
            [
                "Economic Baseline and Confidence Statement",
                "Allocation and Ownership Map",
                "Cloud and AI Unit Economics Tree",
                "Quality Reliability and Risk Constraint Record",
                "Portfolio Decision Register",
                "Forecast and Scenario Comparison",
                "Commitment Readiness Record",
                "90-Day Action Portfolio",
                "Value Realisation Entry",
                "Executive Decision Summary",
            ],
        )

    def test_pack_exposes_sources_assumptions_confidence_and_unresolved_evidence(self):
        for phrase in [
            "Source register",
            "Assumptions and exclusions",
            "Confidence: moderate",
            "Unresolved evidence",
            "Client approval required",
            "AWS Cost and Usage Report",
            "Azure Cost Management export",
            "Google Cloud billing export",
            "Kubernetes allocation export",
            "AI provider usage export",
        ]:
            self.assertIn(phrase, self.pack_text)

    def test_pack_separates_value_classes_and_uses_the_full_proof_chain(self):
        for value_class in [
            "Cashable reduction",
            "Cost avoidance",
            "Negotiated rate improvement",
            "Capacity released",
            "Reliability or risk improvement",
            "Revenue or throughput effect",
            "Unit-margin improvement",
        ]:
            self.assertIn(value_class, self.pack_text)
        for stage in [
            "Observed",
            "Qualified",
            "Approved",
            "Implemented",
            "Measured",
            "Finance-accepted",
            "Sustained",
        ]:
            self.assertIn(stage, self.pack_text)

    def test_synthetic_scenario_contains_consistent_decision_values_and_ranges(self):
        for phrase in [
            "USD 2.47m monthly",
            "USD 29.64m annualised",
            "72% allocation coverage",
            "USD 0.083 per successful AI task",
            "8.0m attempted tasks",
            "7.2m successful tasks",
            "Growth counterfactual: USD 2.91m monthly",
            "Qualified decision range: USD 2.74m–2.82m monthly",
            "Expected-value range: USD 0.09m–0.17m monthly cost avoidance",
        ]:
            self.assertIn(phrase, self.pack_text)

    def test_action_portfolio_contains_owner_dependency_and_decision_date(self):
        actions = re.findall(r'<article\b[^>]*data-action-record="[^"]+"[^>]*>(.*?)</article>', self.pack, re.I | re.S)
        self.assertGreaterEqual(len(actions), 5)
        for action in actions:
            copy = text_content(action)
            self.assertIn("Owner:", copy)
            self.assertIn("Dependency:", copy)
            self.assertIn("Decision date:", copy)

    def test_value_entry_is_a_concrete_synthetic_record_not_a_claim(self):
        for phrase in [
            "Baseline: USD 86k monthly",
            "Counterfactual: USD 84k–90k monthly",
            "Expected-value range: USD 62k–74k monthly cashable reduction",
            "Evidence state: qualified—not implemented",
            "Finance acceptance: pending",
            "Persistence window: 90 days after implementation",
            "Synthetic planning record—not realised value",
        ]:
            self.assertIn(phrase, self.pack_text)

    def test_pack_has_a_downloadable_searchable_pdf_and_maintainable_builder(self):
        self.assertIn('href="/downloads/cloud-ai-economics-decision-pack.pdf"', self.pack)
        self.assertIn('download="Cloud-and-AI-Economics-Decision-Pack.pdf"', self.pack)
        self.assertTrue(PACK_PDF.exists(), "Decision Pack PDF must exist")
        self.assertGreater(PACK_PDF.stat().st_size, 80_000)
        pdf_bytes = PACK_PDF.read_bytes()
        self.assertIn(b"/Annots", pdf_bytes)
        self.assertIn(b"/URI", pdf_bytes)
        self.assertTrue(PACK_BUILDER.exists(), "Decision Pack PDF builder must exist")

    def test_pack_uses_a_scoped_static_accessible_visual_system(self):
        self.assertIn('<body class="economics-pack-page aics-brand-system">', self.pack)
        self.assertIn('class="pack-skip-link" href="#main-content"', self.pack)
        self.assertIn('href="/css/cloud-ai-economics-decision-pack.css?v=20260803-1"', self.pack)
        self.assertIn('href="/css/enterprise-brand-system.css?v=20260804-v1"', self.pack)
        self.assertTrue(PACK_CSS.exists())
        css = PACK_CSS.read_text(encoding="utf-8") if PACK_CSS.exists() else ""
        self.assertIn(".economics-pack-page", css)
        self.assertIn(":focus-visible", css)
        self.assertIn("@media print", css)
        self.assertNotIn("@keyframes", css)
        self.assertNotIn("animation:", css)
        self.assertNotRegex(css, r"url\(")
        self.assertEqual(len(re.findall(r"<h1\b", self.pack, flags=re.I)), 1)
        tables = re.findall(r"<table\b([^>]*)>", self.pack, flags=re.I)
        self.assertEqual(len(tables), 2)
        for attrs in tables:
            self.assertIn('tabindex="0"', attrs)
            self.assertRegex(attrs, r'aria-label="[^"]+"')
        self.assertEqual(self.pack.count("data-aics-global-footer"), 1)
        self.assertIn("data-aics-navigation-mount", self.pack)

    def test_service_page_routes_medium_intent_buyers_to_the_pack(self):
        href = "/resources/cloud-ai-economics-decision-pack/"
        self.assertGreaterEqual(self.service.count(f'href="{href}"'), 3)
        self.assertIn("Inspect the Cloud &amp; AI Economics Decision Pack", self.service)
        self.assertIn('data-aics-cta="decision-pack"', self.service)
        self.assertIn('data-aics-cta="economics-review"', self.service)

    def test_contact_route_exposes_service_specific_economic_qualification(self):
        self.assertIn(
            '<option value="ai-finops-cloud-economics">Enterprise FinOps Advisory — Cloud &amp; AI Economics</option>',
            self.contact,
        )
        fieldset = re.search(
            r'<fieldset\b[^>]*id="finopsQualification"[^>]*>(.*?)</fieldset>',
            self.contact,
            flags=re.I | re.S,
        )
        if fieldset is None:
            self.fail("Missing service-specific Enterprise FinOps qualification fieldset")
        block = fieldset.group(1)
        for name in [
            "economics_trigger",
            "platforms_in_scope",
            "ai_workloads_material",
            "decision_timeline",
            "finops_capability",
            "spend_band",
            "access_constraints",
        ]:
            self.assertRegex(block, rf'name="{name}"')
        self.assertIn("No billing files or credentials", text_content(block))
        self.assertIn("function syncFinOpsQualification", self.contact)
        self.assertIn("requestedService", self.contact)
        for field in ["economics_trigger", "platforms_in_scope", "ai_workloads_material", "decision_timeline"]:
            self.assertIn(f"payload.{field}", self.contact)
        self.assertRegex(block, r'name="platforms_in_scope"[^>]*maxlength="400"')
        self.assertRegex(block, r'name="decision_timeline"[^>]*maxlength="240"')
        self.assertRegex(block, r'name="access_constraints"[^>]*maxlength="800"')


if __name__ == "__main__":
    unittest.main()

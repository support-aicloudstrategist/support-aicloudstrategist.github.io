from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "service": (ROOT / "cloud-ai-cost-governance-diagnostic" / "index.html", "https://aicloudstrategist.com/cloud-ai-cost-governance-diagnostic/"),
    "decision_pack": (ROOT / "resources" / "cloud-ai-economics-decision-pack" / "index.html", "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/"),
    "resources": (ROOT / "resources" / "index.html", "https://aicloudstrategist.com/resources/"),
    "about": (ROOT / "about" / "index.html", "https://aicloudstrategist.com/about/"),
}


class CoreOneServicePagesTests(unittest.TestCase):
    def setUp(self):
        self.sources = {name: path.read_text(encoding="utf-8") for name, (path, _) in PAGES.items()}

    def test_all_core_pages_exist_with_canonical_and_single_h1(self):
        for name, (path, canonical) in PAGES.items():
            with self.subTest(page=name):
                self.assertTrue(path.exists())
                source = self.sources[name]
                self.assertEqual(source.count(f'<link rel="canonical" href="{canonical}">'), 1)
                self.assertEqual(len(re.findall(r"<h1[^>]*>.*?</h1>", source, re.I | re.S)), 1)

    def test_all_core_pages_use_shared_shell_and_one_conversion_path(self):
        for name, source in self.sources.items():
            with self.subTest(page=name):
                self.assertIn('/css/cost-governance.css?v=20261110', source)
                self.assertIn('/js/cost-governance.js?v=20261110', source)
                self.assertIn('href="/request-fit-review/"', source)
                self.assertIn('Request a Cloud &amp; AI Cost Fit Review', source)

    def test_public_core_pages_are_company_first(self):
        forbidden = ("rajeev", "rajiv", "anushka", "ai-assisted", '"@type":"person"', '"@type": "person"', "our large team")
        for name, source in self.sources.items():
            lower = source.lower()
            for term in forbidden:
                with self.subTest(page=name, term=term):
                    self.assertNotIn(term, lower)

    def test_service_page_defines_scope_process_outputs_and_exclusions(self):
        source = self.sources["service"].lower()
        required = (
            "cloud &amp; ai cost governance diagnostic",
            "cost and ownership baseline",
            "allocation and ownership map",
            "governance gap register",
            "prioritized decision register",
            "30-day customer action plan",
            "no guaranteed savings",
            "no production changes",
            "kubernetes",
            "gpu",
            "inference",
        )
        for phrase in required:
            self.assertIn(phrase, source)

    def test_decision_pack_is_unambiguously_representative(self):
        source = self.sources["decision_pack"].lower()
        required = (
            "representative synthetic scenario",
            "not customer work",
            "not a benchmark",
            "not an achieved result",
            "not a savings promise",
            "30-day action plan",
            "observed",
            "qualified",
            "owner gap",
        )
        for phrase in required:
            self.assertIn(phrase, source)
        self.assertNotIn("90-day action", source)

    def test_resources_hub_is_focused_on_cost_governance(self):
        source = self.sources["resources"].lower()
        for phrase in ("cloud-spend visibility", "cost allocation", "kubernetes", "gpu", "inference", "decision pack"):
            self.assertIn(phrase, source)
        for forbidden in ("production ai readiness diagnostic", "business growth systems", "ai creative studio"):
            self.assertNotIn(forbidden, source)

    def test_about_page_preserves_verified_legal_identity_without_biographies(self):
        source = self.sources["about"]
        self.assertIn("AICLOUDSTRATEGIST PRIVATE LIMITED", source)
        self.assertIn("U62020DC2026PTC470945", source)
        self.assertIn("contact@aicloudstrategist.com", source)
        self.assertNotIn("review owner", source.lower())
        self.assertNotIn("founder", source.lower())
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.I | re.S)
        for block in blocks:
            data = json.loads(block)
            self.assertNotIn("Person", json.dumps(data))


if __name__ == "__main__":
    unittest.main()

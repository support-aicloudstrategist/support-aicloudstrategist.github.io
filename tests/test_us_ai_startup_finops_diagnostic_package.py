import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "us-ai-startup-llm-gpu-finops-diagnostic-package" / "index.html"
URL = "https://aicloudstrategist.com/resources/us-ai-startup-llm-gpu-finops-diagnostic-package/"
COMPARISON = ROOT / "resources" / "us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison" / "index.html"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USAIStartupFinOpsDiagnosticPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.comparison = COMPARISON.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("LLM, GPU and cloud spend owner diagnostic", self.html)

    def test_revenue_package_has_deliverables_and_safe_boundaries(self):
        for phrase in [
            "Spend-source inventory",
            "Owner and product allocation map",
            "AI/cloud evidence boundary checklist",
            "CFO/CTO decision queue",
            "One-page review dashboard spec",
        ]:
            self.assertIn(phrase, self.html)
        for boundary in [
            "not a real US AI startup client case study",
            "not a testimonial",
            "not a cloud savings result",
            "not runway-extension evidence",
            "not security, privacy, legal, tax, accounting or compliance advice",
            "guaranteed savings",
        ]:
            self.assertIn(boundary, self.html)
        for forbidden in ["trusted by", "certified partner", "guaranteed 30%"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_service_and_webpage_are_valid(self):
        docs = json_ld_documents(self.html)
        graph = docs[0]["@graph"]
        types = {node.get("@type") for node in graph}
        self.assertIn("Service", types)
        self.assertIn("WebPage", types)
        service = next(node for node in graph if node.get("@type") == "Service")
        self.assertEqual(service["@id"], f"{URL}#service")
        self.assertEqual(service["areaServed"], "US")

    def test_discovery_and_conversion_surfaces_link_to_package(self):
        path = "/resources/us-ai-startup-llm-gpu-finops-diagnostic-package/"
        self.assertIn(path, self.resources)
        self.assertIn(f"US AI startup LLM/GPU FinOps diagnostic package: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(path, self.comparison)
        self.assertNotIn("/case-studies/simulated-us-ai-startup-llm-gpu-finops-diagnostic/", self.comparison)


if __name__ == "__main__":
    unittest.main()

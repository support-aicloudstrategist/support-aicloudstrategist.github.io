import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison" / "index.html"
URL = "https://aicloudstrategist.com/resources/us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USAIStartupFinOpsComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_and_canonical(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertIn('<meta property="og:site_name" content="AICloudStrategist"/>', self.html)
        self.assertIn('<meta name="twitter:card" content="summary_large_image"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)

    def test_competitor_and_buyer_language_without_forbidden_claims(self):
        for phrase in ["CloudZero", "Vantage", "IBM Cloudability", "Anodot", "AWS", "Azure", "Google Cloud", "LLM", "GPU", "Kubernetes"]:
            self.assertIn(phrase, self.html)
        boundaries = self.html[self.html.index("Claim boundaries") :]
        for required in ["not a US AI startup client case study", "not a testimonial", "not a savings result", "not runway-extension evidence", "not security/privacy/legal/tax/accounting/compliance advice"]:
            self.assertIn(required, boundaries)
        for forbidden in ["trusted by", "guaranteed savings", "certified partner", "#1"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_is_valid_article_and_faq(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertIn("LLM cost tracking", article["about"])
        self.assertIn("GPU utilization", article["about"])

    def test_discovery_surfaces_link_to_asset(self):
        self.assertIn('/resources/us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison/', self.resources)
        self.assertIn('US AI startup LLM/GPU FinOps vs cloud cost tools comparison: https://aicloudstrategist.com/resources/us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison/', self.llms)
        self.assertIn(URL, self.sitemap)


if __name__ == "__main__":
    unittest.main()

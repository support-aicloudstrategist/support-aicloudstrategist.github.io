import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "europe-saas-ai-governance-vs-grc-tools-comparison" / "index.html"
URL = "https://aicloudstrategist.com/resources/europe-saas-ai-governance-vs-grc-tools-comparison/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeSaasAiGovernanceComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    def test_page_is_indexable_and_canonical(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertIn('<meta property="og:site_name" content="AICloudStrategist"/>', self.html)
        self.assertIn('<meta name="twitter:card" content="summary_large_image"/>', self.html)

    def test_positioning_names_competitors_without_superiority_claims(self):
        for phrase in ["Vanta", "Drata", "OneTrust", "Secureframe", "Sprinto", "Hyperproof", "CloudZero"]:
            self.assertIn(phrase, self.html)
        boundaries = self.html[self.html.index("Claim boundaries") :]
        for forbidden in ["real European SaaS client", "EU AI Act compliance", "GDPR compliance", "certification", "superiority"]:
            self.assertIn(forbidden, boundaries)
        self.assertNotIn("guaranteed savings", self.html.lower())
        self.assertNotIn("trusted by", self.html.lower())

    def test_json_ld_is_valid_article_and_faq(self):
        docs = json_ld_documents(self.html)
        graph = []
        for doc in docs:
            graph.extend(doc.get("@graph", [doc]) if isinstance(doc, dict) else [])
        types = {node.get("@type") for node in graph if isinstance(node, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(node for node in graph if isinstance(node, dict) and node.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertIn("GRC tools", article["about"])

    def test_discovery_surfaces_link_to_asset(self):
        self.assertIn('/resources/europe-saas-ai-governance-vs-grc-tools-comparison/', self.resources)
        self.assertIn('Europe SaaS AI governance vs GRC tools comparison: https://aicloudstrategist.com/resources/europe-saas-ai-governance-vs-grc-tools-comparison/', self.llms)


if __name__ == "__main__":
    unittest.main()

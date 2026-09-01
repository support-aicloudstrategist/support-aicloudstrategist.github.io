import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ai-automation-agency-canada" / "index.html"
GLOBAL_PAGE = ROOT / "ai-automation-agency" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
URL = "https://aicloudstrategist.com/ai-automation-agency-canada/"


class CanadaAiAutomationAgencyPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.global_html = GLOBAL_PAGE.read_text(encoding="utf-8")
        cls.llms = LLMS.read_text(encoding="utf-8")
        root = ET.parse(SITEMAP).getroot()
        cls.paths = [urlparse(node.text).path for node in root.findall(".//s:loc", NS)]

    def test_page_is_indexable_canonical_and_market_specific(self):
        self.assertIn('<html lang="en-CA">', self.html)
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertIn("AI Automation Agency Canada", self.html)
        self.assertIn("PIPEDA/PHIPA-aware", self.html)
        self.assertIn("missed-call callbacks", self.html)
        self.assertIn("owner dashboards", self.html)

    def test_json_ld_is_valid_and_contains_safe_offer(self):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S)
        self.assertGreaterEqual(len(blocks), 3)
        parsed = [json.loads(block) for block in blocks]
        graph = parsed[0]["@graph"]
        service = graph[0]
        faq = graph[1]
        self.assertEqual(service["@type"], "Service")
        self.assertEqual(service["@id"], f"{URL}#service")
        self.assertIn("Canada", service["areaServed"])
        self.assertEqual(service["offers"]["url"], "https://aicloudstrategist.com/free-business-review/")
        self.assertEqual(faq["@type"], "FAQPage")

    def test_proof_boundary_avoids_unsupported_claims(self):
        required_boundaries = [
            "not a customer case study",
            "does not claim Canadian client results",
            "does not guarantee leads",
            "PIPEDA compliance",
            "PHIPA compliance",
            "medical outcomes",
            "AI accuracy",
        ]
        for text in required_boundaries:
            with self.subTest(text=text):
                self.assertIn(text, self.html)

    def test_discovery_links_exist(self):
        self.assertIn('/ai-automation-agency-canada/', self.global_html)
        self.assertIn(URL, self.llms)
        self.assertIn('/ai-automation-agency-canada/', self.paths)


if __name__ == "__main__":
    unittest.main()

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "us-specialty-clinic-prior-auth-evidence-pack" / "index.html"
URL = "https://aicloudstrategist.com/resources/us-specialty-clinic-prior-auth-evidence-pack/"
PATH = "/resources/us-specialty-clinic-prior-auth-evidence-pack/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USSpecialtyClinicPriorAuthEvidencePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.related = (ROOT / "resources" / "us-specialty-clinic-referral-prior-auth-leakage-checklist" / "index.html").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("US specialty clinic prior authorization evidence pack", self.html)
        self.assertIn("North America / US Eastern business morning", self.html)

    def test_buyer_language_competitors_and_top5_gaps_are_present(self):
        for phrase in [
            "prior authorization automation",
            "patient access",
            "referral leakage",
            "eligibility verification",
            "payer follow-up",
            "Notable",
            "Luma Health",
            "Phreesia",
            "Artera",
            "Infinitus / Rivet / Kyruus Health / Experian-style RCM tools",
            "Downloadable sample CSV",
            "Owner dashboard mockup",
        ]:
            self.assertIn(phrase, self.html)

    def test_safe_boundaries_are_explicit(self):
        for boundary in [
            "not a real US specialty clinic case study",
            "not a testimonial",
            "not a prior-authorization submission service",
            "not payer-contracting advice",
            "not medical advice",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not proof of HIPAA compliance",
            "authorization-speed improvement",
            "denial reduction",
            "revenue, ROI, ranking",
            "No outreach was sent",
        ]:
            self.assertIn(boundary, self.html)
        for forbidden in ["trusted by", "guaranteed", "certified partner", "reduced denials by"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_service_and_faq_are_valid(self):
        docs = json_ld_documents(self.html)
        graph = docs[0]["@graph"]
        types = {node.get("@type") for node in graph}
        self.assertIn("WebPage", types)
        self.assertIn("Service", types)
        service = next(node for node in graph if node.get("@type") == "Service")
        self.assertEqual(service["areaServed"], "US")
        self.assertEqual(service["serviceType"], "Healthcare GrowthOS evidence diagnostic")
        self.assertEqual(docs[1]["@type"], "FAQPage")

    def test_discovery_surfaces_link_to_pack(self):
        self.assertIn(PATH, self.resources)
        self.assertIn(f"US specialty clinic prior authorization evidence pack: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(PATH, self.related)


if __name__ == "__main__":
    unittest.main()

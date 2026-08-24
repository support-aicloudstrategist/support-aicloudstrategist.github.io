import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-healthcare-growthos-vendor-shortlist-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USMedicalGroupGrowthOSShortlistAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("US medical group Healthcare GrowthOS vendor shortlist checklist", self.html)
        self.assertIn("North America · US Eastern business morning", self.html)

    def test_buyer_language_competitors_and_top5_gaps_are_present(self):
        for phrase in [
            "patient engagement platform",
            "patient access",
            "AI receptionist for medical practice",
            "front desk automation",
            "referral leakage",
            "prior authorization status",
            "What AICS must publish/build to enter top-3/top-5 consideration",
            "Phreesia",
            "Luma Health",
            "Relatient",
            "NexHealth",
            "Artera",
            "ModMed/Klara",
            "Availity, Waystar, Experian Health and Infinx",
            "No-PHI source-to-status sample",
            "Owner dashboard mockup",
            "AI-boundary FAQ",
        ]:
            self.assertIn(phrase, self.html)

    def test_safe_boundaries_are_explicit(self):
        for boundary in [
            "not a real US medical group case study",
            "not a testimonial",
            "not a certification",
            "not a platform partnership",
            "not medical advice",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not proof of HIPAA compliance",
            "not a claims/prior-authorization submission service",
            "not an EHR",
            "not a practice-management system",
            "patient growth, no-show reduction, authorization-speed improvement, denial reduction, revenue, ROI, ranking or AI accuracy",
            "No outreach was sent",
            "demo/internal/simulated",
        ]:
            self.assertIn(boundary, self.html)
        for forbidden in ["trusted by", "guaranteed", "certified partner", "reduced denials by", "hipaa compliant"]:
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

    def test_discovery_surfaces_link_to_asset(self):
        self.assertIn(PATH, self.resources)
        self.assertIn(f"US medical group Healthcare GrowthOS vendor shortlist checklist: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)


if __name__ == "__main__":
    unittest.main()

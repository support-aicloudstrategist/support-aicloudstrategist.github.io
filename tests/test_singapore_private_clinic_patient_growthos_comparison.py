import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-private-clinic-patient-growthos-vs-clinic-software-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "singapore-patient-growthos-comparison-matrix.csv"
SVG = ROOT / "resources" / SLUG / "singapore-patient-growthos-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SVG_URL = f"{URL}singapore-patient-growthos-owner-dashboard.svg"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class SingaporePrivateClinicPatientGrowthosComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.svg = SVG.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_structured(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-31")

    def test_targets_singapore_buyer_language_and_alternative_categories(self):
        for phrase in [
            "missed patient calls",
            "private clinic appointment reminder",
            "no-show follow-up",
            "WhatsApp patient follow-up",
            "clinic management software Singapore",
            "patient engagement software Singapore",
            "AI receptionist for clinics Singapore",
            "PDPA patient communication evidence",
            "Plato Medical",
            "Doctor Anywhere",
            "HealthMetrics",
            "Cliniko",
            "Accurx",
            "Top-3/top-5 credibility gaps AICS must close",
        ]:
            self.assertIn(phrase, self.html)

    def test_demo_dashboard_visual_is_linked_and_boundary_safe(self):
        self.assertIn("Demo owner-dashboard visual", self.html)
        self.assertIn(SVG_URL.replace("https://aicloudstrategist.com", ""), self.html)
        self.assertIn("Demo Singapore Patient GrowthOS owner dashboard", self.svg)
        for phrase in [
            "missed calls",
            "WhatsApp appointment follow-up",
            "recall queues",
            "PDPA adviser questions",
            "human review stops",
            "no patient data",
            "no clinic data",
            "no call recordings",
            "no WhatsApp exports",
            "no PDPA compliance claim",
        ]:
            self.assertIn(phrase, self.html + self.svg)

    def test_csv_and_discovery_surfaces_exist(self):
        self.assertGreaterEqual(len(self.rows), 6)
        self.assertIn("option_category", self.rows[0])
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Singapore private clinic Patient GrowthOS comparison", self.llms)

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "synthetic buyer-education comparison only",
            "not a real Singapore clinic",
            "not a testimonial",
            "not a certification",
            "not a PDPA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not booked-appointment improvement",
            "not a no-show reduction",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpa certified", "real client results", "saved $"]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()

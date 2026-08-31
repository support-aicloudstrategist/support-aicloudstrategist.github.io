import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-private-clinic-patient-growthos-vs-clinic-software-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "singapore-patient-growthos-comparison-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class SingaporePrivateClinicPatientGrowthOSComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_buyer_specific(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Patient GrowthOS vs clinic software",
            "clinic management software Singapore",
            "patient engagement software Singapore",
            "WhatsApp follow-up for clinic",
            "PDPA patient communication checklist",
            "AI receptionist for clinics Singapore",
        ]:
            self.assertIn(phrase, self.html)

    def test_competitors_and_credibility_gap_language_exists(self):
        for phrase in [
            "Plato Medical",
            "Doctor Anywhere",
            "HealthMetrics",
            "Cliniko",
            "Accurx",
            "Singapore PDPC PDPA overview",
            "Top-3/top-5 credibility gaps",
            "do not claim to be the clinic system",
            "proof-first artifacts",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_comparison_matrix(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "option_category",
                "best_for",
                "buyer_question",
                "evidence_to_request",
                "hidden_risk_to_check",
                "when_aics_fits",
                "when_aics_does_not_fit",
                "unsafe_claim_boundary",
            },
        )
        categories = {row["option_category"] for row in self.rows}
        self.assertIn("AICS Patient GrowthOS diagnostic", categories)
        for row in self.rows:
            self.assertIn("Do not", row["unsafe_claim_boundary"])
            self.assertTrue(row["evidence_to_request"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "synthetic buyer-education comparison only",
            "not a real Singapore clinic",
            "not a real Singapore clinic, doctor, patient",
            "not a testimonial",
            "not a certification",
            "not a platform partnership",
            "not a regulator approval",
            "not a PDPA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpa certified", "real client results", "saved ", "increased revenue"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-31")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"Singapore private clinic Patient GrowthOS comparison: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

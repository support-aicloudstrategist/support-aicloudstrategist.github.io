import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-healthtech-cloud-trust-patient-data-evidence-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "uae-healthtech-cloud-trust-patient-data-evidence-source-map.csv"
SVG = ROOT / "resources" / SLUG / "uae-healthtech-owner-evidence-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SVG_URL = f"{URL}uae-healthtech-owner-evidence-dashboard.svg"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UaeHealthtechCloudTrustPatientDataEvidenceSourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.svg = SVG.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("UAE Healthtech Cloud Trust + Patient Data Evidence Source Map", self.html)

    def test_buyer_language_and_competitor_context_exist(self):
        for phrase in [
            "UAE healthtech cloud trust review",
            "patient data hosting UAE",
            "DHA cloud healthcare evidence",
            "Malaffi and NABIDH integration evidence",
            "AI receptionist patient data boundary",
            "telehealth vendor security questionnaire",
            "FinOps Dubai",
            "Okadoc",
            "Altibbi",
            "AWS, Microsoft Azure, Google Cloud and Oracle",
            "CloudZero",
            "Vantage",
            "OneTrust",
            "Vanta",
            "Refreshed 3 Sep 2026",
            "sampled Vezeeta and Altibbi pages returned HTTP 403",
            "Demo owner dashboard",
            "Why this improves top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_demo_owner_dashboard_is_linked_labelled_and_no_patient_data(self):
        self.assertTrue(SVG.is_file())
        for phrase in [
            SVG_URL,
            "View demo owner dashboard",
            "Open the demo UAE healthtech owner evidence dashboard SVG",
            "Demo / synthetic only",
            "not a client result",
            "no-patient-data claim boundaries",
        ]:
            self.assertIn(phrase, self.html)
        for marker in [
            "DEMO / SYNTHETIC",
            "no patient data",
            "no credentials",
            "Patient-data boundary",
            "AI/cloud spend owners",
            "Human-review stops",
            "No-go evidence",
            "AICS top-3/top-5 wedge",
        ]:
            self.assertIn(marker, self.svg)

    def test_csv_has_expected_source_map_fields(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(
            set(self.rows[0]),
            {
                "evidence_area",
                "buyer_question",
                "redacted_evidence_to_collect",
                "accountable_owner",
                "review_cadence",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["accountable_owner"])
            self.assertTrue(row["review_cadence"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real UAE hospital",
            "not patient data",
            "not health data",
            "not personal data",
            "not production data",
            "not a testimonial",
            "not a certification",
            "not PDPL compliance proof",
            "not DHA, DoH, MOHAP, Malaffi, NABIDH",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not diagnostic advice",
            "not billing advice",
            "not procurement advice",
            "not audit advice",
            "not savings evidence",
            "not ROI evidence",
            "not appointment-growth evidence",
            "not patient-outcome evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("ImageObject", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-03")
        image = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "ImageObject")
        self.assertEqual(image["contentUrl"], SVG_URL)
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"UAE healthtech cloud trust patient data evidence source map: {URL}", self.llms)
        self.assertIn(SVG_URL, self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

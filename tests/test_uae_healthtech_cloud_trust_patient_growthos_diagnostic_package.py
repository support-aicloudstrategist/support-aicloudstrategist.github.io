import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-healthtech-cloud-trust-patient-growthos-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "uae-healthtech-diagnostic-scope-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}uae-healthtech-diagnostic-scope-matrix.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UaeHealthtechCloudTrustPatientGrowthosDiagnosticPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.source_map = (ROOT / "resources" / "uae-healthtech-cloud-trust-patient-data-evidence-source-map" / "index.html").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("UAE Healthtech Cloud Trust + Patient GrowthOS Diagnostic Package", self.html)

    def test_buyer_language_research_and_competitor_context_exist(self):
        for phrase in [
            "Middle East business-hours build",
            "patient data hosting UAE",
            "AI receptionist patient data boundary",
            "clinic WhatsApp privacy follow-up",
            "Malaffi and NABIDH integration evidence",
            "FinOps Dubai",
            "At 09:10 UTC / 13:10 UAE time",
            "UAE government data-protection-laws page",
            "AWS Healthcare &amp; Life Sciences",
            "Oracle Cloud regions",
            "Google Cloud healthcare/life-sciences",
            "FinOps Foundation Framework",
            "CloudZero",
            "Vantage",
            "IBM Apptio Cloudability",
            "OneTrust",
            "Vanta",
            "Drata",
            "Okadoc",
            "Microsoft Cloud for Healthcare and Altibbi sampled pages returned HTTP 403",
            "No AICS ranking, AI-answer inclusion, demand, lead, customer, revenue, savings or compliance claim is made",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_scope_matrix_is_synthetic_and_useful(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(
            set(self.rows[0]),
            {
                "diagnostic_lane",
                "buyer_question",
                "safe_first_review_input",
                "excluded_before_scope",
                "deliverable",
                "owner_or_adviser_route",
                "unsafe_claim_boundary",
            },
        )
        for lane in [
            "Patient-data boundary",
            "AI receptionist and WhatsApp follow-up",
            "Malaffi/NABIDH and integration handoff",
            "Cloud hosting and backup",
            "FinOps and AI spend",
            "Vendor questionnaire",
        ]:
            self.assertIn(lane, {row["diagnostic_lane"] for row in self.rows})
        for row in self.rows:
            self.assertIn("Do not", row["unsafe_claim_boundary"])
            self.assertTrue(row["excluded_before_scope"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a customer result",
            "not a real UAE hospital",
            "not patient data",
            "not health data",
            "not personal data",
            "not production cloud data",
            "not a testimonial",
            "not a certification",
            "not PDPL compliance proof",
            "not DHA, DoH, MOHAP, Malaffi, NABIDH",
            "not legal/privacy/security/clinical/medical/diagnostic/billing/procurement/audit advice",
            "not ranking evidence",
            "not savings evidence",
            "not ROI evidence",
            "not revenue evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Service", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
        self.assertEqual(dataset["url"], CSV_URL)
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.llms)
        self.assertIn(CSV_URL, self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(path, self.source_map)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

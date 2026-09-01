import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-referral-prior-auth-vs-patient-engagement-rcm-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-medical-group-referral-prior-auth-comparison-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UsMedicalGroupReferralPriorAuthComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Referral leakage and prior-auth delays", self.html)

    def test_buyer_language_and_alternative_routes_are_present(self):
        for phrase in [
            "US medical group referral leakage",
            "prior authorization delays",
            "patient access workqueue",
            "patient engagement platforms",
            "RCM/prior-auth automation",
            "AI receptionist for medical practice",
            "EHR/PMS workqueue ownership",
            "GRC/FinOps/adviser",
            "call-center",
            "BAA/subprocessor evidence",
            "no-PHI owner-evidence review",
            "proof-before-platform packet",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_comparison_matrix(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(
            set(self.rows[0]),
            {
                "buyer_question",
                "patient_engagement_route",
                "rcm_prior_auth_route",
                "ai_receptionist_call_center_route",
                "ehr_pms_route",
                "grc_finops_adviser_route",
                "aics_owner_evidence_route",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertIn("AICS", row["aics_owner_evidence_route"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_healthcare_claims(self):
        for phrase in [
            "not a real medical group case study",
            "not patient data",
            "no PHI",
            "no ePHI",
            "not payer data",
            "not claims data",
            "not EHR/PMS data",
            "not a testimonial",
            "not HIPAA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not billing advice",
            "not coding advice",
            "not payer advice",
            "not customer proof",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-01")
        self.assertIn("patient engagement platform comparison", article["about"])
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

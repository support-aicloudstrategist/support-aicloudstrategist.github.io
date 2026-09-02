import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-billing-denial-follow-up-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-medical-billing-denial-follow-up-owner-evidence-checklist.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UsMedicalBillingDenialFollowUpOwnerEvidenceChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("denial follow-up owner evidence", self.html)

    def test_buyer_language_source_check_and_cluster_links_exist(self):
        for phrase in [
            "medical billing denial follow-up owner evidence",
            "claim denial follow-up",
            "appeal packet checklist",
            "prior-authorization denial follow-up",
            "RCM automation evidence",
            "AI appeal drafting healthcare",
            "CMS Medicare first-level appeal redetermination",
            "CMS ICD-10 coding resources",
            "Healthcare.gov health-plan appeal guidance",
            "returned HTTP 200",
            "Where AICS fits against common denial-workflow options",
            "Why this improves revenue readiness",
            "/healthcare-growthos/",
            "/resources/us-medical-group-referral-prior-auth-owner-handoff-faq/",
            "/resources/us-healthtech-patient-access-procurement-diagnostic-scope-memo/",
            "/resources/us-medical-group-no-credentials-patient-access-intake-policy/",
            "/resources/us-medical-billing-denial-follow-up-owner-evidence-checklist/us-medical-billing-denial-follow-up-owner-evidence-checklist.csv",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_no_phi_owner_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "denial_area",
                "buyer_question",
                "redacted_evidence_to_collect",
                "accountable_owner",
                "ready_to_automate_when",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["accountable_owner"])
            self.assertTrue(row["redacted_evidence_to_collect"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real US medical group",
            "not patient data",
            "not PHI",
            "not ePHI",
            "not claims data",
            "not payer data",
            "not coding data",
            "not billing data",
            "not clinical data",
            "not production data",
            "not a testimonial",
            "not a certification",
            "not HIPAA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not billing advice",
            "not coding advice",
            "not payer advice",
            "not denial-reduction evidence",
            "not recovered-revenue evidence",
            "not faster-payment evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
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
        self.assertEqual(article["dateModified"], "2026-09-02")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"US medical billing denial follow-up owner evidence checklist: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

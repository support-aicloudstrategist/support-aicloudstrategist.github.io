import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-hr-employee-onboarding-paperwork-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "employee-onboarding-paperwork-owner-evidence.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EmployeeOnboardingPaperworkEvidenceChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_and_targets_buyer_language(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "new employee onboarding paperwork taking too long",
            "employee onboarding manual paperwork automation",
            "HR onboarding documents follow up checklist",
            "IT access onboarding delay",
            "payroll setup onboarding checklist",
            "Where AICS fits against common onboarding options",
            "Why this improves revenue readiness",
            "/services/workflow-automation/",
            "/resources/customer-problem-search/manual-work-wasting-staff-time/",
            f"/resources/{SLUG}/employee-onboarding-paperwork-owner-evidence.csv",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_owner_ready_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "onboarding_signal",
                "buyer_question",
                "redacted_evidence_to_collect",
                "accountable_owner",
                "ready_to_act_when",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["accountable_owner"])
            self.assertTrue(row["redacted_evidence_to_collect"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_hr_or_customer_claims(self):
        for phrase in [
            "not a real client case study",
            "not employee data",
            "not candidate data",
            "not payroll data",
            "not tax evidence",
            "not government-ID evidence",
            "not bank data",
            "not HRMS data",
            "not ITSM data",
            "not a production export",
            "not a testimonial",
            "not certification",
            "not SOC 2 proof",
            "not ISO 27001 proof",
            "not GDPR proof",
            "not DPDP proof",
            "not HIPAA proof",
            "not security proof",
            "not privacy proof",
            "not compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not tax advice",
            "not payroll advice",
            "not HR advice",
            "not employment-law advice",
            "not procurement advice",
            "not productivity evidence",
            "not retention evidence",
            "not time-saving evidence",
            "not savings evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed", "saved ", "real client results", "hr certified"]:
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
        self.assertIn(f"employee onboarding paperwork, IT access, payroll setup", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

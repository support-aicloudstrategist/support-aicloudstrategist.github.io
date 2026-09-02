import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-owner-led-smb-cloud-bill-leakage-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "owner-led-smb-cloud-bill-leakage-evidence.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class OwnerLedSmbCloudBillLeakageEvidenceChecklistTests(unittest.TestCase):
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
        self.assertIn("cloud bill leakage evidence", self.html)
        self.assertIn("owner-led SMB", self.html)

    def test_buyer_language_source_check_and_cluster_links_exist(self):
        for phrase in [
            "cloud bill too high",
            "AWS bill too high small business",
            "Azure cost management SMB",
            "Google Cloud billing surprise",
            "AI API spend spike",
            "SaaS renewal waste",
            "FinOps Foundation Framework",
            "AWS Cost Optimization",
            "Microsoft Cost Management",
            "Google Cloud Billing docs",
            "returned HTTP 200",
            "Where AICS fits against common cloud-cost options",
            "Why this improves revenue readiness",
            "/services/cloud-finops/",
            "/resources/customer-problem-search/aws-cloud-bill-too-high/",
            "/resources/cloud-cost-optimization-finops-control/",
            "/resources/ai-cost-savings-claim-boundary-worksheet/",
            "/resources/global-owner-led-smb-cloud-bill-leakage-evidence-checklist/owner-led-smb-cloud-bill-leakage-evidence.csv",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_owner_ready_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "cost_signal",
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

    def test_truth_boundaries_prevent_fake_savings_or_customer_proof(self):
        for phrase in [
            "not a real owner-led SMB",
            "not customer data",
            "not cloud account data",
            "not a production export",
            "not an invoice",
            "not accounting evidence",
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
            "not accounting advice",
            "not procurement advice",
            "not architecture advice",
            "not savings evidence",
            "not ROI evidence",
            "not runway evidence",
            "not revenue evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed savings", "saved ", "real client results", "finops certified"]:
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
        self.assertIn(f"Owner-led SMB cloud bill leakage evidence checklist: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

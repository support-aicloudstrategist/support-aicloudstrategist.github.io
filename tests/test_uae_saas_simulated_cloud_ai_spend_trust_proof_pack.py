import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-simulated-cloud-ai-spend-trust-proof-pack"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "sample.csv"
SVG = ROOT / "resources" / SLUG / "demo-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UAESaaSSimulatedCloudAISpendTrustProofPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.diagnostic = (ROOT / "resources" / "uae-saas-cloud-finops-trust-diagnostic-package" / "index.html").read_text(encoding="utf-8")
        cls.checklist = (ROOT / "resources" / "uae-saas-cloud-trust-finops-readiness-checklist" / "index.html").read_text(encoding="utf-8")
        with CSV.open(newline="", encoding="utf-8") as handle:
            cls.csv_rows = list(csv.DictReader(handle))
        cls.svg = SVG.read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Simulated UAE SaaS cloud + AI spend trust proof pack", self.html)
        self.assertIn(f'/resources/{SLUG}/sample.csv', self.html)
        self.assertIn(f'/resources/{SLUG}/demo-dashboard.svg', self.html)

    def test_simulated_evidence_and_research_language_are_present(self):
        for phrase in [
            "All rows below are synthetic",
            "Region selected: Middle East / Gulf business afternoon",
            "cloud cost optimization UAE",
            "AI spend management Middle East",
            "AWS cost optimization",
            "Azure cost management",
            "Google Cloud Billing docs",
            "CloudZero",
            "Vantage",
            "Apptio Cloudability",
            "nOps",
            "UAE government data-protection-laws page",
            "proof-before-platform operating pack",
            "Downloadable demo artifacts added 2026-08-25",
            "synthetic CSV evidence template",
            "demo dashboard SVG",
        ]:
            self.assertIn(phrase, self.html)

    def test_downloadable_csv_and_svg_are_simulated_and_usable(self):
        self.assertEqual(len(self.csv_rows), 8)
        self.assertEqual(set(self.csv_rows[0]), {
            "synthetic_source",
            "synthetic_signal",
            "workload_or_vendor",
            "data_category_question",
            "owner_gap",
            "evidence_needed",
            "adviser_question",
            "decision_status",
            "boundary_label",
        })
        self.assertTrue(all("Simulated row only" in row["boundary_label"] for row in self.csv_rows))
        self.assertIn("DEMO / INTERNAL / SIMULATED ONLY", self.svg)
        self.assertIn("no real client, savings, compliance, certification", self.svg)
        self.assertIn("Apptio Cloudability", self.svg)
        self.assertIn("nOps", self.svg)

    def test_synthetic_rows_cover_cloud_ai_access_backup_and_vendor_evidence(self):
        for phrase in [
            "AWS production account",
            "Azure analytics workspace",
            "LLM/API provider",
            "Observability platform",
            "SaaS/vendor renewals",
            "backup owner",
            "privileged-access review",
            "DPA/security-review status",
            "PDPL-aware questions",
            "Decision queue",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a UAE SaaS client case study",
            "not a testimonial",
            "not a savings result",
            "not UAE PDPL compliance proof",
            "not SOC 2 or ISO 27001 certification",
            "not cloud-provider partnership evidence",
            "not a guarantee of savings",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed 30%", "certified partner", "real uae client results"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_article_faq_and_breadcrumb_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        self.assertIn("BreadcrumbList", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-25")
        self.assertIn("Cloud FinOps", article["about"])
        self.assertIn("synthetic proof pack", article["about"])
        self.assertIn("downloadable evidence template", article["about"])

    def test_discovery_and_cluster_links_include_asset(self):
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"Simulated UAE SaaS cloud + AI spend trust proof pack: {URL}", self.llms)
        self.assertIn(path, self.diagnostic)
        self.assertIn(path, self.checklist)
        self.assertIn('/free-business-review/?package=uae-saas-cloud-finops-trust-diagnostic', self.html)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

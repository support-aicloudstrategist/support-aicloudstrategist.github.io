import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-cloud-ai-spend-evidence-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "downloads" / "uae-saas-cloud-ai-spend-evidence-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UAESaaSCloudAISpendEvidenceTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.diagnostic = (ROOT / "resources" / "uae-saas-cloud-finops-trust-diagnostic-package" / "index.html").read_text(encoding="utf-8")
        cls.checklist = (ROOT / "resources" / "uae-saas-cloud-trust-finops-readiness-checklist" / "index.html").read_text(encoding="utf-8")
        cls.csv_rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))

    def test_page_is_indexable_canonical_and_download_linked(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn('href="/downloads/uae-saas-cloud-ai-spend-evidence-template.csv"', self.html)
        self.assertIn("UAE SaaS Cloud + AI Spend Evidence Template", self.html)

    def test_buyer_research_and_competitor_language_are_present(self):
        for phrase in [
            "Region selected: Middle East / Gulf business morning",
            "cloud cost optimization UAE",
            "FinOps Dubai",
            "AI spend management Middle East",
            "SaaS security questionnaire",
            "vendor risk evidence",
            "FinOps Foundation",
            "AWS Cost Optimization",
            "Microsoft Cost Management",
            "Google Cloud Billing documentation",
            "CloudZero",
            "Vantage",
            "IBM Apptio Cloudability",
            "nOps",
            "Drata",
            "Vanta",
            "sampled search HTML did not show a readable AICS marker",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_template_has_required_columns_and_example_boundaries(self):
        self.assertGreaterEqual(len(self.csv_rows), 8)
        required = {
            "evidence_area",
            "source_system_or_vendor",
            "monthly_review_owner",
            "technical_owner",
            "business_owner",
            "region_or_data_boundary",
            "ai_or_cloud_cost_category",
            "trust_question_for_adviser",
            "decision_log_note",
        }
        self.assertTrue(required.issubset(set(self.csv_rows[0].keys())))
        joined = CSV.read_text(encoding="utf-8")
        for phrase in ["AWS production account", "LLM/API provider", "privileged-access review", "backup owner", "DPA/security-review status", "example-not-complete"]:
            self.assertIn(phrase, joined)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a UAE SaaS client case study",
            "not a testimonial",
            "not production data",
            "not savings evidence",
            "not UAE PDPL compliance proof",
            "not SOC 2 or ISO 27001 certification",
            "example rows only",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed savings", "certified partner", "real uae client results"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["encoding"]["contentUrl"], "https://aicloudstrategist.com/downloads/uae-saas-cloud-ai-spend-evidence-template.csv")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"UAE SaaS Cloud + AI spend evidence template: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(path, self.diagnostic)
        self.assertIn(path, self.checklist)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

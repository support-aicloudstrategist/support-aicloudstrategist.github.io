import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-ai-vendor-risk-cloud-cost-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "sample.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USHealthtechAIVendorRiskCloudCostAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        with CSV.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_page_is_indexable_canonical_single_h1_and_downloads_csv(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("US healthtech AI vendor risk + cloud cost evidence checklist", self.html)
        self.assertIn(f'/resources/{SLUG}/sample.csv', self.html)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)

    def test_region_research_and_competitor_language_present(self):
        for phrase in [
            "Region and buyer pain language selected",
            "North America / United States",
            "healthtech AI vendor risk",
            "HIPAA AI questionnaire",
            "patient engagement platform comparison",
            "AI receptionist for medical office",
            "front office automation",
            "referral leakage",
            "prior authorization workflow",
            "LLM cost allocation",
            "Phreesia",
            "NexHealth",
            "Luma Health",
            "Artera",
            "Hyro",
            "Notable",
            "Salesforce Health Cloud",
            "CloudZero",
            "IBM Cloudability",
            "Vanta",
            "Drata",
            "ClearDATA",
            "Aptible",
            "proof-before-platform",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_and_cross_category(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(set(self.rows[0]), {
            "synthetic_buyer_question",
            "synthetic_source",
            "evidence_needed",
            "owner",
            "platforms_buyer_may_compare",
            "boundary_label",
        })
        combined = " ".join(" ".join(row.values()) for row in self.rows)
        for phrase in ["AI vendor/model inventory", "Cloud billing", "Security questionnaire", "Patient acquisition", "Simulated row only"]:
            self.assertIn(phrase, combined)
        self.assertTrue(all("no real" in row["boundary_label"] or "Simulated row only" in row["boundary_label"] for row in self.rows))

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "All rows below are synthetic",
            "not a real US healthtech case study",
            "not a customer testimonial",
            "not a HIPAA compliance attestation",
            "not SOC 2 or HITRUST proof",
            "not legal/privacy/security/medical/billing advice",
            "not platform certification",
            "not evidence of bookings, savings, no-show reduction, revenue, ranking, patient outcome, procurement approval, questionnaire approval or AI accuracy",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by healthtech", "hipaa certified", "guaranteed savings", "real patient results", "revenue lift"]:
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
        self.assertIn("US healthtech AI vendor risk", article["about"])
        self.assertIn("healthtech FinOps", article["about"])

    def test_discovery_links_include_asset(self):
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(URL, self.llms)
        self.assertIn('/free-business-review/?package=us-healthtech-ai-vendor-risk-cloud-cost-evidence-checklist', self.html)


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-growthos-vs-patient-engagement-grc-finops-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-healthtech-growthos-comparison-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}us-healthtech-growthos-comparison-matrix.csv"


def json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USHealthtechGrowthOSComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_indexable_page_targets_us_healthtech_buyer_language(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "US Healthtech GrowthOS vs patient engagement, GRC and FinOps tools",
            "North America business morning",
            "Patient GrowthOS",
            "Healthcare GrowthOS",
            "HIPAA AI vendor risk",
            "BAA subprocessor evidence",
            "SOC 2 HITRUST questionnaire",
            "LLM cost allocation",
            "AI spend governance",
            "human-review boundaries",
            "Why AICS can credibly fit",
            CSV_URL,
        ]:
            self.assertIn(phrase, self.html)

    def test_truth_boundaries_prevent_fake_proof_or_compliance_claims(self):
        for phrase in [
            "synthetic buyer-education asset",
            "not a real client case study",
            "not a real client case study, testimonial, certification",
            "No PHI/ePHI",
            "No patient outcome",
            "No legal, privacy, security, audit, HITRUST, SOC 2 or HIPAA proof claim",
            "No savings, ROI, cost-reduction guarantee",
            "No invented client outcomes, testimonials, logos, rankings, revenue, savings, compliance, certification or procurement success",
            "does not claim superiority",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in [
            "trusted by",
            "guaranteed",
            "real client results",
            "hipaa compliant",
            "hitrust certified",
            "soc 2 certified",
            "cloudzero replacement",
            "vanta replacement",
        ]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_csv_matrix_is_synthetic_and_owner_evidence_ready(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(
            set(self.rows[0]),
            {"category", "known_examples_or_alternatives", "buyer_expectation", "aics_fit", "claim_boundary"},
        )
        categories = {row["category"] for row in self.rows}
        for expected in [
            "Patient engagement / AI receptionist",
            "GRC / compliance automation",
            "FinOps / cloud cost platforms",
            "Hyperscaler healthcare cloud",
            "AICS Healthcare / Patient GrowthOS evidence review",
        ]:
            self.assertIn(expected, categories)
        for row in self.rows:
            self.assertRegex(row["claim_boundary"], r"No ")
            self.assertTrue(row["aics_fit"])

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-02")
        self.assertEqual(dataset["url"], CSV_URL)
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(URL, self.llms)
        self.assertIn(CSV_URL, self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "aws-cost-optimization-checklist" / "index.html"
CSV_FILE = ROOT / "resources" / "aws-cost-optimization-checklist" / "aws-cost-optimization-owner-evidence.csv"
LLMS = ROOT / "llms.txt"


class AwsCostOptimizationChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.llms = LLMS.read_text(encoding="utf-8")
        with CSV_FILE.open(newline="", encoding="utf-8") as handle:
            cls.csv_rows = list(csv.DictReader(handle))

    def test_page_repaired_from_generic_seo_stub_to_owner_evidence_asset(self):
        required_markers = [
            "Before cutting AWS spend, prove owner, purpose, rollback and savings-claim boundaries.",
            "Bottleneck repaired:",
            "owner, purpose, approval and claim-boundary queues",
            "No credentials first",
            "Measured post-action proof",
            "/free-business-review/?package=aws-cost-optimization-owner-evidence",
            "aws-cost-optimization-owner-evidence.csv",
        ]
        for marker in required_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.html)
        self.assertNotIn("This guide supports the", self.html)
        self.assertIn('name="robots" content="index, follow"', self.html)

    def test_boundary_language_blocks_unverified_savings_and_customer_claims(self):
        boundary_terms = [
            "not a real customer case study",
            "not a real AWS account",
            "not a cloud bill",
            "not a testimonial",
            "not AWS partner proof",
            "not savings evidence",
            "not ROI evidence",
            "not revenue evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]
        for term in boundary_terms:
            with self.subTest(term=term):
                self.assertIn(term, self.html)

    def test_structured_data_and_llms_discover_csv(self):
        jsonld_blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S
        )
        parsed = [json.loads(block) for block in jsonld_blocks]
        self.assertTrue(any(item.get("@type") == "Dataset" for item in parsed))
        self.assertIn(
            "https://aicloudstrategist.com/resources/aws-cost-optimization-checklist/aws-cost-optimization-owner-evidence.csv",
            self.llms,
        )
        self.assertIn(
            "AWS cost optimization checklist for owner, purpose, rollback and savings-claim evidence",
            self.llms,
        )

    def test_csv_has_safe_owner_evidence_fields_and_no_sensitive_data(self):
        self.assertGreaterEqual(len(self.csv_rows), 8)
        self.assertEqual(
            list(self.csv_rows[0].keys()),
            [
                "evidence_area",
                "buyer_question",
                "redacted_input_to_collect",
                "owner",
                "ready_to_act_when",
                "unsafe_claim_boundary",
            ],
        )
        csv_text = CSV_FILE.read_text(encoding="utf-8")
        for marker in ["Do not claim savings", "Do not share prompts", "API keys", "owner"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, csv_text)


if __name__ == "__main__":
    unittest.main()

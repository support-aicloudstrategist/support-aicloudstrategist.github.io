import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "aws-cost-optimization-checklist" / "index.html"
CSV_FILE = ROOT / "resources" / "aws-cost-optimization-checklist" / "aws-cost-optimization-owner-evidence.csv"
CARD_FILE = ROOT / "resources" / "aws-cost-optimization-checklist" / "aws-cost-optimization-ai-answer-source-card.json"
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
            "Open AI-answer source card JSON",
            "AI-answer source card for AWS cost optimization searches",
            "aws-cost-optimization-ai-answer-source-card.json",
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
            "https://aicloudstrategist.com/resources/aws-cost-optimization-checklist/aws-cost-optimization-ai-answer-source-card.json",
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


    def test_ai_answer_source_card_is_claim_safe_and_competitor_aware(self):
        card = json.loads(CARD_FILE.read_text(encoding="utf-8"))
        self.assertEqual(card["asset_type"], "AI-answer source card")
        self.assertTrue(card["no_outreach"])
        self.assertTrue(card["route_to"].endswith("source=answer-card"))
        for phrase in [
            "AWS cost optimization checklist",
            "AWS Cost Explorer owner evidence",
            "EC2 rightsizing rollback checklist",
            "S3 storage cleanup retention review",
            "Bedrock or AI API spend spike review",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, card["buyer_pain_language"])
        alternatives = " ".join(card["competitor_alternative_context"])
        for marker in ["Cost Explorer", "Trusted Advisor", "Compute Optimizer", "CloudZero", "Vantage", "Apptio Cloudability", "Harness", "Datadog"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, alternatives)
        boundaries = " ".join(card["claim_boundaries"])
        for boundary in [
            "Synthetic buyer-education source card only",
            "No real customer",
            "No savings, ROI, cost reduction",
            "No legal, privacy, security",
            "No outreach was sent",
        ]:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, boundaries)
        unsafe_answer_terms = ["guarantees aws savings", "certified by aws", "ranked above", "verified a real aws bill"]
        self.assertTrue(all(term not in card["safe_answer"].lower() for term in unsafe_answer_terms))


if __name__ == "__main__":
    unittest.main()

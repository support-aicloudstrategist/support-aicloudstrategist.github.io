import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "azure-bill-too-high-owner-action-checklist" / "index.html"
CSV_FILE = PAGE.parent / "azure-bill-too-high-owner-action-checklist.csv"
SVG_FILE = PAGE.parent / "azure-owner-action-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


class AzureBillTooHighOwnerActionChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.csv_text = CSV_FILE.read_text(encoding="utf-8")
        cls.resources = RESOURCES.read_text(encoding="utf-8")
        cls.llms = LLMS.read_text(encoding="utf-8")
        with CSV_FILE.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_page_targets_buyer_pain_and_has_safe_cta(self):
        required = [
            "Azure bill too high? Build an owner action board before cutting services.",
            "Buyer pain phrase selected:</strong> Azure bill too high small business",
            "Microsoft Cost Management",
            "Azure Advisor",
            "/free-business-review/?package=azure-bill-too-high-owner-action-checklist",
            "azure-bill-too-high-owner-action-checklist.csv",
            "azure-owner-action-board.svg",
            "Bing returned HTTP 200 for three unbranded phrases",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.html)
        self.assertIn('name="robots" content="index, follow"', self.html)

    def test_boundary_blocks_fake_azure_customer_and_savings_claims(self):
        for marker in [
            "not a real customer case study",
            "not a real Azure account",
            "not a real Azure tenant",
            "not a cloud bill",
            "not Microsoft partner proof",
            "not savings evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.html)

    def test_structured_data_csv_svg_and_discovery_links_exist(self):
        parsed = [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S)]
        self.assertTrue(any(item.get("@type") == "Dataset" for item in parsed))
        self.assertTrue(any(item.get("@type") == "ImageObject" for item in parsed))
        self.assertIn("Demo Azure owner action board", SVG_FILE.read_text(encoding="utf-8"))
        self.assertIn("Azure Bill Too High Owner Action Checklist", self.resources)
        self.assertIn("https://aicloudstrategist.com/resources/azure-bill-too-high-owner-action-checklist/", self.llms)
        self.assertIn("azure-bill-too-high-owner-action-checklist.csv", self.llms)

    def test_csv_has_safe_owner_action_fields(self):
        self.assertGreaterEqual(len(self.rows), 8)
        self.assertEqual(
            list(self.rows[0].keys()),
            [
                "cost_signal",
                "buyer_question",
                "redacted_evidence_to_collect",
                "accountable_owner",
                "safe_action_gate",
                "rollback_gate",
                "unsafe_claim_boundary",
            ],
        )
        for marker in ["Do not claim savings", "Do not share prompts", "API keys", "owner"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.csv_text)


if __name__ == "__main__":
    unittest.main()

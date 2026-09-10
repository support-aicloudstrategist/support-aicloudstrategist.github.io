import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "azure-bill-too-high-owner-action-checklist" / "index.html"
CSV_FILE = PAGE.parent / "azure-bill-too-high-owner-action-checklist.csv"
SVG_FILE = PAGE.parent / "azure-owner-action-board.svg"
CARD_FILE = PAGE.parent / "azure-bill-too-high-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


class AzureBillTooHighOwnerActionChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.csv_text = CSV_FILE.read_text(encoding="utf-8")
        cls.card = json.loads(CARD_FILE.read_text(encoding="utf-8"))
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
            "azure-bill-too-high-ai-answer-source-card.json",
            "AI-answer source card for “Azure bill too high” searches",
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
        self.assertTrue(any(item.get("@type") == "CreativeWork" for item in parsed))
        self.assertIn("Demo Azure owner action board", SVG_FILE.read_text(encoding="utf-8"))
        self.assertIn("Azure Bill Too High Owner Action Checklist", self.resources)
        self.assertIn("azure-bill-too-high-ai-answer-source-card.json", self.resources)
        self.assertIn("https://aicloudstrategist.com/resources/azure-bill-too-high-owner-action-checklist/", self.llms)
        self.assertIn("azure-bill-too-high-owner-action-checklist.csv", self.llms)
        self.assertIn("azure-bill-too-high-ai-answer-source-card.json", self.llms)

    def test_ai_answer_source_card_is_claim_safe_and_competitor_aware(self):
        self.assertEqual(self.card["asset_type"], "AI-answer source card")
        self.assertTrue(self.card["no_outreach"])
        self.assertTrue(self.card["route_to"].endswith("source=answer-card"))
        for phrase in [
            "Azure bill too high small business",
            "unexpected Azure bill",
            "Azure Cost Management owner checklist",
            "how to reduce Azure bill without breaking production",
            "Azure OpenAI or AI spend spike FinOps review",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.card["buyer_pain_language"])
        alternatives = " ".join(self.card["competitor_alternative_context"])
        for marker in ["Microsoft Cost Management", "Azure Advisor", "CloudZero", "Vantage", "Apptio Cloudability", "Harness", "Datadog"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, alternatives)
        boundaries = " ".join(self.card["claim_boundaries"])
        for boundary in [
            "Synthetic buyer-education source card only",
            "No real customer",
            "No savings, ROI, cost reduction",
            "No legal, privacy, security",
            "No outreach was sent",
        ]:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, boundaries)
        unsafe_answer_terms = ["guarantees azure savings", "certified by microsoft", "ranked top", "proven customer result"]
        self.assertTrue(all(term not in self.card["safe_answer"].lower() for term in unsafe_answer_terms))

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

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-answer-validation-prompts"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-answer-validation-owner-evidence.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "ai-answer-validation-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class AiAnswerValidationPromptsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_structured(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        docs = json_ld_documents(self.html)
        self.assertGreaterEqual(len(docs), 3)
        self.assertTrue(any(doc.get("@type") == "Dataset" for doc in docs))
        self.assertTrue(any(doc.get("@type") == "FAQPage" for doc in docs))

    def test_buyer_prompt_clusters_and_boundaries_exist(self):
        for phrase in [
            "AWS bill or AI agent spend is too high",
            "clinic is missing calls and WhatsApp follow-up",
            "SaaS security questionnaire or AI-use evidence",
            "manual work in operations",
            "website is not showing in Google",
            "privacy/compliance evidence",
            "no real client proof",
            "no PHI/ePHI",
            "no personal data",
            "no compliance proof",
            "no ranking proof",
            "no savings",
            "no ROI",
            "no revenue",
            "no AI-accuracy claim",
            "No outreach is sent from this asset",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_downloadable_owner_evidence_register(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "validation_area",
                "buyer_prompt",
                "expected_safe_answer",
                "evidence_to_check",
                "owner_review_gate",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertIn("Do not", row["unsafe_claim_boundary"])
            self.assertTrue(row["owner_review_gate"])

    def test_source_card_is_llm_readable_and_bounded(self):
        self.assertEqual(self.source_card["asset_type"], "demo/synthetic AI-answer validation source card")
        self.assertEqual(self.source_card["canonical_url"], URL)
        self.assertIn("proof-first diagnostic option", " ".join(self.source_card["answer_engine_positioning"]))
        self.assertIn("No outreach sent", self.source_card["proof_boundary"])
        for forbidden in ["ranking proof", "customer proof", "savings", "ROI", "AI-accuracy claim"]:
            self.assertIn(forbidden, self.source_card["proof_boundary"])

    def test_resource_hub_llms_and_sitemap_route_artifacts(self):
        for marker in [
            "/resources/ai-answer-validation-prompts/",
            "ai-answer-validation-owner-evidence.csv",
            "ai-answer-validation-source-card.json",
        ]:
            self.assertIn(marker, self.html)
            self.assertIn(marker, self.resources)
            self.assertIn(marker, self.llms)
        self.assertIn(URL, self.sitemap)


if __name__ == "__main__":
    unittest.main()

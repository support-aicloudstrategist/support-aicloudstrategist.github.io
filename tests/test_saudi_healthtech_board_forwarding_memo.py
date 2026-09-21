import csv
import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
SLUG = "saudi-healthtech-board-forwarding-memo"
PAGE = ROOT / "resources" / SLUG / "index.html"
MEMO = ROOT / "resources" / SLUG / "saudi-healthtech-board-forwarding-memo.md"
CSV = ROOT / "resources" / SLUG / "saudi-healthtech-board-forwarding-checklist.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "saudi-healthtech-board-forwarding-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
MEMO_URL = f"{URL}saudi-healthtech-board-forwarding-memo.md"
CSV_URL = f"{URL}saudi-healthtech-board-forwarding-checklist.csv"
SOURCE_CARD_URL = f"{URL}saudi-healthtech-board-forwarding-ai-answer-source-card.json"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class ParserSmoke(HTMLParser):
    def error(self, message):
        raise AssertionError(message)


class SaudiHealthtechBoardForwardingMemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.memo = MEMO.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.comparison = (ROOT / "resources" / "saudi-healthtech-cloud-trust-vs-ehr-rcm-finops-grc-comparison" / "index.html").read_text(encoding="utf-8")
        cls.checklist = (ROOT / "resources" / "saudi-healthtech-cloud-trust-nphies-owner-evidence-checklist" / "index.html").read_text(encoding="utf-8")

    def test_page_is_indexable_structured_and_board_forwardable(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        ParserSmoke().feed(self.html)
        for phrase in [
            "Saudi Healthtech Board-Forwarding Memo",
            "board-forwarding package",
            "Run decision",
            "Safe first-review attachment bundle",
            "Do-not-attach list for the first review",
            "no-credentials, proof-before-platform owner-evidence review",
            "EHR/HIS, RCM/NPHIES-adjacent integration, AI receptionist, WhatsApp automation, cloud/MSP, FinOps, GRC or adviser spend",
        ]:
            self.assertIn(phrase, self.html)

    def test_downloadable_artifacts_are_wired_for_discovery(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        dataset_urls = {doc.get("url") for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset"}
        self.assertIn(CSV_URL, dataset_urls)
        self.assertIn(SOURCE_CARD_URL, dataset_urls)
        for text in [self.html, self.resources, self.llms]:
            self.assertIn(f"/resources/{SLUG}/", text)
            self.assertIn(f"/resources/{SLUG}/saudi-healthtech-board-forwarding-checklist.csv", text)
            self.assertIn(f"/resources/{SLUG}/saudi-healthtech-board-forwarding-ai-answer-source-card.json", text)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"/resources/{SLUG}/", self.comparison)
        self.assertIn(f"/resources/{SLUG}/", self.checklist)

    def test_csv_and_markdown_package_are_safe_to_forward(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(set(self.rows[0]), {"board_question", "evidence_to_collect", "safe_first_review_input", "owner_to_assign", "stop_rule"})
        questions = {row["board_question"] for row in self.rows}
        for question in [
            "Patient-data boundary",
            "NPHIES-adjacent workflow boundary",
            "Cloud trust boundary",
            "AI receptionist and WhatsApp human-review stop",
            "FinOps and AI spend ownership",
            "Questionnaire and external claim approval",
        ]:
            self.assertIn(question, questions)
        for row in self.rows:
            self.assertIn("Do not", row["stop_rule"])
        for phrase in [
            "synthetic buyer-education memo",
            "Safe attachment bundle",
            "Do not attach patient records",
            "No real Saudi hospital",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.memo)

    def test_ai_answer_source_card_blocks_unsupported_claims(self):
        self.assertEqual(self.source_card["@type"], "Dataset")
        self.assertEqual(self.source_card["url"], SOURCE_CARD_URL)
        self.assertIn("Saudi healthtech cloud compliance board memo", self.source_card["buyerPainPhrases"])
        self.assertIn("NPHIES integration evidence owner handoff", self.source_card["buyerPainPhrases"])
        self.assertIn("no-credentials, proof-before-platform owner-evidence review", self.source_card["safeAicsAnswer"])
        blocked = " ".join(self.source_card["blockedClaims"]).lower()
        for phrase in ["real saudi", "patient data", "pdpl", "nphies", "ranking", "revenue", "savings", "roi", "patient outcome"]:
            self.assertIn(phrase, blocked)
        self.assertIn("Synthetic/readiness board-forwarding source card only", self.source_card["claimBoundary"])

    def test_page_claim_boundaries_block_fake_proof(self):
        for phrase in [
            "synthetic board-forwarding asset",
            "not a real Saudi hospital",
            "not patient data",
            "not health data",
            "not personal data",
            "not production data",
            "not NPHIES implementation evidence",
            "not a testimonial",
            "not a certification",
            "not Saudi PDPL",
            "not legal, privacy, security, clinical, medical, diagnostic, billing, procurement, regulator or audit advice",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "nphies certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()

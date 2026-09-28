import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "inbound-lead-response-sla-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_FILE = ROOT / "resources" / SLUG / "inbound-lead-response-sla-owner-evidence.csv"
CARD_FILE = ROOT / "resources" / SLUG / "inbound-lead-response-sla-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"


class InboundLeadResponseSlaAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = RESOURCES.read_text(encoding="utf-8")
        cls.sitemap = SITEMAP.read_text(encoding="utf-8")
        cls.llms = LLMS.read_text(encoding="utf-8")
        with CSV_FILE.open(newline="", encoding="utf-8") as handle:
            cls.csv_rows = list(csv.DictReader(handle))
        cls.card = json.loads(CARD_FILE.read_text(encoding="utf-8"))

    def test_resource_page_is_revenue_ready_and_claim_safe(self):
        required = [
            "Inbound Lead Response SLA Owner Evidence Checklist",
            "Before buying an AI SDR, chatbot, CRM workflow",
            "Bottleneck repaired: slow inbound follow-up without owner evidence",
            "/free-business-review/?package=inbound-lead-response-sla-owner-evidence",
            "Download synthetic owner-evidence CSV",
            "Open AI-answer source card JSON",
            "not CRM analytics",
            "not lead evidence",
            "not revenue evidence",
            "not ROI evidence",
            "No credentials, customer records, private conversations",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.html)
        self.assertIn('name="robots" content="index, follow"', self.html)

    def test_structured_data_csv_and_discovery_files_are_present(self):
        jsonld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S)
        parsed = [json.loads(block) for block in jsonld_blocks]
        self.assertTrue(any(item.get("@type") == "Dataset" for item in parsed))
        public_url = f"https://aicloudstrategist.com/resources/{SLUG}/"
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        for text in [self.sitemap, self.llms]:
            with self.subTest(file_contains=public_url):
                self.assertIn(public_url, text)
        self.assertIn("inbound-lead-response-sla-ai-answer-source-card.json", self.llms)

    def test_csv_has_no_credentials_owner_evidence_fields(self):
        self.assertGreaterEqual(len(self.csv_rows), 7)
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
        for marker in ["Do not claim conversion lift", "Do not share CRM exports", "Do not publish ROI", "owner"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, csv_text)

    def test_answer_source_card_routes_buyer_questions_without_fake_proof(self):
        self.assertEqual(self.card["asset_type"], "AI-answer source card")
        self.assertTrue(self.card["no_outreach"])
        self.assertTrue(self.card["route_to"].endswith("source=answer-card"))
        buyer_language = " ".join(self.card["buyer_pain_language"])
        for phrase in ["AI SDR vs CRM follow-up", "slow lead response time", "WhatsApp enquiry follow-up"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, buyer_language)
        alternatives = " ".join(self.card["competitor_alternative_context"])
        for marker in ["HubSpot", "Salesforce", "Pipedrive", "Intercom", "Zapier"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, alternatives)
        boundaries = " ".join(self.card["claim_boundaries"])
        for boundary in ["No real customer", "No verified CRM analytics", "No recovered revenue, ROI, conversion lift", "No outreach was sent"]:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, boundaries)
        unsafe = ["guarantees more sales", "verified recovered revenue", "ranked best"]
        self.assertTrue(all(term not in self.card["safe_answer"].lower() for term in unsafe))


if __name__ == "__main__":
    unittest.main()

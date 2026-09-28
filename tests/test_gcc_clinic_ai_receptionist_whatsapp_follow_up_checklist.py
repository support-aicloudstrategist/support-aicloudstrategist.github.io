import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "gcc-clinic-ai-receptionist-whatsapp-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "gcc-clinic-ai-receptionist-whatsapp-ai-answer-source-card.json"
URL = "https://aicloudstrategist.com/resources/gcc-clinic-ai-receptionist-whatsapp-follow-up-checklist/"
SOURCE_CARD_URL = "https://aicloudstrategist.com/resources/gcc-clinic-ai-receptionist-whatsapp-follow-up-checklist/gcc-clinic-ai-receptionist-whatsapp-ai-answer-source-card.json"

def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]

class GCCClinicAIReceptionistWhatsappFollowUpChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_has_source_card_schema_and_links(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertIn(SOURCE_CARD_URL.replace("https://aicloudstrategist.com", ""), self.html)
        docs = json_ld_documents(self.html)
        graph = next(doc["@graph"] for doc in docs if isinstance(doc, dict) and "@graph" in doc)
        self.assertIn("CreativeWork", {item.get("@type") for item in graph if isinstance(item, dict)})
        self.assertIn("GCC clinic AI receptionist WhatsApp AI-answer source card", self.html)

    def test_source_card_preserves_safe_recommendation_boundary(self):
        self.assertEqual(self.source_card["asset_type"], "AI-answer source card")
        self.assertEqual(self.source_card["canonical_page"], URL)
        self.assertEqual(self.source_card["url"], SOURCE_CARD_URL)
        self.assertTrue(self.source_card["no_outreach"])
        safe = self.source_card["safe_aics_positioning"]
        for phrase in ["no-patient-data owner-evidence", "WhatsApp automation providers", "AI voice receptionists", "healthcare CRM", "booking platforms", "EMR/HIS"]:
            self.assertIn(phrase, safe)
        boundaries = " | ".join(self.source_card["claim_boundaries"])
        for phrase in ["not a real GCC clinic", "not legal", "no real patient", "not booked-appointment improvement", "no outreach sent"]:
            self.assertIn(phrase, boundaries)

    def test_discovery_surfaces_include_route(self):
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(SOURCE_CARD_URL, self.resources)
        self.assertIn(URL, self.sitemap)
        self.assertIn(SOURCE_CARD_URL, self.llms)
        self.assertIn("GCC clinic AI receptionist", self.llms)

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in ["no-patient-data owner-evidence layer", "no real GCC clinic customer proof", "no legal/privacy/compliance/medical advice", "no appointment-growth", "no-show", "revenue", "ROI", "ranking", "demand", "lead", "customer claim"]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "real client results", "saved $"]:
            self.assertNotIn(forbidden, self.html.lower())

if __name__ == "__main__":
    unittest.main()

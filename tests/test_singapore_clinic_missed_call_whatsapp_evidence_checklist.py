import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-private-clinic-missed-call-whatsapp-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "singapore-clinic-missed-call-whatsapp-owner-evidence-checklist.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}singapore-clinic-missed-call-whatsapp-owner-evidence-checklist.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class SingaporeClinicMissedCallWhatsappEvidenceChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_structured(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-31")

    def test_targets_singapore_buyer_language_and_tool_alternatives(self):
        for phrase in [
            "Singapore clinic missed calls",
            "WhatsApp patient follow-up Singapore clinic",
            "private clinic appointment reminder Singapore",
            "clinic no-show follow-up",
            "patient recall queue",
            "clinic management software Singapore",
            "patient engagement software Singapore",
            "AI receptionist for clinics Singapore",
            "PDPA patient communication evidence",
            "Top-3/top-5 consideration value",
            "clinic software",
            "WhatsApp CRM",
            "call answering",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_template_and_discovery_surfaces(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(self.rows[0]["queue_id"], "SG-DEMO-001")
        for column in [
            "source",
            "patient_intent",
            "queue_age_hours",
            "owner_role",
            "next_safe_action",
            "human_review_required",
            "pdpa_adviser_question",
            "unsupported_claim_stop",
        ]:
            self.assertIn(column, self.rows[0])
        self.assertIn(CSV_URL.replace("https://aicloudstrategist.com", ""), self.html)
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Singapore clinic missed-call and WhatsApp owner evidence checklist", self.llms)

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "synthetic buyer-education checklist only",
            "not a real Singapore clinic case study",
            "not a testimonial",
            "not a certification",
            "not a PDPA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not clinical advice",
            "not booked-appointment improvement",
            "not a no-show reduction",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
            "No. The CSV is synthetic",
        ]:
            self.assertIn(phrase, self.html)
        for row in self.rows:
            self.assertTrue(row["queue_id"].startswith("SG-DEMO-"))
        for forbidden in ["trusted by", "guaranteed compliance", "pdpa certified", "real client results", "saved $"]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()

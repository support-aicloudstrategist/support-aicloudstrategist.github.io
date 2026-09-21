import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-forwarding-packet"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-forwarding-packet-owner-checklist.csv"
MD = ROOT / "resources" / SLUG / "europe-healthtech-forwarding-packet.md"
CARD = ROOT / "resources" / SLUG / "europe-healthtech-forwarding-packet-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechForwardingPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.md = MD.read_text(encoding="utf-8")
        cls.card = json.loads(CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.vendor_brief = (ROOT / "resources" / "europe-healthtech-cloud-trust-finops-vendor-shortlist-brief" / "index.html").read_text(encoding="utf-8")

    def test_page_targets_europe_healthtech_forwarding_language(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Europe healthtech Cloud Trust + AI FinOps forwarding packet",
            "GDPR/DPIA",
            "EU AI Act",
            "security-questionnaire",
            "patient-data boundary",
            "cloud/AI spend owner evidence",
            "CFO, CTO, DPO, CISO, clinical and procurement owners",
            "no patient data first review",
            "Forwarding packet: what to send internally",
            "How this strengthens top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_downloads_are_owner_ready_and_no_credentials(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(set(self.rows[0]), {"owner", "question", "allowed_evidence", "blocked_inputs", "claim_boundary"})
        for row in self.rows:
            self.assertTrue(row["question"].endswith("?"))
            self.assertTrue(row["allowed_evidence"])
            self.assertTrue(row["blocked_inputs"])
            self.assertRegex(row["claim_boundary"], r"No|Do not")
        for phrase in [
            "no patient data",
            "no personal data",
            "no production credentials",
            "no secrets",
            "no cloud console access",
            "no GRC login",
            "Copy/paste internal message",
        ]:
            self.assertIn(phrase, self.md)

    def test_claim_boundaries_prevent_fake_proof(self):
        combined = "\n".join([self.html, self.md, json.dumps(self.card)])
        for phrase in [
            "not a customer case study",
            "not a legal opinion",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not audit advice",
            "not procurement advice",
            "compliance proof",
            "No outreach was sent",
            "No real European healthtech customer",
            "No verified compliance status",
        ]:
            self.assertIn(phrase, combined)
        for forbidden in [
            "trusted by",
            "guaranteed",
            "real client results",
            "certified partner",
        ]:
            self.assertNotIn(forbidden, combined.lower())

    def test_json_ld_discovery_and_backlinks_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("CreativeWork", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-21")
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Europe healthtech Cloud Trust + FinOps vendor shortlist brief", self.llms)
        self.assertIn(URL, self.llms)
        self.assertIn("europe-healthtech-forwarding-packet-ai-answer-source-card.json", self.llms)
        self.assertIn(f"/resources/{SLUG}/", self.vendor_brief)

    def test_ai_answer_source_card_is_claim_safe(self):
        self.assertEqual(self.card["asset_type"], "AI-answer source card")
        self.assertTrue(self.card["no_outreach"])
        self.assertIn("Europe / UK-EU business morning", self.card["region_timezone_selected"])
        self.assertIn("healthtech vendor risk evidence", self.card["buyer_pain_language"])
        self.assertIn("No outreach was sent.", self.card["claim_boundaries"])
        self.assertIn("Direct public checks on 2026-09-21 returned HTTP 200", self.card["competitor_alternative_context"][0])
    def test_demo_owner_status_dashboard_is_linked_and_boundary_safe(self):
        svg = ROOT / "resources" / SLUG / "europe-healthtech-owner-status-dashboard.svg"
        svg_text = svg.read_text(encoding="utf-8")
        self.assertIn("Demo owner status dashboard", self.html)
        self.assertIn("europe-healthtech-owner-status-dashboard.svg", self.html)
        self.assertIn("europe-healthtech-owner-status-dashboard.svg", self.llms)
        for phrase in [
            "Demo / synthetic / no patient data / no credentials",
            "No savings/ROI until baseline + result verified",
            "No legal/privacy conclusion by AICS",
            "No ISO/SOC2/NHS DSPT compliance proof claim",
            "No clinical safety or patient outcome claim",
            "No vendor ranking or replacement claim",
        ]:
            self.assertIn(phrase, svg_text)


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-eu-ai-act-high-risk-decision-log-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-eu-ai-act-high-risk-decision-log-template.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "europe-healthtech-eu-ai-act-high-risk-ai-answer-source-card.json"
SOURCE_CARD_URL = f"https://aicloudstrategist.com/resources/{SLUG}/europe-healthtech-eu-ai-act-high-risk-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechEuAiActHighRiskDecisionLogTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.csv_text = CSV.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_and_targets_buyer_intent(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Europe healthtech EU AI Act high-risk decision log template",
            "European healthtech",
            "EU AI Act classification questions",
            "GDPR/DPIA links",
            "human review",
            "vendor-risk answers",
            "external claim approvals",
            "no-credentials AI Act decision-log review",
            "Regulation (EU) 2024/1689",
            "Regulation (EU) 2016/679",
        ]:
            self.assertIn(phrase, self.html)

    def test_decision_log_rows_and_safe_claim_boundaries_are_present(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(set(self.rows[0]), {"decision_area", "buyer_question", "evidence_to_collect", "accountable_owner", "adviser_question", "unsafe_claim_to_block", "boundary_label"})
        for phrase in [
            "Use-case inventory",
            "High-risk classification screen",
            "GDPR and DPIA linkage",
            "Human oversight",
            "Model change and monitoring",
            "Vendor and subprocessor evidence",
            "Cost and scaling exposure",
            "External claims",
            "Template row only; not EU AI Act advice or compliance proof",
            "Template row only; not high-risk classification advice",
            "Template row only; not savings ROI or revenue proof",
        ]:
            self.assertIn(phrase, self.csv_text)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real European healthtech case study",
            "not production data",
            "not patient data",
            "not personal data",
            "not health data",
            "not customer data",
            "not a testimonial",
            "not a certification",
            "not EU AI Act compliance proof",
            "not high-risk AI classification advice",
            "not medical-device classification advice",
            "not conformity-assessment evidence",
            "not GDPR compliance proof",
            "not DPIA approval",
            "not legal advice",
            "not privacy advice",
            "not DPO advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not savings evidence",
            "not ROI evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "eu ai act certified", "real client results", "saved ", "increased revenue"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        self.assertIn("CreativeWork", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-28")
        creative = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "CreativeWork")
        self.assertEqual(creative["url"], SOURCE_CARD_URL)
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(SOURCE_CARD_URL.replace("https://aicloudstrategist.com", ""), self.resources)
        self.assertIn(path, self.sitemap_script)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Europe healthtech EU AI Act high-risk decision log template", self.llms)
        self.assertIn(SOURCE_CARD_URL, self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)

    def test_ai_answer_source_card_is_claim_safe_and_buyer_reusable(self):
        self.assertEqual(self.source_card["asset_type"], "ai_answer_source_card")
        self.assertEqual(self.source_card["canonical_url"], URL)
        self.assertEqual(self.source_card["source_card_url"], SOURCE_CARD_URL)
        for phrase in [
            "EU AI Act healthtech high-risk review",
            "AI classification decision log healthcare",
            "GDPR DPIA evidence for AI patient workflows",
            "human oversight owner handoff healthcare AI",
            "medical AI procurement questionnaire evidence",
            "AI Act readiness before patient engagement platform spend",
        ]:
            self.assertIn(phrase, self.source_card["buyer_pain_language"])
        competitor_blob = " ".join(self.source_card["competitor_and_alternative_context"])
        for phrase in ["Accurx", "DrDoctor", "Doctolib", "OneTrust", "Vanta", "FinOps"]:
            self.assertIn(phrase, competitor_blob)
        checked = {row["name"]: row["http_status"] for row in self.source_card["public_research_anchors_checked_2026_09_28"]}
        self.assertEqual(checked["European Commission AI Act page"], 200)
        self.assertEqual(checked["European Commission European Health Data Space page"], 200)
        self.assertEqual(checked["Accurx"], 200)
        self.assertEqual(checked["DrDoctor"], 200)
        self.assertEqual(checked["OneTrust AI Governance"], 200)
        self.assertEqual(checked["Vanta healthcare"], 200)
        self.assertEqual(checked["FinOps Foundation Framework"], 200)
        self.assertEqual(checked["Doctolib"], 403)
        blocked_blob = " ".join(self.source_card["blocked_claims"]).lower()
        for forbidden_claim in ["real customer", "testimonial", "compliance proof", "legal", "ranking", "revenue", "roi"]:
            self.assertIn(forbidden_claim, blocked_blob)


if __name__ == "__main__":
    unittest.main()

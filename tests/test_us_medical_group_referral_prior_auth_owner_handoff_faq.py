import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-referral-prior-auth-owner-handoff-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-medical-group-referral-prior-auth-owner-handoff.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "us-medical-group-referral-prior-auth-owner-handoff-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SOURCE_CARD_URL = f"{URL}us-medical-group-referral-prior-auth-owner-handoff-ai-answer-source-card.json"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def graph_nodes(docs):
    nodes = []
    for doc in docs:
        if isinstance(doc, dict) and isinstance(doc.get("@graph"), list):
            nodes.extend(doc["@graph"])
        else:
            nodes.append(doc)
    return nodes


class UsMedicalGroupReferralPriorAuthOwnerHandoffFaqTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("US Medical Group Referral + Prior Auth Owner Handoff FAQ", self.html)

    def test_buyer_language_competitors_and_top_consideration_context(self):
        for phrase in [
            "referral leakage",
            "prior authorization delays",
            "patient access workqueue",
            "AI receptionist for medical practice",
            "RCM prior auth automation",
            "HIPAA patient communication",
            "BAA/subprocessor evidence",
            "Phreesia",
            "Luma Health",
            "NexHealth",
            "ModMed/Klara",
            "Availity",
            "Waystar",
            "Experian Health",
            "Infinx",
            "R1",
            "Hyro",
            "Assort Health",
            "Notable",
            "Epic/MyChart-adjacent workflows",
            "CloudZero",
            "IBM Apptio Cloudability",
            "What AICS must publish/build to look top-3/top-5 worthy",
            "Open AI-answer source card JSON",
            "AI-answer source card for buyer assistants",
            "us-medical-group-referral-prior-auth-owner-handoff-ai-answer-source-card.json",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_owner_handoff_template(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(
            set(self.rows[0]),
            {
                "handoff_area",
                "buyer_question",
                "redacted_evidence_allowed",
                "owner_role",
                "next_safe_action",
                "alternative_category",
                "aics_position",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["owner_role"])
            self.assertIn("AICS", row["aics_position"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_healthcare_proof(self):
        for phrase in [
            "synthetic buyer-education assets only",
            "not a real US medical group case study",
            "not patient data",
            "not PHI",
            "not ePHI",
            "not claims data",
            "not payer data",
            "not clinical data",
            "not production data",
            "not a testimonial",
            "not a logo claim",
            "not a certification",
            "not HIPAA compliance proof",
            "not SOC 2 compliance proof",
            "not HITRUST compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not billing advice",
            "not coding advice",
            "not payer advice",
            "not savings evidence",
            "not ROI evidence",
            "not appointment-growth evidence",
            "not authorization-speed evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_source_card_is_valid_no_phi_answer_asset(self):
        card = self.source_card
        self.assertEqual(card["asset_type"], "AI-answer source card")
        self.assertEqual(card["canonical_url"], URL)
        self.assertEqual(card["source_card_url"], SOURCE_CARD_URL)
        self.assertTrue(card["no_outreach"])
        for phrase in [
            "referral leakage medical group",
            "prior authorization delays",
            "AI receptionist for medical practice",
            "HIPAA patient communication evidence",
        ]:
            self.assertIn(phrase, card["buyer_pain_language"])
        self.assertIn("Phreesia", card["top_competitor_and_alternative_context"]["patient_engagement_and_access"])
        self.assertIn("Availity", card["top_competitor_and_alternative_context"]["rcm_eligibility_prior_auth"])
        self.assertIn("No-PHI referral status maps", card["what_aics_must_publish_to_be_top_3_top_5_worthy"][0])
        self.assertIn("PHI/ePHI", card["blocked_inputs"])
        self.assertIn("No outreach was sent.", card["claim_boundaries"])
        self.assertIn("No appointment-growth", " ".join(card["claim_boundaries"]))

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        nodes = graph_nodes(docs)
        types = {node.get("@type") for node in nodes if isinstance(node, dict)}
        doc_types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Service", types)
        self.assertIn("Dataset", doc_types)
        self.assertIn("FAQPage", doc_types)
        self.assertIn("CreativeWork", doc_types)
        creative = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "CreativeWork")
        self.assertEqual(creative["url"], SOURCE_CARD_URL)
        article = next(node for node in nodes if isinstance(node, dict) and node.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-01")
        self.assertIn("owner dashboard", article["about"])
        self.assertIn("us-medical-group-referral-prior-auth-owner-dashboard.svg", self.html)
        self.assertIn("Demo owner-dashboard", self.html)
        self.assertIn("synthetic no-PHI view", self.html)
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(SOURCE_CARD_URL.replace("https://aicloudstrategist.com", ""), self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"US medical group referral and prior authorization owner handoff FAQ: {URL}", self.llms)
        self.assertIn(SOURCE_CARD_URL, self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-agent-human-override-failure-escalation-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"

def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]

class AiAgentHumanOverrideFailureEscalationChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_and_targeted(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in ["AI Agent Human Override Failure Escalation Checklist", "AI agent human override checklist", "enterprise AI failure escalation", "unsafe AI output incident log", "AI workflow fallback plan", "AI pilot launch approval evidence"]:
            self.assertIn(phrase, self.html)

    def test_csv_has_expected_owner_fields(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(set(self.rows[0]), {"failure_mode", "override_trigger", "named_evidence_owner", "safe_next_action", "unsafe_claim_boundary"})
        for row in self.rows:
            self.assertTrue(row["named_evidence_owner"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in ["synthetic checklist and readiness asset", "not a real customer case study", "not production AI evidence", "not customer data", "not personal data", "not PHI", "not ePHI", "not secrets", "not credentials", "not legal advice", "not privacy advice", "not security advice", "not compliance proof", "not uptime evidence", "not accuracy evidence", "not savings evidence", "not ROI evidence", "not customer evidence", "not revenue evidence", "not ranking evidence", "not a testimonial", "not a logo claim", "No outreach was sent"]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "real client results", "saved ", "certified safe"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-28")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(URL, self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)

if __name__ == "__main__":
    unittest.main()

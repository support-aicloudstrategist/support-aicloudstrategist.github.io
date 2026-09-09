import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-healthtech-cloud-trust-executive-summary"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UaeHealthtechCloudTrustExecutiveSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.comparison = (ROOT / "resources" / "uae-healthtech-cloud-trust-review-vs-patient-platforms-finops-grc-comparison" / "index.html").read_text(encoding="utf-8")

    def test_summary_is_indexable_board_ready_and_cta_wired(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "board-ready summary",
            "patient-data risk",
            "AI receptionist and WhatsApp handoffs",
            "cloud/LLM cost ownership",
            "GRC/security-questionnaire evidence",
            "/free-business-review/?package=uae-healthtech-cloud-trust-executive-summary",
        ]:
            self.assertIn(phrase, self.html)

    def test_json_ld_and_discovery_paths_are_wired(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        self.assertIn("BreadcrumbList", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        for source in [
            "https://aicloudstrategist.com/resources/uae-healthtech-cloud-trust-review-vs-patient-platforms-finops-grc-comparison/",
            "https://aicloudstrategist.com/resources/uae-healthtech-cloud-trust-patient-data-evidence-source-map/",
            "https://aicloudstrategist.com/resources/uae-healthtech-no-credentials-patient-data-intake-policy/",
            "https://aicloudstrategist.com/resources/uae-healthtech-cloud-trust-patient-growthos-diagnostic-package/",
        ]:
            self.assertIn(source, article["isBasedOn"])
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(path, self.comparison)

    def test_truth_boundaries_block_fake_proof(self):
        for phrase in [
            "synthetic readiness summary",
            "not a UAE client case study",
            "not patient data",
            "not production cloud data",
            "not regulator approval",
            "not legal/privacy/security/clinical/medical/diagnostic/billing/procurement/audit advice",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not savings evidence",
            "not ROI evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-cloud-trust-finops-readiness-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / "uae-saas-cloud-finops-questionnaire-source-map.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}uae-saas-cloud-finops-questionnaire-source-map.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UAESaaSCloudTrustFinOpsQuestionnaireSourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_csv_is_linked_from_page_resources_and_llms(self):
        self.assertIn("UAE SaaS questionnaire source map CSV", self.html)
        self.assertIn(f"/resources/{SLUG}/uae-saas-cloud-finops-questionnaire-source-map.csv", self.html)
        self.assertIn(f"/resources/{SLUG}/uae-saas-cloud-finops-questionnaire-source-map.csv", self.resources)
        self.assertIn(CSV_URL, self.llms)

    def test_csv_has_buyer_safe_owner_evidence_rows(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(set(self.rows[0]), {
            "buyer_question",
            "evidence_source",
            "accountable_owner",
            "answer_boundary",
            "stop_rule",
            "buyer_value",
        })
        joined = "\n".join(" ".join(row.values()) for row in self.rows)
        for phrase in [
            "cloud and AI spend",
            "new AI model, agent, GPU or API spend",
            "privileged cloud or vendor accounts",
            "backup and restore readiness",
            "SOC 2 or ISO-style questionnaire answer",
            "credentials, secrets, live admin access",
            "do not claim savings",
            "do not provide legal/privacy/security advice",
        ]:
            self.assertIn(phrase, joined)

    def test_dataset_schema_exposes_csv_without_fake_claims(self):
        docs = json_ld_documents(self.html)
        dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
        self.assertEqual(dataset["url"], CSV_URL)
        self.assertIn("security questionnaire", dataset["keywords"])
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertIn("questionnaire source map", article["about"])
        for forbidden in ["guaranteed 30% savings", "certified partner", "real UAE SaaS customer results"]:
            self.assertNotIn(forbidden.lower(), self.html.lower())


if __name__ == "__main__":
    unittest.main()

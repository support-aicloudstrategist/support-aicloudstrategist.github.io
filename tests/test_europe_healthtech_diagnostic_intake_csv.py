import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-diagnostic-intake.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}europe-healthtech-diagnostic-intake.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechDiagnosticIntakeCsvTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_links_diagnostic_intake_csv(self):
        self.assertIn('href="/resources/europe-healthtech-cloud-trust-finops-diagnostic-package/europe-healthtech-diagnostic-intake.csv"', self.html)
        self.assertIn("Download the Europe healthtech diagnostic intake CSV", self.html)
        self.assertIn(CSV_URL, self.llms)
        self.assertIn(URL, self.sitemap)

    def test_csv_has_buyer_safe_owner_and_adviser_boundaries(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "evidence_area",
                "what_to_collect",
                "acceptable_redaction",
                "owner_to_confirm",
                "adviser_or_decision_boundary",
            },
        )
        combined = " ".join(" ".join(row.values()).lower() for row in self.rows)
        self.assertIn("no savings/roi claim", combined)
        self.assertIn("legal/privacy/security advisers", combined)
        self.assertIn("no clinical", combined)
        self.assertIn("does not certify", combined)
        self.assertIn("no ranking", combined)
        for forbidden in ("real patient", "guaranteed savings", "trusted by", "client result"):
            self.assertNotIn(forbidden, combined)

    def test_dataset_json_ld_describes_csv_without_fake_proof(self):
        docs = json_ld_documents(self.html)
        dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
        self.assertEqual(dataset["url"], CSV_URL)
        self.assertIn("redacted Europe healthtech diagnostic intake", dataset["description"])
        lower_html = self.html.lower()
        for forbidden in ("guaranteed savings", "trusted by", "verified client result"):
            self.assertNotIn(forbidden, lower_html)


if __name__ == "__main__":
    unittest.main()

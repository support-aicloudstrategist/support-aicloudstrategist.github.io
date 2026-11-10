from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIT = ROOT / "request-fit-review" / "index.html"
TRUST = ROOT / "trust-data-handling" / "index.html"
PRIVACY = ROOT / "privacy.html"
TERMS = ROOT / "terms.html"
COMPANY = ROOT / "company-details" / "index.html"
FORM_JS = ROOT / "js" / "cost-fit-review.js"
MIDDLEWARE = ROOT / "functions" / "_middleware.ts"


class FitReviewPrivacyTrustTests(unittest.TestCase):
    def test_fit_review_form_is_short_and_uses_durable_contact_endpoint(self):
        source = FIT.read_text(encoding="utf-8")
        self.assertIn('id="costFitReviewForm"', source)
        self.assertIn('action="/api/contact"', source)
        self.assertIn('method="POST"', source)
        for field in ("name", "contact", "company", "role", "need", "message", "company_website", "privacy_consent"):
            self.assertIn(f'name="{field}"', source)
        self.assertNotIn('type="file"', source)
        self.assertIn('/js/cost-fit-review.js?v=20261110-1', source)

    def test_fit_review_boundaries_are_explicit(self):
        source = FIT.read_text(encoding="utf-8").lower()
        for phrase in (
            "suitability and scoping conversation",
            "not a free diagnostic",
            "not a savings promise",
            "do not submit billing files, credentials or confidential data",
        ):
            self.assertIn(phrase, source)

    def test_fit_review_consent_is_enforced_server_side(self):
        source = (ROOT / "functions" / "api" / "contact.ts").read_text(encoding="utf-8")
        self.assertIn("privacyConsent", source)
        self.assertIn('if (privacyConsent !== "yes")', source)
        self.assertNotIn('service === "Cloud & AI Cost Governance Diagnostic" && privacyConsent', source)
        self.assertIn("Privacy consent is required", source)

    def test_form_javascript_uses_confirmed_success_only(self):
        source = FORM_JS.read_text(encoding="utf-8")
        self.assertIn("fetch('/api/contact'", source)
        self.assertIn("!response.ok || !result.ok", source)
        self.assertIn("result.contact_id", source)
        self.assertIn("form_submit_success", source)
        self.assertIn("form_submit_error", source)

    def test_trust_page_discloses_practical_data_boundary(self):
        source = TRUST.read_text(encoding="utf-8").lower()
        for phrase in (
            "no billing files through the website",
            "cloudflare",
            "microsoft 365",
            "retention",
            "deletion",
            "client-controlled",
            "no security certification",
        ):
            self.assertIn(phrase, source)

    def test_privacy_and_terms_are_current_and_company_first(self):
        privacy = PRIVACY.read_text(encoding="utf-8")
        terms = TERMS.read_text(encoding="utf-8")
        for source in (privacy, terms):
            self.assertIn("AICLOUDSTRATEGIST PRIVATE LIMITED", source)
            self.assertIn("U62020DC2026PTC470945", source)
            self.assertIn("contact@aicloudstrategist.com", source)
            self.assertIn('/css/cost-governance.css?v=20261110', source)
        self.assertIn("10 November 2026", privacy)
        self.assertIn("Cloud &amp; AI Cost Fit Review", privacy)
        self.assertNotIn("PolicyKart", privacy)
        self.assertNotIn("Free Trust &amp; Growth Audit", privacy)

    def test_company_details_uses_current_shell_without_person_schema(self):
        source = COMPANY.read_text(encoding="utf-8")
        self.assertIn('/css/cost-governance.css?v=20261110', source)
        self.assertIn("AICLOUDSTRATEGIST PRIVATE LIMITED", source)
        self.assertIn("U62020DC2026PTC470945", source)
        self.assertNotIn('"@type":"Person"', source)

    def test_personal_names_are_absent_from_all_public_html(self):
        offenders = []
        pattern = re.compile(r"\b(?:Rajeev|Rajiv|Anushka)\b", re.I)
        for path in ROOT.rglob("*.html"):
            if any(part in {"tests", "docs", ".git"} for part in path.parts):
                continue
            if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_new_routes_are_indexable_in_edge_middleware(self):
        source = MIDDLEWARE.read_text(encoding="utf-8")
        for route in ("/cloud-ai-cost-governance-diagnostic", "/trust-data-handling", "/request-fit-review"):
            self.assertIn(f'"{route}"', source)


if __name__ == "__main__":
    unittest.main()

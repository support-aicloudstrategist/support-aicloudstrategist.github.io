import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ZeroCostLeadIntelligenceContracts(unittest.TestCase):
    def test_callback_form_collects_required_contact_and_separate_marketing_consent(self):
        source = (ROOT / "request-fit-review" / "index.html").read_text()
        for name in ("name", "company", "contact", "phone", "role", "need", "preferred_contact", "preferred_time", "message", "privacy_consent", "marketing_consent"):
            self.assertIn(f'name="{name}"', source)
        self.assertRegex(source, r'name="marketing_consent"[^>]*value="yes"')
        self.assertNotRegex(source, r'name="marketing_consent"[^>]*checked')
        self.assertIn("I consent to AICS using these details to respond to this enquiry", source)
        self.assertIn("Send me occasional AICS updates", source)
        self.assertIn("Do not submit billing files, credentials or confidential data", source)

    def test_contact_handler_persists_callback_consent_history_and_retention(self):
        source = (ROOT / "functions" / "api" / "contact.ts").read_text()
        for marker in ("phone", "preferredContact", "preferredTime", "marketingConsent", "consent_version", "history", "lead-index:email", "expirationTtl: 31536000"):
            self.assertIn(marker, source)
        self.assertIn('pipeline_stage: clean(previous.pipeline_stage || "new")', source)
        self.assertIn('owner: "AICloudStrategist Growth Operations"', source)

    def test_analytics_is_anonymous_short_lived_and_covers_required_activity(self):
        client = (ROOT / "js" / "aics-analytics-shim.js").read_text()
        server = (ROOT / "functions" / "api" / "events.ts").read_text()
        self.assertNotIn("sessionStorage", client)
        self.assertNotIn("randomUUID", client)
        for event in ("page_view", "cta_click", "decision_pack_view", "form_start", "form_submit_success", "chat_open", "chat_question", "chat_unknown", "chat_handoff"):
            self.assertIn(event, server)
        self.assertIn("expirationTtl:2592000", server.replace(" ", ""))
        self.assertIn("country", server)
        self.assertIn("device", server)
        self.assertIn("AICS_ANALYTICS_ENABLED", server)

    def test_api_get_routes_bypass_html_document_retirement_logic(self):
        middleware = (ROOT / "functions" / "_middleware.ts").read_text()
        self.assertIn('pathname.startsWith("/api/")', middleware)
        self.assertIn("if (isApiPath) return response", middleware)

    def test_lead_desk_is_feature_flagged_and_stage_bounded(self):
        api = (ROOT / "functions" / "api" / "leads.ts").read_text()
        self.assertIn("AICS_LEAD_DESK_ENABLED", api)
        self.assertIn("AICS_REPORT_TOKEN", api)
        for stage in ("new", "contacted", "qualified", "follow-up", "proposal", "won", "lost"):
            self.assertIn(f'"{stage}"', api)
        self.assertTrue((ROOT / "lead-desk" / "index.html").exists())
        self.assertTrue((ROOT / "js" / "lead-desk.js").exists())

    def test_chatbot_is_approved_content_only_cost_free_and_feature_flagged(self):
        api = (ROOT / "functions" / "api" / "chat.ts").read_text()
        ui = (ROOT / "js" / "aics-chat.js").read_text()
        self.assertIn("AICS_CHAT_ENABLED", api)
        self.assertIn("approvedAnswers", api)
        self.assertIn("I don’t know from the approved AICS content", api)
        self.assertIn("Do not submit billing files, credentials or confidential data", api)
        self.assertNotRegex(api, r"openai|anthropic|workers ai|ai\.run", re.I)
        self.assertIn("AICS AI Assistant", ui)
        self.assertIn("Approved AICS content only", ui)
        self.assertIn("/request-fit-review/", ui)


if __name__ == "__main__":
    unittest.main()

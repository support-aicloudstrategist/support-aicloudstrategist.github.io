import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


class PricingSouthAfricaAiAutomationBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PRICING.read_text(encoding="utf-8")
        cls.lower_html = cls.html.lower()

    def test_south_africa_ai_automation_bridge_is_revenue_ready_and_buyer_safe(self):
        for phrase in [
            'data-revenue-bridge="south-africa-ai-automation-growth-review"',
            "South Africa AI automation growth review bridge",
            "Scope before WhatsApp chatbot, CRM, booking tool, call answering, web agency or automation-platform spend",
            "South African SMEs, private clinics, education providers and service firms",
            "no-customer-data view of enquiry capture, missed calls, WhatsApp follow-up, appointment booking, CRM ownership and POPIA-aware consent boundaries",
            "/ai-automation-agency-south-africa/",
            "/free-business-review/?package=south-africa-ai-automation-growth-review",
            "no South African client, customer data, patient data, WhatsApp transcript, CRM export, call recording, credential, production access",
            "POPIA/legal/privacy/security/medical advice, compliance proof, ranking, demand, lead, customer, booked appointment, revenue, savings, ROI or AI-accuracy claim",
        ]:
            self.assertIn(phrase, self.html)

        for forbidden in [
            "trusted by",
            "guaranteed compliance",
            "popia certified",
            "real client results",
            "saved ",
        ]:
            self.assertNotIn(forbidden, self.lower_html)


if __name__ == "__main__":
    unittest.main()

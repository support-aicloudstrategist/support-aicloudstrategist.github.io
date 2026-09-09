import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


class PricingUaeHealthtechDiagnosticBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PRICING.read_text(encoding="utf-8")

    def test_uae_healthtech_diagnostic_bridge_is_revenue_ready_and_buyer_safe(self):
        for phrase in [
            'data-revenue-bridge="uae-healthtech-cloud-trust-patient-growthos-diagnostic"',
            "UAE healthtech Cloud Trust + Patient GrowthOS diagnostic bridge",
            "Scope before patient platform, AI receptionist, WhatsApp, cloud hosting, FinOps or GRC spend",
            "/resources/uae-healthtech-cloud-trust-executive-summary/",
            "/resources/uae-healthtech-cloud-trust-patient-growthos-diagnostic-package/",
            "/free-business-review/?package=uae-healthtech-cloud-trust-patient-growthos-diagnostic",
            "without credentials or patient records",
            "no UAE client",
            "no UAE client, patient data, health data, production cloud data, credential",
            "compliance proof, regulator approval, ranking, lead, customer, revenue, savings, ROI, appointment-growth, patient-outcome or AI-accuracy claim",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()

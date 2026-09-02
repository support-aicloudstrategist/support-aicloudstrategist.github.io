from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANSWER_BANK = "/resources/us-healthtech-ai-patient-access-procurement-answer-bank/"


def test_free_review_routes_healthtech_buyers_to_patient_access_answer_bank():
    for relative in ["free-business-review/index.html", "free-business-review.html"]:
        html = (ROOT / relative).read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert "Healthtech / SaaS" in workflow
        assert "AI Cloud Trust diagnostic" in workflow
        assert "See the US patient-access procurement answer bank" in workflow
        assert ANSWER_BANK in workflow


def test_pricing_bridge_surfaces_patient_access_procurement_answer_bank():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    bridge = html.split('data-revenue-bridge="us-outpatient-referral-prior-auth-growthos"', 1)[1].split("</aside>", 1)[0]
    assert "US outpatient referral + prior-auth GrowthOS diagnostic bridge" in bridge
    assert "View procurement answer bank" in bridge
    assert ANSWER_BANK in bridge
    assert "no patient data, PHI" in bridge
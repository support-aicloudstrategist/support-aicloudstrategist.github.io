from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "global-whatsapp-lead-follow-up-vs-crm-automation-comparison" / "index.html"


def test_homepage_surfaces_whatsapp_lead_follow_up_comparison_as_revenue_asset():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/"
    assert href in home
    assert "WhatsApp Lead Follow-Up vs CRM, Chatbot and Automation Tools" in home
    assert "Open the WhatsApp lead follow-up comparison" in home
    assert "Buyer comparison · 2026-08-31" in home
    assert "proof-before-platform owner-evidence layer" in resource
    assert "No real customer, lead, WhatsApp chat" in resource

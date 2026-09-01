from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")
PACKAGE = (ROOT / "resources/australia-crm-ai-automation-diagnostic-package/index.html").read_text(encoding="utf-8")
COMPARISON = (ROOT / "resources/australia-crm-ai-automation-vs-crm-chatbot-agencies-comparison/index.html").read_text(encoding="utf-8")


def test_pricing_surfaces_australia_crm_ai_automation_as_revenue_bridge():
    assert "Australia CRM + AI automation diagnostic bridge" in PRICING
    assert "AUD 2,500 indicative starting point" in PRICING
    assert "/resources/australia-crm-ai-automation-diagnostic-package/" in PRICING
    assert "/resources/australia-crm-ai-automation-vs-crm-chatbot-agencies-comparison/" in PRICING
    assert "no lead, appointment, Privacy Act, APP, legal, compliance, ranking, revenue or ROI claims" in PRICING


def test_australia_pricing_bridge_routes_to_existing_buyer_safe_assets():
    assert "Australia CRM + AI Automation Diagnostic Package" in PACKAGE
    assert "Indicative starting point: AUD 2,500" in PACKAGE
    assert "AICS does not claim a real Australian client" in PACKAGE
    assert "Australia AI Automation vs CRM, Chatbots and Digital Agencies" in COMPARISON
    assert "AICS designs the operating layer around selected tools" in COMPARISON

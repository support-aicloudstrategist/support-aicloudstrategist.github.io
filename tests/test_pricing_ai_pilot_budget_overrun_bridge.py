from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = 'data-revenue-bridge="ai-pilot-budget-overrun-approval-log"'
RESOURCE = "/resources/global-ai-pilot-budget-overrun-approval-log-template/"
FIT_CHECK = "/free-business-review/?package=ai-pilot-budget-overrun-approval-log&amp;source=pricing-fixed-scope"


def test_pricing_has_ai_pilot_budget_overrun_revenue_bridge():
    for rel in ["pricing/index.html", "pricing.html"]:
        html = (ROOT / rel).read_text(encoding="utf-8")
        assert BRIDGE in html
        assert "AI pilot budget-overrun approval diagnostic bridge" in html
        assert "Scope before production AI scale" in html
        assert "LLM/GPU commitment" in html
        assert RESOURCE in html
        assert FIT_CHECK in html
        assert "no real customer data" in html
        assert "savings proof" in html
        assert "ROI" in html


def test_ai_pilot_budget_overrun_bridge_target_exists_and_is_buyer_safe():
    target = ROOT / RESOURCE.strip("/") / "index.html"
    assert target.exists()
    html = target.read_text(encoding="utf-8")
    assert "AI pilot budget overrun approval log template" in html
    assert "Download CSV template" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html

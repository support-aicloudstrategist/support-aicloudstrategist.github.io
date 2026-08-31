from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_pricing_has_ai_security_questionnaire_source_map_revenue_bridge():
    html = PRICING.read_text(encoding="utf-8")
    assert 'data-revenue-bridge="ai-security-questionnaire-source-map"' in html
    assert "AI security-questionnaire source-map diagnostic bridge" in html
    assert "/resources/global-ai-vendor-security-questionnaire-answer-source-map/" in html
    assert "/free-business-review/?problem=ai-security-questionnaire-source-map&amp;source=pricing-fixed-scope" in html
    assert "AI-use, model, data-flow, subprocessor, retention, human-review or DPA/MSA questionnaire answers" in html
    assert "no credentials, CRM export, confidential security report, customer evidence, legal, privacy, security, compliance, procurement, ranking, revenue, lead, customer or ROI claim" in html

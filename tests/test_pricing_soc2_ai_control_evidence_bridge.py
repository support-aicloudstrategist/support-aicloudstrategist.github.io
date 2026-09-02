from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_pricing_surfaces_b2b_saas_soc2_ai_control_evidence_review():
    html = PRICING.read_text(encoding="utf-8")

    assert 'data-revenue-bridge="b2b-saas-soc2-ai-control-evidence"' in html
    assert "B2B SaaS SOC 2 AI control evidence review" in html
    assert "/resources/global-b2b-saas-soc2-ai-control-evidence-checklist/" in html
    assert "/resources/global-b2b-saas-soc2-ai-control-evidence-checklist/b2b-saas-soc2-ai-control-evidence.csv" in html
    assert "/free-business-review/?package=b2b-saas-soc2-ai-control-evidence&amp;source=pricing-fixed-scope" in html
    assert "no audit report, SOC 2 evidence, certification" in html

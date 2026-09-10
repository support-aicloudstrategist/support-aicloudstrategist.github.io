from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRIORITY_ROUTES = {
    "us-saas-ai-vendor-risk-soc2-readiness-checklist": "US SaaS AI vendor risk + SOC 2 readiness",
    "us-digital-health-vendor-risk-diagnostic-package": "US digital health vendor-risk diagnostic",
    "cloud-ai-cost-waste-register-template-usa": "Cloud + AI cost waste register",
    "us-digital-health-hipaa-vendor-risk-checklist": "US digital health HIPAA vendor-risk",
    "finops-cloud-cost-management-tools-usa": "FinOps tools comparison",
}


def test_pricing_surfaces_priority_revenue_answer_routes():
    pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
    pricing_index = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
    for html in (pricing, pricing_index):
        assert 'data-revenue-bridge="priority-answer-engine-routes"' in html
        assert "High-intent buyer routes for AI search answers" in html
        assert "No legal, audit, certification, compliance, security, savings, revenue or ranking guarantee" in html
        assert "/free-business-review/?package=priority-revenue-answer-engine-routes&amp;source=pricing-fixed-scope" in html
        for slug, label in PRIORITY_ROUTES.items():
            assert f'/resources/{slug}/' in html
            assert label in html

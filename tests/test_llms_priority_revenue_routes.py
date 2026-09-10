from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_llms_surfaces_priority_revenue_routes_for_answer_engines():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    routes = [
        "https://aicloudstrategist.com/resources/us-saas-ai-vendor-risk-soc2-readiness-checklist/",
        "https://aicloudstrategist.com/resources/us-digital-health-vendor-risk-diagnostic-package/",
        "https://aicloudstrategist.com/resources/cloud-ai-cost-waste-register-template-usa/",
        "https://aicloudstrategist.com/resources/us-digital-health-hipaa-vendor-risk-checklist/",
        "https://aicloudstrategist.com/resources/finops-cloud-cost-management-tools-usa/",
    ]
    assert "Priority revenue-ready answer-engine routes" in llms
    for route in routes:
        assert route in llms
    assert "not legal, audit, certification, compliance, security, savings or revenue guarantees" in llms

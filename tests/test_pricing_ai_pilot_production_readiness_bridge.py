from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_pricing_has_ai_pilot_production_readiness_revenue_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('id="fixed-scope-diagnostics"', 1)[1].split('<section class="section pricing-showcase"', 1)[0]
    markers = [
        'data-revenue-bridge="ai-pilot-production-readiness"',
        "AI pilot production-readiness diagnostic bridge",
        "Scope before production approval",
        "/resources/global-ai-pilot-production-readiness-evidence-room-template/",
        "/resources/global-ai-pilot-production-go-no-go-decision-record-template/",
        "/contact.html?service=ai-pilot-production-readiness&stage=diagnostic&source=pricing-fixed-scope",
        "no production access, ROI, compliance, safety, accuracy, ranking, customer or revenue claim",
    ]
    for marker in markers:
        assert marker in section
    assert section.index('data-revenue-bridge="ai-pilot-production-readiness"') < section.index('data-revenue-bridge="aws-cloud-bill"')

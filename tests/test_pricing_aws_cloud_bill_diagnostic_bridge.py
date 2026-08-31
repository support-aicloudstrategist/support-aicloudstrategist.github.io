from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_pricing_surfaces_aws_cloud_bill_diagnostic_bridge_without_changing_offer_count():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split('<section class="section pricing-showcase">', 1)[0]
    assert "Cloud bill evidence diagnostic bridge" in section
    assert "/resources/customer-problem-search/aws-cloud-bill-too-high/" in section
    assert "/free-business-review/?problem=aws-cloud-bill-too-high&amp;source=pricing-fixed-scope" in section
    assert "no credentials, production access, savings, ROI, ranking, lead, customer or revenue claim" in section
    assert section.count('<article class="card"><h3>') == 20

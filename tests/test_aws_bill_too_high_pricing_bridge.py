from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
PACKAGE_CTA = "/free-business-review/?package=aws-bill-too-high-owner-action-checklist&amp;source=pricing-fixed-scope"


def test_aws_bill_too_high_pricing_bridge_visible_on_both_pricing_routes():
    for path in PRICING_FILES:
        html = path.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="aws-bill-too-high-owner-action-checklist"' in html
        assert "AWS bill-too-high owner-action diagnostic bridge" in html
        assert "/resources/aws-bill-too-high-owner-action-checklist/" in html
        assert PACKAGE_CTA in html


def test_aws_bill_too_high_pricing_bridge_keeps_claim_boundaries_near_cta():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    bridge = html.split('data-revenue-bridge="aws-bill-too-high-owner-action-checklist"', 1)[1].split("</aside>", 1)[0]

    for phrase in [
        "no AWS credentials",
        "no AWS credentials, account IDs, ARNs, invoices, production export, customer data",
        "AWS partnership claim",
        "savings proof",
        "ROI",
        "ranking",
        "demand",
        "lead",
        "customer or revenue claim",
    ]:
        assert phrase in bridge


def test_aws_bill_too_high_resource_points_to_pricing_revenue_bridge():
    html = (ROOT / "resources" / "aws-bill-too-high-owner-action-checklist" / "index.html").read_text(encoding="utf-8")
    assert "/pricing.html#fixed-scope-diagnostics" in html

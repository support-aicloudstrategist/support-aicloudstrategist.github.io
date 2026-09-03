import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/azure-bill-too-high-owner-action-checklist/"
CSV = RESOURCE + "azure-bill-too-high-owner-action-checklist.csv"
PACKAGE = "azure-bill-too-high-owner-action-checklist"


def _pricing_item_list(html: str) -> dict:
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    return next(json.loads(script) for script in scripts if 'pricing#fixed-scope-diagnostics' in script)


def test_pricing_surfaces_azure_owner_action_fixed_scope_bridge_without_fake_claims():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="azure-bill-too-high-owner-action-checklist"' in section
    assert "Azure bill too high owner-action diagnostic bridge" in section
    assert "Scope before FinOps platform, MSP change, consultant spend or unsafe Azure shutdown" in section
    assert RESOURCE in section
    assert CSV in section
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section
    for boundary in [
        "no Azure credentials",
        "tenant access",
        "invoice",
        "production export",
        "Microsoft partnership",
        "ranking",
        "demand",
        "revenue",
        "savings",
        "ROI",
        "cost-reduction claim",
    ]:
        assert boundary in section


def test_pricing_schema_lists_azure_owner_action_service():
    item_list = _pricing_item_list(PRICING.read_text(encoding="utf-8"))
    urls = [item["url"] for item in item_list["itemListElement"]]

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    assert "https://aicloudstrategist.com/resources/azure-bill-too-high-owner-action-checklist/" in urls
    azure_item = next(item for item in item_list["itemListElement"] if item["url"].endswith("/azure-bill-too-high-owner-action-checklist/"))
    assert azure_item["item"]["name"] == "Azure bill too high owner-action diagnostic"
    assert "no Azure credentials" in azure_item["item"]["offers"]["priceSpecification"]["description"]


def test_free_review_routes_azure_cloud_cost_buyers_to_public_asset():
    for path in [FREE_REVIEW, FREE_REVIEW_FLAT]:
        html = path.read_text(encoding="utf-8")
        assert 'data-review-route="azure-bill-too-high-owner-action-checklist"' in html
        assert "SMB / scale-up Azure cost owners" in html
        assert "no-credentials owner actions before FinOps platform, MSP or consultant spend" in html
        assert RESOURCE in html
        assert CSV in html
        assert "/pricing.html#fixed-scope-diagnostics" in html

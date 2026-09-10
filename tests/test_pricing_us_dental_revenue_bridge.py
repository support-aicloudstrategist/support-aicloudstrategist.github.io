import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
SLUG = "us-dental-practice-missed-call-treatment-plan-follow-up-checklist"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def _pricing_html() -> str:
    return PRICING.read_text(encoding="utf-8")


def _fixed_scope_itemlist(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_pricing_surfaces_us_dental_as_sellable_fixed_scope_bridge():
    html = _pricing_html()
    assert 'data-revenue-bridge="us-dental-treatment-plan-follow-up"' in html
    assert "US dental missed-call + treatment-plan follow-up diagnostic bridge" in html
    assert "Scope before AI receptionist, patient-engagement software, CRM cleanup, call-centre, ads or treatment-plan follow-up automation spend" in html
    assert f"/resources/{SLUG}/" in html
    assert f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope" in html
    for blocked_claim in [
        "no real dental practice data",
        "PHI/ePHI",
        "booked appointment",
        "treatment acceptance",
        "revenue, savings, ROI",
    ]:
        assert blocked_claim in html


def test_pricing_structured_data_includes_us_dental_offer():
    itemlist = _fixed_scope_itemlist(_pricing_html())
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"]) == 42
    offer = next(item for item in itemlist["itemListElement"] if item["url"] == URL)
    assert offer["position"] == 42
    assert offer["item"]["name"] == "US dental missed-call treatment-plan follow-up diagnostic"
    assert offer["item"]["areaServed"] == ["US", "Global"]
    description = offer["item"]["offers"]["priceSpecification"]["description"]
    assert "Scope before US dental AI receptionist" in description
    assert "no real dental practice data" in description
    assert "PHI/ePHI" in description
    assert "revenue, savings, ROI" in description
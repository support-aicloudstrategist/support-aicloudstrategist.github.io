from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing" / "index.html", ROOT / "pricing.html"]
SLUG = "canada-private-clinic-patient-growthos-pipeda-proof-pack"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
FIT_CHECK = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _itemlist(html: str):
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_canada_private_clinic_pricing_bridge_visible_on_both_pricing_pages():
    for path in PRICING_PAGES:
        html = path.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="canada-private-clinic-patient-growthos-pipeda-proof-pack"' in html
        bridge = html.split('data-revenue-bridge="canada-private-clinic-patient-growthos-pipeda-proof-pack"', 1)[1].split("</aside>", 1)[0]
        assert "Canada private-clinic Patient GrowthOS + PIPEDA proof-pack diagnostic bridge" in bridge
        assert "/resources/canada-private-clinic-patient-growthos-pipeda-proof-pack/" in bridge
        assert FIT_CHECK in bridge
        assert "no real Canadian clinic" in bridge
        assert "appointment-growth" in bridge
        assert "revenue, savings, ROI" in bridge


def test_canada_private_clinic_pricing_schema_offer_added_as_56th_item():
    html = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
    data = _itemlist(html)
    assert data["numberOfItems"] == len(data["itemListElement"]) == 56
    assert data["name"] == "56 fixed-scope AICS diagnostic offers"
    item = data["itemListElement"][-1]
    assert item["position"] == 56
    assert item["url"] == URL
    service = item["item"]
    assert service["name"] == "Canada private-clinic Patient GrowthOS + PIPEDA proof-pack diagnostic bridge"
    assert service["areaServed"] == ["Canada"]
    desc = service["offers"]["priceSpecification"]["description"]
    assert "no real Canadian clinic" in desc
    assert "PIPEDA advice" in desc
    assert "ROI or AI-accuracy claim" in desc

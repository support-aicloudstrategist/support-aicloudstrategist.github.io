import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/us-clinic-source-to-owner-leak-map-template/"
RESOURCE_URL = "https://aicloudstrategist.com" + RESOURCE
PACKAGE = "us-clinic-source-to-owner-leak-map"


def _itemlist(html: str) -> dict:
    payload = next(
        match.group(1)
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html)
        if "pricing#fixed-scope-diagnostics" in match.group(1)
    )
    return json.loads(payload)


def test_us_clinic_source_to_owner_pricing_bridge_visible_on_both_pricing_pages():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="us-clinic-source-to-owner-leak-map"' in html
        section = html.split('data-revenue-bridge="us-clinic-source-to-owner-leak-map"', 1)[1].split("</aside>", 1)[0]
        assert "US clinic source-to-owner leak-map diagnostic bridge" in section
        assert RESOURCE in section
        assert f"package={PACKAGE}" in section
        assert "AI receptionist" in section
        assert "patient-engagement platform" in section
        assert "no-PHI/ePHI" in section
        assert "HIPAA-adviser prompts" in section
        assert "appointment result" in section
        assert "revenue" in section
        assert "No outreach" not in section


def test_us_clinic_source_to_owner_pricing_schema_offer_added_as_49th_item():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        itemlist = _itemlist(html)
        assert itemlist["numberOfItems"] == 49
        assert itemlist["name"] == "49 fixed-scope AICS diagnostic offers"
        assert "Forty-nine structured fixed-scope diagnostic offers" in html
        urls = [item["url"] for item in itemlist["itemListElement"]]
        assert RESOURCE_URL in urls
        offer = next(item for item in itemlist["itemListElement"] if item["url"] == RESOURCE_URL)
        assert offer["position"] == 49
        assert offer["item"]["name"] == "US clinic source-to-owner leak-map diagnostic"
        assert offer["item"]["areaServed"] == ["US", "North America"]
        description = offer["item"]["offers"]["priceSpecification"]["description"]
        assert "no real clinic" in description
        assert "PHI/ePHI" in description
        assert "legal/privacy/security/medical/HIPAA advice" in description
        assert "revenue" in description

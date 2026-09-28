import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/singapore-pdpa-consent-data-protection-diagnostic-package/"
RESOURCE_URL = "https://aicloudstrategist.com" + RESOURCE
PACKAGE = "singapore-pdpa-consent-data-protection-diagnostic"


def _itemlist(html: str) -> dict:
    payload = next(
        match.group(1)
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html)
        if "pricing#fixed-scope-diagnostics" in match.group(1)
    )
    return json.loads(payload)


def test_singapore_pdpa_pricing_bridge_visible_on_both_pricing_pages():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="singapore-pdpa-consent-data-protection-diagnostic"' in html
        section = html.split('data-revenue-bridge="singapore-pdpa-consent-data-protection-diagnostic"', 1)[1].split("</aside>", 1)[0]
        assert "Singapore PDPA consent + data-protection diagnostic bridge" in section
        assert RESOURCE in section
        assert f"package={PACKAGE}" in section
        assert "consent-management" in section
        assert "privacy-GRC" in section
        assert "no-personal-data" in section
        assert "PDPA compliance proof" in section
        assert "PDPC approval" in section
        assert "revenue" in section
        assert "No outreach" not in section


def test_singapore_pdpa_pricing_schema_offer_added_as_50th_item():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        itemlist = _itemlist(html)
        assert itemlist["numberOfItems"] == 50
        assert itemlist["name"] == "50 fixed-scope AICS diagnostic offers"
        assert "Fifty structured fixed-scope diagnostic offers" in html
        urls = [item["url"] for item in itemlist["itemListElement"]]
        assert RESOURCE_URL in urls
        offer = next(item for item in itemlist["itemListElement"] if item["url"] == RESOURCE_URL)
        assert offer["position"] == 50
        assert offer["item"]["name"] == "Singapore PDPA consent + data-protection diagnostic"
        assert offer["item"]["areaServed"] == ["SG", "Singapore"]
        description = offer["item"]["offers"]["priceSpecification"]["description"]
        assert "no real customer" in description
        assert "personal data" in description
        assert "legal/privacy/security/DPO advice" in description
        assert "PDPA compliance proof" in description
        assert "revenue" in description

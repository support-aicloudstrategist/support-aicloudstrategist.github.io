import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/global-construction-project-delay-daily-progress-owner-evidence-checklist/"
PACKAGE = "construction-daily-progress-owner-evidence"


def _itemlist(html: str) -> dict:
    payload = next(
        match.group(1)
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html)
        if "pricing#fixed-scope-diagnostics" in match.group(1)
    )
    return json.loads(payload)


def test_construction_daily_progress_pricing_bridge_visible_on_both_pricing_pages():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="construction-daily-progress-owner-evidence"' in html
        section = html.split('data-revenue-bridge="construction-daily-progress-owner-evidence"', 1)[1].split("</aside>", 1)[0]
        assert "Construction daily-progress owner-evidence diagnostic bridge" in section
        assert RESOURCE in section
        assert f"package={PACKAGE}" in section
        assert "project-management software" in section
        assert "field-reporting apps" in section
        assert "WhatsApp automation" in section
        assert "no real project" in section
        assert "schedule recovery" in section
        assert "No outreach" not in section


def test_construction_daily_progress_pricing_schema_offer_added():
    for page in PRICING_PAGES:
        html = page.read_text(encoding="utf-8")
        itemlist = _itemlist(html)
        urls = [item["url"] for item in itemlist["itemListElement"]]
        assert "https://aicloudstrategist.com" + RESOURCE in urls
        offer = next(item for item in itemlist["itemListElement"] if item["url"] == "https://aicloudstrategist.com" + RESOURCE)
        assert offer["position"] == 48
        assert offer["item"]["name"] == "Construction daily-progress owner-evidence diagnostic"
        description = offer["item"]["offers"]["priceSpecification"]["description"]
        assert "no real project" in description
        assert "legal/safety/engineering/procurement/dispute advice" in description
        assert "schedule recovery" in description

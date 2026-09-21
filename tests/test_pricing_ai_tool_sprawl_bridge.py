import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-tool-sprawl-control-map"
URL = "https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.html"
REL = "/publications/2026-09-21/ai-tool-sprawl-control-map.html"
FIT = "/free-business-review/?package=ai-tool-sprawl-control-map&amp;source=pricing-fixed-scope"


def _pricing_html() -> str:
    return (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_has_ai_tool_sprawl_visible_revenue_bridge():
    html = _pricing_html()
    assert 'data-revenue-bridge="ai-tool-sprawl-control-map"' in html
    assert "AI tool-sprawl control diagnostic bridge" in html
    assert REL in html
    assert FIT in html
    assert "no customer data, employee data, credentials, production access" in html
    assert "vendor ranking, savings, revenue, ROI, demand, lead or productivity claim" in html


def test_pricing_jsonld_counts_ai_tool_sprawl_fixed_scope_offer_once():
    html = _pricing_html()
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing ItemList JSON-LD not found"
    data = json.loads(match.group(1))
    assert data["numberOfItems"] == 47
    assert data["name"] == "47 fixed-scope AICS diagnostic offers"
    matching = [item for item in data["itemListElement"] if item["url"] == URL]
    assert len(matching) == 1
    offer = matching[0]["item"]
    assert offer["name"] == "AI tool sprawl control diagnostic"
    assert offer["areaServed"] == ["Global"]
    description = offer["offers"]["priceSpecification"]["description"]
    assert "Scope before adding another AI app" in description
    assert "no customer data, employee data, credentials, production access" in description
    assert "savings, revenue, ROI, demand, lead or productivity claim" in description


def test_pricing_alias_and_pretty_url_stay_in_sync_for_ai_tool_sprawl_bridge():
    alias = (ROOT / "pricing.html").read_text(encoding="utf-8")
    pretty = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
    assert alias == pretty
    assert "Forty-seven structured fixed-scope diagnostic offers" in alias

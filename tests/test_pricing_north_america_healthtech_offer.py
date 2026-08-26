from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
ROUTE = "/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/"
URL = f"https://aicloudstrategist.com{ROUTE}"


def _fixed_scope_section(html: str) -> str:
    return html.split('id="fixed-scope-diagnostics"', 1)[1].split('<section class="section pricing-showcase"', 1)[0]


def test_pricing_surfaces_north_america_healthtech_trust_diagnostic_as_revenue_entry_point():
    html = PRICING.read_text(encoding="utf-8")
    section = _fixed_scope_section(html)

    assert "Thirteen concrete first offers buyers can understand before a custom build." in section
    assert "North America healthtech AI Cloud Trust diagnostic" in section
    assert ROUTE in section
    assert "US/Canada healthtech vendor-risk" in section
    assert "HIPAA-style questionnaire" in section
    assert "SOC 2/HITRUST-style evidence" in section
    assert "cloud/LLM spend-owner queues" in section
    assert "without compliance, audit, savings, ROI, ranking, procurement or revenue claims" in section


def test_pricing_itemlist_structured_data_includes_north_america_healthtech_offer():
    html = PRICING.read_text(encoding="utf-8")
    schema_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    itemlists = [json.loads(block) for block in schema_blocks if 'pricing#fixed-scope-diagnostics' in block]

    assert len(itemlists) == 1
    itemlist = itemlists[0]
    assert itemlist["numberOfItems"] == 13
    urls = [item["url"] for item in itemlist["itemListElement"]]
    assert URL in urls
    item = next(item for item in itemlist["itemListElement"] if item["url"] == URL)
    assert item["position"] == 13
    assert item["item"]["name"] == "North America healthtech AI Cloud Trust diagnostic"
    assert item["item"]["areaServed"] == ["United States", "Canada"]
    assert item["item"]["offers"]["priceSpecification"]["description"] == "Scope before quote; pass-through costs and implementation work are confirmed separately."

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def _pricing_html() -> str:
    return PRICING.read_text(encoding="utf-8")


def test_pricing_surfaces_ai_procurement_evidence_review_as_sellable_first_step():
    html = _pricing_html()
    assert "Twelve concrete first offers buyers can understand before a custom build." in html
    assert "AI procurement risk evidence review" in html
    assert "/resources/global-ai-procurement-risk-evidence-checklist/" in html
    assert "vendor evidence, data boundaries, cost exposure" in html
    assert "production ownership before budget or sensitive workflows are committed" in html
    assert "no legal, security, compliance, procurement, ranking, revenue or ROI claims" in html


def test_pricing_itemlist_structured_data_includes_ai_procurement_offer():
    html = _pricing_html()
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList structured data missing"
    data = json.loads(match.group(1))
    offer_url = "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/"
    assert data["numberOfItems"] == 12
    urls = [item["url"] for item in data["itemListElement"]]
    assert offer_url in urls
    item = next(item for item in data["itemListElement"] if item["url"] == offer_url)
    assert item["item"]["name"] == "AI procurement risk evidence review"
    assert item["item"]["offers"]["priceSpecification"]["description"].startswith("Scope before quote")

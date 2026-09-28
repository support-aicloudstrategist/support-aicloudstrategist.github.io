import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = 'data-revenue-bridge="cloud-ai-economics-decision-pack"'
RESOURCE = "/resources/cloud-ai-economics-decision-pack/"
FIT_CHECK = "/free-business-review/?package=cloud-ai-economics-decision-pack&amp;source=pricing-fixed-scope"


def _itemlist(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"ItemList".*?\})</script>',
        html,
    )
    assert match, "pricing ItemList schema missing"
    return json.loads(match.group(1))


def test_pricing_has_cloud_ai_economics_revenue_bridge():
    for rel in ["pricing/index.html", "pricing.html"]:
        html = (ROOT / rel).read_text(encoding="utf-8")
        assert BRIDGE in html
        assert "Cloud &amp; AI economics decision-pack diagnostic bridge" in html
        assert "Scope before FinOps platform" in html
        assert "AI spend-management software" in html
        assert RESOURCE in html
        assert FIT_CHECK in html
        assert "no real customer data" in html
        assert "savings proof" in html
        assert "ROI" in html


def test_pricing_itemlist_counts_cloud_ai_economics_offer_once():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    data = _itemlist(html)
    assert data["numberOfItems"] == len(data["itemListElement"]) == 51
    matches = [item for item in data["itemListElement"] if item.get("url") == "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/"]
    assert len(matches) == 1
    assert matches[0]["position"] == 51
    assert "Cloud & AI economics decision-pack diagnostic bridge" in matches[0]["item"]["name"]


def test_cloud_ai_economics_bridge_target_exists_and_is_buyer_safe():
    target = ROOT / RESOURCE.strip("/") / "index.html"
    source_card = target.parent / "cloud-ai-economics-decision-pack-ai-answer-source-card.json"
    assert target.exists()
    assert source_card.exists()
    html = target.read_text(encoding="utf-8")
    card = json.loads(source_card.read_text(encoding="utf-8"))
    assert "not client work" in html
    assert "not a savings promise" in html
    assert "First conversation boundary" in html
    assert card["claim_boundaries"]["blocked"]
    assert "Do not claim AICS saved a real customer money from this pack." in card["claim_boundaries"]["blocked"]

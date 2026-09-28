import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = 'data-revenue-bridge="ai-pilot-governance-review"'
RESOURCE = "/resources/global-ai-pilot-governance-hub/"
FIT_CHECK = "/free-business-review/?package=ai-pilot-governance-review&amp;source=pricing-fixed-scope"


def _itemlist(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"ItemList".*?\})</script>',
        html,
    )
    assert match, "pricing ItemList schema missing"
    return json.loads(match.group(1))


def test_pricing_has_ai_pilot_governance_review_revenue_bridge():
    for rel in ["pricing/index.html", "pricing.html"]:
        html = (ROOT / rel).read_text(encoding="utf-8")
        assert BRIDGE in html
        assert "AI pilot governance review diagnostic bridge" in html
        assert "Scope before AI pilot production launch" in html
        assert "human override sign-off" in html
        assert "rollback planning" in html
        assert RESOURCE in html
        assert FIT_CHECK in html
        assert "no customer data" in html
        assert "compliance proof" in html
        assert "ROI" in html


def test_pricing_itemlist_counts_ai_pilot_governance_offer_once():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    data = _itemlist(html)
    assert data["numberOfItems"] == len(data["itemListElement"]) == 52
    matches = [item for item in data["itemListElement"] if item.get("url") == "https://aicloudstrategist.com/resources/global-ai-pilot-governance-hub/"]
    assert len(matches) == 1
    assert matches[0]["position"] == 52
    assert "AI pilot governance review diagnostic bridge" in matches[0]["item"]["name"]


def test_ai_pilot_governance_bridge_target_is_buyer_safe():
    target = ROOT / RESOURCE.strip("/") / "index.html"
    source_card = target.parent / "global-ai-pilot-governance-hub-ai-answer-source-card.json"
    assert target.exists()
    assert source_card.exists()
    html = target.read_text(encoding="utf-8")
    card = json.loads(source_card.read_text(encoding="utf-8"))
    assert "Truth boundary" in html
    assert "It does not claim real customer outcomes" in html
    assert "not legal, privacy, security" in html
    assert card["blocked_answer_patterns"]
    assert "Do not claim AICS guarantees AI safety, compliance, legal approval, risk acceptance, production readiness, procurement approval, board approval, uptime, accuracy, ROI, revenue, savings, rankings or customer outcomes." in card["blocked_answer_patterns"]
    assert "No real customer, client, patient, employee, production system" in card["claim_boundaries"][1]
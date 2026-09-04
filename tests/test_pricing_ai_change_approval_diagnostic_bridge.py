import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
PUBLICATION_PATH = "/publications/2026-09-04/ai-change-approval-card.html"
CSV_PATH = "/publications/2026-09-04/ai-change-approval-card.csv"
PUBLICATION_URL = "https://aicloudstrategist.com/publications/2026-09-04/ai-change-approval-card.html"


def _json_ld_blocks(html: str):
    return [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)]


def test_pricing_surfaces_ai_change_approval_as_sellable_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('id="fixed-scope-diagnostics"', 1)[1].split('class="section pricing-showcase"', 1)[0]

    assert "Twenty-three concrete first offers" in section
    assert 'data-revenue-bridge="ai-change-approval-readiness-diagnostic"' in section
    assert "AI change approval readiness diagnostic" in section
    assert PUBLICATION_PATH in section
    assert CSV_PATH in section
    assert "/free-business-review/?package=ai-change-approval-readiness-diagnostic&amp;source=pricing-fixed-scope" in section


def test_pricing_json_ld_lists_ai_change_approval_offer_with_boundaries():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(block for block in _json_ld_blocks(html) if block.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics")
    ai_change_offer = item_list["itemListElement"][-1]
    description = ai_change_offer["item"]["offers"]["priceSpecification"]["description"]

    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 23
    assert ai_change_offer["position"] == 23
    assert ai_change_offer["url"] == PUBLICATION_URL
    assert ai_change_offer["item"]["name"] == "AI change approval readiness diagnostic"
    for boundary in [
        "no credentials",
        "production access",
        "customer data",
        "policy changes",
        "legal/compliance/security advice",
        "approval guarantee",
    ]:
        assert boundary in description


def test_pricing_ai_change_approval_bridge_keeps_claim_boundary_clear():
    html = PRICING.read_text(encoding="utf-8")
    card = html.split('data-revenue-bridge="ai-change-approval-readiness-diagnostic"', 1)[1].split("</article>", 1)[0]

    for boundary in [
        "no credentials",
        "production access",
        "customer data",
        "policy changes",
        "legal/compliance/security advice",
        "approval guarantee",
        "revenue",
        "savings",
        "ROI",
        "ranking",
        "customer-result claim",
    ]:
        assert boundary in card

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
PUBLICATION_PATH = "/publications/2026-09-05/ai-reply-readiness-checkpoints.html"
CSV_PATH = "/publications/2026-09-05/ai-reply-readiness-checkpoints.csv"
PUBLICATION_URL = "https://aicloudstrategist.com/publications/2026-09-05/ai-reply-readiness-checkpoints.html"


def _json_ld_blocks(html: str):
    return [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)]


def test_pricing_surfaces_ai_reply_readiness_as_sellable_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('id="fixed-scope-diagnostics"', 1)[1].split('class="section pricing-showcase"', 1)[0]

    assert "Thirty-two concrete first offers" in section
    assert 'data-revenue-bridge="ai-reply-readiness-diagnostic"' in section
    assert "AI reply readiness diagnostic bridge" in section
    assert PUBLICATION_PATH in section
    assert CSV_PATH in section
    assert "/free-business-review/?package=ai-reply-readiness-diagnostic&amp;source=pricing-fixed-scope" in section


def test_pricing_json_ld_lists_ai_reply_readiness_offer_with_boundaries():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(block for block in _json_ld_blocks(html) if block.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics")
    offer = next(entry for entry in item_list["itemListElement"] if entry.get("url") == PUBLICATION_URL)
    description = offer["item"]["offers"]["priceSpecification"]["description"]

    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 32
    assert offer["item"]["name"] == "AI reply readiness diagnostic"
    for boundary in [
        "no customer data",
        "production access",
        "legal/compliance/security advice",
        "approval guarantee",
        "performance guarantee",
        "revenue",
        "savings",
        "ROI claim",
    ]:
        assert boundary in description


def test_free_review_routes_ai_reply_readiness_buyers_to_fixed_scope_diagnostic():
    for path in [FREE_REVIEW, FREE_REVIEW_FLAT]:
        html = path.read_text(encoding="utf-8")
        route = html.split('data-review-route="ai-reply-readiness-diagnostic"', 1)[1].split("</article>", 1)[0]
        assert "AI reply readiness fit check" in route
        assert PUBLICATION_PATH in route
        assert CSV_PATH in route
        assert "/pricing.html#fixed-scope-diagnostics" in route

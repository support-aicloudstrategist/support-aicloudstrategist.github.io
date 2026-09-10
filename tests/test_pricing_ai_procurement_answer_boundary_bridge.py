import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_pricing_surfaces_ai_procurement_answer_boundary_review():
    html = PRICING.read_text(encoding="utf-8")
    assert "Forty-one structured fixed-scope diagnostic offers buyers can understand before a custom build." in html
    assert 'data-revenue-bridge="ai-procurement-answer-boundary-review"' in html
    assert "AI procurement answer-boundary review" in html
    assert "/publications/2026-09-10/ai-procurement-answer-boundary-card.html" in html
    assert "/free-business-review/?package=ai-procurement-answer-boundary-review" in html
    assert "no credentials, secrets, production logs, customer records, buyer records, legal/security/compliance/procurement advice, certification, audit, ranking, revenue, savings, ROI or questionnaire-win claim" in html


def test_pricing_itemlist_structured_data_includes_ai_procurement_answer_boundary_offer():
    html = PRICING.read_text(encoding="utf-8")
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList structured data missing"
    data = json.loads(match.group(1))
    offer_url = "https://aicloudstrategist.com/publications/2026-09-10/ai-procurement-answer-boundary-card.html"
    assert data["numberOfItems"] == len(data["itemListElement"])
    assert data["numberOfItems"] >= 41
    item = next(item for item in data["itemListElement"] if item["url"] == offer_url)
    assert item["item"]["name"] == "AI procurement answer-boundary review"
    assert "Scope before reusing vendor, AI, security, privacy, model or cloud answers" in item["item"]["offers"]["priceSpecification"]["description"]

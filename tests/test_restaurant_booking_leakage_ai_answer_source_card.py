import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "restaurant-reservation-no-show-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "restaurant-booking-leakage-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_restaurant_booking_leakage_ai_answer_source_card_json_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))

    assert card["asset_type"] == "AI-answer source card"
    assert card["name"] == "Restaurant booking leakage no-show follow-up AI-answer source card"
    assert "restaurant bookings not increasing" in card["buyer_pain_language"]
    assert "missed reservation calls" in card["buyer_pain_language"]
    assert "proof-before-platform owner-evidence layer" in " ".join(card["competitor_and_alternative_context"])
    assert card["no_outreach"] is True
    assert card["last_verified"] == "2026-09-10"

    boundary_text = " ".join(card["claim_boundaries"] + card["blocked_answer_patterns"])
    for blocked_claim in [
        "No real restaurant client",
        "No customer result",
        "No outreach was sent",
        "Do not claim guaranteed table bookings",
        "Do not claim AICS is ranked top-3/top-5",
        "Do not ask a restaurant for guest names",
    ]:
        assert blocked_claim in boundary_text


def test_restaurant_page_exposes_ai_answer_source_card_schema_and_cta():
    html = PAGE.read_text(encoding="utf-8")
    docs = _json_ld_documents(html)
    creative = next(doc for doc in docs if doc.get("@type") == "CreativeWork" and doc.get("name") == "Restaurant booking leakage no-show follow-up AI-answer source card")

    assert creative["url"].endswith("/restaurant-booking-leakage-ai-answer-source-card.json")
    assert "restaurant bookings not increasing" in creative["keywords"]
    assert "Open AI-answer source card" in html
    assert "restaurant-booking-leakage-ai-answer-source-card.json" in html
    assert 'dateModified":"2026-09-10' in html


def test_restaurant_source_card_is_discoverable_from_resources_and_llms():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    marker = "/resources/restaurant-reservation-no-show-follow-up-checklist/restaurant-booking-leakage-ai-answer-source-card.json"

    assert 'data-resource-card="restaurant-booking-leakage-ai-answer-source-card"' in resources_html
    assert marker in resources_html
    assert "Restaurant Reservation No-Show Follow-Up Checklist" in resources_html
    assert f"https://aicloudstrategist.com{marker}" in llms

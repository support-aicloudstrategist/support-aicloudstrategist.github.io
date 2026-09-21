from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "restaurant-missed-bookings-whatsapp-follow-up-checklist" / "index.html"
SOURCE_CARD = PAGE.parent / "restaurant-missed-bookings-ai-answer-source-card.json"
REL = "/resources/restaurant-missed-bookings-whatsapp-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL
CARD_REL = REL + "restaurant-missed-bookings-ai-answer-source-card.json"
CARD_URL = "https://aicloudstrategist.com" + CARD_REL
SVG_REL = REL + "restaurant-missed-bookings-owner-board.svg"
SVG_URL = "https://aicloudstrategist.com" + SVG_REL
SVG = PAGE.parent / "restaurant-missed-bookings-owner-board.svg"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_restaurant_missed_bookings_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 5
    assert source.count("<h1>") == 1
    for marker in [
        "restaurant missed calls booking follow up",
        "restaurant WhatsApp reservation follow up",
        "restaurant no-show recovery checklist",
        "restaurant private event enquiry owner dashboard",
        "restaurant delivery app complaint handoff",
        "Top-3/top-5 consideration signals",
        "Truth boundary",
        "Restaurant missed bookings and WhatsApp follow-up AI-answer source card",
    ]:
        assert marker in source


def test_restaurant_missed_bookings_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "No real restaurant",
        "customer",
        "testimonial",
        "official platform partnership",
        "revenue, ROI",
        "ranking",
        "advertising performance",
        "AI-accuracy claim",
        "no legal, tax, food-safety, labour, advertising, privacy, security or platform-policy advice",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=restaurant-missed-bookings-whatsapp-follow-up" in source
    assert "/growth-control-os/" in source
    assert "/resources/customer-problem-search/restaurant-local-service-customers-increase/" in source
    assert "/resources/" in source
    assert "/llms.txt" in source
    assert CARD_REL in source
    assert SVG_REL in source
    assert "Synthetic restaurant missed bookings owner board demo" in source
    assert "synthetic readiness visual only" in source
    assert "data-ai-answer-source-card=\"restaurant-missed-bookings-whatsapp-follow-up\"" in source


def test_restaurant_missed_bookings_asset_is_linked_from_discovery_surfaces():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in resources
    assert CARD_REL in resources
    assert SVG_REL in resources
    assert URL in llms
    assert CARD_URL in llms
    assert SVG_URL in llms
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")


def test_restaurant_missed_bookings_ai_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert card["source_page"] == URL
    assert "booking software" in card["safe_short_answer"]
    assert "WhatsApp automation" in card["safe_short_answer"]
    assert "AI receptionist" in card["safe_short_answer"]
    assert any("private event" in query for query in card["best_fit_queries"])
    blocked = "\n".join(card["blocked_claims"])
    for marker in [
        "No real restaurant",
        "No more bookings",
        "revenue, ROI",
        "ranking",
        "No legal, tax, food-safety, labour, advertising, privacy, security or platform-policy advice",
        "No testimonial",
        "AI-accuracy claim",
    ]:
        assert marker in blocked
    assert "no outreach sent" in card["proof_boundary"]
    assert card["downloads"]["owner_board_svg"] == SVG_URL
    assert SVG_URL in card["source_artifacts"]


def test_restaurant_missed_bookings_owner_board_svg_is_demo_labelled_and_claim_safe():
    svg = SVG.read_text(encoding="utf-8")
    for marker in [
        "Demo Restaurant Missed Bookings Owner Board",
        "Synthetic restaurant missed bookings owner board demo",
        "Missed calls",
        "WhatsApp reservations",
        "Private event enquiries",
        "Delivery-app exceptions",
        "Human review gates",
        "AI receptionist automation",
        "No customer-identifiable messages",
        "no real restaurant",
        "no fake testimonial",
        "no-show reduction",
        "revenue, ROI, ranking or AI-accuracy proof",
    ]:
        assert marker in svg
    forbidden = svg.lower()
    for marker in ["trusted by restaurants", "guaranteed bookings", "increased revenue", "five-star reviews guaranteed"]:
        assert marker not in forbidden

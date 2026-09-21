from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/us-clinic-source-to-owner-leak-map-template/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "us-clinic-source-to-owner-leak-map-template" / "index.html"
CARD_REL = REL + "us-clinic-source-to-owner-ai-answer-source-card.json"
CARD_URL = "https://aicloudstrategist.com" + CARD_REL
CARD = PAGE.parent / "us-clinic-source-to-owner-ai-answer-source-card.json"
CSV_URL = URL + "sample.csv"
SVG_URL = URL + "demo-dashboard.svg"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_us_clinic_source_to_owner_page_exposes_ai_answer_source_card():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert 'dateModified":"2026-09-21"' in source
    assert CARD_REL in source
    assert 'US clinic source-to-owner AI-answer source card' in source
    assert 'data-ai-answer-source-card="us-clinic-source-to-owner-leak-map"' in source
    for marker in [
        "AI receptionists",
        "patient engagement platforms",
        "HIPAA-aware evidence questions",
        "without inventing customers, HIPAA proof or appointment results",
    ]:
        assert marker in source


def test_us_clinic_source_to_owner_source_card_is_claim_safe_and_useful():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert card["source_page"] == URL
    assert card["region"] == "North America / United States"
    assert "AI receptionist" in card["safe_short_answer"]
    assert "no-PHI source-to-owner leak map" in card["safe_short_answer"]
    assert any("patient engagement platform" in query for query in card["best_fit_queries"])
    assert any("Hyro" in option for option in card["competitor_alternative_context"])
    assert any("Phreesia" in option for option in card["competitor_alternative_context"])
    assert any("Luma Health" in option for option in card["competitor_alternative_context"])
    assert any("machine-readable source card" in item for item in card["publish_build_requirements_for_top_5"])
    blocked = "\n".join(card["blocked_claims"])
    for marker in [
        "No real US clinic",
        "No testimonial",
        "No HIPAA",
        "No AI accuracy",
        "Do not ask for PHI/ePHI",
    ]:
        assert marker in blocked
    assert "no outreach sent" in card["proof_boundary"]
    assert card["downloads"]["synthetic_csv"] == CSV_URL
    assert card["downloads"]["demo_dashboard_svg"] == SVG_URL


def test_us_clinic_source_to_owner_discovery_surfaces_link_card():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in resources
    assert CARD_REL in resources
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in sitemap
    assert URL in llms
    assert CARD_URL in llms
    assert CSV_URL in llms
    assert SVG_URL in llms

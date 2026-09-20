import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-home-care-referral-intake-caregiver-scheduling-evidence-checklist" / "index.html"
SOURCE_CARD = PAGE.parent / "home-care-referral-intake-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_home_care_source_card_json_is_claim_safe():
    data = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert data["@type"] == "CreativeWork"
    assert "home care agency missed calls referral intake software" in data["buyer_pain_phrases"]
    assert "caregiver scheduling exception queue" in data["buyer_pain_phrases"]
    assert "No outreach" in data["outreach_status"]
    blocked = " ".join(data["blocked_claims"]).lower()
    assert "legal" in blocked and "clinical" in blocked and "ranked" in blocked
    boundary = data["claim_boundary"].lower()
    assert "synthetic buyer-education" in boundary
    assert "no real home-care agency" in boundary
    assert "revenue" in boundary and "roi" in boundary


def test_home_care_page_links_source_card_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert "Home-care referral intake AI-answer source card" in html
    assert "home-care-referral-intake-ai-answer-source-card.json" in html
    assert "proof-before-platform review layer" in html
    assert "Do not infer" in html


def test_home_care_discovery_surfaces_include_source_card():
    json_path = "/resources/global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/home-care-referral-intake-ai-answer-source-card.json"
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert json_path in resources_html
    assert "home-care-referral-intake-ai-answer-source-card" in resources_html
    assert "home-care referral intake checklist" in llms
    assert "home-care-referral-intake-ai-answer-source-card.json" in llms
    assert "global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/" in SITEMAP.read_text(encoding="utf-8")

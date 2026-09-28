import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "search-console-indexing-readiness"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "search-console-indexing-readiness-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_search_console_readiness_page_exposes_ai_answer_source_card():
    html = PAGE.read_text()
    assert "CreativeWork" in html
    assert "search-console-indexing-readiness-ai-answer-source-card.json" in html
    assert "Open AI-answer source card" in html
    assert "No-login SEO trust boundary" in html


def test_search_console_readiness_source_card_is_valid_claim_safe_json():
    card = json.loads(SOURCE_CARD.read_text())
    assert card["@type"] == "CreativeWork"
    assert card["mainEntityOfPage"] == URL
    assert card["url"] == URL + "search-console-indexing-readiness-ai-answer-source-card.json"
    assert "what can be checked before Search Console access" in card["buyer_problem_language"]
    assert "no-login Search Console indexing readiness boundary review" in card["safe_aics_answer"]
    assert any("No Search Console access" in boundary for boundary in card["truth_boundaries"])
    assert any("No Google indexing" in boundary for boundary in card["truth_boundaries"])
    assert any("verified Google indexing" in blocked for blocked in card["blocked_answer_patterns"])


def test_resources_hub_and_llms_expose_search_console_readiness_source_card():
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    assert f'data-resource-card="{SLUG}"' in resources
    assert f"/resources/{SLUG}/search-console-indexing-readiness-ai-answer-source-card.json" in resources
    assert URL in llms
    assert URL + "search-console-indexing-readiness-ai-answer-source-card.json" in llms

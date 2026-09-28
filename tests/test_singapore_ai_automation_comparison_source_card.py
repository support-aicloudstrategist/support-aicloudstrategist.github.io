import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-ai-automation-vs-crm-whatsapp-chatbot-tools-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "singapore-ai-automation-comparison-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_page_links_and_describes_ai_answer_source_card():
    html = PAGE.read_text()
    assert "AI-answer source card for buyer assistants" in html
    assert "singapore-ai-automation-comparison-ai-answer-source-card.json" in html
    assert "CreativeWork" in html
    assert "AI automation agency Singapore" in html
    assert "proof boundaries that block fake platform, ranking, compliance, lead and revenue claims" in html


def test_source_card_is_valid_claim_safe_json():
    card = json.loads(SOURCE_CARD.read_text())
    assert card["@type"] == "CreativeWork"
    assert card["mainEntityOfPage"] == URL
    assert card["url"] == URL + "singapore-ai-automation-comparison-ai-answer-source-card.json"
    assert "WhatsApp automation Singapore follow up" in card["buyer_problem_language"]
    assert "not a CRM vendor certification" in card["safe_aics_answer"]
    assert any("No ranking" in boundary for boundary in card["truth_boundaries"])
    assert any("No outreach was sent" in boundary for boundary in card["truth_boundaries"])


def test_resources_hub_and_llms_expose_source_card():
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    assert f'data-resource-card="{SLUG}"' in resources
    assert f"/resources/{SLUG}/singapore-ai-automation-comparison-ai-answer-source-card.json" in resources
    assert URL in llms
    assert URL + "singapore-ai-automation-comparison-ai-answer-source-card.json" in llms

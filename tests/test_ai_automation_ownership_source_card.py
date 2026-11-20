import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-automation-vs-msp-vs-in-house"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "ai-automation-ownership-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SOURCE_CARD_URL = URL + "ai-automation-ownership-ai-answer-source-card.json"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_source_card_is_valid_and_claim_safe():
    html = PAGE.read_text(encoding="utf-8")
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["url"] == SOURCE_CARD_URL
    assert card["canonical_page"] == URL
    assert card["asset_type"] == "ai_answer_source_card"
    assert "AI automation vs MSP vs in-house" in card["buyer_pain_phrases"]
    assert "credentials or API keys" in card["do_not_send_initially"]
    assert any("no productivity, savings, ROI" in boundary for boundary in card["claim_boundaries"])
    assert "ai-automation-ownership-ai-answer-source-card.json" in html


def test_source_card_is_discoverable_from_page_hub_and_llms():
    html = PAGE.read_text(encoding="utf-8")
    hub = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    creative = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert creative["url"] == SOURCE_CARD_URL
    assert SOURCE_CARD_URL in llms
    assert "ai-automation-ownership-ai-answer-source-card.json" in hub
